
class TranSMARTConstants():
	#Demographic mappings
	DemographicSex 			= 2000000609
	DemographicRace 		= 2000000603
	DemographicEthnic 		= 2000000555
	DemographicBirthYear 	= 2000000503
	#DemographicCounty 		= 2000000065
	#DemographicAge 		= 2000000488

	#Observation query index
	ObservationPersonIdIndex       		= 10#1
	ObservationObsvationConceptIdIndex	= 2
	ObservationValuesAsNumberIndex		= 6
	ObservationValuesAsStringIndex		= 7
	ObservationValuesAsConceptIdIndex	= 8
	ObservationValuesAsConceptNameIndex	= 9

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
		