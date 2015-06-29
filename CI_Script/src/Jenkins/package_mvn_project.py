# -*- coding: utf-8 -*-
#author:Dong Jie
#mail:dongjie789@sina.com
#!/usr/bin/python
import os,sys,re,subprocess,time,platform
from ConfigParser import ConfigParser
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from Jenkins import SysUtil
class package_mvn_project(object):
    '''
    this class is use to analyze maven project, and package them one by one.
    '''
    def __init__(self,maven_project,target_version,scope='all',dict_file=None,
                 read_dict=False,ignore_failure=True):
        '''
        initialize the class parameters:
        maven_project: project folder, like "E:\webpay_workspace_test",
                "/jenkins/jobs/Webpay_Trunk_Compile_Package_On_Linux/workspace".
        target_version: build version like "0.4.1-SNAPSHOT".
        scope: projects to be build, like 'all','payment-ac','payment-ac-api'.
        dict_file: the dictionary file path, the file contains the dependency of whole project.
        read_dict: True: read from dict_file; 
                   False: will generate dependency from analyzing
        ignore_failure: when read_dict is false, it will generate dependency from analyzing result. 
                True: ignore the analyze failure; 
                False: won't ignore the analyze failure
            About the relationship of dict_file and ignore_failure:
            read_dict
                False: output and analyze dependency log 
                    --> ignore_failure === ignore_check_dependency_log, it is active when read_dict was False.
                        True: will generate dependency dictionary when some projects build failed. 
                        False: won't generate dependency dictionary when some projects build failed.
                True: won't output and analyze dependency log; 
                       will use this specified dictionary file to generate dependency dictionary                                                
        '''
        self.maven_project = maven_project
        self.target_version = target_version
        self.scope=scope
        self.dict_file = dict_file
        self.read_dict = read_dict
        self.ignore_failure = ignore_failure
        self.maven_home = ""
        self.dependencies = {}
        self.package_status = {}
        self.os_type = None
        self.dependency_check_result = "Jenkins/mvn_dependency.txt"
        self.dependency_tree = "Jenkins/mvn_dependecy_tree.txt"
        self.sub_maven_project = []
        self.obsolete_project = [".svn"]
        self.mvn_timeout=20
        sys.setrecursionlimit(1000)
        self.os_types = self._enum(Windows = "windows",Linux = "linux", Mac = "mac")
        self._getostype()
        self._get_maven_env()
        self._read_cfg()

    def pre_mvn_project(self):
        '''
        prepare maven projects and store them to sub_maven_project
        '''
        maven_project = self.maven_project
        sub_maven_project = []        
        for root, dirs, files in os.walk(maven_project):
            print "==========Start to ignore obsolete folder=========="
            for obsolete in self.obsolete_project:
                if obsolete in dirs:
                    dirs.remove(obsolete)
                    print "There's no need to build %s, ignore it."%obsolete
            sub_maven_project = dirs[:]
            print "==========Start to check the pom file and ignore the illegal folder=========="
            for sub_dir in dirs:
                for level_1_root, level_1_dirs, level_1_files in os.walk(maven_project+os.sep+sub_dir):
                    if len(level_1_files) == 0:
                        sub_maven_project.remove(sub_dir)
                        print "There's no file under %s, ignore it."%sub_dir
                    else:
                        #if contains pom.xml, then check its version
                        for level_1_element in level_1_files:
                            if "pom.xml".lower() in level_1_element.lower():
                                self._check_pom_version(maven_project+os.sep+sub_dir+os.sep+"pom.xml")
                    for sub_sub_dir in level_1_dirs:
                        for level_2_root, level_2_dirs, level_2_files in os.walk(maven_project+os.sep+sub_dir+os.sep+sub_sub_dir):
                            #if contains pom.xml, then check its version
                            for level_2_element in level_2_files:
                                if "pom.xml".lower() in level_2_element.lower():
                                    self._check_pom_version(maven_project+os.sep+sub_dir+os.sep+sub_sub_dir+os.sep+"pom.xml")
                            break
                    break
            break
        self.sub_maven_project = sub_maven_project
  
    def gen_depend_dict(self):
        if self.read_dict:
            gen_result = self._read_dict_file()
        else:
            gen_result = self._op_analyze_depend()   
        return gen_result     

    def package(self):
        '''
        Package according to the dependencies
        '''
        print "==========Start to package needed maven projects=========="
        scope = self.scope
        self._package_start()
        dependencies = self.dependencies
        package_status = self.package_status
        for key in dependencies.keys():
            package_status[key] = ""
        if scope == 'all':
            for key in package_status.keys():
                self._package_project(key)
        elif scope.count('-')>=2 or scope.count('-') == 0:
            self._package_project(scope.strip())
        elif scope.count('-')==1:
            for key in dependencies.keys():
                if scope+'-' in key:
                    self._package_project(key)

    def remove_pom(self):
        '''
        remove pom.xml file, because they has been modified, when update the svn folder, it cause some error
        '''
        for root, dirs, files in os.walk(self.maven_project):
            for f in files:
                if "pom.xml" in f:
                    print "Now remove the modified pom.xml file %s ..."%str(os.path.join(root,f))
                    os.remove(os.path.join(root,f))
    
    def save_dict_file(self):
        '''
        Save the dependencies to dict file
        '''
