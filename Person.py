from BaseTable import BaseTable

class Person(BaseTable):
    '''Class to build the Person table mapping.

    Constructor arguments: See BaseTable
    '''
    def __init__(self, cohort, harmonizerAdHoc, columnMapper, contentMapping):
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
        cohortFiltered = self.__filterCohort(cohort, harmonizerAdHoc, "person")
        super(Person, self).__init__(cohort          = cohortFiltered,
                                     harmonizerAdHoc = harmonizerAdHoc, 
                                     columnsDst      = columns, 
                                     table           = "person",
                                     columnMapper    = columnMapper,
                                     size            = len(cohortFiltered),
                                     contentMapping  = contentMapping)

    def __filterCohort(self, cohort, harmonizerAdHoc, table):
        return BaseTable.cohortFilter(cohort          = cohort.drop_duplicates().reset_index(drop=True), 
                                      table           = table,
                                      harmonizerAdHoc = harmonizerAdHoc)

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
   