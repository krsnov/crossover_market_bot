import configparser

config_file = 'bots.conf'

config = configparser.ConfigParser()
config.read(config_file)

db_connection_string = config['bots']['db_dsn']