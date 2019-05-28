from BaseTable import BaseTable

class ObservationPeriod(BaseTable):
    '''Class to build the Observation Period table mapping.

    Constructor arguments: See BaseTable
    '''
    def __init__(self, cohort, harmonizerAdHoc, columnMapper, contentMapping):
        columns = [
            'observation_period_id',         
            'person_id',                     
            'observation_period_start_date', 
            'observation_period_end_date',   
            'period_type_concept_id'       
        ]
        size = self.__calculateTableSize(cohort       = cohort, 
                                         columnMapper = columnMapper, 
                                         id           = 'observation_period_id')
        super(ObservationPeriod, self).__init__(cohort          = cohort, 
                                                harmonizerAdHoc = harmonizerAdHoc, 
                                                columnsDst      = columns, 
                                                table           = "observation_period",
                                                columnMapper    = columnMapper,
                                                size            = size,
                                                contentMapping  = contentMapping)
        print ("ObservationPeriod - ToDo")

    def __calculateTableSize(self, cohort, columnMapper, id):
        print ("ObservationPeriod - ToDo")
        return len(cohort) 

    def getDataTypesForSQL():
        return {
            'observation_period_id':          sa.types.BigInteger,
            'person_id':                      sa.types.BigInteger,
            'observation_period_start_date':  sa.types.Date,
            'observation_period_end_date':    sa.types.Date,
            'period_type_concept_id':         sa.types.BigInteger,
        }
   