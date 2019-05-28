from BaseTable import BaseTable

class Person(BaseTable):
    '''Class to build the Person table mapping.

    Constructor arguments: See BaseTable
    '''
    def __init__(self, cohort, harmonizer, columnMapper):
        columns = [
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
        size = self.__calculateTableSize(cohort       = cohort, 
                                         columnMapper = columnMapper, 
                                         id           = 'person_id')
        super(Person, self).__init__(cohort         = cohort.drop_duplicates().reset_index(drop=True), 
                                     harmonizer     = harmonizer, 
                                     columnsDst     = columns, 
                                     table          = "person",
                                     columnMapper   = columnMapper,
                                     size           = size)

    def __calculateTableSize(self, cohort, columnMapper, id):
        try:
            if(len(cohort.drop_duplicates()) != len(cohort[columnMapper[id]].unique())):
                raise Exception("Inconsistency in the Person ids!")

            return len(cohort[columnMapper[id]].unique())
        except:
            raise Exception("Person id not found!")

    def getDataTypesForSQL():
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
   