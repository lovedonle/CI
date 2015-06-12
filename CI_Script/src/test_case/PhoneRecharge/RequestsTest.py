# -*- coding: utf-8 -*-
'''
Created on 2015-3-19

@author: cfds
'''
import requests
import json
import random
import base64
import rsa
from binascii import unhexlify as unhex
from binascii import hexlify
from pyDes import *
from hashlib import md5
from Constants import Constants
from Config import Config

class RequestsTest(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.LETTERS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n","o", "p", "q",
                         "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", 
                         "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        self.NUMS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.LETTERNUMS = [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", 
                           "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", 
                           "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
                           "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        self.NUMSLETTER_A_F = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B","C", "D", "E", "F"]
        
    def _orgSignSrc(self,signFields, dict_packet):
        signSrc = ""
        i = 0
        for key in signFields:
            signSrc=signSrc+key
            signSrc=signSrc+Constants.EQUAL
            if dict_packet[key] is not None:
                signSrc=signSrc+str(dict_packet[key])
            #最后一个元素后面不加&
            if i < (len(signFields) - 1):
                signSrc=signSrc+"&"
            i=i+1
        #print signSrc
        return signSrc.decode('utf-8')
    
    def _getMessageDigest(self,signSrc):
        md = md5()
        md.update(signSrc)
        psw = md.hexdigest()
        return psw
        
    def phoneRecharge(self,merchantcode=Config.merchantCode_Telrecharge,phone="15928140495",amount=50000l):
        self.outorderid = str(random.randint(1000000,9999999))
        self.merchantcode = merchantcode
        param = {Constants.MERCHANTCODE:self.merchantcode,
                 Constants.OUTORDERID:self.outorderid,
                 Constants.PHONE:phone,
                 Constants.AMOUNT:amount,
                 Constants.CHARGETYPE:"01",
                 Constants.NOTICEURL:"http://192.168.6.34:10000/merchant/telcharge_notice.jsp",
                 Constants.REMARK:u"测试话费充值"
                 }
        signFields = [Constants.MERCHANTCODE, Constants.OUTORDERID, Constants.PHONE, Constants.AMOUNT,
                Constants.CHARGETYPE, Constants.NOTICEURL]
        signFields.sort()#加密原数据一定要按照键值升序排列
        signSrc = self._orgSignSrc(signFields,param)
        signSrc = signSrc+"&KEY=123456ADSEF"
        sign = self._getMessageDigest(signSrc).upper();#注意这里必须要把MD5 转换成大写；默认的都是小写
        param[Constants.SIGN] = sign
        json_param = json.dumps(param,sort_keys=True)
        print u"话费充值请求报文:" + json_param
        recharge = requests.post("http://192.168.6.34:10086/telcharges/charge.do",data=json_param)
        print u"话费充值应答报文:" + recharge.text
    def phoneQuery(self):
        param = {Constants.MERCHANTCODE:self.merchantcode,
                 Constants.OUTORDERID:self.outorderid
                 }
        signFields = [Constants.MERCHANTCODE,Constants.OUTORDERID]
        signSrc = self._orgSignSrc(signFields, param)
        signSrc = signSrc+"&KEY=123456ADSEF"
        sign = self._getMessageDigest(signSrc).upper()
        param[Constants.SIGN] = sign
        json_param = json.dumps(param,sort_keys=True)
        print u"话费查询请求报文:" + json_param
        recharge = requests.post("http://192.168.6.34:10086/telcharges/result.do",data=json_param)
        print u"话费查询应答报文:" + recharge.text
      
    def _getRandomNumAndLetterAF(self,length):
        if len(self.NUMSLETTER_A_F)<length:
            loop_num = round(float(length)/len(self.NUMSLETTER_A_F))
            #raise "sample larger than population"
            s = ''
            i = 0
            while i <loop_num:
                s += "".join(random.sample(self.NUMSLETTER_A_F,len(self.NUMSLETTER_A_F)))
                i += 1
            if not length%len(self.NUMSLETTER_A_F) == 0:
                s +=  "".join(random.sample(self.NUMSLETTER_A_F,length - (loop_num-1)*len(self.NUMSLETTER_A_F)))
            return s
        else:
            return "".join(random.sample(self.NUMSLETTER_A_F,length))
          
    def _getRandomLetterAndNum(self,length):
        if len(self.LETTERNUMS)<length:
            raise "sample larger than population"
        return "".join(random.sample(self.LETTERNUMS,length))
    
    def _getRandomLetter(self,length):
        if len(self.LETTERS)<length:
            raise "sample larger than population"
        return "".join(random.sample(self.LETTERS,length))
    
    def _getRandomNum(self,length):
        if len(self.NUMS)<length:
            raise "sample larger than population"
        return "".join(random.sample(self.NUMS,length))

        
    def _createRSAPublicKey(self,pubKey):
        key = base64.decodestring(pubKey)
        try:
            return rsa.PublicKey.load_pkcs1_openssl_der(key)
        except Exception as e:
            return rsa.PublicKey.load_pkcs1(key, format='DER')
       
    def _createRSAPrivateKey(self,priKey):
        key = base64.decodestring(priKey)
        return rsa.PrivateKey.load_pkcs1(key,format='DER')
    
    def _VerifyMerchant(self,merchantCode):
        MODEL = "获取令牌";        
        pak = {Constants.PROJECT_ID:Config.projectId}
        param = {Constants.MERCHANTCODE:merchantCode}        
        twk = self._getRandomNumAndLetterAF(32)                
        rsaKey = self._createRSAPublicKey(Config.tmk)        
        param[Constants.TWK] = hexlify(rsa.encrypt(unhex(twk), rsaKey))
        pak["param"] = param
        pak_sort = json.dumps(pak,sort_keys=True)
        print "请求报文:%s"%pak_sort
        retStr = requests.post("http://192.168.6.34:10086/verify/verify.do",data=pak_sort)
        print "响应报文:%s"%retStr.text
        dict_results = json.loads(retStr.text)
        code = dict_results[Constants.CODE]
        #获取令牌失败
        if  not "00" == code:
            print "失败 code=%s;msg=%s;"%(code, dict_results[Constants.MSG])
        data = dict_results[Constants.DATA]
        token = data[Constants.TOKEN]
        wk = data[Constants.WK]
        t_des = triple_des(unhex(twk))
        wk = hexlify(t_des.decrypt(unhex(wk.encode('ascii'))))
        tokens = [token, twk, wk.strip()]
        print "返回数据:%s"%str(tokens)
        return tokens
    
    def _payment(self, projectId, merchantCode, merPriKey, outUserId, outOrderId, 
                totalAmount, intoCardNo, intoCardName, intoCardType, bankCode, bankName,k):
        param={
                Constants.MERCHANTCODE:merchantCode,
                Constants.NONCESTR:self._getRandomLetterAndNum(32),
                Constants.OUTUSERID:outUserId,
                Constants.OUTORDERID:outOrderId,
                Constants.TOTALAMOUNT:totalAmount,
                Constants.INTOCARDNO:intoCardNo,
                Constants.INTOCARDNAME:intoCardName,
                Constants.INTOCARDTYPE:intoCardType,
                Constants.BANKCODE:bankCode,
                Constants.BANKNAME:bankName
               }
        #验证签名
        signFields = [Constants.MERCHANTCODE, Constants.NONCESTR, Constants.OUTORDERID,
        Constants.TOTALAMOUNT, Constants.INTOCARDNO, Constants.INTOCARDNAME, Constants.INTOCARDTYPE,
        Constants.BANKCODE, Constants.BANKNAME, Constants.OUTUSERID]
        #签名
        signFields.sort()
        signSrc = self._orgSignSrc(signFields, param)   
        #load java生成的 prikey失败，貌似是因为pyasn1 库有bug      
        priKey = self._createRSAPrivateKey(merPriKey)      
        param[Constants.SIGN] = hexlify(rsa.sign(signSrc,priKey,'MD5'))
        print "验证商户签名:%s"%str(rsa.verify(signSrc,unhex(param[Constants.SIGN]),self._createRSAPublicKey(Config.merPubKey)))
        print "商户 订单号 " + outOrderId
        src_json = json.dumps(param,sort_keys=True)
        print len(src_json)
        print  "3des加密数据：%s"%src_json
        #k[1]是16进制字串，需要转化为byte传入才能正确处理，python里3des key长度为16或24,接口服务不是按照python默认的解密来解析，这里需要手动增加长度
        #t_des = triple_des(unhex(k[1]),pad='0')#pad='0',padmode=PAD_PKCS5
        t_des = triple_des(unhex(k[1]))
        #转换成二进制数据的16进制表示再调用接口post传入
        src_byte = hexlify(src_json)
        if len(src_byte)%16 != 0:
            pad_len = 16 - len(src_byte)%16
            print "byte_len:%s"%str(len(src_byte))
            print "pad_len:%s"%str(pad_len)
            src_byte=src_byte+pad_len/2*hexlify('\x00')
            print len(src_byte)
            src_json=unhex(src_byte) 
        print len(src_byte)
        packChiper = hexlify(t_des.encrypt(src_json)) 
        #print "3des加密后密文%s"%packChiper
        print "3des解密数据：%s"%t_des.decrypt(t_des.encrypt(src_json)) 
        reqPak = {Constants.PROJECT_ID:projectId, 'param':json.dumps({Constants.TOKEN:k[0], Constants.MERCHANTCODE:merchantCode,Constants.PACKCHIPER:packChiper},sort_keys=True)}
        reqPak_sort = json.dumps(reqPak,sort_keys=True)
        print "出款 请求报文:" + reqPak_sort
        chukuan_ret = requests.post("http://192.168.6.34:10086/payment/payment.do",data=reqPak_sort)
        print "出款 应答报文:" + chukuan_ret.text        
    
    def payment_Chukuan(self,merchantCode=Config.merchantCode_Chukuan):
        k = self._VerifyMerchant(merchantCode);
        intoCardName = Config.holder
        intoCardNo = Config.payCarNo
        bankCode = "102100099996"
        bankName = u"中国工商银行股份有限公司四川省成都石油路支行"
        intoCardType = "1" # 1-对公 2-对私
        self._payment(Config.projectId, merchantCode, Config.merPriKey, "",
                      self._getRandomLetterAndNum(32), 100l, intoCardNo, intoCardName, intoCardType, bankCode,bankName, k)

if __name__=="__main__":   
    rt=RequestsTest()
    rt.phoneRecharge(merchantcode="1000000431",phone="13008127082",amount=3000l)
    rt.phoneQuery()
    #rt.payment_Chukuan()
        
        