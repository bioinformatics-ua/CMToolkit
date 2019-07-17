from BaseTable import BaseTable
import sqlalchemy as sa

class Domain(BaseTable):
    '''Class to build the Domain table mapping.

    Constructor arguments:
    :param content: CSV content to add into database
    '''
    def __init__(self, content):
        columns = [
            'domain_id',
            'domain_name',
            'domain_concept_id'
        ]
        super(Domain, self).__init__(cohort          = content, 
                                     harmonizerAdHoc = None, 
                                     columnsDst      = columns, 
                                     table           = "domain",
                                     columnMapper    = None,
                                     size            = len(content),
                                     contentMapping  = None)

    def getDataTypesForSQL():
        return {
            'domain_id':          sa.types.String,
            'domain_name':        sa.types.String,
            'domain_concept_id':  sa.types.BigInteger
        }
   