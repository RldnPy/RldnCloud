#-*- coding:utf-8 -*-
class WebSettings:
    """
    웹 설정
    open_url: 열려는 주소
    port: 열려는 포트
    url: 웹의 주소

    database: 데이터 베이스 파일 이름
    """

    open_url = "0.0.0.0"
    port = 80
    url = ""

    database = "database.db"


class CloudSettings:
    """
    클라우드 시스템 설정

    admin_id: 관리자 계정 ID
    admin_password: 관리자 계정 비밀번호
    del_user: 파일 삭제시 사용자 확인 페이지 활성화 여부 (True/False)

    preview_ban: 파일 미리보기에서 불가능하도록할 확장자 (List[Str])
    """

    admin_id = ""
    admin_password = ""
    del_user = True

    preview_ban = ["html", "php", "mhtml", "htm", "rfc822"]


class Debug:
    """
    개발을 위해 있는 부분입니다.
    수정할 경우 시스템에 문제가 생길수 있습니다.
    """
    debug = False
    version = "1.1.5"
    version_day = "220709"

    open_url = ""
    port = 5000
    url = ""