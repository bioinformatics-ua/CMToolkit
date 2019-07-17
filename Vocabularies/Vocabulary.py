from BaseTable import BaseTable
import sqlalchemy as sa

class Vocabulary(BaseTable):
    '''Class to build the Vocabulary table mapping.

    Constructor arguments:
    :param content: CSV content to add into database
    '''
    def __init__(self, content):
        columns = [
            'vocabulary_id',
            'vocabulary_name',
            'vocabulary_reference',
            'vocabulary_version',
            'vocabulary_concept_id'
        ]
        super(Vocabulary, self).__init__(cohort          = content, 
                                         harmonizerAdHoc = None, 
                                         columnsDst      = columns, 
                                         table           = "vocabulary",
                                         columnMapper    = None,
                                         size            = len(content),
                                         contentMapping  = None)

    def getDataTypesForSQL():
        return {
            'vocabulary_id':            sa.types.String,
            'vocabulary_name':          sa.types.String,
            'vocabulary_reference':     sa.types.String,
            'vocabulary_version':       sa.types.String,
            'vocabulary_concept_id':    sa.types.BigInteger
        }
   