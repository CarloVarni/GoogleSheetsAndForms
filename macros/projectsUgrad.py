
from GoogleSheetsAndForms.Core.Context import Context
from GoogleSheetsAndForms.ProjectUgrad import ProjectUgrad
from GoogleSheetsAndForms.Core.Messages import FAIL, NOTE, OK
import json

class CompareUgradProjects:
    def __init__(self, NAME: str, UPDATE: bool = False):
        self.__NAME: str = NAME
        self.__UPDATE: bool = UPDATE

        self.__RefFile: str = ""
        self.__ProjectCollectionName: str = ""
        self.__DiffCollectionName: str = ""
        
    @property
    def NAME(self) -> str:
        return self.__NAME

    @property
    def UPDATE(self) -> bool:
        return self.__UPDATE
    
    @property
    def RefFile(self) -> str:
        return self.__RefFile

    @RefFile.setter
    def RefFile(self, value: str):
        if not isinstance(value, str):
            raise Exception(FAIL("Property Error : 'RefFile' property of class 'CompareUgradProjects' must be a string!"))
        if value == "":
            raise Exception(FAIL("Property Error : 'RefFile' property of class 'CompareUgradProjects' must not be blank!"))

        self.__RefFile = value

    @property
    def ProjectCollectionName(self) -> str:
        return self.__ProjectCollectionName

    @ProjectCollectionName.setter
    def ProjectCollectionName(self, value: str):
        if not isinstance(value, str):
            raise Exception(FAIL("Property Error : 'ProjectCollectionName' property of class 'CompareUgradProjects' must be a string!"))
        if value == "":
            raise Exception(FAIL("Property Error : 'ProjectCollectionName' property of class 'CompareUgradProjects' must not be blank!"))

        self.__ProjectCollectionName = value

    @property
    def DiffCollectionName(self) -> str:
        return self.__DiffCollectionName

    @DiffCollectionName.setter
    def DiffCollectionName(self, value: str):
        if not isinstance(value, str):
            raise Exception(FAIL("Property Error : 'DiffCollectionName' property of class 'CompareUgradProjects' must be a string!"))
        if value == "":
            raise Exception(FAIL("Property Error : 'DiffCollectionName' property of class 'CompareUgradProjects' must not be blank!"))

        self.__DiffCollectionName = value
    
    def __str__(self):
        output = "CompareUgradProjects: '{0}'\n".format(self.NAME)
        output += "   \\__ Update Mode: '{0}'\n".format(self.UPDATE)
        output += "   \\__ Reference File: '{0}'\n".format(self.RefFile)
        output += "   \\__ Project Collection: '{0}'\n".format(self.ProjectCollectionName)
        output += "   \\__ Differences Collection: '{0}'\n".format(self.DiffCollectionName)
        return output
        
    def execute(self, CTX: Context):
        if not isinstance(CTX, Context):
            raise Exception(FAIL("Execute method accept Context objects as input!"))

        if self.RefFile == "":
            raise Exception(FAIL("Property 'RefFile' is blank for '{0}'!".format(self.NAME)))
        if self.ProjectCollectionName == "":
            raise Exception(FAIL("Property 'ProjectCollectionName' is blank for '{0}'!".format(self.NAME)))
        if self.DiffCollectionName == "":
            raise Exception(FAIL("Property 'DiffCollectionName' is blank for '{0}'!".format(self.NAME)))
        
        print(NOTE("Checking projects ..."))
        
        projectCollection = CTX.retrieve(self.ProjectCollectionName)
        for el in projectCollection:
            print(projectCollection[el])

        if self.UPDATE:
            self.updateReferenceFile(projectCollection)
            return

        diffs = self.compareWithReference(projectCollection)

        print(NOTE("Checking differences ..."))
        for el in diffs:
            proj = diffs[el]
            print("   \\__ Difference for project '" + el + "' with following reason: {}".format(proj[1]))
        if len(diffs) == 0:
            print("   \\__ {0}".format(OK("All projects are up-to-date!")))

        print()

        toSave = []
        for el in diffs:
            proj = diffs[el]
            toAdd = {}
            toAdd['title'] = proj[0].title
            toAdd['description'] = proj[0].description
            toAdd['other'] = proj[0].other
            toAdd['contact'] = proj[0].contact
            toAdd['email'] = proj[0].email
            toAdd['reason'] = proj[1]
            toSave.append(toAdd)
        CTX.store(self.DiffCollectionName, toSave)

        
    def createDictionary(self, collection: list) -> dict:
        data = {}
        for proj in collection:
            el = collection[proj]
            toAdd = {}
            toAdd['title'] = el.title
            toAdd['description'] = el.description
            toAdd['other'] = el.other
            toAdd['contact'] = el.contact
            toAdd['email'] = el.email
            data[el.title] = toAdd
        return data
        
    def updateReferenceFile(self, data: dict) -> None:
        print(OK("Updating reference file : '{0}'\n".format(self.RefFile)))
        dataDict = self.createDictionary(data)
        refFile = open(self.RefFile, 'w')
        json.dump(dataDict, refFile)
        refFile.close()
        
    def compareWithReference(self, new_data: dict) -> dict:
        differences = {}
        
        print("Retrieving reference data from file: '{0}'".format(self.RefFile))
        refFile = open(self.RefFile, 'r')
        ref_rawdata = json.load(refFile)
        refFile.close()

        ref_data = {}
        for key in ref_rawdata:
            el = ref_rawdata[key]
            toAdd = ProjectUgrad(el["title"],
                                 el["description"],
                                 el["other"],
                                 el["contact"],
                                 el["email"])
            ref_data[toAdd.title] = toAdd

        for key in new_data:
            print("   \\__ Checking project: '{}'".format(key))
            newProj = new_data[key]
            refProj = ref_data.get(key, None)
            if refProj is None:
                differences[key] = [newProj, ["new entry"]]
                continue

            if newProj == refProj:
                continue

            diffs = newProj.diffFields(refProj)
            differences[key] = [newProj, diffs]

        print("   \\__ Checking removed project ...")
        for key in ref_data:
            oldProj = ref_data[key]
            if new_data.get(key, None) is not None:
                continue

            differences[key] = [oldProj, ["removed"]]

        print()
        return differences

    
