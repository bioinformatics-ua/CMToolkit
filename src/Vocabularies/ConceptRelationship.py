from BaseTable import BaseTable
import sqlalchemy as sa

class ConceptRelationship(BaseTable):
    '''Class to build the ConceptRelationship table mapping.

    Constructor arguments:
    :param content: CSV content to add into database
    '''
    def __init__(self, content):
        columns = [
            'concept_id_1',
            'concept_id_2',
            'relationship_id',
            'valid_start_date',
            'valid_end_date',
            'invalid_reason'
        ]
        super(ConceptRelationship, self).__init__(cohort          = content, 
                                                  harmonizerAdHoc = None, 
                                                  columnsDst      = columns, 
                                                  table           = "concept_relationship",
                                                  columnMapper    = None,
                                                  size            = len(content),
                                                  contentMapping  = None)

    def getDataTypesForSQL():
        return {
            'concept_id_1':     sa.types.BigInteger,
            'concept_id_2':     sa.types.BigInteger,
            'relationship_id':  sa.types.String,
            'valid_start_date': sa.types.String,
            'valid_end_date':   sa.types.Date,
            'invalid_reason':   sa.types.String
        }
   