#        package_folder = os.path.split(os.path.abspath(sys.argv[0]))[0]
#        package_name = os.path.split(package_folder)[1]
#        print os.path.join(self.maven_project,package_name)
        os.chdir(os.path.join(self.maven_project,"Jenkins"))
        print "Save the dependencies to %s under %s"%(self.dict_file,os.getcwd())
        if os.path.exists(self.dict_file):
            os.remove(self.dict_file)
        s_dict = open(self.dict_file,'a')
        for key in self.dependencies.keys():
            s_dict.write("%s %s\n"%(key,str(self.dependencies[key])))
        s_dict.close()

    def _enum(self,**enums):
        return type('Enum',(),enums)

    def _getostype(self):
        os_string = platform.platform().lower()
        if self.os_types.Windows in os_string:
            self.os_type = self.os_types.Windows
        elif self.os_types.Linux in os_string:
            self.os_type = self.os_types.Linux
        else:
            print "Cannot get OS type, exit..."
            sys.exit(1)
        print "OS type is %s"%self.os_type
    
    def _get_maven_env(self):
        '''
        Get the maven install path and other information
        '''
        maven_home=''
        os_type = self.os_type
        os.popen("mvn -version>maven_info.txt")
        maven_file = open("maven_info.txt","r")
        try: 
            maven_info = maven_file.read()
            if maven_info != "":
                maven_lines = maven_info.splitlines()
                for each_line in maven_lines:
                    if "Maven home".lower() in each_line.lower():
                        maven_home = each_line.split("home:")[1].strip()
                        if "bin" not in maven_home:
                            maven_home = maven_home+os.sep+"bin"
                        else:
                            if not maven_home.endswith("bin"):
                                maven_home = maven_home.split("bin")[0]+"bin"
                        if "windows" in os_type:
                            maven_home = maven_home + os.sep + "mvn.bat"
                        elif "linux" in os_type:
                            maven_home = maven_home + os.sep + "mvn"
                        print "Maven home: %s"%maven_home
                        self.maven_home = maven_home                        
        except Exception as error:
            print "Exception occur: %s."%error
        finally:
            maven_file.close()       
        if maven_home == "":
            print "Maven environment is not configured correctly, please check."
            sys.exit(1)
    def _read_cfg(self):
        '''read configuration'''
        config = ConfigParser()
        config.readfp(open("Jenkins.ini"))
        self.obsolete_project[len(self.obsolete_project):] = eval(config.get("package","exclude_project"))
        print "obsolete project folder are %s"%self.obsolete_project
            
    def _check_pom_version(self,pom_file):
        '''
        check the sub version of each project's pom file
        '''
        target_version = self.target_version
        post_pom_file = pom_file.replace(self.maven_project,'')
        #exclude the test folder contains the pom.xml file
        if "test" not in post_pom_file.lower():
            pom = open(pom_file,'r+')
            try:
                pom_content = pom.read()
            finally:
                pom.close()
            if "<version>" + target_version + "</version>" in pom_content:
                print "The version of %s is right."%pom_file
            else:
                print "The version of %s is not %s, fix it."%(pom_file,target_version)
                pom_content = re.sub("<version>\d{1,2}\.\d{1,2}\.\d{1,2}-SNAPSHOT</version>", "<version>"+target_version+"</version>", pom_content, 0, re.IGNORECASE)
