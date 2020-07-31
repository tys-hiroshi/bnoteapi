import requests
import binascii

from openapi_server.utils.models.FileDownloaderOnChain.ResponseDownloadFileModel import ResponseDownloadFileModel

class FileDownloaderOnChain:

    def __init__(self, network: str = ''):
        self.tx_hash_base_url = f"https://api.whatsonchain.com/v1/bsv/{network}/tx/hash/"
        self.MAX_RETRY_COUNT = 5

    def download_file(self, tx_id: str):
        error_count = 0
        while error_count < self.MAX_RETRY_COUNT:
            try:
                url = self.tx_hash_base_url + tx_id
                
                headers = {"content-type": "application/json"}
                r = requests.get(url, headers=headers)
                data = r.json()
                op_return = data['vout'][0]['scriptPubKey']['opReturn']
                uploaded_data = data['vout'][0]['scriptPubKey']['asm'].split()[3] ##uploaddata (charactor)
                uploaded_mimetype = op_return['parts'][1] ##MEDIA_Type:  image/png, image/jpeg, text/plain, text/html, text/css, text/javascript, application/pdf, audio/mp3
                uploaded_charset = op_return['parts'][2] ##ENCODING: binary, utf-8 (Definition polyglot/upload.py)
                uploaded_filename = op_return['parts'][3] ##filename
                print("uploaded_mimetype: " + uploaded_mimetype)
                print("uploaded_charset: " + uploaded_charset)
                print("uploaded_filename: " + uploaded_filename)
                if uploaded_charset == 'binary':  #47f0706cdef805761a975d4af2a418c45580d21d4d653e8410537a3de1b1aa4b
                    data = binascii.unhexlify(uploaded_data)
                elif uploaded_charset == 'utf-8':  #cc80675a9a64db116c004b79d22756d824b16d485990a7dfdf46d4a183b752b2
                    data = op_return['parts'][0]
                else:
                    print('upload_charset' + uploaded_charset)
                    data = ''
                return ResponseDownloadFileModel(data, uploaded_filename)
            except Exception as ex:
                error_count += 1
                ##TODO: output logger
        
        return ""
