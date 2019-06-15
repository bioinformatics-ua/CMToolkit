import pathlib
import pandas as pd
import os

class FileManager():    
	'''Class to manage the read/write files

    Constructor arguments:
    TODO

    Cohort needs to have at least 2 files
    - The patient data file
    - The observations/measurements
    '''
	def __init__(self, args):
		self.columnsMapping 	= self.__readUSAGIMapping(args.columns, args.usagisep)
		self.contentMapping 	= self.__readUSAGIMapping(args.measurements, args.usagisep) if args.measurements != None else pd.DataFrame()
		self.cohort 			= self.__readCohort(args)
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

	def __readCohort(self, args):
		sep = args.cohortsep if args.cohortsep != "\\t" else "\t"
		cohortDir = args.cohortdir[:-1] if args.cohortdir.endswith("/") else args.cohortdir
		cohort = {}
		cohort["person"] = pd.read_csv('{}/{}'.format(cohortDir, args.patientcsv), na_values='null', sep=sep)
		cohort["observation"] = pd.read_csv('{}/{}'.format(cohortDir, args.obscsv), na_values='null', sep=sep)
		return cohort


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
		columns = fileredRows['sourceName'].drop_duplicates().reset_index(drop=True).tolist()
		return columns, dictOfMappingColumns

	def getContentMapping(self):
		if(not self.contentMapping.empty):
			return self.contentMapping[["sourceCode", "sourceName", "targetConceptId"]]
		return None

	def getCohort(self):
		return self.cohort