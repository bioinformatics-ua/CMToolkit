from BaseTable import BaseTable
import sqlalchemy as sa

class ConceptClass(BaseTable):
    '''Class to build the ConceptClass table mapping.

    Constructor arguments:
    :param content: CSV content to add into database
    '''
    def __init__(self, content):
        columns = [
            'concept_class_id',
            'concept_class_name',
            'concept_class_concept_id'
        ]
        super(ConceptClass, self).__init__(cohort         = content, 
                                          harmonizerAdHoc = None, 
                                          columnsDst      = columns, 
                                          table           = "concept_class",
                                          columnMapper    = None,
                                          size            = len(content),
                                          contentMapping  = None)

    def getDataTypesForSQL():
        return {
            'concept_class_id':         sa.types.String,
            'concept_class_name':       sa.types.String,
            'concept_class_concept_id': sa.types.BigInteger
        }
   