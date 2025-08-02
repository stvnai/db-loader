from app import create_app
from app.set_logging import set_logging

set_logging()

app= create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002, debug=True)
 