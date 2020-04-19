import sys

import acarsserver

sys.path = ['../../..'] + sys.path


def get_app():
    return acarsserver.AcarsServer(template_path='../../../app/views/').app
