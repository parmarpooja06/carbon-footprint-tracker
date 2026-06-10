class Config:
    SECRET_KEY = "carbontracker123"

    SQLALCHEMY_DATABASE_URI = "sqlite:///carbon.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False