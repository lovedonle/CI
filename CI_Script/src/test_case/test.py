# -*- coding: utf-8 -*-
#import re
#
#file_hand = open(r"C:\text.txt")
#content = file_hand.read()
#file_hand.close()
#re_obj = "<plugin>\n.*\n.*<artifactId>wagon-maven-plugin</artifactId>(\n.*){1,15}<url>scp.*</url>(\n.*){1,20}</plugin>"#"<plugin>\r\n.*\r\n.*<artifactId>wagon-maven-plugin</artifactId>(\r\n.*){1,15}<url>scp.*</url>(\r\n.*){1,20}</plugin>"
#a = re.subn(re_obj,"",content,0,flags=re.IGNORECASE)
#print a


#def test():
#    print a
#if __name__== '__main__':
#    a = 'yes'
#    test()

# def enum(**enums):
#     return type('Enum', (), enums)
#  
# Numbers = enum(ONE=1, TWO=2, THREE='three')
# print Numbers.ONE
# print Numbers.TWO
# print Numbers.THREE
# print Numbers.__name__
# print Numbers.__bases__ 
# print Numbers.__dict__ 

def A(a):
    print a
    
A([1,2,3])
#if m is not None:
#    print m.group()
#import os
#import re
#def funcA(a=1,b=0,*c,**d):
#    print a
#    print b
#    print c
#    print d
##if __name__ == '__main__':
##    funcA(1,2,4,8,6,9,c=2,d=3)
#    
#'''    
#for a,b,c in os.walk(r"E:\34package"):
#    print a,b,c
#'''
##匹配正整数
#print re.search("^[1-9]$|^[1-9]\d+", "").group()
##不含abc字符串
#print re.search("^((?!abc).)+$", "asdabqwerrre").group()
##匹配二进制字符串
#print re.search("^[01]+$", "11111010101101").group()

#from hashlib import md5
#md = md5()
#md.update("amount=50000&chargeType=01&merchantCode=1000000431&noticeUrl=http://192.168.6.34:10000/merchant/telcharge_notice.jsp&outOrderId=83359903782735557022148768081237&phone=15928140495&KEY=123456ADSEF")
#psw = md.hexdigest()
#print psw