#                pom.seek(0)
#                pom.write(pom_content)
            #Why Linux is \r\n,windows is \n??????
            re_obj_run_on_windows = "<plugin>\n.*\n.*<artifactId>wagon-maven-plugin</artifactId>(\n.*){1,15}<url>scp.*</url>(\n.*){1,20}</plugin>"
            re_obj_run_on_linux = "<plugin>\r\n.*\r\n.*<artifactId>wagon-maven-plugin</artifactId>(\r\n.*){1,15}<url>scp.*</url>(\r\n.*){1,20}</plugin>"
            if self.os_type == 'windows':
                re_obj = re_obj_run_on_windows
            elif self.os_type == 'linux':
                re_obj = re_obj_run_on_linux
            else:
                print "The os is not windows or linux, please check."
            re_parent_obj = "<subSystem.version>\d{1,2}\.\d{1,2}\.\d{1,2}-SNAPSHOT</subSystem.version>"
            if re.search(re_obj,pom_content,flags=re.IGNORECASE):
                pom_content = re.sub(re_obj,"",pom_content,0,flags=re.IGNORECASE)
            if re.search(re_parent_obj,pom_content,flags=re.IGNORECASE):
                pom_content = re.sub(re_parent_obj,"<subSystem.version>"+target_version+"</subSystem.version>",pom_content,0,flags=re.IGNORECASE)
            pom = open(pom_file,"w")
            try:
                pom.write(pom_content)
            finally:
                pom.close()
 
    def _op_analyze_depend(self):
        '''
        use "mvn dependency:tree" to output dependencies of whole project and analyse them
        '''
        maven_project = self.maven_project
        dependency_check_result = self.dependency_check_result
        print "==========Start to output the dependency=========="
        os.chdir(maven_project)
        if os.path.exists(dependency_check_result):
            os.remove(dependency_check_result)
        for sub_folder in self.sub_maven_project:
            os.chdir(maven_project+os.sep+sub_folder)
            print "Check the dependency of %s"%sub_folder
            os.popen("mvn dependency:tree>>../"+dependency_check_result)
        if len(self.sub_maven_project) == 0:
            print "The maven project folder structure is empty, please check"
            sys.exit(1)        
        #filter all dependencies, exclude the maven goal is pom type
        start = False
        all_dependency = []
        dependency_file = open(maven_project+os.sep+dependency_check_result,"rU")
        one_package_name = ""
        try:
            dependency_content = dependency_file.readlines()
        finally:
            dependency_file.close()
        for line in dependency_content:
            if "[INFO] --- maven-dependency-plugin:" in line:
                start = True
                one_package_name = line.split("@")[1].strip()
                all_dependency.append(line)
                continue
            if start:
                if ":" in line:
                    if line.split(":")[1] in one_package_name:
                        maven_goal = line.split(":")[2].lower()
                        if maven_goal != "jar" and maven_goal != "war":
                            start = False
                            all_dependency.pop()
                            one_package_name = ""
                            continue            
                if "[INFO] ----------------------------" in line:
                    start = False
                all_dependency.append(line)        
        #Save all the dependency tree to file
        depend_hander = open(maven_project+os.sep+self.dependency_tree,"w")
        try:
            depend_hander.writelines(all_dependency)
        finally:
            depend_hander.close()    
        print "==========Start to check the dependency log=========="
        if not self.ignore_failure:
            if self._check_depend_succ():
                print "All maven projects check dependency success, continue create the dependencies dictionary."
                self._create_dependencies(all_dependency)
                return True
            else: 
                print "Some maven projects check dependency failed."
                return False
        else:
            print "Flag 'ignore_failure' is set to True, so ignore checking dependency log."
            self._create_dependencies(all_dependency)
            return True
    
    def _check_depend_succ(self):
        '''
        Check the all the dependency creating with out Error or FAILURE
        '''
        check_log = open(self.maven_project+os.sep+self.dependency_check_result,"r")
        success = True
        #todo: sometimes cannot read all content of the dependency log file
        try:
            check_content = check_log.readlines()
            for line in check_content:
                if "[INFO] BUILD FAILURE" in line:# or "[ERROR]" in line:
                    print "Some maven projects check dependency failed, please check....."
                    success = False
                    #break
        finally:
            check_log.close()
            return success
        
    def _create_dependencies(self,all_dependency):
        '''Add 2 flags lines to mark the first line of file and last line of maven project'''
        current_project = []
        startline = "---start---"
        endline = "---end---"
        current_project.append(startline)
        #filter the projects like pament-xx-xxx out,exclude deep dependencies which from third part
        for line in all_dependency:
            if "payment" in line:
                current_project.append(line)
            if "[INFO] ----------------------------" in line:
                current_project.append(endline)
        #Create a dictionary according to current_project
        print "==========Start to create the dependency dictionary=========="
        item_key = ""
        dependency_item_value = []
        item_begin = False
        for each_line in current_project:
            #Need confirm why the format of payment boss is not same to other
            if "[INFO] com.zlinepay.payment" in each_line or "[INFO] payment-boss" in each_line:
                item_begin = True
                item_key = each_line.split(":")[1]
                continue
            if item_begin:
                if ("[INFO] +- com.zlinepay.payment" in each_line or "[INFO] \- com.zlinepay.payment" in each_line):
                    dependency_item_value.append(each_line.split(":")[1])
                    continue
                #match the key words or last item
                if endline == each_line:
                    item_begin = False
                    self.dependencies[item_key] = dependency_item_value[:]
                    print item_key, dependency_item_value
                    #Reset the key and value
                    item_key = ""
                    dependency_item_value = []
                    continue
 
    def _read_dict_file(self):
        '''
        To use this script, need prepare the dictionary file about the dependency tree, 
        it will create dependencies dictionary
        '''
        read_status = True
        re_key_obj = ' |:'
        re_value_obj = '\[|\]'
        depend_file = open(self.dict_file,'r')
        try:
            depeng_content = depend_file.readlines()
        except Exception as error:
            print error
            read_status = False
        finally:
            depend_file.close()
        try:
            for each_depend in depeng_content:
                each_depend = each_depend.strip()
                key = re.split(re_key_obj, each_depend)[0].strip("\'")
                value = re.split(re_value_obj,each_depend)[1]
                list_value = []
                if len(value) != 0:
                    for item in value.split(","):
                        list_value.append(item.strip().strip("\'"))
                else:
                    list_value = []
                self.dependencies[key] = list_value
                print key,list_value
        except Exception as error:
            print "Generate dependencies dictionary failed: %s"%error
            read_status = False
        return read_status
    
    def _package_start(self):
        '''
        for some special maven projects like parent which 
        maven goal type is 'pom' need package first
        '''
        project = ["payment-parent"]
        for sub_project in project:
            self._change_dir(sub_project)
            print "Current folder: %s, start package %s"%(os.path.abspath("."),sub_project)
            p = subprocess.Popen([self.maven_home,"clean","install"],stdout=subprocess.PIPE)
            self._pollprocess(sub_project,p)
 
    def _package_project(self,key):
        '''
        package directed maven project using recurs
        '''
        dependencies = self.dependencies
        package_status = self.package_status
        maven_home = self.maven_home 
        try:
            if package_status[key] == "":
                if len(dependencies[key]) == 0:
                    self._change_dir(key)
                    print "Current folder: %s, start package %s"%(os.path.abspath("."),key)
