from BaseTable import BaseTable
import pandas as pd
import sqlalchemy as sa

class Person(BaseTable):
    '''Class to build the Person table mapping.

    Constructor arguments: See BaseTable
    '''
    pesondIdDict = {}

    def __init__(self, cohort, harmonizerAdHoc, columnMapper):
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
        super(Person, self).__init__(cohort                  = cohortFiltered,
                                     harmonizerAdHoc         = harmonizerAdHoc, 
                                     columnsDst              = columns, 
                                     table                   = "person",
                                     columnMapper            = columnMapper,
                                     size                    = len(cohortFiltered),
                                     commonHarmonizerMethods = Person.CommonHarmonizerMethods())

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

    class CommonHarmonizerMethods(object):
        '''Class with the most common harmonized methods.
        This class follow the same rules as all the hamonized classes in the method name definition.
        See more: TO DO docs
        '''
        def set_person_person_id(self, value):
            person_dict = value.to_dict()
            person_dict = {i[1]:i[0] for i in person_dict.items()}
            Person.pesondIdDict = person_dict
            return value.map(person_dict)

        def set_person_year_of_birth(self, value):
            return pd.DatetimeIndex(value).year

        def set_person_month_of_birth(self, value):
            return pd.DatetimeIndex(value).month

        def set_person_day_of_birth(self, value):
            return pd.DatetimeIndex(value).day