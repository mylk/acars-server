import logging

# server backend
server = 'cherrypy'
# debug error messages
debug = False
# auto-reload
reloader = False
web_root_path = '/acars-server'

# database url
db_url = 'sqlite:///acarsserver/db/db.sqlite3'
# echo database engine messages
db_echo = False

logging_level = logging.INFO

# the host and port of the listener
# that receives the data from the client
listener_host = 'listener'
listener_port = 5555

queue_host = 'rabbitmq'
