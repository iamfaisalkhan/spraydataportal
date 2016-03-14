import ConfigParser
import logging
import os


class Config(dict):

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('SprayData')

    def __init__(self, args, cli = None):
        self.dict = {}
        self['keymap'] = {}
        self['mongodb'] = {}

        self.build(args.configPath)
        
        if args.datasetName:
            self['datasetName'] = args.datasetName
        else:
            self['datasetName'] = None

    def build(self, configPath):
        if not configPath:
            configPath = 'spraydata_config'

        if not os.path.isfile(configPath):
            Config.logger.debug('config file does not exist')
            return 

        try:
            parser = ConfigParser.RawConfigParser(allow_no_value = True)
            parser.read(configPath)

            for item in parser.items('general'):
                self[item[0].lower()] = item[1]

            for section in ['keymap', 'mongodb']:
                for item in parser.items(section):
                    self[section][item[0].lower()] = item[1]

        except Exception, e:
            Config.logger.error('Failed to read config file', exc_info=True)