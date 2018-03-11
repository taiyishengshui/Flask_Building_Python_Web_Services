import  string
def sanitize_string(userinput):
    whilelist = string.ascii_letters + string.digits + "!@#-=_+"
    return filter(lambda x: x in whilelist, userinput)
print(list(sanitize_string("aaa")))