# -*- coding: utf-8 -*-
import unittest


class OperateLog(unittest.TestCase):


    def setUp(self):
        print "setUp..."

    def tearDown(self):
        print "tearDown..."

    def testName(self):
        u"""执行操作日志管理"""
        print "Run Operate log management..."
    def testOpen(self):
        u"""打开操作日志管理"""
        print "Open operate log management..."
    def testOpened(self):
        u"""操作日志管理打开成功"""
        print "Operate log opened..."
    def testClose(self):
        u"""关闭操作日志管理"""
        print "Close operate log..."


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()