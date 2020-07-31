import connexion
import six

from openapi_server.models.response_uploadtocloud_model import ResponseUploadToCloudModel  # noqa: E501
from openapi_server import util

import polyglot
import os
from flask import request

from openapi_server import app

from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions, ContainerClient, BlobClient
import asyncio

from openapi_server.utils.Config import Config
from openapi_server.utils.AzureUploader import AzureUploader
import uuid
import datetime
from openapi_server.utils.DivideFile import DivideFile
from openapi_server.utils.DivideStream import DivideStream
from openapi_server.utils.GenRandom import GenRandom
from openapi_server.utils.CryptUtil import CryptUtil
from openapi_server.utils.FileUtil import FileUtil
from openapi_server.utils.FileUploaderOnChain import FileUploaderOnChain
from pprint import pprint
from distutils.util import strtobool
import hashlib
import time

configFile = "app_config.yml"
config = Config(configFile).content
ACCOUNT_NAME = config['API_CONFIG']['AZURE_INFO']['ACCOUNT_NAME']
ACCOUNT_KEY = config['API_CONFIG']['AZURE_INFO']['ACCOUNT_KEY']
CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix=core.windows.net".format(ACCOUNT_NAME, ACCOUNT_KEY)
UPLOAD_CONTAINER_NAME = config['API_CONFIG']['AZURE_INFO']['UPLOAD_CONTAINER_NAME']
AZURE_INFO_CHUNK_SIZE_BYTES = int(config['API_CONFIG']['AZURE_INFO']['CHUNK_SIZE_BYTES'])
BSV_INFO_CHUNK_SIZE_BYTES = int(config['API_CONFIG']['BSV_INFO']['CHUNK_SIZE_BYTES'])
BSV_INFO_NETWORK = config['API_CONFIG']['BSV_INFO']['NETWORK']

MAX_BSV_SIZE_BYTES = 100000

# アップロードされる拡張子の制限
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'txt', 'md', 'json', 'yaml', 'yml'])

def allwed_file(filename):
    # .があるかどうかのチェックと、拡張子の確認
    # OKなら１、だめなら0
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def api_uploadtocloud(file=None, privatekey_wif = None, public_key_hex=None, on_chain = None):  # noqa: E501
    """upload file on Cloud

    convert mnemonic words to wif, asset on Bitcoin SV. # noqa: E501

    :param privatekey_wif: 
    :type privatekey_wif: str
    :param file: 
    :type file: str
    :param public_key_hex: 
    :type public_key_hex: str
    :param on_chain: 
    :type on_chain: boolean
    

    :rtype: ResponseUploadToCloudModel
    """
    try:
        ## NOTE: 多分引数では値が取れないので。なぜかは知らない
        privatekey_wif = request.form["privatekey_wif"]
        public_key_hex = request.form["public_key_hex"]
        on_chain = strtobool(request.form["on_chain"])
        
        req_file = file

        stream = req_file.stream
        app.app.logger.info("allwed_file(req_file.filename)")
        app.app.logger.info(allwed_file(req_file.filename))
        app.app.logger.info("req_file.filename")
        app.app.logger.info(req_file.filename)
        # ファイル名がなかった時の処理
        if req_file.filename == '':
            return ResponseUploadToCloudModel(code=400, file_id="").to_dict(), 400
        # ファイルのチェック
        if req_file and allwed_file(req_file.filename):
            fileUtil = FileUtil()
            filename = fileUtil.convert_filename_jpeg_to_jpg(req_file.filename)
            file_extention = fileUtil.get_file_extension(filename)
            # 1. divid upload file
            # 2. get divid file array
            divideStream = DivideStream()
            # ex. 100000 Byte = 100kb で分割
            if on_chain:
                chunkSize = BSV_INFO_CHUNK_SIZE_BYTES
            else:
                chunkSize = AZURE_INFO_CHUNK_SIZE_BYTES
            
            dividedStreamList = divideStream.divide_stream(stream, chunkSize)

            # 3. generate random index array
            genRandom = GenRandom()
            random_index_list = genRandom.generate_random_index(len(dividedStreamList))
            # 4. divided file array is numbering random index
            ## random_index_list の上から順にValue(index)に対応する dividedStreamList のIndexのValueをUploadする

            dt_now = datetime.datetime.now()
            blob_service_client = None

            fileUploaderOnChain = FileUploaderOnChain(privatekey_wif, BSV_INFO_NETWORK)
            if not on_chain:
                azUploader = AzureUploader(CONNECTION_STRING, UPLOAD_CONTAINER_NAME)
                azUploader.make_container_retry()
                # Create the BlobServiceClient object which will be used to create a container client
                blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

            uid = str(uuid.uuid4().hex)
            index = 0
            dateTimeNowStr = dt_now.strftime('%Y%m%d%H%M%S')
            file_id = "{}_{}".format(dateTimeNowStr, uid)
            tx_id_list = []
            for i in random_index_list:
                file_name = "{}_{}.{}".format(file_id, str(index).zfill(6), file_extention)

                if on_chain:
                    ## 6-1. on blockchain
                    file_bytearray = bytearray(dividedStreamList[i])
                    tx_id = fileUploaderOnChain.upload_file_bytearray(file_name, file_bytearray)
                    tx_id_list.append(tx_id)
                else:
                    ## 6-2. on cloud
                    # Create a blob client using the local file name as the name for the blob
                    blob_client = blob_service_client.get_blob_client(UPLOAD_CONTAINER_NAME, file_name)

                    app.app.logger.info("\nUploading to Azure Storage as blob:\n\t" + file_name)

                    # Upload the created file
                    blob_client.upload_blob(dividedStreamList[i])  ## i is random index

                index += 1

            app.app.logger.info("5. encrypt generate random index array to string")
            # 5. encrypt generate random index array to string
            maped_random_index_list = map(str, random_index_list)  #mapで要素すべてを文字列に
            random_index_str = ','.join(maped_random_index_list)
            cryptUtil = CryptUtil()
            
            encrypt_str_hex = cryptUtil.encrypt(public_key_hex, random_index_str.encode()).hex()

            # 7. calculate file hash and write hash on BlockChain.
            #calculate file hash
            hash = hashlib.new('ripemd160')
            hash.update(bytearray(stream))
            ripemd160_hash = hash.hexdigest()

            file_name = f"{file_id}_ripemd160_hash"
            
            hash_txid = fileUploaderOnChain.upload_text_file(file_name=file_name, message=ripemd160_hash)
            tx_id_list.append(hash_txid)
            return ResponseUploadToCloudModel(code=0, file_id=file_id, encrypt_hex=encrypt_str_hex, tx_id_list=tx_id_list).to_dict(), 200
        else:
            return ResponseUploadToCloudModel(code=400, file_id="").to_dict(), 400
    except Exception as e:
        app.app.logger.error("!!Exception!!")
        app.app.logger.error(e)
        #print(e)
        return e, 500
