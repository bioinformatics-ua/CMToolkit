from Person import Person
from Observation import Observation
from ObservationPeriod import ObservationPeriod
from VisitOccurrence import VisitOccurrence

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
	def __init__(self, cohortDir, person, observations, columnMapping, fileManager):
		self.adHocHarmonization = None
		self.cohortDir 			= cohortDir
		self.person 			= person
		self.observations 		= observations
		self.columnMapping 		= columnMapping
		self.fileManager		= fileManager
		self.result 			= {}

	def setAdHocMethods(self, adHocMethod):
		self.adHocHarmonization = adHocMethod()

	def migrate(self, table=None):
		if(table == "person"):
			cohortData = self.fileManager.readCohort(self.person)
			columns, dictOfMappingColumns = self.fileManager.getColumnsMappingBySourceCode(self.person)
			cohortData = cohortData.loc[:, columns]
			migration = Person(cohort 	   		= cohortData,
						       harmonizerAdHoc  = self.adHocHarmonization,
						       columnMapper 	= dictOfMappingColumns,
						       contentMapping	= None)#self.contentMapping)
		else:
			return None
		self.result[table] = migration.getMapping()

	def getMigrationResults(self):
		return self.result