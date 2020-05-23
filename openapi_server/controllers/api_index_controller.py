from openapi_server.models.request_add_address_model import RequestAddAddressModel  # noqa: E501
from openapi_server.models.request_upload_text_model import RequestUploadTextModel  # noqa: E501
from openapi_server.models.response_add_address_model import ResponseAddAddressModel  # noqa: E501
from openapi_server.models.response_tx_model import ResponseTxModel  # noqa: E501
from openapi_server.models.response_upload_text_model import ResponseUploadTextModel  # noqa: E501
from openapi_server import util

from pymongo import DESCENDING, ASCENDING
import connexion
import six
import multiprocessing
from openapi_server import app, mongo, bootstrap

def index():  # noqa: E501
    # """get transactions.

    # get transaction from mongodb. # noqa: E501

    # :param addr: bitcoin sv address
    # :type addr: str
    # :param start_index: start index ( default is 0 )
    # :type start_index: int
    # :param count: get transaction count ( default is 5 )
    # :type count: int

    # :rtype: List[ResponseTxModel]
    # """
    return 'do some magic!'