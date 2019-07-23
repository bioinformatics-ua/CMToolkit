import configparser
import argparse
from Args import Args

class MigratorArgs(Args):
	'''Class design to deal with the args for the Migrator

    Constructor arguments:
    :param args: The args received from the args_parse
    '''
	def __init__(self, args):
		super(MigratorArgs, self).__init__(args = args) 
		#Flags
		self.transformcsv   	= args.transform
		self.migrate   			= args.migrate
		self.adhocmethods		= args.adhoc
		self.writeindb	 		= args.writeindb
		self.appendindb			= args.appendindb
		self.harmonize 			= args.harmonize

		#Args
		self.cohortdir			= super().argAsDir(self.__defineArg(args, "cohortdir"))
		self.headers			= self.__defineArg(args, "headers")
		self.measures 			= self.__defineArg(args, "measures")
		self.cohortdest 		= super().argAsDir(self.__defineArg(args, "cohortdest"))
		self.harmonizedest 		= super().argAsDir(self.__defineArg(args, "cohortharmonizeddest"))
		self.patientcsv 		= self.__defineArg(args, "patientcsv")
		self.obsdir 			= super().argAsDir(self.__defineArg(args, "obsdir"))
		self.columnsmapping 	= self.__defineArg(args, "columnsmapping")
		self.contentmapping 	= self.__defineArg(args, "contentmapping")
		self.results 			= super().argAsDir(self.__defineArg(args, "results"))
		sep 					= self.__defineArg(args, "cohortsep")
		self.cohortsep 			= '\t' if sep == "\\t" else sep
		sep 					= self.__defineArg(args, "usagisep")
		self.usagisep 			= '\t' if sep == "\\t" else sep
		self.vocabulariesdir	= super().argAsDir(self.__defineArg(args, "vocabulariesdir"))

	def __defineArg(self, args, arg):
		if (hasattr(args, arg)):
			if(getattr(args, arg)):
				return getattr(args, arg)
		if (arg in self.settings["cohort_info"]):
			return self.settings["cohort_info"][arg]
		if (arg in self.settings["cohort_mappings"]):
			return self.settings["cohort_mappings"][arg]
		if (arg in self.settings["cohort_transformation"]):
			return self.settings["cohort_transformation"][arg]
		if (arg in self.settings["cohort_harmonization"]):
			return self.settings["cohort_harmonization"][arg]
		return None
	
	def help(show=False): #TODO
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
	    executionMode.add_argument('-H', '--harmonize', default=False, action='store_true', \
	                        help='Setting this true to harmonize the transformed csv files, step 5 (default: False)')
	    executionMode.add_argument('-m', '--migrate', default=False, action='store_true', \
	                        help='Setting this true to migrate the cohort. First transform and harmonize the csv (step 4 and 5) (default: False)')
	    
	    executionSettings = parser.add_argument_group('Execution Settings', 'Flags to setup some execution settings. This kind of flags are not available in the settings file!')
	    executionSettings.add_argument('-a', '--adhoc', default=False, action='store_true', \
	                        help='Active the standard ad hoc methods. Some tables have their own ad hoc tables used in several cohorts. Setting this true to use these methods. (default: False)')
	    executionSettings.add_argument('-w', '--writeindb', default=False, action='store_true', \
	                        help='Setting this true to write the cohort in the defined database. (default: False)')
	    executionSettings.add_argument('-w+', '--appendindb', default=False, action='store_true', \
	                        help='Setting this true to append the cohort in the defined database. (default: False)')
	    
	    if show:
	    	parser.print_help()
	    return parser.parse_args()