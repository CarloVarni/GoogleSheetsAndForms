
from GoogleSheetsAndForms.Core.GoogleReader import GoogleReader
from GoogleSheetsAndForms.Core.Messages import NOTE, FAIL
from GoogleSheetsAndForms.Core.Context import Context

class GoogleDocsReader(GoogleReader):
    def __init__(self, NAME: str, ID: str):
        super(GoogleDocsReader, self).__init__(NAME, ID)
    
    def __str__(self):
        return super(GoogleDocsReader, self).__str__()
    
    def execute(self, CTX: Context):
        if not isinstance(CTX, Context):
            raise Exception(FAIL("Execute method accept Context objects as input!"))

        if len(self.ValuesCollectionName) == 0:
            raise Exception(FAIL("Property 'ValuesCollectionName' is blank for '{0}'!".format(self.NAME)))

        print(NOTE("Reading data from Google Docs ... "))
        print("   \\__ Getting Google Docs '{}'".format(self.ID))
        
        document = CTX.retrieve("__SERVICE")["docs"].documents().get(documentId=self.ID).execute()
        print("   \\__ Retrived document with title '{}'".format(document.get('title')))
        print()

        CTX.store(self.ValuesCollectionName[0], document.get('body'))
            
        
