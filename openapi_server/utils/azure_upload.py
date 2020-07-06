from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions, ContainerClient, BlobClient
import asyncio
import os
import uuid

def is_exist_container(connectStr, containerName):
    container = ContainerClient.from_connection_string(connectStr, containerName)
    try:
        container_properties = container.get_container_properties()
        # Container foo exists. You can now use it.
        return True
    except Exception as e:
        # Container foo does not exist. You can now create it.
        print(e)
        return False

def make_container(connectStr, containerName):
    try:
        container_client = ContainerClient.from_connection_string(conn_str=connectStr, container_name=containerName)
        container_client.create_container()
        return True
    except Exception as e:
        # Container foo does not exist. You can now create it.
        print(e)
        return False

def make_container_retry(connectStr, containerName, maxRetryCount = 5):
    retryCount = 0
    while retryCount < maxRetryCount:
        retryCount += 1
        if not is_exist_container(connectStr, containerName):
            isSuccess = make_container(connectStr, containerName)
            if isSuccess:
                break

async def async_task_make_container(connectStr, containerName):
    container_client = ContainerClient.from_connection_string(conn_str=connectStr, container_name=containerName)
    await container_client.create_container()
    return True

async def async_make_container(loop, connectStr, containerName):
    await loop.create_task(async_task_make_container(connectStr, containerName))
    #await task_make_container(connection_string, container_name)
    return True
