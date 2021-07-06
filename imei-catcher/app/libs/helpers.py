import subprocess as sp
import json


def check_imei(imei):
    """
    Check the IMEI number
    :rtn: Bool - True if good IMEI
    """
    if len(imei) == 15:
        digits = []
        for i in range(14):
            v = int(imei[i])
            if i % 2:
                v *= 2

            [digits.append(int(x)) for x in str(v)]

        chek = 0
        valu = sum(digits)
        remd = valu % 10
        if remd != 0:
            chek = 10 - remd

        return imei[-1] == str(chek)
    else:
        return False


def process_imei(imei):
    """
        Process the IMEI by exceuting check.py against it.
    """
    if check_imei(imei):
        sh = sp.Popen(["python3.8", "/app/connectors/copy9.py", imei],
                      stdout=sp.PIPE, stderr=sp.PIPE).communicate()
        res = json.loads(sh[0].decode('utf8'))

        for k, v in res.items():
            if v == True:
                return True
        else:
            return False
