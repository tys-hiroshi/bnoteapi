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

def api_download(txid):  # noqa: E501
    """get data for transaction id on Bitcoin SV.

    get data for transaction id on Bitcoin SV. # noqa: E501

    :param txid: bitcoin sv transaction id
    :type txid: str

    :rtype: file
    """
    # return 'do some magic!'
    url = "https://api.whatsonchain.com/v1/bsv/test/tx/hash/" + txid
    headers = {"content-type": "application/json"}
    r = requests.get(url, headers=headers)
    data = r.json()
    op_return = data['vout'][0]['scriptPubKey']['opReturn']
    upload_data = data['vout'][0]['scriptPubKey']['asm'].split()[3] ##uploaddata (charactor)
    upload_mimetype = op_return['parts'][1] ##MEDIA_Type:  image/png, image/jpeg, text/plain, text/html, text/css, text/javascript, application/pdf, audio/mp3
    upload_charset = op_return['parts'][2] ##ENCODING: binary, utf-8 (Definition polyglot/upload.py)
    upload_filename = op_return['parts'][3] ##filename
    print("upload_mimetype: " + upload_mimetype)
    print("upload_charset: " + upload_charset)
    print("upload_filename: " + upload_filename)
    if upload_charset == 'binary':  #47f0706cdef805761a975d4af2a418c45580d21d4d653e8410537a3de1b1aa4b
        #print(binascii.hexlify(upload_data))
        data = binascii.unhexlify(upload_data)
    elif upload_charset == 'utf-8':  #cc80675a9a64db116c004b79d22756d824b16d485990a7dfdf46d4a183b752b2
        data = op_return['parts'][0]
    else:
        print('upload_charset' + upload_charset)
        data = ''
    downloadFilename = upload_filename
    #headers["Content-Disposition"] = 'attachment; filename=' + downloadFilename
    header_ContentDisposition = 'attachment; filename=' + downloadFilename
    mimetype = upload_mimetype
    
    response = app.app.make_response(data)
    response.data = data
    response.headers["Content-Disposition"] = header_ContentDisposition
    response.mimetype = mimetype
    return response
