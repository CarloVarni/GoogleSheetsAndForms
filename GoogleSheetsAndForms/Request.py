
from GoogleSheetsAndForms.Core.Messages import NOTE, FAIL

class Request:
    def __init__(self, name: str, labels: list, validator=None, printFormat=None):
        self.__name: str = name
        self.__labels: list[str] = labels
        self.__requests: list = []

        self.__validator = validator
        self.__printFormat = printFormat

        self.__size: int = 0

    @property
    def name(self) -> str:
        return self.__name

    @property
    def requests(self) -> list:
        return self.__requests

    @property
    def labels(self) -> list:
        return self.__labels

    @property
    def size(self) -> int:
        return self.__size
    
    def __str__(self):
        output = NOTE("Summary of requests for Google Sheet: " + self.name) + "\n"

        # Default print format
        if self.__printFormat is None:
            output += "List of " + str(self.size) + " requests... \n"
            for el in self.requests:
                output += "   \\__ " + el.__str__() + "\n"
        # Custom print format
        else:
            output += self.__printFormat(self.requests)

        return output

    def validateRequest(self, req: list):
        if len(req) != len(self.labels):
            raise Exception(FAIL("{0}: Labels do not match with requests due to different sizes: {1} vs {2}!".format(self.name, len(req), len(self.labels))))

        for el in req:
            if not isinstance(el, str):
                raise Exception(FAIL("{0}: Invalid input for entry in Google Sheet due to non-str input!".format(self.name)))
        
    def addRequest(self, el: list):
        # Base Validation
        self.validateRequest(el)
         
        toAdd = {}
        for i in range(0, len(self.labels)):
            toAdd[self.labels[i]] = el[i].strip()

        # Custom Validation
        if self.__validator is not None:
            self.__validator(toAdd)

        self.__requests.append(toAdd)
        self.__size += 1
        
    def processInput(self, results: list):
        for el in results:
            self.addRequest(el)

                
