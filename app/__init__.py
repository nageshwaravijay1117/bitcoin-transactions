import logging
import platform
import string
from importlib import import_module
from logging.handlers import RotatingFileHandler

from flask import Blueprint, Flask
from flask_compress import Compress
from flask_jwt import JWT
from flask_restful import Api
from flask_cors import CORS

compress = Compress()
API_URL_PREFIX = '/api'
api_blueprint = Blueprint('api', __name__)

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

api = Api(
    app=api_blueprint,
    prefix = API_URL_PREFIX,
    catch_all_404s=True
)



from app.transactions.transactions import Transaction
from app.address.address import HighValueAddress
from app.transactions_per_minute.transactions_per_minute import TransactionPerMinute,TransactionPerMinuteLastHour

api.add_resource(Transaction, '/show_transactions', endpoint='show_transactions')
api.add_resource(TransactionPerMinute, '/transactions_count_per_minute', endpoint='transactions_count_per_minute')
api.add_resource(TransactionPerMinuteLastHour, '/transactions_count_per_minute_last_hour', endpoint='transactions_count_per_minute_last_hour')
api.add_resource(HighValueAddress, '/high_value_addr', endpoint='high_value_addr')


app.register_blueprint(api_blueprint)
api.init_app(app)