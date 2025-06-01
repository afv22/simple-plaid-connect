import os
from dotenv import load_dotenv

from waitress import serve

from app import create_app

if __name__ == "__main__":
    load_dotenv(override=True)
    host, port = "0.0.0.0", os.getenv("PORT", 5001)
    print(f"Serving app on http://{host}:{port}")
    serve(create_app(), host=host, port=port)
