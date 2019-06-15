import sys
sys.path.insert(0, '../../../')

import Baseline
import pandas as pd

class Harmonizer(object):
	#def filter_person(self, cohort):
		#return cohort.loc[cohort["GenderFM"]!='69'].reset_index(drop=True)

	def set_person_year_of_birth(self, value):
		return pd.DatetimeIndex(value).year

	def set_person_month_of_birth(self, value):
		return pd.DatetimeIndex(value).month

	def set_person_day_of_birth(self, value):
		return pd.DatetimeIndex(value).day

	def set_person_person_id(self, value):
		person_dict = value.to_dict()
		person_dict = {i[1]:i[0] for i in person_dict.items()}
		return value.map(person_dict)

#Baseline.main(Harmonizer)
Baseline.main()