from BaseTable import BaseTable
import sqlalchemy as sa

class Concept(BaseTable):
    '''Class to build the Concept table mapping.

    Constructor arguments:
    :param content: CSV content to add into database
    '''
    def __init__(self, content):
        columns = [
            'concept_id integer',
            'concept_name',
            'domain_id',
            'vocabulary_id', 
            'concept_class_id',
            'standard_concept', 
            'concept_code', 
            'valid_start_date',
            'valid_end_date',
            'invalid_reason'
        ]
        super(Concept, self).__init__(cohort          = content, 
                                      harmonizerAdHoc = None, 
                                      columnsDst      = columns, 
                                      table           = "Concept",
                                      columnMapper    = None,
                                      size            = len(content),
                                      contentMapping  = None)

    def getDataTypesForSQL():
        return {
            'concept_id integer':   sa.types.BigInteger,
            'concept_name':         sa.types.String,
            'domain_id':            sa.types.String,
            'vocabulary_id':        sa.types.String,
            'concept_class_id':     sa.types.String,
            'standard_concept':     sa.types.String,
            'concept_code':         sa.types.String,
            'valid_start_date':     sa.types.Date,
            'valid_end_date':       sa.types.Date,
            'invalid_reason':       sa.types.String
        }
   