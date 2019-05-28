import configparser
import pathlib
import pandas as pd
import os

class FileManager():
	def __init__(self, args):
		self.settings 			= self.__readSettings(args.settings)
		self.columnsMapping 	= self.__readUSAGIMapping(args.columns, args.sep)
		self.contentMapping 	= self.__readUSAGIMapping(args.measures, args.sep) if args.measures != "" else None
		self.cohort 			= self.__readCohort(args.input, args.sep)
		self.resulsDir			= args.results[:-1] if args.results.endswith("/") else args.results
		
		pathlib.Path(self.resulsDir).mkdir(parents=True, exist_ok=True) 

	def __readSettings(self, settingsFile):
		configuration = configparser.ConfigParser()
		configuration.read(settingsFile)
		if not configuration:
			raise Exception("The settings file was not found!")
		return configuration

	def __readUSAGIMapping(self, file, sep):
		columnsToRead = ["sourceCode", "sourceName", "targetConceptId", "targetConceptName", "targetDomainId"]
		fileContent = pd.read_csv(file, na_values='null', sep=sep)
		try:
			return fileContent.loc[:, columnsToRead]
		except:
			raise Exception("It was not possible allocate the columns to the file, " \
				"maybe the select CSV column separator is wrong!")

	def __readCohort(self, file, sep):
		if os.path.isfile(file):
			return pd.read_csv(file, na_values='null', sep=sep)
		else:
			raise Exception("TO DO!")

	def writeResults(self, results, configuration):
		for table in results:
			#print(results[table])
			results[table].to_csv('{}/{}.csv'.format(self.resulsDir, table), index=False)
			
			#table.to_sql(table, engine, if_exists='append',
			#							index=False,
			#							schema='sbcdm',
			#							dtype=todo)

    ####################
    ### 	Gets 	 ###
    ####################
	def getSystemSettings(self):
		return self.settings

	def getColumnsMappingByDomain(self, domain, sourceNameAsKey=False):
		fileredRowsByDomain = self.columnsMapping[self.columnsMapping['targetDomainId'].str.contains(domain)]
		fileredRows = fileredRowsByDomain[['sourceName','targetConceptName']]
		return self.__getDictOfMappingColumns(fileredRows, sourceNameAsKey)

	def __getDictOfMappingColumns(self, fileredRows, sourceNameAsKey):
		if(sourceNameAsKey):
			dictOfMappingColumns = pd.Series(fileredRows["targetConceptName"].values, index=fileredRows['sourceName']).to_dict()
		else:
			dictOfMappingColumns = pd.Series(fileredRows["sourceName"].values, index=fileredRows['targetConceptName']).to_dict()
		return fileredRows['sourceName'].tolist(), dictOfMappingColumns

	def getContentMapping(self):
		return self.contentMapping[["sourceCode", "sourceName", "targetConceptId"]]

	def getCohort(self):
		return self.cohort