import ConfigParser

config = ConfigParser.ConfigParser()
config.read('config.ini')

username = config.get('main', 'username')
password = config.get('main', 'password')
ws_uri = config.get('main', 'ws_uri')
