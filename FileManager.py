import configparser
import pandas as pd

class FileManager():
	def __init__(self, args):
		self.settings 			= self.__readSettings(args.settings)
		self.columnsMapping 	= self.__readUSAGIMapping(args.columns, args.sep)
		self.contentMapping 	= self.__readUSAGIMapping(args.measures, args.sep) if args.measures != "" else None
		self.cohort 			= self.__readCohort(args.input, args.sep)
		self.resulsDir			= args.results

	def __readSettings(self, settingsFile):
		configuration = configparser.ConfigParser()
		configuration.read(settingsFile)
		if not configuration:
			raise Exception("The settings file was not found!")
		return configuration

	def __readUSAGIMapping(self, file, sep):
		columnsToRead = ["sourceName", "targetConceptId", "targetConceptName", "targetDomainId"]
		fileContent = pd.read_csv(file, na_values='null', sep=sep)
		try:
			return fileContent.loc[:, columnsToRead]
		except:
			raise Exception("It was not possible allocate the columns to the file, " \
				"maybe the select CSV column separator is wrong!")

	def __readCohort(self, file, sep):
		return pd.read_csv(file, na_values='null', sep=sep)

	def getSystemSettings(self):
		return self.settings

	def getColumnsMappingByDomain(self, domain):
		fileredRows = self.columnsMapping[self.columnsMapping['targetDomainId'].str.contains(domain)]
		return fileredRows['sourceName'].tolist()

	def getContentMapping(self):
		return self.contentMapping

	def getCohort(self):
		return self.cohort

	def writeResults(self, results, configuration):
		print ("TO DO - write results")
		#persons.to_csv('results/{}person.csv'.format(write_path), index=False)
		#persons.to_sql("person", engine, if_exists='append',index=False,schema='omopcdm',dtype=
		