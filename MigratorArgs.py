import configparser
import argparse

class MigratorArgs(object):
	'''Class design to deal with the args and the settings file
	Note: When added a new arg in the help function, it is necessary add a new 
	entry in the constructor

    Constructor arguments:
    :param args: The args received from the args_parse
    '''
	def __init__(self, args):
		self.settings 		= self.__readSettings(args.settings)
		self.transformcsv   = args.transform
		self.migrate   		= args.migrate
		self.cohortdir		= self.__defineArg(args, "cohortdir")
		self.headers		= self.__defineArg(args, "headers")
		self.measures 		= self.__defineArg(args, "measures")
		self.cohortdest 	= self.__defineArg(args, "cohortdest")
		sep 				= self.__defineArg(args, "cohortsep")
		self.cohortsep 		= '\t' if sep == "\\t" else sep

		self.cohortdir 		= self.__defineArg(args, "cohortdir")
		self.patientcsv 	= self.__defineArg(args, "patientcsv")
		self.obscsv 		= self.__defineArg(args, "obscsv")
		self.columns 		= self.__defineArg(args, "columns")
		self.measurements 	= self.__defineArg(args, "measurements")
		self.usagisep 		= self.__defineArg(args, "usagisep")
		self.results 		= self.__defineArg(args, "results")


	def __defineArg(self, args, arg):
		if (hasattr(args, arg)):
			if(getattr(args, arg)):
				return getattr(args, arg)
		if (arg in self.settings["cohortinfo"]):
			return self.settings["cohortinfo"][arg]
		if (arg in self.settings["cohorttransformation"]):
			return self.settings["cohorttransformation"][arg]
		return None
	
	def __readSettings(self, settingsFile):
		configuration = configparser.ConfigParser()
		configuration.read(settingsFile)
		if not configuration:
			raise Exception("The settings file was not found!")
		return configuration

	def getDBConfigs(self):
		return self.settings["database"]
	
	def help(show=False):
	    parser = argparse.ArgumentParser(description='Cohort mapper arguments')
	    configs = parser.add_argument_group('Global settings', 'Some of the global settings. More settings in the settings file')
	    configs.add_argument('-i', '--cohortdir', dest='cohortdir', type=str, \
	                        help='The dir with all CSV files related to the cohort')
	    """
	    parser.add_argument('-p', '--patientcsv', dest='patientcsv', type=str, \
	                        help='The CSV file with the patient information.')
	    parser.add_argument('-o', '--obscsv', dest='obscsv', type=str, \
	                        help='The CSV file with the observations.')

	    parser.add_argument('-c', '--columns', dest='columns', type=str, \
	                        help='The USAGI output file in CSV format with the column mapping')
	    parser.add_argument('-m', '--measurements', dest='measurements', type=str, \
	                        help='The USAGI output file in CSV format with the cohort content harmonized')

	    parser.add_argument('-b', '--cohortsep', dest='cohortsep', type=str, \
	                        help='The separator used in the cohort CSV files')
	    parser.add_argument('-u', '--usagisep', dest='usagisep', type=str, \
	                        help='The separator used in the USAGI output files')
		"""
	    configs.add_argument('-r', '--results', dest='results', type=str, \
	                        help='The path to write the CSV tables with the cohort migrated to OMOP CDM v5 ')
	    
	    configs.add_argument('-s', '--settings', dest='settings', \
	                        type=str, default="settings.ini", \
	                        help='The system settings file (default: settings.ini)')

	    executionMode = parser.add_argument_group('Execution Mode', 'Flags to select the execution mode!')
	    executionMode.add_argument('-t', '--transform', default=False, action='store_true', \
	                        help='Setting this true to transform the cohort, step 4 (default: False)')
	    executionMode.add_argument('-m', '--migrate', default=False, action='store_true', \
	                        help='Setting this true to migrate the cohort. First transform the csv (step 4) (default: False)')
	    if show:
	    	parser.print_help()
	    return parser.parse_args()