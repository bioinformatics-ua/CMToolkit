import glob
import pandas as pd
import numpy as np
import datetime
import math
from dateutil import relativedelta
from Person import Person
from Observation import Observation
from ObservationPeriod import ObservationPeriod
from VisitOccurrence import VisitOccurrence
from Harmonizer import Harmonizer
from FileManager import FileManager

from MigratorArgs import MigratorArgs

class Migrator():    
	'''Class base to orchestrate the migration.

    Constructor arguments: #todo
    :param cohort:         the cohort sctruturd readed from CSV file
    :param columnsMapping: the method that returns the mapping from the defined table
    :param contentMapping: the structure with all concepts mapped having the 
    							- sourceCode: the cohort column 
    							- sourceName: one of the entries in the cohort for the column defined
    							- targetConceptId: the target concept mapped
    '''
	def __init__(self, cohortDir, person, observations):
		self.adHocHarmonization = None
		self.cohortDir 			= cohortDir
		self.person 			= person
		self.observations 		= observations
		self.fileManager    	= FileManager()
		self.result 			= {}
		self.args 				= MigratorArgs()

	def setAdHocClass(self, adHocClass):
		self.adHocHarmonization = adHocClass()

	def migrate(self, table=None):
		if(table == "person"):
			cohortData = self.fileManager.readCohort(self.person)
			conceptToSearch = self.person.split(Harmonizer.MARK)[1] 
			columns, dictOfMappingColumns = self.fileManager.getColumnsMappingBySourceCodeAndDomain(conceptToSearch, table)
			cohortData = cohortData.reindex(columns=columns)
			migration = Person(cohort 	   		= cohortData,
						       harmonizerAdHoc  = self.adHocHarmonization,
						       columnMapper 	= dictOfMappingColumns)

		elif(table == "observation"):
			result = glob.glob('{}*.{}'.format(self.observations, "csv"))
			observationResult = []
			for obs in result:
				#Load initial data
				cohortData = self.fileManager.readCohort(obs)
				conceptToSearch = obs.split(Harmonizer.MARK)[1] 
				patientIDLabel = self.args.settings["patient_ids"][conceptToSearch.replace(" ", "_")]
				patientIDLabel = patientIDLabel.lstrip('\"').rstrip('\"')

				#Columns
				columns, dictOfMappingColumns = self.fileManager.getColumnsMappingBySourceCodeAndDomain(conceptToSearch, table)
				columns	+= ["Variable", "Measure", "VariableConcept", "MeasureConcept", "MeasureString", "MeasureNumber", "VisitConcept"]
				
				#Mapp columns
				dictOfMappingColumns["observation_source_value"] =  "Variable"
				dictOfMappingColumns["qualifier_source_value"] =  "Measure"
				dictOfMappingColumns["observation_concept_id"] = "VariableConcept" 
				dictOfMappingColumns["value_as_concept_id"] = "MeasureConcept"
				dictOfMappingColumns["value_as_string"] = "MeasureString" 
				dictOfMappingColumns["value_as_number"] = "MeasureNumber" 
				dictOfMappingColumns["observation_type_concept_id"] = "VisitConcept"

				#Process last things
				cohortData = self.__calculateVisitConcepts(cohortData, dictOfMappingColumns)
				cohortData = cohortData.reindex(columns=columns)
				
				#Migrate
				migration = Observation(cohort 	     	= cohortData,
						       			harmonizerAdHoc	= self.adHocHarmonization,
						       			columnMapper 	= dictOfMappingColumns, 
						       			patientIDLabel	= patientIDLabel)
				observationResult += [migration.getMapping()]
			self.result[table] = pd.concat(observationResult)
			return None
		else:
			return None
		self.result[table] = migration.getMapping()

	def __calculateVisitConcepts(self, cohortData, mappings):
		cohortData["VisitConcept"] = pd.Series("2100000000")
		patientIDLabel = mappings["person_id"].strip()
		observationDateLabel = mappings["observation_date"].strip()
		dataDict = cohortData.to_dict(orient='records')
		patientVisits = {}
		outputDataDict = []
		#Get the older observation date for the patient
		for row in dataDict:
			patientID = row[patientIDLabel]
			date = row[observationDateLabel]
			if isinstance(date, float):
				if math.isnan(date):
					continue
			if patientID in patientVisits:
				d0 = datetime.datetime.strptime(patientVisits[patientID], '%d-%M-%Y')
				d1 = datetime.datetime.strptime(date, '%d-%M-%Y')
				r = relativedelta.relativedelta(d1, d0)
				if (((r.years*12) + r.months)) < 0:
					patientVisits[patientID] = date
			else:
				patientVisits[patientID] = date
		#Calculate the months interval
		for row in dataDict:
			patientID = row[patientIDLabel]
			date = row[observationDateLabel]
			if isinstance(date, float):
				if math.isnan(date):
					row["VisitConcept"] = "2100000000" #Baseline
					outputDataDict += [row]
					continue
			d0 = datetime.datetime.strptime(patientVisits[patientID], '%d-%M-%Y')
			d1 = datetime.datetime.strptime(date, '%d-%M-%Y')
			r = relativedelta.relativedelta(d1, d0)
			months = round((((r.years*12) + r.months))/6)

			if months >= 0 and months <= 40:
				row["VisitConcept"] = "21000000" + str(months).zfill(2)
			else:
				self.logger.warn(warnType	= OUT_OF_RANGE, 
								 patientID 	= patientID, 
								 variable 	= "Visit Concept", 
								 measure 	= months*6,
								 msg 		= "Difference of follow up months superior to 90 (rounded)")
				continue
			outputDataDict += [row]
		return pd.DataFrame(outputDataDict, columns = cohortData.columns.values)


	def getMigrationResults(self):
		return self.result