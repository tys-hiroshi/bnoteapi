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

import polyglot

# アップロードされる拡張子の制限
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif', 'txt'])

def allwed_file(filename):
    # .があるかどうかのチェックと、拡張子の確認
    # OKなら１、だめなら0
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def api_upload(file=None, privatekey_wif=None):  # noqa: E501
    """upload file on Bitcoin SV. (100kb)

    convert mnemonic words to wif, asset on Bitcoin SV. # noqa: E501

    :param privatekey_wif: 
    :type privatekey_wif: str
    :param file: 
    :type file: str

    :rtype: ResponseUploadModel
    """
    #return 'do some magic!'
    
    # # ファイルがなかった場合の処理
    # if 'file' not in request.files:
    #     print('ファイルがありません')
    #     return redirect(request.url)
    # データの取り出し
    req_file = file
    stream = req_file.stream
    #img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)

    # ファイル名がなかった時の処理
    if req_file.filename == '':
        return {}, 400
    # ファイルのチェック
    if req_file and allwed_file(req_file.filename):
        # 危険な文字を削除（サニタイズ処理）
        #filename = secure_filename(req_file.filename)
        # ファイルの保存
        #filepath = os.path.join(app.config['UPLOAD_FOLDER'], req_file.filename)
        #req_file.save(filepath)
        #privatekey_wif = "cTqvJoYPXAKUuNWre4B53LDSUQNRq8P6vcRHtrTEnrSSNhUynysF"
        uploader = polyglot.Upload(privatekey_wif, 'test')
        print(uploader.network)
        req_file_bytearray = bytearray(stream.read())
        print(req_file_bytearray)
        #transaction = uploader.bcat_parts_send_from_binary(req_file_bytearray)
        media_type = uploader.get_media_type_for_file_name(req_file.filename)
        encoding = uploader.get_encoding_for_file_name(req_file.filename)
        print(media_type)
        print(encoding)
        rawtx = uploader.b_create_rawtx_from_binary(req_file_bytearray, media_type, encoding, req_file.filename)
        txid = uploader.send_rawtx(rawtx)
        #transaction = uploader.upload_b(filepath)
        #['5cd293a25ecf0b346ede712ceb716f35f1f78e2c5245852eb8319e353780c615']
        print(txid)

        return ResponseUploadModel(0, txid).to_str()
