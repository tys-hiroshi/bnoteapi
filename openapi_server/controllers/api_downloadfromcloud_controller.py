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
    
    blob_list = container.list_blobs(file_id)
    for blob in blob_list:
        print(blob.name + '\n')
    # blob = BlobClient.from_connection_string(conn_str=CONNECTION_STRING container_name="my_container", blob_name="my_blob")

    # blob_data = blob.download_blob()
    
    # downloadFilename = upload_filename
    # #headers["Content-Disposition"] = 'attachment; filename=' + downloadFilename
    # header_ContentDisposition = 'attachment; filename=' + downloadFilename
    # mimetype = upload_mimetype
    
    # response = app.app.make_response(data)
    # response.data = data
    # response.headers["Content-Disposition"] = header_ContentDisposition
    # response.mimetype = mimetype
    return {}, 200
