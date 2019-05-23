class Person(object):
    '''Class for build the Person table mapping.

    Constructor arguments:
    :param cohort: the cohort sctruturd readed from CSV file
    :param harmonizer: object with ad hoc methods to harmonize that types of fields
    '''
    def __init__(self, cohort, harmonizer):
        self.person_columns = [
        'person_id',
        'gender_concept_id',
        'year_of_birth',
        'month_of_birth',
        'day_of_birth',
		'birth_datetime',
        'death_datetime',
        'race_concept_id',
        'ethnicity_concept_id',
        'location_id',
		'provider_id',
        'care_site_id',
        'person_source_value',
        'gender_source_value',
        'gender_source_concept_id',
		'race_source_value',
        'race_source_concept_id',
        'ethnicity_source_value',
        'ethnicity_source_concept_id'
        ]
        self.cohort = cohort
        self.harmonizer = harmonizer
        self.person = {}

        self.__populate()

    def __populate(self):
        for element in self.person_columns:
            methodName = "set_person_" + element
            if(hasattr(self.harmonizer, methodName)): #maybe check if is None
                self.person[element] = getattr(self.harmonizer, methodName)()
            else:
                self.person[element] = self.cohort[element] if element in self.cohort != None else None

    def getMapping(self):
        return self.person

    def getDataTypesForSQL(self):
        return {
            'person_id':                    sa.types.BigInteger,
            'gender_concept_id':            sa.types.BigInteger,
            'year_of_birth':                sa.types.Integer,
            'month_of_birth':               sa.types.Integer,
            'day_of_birth':                 sa.types.Integer,
            'birth_datetime':               sa.types.String,
            'death_datetime':               sa.types.String,
            'race_concept_id':              sa.types.BigInteger,
            'ethnicity_concept_id':         sa.types.BigInteger,
            'location_id':                  sa.types.BigInteger,
            'provider_id':                  sa.types.BigInteger,
            'care_site_id':                 sa.types.BigInteger,
            'person_source_value':          sa.types.String,
            'gender_source_value':          sa.types.String,
            'gender_source_concept_id':     sa.types.BigInteger,
            'race_source_value':            sa.types.String,
            'race_source_concept_id':       sa.types.BigInteger,
            'ethnicity_source_value':       sa.types.String,
            'ethnicity_source_concept_id':  sa.types.BigInteger 
        }
   