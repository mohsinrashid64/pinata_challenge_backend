from flask import Blueprint

test_bp = Blueprint('test', __name__)

@test_bp.route('/test', methods=['GET'])
def test():
    return {'HEY THERE': 'HEY THERE'}
