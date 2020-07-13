# coding: UTF-8

class FileUtil:
    
    def __init__(self):
        self.MEDIA_TYPE = {
            # Images
            'png': 'image/png',
            'jpg': 'image/jpeg',

            # Documents
            'txt': 'text/plain',
            'html': 'text/html',
            'css': 'text/css',
            'js': 'text/javascript',
            'pdf': 'application/pdf',

            # Audio
            'mp3': 'audio/mp3',
        }

    def get_file_extention(self, filename):
        return filename.rsplit('.', 1)[1].lower()

    def convert_filename_jpeg_to_jpg(self, filename):
        basename_without_ext = filename.split('.')[0]
        print("basename_without_ext")
        print(basename_without_ext)
        extension = filename.rsplit('.', 1)[1].lower()
        print("extension")
        print(extension)
        if extension == "jpeg":
            extension = "jpg"
        newfilename = f"{basename_without_ext}.{extension}"
        return newfilename

    def get_media_type_for_extension(self, ext):
        return self.MEDIA_TYPE[str(ext)]