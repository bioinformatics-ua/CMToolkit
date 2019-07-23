import configparser
import argparse

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Args(object, metaclass=Singleton):
	'''Class design to be the base of the classes which will deal with the args
	 and the settings file from the different applications
	Note: This is a singleton so I can easly access any of these variables in the code

    Constructor arguments:
    :param args: The args received from the args_parse
    '''
	def __init__(self, args):
		self.settings 			= self.readSettings(args.settings)

		#DB
		self.db 				= self.settings["database"]

	def argAsDir(self, arg):
		return arg if arg.endswith("/") else arg + "/"
	
	def readSettings(self, settingsFile):
		configuration = configparser.ConfigParser()
		configuration.read(settingsFile)
		if not configuration:
			raise Exception("The settings file was not found!")
		return configuration

	def getDBConfigs(self):
		return self.settings["database"]
	