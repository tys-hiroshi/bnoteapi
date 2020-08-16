from openapi_server.utils.FileUtil import FileUtil

class ResponseDownloadFileModel:
    
    def __init__(self, data: object, file_name: str):
        self.data = data
        fileUtil = FileUtil()
        self.file_extension = fileUtil.get_file_extention(file_name)