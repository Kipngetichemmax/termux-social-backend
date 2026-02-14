from flask import Blueprint
feed_bp = Blueprint('feed', __name__)

@feed_bp.route('/', methods=['GET'])
def get_feed():
    return {"feed": []}

