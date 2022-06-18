#-*- coding:utf-8 -*-
from .json_handler import Json
import os
from typing import Optional, Union, List
from .error import Error
import datetime
from .file import File

class DirectoryBase:
    def __init__(self, data: dict):
        self.setting_json = Json("settings.json")
        self._update(data)

    def __repr__(self) -> str:
        return (
            f"<system_handler.DirectoryBase path={self.path} name={self.name}>"
        )

    def __str__(self) -> str:
        return f"<system_handler.DirectoryBase path={self.path} name={self.name}>"

    def _byte_transform(self, bytes:int, to:str, lens:int = 0, bsize = 1024):
        a = {'k': 1, 'm': 2, 'g': 3, 't': 4, 'p': 5, 'e': 6, 'K': 1, 'M': 2, 'G': 3, 'T': 4, 'P': 5, 'E': 6}
        r = float(bytes)
        for i in range(a[to]): r = r / bsize
        return round(r, lens)

    def _update(self, data: dict):
        self.path = str(data.get("path"))
        if len(self.path.strip()) <= 0: self.path = "."
        self.name = str(data.get("name"))
        self.type = "directory"
        self.url = f"{self.path}/{self.name}".replace(self.setting_json.get("cloud_path"), ".")

    def get_dir_size(self, path='.'):
        total = 0
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += self.get_dir_size(entry.path)
        return total

    @property
    def bytes(self) -> int:
        if not os.path.isdir(f"{self.path}/{self.name}"): raise Error.NotFound("directory Not Found")
        return int(self.get_dir_size(path=f"{self.path}/{self.name}"))

    @property
    def bytes_str(self) -> str:
        if not os.path.isdir(f"{self.path}/{self.name}"): raise Error.NotFound("directory Not Found")
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
        if not os.path.isdir(f"{self.path}/{self.name}"): raise Error.NotFound("directory Not Found")
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
    def files(self):
        if not os.path.isdir(f"{self.path}/{self.name}"): raise Error.NotFound("directory Not Found")
        file_list = os.listdir(f"{self.path}/{self.name}")
        return_dir_list = []
        return_file_list = []
        for i in file_list:
            if os.path.isfile(f"{f'{self.path}/{self.name}'}/{i}"):
                data = dict()
                data["path"] = f"{self.path}/{self.name}"
                data["name"] = i
                return_file_list.append(File(data))
            else:
                data = dict()
                data["path"] = f"{self.path}/{self.name}"
                data["name"] = i
                return_dir_list.append(Directory(data))


        return return_dir_list + return_file_list

    @property
    def make_time(self) -> int:
        if not os.path.isdir(f"{self.path}/{self.name}"): raise Error.NotFound("directory Not Found")
        return int(os.path.getctime(f"{self.path}/{self.name}"))

    @property
    def make_time_str(self) -> str:
        if not os.path.isdir(f"{self.path}/{self.name}"): raise Error.NotFound("directory Not Found")
        return (datetime.datetime.fromtimestamp(self.make_time).strftime('%Y! %m@ %d# %H:%M:%S')).replace("!", "년").replace("@", "월").replace("#", "일")


class Directory(DirectoryBase):
    def __init__(self, data: dict):
        super().__init__(data)
        self.base = super()

    def __repr__(self) -> str:
        return (
            f"<system_handler.Directory>"
        )

    def __str__(self) -> str:
        return f"<system_handler.Directory>"
