import connexion
import six

from openapi_server.models.response_genkey_model import ResponseGenKeyModel  # noqa: E501
from openapi_server import util

from openapi_server import app, mongo, bootstrap
import requests
import binascii
from openapi_server.utils.CryptUtil import CryptUtil

def api_genkey(typeid=None):  # noqa: E501
    """get data for transaction id on Bitcoin SV.

    get data for transaction id on Bitcoin SV. # noqa: E501

    :param typeid: typeid
    :type typeid: str
    """
    # return 'do some magic!'
    if typeid == 'ecies':
        cryptUtil = CryptUtil()
        ec_key = cryptUtil.generateEciesKey()
        secret_key_hex = ec_key.to_hex()
        public_key_hex = ec_key.public_key.to_hex()

        return ResponseGenKeyModel(0, secret_key_hex, public_key_hex).to_dict(), 200
    else:
        return {}, 500

