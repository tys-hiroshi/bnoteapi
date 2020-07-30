import polyglot

class FileUploaderOnChain:

    def __init__(self):
        self.MAX_BSV_SIZE_BYTES = 100000
        self.ENCODING = "utf-8"

    def upload_text_file(self, file_name: str, message: str, privatekey_wif: str, network: str = '') -> str:
        message_bytes = message.encode(self.ENCODING)
        message_bytes_length = len(message_bytes)
        print(message_bytes_length)
        if(message_bytes_length >= self.MAX_BSV_SIZE_BYTES):   #more less 100kb = 100000bytes.
            return None

        req_bytearray = bytearray(message_bytes)
        media_type = "text/plain"
        #upload data
        uploader = polyglot.Upload(privatekey_wif, network=network)
        rawtx = uploader.b_create_rawtx_from_binary(req_bytearray, media_type, self.ENCODING, file_name)
        hash_txid = uploader.send_rawtx(rawtx)

        return hash_txid