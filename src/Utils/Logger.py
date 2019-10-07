import logbook
from Singleton import Singleton

WRONG_VALUE		= "[WRONG VALUE]"
WRONG_TYPE 		= "[WRONG TYPE]"
OUT_OF_RANGE 	= "[OUT OF RANGE]"
INVALID_DATE 	= "[INVALID DATE]"
MISSING_VALUE 	= "[MISSING VALUE]"

class Logger(object, metaclass=Singleton):
	'''Class to write the execution logs
    '''
	def __init__(self, args):
		self.args = args
		self.logger = logbook.Logger("{} logger".format(args.cohortname))
		log = logbook.FileHandler(args.log, mode='w')
		log.push_application()

	def info(self, msg, verbose=False):
		if verbose:
			print(msg)
		self.logger.info("\t"+msg)

	def warn(self, warnType, patientID, variable, measure="", msg="", verbose=False):
		self.logger.warn("\t"+self.__buildMsg(warnType, patientID, variable, measure, msg, verbose))

	def error(self, errorType, patientID, variable, measure="", msg="", verbose=False):
		self.logger.error("\t"+self.__buildMsg(errorType, patientID, variable, measure, msg, verbose))

	def __buildMsg(self, msgType, patientID, variable, measure, msg, verbose):
		#one day I will have problems with this shit, so in that day I can solve this :D
		patient = patientID if str(patientID).isdigit() else patientID.split(".")[0]
		finalMsg = "{}\tPatient id: {}\tVariable: {}\t".format(msgType, patient, variable)
		if measure != "":
			finalMsg += "Measure: {}".format(measure)
		finalMsg += "\t"
		if msg != "":
			finalMsg += "Message: {}".format(msg)
		if verbose:
			print(finalMsg)
		return finalMsg