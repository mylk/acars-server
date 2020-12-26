import os

environment = os.environ.get('ENV')

if environment == 'production':
    import acarsserver.config.environments.production as env
elif environment == 'development':
    import acarsserver.config.environments.development as env
elif environment == 'test':
    import acarsserver.config.environments.test as env

web_server = env.web_server
web_debug = env.web_debug
web_reloader = env.web_reloader
web_root_path = env.web_root_path
db_url = env.db_url
db_echo = env.db_echo
logging_level = env.logging_level
logging_file = env.logging_file
listener_host = env.listener_host
listener_port = env.listener_port
queue_host = env.queue_host
environment = env.environment
