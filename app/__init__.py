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
        self.routes = routes.Routes(self)
        

        
        
        
        
        
        