
from GoogleSheetsAndForms.Messages import NOTE, FAIL

class DataAdder:
    def __init__(self, NAME):
        self.__NAME = NAME
        
        self.OutputCollectionName = []
        self.Data = []
        
    @property
    def NAME(self):
        return self.__NAME

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
        
