from bottle import TEMPLATE_PATH
import sys

import acarsserver

sys.path = ['../../..'] + sys.path


def get_app():
    TEMPLATE_PATH.insert(0, '../../../app/views')
    return acarsserver.AcarsServer(web_debug=False).app
