#-*- coding:utf-8 -*-
class Error:
    class LoginFailed(Exception):
        """
        계정 로그인에 실패하였습니다.
        """
        pass

    class AlreadyLogin(Exception):
        """
        이미 로그인한 상태이거나 미로그인상태 입니다.
        """
        pass

    class AlreadyExists(Exception):
        """
        계정 생성또는 데이터 생성시 이미 중복된 데이터가 있을경우 발생하는 버그입니다.
        """
        pass

    class NotFound(Exception):
        """
        데이터가 없거나 할경우 발생합니다.
        """
        pass

    class Forbidden(Exception):
        """
        권한이 없을경우 발생합니다.
        """
        pass