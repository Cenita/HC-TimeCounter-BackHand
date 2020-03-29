import datetime
import hashlib


def GenerateCode():
    t = str(datetime.datetime.today().date())+"Code"
    sha1 = hashlib.sha1()
    sha1.update(t.encode('utf-8'))
    return sha1.hexdigest()[:4]


def VerifyCode(code):
    if str(code) == GenerateCode():
        return True
    else:
        return False
