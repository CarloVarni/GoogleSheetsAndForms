
from GoogleSheetsAndForms.Messages import FAIL, NOTE, OK
import requests
import time

class GoogleFormSubmitter:
    def __init__(self, NAME, FORMLINK,
                 selectionFunction=None,
                 positiveSubmissionUpdate=None,
                 negativeSubmissionUpdate=None):
        self.__NAME = NAME
        self.__FORMLINK = "https://docs.google.com/forms/d/e/" + FORMLINK + "/viewform"
        self.InputLabels = []
        self.FormIds = []

        self.RequestCollectionName = ""
        self.UpdatedRequestCollectionName = ""
        
        self.__selectionFunction = selectionFunction
        self.__positiveSubmissionUpdate = positiveSubmissionUpdate
        self.__negativeSubmissionUpdate = negativeSubmissionUpdate
        
    @property
    def NAME(self):
        return self.__NAME

    @property
    def FORMLINK(self):
        return self.__FORMLINK

    def __str__(self):
        output = "GoogleFormSubmitter: '{0}' \n".format(self.NAME)
        output += "   \\__ Form link: " + self.FORMLINK + "\n" 
        output += "   \\__ InputLabels: {} \n".format(self.InputLabels)
        output += "   \\__ FormIds: {} \n".format(self.FormIds)
        output += "   \\__ Input Collection Name: '{0}'\n".format(self.RequestCollectionName)
        output += "   \\__ Output Collection Name: '{0}'\n".format(self.UpdatedRequestCollectionName)
        return output
    
    def execute(self, CTX):
        if len(self.RequestCollectionName) == 0:
            raise Exception(FAIL("Property 'RequestCollectionName' is blank for '{0}'!".format(self.NAME)))
        
        requestList = CTX.retrieve(self.RequestCollectionName).requests

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
