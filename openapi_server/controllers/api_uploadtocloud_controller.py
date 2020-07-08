import connexion
import six

from openapi_server.models.request_add_address_model import RequestAddAddressModel  # noqa: E501
from openapi_server.models.request_mnemonic_model import RequestMnemonicModel  # noqa: E501
from openapi_server.models.request_upload_text_model import RequestUploadTextModel  # noqa: E501
from openapi_server.models.response_add_address_model import ResponseAddAddressModel  # noqa: E501
from openapi_server.models.response_mnemonic_model import ResponseMnemonicModel  # noqa: E501
from openapi_server.models.response_tx_model import ResponseTxModel  # noqa: E501
from openapi_server.models.response_upload_model import ResponseUploadModel  # noqa: E501
from openapi_server.models.response_upload_text_model import ResponseUploadTextModel  # noqa: E501
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
from pprint import pprint

configFile = "app_config.yml"
config = Config(configFile).content
ACCOUNT_NAME = config['API_CONFIG']['AZURE_INFO']['ACCOUNT_NAME']
ACCOUNT_KEY = config['API_CONFIG']['AZURE_INFO']['ACCOUNT_KEY']
CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix=core.windows.net".format(ACCOUNT_NAME, ACCOUNT_KEY)

# アップロードされる拡張子の制限
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'txt', 'md', 'json', 'yaml', 'yml'])

def allwed_file(filename):
    # .があるかどうかのチェックと、拡張子の確認
    # OKなら１、だめなら0
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_extention(filename):
    return filename.rsplit('.', 1)[1].lower()

def convert_filename_jpeg_to_jpg(filename):
    basename_without_ext = filename.split('.')[0]
    print("basename_without_ext")
    print(basename_without_ext)
    extension = filename.rsplit('.', 1)[1].lower()
    print("extension")
    print(extension)
    if extension == "jpeg":
        extension = "jpg"
    newfilename = f"{basename_without_ext}.{extension}"
    return newfilename

def api_uploadtocloud(file=None, privatekey_wif = None):  # noqa: E501
    """upload file on Cloud

    convert mnemonic words to wif, asset on Bitcoin SV. # noqa: E501

    :param file: 
    :type file: str

    :rtype: ResponseUploadToCloudModel
    """
    
    try:
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
            filename = convert_filename_jpeg_to_jpg(req_file.filename)
            file_extention = get_file_extention(filename)
            # 1. divid upload file
            # 2. get divid file array
            divideStream = DivideStream()
            chunkSize = 81
            # 300000 Byte で分割
            dividedStreamList = divideStream.divide_stream(stream, chunkSize)

            # 3. generate random index array
            genRandom = GenRandom()
            random_index_list = genRandom.generate_random_index(len(dividedStreamList))
            # 4. divided file array is numbering random index
            ## random_index_list の上から順にValue(index)に対応する dividedStreamList のIndexのValueをUploadする
            containerName = "containertest"
            azUploader = AzureUploader(CONNECTION_STRING, containerName)
            azUploader.make_container_retry()
            dt_now = datetime.datetime.now()
            # Create the BlobServiceClient object which will be used to create a container client
            blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
            uid = str(uuid.uuid4().hex)
            index = 0
            for i in random_index_list:
                dateTimeNowStr = dt_now.strftime('%Y%m%d%H%M%S')
                file_name = "upload{}_{}_{}.{}".format(dateTimeNowStr, uid, str(index).zfill(6), file_extention)
                # Create a blob client using the local file name as the name for the blob
                blob_client = blob_service_client.get_blob_client(container=containerName, blob=file_name)

                print("\nUploading to Azure Storage as blob:\n\t" + file_name)

                # Upload the created file
                blob_client.upload_blob(dividedStreamList[i])
                index += 1
            
            ## when divided teststring.txt ( chunkSize = 81 ), then upload file is random.

            # 5. encrypt generate random index array to string
            maped_random_index_list = map(str, random_index_list)  #mapで要素すべてを文字列に
            random_index_str = ','.join(maped_random_index_list)

            cryptUtil = CryptUtil()
            generate_key = cryptUtil.generateEciesKey()
            secret_key = generate_key.to_hex()
            public_key = generate_key.public_key.to_hex()
            encrypt_str = cryptUtil.encrypt(public_key, random_index_str.encode())
            decrypt_str = cryptUtil.decrypt(secret_key, encrypt_str)  ##it's success (return is bytes)
            
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

            ## 6-1. on blockchain

            ## 6-2. on cloud


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
            txid = -1
            return ResponseUploadModel(0, txid).to_dict(), 200
        else:
            return ResponseUploadModel(400, "").to_dict(), 400
    except Exception as e:
        app.app.logger.error("!!Exception!!")
        app.app.logger.error(e)
        #print(e)
        return e, 500
