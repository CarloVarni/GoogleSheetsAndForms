
from GoogleSheetsAndForms.Messages import NOTE, FAIL

class DataAdder:
    def __init__(self, NAME):
        self.__NAME = NAME
        
        self.__OutputCollectionName = []
        self.__Data = []
        
    @property
    def NAME(self):
        return self.__NAME

    @property
    def OutputCollectionName(self):
        return self.__OutputCollectionName
    
    @OutputCollectionName.setter
    def OutputCollectionName(self, value):
        if not isinstance(value, list):
            raise Exception(FAIL("Property Error: 'OutputCollectionName' property of class 'DataAdder' must be an array of strings!"))
        if len(value) == 0:
            raise Exception(FAIL("Property Error: 'OutputCollectionName' property of class 'DataAdder' must have at least one entry!"))
        for el in value:
            if not isinstance(el, str):
                raise Exception(FAIL("Property Error: 'OutputCollectionName' property of class 'DataAdder' must be an array of strings!"))
            if len(el) == 0:
                raise Exception(FAIL("Property Error: 'OutputCollectionName' property of class 'DataAdder' must not contain blank values!"))
        self.__OutputCollectionName = value

    @property
    def Data(self):
        return self.__Data

    @Data.setter
    def Data(self, value):
        if not isinstance(value, list):
            raise Exception(FAIL("Property Error: 'Data' property of class 'DataAdder' must be an array!"))
        if len(value) == 0:
            raise Exception(FAIL("Property Error: 'Data' property of class 'DataAdder' must have at least one entry!"))
        for el in value:
            if el is None:
                raise Exception(FAIL("Property Error: 'Data' property of class 'DataAdder' must not container NONE elements!"))
        self.__Data = value
            
    def __str__(self):
        output = "DataAdder: '{0}'\n".format(self.NAME)
        output += "   \\__ Output Collection Name: {}\n".format(self.OutputCollectionName)
        return output

    def execute(self, CTX):
        if len(self.OutputCollectionName) == 0:
            raise Exception(FAIL("No Data has been specified to be added to the Context!"))
        if len(self.OutputCollectionName) != len(self.Data):
            raise Exception(FAIL("Collection Name of Data to be added to Context MUST match!"))
        
        print(NOTE("Adding Data to Context ..."))
        for i in range(0, len(self.OutputCollectionName)):
            print("   \\__ Collection: '{0}'".format(self.OutputCollectionName[i]))

            if self.Data[i] is None:
                raise Exception(FAIL("NONE Data cannot be added to the Context!"))
            CTX.store(self.OutputCollectionName[i], self.Data[i])

        print()
        
