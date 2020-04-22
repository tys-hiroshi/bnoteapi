import connexion
import six

from openapi_server.models.request_add_address_model import RequestAddAddressModel  # noqa: E501
from openapi_server.models.request_upload_text_model import RequestUploadTextModel  # noqa: E501
from openapi_server.models.response_add_address_model import ResponseAddAddressModel  # noqa: E501
from openapi_server.models.response_tx_model import ResponseTxModel  # noqa: E501
from openapi_server.models.response_upload_text_model import ResponseUploadTextModel  # noqa: E501
from openapi_server import util

from openapi_server import app, mongo, bootstrap
import bitsv
from openapi_server.bip39mnemonic import Bip39Mnemonic
import polyglot
import datetime

def api_uploadtext(body):  # noqa: E501
    """upload text data on Bitcoin SV.

     # noqa: E501

    :param body: upload text data on Bitcoin SV.
    :type body: dict | bytes

    :rtype: List[ResponseUploadTextModel]
    """
    try:
        if connexion.request.is_json:
            body = RequestUploadTextModel.from_dict(connexion.request.get_json())  # noqa: E501
        app.app.logger.info("start /api/upload_text")
        if connexion.request.headers['Content-Type'] != 'application/json':
            print(connexion.request.headers['Content-Type'])
            return ResponseUploadTextModel(0, "success").to_dict(), 400
        mnemonic_words = body.mnemonic_words
        message = body.message
        bip39Mnemonic = Bip39Mnemonic(mnemonic_words, passphrase="", network="test")
        privateKey = bitsv.Key(bip39Mnemonic.privatekey_wif, network = 'test')

        encoding = "utf-8"
        print("bip39Mnemonic.privatekey_wif")
        print(bip39Mnemonic.privatekey_wif)
        message_bytes = message.encode(encoding)
        message_bytes_length = len(message_bytes)
        print(message_bytes_length)
        if(message_bytes_length >= 100000):   #more less 100kb = 100000bytes.
            return {}, 400

        req_bytearray = bytearray(message_bytes)
        #transaction = uploader.bcat_parts_send_from_binary(req_file_bytearray)
        media_type = "text/plain"
        print(media_type)
        print(encoding)
        file_name = format(datetime.date.today(), '%Y%m%d')
        #upload data
        uploader = polyglot.Upload(bip39Mnemonic.privatekey_wif, network='test')
        print(uploader.filter_utxos_for_bcat())
        rawtx = uploader.b_create_rawtx_from_binary(req_bytearray, media_type, encoding, file_name)
        txid = uploader.send_rawtx(rawtx)
        mongo.db.transaction.insert({"address": privateKey.address, "txid": txid})
        #transaction = uploader.upload_b(filepath)
        #['5cd293a25ecf0b346ede712ceb716f35f1f78e2c5245852eb8319e353780c615']
        print("upload txid")
        print(txid)

        return RequestUploadTextModel(0, "success").to_dict(), 200
    except Exception as e:
        print(e)
        return {}, 500