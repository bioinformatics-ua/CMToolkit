from BaseTable import BaseTable
import sqlalchemy as sa

class VisitOccurrence():#BaseTable):
    '''Class to build the VisitOccurrence table mapping.

    Constructor arguments: See BaseTable
    '''
    def __init__(self, cohort, harmonizerAdHoc, columnMapper):
        columns = [
            'visit_occurrence_id',
            'person_id',
            'visit_concept_id',
            'visit_start_date',
            'visit_start_datetime',
            'visit_end_date',
            'visit_end_datetime',
            'visit_type_concept_id',
            'provider_id',
            'care_site_id',
            'visit_source_value',
            'visit_source_concept_id',
            'admitting_source_concept_id',
            'admitting_source_value',
            'discharge_to_concept_id',
            'discharge_to_source_value',
            'preceding_visit_occurrence_id'
        ]
        size = self.__calculateTableSize(cohort       = cohort, 
                                         columnMapper = columnMapper, 
                                         id           = 'visit_occurrence_id')
        super(VisitOccurrence, self).__init__(cohort          = cohort, 
                                              harmonizerAdHoc = harmonizerAdHoc, 
                                              columnsDst      = columns, 
                                              table           = "visit_occurrence",
                                              columnMapper    = columnMapper,
                                              size            = size)
        print ("VisitirOccurence - ToDo")

    def __calculateTableSize(self, cohort, columnMapper, id):
        print ("VisitirOccurence - ToDo")
        return len(cohort) 

    def getDataTypesForSQL():
        return {
            'visit_occurrence_id':            sa.types.BigInteger,
            'person_id':                      sa.types.BigInteger,
            'visit_concept_id':               sa.types.BigInteger,
            'visit_start_date':               sa.types.Date,
            'visit_start_datetime':           sa.types.String,
            'visit_end_date':                 sa.types.Date,
            'visit_end_datetime':             sa.types.String,
            'visit_type_concept_id':          sa.types.BigInteger,
            'provider_id':                    sa.types.BigInteger,
            'care_site_id':                   sa.types.BigInteger,
            'visit_source_value':             sa.types.String,
            'visit_source_concept_id':        sa.types.BigInteger,
            'admitting_source_concept_id':    sa.types.BigInteger,
            'admitting_source_value':         sa.types.String,
            'discharge_to_concept_id':        sa.types.BigInteger,
            'discharge_to_source_value':      sa.types.String,
            'preceding_visit_occurrence_id':  sa.types.BigInteger
        }
   