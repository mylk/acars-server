import sys

sys.path = ['../../..'] + sys.path

import acarsserver


def get_app():
    return acarsserver.AcarsServer(template_path='../../app/views/').app
