import glob
import pandas as pd
from Person import Person
from Observation import Observation
from ObservationPeriod import ObservationPeriod
from VisitOccurrence import VisitOccurrence
from Harmonizer import Harmonizer

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
	def __init__(self, cohortDir, person, observations, fileManager):
		self.adHocHarmonization = None
		self.cohortDir 			= cohortDir
		self.person 			= person
		self.observations 		= observations
		self.fileManager		= fileManager
		self.result 			= {}

	def setAdHocMethods(self, adHocMethod):
		self.adHocHarmonization = adHocMethod()

	def migrate(self, table=None):
		if(table == "person"):
			cohortData = self.fileManager.readCohort(self.person)
			conceptToSearch = self.person.split(Harmonizer.MARK)[1] 
			columns, dictOfMappingColumns = self.fileManager.getColumnsMappingBySourceCodeAndDomain(conceptToSearch, table)
			cohortData = cohortData.reindex(columns=columns)
			migration = Person(cohort 	   		= cohortData,
						       harmonizerAdHoc  = self.adHocHarmonization,
						       columnMapper 	= dictOfMappingColumns,
						       contentMapping	= None)#self.contentMapping)

		elif(table == "observation"):
			result = glob.glob('{}*.{}'.format(self.observations, "csv"))
			observationResult = []
			for obs in result:
				cohortData = self.fileManager.readCohort(obs)
				conceptToSearch = obs.split(Harmonizer.MARK)[1] 
				columns, dictOfMappingColumns = self.fileManager.getColumnsMappingBySourceCodeAndDomain(conceptToSearch, table)
				columns += ["Variable", "Measure", "VariableConcept", "MeasureConcept"]
				dictOfMappingColumns["observation_source_value"] =  "Variable"
				dictOfMappingColumns["qualifier_source_value"] =  "Measure"
				dictOfMappingColumns["observation_concept_id"] = "VariableConcept" 
				dictOfMappingColumns["value_as_concept_id"] = "MeasureConcept"
				#dictOfMappingColumns["value_as_string"] = "Measure" #Temporary, change this to verifiy the typr

				cohortData = cohortData.reindex(columns=columns)
				migration = Observation(cohort 	     	= cohortData,
						       			harmonizerAdHoc	= self.adHocHarmonization,
						       			columnMapper 	= dictOfMappingColumns,
						       	 		contentMapping	= None)
				observationResult += [migration.getMapping()]
			self.result[table] = pd.concat(observationResult)
			return None
		else:
			return None
		self.result[table] = migration.getMapping()

	def getMigrationResults(self):
		return self.result