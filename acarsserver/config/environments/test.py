import logging

environment = 'test'

# server backend
web_server = 'wsgiref'
# debug error messages
web_debug = True
# auto-reload
web_reloader = False
web_root_path = ''

# database url
db_url = 'sqlite:///:memory:'
# echo database engine messages
db_echo = False

logging_level = logging.DEBUG
logging_file = "acarsserver/log/app.log"

# the host and port of the listener
# that receives the data from the client
listener_host = 'localhost'
listener_port = 5555

queue_host = 'rabbitmq'
