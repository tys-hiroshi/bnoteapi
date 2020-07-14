# coding: UTF-8

## https://qiita.com/5zm/items/49118188d76e61ca5113
import os
from io import BytesIO
import contextlib

class DivideStream:
    def __init__(self):
        pass

    # 指定されたデータサイズでファイルを分割する
    def divide_stream(self, stream, chunkSize):

        def read():
            while True:
                data = stream.read(chunkSize)
                if len(data) == 0:
                    return
                yield data

        # def write(filePath, data):
        #     with open(filePath, 'wb') as f:
        #         f.write(data)

        def divide():
            for i, data in enumerate(read()):
                #saveFilePath = '%s.%s' % ("teststrea", i)
                #write(saveFilePath, data)
                yield data

        return list(divide())

    # 渡されたファイルリストの順序で１つのファイルに結合する
    def join_file(self, fileList, filePath):

        with open(filePath, 'wb') as saveFile:
            for f in fileList:
                data = open(f, "rb").read()
                saveFile.write(data)
                saveFile.flush()

    # 渡されたファイルリストの順序で１つのファイルに結合する
    #https://blog.hirokiky.org/entry/2019/04/29/161729
    @contextlib.contextmanager
    def join_stream(self, streamList):
        with BytesIO() as bs:
            for stream in streamList:
                bs.write(stream)
            yield bs
    
    # 渡されたファイルリストの順序で１つのファイルに結合する
    #https://blog.hirokiky.org/entry/2019/04/29/161729
    def join_stream_to_bytes(self, streamList, bytesio):
        for stream in streamList:
            bytesio.write(stream)
        return bytesio

    # 指定された部分データをファイルから取得する
    def partial_content(self, filePath, start, end):

        partialSize = end - start + 1
        f = open(filePath, "rb")
        f.seek(start)
        data = f.read(partialSize)
        print(type(data))
        return data

# # main
# if __name__ == "__main__":
#     #mkfile 3m testfile
#     # 3126866 Byte
#     #target = "image.jpg"
#     target = "test10m.jpg"

#     # 250000 Byte で分割
#     fileList = divide_file(target, 250000)
#     # 分割したファイルを結合
#     join_file(fileList, 'join_' + target)

#     # 0-9999 の 10000 Byte を取り出す
#     data01 = partial_content(target, 0, 9999)
#     # 10000-残り全て を取り出す
#     data02 = partial_content(target, 10000, os.path.getsize(target))
#     # 結合して確かめる
#     with open('partial_' + target, 'wb') as filePartial:
#         filePartial.write(data01)
#         filePartial.write(data02)