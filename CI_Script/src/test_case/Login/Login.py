# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, sys, os

sys.path.append(os.sep.join(os.path.abspath(".").split(os.sep)[:-1]))
import WebpayCommon

class Login(unittest.TestCase):
    
    def setUp(self):
        u"""加载firefox配置文件，否则会启动一个和最初安装一样的firefox，不带后续安装的插件以及证书等"""
        base_url = "https://payment-boss.kklpay.com:7777/"
        self.driver = WebpayCommon.open_configured_browser(base_url,"firefox")
        self.verificationErrors = []
        self.accept_next_alert = True
        
    def test_login(self):
        u"""BOSS后台系统管理登录测试"""
        driver = WebpayCommon.login_boss(self.driver)
        print driver.title        
        driver.set_window_size(800, 800)
        time.sleep(3)
        driver.maximize_window()
        #print driver.get_window_size()
        time.sleep(3)
        '''获取隐藏元素的的text value'''
        script = "return document.getElementById(\"/operateLog\").innerHTML"
        print driver.execute_script(script)        
        print "Open operatelog................."
        #menu=driver.find_element_by_xpath(r"//div[@id='navbar']/ul[1]/li[1]/a")
        menu=driver.find_element_by_link_text(u"安全管理")
        hide_submenu=driver.find_element_by_id(r"/operateLog")
        #hide_submenu=driver.find_element_by_link_text(u"操作日志")  #仅仅只用link text还无法准确定位到该元素
        #print "弹出安全管理菜单之前: %s"%driver.find_element_by_id(r"/operateLog").text
        webdriver.ActionChains(driver).move_to_element(menu).click(hide_submenu).perform()
        print u"弹出安全管理菜单之后: %s"%driver.find_element_by_id(r"/operateLog").text
        time.sleep(3)
#        action=webdriver.ActionChains(driver)
#        action.move_to_element(menu)
#        action.click(hide_submenu)
#        action.perform()
        print "OperateLog opened.........."
        time.sleep(3)
        driver.switch_to_frame("contentFrame")
        driver.find_element_by_id("opModule").clear()
        driver.find_element_by_id("opModule").send_keys(u"用户登录")
        driver.find_element_by_xpath(r"//input[@id='search']").click()
        driver.switch_to.parent_frame()
        print "Open datadict................."
        #menu=driver.find_element_by_xpath(r"//div[@id='navbar']/ul[1]/li[1]/a")
        menu=driver.find_element_by_link_text(u"安全管理")
        hide_submenu=driver.find_element_by_id(r"/datadict")
        #hide_submenu=driver.find_element_by_partial_link_text(u"数据字典")
        webdriver.ActionChains(driver).move_to_element(menu).click(hide_submenu).perform()
        print "Datadict opened.........."
        time.sleep(3)
        driver.switch_to_frame("contentFrame")
        driver.find_element_by_id("name").clear()
        driver.find_element_by_id("name").send_keys("sex")
        driver.find_element_by_xpath("//input[@id=\"search\"]").click()
        driver.switch_to.parent_frame()
        print "Open merchant................."
        #menu=driver.find_element_by_xpath(r"//div[@id='navbar']/ul[1]/li[2]/a")
        menu=driver.find_element_by_link_text(u"客户管理")
        hide_submenu=driver.find_element_by_id(r"/merchant")
        #hide_submenu=driver.find_element_by_link_text(u"商户管理")
        webdriver.ActionChains(driver).move_to_element(menu).click(hide_submenu).perform()
        print "Merchant opened.........."
        time.sleep(3)
        driver.switch_to_frame("contentFrame")
        driver.find_element_by_xpath("//input[@id=\"new\"]").click()
        driver.switch_to.parent_frame()
        # This is a comments, switch browser tab
        first_window=driver.current_window_handle
        all_windows=driver.window_handles
        #print first_window
        #print all_windows
        driver.switch_to_window(all_windows[1])
        time.sleep(5)        
        driver.close()
        driver.switch_to.window(first_window)
        print u"退出BOSS系统"
        driver.find_element_by_link_text(u"退出").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        u"""退出浏览器，关闭驱动"""
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    #unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(Login("test_login"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
