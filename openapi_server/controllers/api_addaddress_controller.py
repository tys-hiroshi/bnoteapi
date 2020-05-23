import connexion
import six

from openapi_server.models.request_add_address_model import RequestAddAddressModel  # noqa: E501
from openapi_server.models.request_upload_text_model import RequestUploadTextModel  # noqa: E501
from openapi_server.models.response_add_address_model import ResponseAddAddressModel  # noqa: E501
from openapi_server.models.response_tx_model import ResponseTxModel  # noqa: E501
from openapi_server.models.response_upload_text_model import ResponseUploadTextModel  # noqa: E501
from openapi_server import util

from openapi_server import app, mongo, bootstrap

def api_addaddress(body):  # noqa: E501
    """/api/address

     # noqa: E501

    :param body: request /api/add_address
    :type body: dict | bytes

    :rtype: ResponseAddAddressModel
    """
    # if connexion.request.is_json:
    #     body = RequestAddAddressModel.from_dict(connexion.request.get_json())  # noqa: E501
    # return 'do some magic!'
    try:
        if connexion.request.is_json:
            body = RequestAddAddressModel.from_dict(connexion.request.get_json())  # noqa: E501
        print(connexion.request.headers['Content-Type'])
        if connexion.request.headers['Content-Type'] != 'application/json':
            print(app.app.request.headers['Content-Type'])
            return {}, 400
        address = body.address
        if address == None or address == "":
            return {}, 400
        record_address = mongo.db.address.find({"address": address})
        if record_address.count() == 0:
            mongo.db.address.insert({"address": address})
        return ResponseAddAddressModel(0, "success").to_dict(), 200
    except Exception as e:
        app.app.logger.error(e)
        print(e)
        return {}, 500
