# -*- coding: utf-8 -*-
#author:Dong Jie
#mail:dongjie789@sina.com
#!/bin/bash
import re,os,sys,shutil,time,stat
from Jenkins import SysUtil
class deploy(object):
    '''
    this case is about deploy maven project, configure and restart service
    #传入参数 source_folder deploy_scope['all'|'payment-ac'|'payment-ac-api'] 
    #如果传入参数是all循环执行每个工程，如果是单个则执行一遍则完成
    {
    #备份所有即将被覆盖的文件，备份在指定目录下，并以job传入的时间戳为文件夹名称的一部分；
    #当新部署的包不能正常工作时可以再替换回来；
    #替换文件为新文件；
    #重启：根据所部署的模块名字，ps -ef|grep 模块名 得到进程号，使用kill -9关闭其进程，然后重启；
    #修改配置,war工程在重启后-->修改配置-->重启，服务直接修改配置后再重启；
    }
    #检查所有服务、web工程、以及其他必须的监控服务都正常启动，dubbo monitor，zookeper，等等
    #如果不是都启动则重启动，再次检测，仍未启动则报错
    '''
    def __init__(self,source_folder,deploy_scope):
        '''
        initialize the parameters
        '''
        self.source_folder = source_folder
        self.deploy_scope = deploy_scope
        self.backup = source_folder+os.sep+'backup'
        SysUtil.createfolder(self.source_folder,'backup')        
        self.web_items = {"boss":"payment-boss-web","merchant":"payment-merchant-web","pre":"payment-pre-interface"}
        self.svc_items = {"ac":"payment-ac","account":"payment-account","ams":"payment-ams",
                    "channel":"payment-channel","cm":"payment-cm","cms":"payment-cms",
                    "fastdfs":"payment-fastdfs","mas":"payment-mas","pe":"payment-pe",
                    "pss":"payment-pss","rcs":"payment-rcs","route":"payment-route",
                    "security":"payment-security","settle":"payment-settle","tasks":"payment-tasks"}
        self.__gen_dirctory()

    def __gen_dirctory(self):
        '''
        define the head and tail name of the deploy path and run path.
        generate deploy and run directory of web and service
        '''
        web_deploy = {"head":"/data/run/","tail":""}
        svc_deploy = {"head":"/data/program/payment/","tail":"/deploy"}
        web_run = {"head":"/data/program/tomcat/","tail":"/node/bin"}
        svc_run = {"head":"/data/program/payment/","tail":"/bin"}
        self.source_items = dict()
        self.backup_items = dict()
        self.web_deploy_items=dict()
        self.svc_deploy_items=dict()
        self.web_run_items=dict()
        self.svc_run_items=dict()
        for key in self.web_items.keys():
            self.source_items[key]=self.source_folder+os.sep+self.web_items[key]
            self.backup_items[key]=self.source_folder+os.sep+"backup"+os.sep+self.web_items[key]
            self.web_deploy_items[key]=web_deploy['head']+self.web_items[key]+web_deploy['tail']
            self.web_run_items[key]=web_run['head']+self.web_items[key]+web_run['tail']
        for key in self.svc_items.keys():
            self.source_items[key]=self.source_folder+os.sep+self.svc_items[key]
            self.backup_items[key]=self.source_folder+os.sep+"backup"+os.sep+self.svc_items[key]     
            self.svc_deploy_items[key]=svc_deploy['head']+self.svc_items[key]+svc_deploy['tail']
            self.svc_run_items[key]=svc_run['head']+self.svc_items[key]+svc_run['tail']
        print self.source_items
        print self.backup_items
        print self.web_deploy_items
        print self.svc_deploy_items
        print self.web_run_items
        print self.svc_run_items
        
    def deploy_specified(self,sub_sc):
        #Service
        #todo  del and copy every jar file，根据源目录，来处理目标部署目录，目标部署目录不存在报错
        if sub_sc in self.svc_items.keys():
            svc_deploy_folder = self.svc_deploy_items[sub_sc]
            print "Target deploy folder is %s"%svc_deploy_folder
            svc_run_folder = self.svc_run_items[sub_sc]
            print "Target cmd folder is %s"%svc_run_folder
            source_sub_folder = self.source_items[sub_sc]
            backup_sub_folder = self.backup_items[sub_sc]
            if os.path.exists(source_sub_folder):
                source_file = os.listdir(source_sub_folder)
                if len(source_file) == 0:
                    print "No service file under %s"%source_sub_folder
                if (os.path.exists(svc_deploy_folder)):
                    '''bckup action will remove the folder'''
                    #time_prefix = time.strftime('%Y-%m-%d_%H-%M-%S')
                    if not os.path.exists(backup_sub_folder):
                        print "The backup folder not exists, copy the files in target folder to backup folder..."
                        shutil.move(svc_deploy_folder, backup_sub_folder)
                    else:
                        print "File already exist, no need to move again, but only clean the target folder"
                        shutil.rmtree(svc_deploy_folder)
                    '''Copy jar folder to target path'''
                    shutil.copytree(source_sub_folder,svc_deploy_folder)
                    endprocess(sub_sc)
                    restart_command = svc_run_folder + "restart.sh"
                    os.chmod(restart_command,stat.S_IRWXU+stat.S_IRWXG+stat.S_IRWXO)
                    os.popen("sh " + restart_command)
                else:
                    "Deploy folder %s not exist!"%svc_deploy_folder
            else:
                print "The source folder: %s not exist!"%source_sub_folder    
        #Web application
        #todo,根据源目录，来处理目标部署目录，目标部署目录不存在报错
        elif sub_sc in self.web_items.keys():
            web_deploy_folder = self.web_deploy_items[sub_sc]
            print "Target deploy folder is %s"%web_deploy_folder
            web_run_folder = self.web_run_items[sub_sc]
            print "Target cmd folder is %s"%web_run_folder
            source_sub_folder = self.source_items[sub_sc]
            backup_sub_folder = self.backup_items[sub_sc]
            if os.path.exists(source_sub_folder):
                source_file = os.listdir(source_sub_folder)
                if len(source_file) != 1:
                    print "No web file or more than one file under %s"%source_sub_folder
                else:
                    temp = source_file.split('.war')[0]
                    if (os.path.exists(web_deploy_folder)):
                        '''backup action will remove the folder'''
                        shutil.rmtree(web_deploy_folder + temp)
                        if not os.path.exists(backup_sub_folder):
                            print "The backup folder not exists, copy the files in target folder to backup folder..."
                            shutil.move(web_deploy_folder+os.sep+source_file,backup_sub_folder)
                        else:
                            print "File already exist, no need to move again, only clean the target folder"
                            shutil.rmtree(web_deploy_folder+os.sep+source_file)
                        '''Copy war file to target path'''
                        shutil.copy(source_sub_folder + os.sep + source_file,web_deploy_folder)
                        endprocess(sub_sc)
                        restart_command = web_run_folder + "startup.sh"
                        os.chmod(restart_command,stat.S_IRWXU+stat.S_IRWXG+stat.S_IRWXO)
                        os.popen("sh " + restart_command)
                    else:
                        "Deploy folder %s not exist!"%web_deploy_folder
    
            else:
                print "The source folder: %s not exist!"%source_sub_folder
        else:
            print "There's no such service or web application: %s"%sub_sc

    def endprocess(self,sub_sc):
        if sub_sc in self.svc_items.keys():
            sub_sc = self.svc_items[sub_sc]
        elif sub_sc in self.web_items.keys():
            sub_sc = self.web_items[sub_sc]
        else:
            print "Please check whether the %s exist..."%sub_sc
        print sub_sc
        process_number=os.popen("ps -ef|grep " + sub_sc + "/|grep -v grep|awk '{print $2}'").read()
        process_number.strip()
        print process_number
        if process_number.isalnum():
            print "Kill the process %s of %s"%(process_number,sub_sc)
            os.popen("kill -9 "+ process_number)
        else:
            print "No process for %s"%sub_sc
                
    def recover(self):
        pass
    
    def restart(self):
        pass
    
    def check(self):
        pass
    
def run():
    pass

def test_run():
    dep = deploy(r"C:\log",'all')
    #dep = deploy(r"/root/Webpay-package-files/0.3.4/2015-01-09_18-10-00",'all')
if __name__ == "__main__":
    test_run()