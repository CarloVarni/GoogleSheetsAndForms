
class ProjectUgrad:
    def __init__(self, TITLE: str, DESCRIPTION: str, OTHER: list, CONTACT: list, EMAIL: list):
        self.__title: str = TITLE
        self.__description: str = DESCRIPTION
        self.__other: list[str] = OTHER
        self.__contact: list = CONTACT
        self.__email: list = EMAIL
        
    @property
    def title(self) -> str:
        return self.__title

    @property
    def description(self) -> str:
        return self.__description

    @property
    def other(self) -> list:
        return self.__other

    @property
    def contact(self) -> list:
        return self.__contact

    @property
    def email(self) -> list:
        return self.__email
        
    def __str__(self):
        output = "Project:\n"
        output += "   \\__ Title: " + self.title + "\n"
        output += "   \\__ Description: " + self.description + "\n"
        output += "   \\__ Other Info: \n"
        for el in self.other:
            output += "      \\__ " + el + "\n"
        output += "   \\__ Contact: {}\n".format(self.contact)
        output += "   \\__ e-Mail: {}\n".format(self.email)
        return output

    def __eq__(self, other):
        if self.title != other.title:
            return False
        if self.description != other.description:
            return False
        if self.other != other.other:
            return False
        if self.contact != other.contact:
            return False
        if self.email != other.email:
            return False
        return True

    def diffFields(self, other) -> list:
        output = []
        if self.title != other.title:
            output.append("title")
        if self.description != other.description:
            output.append("description")
        if self.other != other.other:
            output.append("other")
        if self.contact != other.contact:
            output.append("contact")
        if self.email != other.email:
            output.append("email")
        return output
                
