from Person import Person

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
		result["person"] 				= self.__person()
		#TO DO
		result["observation"] 			= self.__observation()
		result["observation_period"] 	= self.__observation_period()
		result["visit_occurrence"] 		= self.__visit_occurrence()
		return result


	def __person(self):
		columns = self.columnsMapping("person")
		person = Person(cohort 	   = self.cohort.loc[:, columns],
						harmonizer = self.adHocHarmonization)

	def __observation(self):
		return None

	def __observation_period(self):
		return None

	def __visit_occurrence(self):
		return None