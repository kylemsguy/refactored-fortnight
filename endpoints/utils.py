from flask.blueprints import Blueprint

root = Blueprint('root', __name__,
                 template_folder='templates',
                 static_folder='static')

api = Blueprint('api', __name__,
                 template_folder='templates',
                 static_folder='static')