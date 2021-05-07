
from GoogleSheetsAndForms.Core.Context import Context
from GoogleSheetsAndForms.Core.Messages import NOTE, FAIL
from GoogleSheetsAndForms.ProjectUgrad import ProjectUgrad
import re

class ProjectUgradMaker:
    def __init__(self, NAME: str):
        self.__NAME = NAME
        
        self.__DocumentCollectionName: str = ""
        self.__ProjectsCollectionName: str = ""

    @property
    def NAME(self) -> str:
        return self.__NAME

    @property
    def DocumentCollectionName(self) -> str:
        return self.__DocumentCollectionName

    @DocumentCollectionName.setter
    def DocumentCollectionName(self, value: str):
        if not isinstance(value, str):
            raise Exception(FAIL("Property Error : 'DocumentCollectionName' property of class 'ProjectUgradMaker' must be a string!"))
        if len(value) == 0:
            raise Exception(FAIL("Property Error : 'DocumentCollectionName' property of class 'ProjectUgradMaker' must not be blank!"))
        self.__DocumentCollectionName = value

    @property
    def ProjectsCollectionName(self) -> str:
        return self.__ProjectsCollectionName

    @ProjectsCollectionName.setter
    def ProjectsCollectionName(self, value: str):
        if not isinstance(value, str):
            raise Exception(FAIL("Property Error : 'ProjectsCollectionName' property of class 'ProjectUgradMaker' must be a string!"))
        if len(value) == 0:
            raise Exception(FAIL("Property Error : 'ProjectsCollectionName' property of class 'ProjectUgradMaker' must not be blank!"))
        self.__ProjectsCollectionName = value
    
    def __str__(self):
        output = "ProjectUgradMaker: '{0}'\n".format(self.NAME)
        output += "   \\__ Input Document Collection Name: '{0}'\n".format(self.DocumentCollectionName)
        output += "   \\__ Output Collection Name: '{0}' \n".format(self.ProjectsCollectionName)
        return output
    
    def execute(self, CTX: Context):
        if not isinstance(CTX, Context):
            raise Exception(FAIL("Execute method accept Context objects as input"))

        if self.DocumentCollectionName == "":
            raise Exception(FAIL("Property 'DocumentCollectionName' is blank for '{0}'!".format(self.NAME)))
        if self.ProjectsCollectionName == "":
            raise Exception(FAIL("Property 'ProjectsCollectionName' is blank for '{0}'!".format(self.NAME)))

        print(NOTE("Creating Project Entries..."))
        
        values = CTX.retrieve(self.DocumentCollectionName)

        delimited_text = []
        filtered_text = []
        storeEntry = False

        for el in values['content']:
            if el.get('paragraph', None) is None:
                continue

            textElements = el['paragraph']['elements']
            text = ""
            for el in textElements:
                if len(el['textRun']['content'].strip()) == 0:
                    continue
                text += el['textRun']['content'].strip()

#            text = el['paragraph']['elements'][0]['textRun']['content'].strip()

            if len(text) == 0:
                continue
            if not storeEntry and text == "Projects:":
                storeEntry = True
                continue
            
            if storeEntry:
                if "title:" in text.lower():
                    if len(filtered_text) != 0:
                        delimited_text.append(filtered_text)
                    filtered_text = []
                filtered_text.append(text)

        if storeEntry and len(filtered_text) != 0:
            delimited_text.append(filtered_text)

        projects = self.createProjects(delimited_text)
        CTX.store(self.ProjectsCollectionName, projects)
        
    def createProjects(self, text: list) -> list:
        projectList = {}
        for el in text:
            parsed = self.parseInfo(el)
            project = ProjectUgrad(parsed["title"],
                                   parsed["description"],
                                   parsed["other"],
                                   parsed["contact"],
                                   parsed["email"])
            if projectList.get(project.title, None) is not None:
                raise Exception(FAIL("The project '{}' has already been recorded... Possible duplication of entries or two entries with same name?".format(project.title)))
            projectList[project.title] = project
            print(project)
        return projectList
    
    def parseInfo(self, info: list) -> dict:
        output = {"title": "",
                  "description": "",
                  "other": [],
                  "contact": "",
                  "email": []}
        
        for el in info:
            el = el.strip()
            titleParse = re.findall("^Title:(.*)", el)
            if len(titleParse) != 0:
                output['title'] = titleParse[0].strip()
                continue

            descriptionParse = re.findall("^Description:(.*)", el)
            if len(descriptionParse) != 0:
                output["description"] = descriptionParse[0].strip()
                continue

            contactParse = re.findall("^Contact.*:(.*)", el)
            if len(contactParse) != 0:
                name_mail = re.findall("^([^\[]+)\W+([^\[]+@[^\]]+)", contactParse[0])
                output["contact"] = [name_mail[0][0].strip()]
                output["email"] = name_mail[0][1].strip().split(",")
                continue

            output["other"].append(el)

        return output
