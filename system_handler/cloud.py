#-*- coding:utf-8 -*-
from .json_handler import Json
import os
from typing import Optional, Union, List
from .error import Error
from .file import File
from .directory import Directory

class CloudBase:
    def __init__(self):
        self.setting_json = Json("settings.json")

    def __repr__(self) -> str:
        return (
            f"<system_handler.CloudBase>"
        )

    def __str__(self) -> str:
        return f"<system_handler.CloudBase>"

    async def get_files(self, path: Optional[str] = None) -> List[Union[File, Directory]]:
        if not path: path = self.setting_json.get("cloud_path")
        else:
            path_list = path.split("/")
            if path_list[0] != str(self.setting_json.get("cloud_path")).split("/")[0]:
                path = f"{str(self.setting_json.get('cloud_path'))}/{path}"
        if not os.path.isdir(path): raise Error.NotFound("There is no path.")
        file_list = os.listdir(path)
        return_dir_list = []
        return_file_list = []
        for i in file_list:
            if os.path.isfile(f"{path}/{i}"):
                data = dict()
                data["path"] = path
                data["name"] = i
                return_file_list.append(File(data))
            else:
                data = dict()
                data["path"] = path
                data["name"] = i
                return_dir_list.append(Directory(data))


        return return_dir_list + return_file_list

    async def get_file(self, path: str = None) -> File:
        if not os.path.isfile(str(path)): raise Error.NotFound("File Not Found")
        data = dict()
        data["path"] = "/".join(path.split("/")[:-1])
        data["name"] = path.split("/")[-1]
        return File(data)

    async def get_directory(self, path: str = None) -> Directory:
        if not os.path.isdir(str(path)): raise Error.NotFound("directory Not Found")
        data = dict()
        data["path"] = "/".join(path.split("/")[:-1])
        data["name"] = path.split("/")[-1]
        return Directory(data)

class Cloud(CloudBase):
    def __init__(self):
        super().__init__()
        self.base = super()

    def __repr__(self) -> str:
        return (
            f"<system_handler.Cloud>"
        )

    def __str__(self) -> str:
        return f"<system_handler.Cloud>"

    async def get_files(self, path: Optional[str] = None) -> List[Union[File, Directory]]:
        """
        특정 폴더의 파일을 불러옵니다.

        Returns
        --------
        List[Union[File, Directory]]

        Raises
        -------
        Error.NotFound
            폴더가 아니거나 없을경우 발생 합니다.
        """
        return await self.base.get_files(path)

    async def get_file(self, path: str = None) -> File:
        """
        특정 파일을 불러옵니다.

        Returns
        --------
        File

        Raises
        -------
        Error.NotFound
            없는 파일일경우 발생 합니다.
        """
        return await self.base.get_file(path)

    async def get_directory(self, path: str = None) -> Directory:
        """
        특정 폴더를 불러옵니다.

        Returns
        --------
        Directory

        Raises
        -------
        Error.NotFound
            없는 폴더일경우 발생 합니다.
        """
        return await self.base.get_directory(path)