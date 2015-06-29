# -*- coding: utf-8 -*-
#author:Dong Jie
#mail:dongjie789@sina.com
#!/usr/bin/python
import os,sys,shutil,stat
from ConfigParser import ConfigParser
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from Jenkins import SysUtil
class deploy(object):
    '''
    this case is about deploy maven project, configure and restart service
    #传入参数 source_folder deploy_scope['all'|'payment-ac'|'payment-ac-api'] 
    #如果传入参数是all循环执行每个工程，如果是单个则执行一遍则完成
    {
    #备份所有即将被覆盖的文件，备份在指定目录下，并以job传入的时间戳为文件夹名称的一部分；
    #当新部署的包不能正常工作时可以再替换回来；
    #替换文件为新文件；done
    #检查配置文件
    #修改db配置文件，和dubbo配置文件，已有的服务可以忽略，新的服务需要修改这两项；web工程需要先启动，然后修改，最后重启【也可以考虑在打包时修改配置文件】
    #
    #重启：根据所部署的模块名字，ps -ef|grep 模块名 得到进程号，使用kill -9关闭其进程，然后重启；
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
        self.web_item_dst_name = 'ROOT.war'
        self.__read_cfg()
        self.__gen_dirctory()
        
    def __read_cfg(self):
        '''read configuration'''
        config = ConfigParser()
        config.readfp(open("Jenkins.ini"))
        self.web_items = eval(config.get("deploy","web_items"))
        self.svc_items = eval(config.get("deploy","svc_items"))
        print self.web_items
        print self.svc_items
        
    def __gen_dirctory(self):
        '''
        define the head and tail name of the deploy path and run path.
        generate deploy and run directory of web and service
        '''
        cfg_file = "Jenkins.ini"
        web_deploy = SysUtil.read_cfg(cfg_file, "deploy", "web_deploy")
        svc_deploy = SysUtil.read_cfg(cfg_file, "deploy", "svc_deploy")
        web_run = SysUtil.read_cfg(cfg_file, "deploy", "web_run")
        svc_run = SysUtil.read_cfg(cfg_file, "deploy", "svc_run")
        web_cfg = SysUtil.read_cfg(cfg_file, "deploy", "web_cfg")
        svc_cfg = SysUtil.read_cfg(cfg_file, "deploy", "svc_cfg")
        self.source_items = dict()
        self.backup_items = dict()
        self.web_deploy_items = dict()
        self.svc_deploy_items = dict()
        self.web_run_items = dict()
        self.svc_run_items = dict()
        self.web_cfg_items = dict()
        self.svc_cfg_items = dict()
        for key in self.web_items.keys():
            self.source_items[key]=os.path.join(self.source_folder,self.web_items[key])
            self.backup_items[key]=os.path.join(self.backup,self.web_items[key])
            self.web_deploy_items[key]=web_deploy['head']+self.web_items[key]+web_deploy['tail']
            self.web_run_items[key]=web_run['head']+self.web_items[key]+web_run['tail']
            self.web_cfg_items[key]=web_cfg['head']+self.web_items[key]+web_cfg['tail']
        for key in self.svc_items.keys():
            self.source_items[key]=os.path.join(self.source_folder,self.svc_items[key])
            self.backup_items[key]=os.path.join(self.backup,self.svc_items[key]) 
            self.svc_deploy_items[key]=svc_deploy['head']+self.svc_items[key]+svc_deploy['tail']
            self.svc_run_items[key]=svc_run['head']+self.svc_items[key]+svc_run['tail']
            self.svc_cfg_items[key]=svc_cfg['head']+self.svc_items[key]+svc_cfg['tail']
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
                            print '''Backup files already exist, cannot backup again, if you want backup mandatory, please set the flag: "force_backup" to 'True', here only clean the target folder'''
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
                    self.__restart(self.svc_items[sub_sc],self.svc_run_items[sub_sc])
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
                            print '''Backup files already exist, cannot backup again, if you want backup mandatory, please set the flag: "force_backup" to 'True', here only clean the target folder'''
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
                    shutil.rmtree(self.web_run_items[key].split(os.sep)[-1]+r"work/Catalina/localhost")
                    print "Remove the cache file under run folder: node/work/Catalina/localhost"
                    self.__restart(self.web_items[sub_sc],self.web_run_items[sub_sc])
                else:
                    "Deploy folder %s not exist!"%web_deploy_folder    
            else:
                print "No web file or more than one file under %s"%source_sub_folder
        else:
            print "The source folder: %s not exist!"%source_sub_folder

    def __cls_oldver(self,path):
        files = os.listdir(path)
        for f in files:
            if "-SNAPSHOT.jar".lower() in f.lower():
                os.remove(os.path.join(path,f))
    def __checkcfg(self):
        '''check dbs configuration and dubbo configuration'''
        pass
    def __restart(self,sub_item,run_folder):
        print "Restart %s, and the command folder is %s"%(sub_item,run_folder)
        process_id = os.popen("ps -ef|grep " + sub_item + "/|grep -v grep|awk '{print $2}'").read()
        process_id = process_id.strip(os.linesep)
        print "%s current process id is %s"%(sub_item,process_id)
        if process_id is not None:
            os.popen("kill -9 "+ process_id)
            print "Kill current process id %s of %s."%(process_id,sub_item)
        else:
            print "No process id for %s, start it directly."%sub_item
        restart_command = run_folder + "/start.sh"
        print "Restart script path is %s"%restart_command
        os.chmod(restart_command,stat.S_IRWXU+stat.S_IRWXG+stat.S_IRWXO)
        os.popen("sh " + restart_command) 
        new_process_id = os.popen("ps -ef|grep " + sub_item + "/|grep -v grep|awk '{print $2}'").read()
        new_process_id = new_process_id.strip(os.linesep)
        print "%s restart process id is %s ."%(sub_item,new_process_id)
        
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
    errmsg = """Format of arguments are not right, please check.
        usage:deploy.py source_folder,deploy_scope 
        example:
            deploy all projects:
                deploy.py '/root/Trunk' 'all' 
            package projects of payment-ac:
                deploy.py '/root/Trunk' 'payment-ac'"""
    if len(sys.argv) != 3:
        print errmsg
        sys.exit(1)
    else:
        d = deploy(sys.argv[1],sys.argv[2])
        d.start_deploy()
if __name__ == "__main__":
#    deploy_test()
    deploy_run()