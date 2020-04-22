# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.request_add_address_model import RequestAddAddressModel  # noqa: E501
from openapi_server.models.request_mnemonic_model import RequestMnemonicModel  # noqa: E501
from openapi_server.models.request_upload_text_model import RequestUploadTextModel  # noqa: E501
from openapi_server.models.response_add_address_model import ResponseAddAddressModel  # noqa: E501
from openapi_server.models.response_mnemonic_model import ResponseMnemonicModel  # noqa: E501
from openapi_server.models.response_tx_model import ResponseTxModel  # noqa: E501
from openapi_server.models.response_upload_model import ResponseUploadModel  # noqa: E501
from openapi_server.models.response_upload_text_model import ResponseUploadTextModel  # noqa: E501
from openapi_server.test import BaseTestCase


class TestApiController(BaseTestCase):
    """ApiController integration test stubs"""

    def test_api_addaddress(self):
        """Test case for api_addaddress

        search data for added address on bitcoin sv
        """
        body = {
  "address" : "bitcoin sv address"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'api_key': 'special-key',
        }
        response = self.client.open(
            '/v1/api/add_address',
            method='POST',
            headers=headers,
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_download(self):
        """Test case for api_download

        get data for transaction id on Bitcoin SV.
        """
        headers = { 
            'Accept': 'text/plain',
            'api_key': 'special-key',
        }
        response = self.client.open(
            '/v1/api/download/{txid}'.format(txid='txid_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_mnemonic(self):
        """Test case for api_mnemonic

        convert mnemonic words to wif, asset on Bitcoin SV.
        """
        body = {
  "mnemonic" : "bitcoin sv mnemonic words"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'api_key': 'special-key',
        }
        response = self.client.open(
            '/v1/api/mnemonic',
            method='POST',
            headers=headers,
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_tx(self):
        """Test case for api_tx

        get transactions.
        """
        query_string = [('start_index', 56),
                        ('count', 56)]
        headers = { 
            'Accept': 'application/json',
            'api_key': 'special-key',
        }
        response = self.client.open(
            '/v1/api/tx/{addr}'.format(addr='addr_example'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @unittest.skip("multipart/form-data not supported by Connexion")
    def test_api_upload(self):
        """Test case for api_upload

        upload file on Bitcoin SV. (100kb)
        """
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'multipart/form-data',
            'api_key': 'special-key',
        }
        data = dict(privatekey_wif='privatekey_wif_example',
                    file=(BytesIO(b'some file data'), 'file.txt'))
        response = self.client.open(
            '/v1/api/upload',
            method='POST',
            headers=headers,
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_api_uploadtext(self):
        """Test case for api_uploadtext

        upload text data on Bitcoin SV.
        """
        body = {
  "mnemonic_words" : "",
  "message" : "upload text"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'api_key': 'special-key',
        }
        response = self.client.open(
            '/v1/api/upload_text',
            method='POST',
            headers=headers,
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
