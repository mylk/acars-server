import os

environment = os.environ.get('ENV')

if environment == 'production':
    import acarsserver.config.environments.production as env
elif environment == 'development':
    import acarsserver.config.environments.development as env
elif environment == 'test':
    import acarsserver.config.environments.test as env
else:
    raise RuntimeError('Environment not set or incorrect.')

server = env.server
debug = env.debug
reloader = env.reloader
db_url = env.db_url
db_echo = env.db_echo
logging_level = env.logging_level
listener_host = env.listener_host
listener_port = env.listener_port
queue_host = env.queue_host
