import pathlib
import pandas as pd
import os
import re
from CSVTransformer import CSVTransformer
from BaseTable import BaseTable
from sqlalchemy import create_engine

class FileManager():    
	'''Class to manage the read/write files

    Constructor arguments:
    TODO

    Cohort needs to have at least 2 files
    - The patient data file
    - The observations/measurements
    '''
	def __init__(self, args):
		self.args 			= args
		self.columnsMapping = self.__readUSAGIMapping(args.columnsmapping, args.usagisep)
		pathlib.Path(args.results).mkdir(parents=True, exist_ok=True) 

	def readCohort(self, fileName):
		return pd.read_csv('{}{}'.format(self.args.cohortdest, fileName), na_values='null', sep=self.args.cohortsep)

	def getColumnsMappingBySourceCode(self, sourceCode, sourceNameAsKey=False):
		#Split by mark, because the file name used in the Usagi was the original and here is the transformed
		conceptToSearch = sourceCode.split(CSVTransformer.MARK)[1] 
		fileredRowsByDomain = self.columnsMapping[self.columnsMapping['sourceCode'].str.contains(conceptToSearch)]
		print(fileredRowsByDomain)
		fileredRows = fileredRowsByDomain[['sourceName','targetConceptName']]
		return self.__getDictOfMappingColumns(fileredRows, sourceNameAsKey)

	def __readUSAGIMapping(self, file, sep):
		columnsToRead = ["sourceCode", "sourceName", "targetConceptId", "targetConceptName", "targetDomainId"]
		fileContent = pd.read_csv(file, na_values='null', sep=self.args.usagisep)
		try:
			return fileContent.loc[:, columnsToRead]
		except:
			raise Exception("It was not possible allocate the columns to the file, "
				"maybe the select CSV column separator is wrong!")

	def writeResults(self, results, configuration):
		for table in results:
			results[table].to_csv('{}{}.csv'.format(self.args.results, table), index=False)

		if self.args.writeindb or self.args.appendindb:
			engine = create_engine(self.args.db["datatype"]+"://"+self.args.db["user"]+":"+self.args.db["password"]+"@"+self.args.db["server"]+":"+self.args.db["port"]+"/"+self.args.db["database"])
			
			if not self.args.appendindb:
				try:
					sqlCmd = ""
					for cls in BaseTable.__subclasses__():
						tableName = re.sub( '(?<!^)(?=[A-Z])', '_', cls.__name__ ).lower()
						sqlCmd += "TRUNCATE TABLE " + self.args.db["schema"] + "." + tableName + "; "
					engine.execute(sqlCmd)
				except:
				    raise Exception("The switchbox database connection credentials are not found or incorrect")

			for table in results:
				results[table].to_sql(table, engine, if_exists 	= 'append',
													 index 		= False,
													 schema 	= self.args.db["schema"],
													 dtype 		= BaseTable.getDataTypesForSQL(table))

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