#                    p = subprocess.Popen([maven_home,"clean","install"],stdout=subprocess.PIPE)
                    p = subprocess.Popen([maven_home,"clean","install","dependency:copy-dependencies","-DoutputDirectory=target/"],stdout=subprocess.PIPE)
                    self._pollprocess(key,p)               
                if len(dependencies[key]) >= 1:
                    depend_values = dependencies[key]
                    for depend_value in depend_values:
                        if package_status[depend_value] == "":
                            self._package_project(depend_value)
                    depengd_pakage_status = True
                    for depend_value in depend_values:
                        if package_status[depend_value] == "unpackaged":
                            depengd_pakage_status = False
                    if depengd_pakage_status:
                        self._change_dir(key)
                        print "Current folder: %s, start package %s"%(os.path.abspath("."),key)
                        p = subprocess.Popen([maven_home,"clean","install","dependency:copy-dependencies","-DoutputDirectory=target/"],stdout=subprocess.PIPE)
                        self._pollprocess(key,p)
                    else:
                        package_status[key] = "unpackaged"
            else:
                #item has been processed, no need to package again.
                pass
        except KeyError as error:
            package_status[key] = "unpackaged"        
            print "%s no such key in dictionary, refer item is %s %s, please check."%(error,key,dependencies[key])
            print key,package_status[key]
        except Exception as error:
            package_status[key] = "unpackaged"        
            print "Exception occur:%s, please check."%error
            print key,package_status[key]

    def _change_dir(self,project_name):
        '''
        Change the work folder according to the maven project, must be sure the folder is like "payment-pss-entity", 
        "payment-pss-common-api", and the "payment-pss" is parent folder
        '''
        if 1<=len(project_name.split("-")) <= 2:
            os.chdir(self.maven_project+os.sep+project_name)
        elif len(project_name.split("-")) >= 3:
            os.chdir(self.maven_project+os.sep+project_name.split("-")[0]+"-"+project_name.split("-")[1]+os.sep+project_name)
        else:
            print "Please check the format of maven folder %s..."%project_name

    def _pollprocess(self, key, process):
        '''
        poll the process until timeout, then end the process, then check all the package all project success or not
        key  the maven project
        process  the subprocess.Popen() object
        '''
        package_status = self.package_status
        temp_time = self.mvn_timeout
        stdout = process.communicate()[0]
        all_stdout = stdout
        print "Sub process return code is %s"%str(process.poll())
        while process.poll() is None:
            print "polling package return or not..."
            print "Polling start..."
            stdout = process.communicate()[0]
            all_stdout = all_stdout+stdout
            time.sleep(0.5)
            temp_time = temp_time-0.5
            if temp_time<0:
                print "Package %s not finish after %d seconds, end the process..."%(key,self.mvn_timeout)
                process.kill()#for linux,Kill the process with SIGKILL
                process.terminate()#for windows,call Windows API TerminateProcess()
                print "Polling end..."
                break
        log = open(self.maven_project+os.sep+"package.txt","a")
        try:
            log.write("==========" + key + " package log start==========/n")
            log.write(all_stdout)
        finally:
            log.close()
        print "Check package result"
        if "[INFO] BUILD SUCCESS" in all_stdout:
            package_status[key] = "packaged"
            print key,package_status[key]
        elif "[INFO] BUILD FAILURE" in all_stdout:
            package_status[key] = "unpackaged"
            print key,package_status[key]
            sys.exit(1)
        else:
            package_status[key] = "unpackaged"
            print "%s log is too less, package status is not sure..."%key
            sys.exit(1)

