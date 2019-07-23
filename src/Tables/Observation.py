from BaseTable import BaseTable
from Person import Person
import sqlalchemy as sa
import pandas as pd

class Observation(BaseTable):
    '''Class to build the Observation table mapping.
    '''
    ObservationID = 0
    ObservationIDSet = []
    '''
    Constructor arguments: See BaseTable
    '''
    def __init__(self, cohort, harmonizerAdHoc, columnMapper):
        columns = [
            'observation_id',
            'person_id',
            'observation_concept_id',
            'observation_date',
            'observation_datetime',
            'observation_type_concept_id',
            'value_as_number',
            'value_as_string',
            'value_as_concept_id',
            'unit_concept_id',
            'provider_id',
            'visit_occurrence_id',
            'visit_detail_id',
            'observation_source_value',
            'observation_source_concept_id',
            'unit_source_value',
            'qualifier_source_value'
        ]
        cohortFiltered = self.__filterCohort(cohort          = cohort, 
                                             table           = "observation",
                                             harmonizerAdHoc = harmonizerAdHoc)
        self.__updateObservationIDs(cohortFiltered)
        super(Observation, self).__init__(cohort                  = cohortFiltered, 
                                          harmonizerAdHoc         = harmonizerAdHoc, 
                                          columnsDst              = columns, 
                                          table                   = "observation",
                                          columnMapper            = columnMapper,
                                          size                    = len(cohortFiltered),
                                          commonHarmonizerMethods = Observation.CommonHarmonizerMethods())

    def __filterCohort(self, cohort, harmonizerAdHoc, table):
        cohortFiltered = BaseTable.cohortFilter(cohort          = cohort, 
                                                table           = table,
                                                harmonizerAdHoc = harmonizerAdHoc)
        return cohortFiltered[pd.notnull(cohortFiltered["Patient ID"].map(Person.pesondIdDict))].reset_index(drop=True)

    def __updateObservationIDs(self, cohortFiltered):
        Observation.ObservationIDSet = range(Observation.ObservationID, Observation.ObservationID + len(cohortFiltered))
        Observation.ObservationID += len(cohortFiltered)

    def getDataTypesForSQL():
        return {
            'observation_id':                   sa.types.BigInteger,
            'person_id':                        sa.types.BigInteger,
            'observation_concept_id':           sa.types.BigInteger,
            'observation_date':                 sa.types.Date,
            'observation_datetime':             sa.types.String,
            'observation_type_concept_id':      sa.types.BigInteger,
            'value_as_number':                  sa.types.Float,
            'value_as_string':                  sa.types.String,
            'value_as_concept_id':              sa.types.BigInteger,
            'unit_concept_id':                  sa.types.BigInteger,
            'provider_id':                      sa.types.BigInteger,
            'visit_occurrence_id':              sa.types.BigInteger,
            'visit_detail_id':                  sa.types.BigInteger,
            'observation_source_value':         sa.types.String,
            'observation_source_concept_id':    sa.types.BigInteger,
            'unit_source_value':                sa.types.String,
            'qualifier_source_value':           sa.types.String
        }

    class CommonHarmonizerMethods(object):
        '''Class with the most common harmonized methods.
        This class follow the same rules as all the hamonized classes in the method name definition.
        See more: TO DO docs
        '''
        def set_observation_observation_id(self, value):
            return Observation.ObservationIDSet

        def set_observation_person_id(self, value):
            return value.map(Person.pesondIdDict)
