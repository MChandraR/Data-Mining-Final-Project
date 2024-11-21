from . import controller as ct

class Routes:
    def __init__(self, app):
        app.add_url_rule("/",'home', ct.index)
        app.add_url_rule("/register",'regist', ct.regist)
        app.add_url_rule("/input",'input', ct.input, methods=["POST", "GET"])
        app.add_url_rule("/login",'login', ct.login, methods=["POST"])
        app.add_url_rule("/penjualan",'penjualan', ct.getPenjualan, methods=["GET"])