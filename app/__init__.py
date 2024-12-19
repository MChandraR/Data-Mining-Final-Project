from flask import Flask, render_template
from . import routes
import os

class App(Flask):
    def __init__(self,__name__):
        Flask.__init__(
            self, 
            __name__,
            template_folder=os.path.abspath(os.path.join('app/templates')), 
            static_folder=os.path.abspath(os.path.join('app/static'))
        )
        self.secret_key = '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'  # Gunakan secret key untuk session

        self.routes = routes.Routes(self)
        

        
        
        
        
        
        