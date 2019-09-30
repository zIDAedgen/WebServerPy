import hashlib




def flip_data(string):
    s = chr(ord(string[-1]) ^ 1)
    return string[:-1] + s

def checkMD5(string):
    
    string = string.encode()
    
    mymd5=hashlib.md5()
    mymd5.update(string)
    print(mymd5)
    #if hdm5 != md5:
        #checkMD5return False









if __name__ == '__main__':
    print(flip_data('adhkad'))
