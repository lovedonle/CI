'''
Created on 2015.2.25

@author: cfds
'''
import unittest

class Dictionary(unittest.TestCase):

    def setUp(self):
        print "setUp..."


    def tearDown(self):
        print "tearDown..."


    def testName(self):
        print "Run Dictionary management..."

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()