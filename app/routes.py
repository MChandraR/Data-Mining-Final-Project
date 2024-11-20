from . import controller as ct

class Routes:
    def __init__(self, app):
        app.add_url_rule("/",'home', ct.index)
        app.add_url_rule("/login",'login', ct.login, methods=["POST"])