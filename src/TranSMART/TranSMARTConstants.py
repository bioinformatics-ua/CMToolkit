
class TranSMARTConstants():
	#Demographic mappings
	DemographicSex 			= "2000000609"
	DemographicRace 		= "2000000603"
	DemographicEthnic 		= "2000000555"
	DemographicBirthYear 	= "2000000503"
	#DemographicCounty 		= 2000000065
	#DemographicAge 		= 2000000488

	#Observation query index
	ObservationPersonIdIndex       			= 10#1
	ObservationObservationConceptIdIndex	= 2
	ObservationObservationTypeConIdIndex	= 5
	ObservationValuesAsNumberIndex			= 6
	ObservationValuesAsStringIndex			= 7
	ObservationValuesAsConceptIdIndex		= 8
	ObservationValuesAsConceptNameIndex		= 9

	def observationQuery(schema):
		return "SELECT observation_id, observation.person_id, observation_concept_id, concept.concept_name, observation_date, \
       				observation_type_concept_id, value_as_number, value_as_string, value_as_concept_id, \
       				valueConcept.concept_name,  person.person_source_value \
	  			FROM "+schema+".observation \
	  			INNER JOIN "+schema+".concept as concept on "+schema+".observation.observation_concept_id=concept.concept_id \
				INNER JOIN "+schema+".person as person on "+schema+".observation.person_id=person.person_id \
	  			LEFT JOIN "+schema+".concept as valueConcept  on "+schema+".observation.value_as_concept_id=valueConcept.concept_id;"

	#Person query index
	PersonPersonIdIndex       		= 12#0
	PersonGenderNameIndex       	= 2
	PersonRaceNameIndex       		= 4
	PersonEthnicNameIndex       	= 6
	PersonBirthYearIndex       		= 7

	def personQuery(schema):
		return "SELECT person_id, gender_concept_id, genderConcept.concept_name as gender_concept_name,\
	       			race_concept_id, raceConcept.concept_name as race_concept_name,\
				    ethnicity_concept_id, ethnicityConcept.concept_name as race_concept_name,\
				    year_of_birth, month_of_birth, day_of_birth, birth_datetime, death_datetime, person_source_value\
				FROM "+schema+".person\
				LEFT JOIN "+schema+".concept as genderConcept on "+schema+".person.gender_concept_id = genderConcept.concept_id\
				LEFT JOIN "+schema+".concept as raceConcept on "+schema+".person.race_concept_id = genderConcept.concept_id\
				LEFT JOIN "+schema+".concept as ethnicityConcept on "+schema+".person.ethnicity_concept_id = ethnicityConcept.concept_id;"
	

	Months = {
		"2100000000":"Baseline",
		"2100000001":"Month_6",
		"2100000002":"Month_12",
		"2100000003":"Month_18",
		"2100000004":"Month_24",
		"2100000005":"Month_30",
		"2100000006":"Month_36",
		"2100000007":"Month_42",
		"2100000008":"Month_48",
		"2100000009":"Month_54",
		"2100000010":"Month_60",
		"2100000011":"Month_66",
		"2100000012":"Month_72",
		"2100000013":"Month_78",
		"2100000014":"Month_84",
		"2100000015":"Month_90",
		"2100000016":"Month_96",
		"2100000017":"Month_102",
		"2100000018":"Month_108",
		"2100000019":"Month_114",
		"2100000020":"Month_120",
		"2100000021":"Month_126",
		"2100000022":"Month_132",
		"2100000023":"Month_138",
		"2100000024":"Month_144",
		"2100000025":"Month_150",
		"2100000026":"Month_156",
		"2100000027":"Month_162",
		"2100000028":"Month_168",
		"2100000029":"Month_174",
		"2100000030":"Month_180",
		"2100000031":"Month_186",
		"2100000032":"Month_192",
		"2100000033":"Month_198",
		"2100000034":"Month_204",
		"2100000035":"Month_210",
		"2100000036":"Month_216",
		"2100000037":"Month_222",
		"2100000038":"Month_228",
		"2100000039":"Month_234",
		"2100000040":"Month_240"
	}	