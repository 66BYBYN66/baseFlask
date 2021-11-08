import datetime

# адрес сервака
host = "http://127.0.0.1:5000/"
# подключение к бд для механизма входа и регестрации
connectionDbInOneRow = "mysql+pymysql://root:42ghbdtn@localhost/site"
# подключение для pymysql
hostDb = 'localhost'
loginDb = 'root'
passwordDb = '42ghbdtn'
database = 'site'


class Configuration(object):
    DEBUG = True
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "ghjergherjk4w3eh%^DS*&(@"
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=365)

    SQLALCHEMY_DATABASE_URI = connectionDbInOneRow

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'ArbitrationCryptocurrencyRates@gmail.com'
    MAIL_DEFAULT_SENDER = 'ArbitrationCryptocurrencyRates@gmail.com'
    MAIL_PASSWORD = "Cx`n%Rhbgns_2009"