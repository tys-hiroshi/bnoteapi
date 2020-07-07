from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions, ContainerClient, BlobClient
import asyncio
import os
import uuid

class AzureUploader(object):
    def __init__(self, connectionString, containerName):
        self.connectionString = connectionString
        self.containerName = containerName

    def is_exist_container(self):
        container = ContainerClient.from_connection_string(self.connectionString, self.containerName)
        try:
            container_properties = container.get_container_properties()
            # Container foo exists. You can now use it.
            return True
        except Exception as e:
            # Container foo does not exist. You can now create it.
            print(e)
            return False

    def make_container(self):
        try:
            container_client = ContainerClient.from_connection_string(conn_str=self.connectionString, container_name=self.containerName)
            container_client.create_container()
            return True
        except Exception as e:
            # Container foo does not exist. You can now create it.
            print(e)
            return False

    def make_container_retry(self, maxRetryCount = 5):
        retryCount = 0
        while retryCount < maxRetryCount:
            retryCount += 1
            if not self.is_exist_container():
                isSuccess = self.make_container()
                if isSuccess:
                    break

    # async def async_task_make_container(connectionString, containerName):
    #     container_client = ContainerClient.from_connection_string(conn_str=connectionString, container_name=containerName)
    #     await container_client.create_container()
    #     return True

    # async def async_make_container(loop, connectStr, containerName):
    #     await loop.create_task(async_task_make_container(connectStr, containerName))
    #     #await task_make_container(connection_string, container_name)
    #     return True
