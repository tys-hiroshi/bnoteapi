# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class RequestDownloadFromCloudModel(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, file_id=None, secret_key_hex=None, encrypt_hex=None, on_chain=None, tx_id_list=None):  # noqa: E501
        """RequestDownloadFromCloudModel - a model defined in OpenAPI

        :param file_id: The file_id of this RequestDownloadFromCloudModel.  # noqa: E501
        :type file_id: str
        :param secret_key_hex: The secret_key_hex of this RequestDownloadFromCloudModel.  # noqa: E501
        :type secret_key_hex: str
        :param encrypt_hex: The encrypt_hex of this RequestDownloadFromCloudModel.  # noqa: E501
        :type encrypt_hex: str
        :param on_chain: The on_chain of this RequestDownloadFromCloudModel.  # noqa: E501
        :type on_chain: str
        :param tx_id_list: The tx_id_list of this RequestDownloadFromCloudModel.  # noqa: E501
        :type tx_id_list: List[str]
        """
        self.openapi_types = {
            'file_id': str,
            'secret_key_hex': str,
            'encrypt_hex': str,
            'on_chain': str,
            'tx_id_list': List[str]
        }

        self.attribute_map = {
            'file_id': 'file_id',
            'secret_key_hex': 'secret_key_hex',
            'encrypt_hex': 'encrypt_hex',
            'on_chain': 'on_chain',
            'tx_id_list': 'tx_id_list'
        }

        self._file_id = file_id
        self._secret_key_hex = secret_key_hex
        self._encrypt_hex = encrypt_hex
        self._on_chain = on_chain
        self._tx_id_list = tx_id_list

    @classmethod
    def from_dict(cls, dikt) -> 'RequestDownloadFromCloudModel':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The RequestDownloadFromCloudModel of this RequestDownloadFromCloudModel.  # noqa: E501
        :rtype: RequestDownloadFromCloudModel
        """
        return util.deserialize_model(dikt, cls)

    @property
    def file_id(self):
        """Gets the file_id of this RequestDownloadFromCloudModel.


        :return: The file_id of this RequestDownloadFromCloudModel.
        :rtype: str
        """
        return self._file_id

    @file_id.setter
    def file_id(self, file_id):
        """Sets the file_id of this RequestDownloadFromCloudModel.


        :param file_id: The file_id of this RequestDownloadFromCloudModel.
        :type file_id: str
        """

        self._file_id = file_id

    @property
    def secret_key_hex(self):
        """Gets the secret_key_hex of this RequestDownloadFromCloudModel.


        :return: The secret_key_hex of this RequestDownloadFromCloudModel.
        :rtype: str
        """
        return self._secret_key_hex

    @secret_key_hex.setter
    def secret_key_hex(self, secret_key_hex):
        """Sets the secret_key_hex of this RequestDownloadFromCloudModel.


        :param secret_key_hex: The secret_key_hex of this RequestDownloadFromCloudModel.
        :type secret_key_hex: str
        """

        self._secret_key_hex = secret_key_hex

    @property
    def encrypt_hex(self):
        """Gets the encrypt_hex of this RequestDownloadFromCloudModel.


        :return: The encrypt_hex of this RequestDownloadFromCloudModel.
        :rtype: str
        """
        return self._encrypt_hex

    @encrypt_hex.setter
    def encrypt_hex(self, encrypt_hex):
        """Sets the encrypt_hex of this RequestDownloadFromCloudModel.


        :param encrypt_hex: The encrypt_hex of this RequestDownloadFromCloudModel.
        :type encrypt_hex: str
        """

        self._encrypt_hex = encrypt_hex

    @property
    def on_chain(self):
        """Gets the on_chain of this RequestDownloadFromCloudModel.


        :return: The on_chain of this RequestDownloadFromCloudModel.
        :rtype: str
        """
        return self._on_chain

    @on_chain.setter
    def on_chain(self, on_chain):
        """Sets the on_chain of this RequestDownloadFromCloudModel.


        :param on_chain: The on_chain of this RequestDownloadFromCloudModel.
        :type on_chain: str
        """

        self._on_chain = on_chain

    @property
    def tx_id_list(self):
        """Gets the tx_id_list of this RequestDownloadFromCloudModel.


        :return: The tx_id_list of this RequestDownloadFromCloudModel.
        :rtype: List[str]
        """
        return self._tx_id_list

    @tx_id_list.setter
    def tx_id_list(self, tx_id_list):
        """Sets the tx_id_list of this RequestDownloadFromCloudModel.


        :param tx_id_list: The tx_id_list of this RequestDownloadFromCloudModel.
        :type tx_id_list: List[str]
        """

        self._tx_id_list = tx_id_list
