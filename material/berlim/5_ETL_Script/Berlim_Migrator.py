import sys
sys.path.insert(0, '../../../')

import Baseline
from Observation import Observation
import pandas as pd

class Harmonizer(object):
	#def filter_person(self, cohort):
		#return cohort.loc[cohort["GenderFM"]!='69'].reset_index(drop=True)

	#Person
	def set_person_gender_concept_id(self, value):
		gender_map = {1:8507, 0:8532}
		return value.map(gender_map)

	#Observation
	def set_observation_observation_type_concept_id(self, value):
		return pd.Series(2000000260, index=Observation.ObservationIDSet)

Baseline.main(Harmonizer)