if __name__ == "__main__":
    from GoogleSheetsAndForms.Core.GoogleBot import GoogleBot
    from GoogleSheetsAndForms.Core.GoogleDocsReader import GoogleDocsReader
    from GoogleSheetsAndForms.ProjectUgradMaker import ProjectUgradMaker
    from GoogleSheetsAndForms.Core.GoogleFormSubmitter import GoogleFormSubmitter
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--update', action='store_true')
    parser.add_argument('-j', '--json', nargs=1, required=True)
    parser.add_argument('-r', '--ref', nargs=1, required=True)
    args = parser.parse_args()

    update = args.update
    jsonFile = args.json[0]
    refFile = args.ref[0]

    try:
        myfile = open(jsonFile, "r")
        myfile.close()
    except Exception:
        raise Exception(FAIL("JSON file cannot be opened!"))

    try:
        if not update:
            myfile = open(refFile, "r")
            myfile.close()
    except Exception:
        raise Exception(FAIL("REF file cannot be opened!"))
    
    # Main Code
    googleBot = GoogleBot("GoogleBot", jsonFile)

    googleReader = GoogleDocsReader("GoogleDocsReader", "1J_HWxp1mDvQXXoRGyE1fYsHSV9uAW6mG6eGeHu88frI")
    googleReader.ValuesCollectionName = ["DOCUMENT"]
    googleBot.addExecutable(googleReader)

    projectMaker = ProjectUgradMaker("ProjectUgradMaker")
    projectMaker.DocumentCollectionName = googleReader.ValuesCollectionName[0]
    projectMaker.ProjectsCollectionName = "PROJECTS"
    googleBot.addExecutable(projectMaker)

    projectComparator = CompareUgradProjects("CompareUgradProjects", update)
    projectComparator.RefFile = refFile
    projectComparator.ProjectCollectionName = projectMaker.ProjectsCollectionName
    projectComparator.DiffCollectionName = "DIFFS"
    googleBot.addExecutable(projectComparator)

    if not update:
        formSubmitter = GoogleFormSubmitter("GoogleFormSubmitter", "1avHrLEmP7yK6kWPwa3Z2pHFez30Fu4cczFrKtTm_nPE")
        formSubmitter.RequestCollectionName = projectComparator.DiffCollectionName
        formSubmitter.UpdatedRequestCollectionName = "SUBMITTED"
        formSubmitter.InputLabels = ['title', 'description', 'other', 'contact', 'email', 'reason']
        formSubmitter.FormIds = ['entry.1923020704', 'entry.1943963817', 'entry.265502880', 'entry.1865927878', 'entry.187158238', 'entry.1940199514']
        googleBot.addExecutable(formSubmitter)

    googleBot.execute()
