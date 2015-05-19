# -*- coding: utf-8 -*-
class Config:
    # 测试商户号 
    merchantCode_Telrecharge = "1000000431"
    merchantCode_Chukuan = "1000000439"
    outUserId = "0123456789"
    # 测试projectId 
    projectId = "test"
    tmk = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDcBUsvOOllqwsDBhD8iTcSUFlXciduSD7aWrXNyXnpo24D8gbvKlyqdL/GtFd9N3277UkOdM1miEWMHPFCRunp8dwz2ykrrBAp/slWC5rgmV3WWA1vdlVgH9YLG5dlXm/PSvOatDrw6U+2qswC2V+iP/bLK64xtAWRwZRSw0ztHwIDAQAB"
    tmkPri = "MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBANwFSy846WWrCwMGEPyJNxJQWVdyJ25IPtpatc3JeemjbgPyBu8qXKp0v8a0V303fbvtSQ50zWaIRYwc8UJG6enx3DPbKSusECn+yVYLmuCZXdZYDW92VWAf1gsbl2Veb89K85q0OvDpT7aqzALZX6I/9ssrrjG0BZHBlFLDTO0fAgMBAAECgYB66Q4mNDHWVOXS65mjqfe06GPwgNncNsm963yymEHdrimwVI1hIBYiNxRHKcnSLqSzzgvI4qE4DRpk+mogb0MOH29Hcawq8dtLmyC8tAihgvkxuPOQHVLTgrxADEdYnwtNeE4T6ts9B5o57hlWp1J4WkrzycwtSETl0vkl1K7BUQJBAPZ8LxTJ3PEBGkMsXHCCsGTBopjU9ev6zEkXerwLZNWYRQqX7Tp/0HAr3k+QjYLrkk0OK28LKxdat+nX0r3aBkcCQQDkg5VAvhtNGeO2aI3OGhm05TnrleoJF5PAQiYrHzGKsgsDSEk7gROSwi2XhObQNGtgaHdQutWiRF6C1Zqy19ZpAkB14ZhmudAX1u4neBzRlj8kQNMxgpAGhtCSmE8TheN4n7VNRrGnC5+1NdXBeaGkHmO+xGsTVWULa1CP3q8kKxRbAkBjo3xQ3pPI6qD/yFcMpxTOa6T1tEh37m/eRPmfk9pmP3vN0pcb+wwt0b1PdAOwhSrMvsBH0y+TsXwEUF9D3BkBAkEAiFHhQWya2bqGzA3/XL55PeRAUzdcQyojh54xQRPKulmH3uM+JJRtPzmUxJ+xk2MA5Td8CZ1wcY0z2sksNXJ7hg=="
    # 测试 支付银行卡卡号  
    payCarNo = "4402226009100013301"
    phone = "13658009431"
    holder = u"成都中联信通科技股份有限公司"
    track2 = "6226222004085895=49125200012645200000"
    pin = "305125"
    idNo = ""
    expire = ""
    cvn2 = ""
    
    # 商户提供 1000000001
    # base64
    # 公钥:MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDjiAb2jxUIUNzKZfDHTmYww2owAwlsRFz/5V0qJ1eVNOANNVxjTbOcggcTCW4yktZJipkJgoZAH5mnTZaSplbXO6rHWativdBINP/U+HI5/3HSg3P80dGzMJ9jXX1XuWN7sVgd3kai0xNU0wF88y5z5tS7NLi3RYez3z58ago+gwIDAQAB
    # base64 私钥:
    # 模拟商户私钥
    #这对密钥：私钥用python无法解析，尝试用python生成密钥对来测试
    #merPriKey = "MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAOOIBvaPFQhQ3Mpl8MdOZjDDajADCWxEXP/lXSonV5U04A01XGNNs5yCBxMJbjKS1kmKmQmChkAfmadNlpKmVtc7qsdZq2K90Eg0/9T4cjn/cdKDc/zR0bMwn2NdfVe5Y3uxWB3eRqLTE1TTAXzzLnPm1Ls0uLdFh7PfPnxqCj6DAgMBAAECgYAfDwh0S5/BXNhmwHeXnToR2fr6xs9YehR/0d1fzbME6QzUgL41x/uGl7FDhfwG50hdDZBKXgjZY/bjgZHWPuKHiO390C659Ioy3FmRAk++eoFdTGU46SsBQrMDwqu1AEcxHj0GrP3wSZ7PNOTY6eZb4v/XtlhdRwRcrIyAguKoUQJBAPmtsGOYEHPdCLj5AjbpecUyXWqNn2USwXly4HDe4b8+HLjbqfeeBGAQVuaL14k3LlIVCI7jBJaxqDkfvlyUSW0CQQDpSso1L+8DCPTH2OJToGwla3mC0mklb9ZAo0//Hsj24NLwhtfFVPdJULCN2mFmjYM9E6Mh6YLavlw0tZOL6SGvAkAm8mgUcREH8c+9guJMjIj5MM0PpP3bN1zExB2snafbPCYg0+skfBq0nXfgyKmbducb2LoYB+OcWiQinQgFyv/VAkBs8Ov0YmnutOP53yHxg1x9LO8VVESdotgeXyUgMbQO9XYLtCxWjhLcPb30wCHzzemXP/BSCcV9eJ9+TbyU/U0pAkEA4DShPeSvije4tiQIJ+R/4sn3S/euYehCLzatMRdYfCC+wV/TPUTR/2ZtLJt5XC5AqwKll8aASn0tjPhiwIwA4Q=="
    #python生成的密钥对，同时需要上传商户服务平台上的商户公钥
    merPriKey = "MIICXwIBAAKBgQCQrDIAu3lg7OJfZ2kAsmH4vzbVHThVvmFluElOTNNNpDICJTkPBOxw5m0quc/lYKfd8ILC7IcrcAYtXl/LIXTUBkmT+tyUWEh87J6SlLO+ghs8grxTac5mE1fQYTWzEt3XNkZZFFZ8YmS8E+3GkrVaCbZAXH/k1MMZ6P0hWuy9swIDAQABAoGAF29NSkEUEFdO9BVUNQCwThLrVuo8zebg8BFCDqTzNYh7cU2GSKCLjF5HILyoqIdXqePjyp915dtnpMG8tWovhDiOk94FJsEAGhKyZN1la4Za3gvUcl1JI98WkuIMmmYhqE+ekYSTY8t7aATgK8JbADZOuLU7uocvK519pjXlNAECRQC0x3A8lV0mGLXjZ5nL+kunrLD+QXUTdssmvL9NVyb93kqPSsEE9TPsoL3D7PoQF0ER/f+v6zvdY25Z+zDxVQzjKO4mwQI9AMzetLaG0sVT25vnhDVkHEelA5gKEWaZM0Gm5hwWUqeFQw5j/Q5fldh7aq8LH9qs9RpsGx8c4/fezyOVcwJEPdD81hqVEZPdjnc8pf1epWVt2GN1r0Qtz383QzEMCj9a64i6XAGk0cNdYIPGNn5dJ9Pc/MDJZbi8YVR9tehJUdwLI4ECPDlMyMqMZwMd8zxlwoqUV3yKYLjzh+5kRvvDzHRqoe+MzDaILM0KWwTTcAFJYT1uRpd/SQ6oq/I19UWElQJEDe4PcwCyDmag/+9t4oafYzU3q1jHd2RXK4B43EawyXEkXXFD1FQPU2VQhT8VQo+aUjapVNPYFwG8IxLwK6yrGaZ0gU0="
    merPubKey = "MIGJAoGBAJCsMgC7eWDs4l9naQCyYfi/NtUdOFW+YWW4SU5M002kMgIlOQ8E7HDmbSq5z+Vgp93wgsLshytwBi1eX8shdNQGSZP63JRYSHzsnpKUs76CGzyCvFNpzmYTV9BhNbMS3dc2RlkUVnxiZLwT7caStVoJtkBcf+TUwxno/SFa7L2zAgMBAAE="
    
    platPubKey = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCjIKKiaz+uXtn08z8Ky4kwCtVxo0nVQTo1sZRgloBliN2CBxFmzKfLTFf4CyeHLHtYNfaZwKNUhVC+Ya/6pTJpGJL24+LuXxxPoV4Hs0frF29ZACMkV2T23kJJ+0KjwptP1Kfiq4CYRbbpFikeCCR1r8LyVhnBZbbU1lALBdm2fQIDAQAB"
    # 平台方提供的公私钥
    # base64 公钥:MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCjIKKiaz+uXtn08z8Ky4kwCtVxo0nVQTo1sZRgloBliN2CBxFmzKfLTFf4CyeHLHtYNfaZwKNUhVC+Ya/6pTJpGJL24+LuXxxPoV4Hs0frF29ZACMkV2T23kJJ+0KjwptP1Kfiq4CYRbbpFikeCCR1r8LyVhnBZbbU1lALBdm2fQIDAQAB
    # base64 私钥:MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAKMgoqJrP65e2fTzPwrLiTAK1XGjSdVBOjWxlGCWgGWI3YIHEWbMp8tMV/gLJ4cse1g19pnAo1SFUL5hr/qlMmkYkvbj4u5fHE+hXgezR+sXb1kAIyRXZPbeQkn7QqPCm0/Up+KrgJhFtukWKR4IJHWvwvJWGcFlttTWUAsF2bZ9AgMBAAECgYAn/LsBN2sP0l55RhthCQ2jAjTaO13A8dFUEii+GIZ23Tr3QcZJPcev9RHnUsyovQWrVOcTP36KHHfzgzzBIzec2QKaGpmZg9y1tDCNcix/VeQ49ZdlqpBT+SwyUwCiiX2ZYLj4rXyzo36i3qhzmihX/ks6O5KBtOBXid6Zo91KvQJBAN7HWbBouf77yQ80HvxoRfik3lEOiQ5YpkQw5n/kwG0oPzWKCUko9axpjjTtxrz3QSH7cLZuPznRQmHTYdkpPbMCQQC7dBRxAhUuzcfgES7t8mBy87zuBOPrPL/eqqFOu5QqV6iLEIFFUXNEmhPV8cus1CgZJUbnzA9N0nmbzArNcgMPAkBDZqToDodXce4ev3Iwg4vH8nmgpHkq8f872l+iih7955NYK28rx0ys4TK5KMdcHKKEGYK8bxaJ85nV5xJPlX6pAkAYNZWuQqaZtNnrhkyZToRGVFRCKT+GUgI1r7PFh1RLY6bQzwDjAvHwGjYVm3TCjWPgW4Acz63qTxSFmoSKo/7hAkEAoEd/ikjlJ2HQskv/MW/VvkVbyj3#oOfK0HelhBsCI8HEq2PNUrs8soUhFT4LOEKxU815W4dx8CBb28dsXN3HA==
    # 加密机识别私钥:7A34B1DECED695358726F73F12E35F0125DA14F4A02D522617024D1A8F51BBD662FC5F6155ABA7B4D417F464BAE476E141F99C9379CA6B0844641C86A95D25A86F3CDEEFF43CE5F679EAA50EF8B88521B70A16D724FDD3E0EA9809A984CFEA3324E5C5F02A618A859602043BAC97297DADEB12C6C3A714F97F3886A0A032F3C5CB727F993AF95852A99DD05276ED10B6E708A3E580D6DE524CDC07DE3A50600F6B8A7244D3F1EF3F4AAF779B3B90FED22CE00CB4033DECCE9B1A5B070FBFD1697DE58CAFBC1EC41815C76FDDBD871B92D512B4F69186F6DEEEFC07A6EC2D7284BCCB34EF1B11B6993C37AA9A78AFA24BF1BA0CA8F8AD0CE9DFF6F8AB8C74A58AB2ACB9C965E48FDF0A22ACA27BFCA4B494CFEE0C7EF082E4C79104161039C91E5A8DFF05B95AB3C329595B3BA8F16CD315729ADBE6E5F75EBD66B10B48F7BE62A8C7C0379B848B4DC0A37DC17473926A57DEB7FDA65829D0AD5B050D04DEBE8614BF9A7E1CAA053B0F155724923B346C58562F1000BDBCEAACE79FE6BD39E3DBFA74261EF34C86CA578D7F185D7FF6B9802E3AD5119F7BB61F35A4A8D6E26B163391D0B52448B55DA3043280D2CBD4D984E0E1B6F5BB17B42EE7E743244AE1B52D940D37321340FFCF57E6D2226DB84AE07E51899B5089DD6E8598052E40EBEE31CF7B92859CC32968AC9F0358AFA62202D7F9BF900A225343F57D6919677CF50024FE8B951B670CED9924C1DFDC24A993CCB1B2453DA15CC6196373796CB86E51362D7060F44B96A0D6AF4C766CDB095D4EB9F0D94867F023C4A9C4C6FBBC82945B07188FE3F9279B4C4CD9F955E452223E29CD78FD9997F5C2AAD905B0106495F8A5E5DD31D900
    # 模拟商户支付通知地址 
    payNotifyUrl = "http:#127.0.0.1:8080/payment-pre-interface/testNoticeRecv/recv.do"
    # sn序列号 
#     sn = "E611201300210848"
#    # 出厂密钥 
#     dfk = "C559754CB200280275DA49C711067168"
#    # 工作密钥 
#     dwk = "CCB90F85794CC92694C7C345111C9029"
    
    snM = "1008600000000001"
    dfkMLmk = "F8944E67A86060AEF8944E67A86060AE" # 加密机识别的
    dwkMLmk = "B2CBA73B6E79F88045C9655BBCEE1903" # 加密机识别的
    dfkM = "11111111111111111111111111111111" # 明文
    dwkM = "7A047031E9F8E0F1C2F215FDA1E0A4FD" # 明文