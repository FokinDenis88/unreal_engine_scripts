import configparser

INI_SECTION_MAIN = 'General'

def read_ini(path):
    config_parser = configparser.ConfigParser()
    config_parser.read(path)
    return config_parser