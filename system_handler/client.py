#-*- coding:utf-8 -*-
from .error import Error
from flask import session, flash
import jwt
import config
from .json_handler import Json
import os
from .cloud import Cloud

class ClientBase:
    def __init__(self):
        self.setting_json = Json("settings.json")
        self._setting_setup()

    def __repr__(self) -> str:
        return (
            f"<system_handler.ClientBase>"
        )

    def __str__(self) -> str:
        return f"<system_handler.ClientBase>"

    def _setting_setup(self):
        if not os.path.isfile(self.setting_json.file):
            self.setting_json.update("cloud_path", ".")

    def login_check(self) -> bool:
        if not session.get("login"): return False
        login_data = session.get("login")
        datas = jwt.decode(login_data, "secret", algorithms=["HS256"])
        if str(datas["_id"]) == str(config.CloudSettings.admin_id) and str(datas["_admin"]): return True
        session.pop("login")
        return False

    async def login(self, id: str, password: str):
        if session.get("login"): raise Error.AlreadyLogin("I'm already logged in.")
        if not str(id) == config.CloudSettings.admin_id or not str(password) == config.CloudSettings.admin_password: raise Error.LoginFailed("Missing ID or password does not match.")
        session["login"] = jwt.encode({"_id": str(config.CloudSettings.admin_id), "_admin": True}, "secret", algorithm="HS256")

    async def logout(self):
        if not session.get("login"): raise Error.AlreadyLogin("I haven't logged in yet.")
        session.pop("login")

    async def set_path(self, path: str):
        if not os.path.isdir(path): raise Error.NotFound("There is no path.")
        self.setting_json.update("cloud_path", path)

    def _byte_transform(self, bytes:int, to:str, lens:int = 0, bsize = 1024):
        a = {'k': 1, 'm': 2, 'g': 3, 't': 4, 'p': 5, 'e': 6, 'K': 1, 'M': 2, 'G': 3, 'T': 4, 'P': 5, 'E': 6}
        r = float(bytes)
        for i in range(a[to]): r = r / bsize
        return round(r, lens)


class Client(ClientBase):
    def __init__(self):
        super().__init__()
        self.base = super()
        self.cloud = Cloud()

    def __repr__(self) -> str:
        return (
            f"<system_handler.Client>"
        )

    def __str__(self) -> str:
        return f"<system_handler.Client>"

    @property
    def login_check(self) -> bool:
        """
        ?????? ???????????? ????????? ???????????? ???????????????.

        Returns
        --------
        bool (True or False)
        """
        return self.base.login_check()

    async def login(self, id: str, password: str):
        """
        ?????? ???????????? ?????????.

        Parameters
        ----------
        id: str
            ????????? ????????? ????????? ????????? id
        password: str
            ????????? ????????? ????????? ????????????
        """

        await self.base.login(id, password)

    async def logout(self):
        """
        ??????????????? ?????????.

        Raises
        -------
        Error.AlreadyLogin
            ???????????? ?????? ???????????? ???????????????.
        """
        await self.base.logout()

    async def set_path(self, path: str):
        """
        ??????????????? ?????? ????????? ???????????????.

        Raises
        -------
        Error.NotFound
            ????????? ????????? ???????????? ???????????????.
        """
        await self.base.set_path(path)