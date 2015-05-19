import unittest
from OperateLog import OperateLog
from Dictionary import Dictionary

__all__=["suite"]

def suite():
    suite = unittest.TestSuite()
    suite.addTest(Dictionary("testName"))
    suite.addTest(OperateLog("testName"))
    suite.addTest(OperateLog("testOpen"))
    suite.addTest(OperateLog("testOpened"))
    suite.addTest(OperateLog("testClose"))
    return suite
    #return unittest.makeSuite(Dictionary, "test")
    
if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run()#suite())
    #unittest.main(defaultTest="suite")