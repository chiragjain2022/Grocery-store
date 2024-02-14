
class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):

    SQLALCHEMY_DATABASE_URI = 'sqlite:///store.db'
    CATEGORY_UPLOAD_FOLDER = 'static/uploads/category'
    PRODUCT_UPLOAD_FOLDER = 'static/uploads/product'
    DEBUG = True
    SECRET_KEY =  "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"

