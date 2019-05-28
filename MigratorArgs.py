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
		self.cohort 		= self.__defineArg(args, "cohort")
		self.patientcsv 	= self.__defineArg(args, "patientcsv")
		self.columns 		= self.__defineArg(args, "columns")
		self.measurements 	= self.__defineArg(args, "measurements")
		self.cohortsep 		= self.__defineArg(args, "cohortsep")
		self.usagisep 		= self.__defineArg(args, "usagisep")
		self.results 		= self.__defineArg(args, "results")

	def __defineArg(self, args, arg):
		if (hasattr(args, arg)):
			if(getattr(args, arg)):
				return getattr(args, arg)
		if (arg in self.settings["cohortinfo"]):
			return self.settings["cohortinfo"][arg]
		return None
	
	def __readSettings(self, settingsFile):
		configuration = configparser.ConfigParser()
		configuration.read(settingsFile)
		if not configuration:
			raise Exception("The settings file was not found!")
		return configuration
		
	def getDBConfigs(self):
		return self.settings["database"]
	
	def help():
	    parser = argparse.ArgumentParser(description='Cohort mapper')
	    parser.add_argument('-i', '--input', dest='cohort', type=str, \
	                        help='The input can be a cohort CSV file or a dir with all CSV files')
	    parser.add_argument('-p', '--patientcsv', dest='patientcsv', type=str, \
	                        help='The CSV file with the patient information. Used only in cohorts splitted by several files.')

	    parser.add_argument('-c', '--columns', dest='columns', type=str, \
	                        help='The USAGI output file in CSV format with the column mapping')
	    parser.add_argument('-m', '--measurements', dest='measurements', type=str, \
	                        help='The USAGI output file in CSV format with the cohort content harmonized')

	    parser.add_argument('-b', '--cohortsep', dest='cohortsep', type=str, \
	                        help='The separator used in the cohort CSV files')
	    parser.add_argument('-u', '--usagisep', dest='usagisep', type=str, \
	                        help='The separator used in the USAGI output files')

	    parser.add_argument('-r', '--results', dest='results', type=str, \
	                        help='The path to write the CSV tables with the cohort migrated to OMOP CDM v5 ')
	    
	    parser.add_argument('-s', '--settings', dest='settings', \
	                        type=str, default="settings.ini", \
	                        help='The system settings file (default: settings.ini)')
	    return parser.parse_args()