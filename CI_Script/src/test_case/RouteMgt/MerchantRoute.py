'''
Created on 2015.2.25

@author: cfds
'''
import unittest


class MerchantRoute(unittest.TestCase):


    def setUp(self):
        print "setUp..."


    def tearDown(self):
        print "tearDown..."


    def testName(self):
        print "Run Merchant route..."

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()