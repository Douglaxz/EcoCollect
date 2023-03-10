# importação de dependencias
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import generate_password_hash, Bcrypt
from flask_qrcode import QRcode
from flask_googlemaps import GoogleMaps


# definição de chave
app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

qrcode = QRcode(app)

# you can set key as config
app.config['GOOGLEMAPS_KEY'] = "AIzaSyA7bWAPSaIKv-8Q0X3g-G2m385_r_-Vcvs"


# Initialize the extension
GoogleMaps(app)

from views import *

if __name__ == '__main__':
    app.run(debug=True)