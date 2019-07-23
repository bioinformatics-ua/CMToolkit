import configparser
import argparse
from Args import Args

class TranSMARTArgs(Args):
	'''Class design to deal with the args for the TranSMART mapper

    Constructor arguments:
    :param args: The args received from the args_parse
    '''
	def __init__(self, args):
		super(MigratorArgs, self).__init__(args = args) 
		self.cohortoutputfile 	= self.__defineArg(args, "cohortoutputfile")
		self.transmartdstdir	= super().argAsDir(self.__defineArg(args, "transmartdstdir"))
		self.protegeoutput		= self.__defineArg(args, "protegeoutput")		
		self.cohortname			= self.__defineArg(args, "cohortname")

	def __defineArg(self, args, arg):
		if (hasattr(args, arg)):
			if(getattr(args, arg)):
				return getattr(args, arg)
		if (arg in self.settings["transmart"]):
			return self.settings["transmart"][arg]
		return None

	def help(show=False):
	    parser = argparse.ArgumentParser(description='From OMOP CDM to TranSMART mapper')
	    configs = parser.add_argument_group('Global settings', 'All the following methods can be defined in the settings file. However, if a parameters is set it will override the same paramenter in the settings file.')
	    configs.add_argument('-co', '--cohortoutput', dest='cohortoutputfile', type=str, \
	                        help='The TSV file which contains the cohort row data to be loaded into the TranSMART (for instance: Transmart.tsv)')
	    configs.add_argument('-cn', '--cohortname', dest='cohortname', type=str, \
	                        help='The name of the cohort that will be displayed in the TranSMART')
	    configs.add_argument('-po', '--protegeoutput', dest='protegeoutput', type=str, \
	                        help='The protege output file resulting from the The Hyve scripts')
	    configs.add_argument('-dd', '--dstdir', dest='transmartdstdir', type=str, \
	                        help='The destination directory to create all the files (cohort, mappings and settings)')

	    #configs.add_argument('-', '--', dest='', type=str, \
	    #                   help='The  ')

	    if show:
	    	parser.print_help()
	    return parser.parse_args()