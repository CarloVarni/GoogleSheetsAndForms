
from GoogleSheetsAndForms.GoogleFormSubmitter import GoogleFormSubmitter
from GoogleSheetsAndForms.Messages import FAIL

class GoogleFormSubmitter_PuntiCanaleGravier(GoogleFormSubmitter):
    def __init__(self, NAME, FORMLINK):
        super().__init__(NAME, FORMLINK,
                         selectionFunction=self.DefaultSelectionFunction,
                         positiveSubmissionUpdate=self.DefaultPositiveSubmissionUpdate,
                         negativeSubmissionUpdate=self.DefaultNegativeSubmissionUpdate)

    def DefaultSelectionFunction(self, req):
        return req['Inserita'] == "N"

    def DefaultPositiveSubmissionUpdate(self, req):
        req['Inserita'] = "Y"
        print("         \\__ Form submitted for: {0}".format(req['AccountTwitch']))

    def DefaultNegativeSubmissionUpdate(self, req):
        print("         \\__ " + FAIL("Error") + " during submission for: {0}".format(req['AccountTwitch']))
