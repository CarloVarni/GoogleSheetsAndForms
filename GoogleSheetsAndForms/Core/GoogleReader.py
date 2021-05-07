
from GoogleSheetsAndForms.Core.Messages import FAIL
from GoogleSheetsAndForms.Core.Context import Context

class GoogleReader:
    def __init__(self, NAME: str, ID: str):
        self.__NAME: str = NAME
        self.__ID: str = ID

        self.__ValuesCollectionName: list[str] = [""]
        
    @property
    def NAME(self) -> str:
        return self.__NAME

    @property
    def ID(self) -> str:
        return self.__ID

    @property
    def ValuesCollectionName(self) -> list:
        return self.__ValuesCollectionName

    @ValuesCollectionName.setter
    def ValuesCollectionName(self, value: list):
        if not isinstance(value, list):
            raise Exception(FAIL("Property Error : 'ValuesCollectionName' property of class 'GoogleReader' must be a list of strings!"))
        if len(value) == 0:
            raise Exception(FAIL("Property Error : 'ValuesCollectionName' property of class 'GoogleReader' must contain at least one entry!"))
        for el in value:
            if not isinstance(el, str):
                raise Exception(FAIL("Property Error : 'ValuesCollectionName' property of class 'GoogleReader' must be a list of strings!"))
            if len(el) == 0:
                raise Exception(FAIL("Property Error : 'ValuesCollectionName' property of class 'GoogleReader' must not contain blank entries!"))

        self.__ValuesCollectionName = value
    
    def __str__(self):
        output = "GoogleReader: '" + self.NAME + "' \n"
        output += "   \\__ ID: '{0}'\n".format(self.ID)
        output += "   \\__ Output Values Collection Name: {0}\n".format(self.ValuesCollectionName)
        return output
    
    def execute(self, CTX: Context):
        pass
        
