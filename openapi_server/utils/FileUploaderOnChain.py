import polyglot

class FileUploaderOnChain:

    def __init__(self, privatekey_wif: str, network: str = ''):
        self.MAX_BSV_SIZE_BYTES = 100000
        self.TEXT_ENCODING = "utf-8"
        self.MAX_RETRY_COUNT = 100000
        self.privatekey_wif = privatekey_wif
        self.network = network

    def upload_file_bytearray(self, file_name: str, file_bytearray: bytearray) -> str:
        error_count = 0
        while error_count < self.MAX_RETRY_COUNT:
            try:
                uploader = polyglot.Upload(wif=self.privatekey_wif, network=self.network)
                media_type = uploader.get_media_type_for_file_name(file_name)  ## WARNING: .jpeg is Error!!!!!
                encoding = uploader.get_encoding_for_file_name(file_name)
                rawtx = uploader.b_create_rawtx_from_binary(file_bytearray, media_type, encoding, file_name)
                tx_id = uploader.send_rawtx(rawtx)  ##TODO: retry or wait. リクエストが早すぎて失敗することがあるので
                if tx_id == None or tx_id == "":
                    raise ValueError("ERROR; tx_id is Empty.")
                return tx_id
            except Exception as e:
                error_count += 1
                ##TODO: output logger
        return ""

    def upload_text_file(self, file_name: str, message: str) -> str:
        error_count = 0
        while error_count < self.MAX_RETRY_COUNT:
            try:
                message_bytes = message.encode(self.TEXT_ENCODING)
                message_bytes_length = len(message_bytes)
                if(message_bytes_length >= self.MAX_BSV_SIZE_BYTES):   #more less 100kb = 100000bytes.
                    return None

                req_bytearray = bytearray(message_bytes)
                media_type = "text/plain"
                #upload data
                uploader = polyglot.Upload(self.privatekey_wif, network=self.network)
                rawtx = uploader.b_create_rawtx_from_binary(req_bytearray, media_type, self.TEXT_ENCODING, file_name)
                tx_id = uploader.send_rawtx(rawtx)
                if tx_id == None or tx_id == "":
                    raise ValueError("ERROR; tx_id is Empty.")
                return tx_id
            except Exception as e:
                    error_count += 1
                ##TODO: output logger
        return ""