# -*- coding: utf-8 -*-
import unittest
from MerchantMgt import MerchantMgt
__all__=["suite"]

def suite():
    '''
    suite = unittest.TestSuite()
    suite.addTest(MerchantMgt("test_query"))
    suite.addTest(MerchantMgt("test_reset"))
    suite.addTest(MerchantMgt("test_newmerchant"))
    return suite
    '''
    return unittest.makeSuite(MerchantMgt, "test")
    
if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run()#suite())