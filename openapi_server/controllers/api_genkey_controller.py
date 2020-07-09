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

from openapi_server import app, mongo, bootstrap
import requests
import binascii
from openapi_server.utils.CryptUtil import CryptUtil

def api_genkey(typeid):  # noqa: E501
    """get data for transaction id on Bitcoin SV.

    get data for transaction id on Bitcoin SV. # noqa: E501

    :param txid: bitcoin sv transaction id
    :type txid: str

    :rtype: file
    """
    # return 'do some magic!'
    cryptUtil = CryptUtil()
    ec_key = cryptUtil.generateEciesKey()
    ec_key.to_hex()
    return response
