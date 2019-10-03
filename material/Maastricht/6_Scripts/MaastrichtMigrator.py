import sys
#GREAT SHIT
sys.path.insert(0, '../../../src/Migrator')
sys.path.insert(0, '../../../src/Tables')
sys.path.insert(0, '../../../src/Utils')
sys.path.insert(0, '../../../src/Vocabularies')

import Baseline
from Observation import Observation
import pandas as pd
from datetime import date
import datetime

class Harmonizer(object):
	def __init__(self):
		#Variables calculated based on other variables
		self.ceradWLRounds = []
		self.ceradWLRecognition = []
		self.apoE = []
		self.diagnosis = {}
		self.etiology = {}
		self.adHocCutOff = {}
		'''
		cutOffs = "cutOffId":{"value":xxxx, "operator": "<" or >"}
		or
		cutOffs = "cutOffId":{"conditionalMethod": method()}
		'''
		self.cutOff = {
			}


	###################################################
	#	Public methods in the harmonization stage	  #
	###################################################
	def harmonizer(self, row):
		variableConcept = str(row["VariableConcept"])
		if "2000000024" in variableConcept:
			print(row)
			#return self.__readCeradWLRounds(row)
		#ACM Transactions on Computer Systems
		#if "2000000049" in variableConcept:
		#	return self.__readCeradWLRounds(row)
		
		return row	

	def addMissingRows(self):
		missingRows = []
		#missingRows += self.__process...
		#....
		return missingRows

	###############
	#	Private	  #
	###############

		
	#######################################
	#	Harmonizer during the migration	  #
	#######################################
	def filter_person(self, cohort):
		cohort = cohort[pd.notnull(cohort['Sex'])]
		return cohort.reset_index(drop=True)

	#Person
	def set_person_gender_concept_id(self, value):
		gender_map = {"M":8507, "V":8532}
		return value.map(gender_map)

	#def set_person_year_of_birth(self, value):
	#	print(value)
	#	raise
	#	return value

def prepareUsagiFiles(args):
	print(args)


prepareUsagiFiles(Baseline.loadArgs())
Baseline.main(Harmonizer)
