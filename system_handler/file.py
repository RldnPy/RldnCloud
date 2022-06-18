#-*- coding:utf-8 -*-
import os
from .error import Error
import datetime
from mimetypes import guess_type

class FileBase:
    def __init__(self, data: dict):
        self._update(data)

    def __repr__(self) -> str:
        return (
            f"<system_handler.FileBase path={self.path} name={self.name}>"
        )

    def __str__(self) -> str:
        return f"<system_handler.FileBase path={self.path} name={self.name}>"

    def _byte_transform(self, bytes:int, to:str, lens:int = 0, bsize = 1024):
        a = {'k': 1, 'm': 2, 'g': 3, 't': 4, 'p': 5, 'e': 6, 'K': 1, 'M': 2, 'G': 3, 'T': 4, 'P': 5, 'E': 6}
        r = float(bytes)
        for i in range(a[to]): r = r / bsize
        return round(r, lens)

    def _update(self, data: dict):
        self.path = str(data.get("path"))
        if len(self.path.strip()) <= 0: self.path = "."
        self.name = str(data.get("name"))
        self.mimetype = str(guess_type(f"{self.path}/{self.name}")[0])
        self.type = "file"

    @property
    def bytes(self) -> int:
        if not os.path.isfile(f"{self.path}/{self.name}"): raise Error.NotFound("File Not Found")
        return int(os.path.getsize(f"{self.path}/{self.name}"))

    @property
    def bytes_str(self) -> str:
        if not os.path.isfile(f"{self.path}/{self.name}"): raise Error.NotFound("File Not Found")
        bytes = self.bytes
        bytes_str = None
        for i in ['E', 'P', 'T', 'G', 'M', 'K']:
            _byte_transfor = self._byte_transform(bytes, str(i), 0)
            if _byte_transfor != 0:
                bytes_str = f"{str(_byte_transfor)}{i}B"
                break
        if bytes_str == None: bytes_str = str(bytes) + "B"
        return str(bytes_str)

    @property
    def bytes_str2(self) -> str:
        if not os.path.isfile(f"{self.path}/{self.name}"): raise Error.NotFound("File Not Found")
        bytes = self.bytes
        bytes_str = None
        for i in ['E', 'P', 'T', 'G', 'M', 'K']:
            _byte_transfor = self._byte_transform(bytes, str(i), 2)
            if int(_byte_transfor) != 0:
                bytes_str = f"{str(_byte_transfor)}{i}B"
                break
        if bytes_str == None: bytes_str = str(bytes) + "B"
        return str(bytes_str)

    @property
    def make_time(self) -> int:
        if not os.path.isfile(f"{self.path}/{self.name}"): raise Error.NotFound("File Not Found")
        return int(os.path.getctime(f"{self.path}/{self.name}"))

    @property
    def revise_time(self) -> int:
        if not os.path.isfile(f"{self.path}/{self.name}"): raise Error.NotFound("File Not Found")
        return int(os.path.getmtime(f"{self.path}/{self.name}"))

    @property
    def access_time(self) -> int:
        if not os.path.isfile(f"{self.path}/{self.name}"): raise Error.NotFound("File Not Found")
        return int(os.path.getatime(f"{self.path}/{self.name}"))

    @property
    def access_time_str(self) -> str:
        if not os.path.isfile(f"{self.path}/{self.name}"): raise Error.NotFound("File Not Found")
        return (datetime.datetime.fromtimestamp(self.access_time).strftime('%Y! %m@ %d# %H:%M:%S')).replace("!", "년").replace("@", "월").replace("#", "일")

    @property
    def revise_time_str(self) -> str:
        if not os.path.isfile(f"{self.path}/{self.name}"): raise Error.NotFound("File Not Found")
        return (datetime.datetime.fromtimestamp(self.revise_time).strftime('%Y! %m@ %d# %H:%M:%S')).replace("!", "년").replace("@", "월").replace("#", "일")

    @property
    def make_time_str(self) -> str:
        if not os.path.isfile(f"{self.path}/{self.name}"): raise Error.NotFound("File Not Found")
        return (datetime.datetime.fromtimestamp(self.make_time).strftime('%Y! %m@ %d# %H:%M:%S')).replace("!", "년").replace("@", "월").replace("#", "일")


class File(FileBase):
    def __init__(self, data: dict):
        super().__init__(data)
        self.base = super()

    def __repr__(self) -> str:
        return (
            f"<system_handler.File>"
        )

    def __str__(self) -> str:
        return f"<system_handler.File>"