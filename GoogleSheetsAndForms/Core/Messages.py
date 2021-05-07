
def NOTE(message):
    return "{0}{1}{2}".format("\033[1;35m", message, "\033[0;0m")

def OK(message):
    return "{0}{1}{2}".format("\033[1;32m", message, "\033[0;0m")

def WARNING(message):
    return "{0}{1}{2}".format("\033[1;33m", message, "\033[0;0m")

def FAIL(message):
    return "{0}{1}{2}".format("\033[1;31m", message, "\033[0;0m")


if __name__ == "__main__":
    print(NOTE("This is a NOTE message"))
    print(OK("This is a OK message"))
    print(WARNING("This is a WARNING message"))
    print(FAIL("This is a FAIL message"))

    
