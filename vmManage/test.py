a = "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."

l = []

for i in a :
    if i in "abcdefghijklmnopqrstuvwxyz":
        if i == 'y':
            print('a', end='')
        elif i == 'z':
            print('b', end='')
        else:
            print(chr(ord(i) + 2), end='')
    else:
        print(i, end='')

a.maketrans()
