
from GoogleSheetsAndForms.Request import Request
from GoogleSheetsAndForms.Messages import FAIL

class RequestMaker:
    def __init__(self, NAME,
                 validateFunction=None,
                 printFunction=None):
        self.__NAME = NAME

        self.ValuesCollectionName = ""
        self.RequestCollectionName = ""

        # This is case dependent
        self.InputFormat = []
        self.InputLabels = []

        self.__validateFunction = validateFunction
        self.__printFunction = printFunction
        
    def __str__(self):
        output = "RequestMaker: '{0}' \n".format(self.NAME)
        output += "   \\__ InputFormat: {} \n".format(self.InputFormat)
        output += "   \\__ InputLabels: {} \n".format(self.InputLabels)
        output += "   \\__ Input Values Collection Name: '{0}'\n".format(self.ValuesCollectionName)
        output += "   \\__ Output Collection Name: '{0}' \n".format(self.RequestCollectionName)
        return output

    @property
    def NAME(self):
        return self.__NAME
    
    def execute(self, CTX):

        if self.ValuesCollectionName == "":
            raise Exception(FAIL("Property 'ValuesCollectionName' is blank for '{0}'!".format(self.NAME)))
        if self.RequestCollectionName == "":
            raise Exception(FAIL("Property 'RequestCollectionName' is blank for '{0}'!".format(self.NAME)))

        if len(self.InputFormat) != len(self.InputLabels):
            raise Exception(FAIL("Format and Labels do not match for '{0}' due to different sizes!".format(self.NAME)))
        for i in range(0, len(self.InputFormat)):
            if (self.InputFormat[i] is None or self.InputLabels[i] is None) and self.InputFormat[i] != self.InputLabels[i]:
                raise Exception(FAIL("Format and Labels do not match for '{0}'!".format(self.NAME)))
        
        values = CTX.retrieve(self.ValuesCollectionName)

        filteredRequests = []
        for req in values:
            if len(req) != len(self.InputFormat):
                continue
            toAdd = [req[i] for i in range(0, len(req)) if self.InputFormat[i] is not None]
            filteredRequests.append(toAdd)

        request = Request(self.RequestCollectionName,
                          labels=[el for el in self.InputLabels if el is not None], 
                          validator=self.__validateFunction,
                          printFormat=self.__printFunction)
        request.processInput(filteredRequests)
        CTX.store(self.RequestCollectionName, request)

        print(request)
