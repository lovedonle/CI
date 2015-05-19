# -*- coding: utf-8 -*-
# 设置spring mvc数据格式与字符集编码 
class Constants:
    PRODUCES = "application/jsoncharset=UTF-8"
    
    B8 = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 }
    F = "F"
    D = "D"
    A = "A"
    Y = "Y"
    # 日志标记 
    LOG_FLAG = "log_flag"
    
    # 编码 
    ENCODE = "UTF-8"
    
    # packet 
    PACKET = "PACKET"
    
    EQUAL = "="
    
    # 支付卡(转出卡) 
    CARDNO = "cardNo"
    # 转入卡 
    INTOCARDNO = "intoCardNo"
    # 收款账户名称 
    INTOCARDNAME = "intoCardName"
    SN = "sn"
    PINRANDOM = "pinRandom"
    TRACKRANDOM = "trackRandom"
    # 加密参数 
    ZERO = "0"
    DOUBLE_ZERO = "00"
    ONE = "1"
    TWO = "2"
    YES = "YES"
    NO = "NO"
    
    # 商户号 
    MERCHANTCODE = "merchantCode"
    # 商户用户体系的用户Id 
    OUTUSERID = "outUserId"
    PAYERID = "payerId"
    NONCESTR = "nonceStr"
    
    # 订单创建时间 
    ORDERCREATETIME = "orderCreateTime"
    # 最后支付时间 
    LASTPAYTIME = "lastPayTime"
    TOTALAMOUNT = "totalAmount"
    CURRENCY = "currency"
    GOODSNAME = "goodsName"
    GOODSEXPLAIN = "goodsExplain"
    # pos支付 
    TOKEN = "token"
    PACKCHIPER = "packChiper"
    CONTROLTYPE = "controlType"
    TRANSTYPE = "transType"
    INSTRUCTCODE = "instructCode"
    TRANSTIME = "transTime"
    # 卡类型 
    CARDTYPE = "cardType"
    PRODUCTCODE = "productCode"
    PAYCHANNEL = "payChannel"
    PINCHIPER = "pinChiper"
    TRACKINFO = "trackInfo"
    ICDATA = "icData"
    AMOUNT = "amount"
    FEE = "fee"
    
    OUTORDERID = "outOrderId"
    PAYCARDNO = "payCardNo"
    
    # 验证商户 
    SIGN_SRC = "sign_src"
    SIGN = "sign"
    PAYKEY = "payKey"
    TWK = "twk"
    WK = "wk"
    MERCHANTNAME = "merchantName"
    
    PAYNOTIFYURL = "payNotifyUrl"
    PIN = "pin"
    TRACK1 = "track1"
    TRACK2 = "track2"
    TRACK3 = "track3"
    ICNUMBER = "icNumber"
    EXPIRE = "expire"
    DCDATA = "dcData"
    
    # 错误码定义 
    CODE = "code"
    MSG = "msg"
    DATA = "data"
    # 令牌失效时间 
    TOKEN_BOLISH = "TOKEN_BOLISH"
    # 系统错误提示配置 
    SYSERROR = "SYSERROR"
    # 令牌对象KEY 
    TOKEN_OBJ = "TOKEN_OBJ"
    # 产品对象 
    PRODUCT_OBJ = "PRODUCT_OBJ"
    RETURNINSTRUCTCODE = "returnInstructCode"
    RETURNTRANSTIME = "returnTransTime"
    ORIINSTRUCTCODE = "oriInstructCode"
    REPLYCODE = "replyCode"
    # 卡号输入方式 
    CARDNOINPUTTYPE = "cardNoInputType"
    # 证件类型 
    IDTYPE = "idType"
    # 证件号 
    IDNO = "idNo"
    # 持卡人姓名 
    HOLDER = "holder"
    # 电话号码 
    PHONE = "phone"
    # 成员类型 
    MEMBERTYPE = "memberType"
    # 成员ID 
    MEMBERID = "memberId"
    # 合同编号 
    CONTRACTNO = "contractNo"
    # 备注 
    REMARK = "remark"
    # 页码 
    PAGENO = "pageNo"
    # 每页记录数 
    PAGESIZE = "pageSize"
    TEN = 10
    NUM_1 = 1
    NUM_0 = 0
    # 列表 
    LIST = "list"
    # 总记录数 
    TOTALSIZE = "totalSize"
    # cvn2数据 
    CVN2 = "cvn2"
    # 发卡机构名 
    ISSUERNAME = "issuerName"
    # 代扣类型01-普通,02-实名 
    WITHHOLDTYPE = "withholdType"
    # 订单ID 
    ORDERID = "orderId"
    # 转账 
    RESULT = "result"
    # 状态 
    STATE = "state"
    # 状态-中文 
    STATEDESP = "stateDesp"
    # 姓名 
    NAME = "name"
    # 加密模式1-非设备,2-设备 
    DECRYPTMODEL = "decryptModel"
    # 银行代码 
    BANKCODE = "bankCode"
    # 转入银行卡名称 
    BANKNAME = "bankName"
    # 开始日期 
    STARTDATE = "startDate"
    # 结束日期 
    ENDDATE = "endDate"
    # 转入卡银行名称 
    INTOBANKNAME = "intoBankName"
    # 转账完成时间 
    FINISHTIME = "finishTime"
    # 转入卡类型 
    INTOCARDTYPE = "intoCardType"
    # 卡类型-中文 
    CARDTYPECN = "cardTypeCN"
    # 银行LOGO URL 
    BANKLOGO = "bankLogo"
    # 元素位图 
    ELEMENTSMAP = "elementsMap"
    # 短信验证码 
    SMSCODE = "smsCode"
    # 是否支持借记卡 
    ISSUPPORTDEBIT = "isSupportDebit"
    # 是否支持贷记卡 
    ISSUPPORTCREDIT = "isSupportCredit"
    # 支付类型 
    PAYTYPE = "payType"
    # 是否绑定支付银行卡 
    ISBIND = "isBind"
    # 设备主密钥 
    DWK = "dwk"
    # 银行卡介质（磁条，ic卡） 
    CARDMEDIUM = "cardMedium"
    # 订单类型 
    ORDERTYPE = "orderType"
    # 原始交易订单号 
    ORIORDERID = "oriOrderId"
    # 订单状态 
    ORDERSTATE = "orderState"
    # 订单状态中文 
    ORDERSTATECN = "orderStateCN"
    # 地址 
    URL = "url"
    # logo地址1 
    LOGOURL1 = "logoUrl1"
    # logo地址2 
    LOGOURL2 = "logoUrl2"
    # 余额 
    BALANCE = "balance"
    # 签名图片目录 配置 
    SIGN_DIR = "SIGN_DIR"
    # 签名图片url 配置 
    SIGN_URL = "SIGN_URL"
    # 是否带有刷卡设备 
    ISDEVICE = "isDevice"
    # 创建时间 
    CREATETIME = "createTime"
    # 脚本 
    SCRIPT = "script"
    # 通知类型 
    NOTICETYPE = "noticeType"
    # 输入模式 
    INPUTMODE = "inputMode"
    # 可用余额 
    AVAILABLEBALANCE = "availableBalance"
    # 冻结余额 
    FROZENBALANCE = "frozenBalance"
    # 昵称 
    NICK = "nick"
    # 密码 
    PASSWORD = "password"
    # 支付渠道（支付编码） 
    TRADEWAY = "tradeWay"
    # 实名认证状态 
    REALNAMEAUTHSTATE = "realNameAuthState"
    # 银行支付地址 
    BANKURL = "bankUrl"
    # 商户取货地址 
    MERURL = "merUrl"
    # 请求参数 
    PARAMS = "params"
    # 自动跳转 
    AUTOJUMP = "autoJump"
    # 跳转等到时间 
    WAITTIME = "waitTime"
    # 通知地址 
    NOTICEURL = "noticeUrl"
    # 是否在商户端选择银行 
    BANKINPUT = "bankInput"
    # 支付银行卡类型 
    BANKCARDTYPE = "bankCardType"
    # 圈存成功时间 
    LOADSUCCTIME = "loadSuccTime"
    # 圈存状态 
    LOADSTATE = "loadState"
    # 圈存银行卡卡号 
    BANKCARDNO = "bankCardNo"
    # 申请人 
    APPLICANT = "applicant"
    SECRET_FIELD = ",icNumber,expire,dcData,track1,track2,track3,pin,trackInfo,icData,"
    # 商户采用MD5签名报文 
    SIGN_KEY_MD5 = "MD5"
    # 商户采用RSA签名报文 
    SIGN_KEY_RSA = "RSA"
    # 充值类型 
    CHARGETYPE = "chargeType"
    # 扣款金额 
    DEDUCT = "deduct"
    # 项目号
    PROJECT_ID = "project_id"