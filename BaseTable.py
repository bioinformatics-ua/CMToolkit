class BaseTable(object):
    '''Class base to build the table mapping.

    Constructor arguments:
    :param cohort: the cohort sctruturd readed from CSV file
    :param harmonizer: object with ad hoc methods to harmonize that types of fields
    :param columns: list of columns from the destination table
    :param table: destination table name to identify the ad hoc methods following our syntax
    			  - Sintax: set_<table name>_<field name>
    '''
    def __init__(self, cohort, harmonizer, columns, table):
        self.columns 	= columns
        self.cohort 	= cohort
        self.harmonizer = harmonizer
        self.table 		= table
        self.mapping 	= {}

        self.__populate()

    def __populate(self):
        for element in self.columns:
            methodName = "set_" + self.table + "_" + element
            if(hasattr(self.harmonizer, methodName)): #maybe check if harmonizer is None
                self.mapping[element] = getattr(self.harmonizer, methodName)()
            else:
                self.mapping[element] = self.cohort[element] if element in self.cohort != None else None

    def getMapping(self):
        return self.mapping

    def getDataTypesForSQL():
        return {}
   