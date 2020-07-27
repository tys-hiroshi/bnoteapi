import connexion
import six
  # noqa: E501
from openapi_server import util
from flask import request

from openapi_server import app, mongo, bootstrap
import requests
import binascii
from azure.storage.blob import BlobClient

from openapi_server.utils.Config import Config
from azure.storage.blob import BlobServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions, ContainerClient, BlobClient
from openapi_server.utils.DivideStream import DivideStream
import io
from openapi_server.utils.CryptUtil import CryptUtil
from openapi_server.utils.FileUtil import FileUtil

from io import BytesIO

configFile = "app_config.yml"
config = Config(configFile).content
ACCOUNT_NAME = config['API_CONFIG']['AZURE_INFO']['ACCOUNT_NAME']
ACCOUNT_KEY = config['API_CONFIG']['AZURE_INFO']['ACCOUNT_KEY']
CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix=core.windows.net".format(ACCOUNT_NAME, ACCOUNT_KEY)
UPLOAD_CONTAINER_NAME = config['API_CONFIG']['AZURE_INFO']['UPLOAD_CONTAINER_NAME']

def api_downloadfromcloud(file_id=None, secret_key_hex=None, encrypt_hex=None):  # noqa: E501
    container = ContainerClient.from_connection_string(CONNECTION_STRING, UPLOAD_CONTAINER_NAME)
    # file_id = request.form["file_id"] ## 多分引数ではだめだったと。
    # secret_key_hex = request.form["secret_key_hex"]
    # encrypt_hex = request.form["encrypt_hex"]
    
    #it's decrypt process.
    cryptUtil = CryptUtil()

    encrypt_str_bytes = bytes.fromhex(encrypt_hex)
    decrypt_str_bytes = cryptUtil.decrypt(secret_key_hex, encrypt_str_bytes)
    decrypt_str = decrypt_str_bytes.decode('utf-8')
    random_index_list = decrypt_str.split(',')

    blob_list = container.list_blobs(file_id)
    random_stream_list = []
    stream_list = []
    file_extension = ""
    fileUtil = FileUtil()
    for blob in blob_list:
        filename = fileUtil.convert_filename_jpeg_to_jpg(blob.name)
        file_extension = fileUtil.get_file_extention(filename)
        
        print(blob.name + '\n')
        blob = BlobClient.from_connection_string(
            CONNECTION_STRING, UPLOAD_CONTAINER_NAME, blob.name)

        blob_data = blob.download_blob().readall() # StorageStreamDownloader
        random_stream_list.append(blob_data)

    sort_list = []
    for idx, val in enumerate(random_index_list):
        sort_list.append(dict(idx= idx, val=val))

    sorted_list = sorted(sort_list, key=lambda x:x['val'])
    for item  in sorted_list:
        stream_list.append(random_stream_list[item["idx"]])

    ## https://docs.microsoft.com/en-us/python/api/azure-storage-file-datalake/azure.storage.filedatalake.storagestreamdownloader?view=azure-python

    divideStream = DivideStream()
    #divideStream.join_stream(stream_list, "join_file")
    
    bs = io.BytesIO()
    divideStream.join_stream_to_bytes(stream_list, bs)

    # filePath = "join_file.jpg"
    # with open(filePath, 'wb') as saveFile:
    #     saveFile.write(bs.getbuffer())
    #     #saveFile.write(bs.read())
    #     saveFile.flush()
    #https://stackoverflow.com/questions/54137790/how-do-i-convert-from-io-bytesio-to-a-bytes-like-object-in-python3-6
    
    #bs.seek(0)
    #joined_stream_to_bytes = bs.read()
    # or 
    joined_stream_to_bytes = bs.getvalue()
    
    downloadFilename = "{}.{}".format(file_id, file_extension)
    # #headers["Content-Disposition"] = 'attachment; filename=' + downloadFilename
    header_ContentDisposition = 'attachment; filename=' + downloadFilename
    mimetype = fileUtil.get_media_type_for_extension(file_extension)
    response = app.app.make_response(joined_stream_to_bytes)
    response.data = joined_stream_to_bytes
    response.headers["Content-Disposition"] = header_ContentDisposition
    response.mimetype = mimetype


    return response, 200
