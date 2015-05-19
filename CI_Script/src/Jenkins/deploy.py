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
        self.force_backup = False
        self.backup = os.path.join(source_folder,'backup')
        SysUtil.createfolder(self.source_folder,'backup')        
        self.web_items = {"boss":"payment-boss-web","merchant":"payment-merchant-web","pre":"payment-pre-interface"}
        self.web_item_dst_name = 'ROOT.war'
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
        web_deploy = {"head":"/data/run/app/","tail":""}
#        svc_deploy = {"head":"/data/program/payment/","tail":"/deploy"}
        svc_deploy = {"head":"F:\\test\\deploy\\","tail":"/deploy"}
        web_run = {"head":"/data/program/tomcat/","tail":"/node/bin"}
        svc_run = {"head":"/data/program/payment/","tail":"/bin"}
        self.source_items = dict()
        self.backup_items = dict()
        self.web_deploy_items=dict()
        self.svc_deploy_items=dict()
        self.web_run_items=dict()
        self.svc_run_items=dict()
        for key in self.web_items.keys():
            self.source_items[key]=os.path.join(self.source_folder,self.web_items[key])
            self.backup_items[key]=os.path.join(self.backup,self.web_items[key])
            self.web_deploy_items[key]=web_deploy['head']+self.web_items[key]+web_deploy['tail']
            self.web_run_items[key]=web_run['head']+self.web_items[key]+web_run['tail']
        for key in self.svc_items.keys():
            self.source_items[key]=os.path.join(self.source_folder,self.svc_items[key])
            self.backup_items[key]=os.path.join(self.backup,self.svc_items[key]) 
            self.svc_deploy_items[key]=svc_deploy['head']+self.svc_items[key]+svc_deploy['tail']
            self.svc_run_items[key]=svc_run['head']+self.svc_items[key]+svc_run['tail']
        print self.source_items
        print self.backup_items
        print self.web_deploy_items
        print self.svc_deploy_items
        print self.web_run_items
        print self.svc_run_items
    

    def __deploy_svc(self,sub_sc):
        '''deploy service'''
        source_sub_folder = self.source_items[sub_sc]
        backup_sub_folder = self.backup_items[sub_sc]
        svc_deploy_folder = self.svc_deploy_items[sub_sc]
        print "Target deploy folder is %s"%svc_deploy_folder
        if os.path.exists(source_sub_folder):
            source_files = os.listdir(source_sub_folder)
            if len(source_files) != 0:
                if (os.path.exists(svc_deploy_folder)):
                    print '''Start backup action'''
                    #time_prefix = time.strftime('%Y-%m-%d_%H-%M-%S')
                    if not os.path.exists(backup_sub_folder):
                        shutil.copytree(svc_deploy_folder, backup_sub_folder)
                        print "Copy %s to %s"%(svc_deploy_folder,backup_sub_folder)
                    else:
                        if not self.force_backup:
                            print '''Backup files already exist, cannot backup again, if you want backup mandatory,
                            please set the flag: "force_backup" to 'True', but only clean the target folder'''
                        else:
                            shutil.rmtree(backup_sub_folder)
                            shutil.copytree(svc_deploy_folder, backup_sub_folder)
                            print "Clean the backup sub folder mandatory and copy %s to %s"%(svc_deploy_folder,backup_sub_folder)
                    self.__cls_oldver(svc_deploy_folder)
                    print "Remove old jar files name with -SNAPSHOT.jar"
                    for each_svc in source_files: 
                        '''Copy each jar file to target path'''
                        src_svc = os.path.join(source_sub_folder,each_svc)
                        dst_svc = os.path.join(svc_deploy_folder,each_svc)
                        if os.path.exists(dst_svc):
                            os.remove(dst_svc)
                        shutil.copy(src_svc,dst_svc)
                        print "Copy service from %s to %s."%(src_svc,dst_svc)
                    #self.__restart(self.svc_items[sub_sc],svc_run_items[sub_sc])
                else:
                   print "Deploy folder %s not exist!"%svc_deploy_folder
            else:                        
                print "No file under %s"%source_sub_folder
        else:
            print "The source folder: %s not exist!"%source_sub_folder   
            
    def __deploy_web(self,sub_sc):
        '''deploy web application'''
        source_sub_folder = self.source_items[sub_sc]
        backup_sub_folder = self.backup_items[sub_sc] 
        web_deploy_folder = self.web_deploy_items[sub_sc]
        print "Target deploy folder is %s"%web_deploy_folder
        if os.path.exists(source_sub_folder):
            source_file = os.listdir(source_sub_folder)
            if len(source_file) != 1:
                if (os.path.exists(web_deploy_folder)):
                    print '''Start backup action'''
                    shutil.rmtree(os.path.join(web_deploy_folder,self.web_item_dst_name.split('.war')[0]))
                    print '''remove the ROOT folder'''
                    if not os.path.exists(backup_sub_folder):
                        shutil.copytree(web_deploy_folder,backup_sub_folder)
                        print "Copy %s to %s"%(web_deploy_folder,backup_sub_folder)
                    else:
                        if not self.force_backup:
                            print '''Backup files already exist, cannot backup again, 
                            if you want backup mandatory, please set the flag: "force_backup" to 'True', but only clean the target folder'''
                        else:
                            shutil.rmtree(backup_sub_folder)
                            shutil.copytree(web_deploy_folder, backup_sub_folder)
                            print "Clean the backup sub folder mandatory and copy %s to %s"%(web_deploy_folder,backup_sub_folder)                        
                    print "Copy war file to target path and rename to 'ROOT.war'"
                    for each_web in source_file:
                        src_web = os.path.join(source_sub_folder,each_web)
                        dst_web = os.path.join(web_deploy_folder,os.path.join(web_deploy_folder,self.web_item_dst_name))
                        if os.path.exists(dst_web):
                            os.remove(dst_web)
                        shutil.copy(src_web,dst_web)
                        print "Copy web package from %s to %s."%(src_web,dst_web)
                    #self.__restart(self.web_items[sub_sc],self.web_run_items[sub_sc])
                else:
                    "Deploy folder %s not exist!"%web_deploy_folder    
            else:
                print "No web file or more than one file under %s"%source_sub_folder
        else:
            print "The source folder: %s not exist!"%source_sub_folder

    def __cls_oldver(self,path):
        files = os.listdir(path)
        for file in files:
            if "-SNAPSHOT.jar".lower() in file.lower():
                os.remove(os.path.join(path,file))

    def __restart(self,sub_item,run_folder):
        print "Restart %s, and the command folder is %s"%(sub_item,run_folder)
        process_number=os.popen("ps -ef|grep " + sub_sc + "/|grep -v grep|awk '{print $2}'").read()
        process_number.strip()
        print process_number
        if process_number.isalnum():
            print "Kill the process %s of %s"%(process_number,sub_sc)
            os.popen("kill -9 "+ process_number)
        else:
            print "No process for %s"%sub_sc
        restart_command = run_folder + "start.sh"
        os.chmod(restart_command,stat.S_IRWXU+stat.S_IRWXG+stat.S_IRWXO)
        os.popen("sh " + restart_command) 
        
    def start_deploy(self):
        sc = self.deploy_scope
        if sc == 'all':
            pass
        else:
            if sc in self.svc_items.keys():
                self.__deploy_svc(sc)
            elif sc in self.web_items.keys():
                self.__deploy_web(sc)
            else:
                print "There's no such service or web application: %s"%sc
                sys.exit(1)
                                       
    def recover(self):
        pass
    
    def check_status(self):
        pass
    
def deploy_test():
    '''传入带有版本号的路径，以及需要部署的service或是web工程，或是需要全部则 all'''
    d = deploy(r"F:\test\source\0.4.1",'ac')
    d.start_deploy()

def deploy_run():
    dep = deploy(r"/root/Webpay-package-files/0.3.4/2015-01-09_18-10-00",'all')
    
if __name__ == "__main__":
    deploy_test()