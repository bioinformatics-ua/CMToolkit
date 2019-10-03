import pathlib
import pandas as pd
import os
import re
import glob
import chardet
from BaseTable import BaseTable
from sqlalchemy import create_engine
from Singleton import Singleton

class FileManager(object, metaclass=Singleton):
	'''Class to read/write the files related with the cohort

    Constructor arguments:
    TODO

    Cohort needs to have at least 2 files
    - The patient data file
    - The observations/measurements
    '''
	def __init__(self, args):
		self.args 			= args
		self.columnsMapping = self.__readUSAGIMapping(args.columnsmapping, args.usagisep)
		self.contentMapping = self.__readUSAGIMapping(args.contentmapping, args.usagisep)
		pathlib.Path(args.results).mkdir(parents=True, exist_ok=True) 

	def readCohort(self, fileName):
		with open('{}{}'.format(self.args.cohortdest, fileName), 'rb') as f:
			result = chardet.detect(f.read())
		return pd.read_csv('{}{}'.format(self.args.cohortdest, fileName), 
						   na_values='null', 
						   sep=self.args.cohortsep, 
						   encoding=result['encoding'])#,  thousands='.', decimal=',')

	def getColumnsMappingBySourceCodeAndDomain(self, sourceCode, domain, sourceNameAsKey=False):
		fileredRowsBySourceCode = self.columnsMapping[self.columnsMapping['sourceCode'].str.contains(sourceCode)]
		fileredRowsByDomain = fileredRowsBySourceCode[fileredRowsBySourceCode['targetDomainId'].str.contains(domain)]
		fileredRows = fileredRowsByDomain[['sourceName','targetConceptName']]
		return self.__getDictOfMappingColumns(fileredRows, sourceNameAsKey)
	
	def getContentMappingBySourceCode(self, sourceCode):
		if(not self.contentMapping.empty):
			fileredRowsBySourceCode = self.contentMapping[self.contentMapping['sourceCode'].str.contains(sourceCode)]
			return fileredRowsBySourceCode[["sourceCode", "sourceName", "targetConceptId"]]
		return None	

	def getContentMapping(self, sourceCodeToIgnore):
		if(not self.contentMapping.empty):
			filteredRows = self.contentMapping
			for term in sourceCodeToIgnore:
				filteredRows = filteredRows[~filteredRows['sourceCode'].str.contains(term)]
			return filteredRows[["sourceCode", "sourceName", "targetConceptId"]]
		return None

	def toCsv(self, dataframe, destDir, destFile, sep):
		pathlib.Path(destDir).mkdir(parents=True, exist_ok=True) 
		dataframe.to_csv('{}{}'.format(destDir, destFile), sep=sep, index=False)

	def writeResults(self, results, configuration):
		for table in results:
			results[table].to_csv('{}{}.csv'.format(self.args.results, table), index=False)

		if self.args.writeindb or self.args.appendindb:
			engine = create_engine(self.args.db["datatype"]+"://"+self.args.db["user"]+":"+self.args.db["password"]+"@"+self.args.db["server"]+":"+self.args.db["port"]+"/"+self.args.db["database"])
			
			if not self.args.appendindb:
				for cls in BaseTable.__subclasses__():
					try:
						tableName = re.sub( '(?<!^)(?=[A-Z])', '_', cls.__name__ ).lower()
						sqlCmd = "TRUNCATE TABLE " + self.args.db["schema"] + "." + tableName + "; "
						engine.execute(sqlCmd)
					except:
						pass

			for table in results:
				results[table].to_sql(table, engine, if_exists 	= 'append',
													 index 		= False,
													 schema 	= self.args.db["schema"],
													 dtype 		= BaseTable.getDataTypesForSQL(table))
			self.__insertVocabularies(engine)

	def __insertVocabularies(self, engine):
		vocabulariesFiles = glob.glob('{}*.{}'.format(self.args.vocabulariesdir, "csv"))
		for file in vocabulariesFiles:
			table = file.split("/")[-1].split(".")[0].lower()
			fileContent = pd.read_csv(file, na_values='null', sep="\t")
			fileContent.to_sql(table, engine, if_exists 	= 'replace',
												 index 		= False,
												 schema 	= self.args.db["schema"],
												 dtype 		= BaseTable.getDataTypesForSQL(table))

	def __getDictOfMappingColumns(self, fileredRows, sourceNameAsKey):
		if(sourceNameAsKey):
			dictOfMappingColumns = pd.Series(fileredRows["targetConceptName"].values, index=fileredRows['sourceName']).to_dict()
		else:
			dictOfMappingColumns = pd.Series(fileredRows["sourceName"].values, index=fileredRows['targetConceptName']).to_dict()
		columns = fileredRows['sourceName'].drop_duplicates().reset_index(drop=True).tolist()
		return columns, dictOfMappingColumns

	def __readUSAGIMapping(self, file, sep):
		columnsToRead = ["sourceCode", "sourceName", "targetConceptId", "targetConceptName", "targetDomainId"]
		fileContent = pd.read_csv(file, na_values='null', sep=self.args.usagisep)
		try:
			return fileContent.astype(str).reindex(columns=columnsToRead)
		except:
			raise Exception("It was not possible allocate the columns to the file, "
				"maybe the select CSV column separator is wrong!")