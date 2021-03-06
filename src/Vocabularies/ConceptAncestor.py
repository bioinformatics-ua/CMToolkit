from BaseTable import BaseTable
import sqlalchemy as sa

class ConceptAncestor(BaseTable):
    '''Class to build the ConceptAncestor table mapping.

    Constructor arguments:
    :param content: CSV content to add into database
    '''
    def __init__(self, content):
        columns = [
            'ancestor_concept_id',
            'descendant_concept_id',
            'min_levels_of_separation',
            'max_levels_of_separation'
        ]
        super(ConceptAncestor, self).__init__(cohort          = content, 
                                              harmonizerAdHoc = None, 
                                              columnsDst      = columns, 
                                              table           = "concept_ancestor",
                                              columnMapper    = None,
                                              size            = len(content),
                                              contentMapping  = None)

    def getDataTypesForSQL():
        return {
            'ancestor_concept_id':      sa.types.BigInteger,
            'descendant_concept_id':    sa.types.BigInteger,
            'min_levels_of_separation': sa.types.BigInteger,
            'max_levels_of_separation': sa.types.BigInteger
        }
   