
from GoogleSheetsAndForms.Core.Messages import FAIL

class Context:
    def __init__(self):
        self.__CTX: dict = {}

    @property
    def CONTEXT(self):
        return self.__CTX
        
    def retrieve(self, objName: str):
        if objName is None:
            raise Exception(FAIL("Cannot Retrieve None Object From Context!"))
        if not isinstance(objName, str):
            raise Exception(FAIL("Cannot Retrieve Non-String-Keyed Object From Context: {}!".format(objName)))

        output = self.CONTEXT.get(objName, None)
        if output is None:
            raise Exception(FAIL("Context has no {0} object!".format(objName)))
        return output

    def store(self, objName: str, obj):
        if not isinstance(objName, str):
            raise Exception(FAIL("Storing key MUST be a string!"))
        if obj is None:
            raise Exception(FAIL("Stored object MUST NOT be None!"))
        if self.CONTEXT.get(objName, None) is not None:
            raise Exception(FAIL("Cannot over-write object in Context!"))

        self.__CTX[objName] = obj