#a = {"a":1,"b":u"测试"}
#print a
#import base64
#NUMSLETTER_A_F = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B","C", "D", "E", "F"]
#a=base64.decodestring("MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDcBUsvOOllqwsDBhD8iTcSUFlXciduSD7aWrXNyXnpo24D8gbvKlyqdL/GtFd9N3277UkOdM1miEWMHPFCRunp8dwz2ykrrBAp/slWC5rgmV3WWA1vdlVgH9YLG5dlXm/PSvOatDrw6U+2qswC2V+iP/bLK64xtAWRwZRSw0ztHwIDAQAB")
#b=base64.decodestring("MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAOOIBvaPFQhQ3Mpl8MdOZjDDajADCWxEXP/lXSonV5U04A01XGNNs5yCBxMJbjKS1kmKmQmChkAfmadNlpKmVtc7qsdZq2K90Eg0/9T4cjn/cdKDc/zR0bMwn2NdfVe5Y3uxWB3eRqLTE1TTAXzzLnPm1Ls0uLdFh7PfPnxqCj6DAgMBAAECgYAfDwh0S5/BXNhmwHeXnToR2fr6xs9YehR/0d1fzbME6QzUgL41x/uGl7FDhfwG50hdDZBKXgjZY/bjgZHWPuKHiO390C659Ioy3FmRAk++eoFdTGU46SsBQrMDwqu1AEcxHj0GrP3wSZ7PNOTY6eZb4v/XtlhdRwRcrIyAguKoUQJBAPmtsGOYEHPdCLj5AjbpecUyXWqNn2USwXly4HDe4b8+HLjbqfeeBGAQVuaL14k3LlIVCI7jBJaxqDkfvlyUSW0CQQDpSso1L+8DCPTH2OJToGwla3mC0mklb9ZAo0//Hsj24NLwhtfFVPdJULCN2mFmjYM9E6Mh6YLavlw0tZOL6SGvAkAm8mgUcREH8c+9guJMjIj5MM0PpP3bN1zExB2snafbPCYg0+skfBq0nXfgyKmbducb2LoYB+OcWiQinQgFyv/VAkBs8Ov0YmnutOP53yHxg1x9LO8VVESdotgeXyUgMbQO9XYLtCxWjhLcPb30wCHzzemXP/BSCcV9eJ9+TbyU/U0pAkEA4DShPeSvije4tiQIJ+R/4sn3S/euYehCLzatMRdYfCC+wV/TPUTR/2ZtLJt5XC5AqwKll8aASn0tjPhiwIwA4Q==")
#b=base64.decodestring("MC4CAQACBQDeKYlRAgMBAAECBQDHn4npAgMA/icCAwDfxwIDANcXAgInbwIDAMZt")
#python
#b=base64.decodestring("MIICYAIBAAKBgQDMtfvgLEaWtFSYRK3x0joIjtv4j7bsnMI2eqtGz7MqD15ieSAdHKrqvUJX7JQggZBNH+uKnfpzi3XNqz2tBgN2v4UqCwgrG2Cz5COvaCspsrKkRuWI9meSxsIcpa5DQ9LQTN2vW+D+HCNBLUOzEvydqrFWGDW/DQEV3z07p1ljewIDAQABAoGAW9yaP5l+v6gCgiXnrKl681YwLdVH79vUZyAa9fbEXm5xG11hZM71f8sYF16JhiC+AW3+g8Cqn+kIHxflcD+Qq+Tefizq3VrcWc7LLAGtH5Imx/FwJW63gbUiTl6WsWBHRb+j43RkAEY9xw4B5yJ8HBHAfHuVZexxFD4gVKCwDhECRQD51bPWPnWMIYPVMtCc9ru8R9yQo6wBjm+t4rvXwLN9bTE/e+b92h/BjWjyUc/QXcpNbcHqrF6K0ScRkCTrGUa3XnhciQI9ANHDN50mUPRcNBDaOrHm8DSLbc9LdQapT3orKWsPZm2BGStyUoDwLCnZ51KmaFEwuRC8fwlE/YwD8wsm4wJEAZra1eR+0tCgTS1PY8K9//6iLxeuEjB9DSvoswEc5hBegZ7lI/pTu+WRqATYhekkVI0A8uX6kX+4dYdshUobRzBHK6kCPQCGTbDI/KRuoK5xb9iO2WdIrVEknZKTLkqF1SbStmyFhlgAOlVa2uvb6/mxMHywJzsG3TmVTMfuIwU1SbMCRG6ghAuiDGyzp7wrQjuUPkaT3kOnBNcsmTy+4ncHJlwa3aH/e+82euRVGDbAeIeaeoUFLDelLUa0K/jgWBDnaV7vGP/R")
#a=base64.decodestring("MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDcBUsv")
#keyhex = []
#for char in a:
#    keyhex.append(NUMSLETTER_A_F[ord(char)>>4&0xf])
#    keyhex.append(NUMSLETTER_A_F[ord(char)&0xf])
#print ''.join(keyhex)

#from binascii import unhexlify as unhex
#from binascii import hexlify as hex
#
#print ("123123abtttt").encode('ascii')
#import rsa
#p1,p2 = rsa.newkeys(1024)
#print "Hello world"
#
#pk = rsa.PrivateKey(13076722682216217668911727294272583229838313778589672850250677075029242416142220961748947024904847449796499629984160803974120604478629965910532982522005869, 65537, 21810176823815734192455345922147068855372457662907797957613070253777084433951304639547406351961166694456550149254274514001403543862780834747273792517924541606172821695315445328569104991781894377103907453936694565832248591293657342500136229724794543526638544615998952140256703369786926910139510516367029872721, 13076722682216217668911727294272583229838313778589672850250677075029242416142220961748947024904847449796499629984160803974120604478629965910532982522005869, 12218501215696562293057120430324994557924691115641465305634877646905553368069262192333803355986940761475190404884565898687925579923213377574918121845236143)
#print pk.exp1
#print pk.exp2
#print pk.coef
#s=base64.encodestring(rsa.PrivateKey.save_pkcs1(pk,format="DER"))
#print s

