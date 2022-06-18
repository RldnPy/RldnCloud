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
    """

    admin_id = ""
    admin_password = "@"

    del_user = True


class Debug:
    debug = False
    version = "1.0"

    open_url = ""
    port = 5000
    url = ""