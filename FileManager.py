import pathlib
import pandas as pd
import os

class FileManager():
	def __init__(self, args):
		self.columnsMapping 	= self.__readUSAGIMapping(args.columns, args.usagisep)
		self.contentMapping 	= self.__readUSAGIMapping(args.measurements, args.usagisep) if args.measurements != None else None
		self.cohort 			= self.__readCohort(args.cohort, args.cohortsep)
		self.resulsDir			= args.results[:-1] if args.results.endswith("/") else args.results
		
		pathlib.Path(self.resulsDir).mkdir(parents=True, exist_ok=True) 


	def __readUSAGIMapping(self, file, sep):
		sep = sep if sep != "\\t" else "\t"
		columnsToRead = ["sourceCode", "sourceName", "targetConceptId", "targetConceptName", "targetDomainId"]
		fileContent = pd.read_csv(file, na_values='null', sep=sep)
		try:
			return fileContent.loc[:, columnsToRead]
		except:
			raise Exception("It was not possible allocate the columns to the file, " \
				"maybe the select CSV column separator is wrong!")

	def __readCohort(self, inputCohort, sep):
		sep = sep if sep != "\\t" else "\t"
		if os.path.isfile(inputCohort):
			return pd.read_csv(inputCohort, na_values='null', sep=sep)
		else:
			for file in os.listdir(inputCohort):
				print(file)


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