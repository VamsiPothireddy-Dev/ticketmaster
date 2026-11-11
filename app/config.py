import os


class Config:
    PORT = int(os.environ.get("PORT", 8000))
