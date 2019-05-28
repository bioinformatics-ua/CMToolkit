import Baseline

class Harmonizer(object):
	def filter_person(self, cohort):
		return cohort.loc[cohort["GenderFM"]!='69'].reset_index(drop=True)

	#def set_person_gender_concept_id(self, value):
	#	gender_map = {"M":8507, "F":8532}
	#	return value.map(gender_map)

	def set_person_person_id(self, value):
		person_dict = value.to_dict()
		person_dict = {i[1]:i[0] for i in person_dict.items()}
		return value.map(person_dict)

Baseline.main(Harmonizer)
#Baseline.main()