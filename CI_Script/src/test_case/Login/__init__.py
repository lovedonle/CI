import unittest
from Login import Login

__all__=["suite"]

def suite():
    '''
    suite = unittest.TestSuite()
    suite.addTest(Login("test_login"))
    return suite
    '''
    return unittest.makeSuite(Login,"test")
    
if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run()#suite())
    #unittest.main(defaultTest="suite")
