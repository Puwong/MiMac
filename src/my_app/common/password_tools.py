import re
from .error_code import ErrorCode

def check_password( uname, password ):
    if uname == password:
        return False, ErrorCode.ERROR_PWD_EQ_UNAME

    #strength = ['Blank','Very Weak','Weak','Medium','Strong','Very Strong']
    score = 1

    if len(password) < 1:
        return False, ErrorCode.ERROR_PWD_WEAK
    if len(password) < 4:
        return False, ErrorCode.ERROR_PWD_WEAK

    if len(password) >= 8:
        score = score + 1
    if len(password) >= 10:
        score = score + 1

    if re.search('\d+',password):
        score = score + 1
    if re.search('[a-z]',password) or re.search('[A-Z]',password):
        score = score + 1
    if re.search('.,[,!,@,#,$,%,^,&,*,(,),_,~,-,]',password):
        score = score + 1

    if score < 4 :
        return False, ErrorCode.ERROR_PWD_WEAK

    return True, None

