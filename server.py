import os
from app import App
from dotenv import load_dotenv

load_dotenv()

app = App(__name__) 
 
if __name__ == '__main__':
    app.run(
        os.environ["HOST"],
        os.environ["PORT"],
        debug=os.environ["DEBUG"]
    )
