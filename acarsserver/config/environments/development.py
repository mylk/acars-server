import logging

# server backend
web_server = 'cherrypy'
# debug error messages
web_debug = True
# auto-reload
web_reloader = True
web_root_path = ''

# database url
db_url = 'sqlite:///acarsserver/db/db.sqlite3'
# echo database engine messages
db_echo = True

logging_level = logging.DEBUG

# the host and port of the listener
# that receives the data from the client
listener_host = 'listener'
listener_port = 5555

queue_host = 'rabbitmq'
