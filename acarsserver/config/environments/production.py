import logging

# server backend
web_server = 'cherrypy'
# debug error messages
web_debug = False
# auto-reload
web_reloader = False
web_root_path = '/acars-server'

# database url
db_url = 'sqlite:///acarsserver/db/db.sqlite3'
# echo database engine messages
db_echo = False

logging_level = logging.INFO
logging_file = "acarsserver/log/app.log"

# the host and port of the listener
# that receives the data from the client
listener_host = 'mylk.wtf'
listener_port = 5555

queue_host = 'rabbitmq'
