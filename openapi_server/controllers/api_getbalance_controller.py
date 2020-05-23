import connexion
import six

from openapi_server.models.response_getbalance_model import ResponseGetBalanceModel  # noqa: E501
from openapi_server import util

import multiprocessing
from openapi_server import app, mongo, bootstrap
import bitsv
from whatsonchain import api      

def api_getbalance(addr):  # noqa: E501
    """get balance from address using woc.

    get balance from address using woc. # noqa: E501

    :param body: request /api/getbalance/{addr}
    :type addr: str

    :rtype: ResponseGetBalanceModel
    """
    # if connexion.request.is_json:
    #     body = RequestMnemonicModel.from_dict(connexion.request.get_json())  # noqa: E501
    # return 'do some magic!'

    try:
        app.app.logger.info("start /api/getbalance/{addr}")
        woc = api.WhatsonchainTestNet()
        response_get_address = woc.get_balance(addr)
        responseGetBalanceModel = ResponseGetBalanceModel.from_dict(response_get_address)  # noqa: E501
        return ResponseGetBalanceModel(0, responseGetBalanceModel.confirmed, responseGetBalanceModel.unconfirmed).to_dict(), 200
    except Exception as e:
        print(e)
        return {}, 500

