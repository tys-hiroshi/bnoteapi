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
from pprint import pprint
from distutils.util import strtobool

configFile = "app_config.yml"
config = Config(configFile).content
ACCOUNT_NAME = config['API_CONFIG']['AZURE_INFO']['ACCOUNT_NAME']
ACCOUNT_KEY = config['API_CONFIG']['AZURE_INFO']['ACCOUNT_KEY']
CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix=core.windows.net".format(ACCOUNT_NAME, ACCOUNT_KEY)
UPLOAD_CONTAINER_NAME = config['API_CONFIG']['AZURE_INFO']['UPLOAD_CONTAINER_NAME']
AZURE_INFO_CHUNK_SIZE_BYTES = int(config['API_CONFIG']['AZURE_INFO']['CHUNK_SIZE_BYTES'])
BSV_INFO_CHUNK_SIZE_BYTES = int(config['API_CONFIG']['BSV_INFO']['CHUNK_SIZE_BYTES'])

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
    # {
    #   "code": 0,
    #   "encrypt_hex": "0485f17ac943cc89b8625431a49f79d58d5593594b5daebe2feb604d0671409157b730176c143373472bc7368225d133a46b51648a794a7d1b4347e5b4222b2bb50cd003f816ca562437379282cf949232c7f78305baf2165303e4fe0cacf74c059595dcdae6",
    #   "file_id": "20200713232737_a1643b1db443499c806514a71980d55b"
    # }
    try:
        ## NOTE: 多分引数では値が取れないので。なぜかは知らない
        privatekey_wif = request.form["privatekey_wif"]
        public_key_hex = request.form["public_key_hex"]
        on_chain = strtobool(request.form["on_chain"])
        
        req_file = file

        stream = req_file.stream
        #img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
        app.app.logger.info("allwed_file(req_file.filename)")
        app.app.logger.info(allwed_file(req_file.filename))
        app.app.logger.info("req_file.filename")
        app.app.logger.info(req_file.filename)
        # ファイル名がなかった時の処理
        if req_file.filename == '':
            return {}, 400
        # ファイルのチェック
        if req_file and allwed_file(req_file.filename):
            fileUtil = FileUtil()
            filename = fileUtil.convert_filename_jpeg_to_jpg(req_file.filename)
            file_extention = fileUtil.get_file_extention(filename)
            # 1. divid upload file
            # 2. get divid file array
            divideStream = DivideStream()
            if on_chain:
                chunkSize = BSV_INFO_CHUNK_SIZE_BYTES
            else:
                chunkSize = AZURE_INFO_CHUNK_SIZE_BYTES

            #chunkSize = 100000  #100kb
            #chunkSize = 81  ## for Test
            # 100000 Byte = 100kb で分割
            dividedStreamList = divideStream.divide_stream(stream, chunkSize)

            # 3. generate random index array
            genRandom = GenRandom()
            random_index_list = genRandom.generate_random_index(len(dividedStreamList))
            # 4. divided file array is numbering random index
            ## random_index_list の上から順にValue(index)に対応する dividedStreamList のIndexのValueをUploadする

            azUploader = AzureUploader(CONNECTION_STRING, UPLOAD_CONTAINER_NAME)
            azUploader.make_container_retry()
            dt_now = datetime.datetime.now()
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
                    uploader = polyglot.Upload(wif=privatekey_wif, network='test')
                    req_file_bytearray = bytearray(dividedStreamList[i])
                    app.app.logger.info(len(req_file_bytearray))
                    media_type = uploader.get_media_type_for_file_name(file_name)  ## WARNING: .jpeg is Error!!!!!
                    encoding = uploader.get_encoding_for_file_name(file_name)
                    rawtx = uploader.b_create_rawtx_from_binary(req_file_bytearray, media_type, encoding, file_name)
                    tx_id = uploader.send_rawtx(rawtx)  ##TODO: retry or wait. リクエストが早すぎて失敗することがあるので
                    tx_id_list.append(tx_id)
                else:
                    ## 6-2. on cloud
                    # Create a blob client using the local file name as the name for the blob
                    blob_client = blob_service_client.get_blob_client(UPLOAD_CONTAINER_NAME, file_name)

                    print("\nUploading to Azure Storage as blob:\n\t" + file_name)

                    # Upload the created file
                    blob_client.upload_blob(dividedStreamList[i])  ## i is random index

                index += 1
            
            ## when divided teststring.txt ( chunkSize = 81 ), then upload file is random.

            # 5. encrypt generate random index array to string
            maped_random_index_list = map(str, random_index_list)  #mapで要素すべてを文字列に
            random_index_str = ','.join(maped_random_index_list)
            cryptUtil = CryptUtil()
            
            # ### test genearte key
            # genkey = cryptUtil.generateEciesKey()
            # secret_key = genkey.to_hex()
            # public_key_hex = genkey.public_key.to_hex()
            # ### test genearte key
            
            encrypt_str_hex = cryptUtil.encrypt(public_key_hex, random_index_str.encode()).hex()
            #decrypt_str = cryptUtil.decrypt(secret_key, encrypt_str)  ##it's success (return is bytes)
            
            # 6. upload files

            #loop = asyncio.get_event_loop()
            # containerName = "containertest"
            # azUploader = AzureUploader(CONNECTION_STRING, containerName)
            # azUploader.make_container_retry()
            # dt_now = datetime.datetime.now()
            # dateTimeNowStr = dt_now.strftime('%Y%m%d%H%M%S')
            # file_name = "upload{}_{}.{}".format(dateTimeNowStr, str(uuid.uuid4().hex), file_extention) 
            # # Create the BlobServiceClient object which will be used to create a container client
            # blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
            # # Create a blob client using the local file name as the name for the blob
            # blob_client = blob_service_client.get_blob_client(container=containerName, blob=file_name)

            # print("\nUploading to Azure Storage as blob:\n\t" + file_name)

            # # Upload the created file
            # blob_client.upload_blob(file)


            # 7. save No.5 string in server


            # 危険な文字を削除（サニタイズ処理）
            #filename = secure_filename(req_file.filename)

            # privatekey_wif = request.form["privatekey_wif"]
            # uploader = polyglot.Upload(privatekey_wif, 'test')
            # app.app.logger.info(uploader.network)
            # req_file_bytearray = bytearray(stream.read())
            # #app.app.logger.info(len(req_file_bytearray))
            # #transaction = uploader.bcat_parts_send_from_binary(req_file_bytearray)
            # media_type = uploader.get_media_type_for_file_name(filename)  ## WARNING: .jpeg is Error!!!!!
            # app.app.logger.info(media_type)
            # encoding = uploader.get_encoding_for_file_name(filename)
            # app.app.logger.info(encoding)
            # #print(media_type)
            # #print(encoding)
            # rawtx = uploader.b_create_rawtx_from_binary(req_file_bytearray, media_type, encoding, filename)
            # app.app.logger.info(rawtx)
            # txid = uploader.send_rawtx(rawtx)
            # #transaction = uploader.upload_b(filepath)
            # #['5cd293a25ecf0b346ede712ceb716f35f1f78e2c5245852eb8319e353780c615']
            # app.app.logger.info(txid)
            ### encrypt_str = encrypt_str.decode('utf-8') #it's error
            #aaa = bytes(encrypt_str_hex, 'utf-8')
            
            # #it's decrypt process.
            # encrypt_str_bytes = bytes.fromhex(encrypt_str_hex)
            # decrypt_str_bytes = cryptUtil.decrypt(secret_key, encrypt_str_bytes)
            # decrypt_str = decrypt_str_bytes.decode('utf-8')

            return ResponseUploadToCloudModel(code=0, file_id=file_id, encrypt_hex=encrypt_str_hex, tx_id_list=tx_id_list).to_dict(), 200
        else:
            return ResponseUploadToCloudModel(code=400, file_id="").to_dict(), 400
    except Exception as e:
        app.app.logger.error("!!Exception!!")
        app.app.logger.error(e)
        #print(e)
        return e, 500
