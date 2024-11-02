from app.controllers.nids_controllers import predict
from flask import Blueprint

nids_bp = Blueprint('nids', __name__)

nids_bp.route('/predict', methods=['POST'])(predict)



