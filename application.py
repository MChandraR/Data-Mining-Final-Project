import os
from app import App
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()
app = App(__name__) 
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
 
if __name__ == '__main__':
    app.run(
        os.environ["HOST"],
        os.environ["PORT"],
        debug=os.environ["DEBUG"]
    )