def package_test(maven_project,target_version,package_scope,dict_file,read_dict,ignore_failure):
    pack_proj = package_mvn_project(maven_project,target_version,scope=package_scope,dict_file=dict_file,
                                    read_dict=read_dict,ignore_failure=ignore_failure)     
    pack_proj.pre_mvn_project()
    if pack_proj.gen_depend_dict():
        print "Length of dependencies is %s ."%str(len(pack_proj.dependencies))
        print pack_proj.dependencies
        pack_proj.package()
        print "Length of package_status is %s ."%str(len(pack_proj.package_status))
        print pack_proj.package_status
        #pack_proj.remove_pom()   
    else:
        print "Dependencies dictionary generate failed...exit."
        #pack_proj.remove_pom()
        sys.exit(1)                

def package_run():
    err_msg ="""Format of arguments are not right, please check.
        usage:package_mvn_project project_folder project_version scope=package_scope 
        dict_file=dict_file output_and_analyse_dependency ignore_check_dependency_log
        example:
            package all projects:
                package.py '/root/Trunk' '0.4.0-SNAPSHOT' 'all'
            package projects of payment-ac:
                package.py '/root/Trunk' '0.4.1-SNAPSHOT' 'payment-ac'
            package specified project:
                package.py 'E:\webpay_workspace_test' '0.4.1-SNAPSHOT' 'payment-ac-api' 
            when only generating dependencies dict use:
                package.py '/root/Trunk' '0.4.0-SNAPSHOT'"""
    if len(sys.argv) == 3:
        if os.path.isdir(sys.argv[1]) and re.search("\d{1,2}\.\d{1,2}\.\d{1,2}-SNAPSHOT",sys.argv[2],re.IGNORECASE):
            maven_project = sys.argv[1]
            target_version = sys.argv[2]
            dict_file = r"dict.txt"
            read_dict = False
            pack_proj = package_mvn_project(maven_project,target_version,dict_file=dict_file,read_dict=read_dict)
            pack_proj.pre_mvn_project()
            if pack_proj.gen_depend_dict():
                print "Length of dependencies is %s ."%str(len(pack_proj.dependencies))
                print pack_proj.dependencies
                pack_proj.save_dict_file()  
            else:
                print "Dependencies dictionary generate failed...exit."
                sys.exit(1) 
        else:
            print err_msg
            sys.exit(1)        
    elif len(sys.argv) == 4:
        if os.path.isdir(sys.argv[1]) and re.search("\d{1,2}\.\d{1,2}\.\d{1,2}-SNAPSHOT",sys.argv[2],re.IGNORECASE):
            maven_project = sys.argv[1]
            target_version = sys.argv[2]
            package_scope = sys.argv[3]
            dict_file = r"dict.txt"
            read_dict = True
            ignore_failure = False
            pack_proj = package_mvn_project(maven_project,target_version,scope=package_scope,dict_file=dict_file,
                                            read_dict=read_dict,ignore_failure=ignore_failure)        
            pack_proj.pre_mvn_project()
            if pack_proj.gen_depend_dict():
                print "Length of dependencies is %s ."%str(len(pack_proj.dependencies))
                print pack_proj.dependencies
                pack_proj.package()
                print "Length of package_status is %s ."%str(len(pack_proj.package_status))
                print pack_proj.package_status  
            else:
                print "Dependencies dictionary generate failed...exit."
                sys.exit(1) 
        else:
            print err_msg
            sys.exit(1)
    else:
        print err_msg
        sys.exit(1)
        
if __name__ == "__main__": 
    #package_test(r"E:\webpay_workspace_test","0.4.1-SNAPSHOT",'all',r"dict.txt",False,True)
    package_run()