from BaseTable import BaseTable
import sqlalchemy as sa

class ConceptSynonym(BaseTable):
    '''Class to build the ConceptSynonym table mapping.

    Constructor arguments:
    :param content: CSV content to add into database
    '''
    def __init__(self, content):
        columns = [
            'concept_id',
            'concept_synonym_name',
            'language_concept_id'
        ]
        super(ConceptSynonym, self).__init__(cohort          = content, 
                                             harmonizerAdHoc = None, 
                                             columnsDst      = columns, 
                                             table           = "concept_synonym",
                                             columnMapper    = None,
                                             size            = len(content),
                                             contentMapping  = None)

    def getDataTypesForSQL():
        return {
            'concept_id':           sa.types.BigInteger,
            'concept_synonym_name': sa.types.String,
            'language_concept_id':  sa.types.BigInteger
        }
   