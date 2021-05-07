
from GoogleSheetsAndForms.Request import Request
from GoogleSheetsAndForms.Core.Messages import FAIL
from GoogleSheetsAndForms.Core.Context import Context

class RequestMaker:
    def __init__(self, NAME: str,
                 validateFunction=None,
                 printFunction=None):
        self.__NAME: str = NAME

        self.__ValuesCollectionName: str = ""
        self.__RequestCollectionName: str = ""

        # This is case dependent
        self.__InputFormat: list = []
        self.__InputLabels: list = []

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
    def NAME(self) -> str:
        return self.__NAME

    @property
    def ValuesCollectionName(self) -> str:
        return self.__ValuesCollectionName

    @ValuesCollectionName.setter
    def ValuesCollectionName(self, value: str):
        if not isinstance(value, str):
            raise Exception(FAIL("Property Error : 'ValuesCollectionName' property of class 'RequestMaker' must be a string!"))
        if len(value) == 0:
            raise Exception(FAIL("Property Error : 'ValuesCollectionName' property of class 'RequestMaker' must not be blank!"))
        self.__ValuesCollectionName = value

    @property
    def RequestCollectionName(self) -> str:
        return self.__RequestCollectionName

    @RequestCollectionName.setter
    def RequestCollectionName(self, value: str):
        if not isinstance(value, str):
            raise Exception(FAIL("Property Error : 'RequestCollectionName' property of class 'RequestMaker' must be a string!"))
        if len(value) == 0:
            raise Exception(FAIL("Property Error : 'RequestCollectionName' property of class 'RequestMaker' must not be blank!"))
        self.__RequestCollectionName = value

    @property
    def InputFormat(self) -> list:
        return self.__InputFormat

    @InputFormat.setter
    def InputFormat(self, value: list):
        if not isinstance(value, list):
            raise Exception(FAIL("Property Error : 'InputFormat' property of class 'RequestMaker' must be a list of types!"))
        if len(value) == 0:
            raise Exception(FAIL("Property Error : 'InputFormat' property of class 'RequestMaker' must have at least one entry!"))
        self.__InputFormat = value

    @property
    def InputLabels(self) -> list:
        return self.__InputLabels

    @InputLabels.setter
    def InputLabels(self, value: list):
        if not isinstance(value, list):
            raise Exception(FAIL("Property Error : 'InputLabels' property of class 'RequestMaker' must be a list!"))
        if len(value) == 0:
            raise Exception(FAIL("Property Error : 'InputLabels' property of class 'RequestMaker' must have at least one entry!"))
        self.__InputLabels = value
        
    def execute(self, CTX: Context):
        if not isinstance(CTX, Context):
            raise Exception(FAIL("Execute method accept Context objects as input!"))
        
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
        CTX.store(self.RequestCollectionName, request.requests)

        print(request)
