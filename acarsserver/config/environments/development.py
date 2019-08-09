import logging

# server backend
server = 'cherrypy'

# debug error messages
debug = True

# auto-reload
reloader = True

# database url
db_url = 'sqlite:///acarsserver/db/db.sqlite3'

# echo database engine messages
db_echo = True

logging_level = logging.DEBUG

# the host and port of the listener
# that receives the data from the client
listener_host = 'listener'
listener_port = 5555

queue_host = 'localhost'
