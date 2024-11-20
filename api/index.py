import sys, os
sys.path.append(os.path.abspath(os.path.join('..', '')))
print(os.path.abspath(os.path.join('..', 'app')))
from app import App

app = App(__name__) 

# if __name__ == '__main__':
#     app.run(
#         os.environ["HOST"],
#         os.environ["PORT"],
#         debug=os.environ["DEBUG"]
#     )
