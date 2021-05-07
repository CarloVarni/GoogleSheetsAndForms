
from GoogleSheetsAndForms.Core.Messages import FAIL, NOTE, OK
from GoogleSheetsAndForms.Core.Context import Context
import requests
import time

class GoogleFormSubmitter:
    def __init__(self, NAME: str, FORMLINK: str,
                 selectionFunction=None,
                 positiveSubmissionUpdate=None,
                 negativeSubmissionUpdate=None):
        self.__NAME: str = NAME
        self.__FORMLINK: str = "https://docs.google.com/forms/d/" + FORMLINK + "/viewform"
        self.__InputLabels: list = []
        self.__FormIds: list = []

        self.__RequestCollectionName: str = ""
        self.__UpdatedRequestCollectionName: str = ""
        
        self.__selectionFunction = selectionFunction
        self.__positiveSubmissionUpdate = positiveSubmissionUpdate
        self.__negativeSubmissionUpdate = negativeSubmissionUpdate
        
    @property
    def NAME(self) -> str:
        return self.__NAME

    @property
    def FORMLINK(self) -> str:
        return self.__FORMLINK

    @property
    def RequestCollectionName(self) -> str:
        return self.__RequestCollectionName

    @RequestCollectionName.setter
    def RequestCollectionName(self, value: str):
        if not isinstance(value, str):
            raise Exception(FAIL("Property Error : 'RequestCollectionName' property of class 'GoogleFormSubmitter' must be a string!"))
        if len(value) == 0:
            raise Exception(FAIL("Property Error : 'RequestCollectionName' property of class 'GoogleFormSubmitter' must not be blank!"))
        self.__RequestCollectionName = value

    @property
    def UpdatedRequestCollectionName(self) -> str:
        return self.__UpdatedRequestCollectionName

    @UpdatedRequestCollectionName.setter
    def UpdatedRequestCollectionName(self, value: str):
        if not isinstance(value, str):
            raise Exception(FAIL("Property Error : 'UpdatedRequestCollectionName' property of class 'GoogleFormSubmitter' must be a string!"))
        if len(value) == 0:
            raise Exception(FAIL("Property Error : 'UpdatedRequestCollectionName' property of class 'GoogleFormSubmitter' must not be blank!"))
        self.__UpdatedRequestCollectionName = value

    @property
    def InputLabels(self) -> list:
        return self.__InputLabels

    @InputLabels.setter
    def InputLabels(self, value: list):
        if not isinstance(value, list):
            raise Exception(FAIL("Property Error : 'InputLabels' property of class 'GoogleFormSubmitter' must be an array of strings!"))
        if len(value) == 0:
            raise Exception(FAIL("Property Error : 'InputLabels' property of class 'GoogleFormSubmitter' must contain at least one element!"))
        for el in value:
            if not isinstance(el, str) and el is not None:
                raise Exception(FAIL("Property Error : 'InputLabels' property of class 'GoogleFormSubmitter' must be an array of strings!"))
            if el is not None and len(el) == 0:
                raise Exception(FAIL("Property Error : 'InputLabels' property of class 'GoogleFormSubmitter' must not contain blank elements!"))
        self.__InputLabels = value

    @property
    def FormIds(self) -> list:
        return self.__FormIds
    
    @FormIds.setter
    def FormIds(self, value: list):
        if not isinstance(value, list):
            raise Exception(FAIL("Property Error : 'FormIds' property of class 'GoogleFormSubmitter' must be an array of strings!"))
        if len(value) == 0:
            raise Exception(FAIL("Property Error : 'FormIds' property of class 'GoogleFormSubmitter' must contain at least one element!"))
        for el in value:
            if not isinstance(el, str) and el is not None:
                raise Exception(FAIL("Property Error : 'FormIds' property of class 'GoogleFormSubmitter' must be an array of strings!"))
            if el is not None and len(el) == 0:
                raise Exception(FAIL("Property Error : 'FormIds' property of class 'GoogleFormSubmitter' must not contain blank elements!"))
        self.__FormIds = value
            
    def __str__(self):
        output = "GoogleFormSubmitter: '{0}' \n".format(self.NAME)
        output += "   \\__ Form link: " + self.FORMLINK + "\n" 
        output += "   \\__ InputLabels: {} \n".format(self.InputLabels)
        output += "   \\__ FormIds: {} \n".format(self.FormIds)
        output += "   \\__ Input Collection Name: '{0}'\n".format(self.RequestCollectionName)
        output += "   \\__ Output Collection Name: '{0}'\n".format(self.UpdatedRequestCollectionName)
        return output
    
    def execute(self, CTX: Context):
        if not isinstance(CTX, Context):
            raise Exception(FAIL("Execute method accept Context objects as input!"))
        if len(self.RequestCollectionName) == 0:
            raise Exception(FAIL("Property 'RequestCollectionName' is blank for '{0}'!".format(self.NAME)))
        
        requestList = CTX.retrieve(self.RequestCollectionName)

        print(NOTE("Compiling Google Form {0} ... ".format(self.NAME)))
        print("   \\__ Compiling Forms for " + self.NAME)
        print("      \\__ Form: " + self.FORMLINK)

        counterUpdatedRequests = 0
        counterFailedRequests = 0

        for el in requestList:
            if self.__selectionFunction is not None:
                if not self.__selectionFunction(el):
                    continue

            d = {}
            for j in range(0, len(self.FormIds)):
                if self.FormIds[j] is None:
                    continue
                d[self.FormIds[j]] = el[self.InputLabels[j]]
            
            x = requests.post(self.FORMLINK.replace("viewform", "formResponse"), data=d)
            if x.status_code == requests.codes.ok:
                if self.__positiveSubmissionUpdate is None:
                    print("         \\__ Form Submitted for: {}".format(d))
                else:
                    self.__positiveSubmissionUpdate(el)

                counterUpdatedRequests += 1
                time.sleep(1)     
            else:
                if self.__negativeSubmissionUpdate is not None:
                    self.__negativeSubmissionUpdate(el)
                else:
                    print(FAIL("An error has occured and entry could not be submitted: {}".format(el)))
                counterFailedRequests += 1
                
        print(OK("      \\__ Total Entries Submitted : " + str(counterUpdatedRequests)))
        if counterFailedRequests != 0:
            print(FAIL("         \\__ Total Entries Failed : " + str(counterFailedRequests)))

        CTX.store(self.UpdatedRequestCollectionName, requestList)
        print()
