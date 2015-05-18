import unittest
from GeneralRoute import GeneralRoute
from MerchantRoute import MerchantRoute

__all__=["suite"]

def suite():
    suite = unittest.TestSuite()
    suite.addTest(GeneralRoute("testName"))
    suite.addTest(MerchantRoute("testName"))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run()#suite())
    #unittest.main(defaultTest="suite")