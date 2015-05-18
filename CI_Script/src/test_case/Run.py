'''
Created on 2015.2.25

@author: cfds
'''
import unittest
import CustomerMgt, Login, SecurityMgt, RouteMgt 
from WebpayCommon.HTMLTestRunner import HTMLTestRunner as htr

CutomerMgt_suite = CustomerMgt.suite()
Login_suite = Login.suite()
RouteMgt_suite = RouteMgt.suite()
SecurityMgt_suite = SecurityMgt.suite()

alltests = unittest.TestSuite((CutomerMgt_suite,Login_suite,RouteMgt_suite,SecurityMgt_suite))
#output the results to console
runner = unittest.TextTestRunner()
runner.run(alltests)

#output the results to a report file
#filename = r'test_result/result1.html'
#fp = file(filename, 'wb')
#runner =htr(stream=fp,title='BOSS testing result',description='BOSS automation test report')
#runner.run(alltests)

