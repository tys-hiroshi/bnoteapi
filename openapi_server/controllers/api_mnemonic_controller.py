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

from pymongo import DESCENDING, ASCENDING
import connexion
import six
import multiprocessing
from openapi_server import app, mongo, bootstrap

from openapi_server.libraires.whats_on_chain_lib import WhatsOnChainLib
import bitsv
from openapi_server.bip39mnemonic import Bip39Mnemonic

def api_mnemonic():  # noqa: E501
    """convert mnemonic words to wif, asset on Bitcoin SV.

    convert mnemonic words to wif, asset on Bitcoin SV. # noqa: E501

    :param body: request /api/mnemonic
    :type body: dict | bytes

    :rtype: ResponseMnemonicModel
    """
    # if connexion.request.is_json:
    #     body = RequestMnemonicModel.from_dict(connexion.request.get_json())  # noqa: E501
    # return 'do some magic!'

    try:
        app.app.logger.info("start /api/mnemonic")
        if connexion.request.is_json:
            body = RequestMnemonicModel.from_dict(connexion.request.get_json())  # noqa: E501
        mnemonic = body.mnemonic  #app.config['TESTNET_MNEMONIC']
        bip39Mnemonic = Bip39Mnemonic(mnemonic, passphrase="", network="test")
        privateKey = bitsv.Key(bip39Mnemonic.privatekey_wif, network = 'test')
        address = privateKey.address
        balance_satoshi = privateKey.get_balance()
        #balance_bsv = float(balance_satoshi) / float(100000000)
            # html = render_template(
            #     'mnemonic.html',
            #     privatekey_wif = bip39Mnemonic.privatekey_wif,
            #     address = address,
            #     balance_satoshi = balance_satoshi,
            #     balance_bsv = balance_bsv,
            #     title="mnemonic")
        return ResponseMnemonicModel(0, bip39Mnemonic.privatekey_wif, address, balance_satoshi).to_str(), 200
    except Exception as e:
        print(e)
        return {}, 500

