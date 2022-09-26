from main import app
from waitress import serve

print(__name__)
if __name__ == '__main__':
    serve(app)