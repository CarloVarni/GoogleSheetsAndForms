
from GoogleSheetsAndForms.Core.GoogleFormSubmitter import GoogleFormSubmitter
from GoogleSheetsAndForms.Core.Messages import FAIL

class GoogleFormSubmitter_PuntiCanaleGravier(GoogleFormSubmitter):
    def __init__(self, NAME: str, FORMLINK: str):
        super().__init__(NAME, FORMLINK,
                         selectionFunction=self.DefaultSelectionFunction,
                         positiveSubmissionUpdate=self.DefaultPositiveSubmissionUpdate,
                         negativeSubmissionUpdate=self.DefaultNegativeSubmissionUpdate)

    def DefaultSelectionFunction(self, req: dict):
        return req['Inserita'] == "N"

    def DefaultPositiveSubmissionUpdate(self, req: dict):
        req['Inserita'] = "Y"
        print("         \\__ Form submitted for: {0}".format(req['AccountTwitch']))

    def DefaultNegativeSubmissionUpdate(self, req: dict):
        print("         \\__ " + FAIL("Error") + " during submission for: {0}".format(req['AccountTwitch']))