#s=rsa.newkeys(1024)
#pub=rsa.PublicKey.load_pkcs1(a, format='DER')
#pub=rsa.PublicKey.load_pkcs1_openssl_der(a)
#print "abc"
#prb=rsa.PrivateKey.load_pkcs1(b, format='DER')
#print "def"

#转为32位的16进制，高位补0
#keyHex = []
##Python提供了ord和chr两个内置的函数，用于字符与ASCII码之间的转换。
#for char in key:
#keyHex.append(self.NUMSLETTER_A_F[ord(char)>>4&0xf])
#keyHex.append(self.NUMSLETTER_A_F[ord(char)&0xf])
#keyhexstr = ''.join(keyHex)
#from binascii import unhexlify 
#from binascii import hexlify
#from pyDes import *
#
#a = "68F5504504CCFCF56C84FE20B11D0E01"
#len(a)
#b = unhexlify(a)
#len(b)
#print b
#
#data = "test"
#k = triple_des(unhexlify("816704ECA539B2DF213D640EBF8AC759"),pad='0')
#d = hexlify(k.encrypt(data))
#print "Encrypted: %r" % d
#print "Decrypted: %r" % k.decrypt(unhexlify(d))
#assert k.decrypt(unhexlify(d)) == data
#
#from M2Crypto.X509 import RSA
#from base64 import b64decode
#
#key64 = b"MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAOOIBvaPFQhQ3Mpl8MdOZjDDajADCWxEXP/lXSonV5U04A01XGNNs5yCBxMJbjKS1kmKmQmChkAfmadNlpKmVtc7qsdZq2K90Eg0/9T4cjn/cdKDc/zR0bMwn2NdfVe5Y3uxWB3eRqLTE1TTAXzzLnPm1Ls0uLdFh7PfPnxqCj6DAgMBAAECgYAfDwh0S5/BXNhmwHeXnToR2fr6xs9YehR/0d1fzbME6QzUgL41x/uGl7FDhfwG50hdDZBKXgjZY/bjgZHWPuKHiO390C659Ioy3FmRAk++eoFdTGU46SsBQrMDwqu1AEcxHj0GrP3wSZ7PNOTY6eZb4v/XtlhdRwRcrIyAguKoUQJBAPmtsGOYEHPdCLj5AjbpecUyXWqNn2USwXly4HDe4b8+HLjbqfeeBGAQVuaL14k3LlIVCI7jBJaxqDkfvlyUSW0CQQDpSso1L+8DCPTH2OJToGwla3mC0mklb9ZAo0//Hsj24NLwhtfFVPdJULCN2mFmjYM9E6Mh6YLavlw0tZOL6SGvAkAm8mgUcREH8c+9guJMjIj5MM0PpP3bN1zExB2snafbPCYg0+skfBq0nXfgyKmbducb2LoYB+OcWiQinQgFyv/VAkBs8Ov0YmnutOP53yHxg1x9LO8VVESdotgeXyUgMbQO9XYLtCxWjhLcPb30wCHzzemXP/BSCcV9eJ9+TbyU/U0pAkEA4DShPeSvije4tiQIJ+R/4sn3S/euYehCLzatMRdYfCC+wV/TPUTR/2ZtLJt5XC5AqwKll8aASn0tjPhiwIwA4Q=="
#
#keyDER = b64decode(key64)
#keyPub = RSA.importKey(keyDER)
#coding:utf-8
#f=open(r'C:\Users\cfds\Desktop\a.txt','r')
#f2=open(r'C:\Users\cfds\Desktop\b.txt','w')
#for line in f:
#    if 'f' in line:
#        print line
#        s = line.replace("\\","\\\\")
#        print s
#        f2.write(s)
#f.close()
#f2.close()

#import socket
#host = "localhost"
#port = 21567
#addr = (host,port)
#s = socket(socket.AF_INET,socket.SOCK_STREAM)

