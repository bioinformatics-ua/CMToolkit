from Person import Person
from Observation import Observation
from ObservationPeriod import ObservationPeriod
from VisitOccurrence import VisitOccurrence

class Migrator():
	def __init__(self, cohort, columnsMapping, contentMapping):
		self.adHocHarmonization = None
		self.cohort 			= cohort
		self.columnsMapping 	= columnsMapping
		self.contentMapping 	= contentMapping

	def setAdHocMethods(self, adHocMethod):
		self.adHocHarmonization = adHocMethod()

	def migrate(self):
		result = {}
		result["person"] 				= self.__migrateTable("person")
		result["observation"] 			= self.__migrateTable("observation")
		result["observation_period"] 	= self.__migrateTable("observation_period")
		result["visit_occurrence"] 		= self.__migrateTable("visit_occurrence")
		return result

	def __migrateTable(self, table):
		columns, dictOfMappingColumns = self.columnsMapping(table)
		migration = None
		if(table == "person"):
			migration = Person(cohort 	   		= self.cohort.loc[:, columns],
						       harmonizerAdHoc  = self.adHocHarmonization,
						       columnMapper 	= dictOfMappingColumns,
						       contentMapping	= self.contentMapping)
		elif(table == "observation"):
			migration = Observation(cohort 	     	= self.cohort.loc[:, columns],
						       		harmonizerAdHoc	= self.adHocHarmonization,
						       		columnMapper 	= dictOfMappingColumns,
						       	 	contentMapping	= self.contentMapping)
		elif(table == "observation_period"):
			migration = ObservationPeriod(cohort 	      = self.cohort.loc[:, columns],
						       			  harmonizerAdHoc = self.adHocHarmonization,
						       			  columnMapper    = dictOfMappingColumns,
						       			  contentMapping  = self.contentMapping)
		elif(table == "visit_occurrence"):
			migration = VisitOccurrence(cohort 	     	= self.cohort.loc[:, columns],
						       			harmonizerAdHoc	= self.adHocHarmonization,
						       			columnMapper 	= dictOfMappingColumns,
						       			contentMapping	= self.contentMapping)
		else:
			return None
		return migration.getMapping()
