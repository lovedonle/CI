# -*- coding: utf-8 -*-
#!/usr/bin/python
#ver0.2
import os,sys,re,subprocess,time,platform

#Project foler
maven_project = r"E:\webpay_workspace_test"#r"/jenkins/jobs/Webpay_Trunk_Compile_Package_On_Linux/workspace"
target_version = "0.4.1-SNAPSHOT"
dict_file = r"dict.txt"

#maven home, like "C:\apache-maven-3.2.5\bin\mvn.bat",but different between linux and windows, create it dynamically
maven_home = ""
#Store the dependencies to a dict
dependencies = {}
#Store the package status
package_status = {}
os_type = ""
dependency_check_result = "mvn_dependency.log"
dependency_tree = "mvn_dependecy_tree.log"
sub_maven_project = []
obsolete_project = [".svn","payment-redis","payment-cashier","zpos-server","sdk_demo"]
sys.setrecursionlimit(1000)
mvn_timeout=20
#flag to output and analyse dependency
output_and_analyse_dependency=False
#flag to check all dependency log fail or success when creating dependencies dict
ignore_check_dependency_log=False

def getostype():
    global os_type
    os_string = platform.platform().lower()
    w = 'windows'
    l = 'linux'
    mac = 'mac'
    if w in os_string:
        os_type = w
    elif l in os_string:
        os_type = l
    else:
        print "Cannot get OS type, exit..."
        sys.exit(1)


def get_maven_env():
    '''
    Get the maven install path and other information
    '''
    global maven_home
    os.popen("mvn -version>maven_info.txt")
    maven_info = open("maven_info.txt","r")
    try:        
        for each_line in maven_info.readlines():
            if "Maven home".lower() in each_line.lower():
                maven_home = each_line.split("home:")[1].strip()
            if "OS name".lower() in each_line.lower():
                OS_type = each_line.split("\"")[1]
    finally:
        maven_info.close()
    if "bin" not in maven_home:
        maven_home = maven_home+os.sep+"bin"
    else:
        if not maven_home.endswith("bin"):
            maven_home = maven_home.split("bin")[0]+"bin"
    if "windows" in OS_type:
        maven_home = maven_home + os.sep + "mvn.bat"
    elif "linux" in OS_type:
        maven_home = maven_home + os.sep + "mvn"
    print "Maven home: %s"%maven_home

def prepare_maven_project():
    '''
    prepare maven projects and store them to sub_maven_project
    '''
    global maven_project,sub_maven_project,obsolete_project
    for root, dirs, files in os.walk(maven_project):
        print "======================Start to remove obsolete folder======================"
        for obsolete in obsolete_project:
            if obsolete in dirs:
                dirs.remove(obsolete)
                print "There's no need to build %s, remove it."%obsolete
        sub_maven_project = dirs[:]
        print "======================Start to check the pom file and remove the illegal folder======================="
        for sub_dir in dirs:
            for level_1_root, level_1_dirs, level_1_files in os.walk(maven_project+os.sep+sub_dir):
                if len(level_1_files) == 0:
                    sub_maven_project.remove(sub_dir)
                    print "There's no file under %s, remove it."%sub_dir
                else:
                    #if contains pom.xml, then check its version
                    for level_1_element in level_1_files:
                        if "pom.xml".lower() in level_1_element.lower():
                            _check_pom_version(maven_project+os.sep+sub_dir+os.sep+"pom.xml")
                for sub_sub_dir in level_1_dirs:
                    for level_2_root, level_2_dirs, level_2_files in os.walk(maven_project+os.sep+sub_dir+os.sep+sub_sub_dir):
                        #if contains pom.xml, then check its version
                        for level_2_element in level_2_files:
                            if "pom.xml".lower() in level_2_element.lower():
                                _check_pom_version(maven_project+os.sep+sub_dir+os.sep+sub_sub_dir+os.sep+"pom.xml")
                        break
                break
        break

def output_analyse_dependency():
    '''
    use "mvn dependency:tree" to output dependencies of whole project and analyse them
    '''
    global maven_project,sub_maven_project,dependencies,dependency_check_result,dependency_tree,ignore_check_dependency_log
    print "======================Start to output the dependency======================="
    os.chdir(maven_project)
    if os.path.exists(dependency_check_result):
        os.remove(dependency_check_result)
    for sub_folder in sub_maven_project:
        os.chdir(maven_project+os.sep+sub_folder)
        print "Check the dependency of %s"%sub_folder
        os.popen("mvn dependency:tree>>../"+dependency_check_result)
    if len(sub_maven_project) == 0:
        print "The maven project folder structure is empty, please check"
        sys.exit(1)

    #filter all dependecy, exclude the maven goal is pom type
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
    depend_hander = open(maven_project+os.sep+dependency_tree,"w")
    try:
        depend_hander.writelines(all_dependency)
    finally:
        depend_hander.close()    
    print "======================Start to check the dependency log======================"
    if not ignore_check_dependency_log:
        if _check_dependency_success():
            print "All maven projects check dependency success, continue create the dependencies dictionary."
            _create_dependencies(all_dependency)
            return True
        else: 
            print "Some maven projects check dependency failed, exit..."
            return False
    else:
        print "Flag 'ignore_check_dependency_log' is set to True, so ignore checking dependency log."
        _create_dependencies(all_dependency)
        return True

def read_dict_file():
    '''
    To use this script, need prepare the dict file about the dependency tree, it will create dependencies dict
    '''
    global dependencies
    read_status = True
    re_key_obj = ' |:'
    re_value_obj = '\[|\]'
    depend_file = open(dict_file,'r')
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
            dependencies[key] = list_value
            print key,list_value
    except Exception as error:
        print "Generate dependencies dictionary failed: %s"%error
        read_status = False
    return read_status

def package(package_scope = None):
    '''
    Package according to the dependencies
    '''
    print "======================Start to package all maven projects======================="
    #package parent
    _package_start()
    #loop package
    global dependencies,package_status
    for key in dependencies.keys():
        package_status[key] = ""
    if package_scope is None:
        for key in package_status.keys():
            _package_one_project(key)
    elif package_scope.count('-')>=2 or package_scope.count('-') == 0:
        _package_one_project(package_scope.strip())
    elif package_scope.count('-')==1:
        for key in dependencies.keys():
            if package_scope+'-' in key:
                _package_one_project(key)
        
def remove_pom():
    '''
    remove pom.xml file, because they has been modified, when update the svn folder, it cause some error
    '''
    global maven_project
    for root, dirs, files in os.walk(maven_project):
        for f in files:
            if "pom.xml" in f:
                print "Now remove the modified pom.xml file %s ..."%str(os.path.join(root,f))
                os.remove(os.path.join(root,f))

def _package_start():
    '''
    for some special maven projects like parent which pakage type is pom, but need package first
    '''
    global package_status,maven_home
    project = ["payment-parent"]
    for sub_project in project:
        _change_dir(sub_project)
        print "Current folder: %s, start package %s"%(os.path.abspath("."),sub_project)
        p = subprocess.Popen([maven_home,"clean","install"],stdout=subprocess.PIPE)
        _pollprocess(sub_project,p)

def _package_one_project(key):
    '''
    package directed maven project using recurs
    '''
    global dependencies,package_status,maven_home
    try:
        if package_status[key] == "":
            if len(dependencies[key]) == 0:
                _change_dir(key)
                print "Current folder: %s, start package %s"%(os.path.abspath("."),key)
                p = subprocess.Popen([maven_home,"clean","install","dependency:copy-dependencies","-DoutputDirectory=target/"],stdout=subprocess.PIPE)
                _pollprocess(key,p)               
            if len(dependencies[key]) >= 1:
                depend_values = dependencies[key]
                for depend_value in depend_values:
                    if package_status[depend_value] == "":
                        _package_one_project(depend_value)
                depengd_pakage_status = True
                for depend_value in depend_values:
                    if package_status[depend_value] == "unpackaged":
                        depengd_pakage_status = False
                if depengd_pakage_status:
                    _change_dir(key)
                    print "Current folder: %s, start package %s"%(os.path.abspath("."),key)
                    p = subprocess.Popen([maven_home,"clean","install","dependency:copy-dependencies","-DoutputDirectory=target/"],stdout=subprocess.PIPE)
                    _pollprocess(key,p)
                else:
                    package_status[key] = "unpackaged"
        else:
            #item has been processed, no need to package again.
            pass
    except KeyError as error:
        package_status[key] = "unpackaged"        
        print "%s no such key in dict, refer item is %s %s, please check."%(error,key,dependencies[key])
        print key,package_status[key]
    except Exception as error:
        package_status[key] = "unpackaged"        
        print "Exception occur:%s, please check."%error
        print key,package_status[key]

def _pollprocess(key, process):
    '''
    poll the process until timeout, then end the process, then check all the package all project success or not
    key  the maven project
    process  the subprocess.Popen() object
    '''
    global package_status,mvn_timeout
    temp_time = mvn_timeout
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
            print "Package %s not finish after %d seconds, end the process..."%(key,mvn_timeout)
            process.kill()#for linux,Kill the process with SIGKILL
            process.terminate()#for windows,call Windows API TerminateProcess()
            print "Polling end..."
            break
    print "Check package result"
    if "[INFO] BUILD SUCCESS" in all_stdout:
        package_status[key] = "packaged"
        print key,package_status[key]
    elif "[INFO] BUILD FAILURE" in all_stdout:
        package_status[key] = "unpackaged"
        print key,package_status[key]
    else:
        package_status[key] = "unpackaged"
        print "%s log is too less, package status is not sure..."%key
    log = open("package.log","w")
    try:
        log.write(all_stdout)
    finally:
        log.close()

def _check_pom_version(pom_file):
    '''
    check the sub version of each project's pom file
    '''
    global maven_project,os_type
    post_pom_file = pom_file.replace(maven_project,'')
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
            print "The version of %s is not equal to %s, try to fix the version info according to the given version."%(pom_file,target_version)
            #replace all version in the pom file
            pom_content = re.sub("<version>\d{1,2}\.\d{1,2}\.\d{1,2}-SNAPSHOT</version>", "<version>"+target_version+"</version>", pom_content, 0, re.IGNORECASE)
##            pom.seek(0)
##            pom.write(pom_content)
        #Why Linux is \r\n,windows is \n??????
        re_obj_run_on_windows = "<plugin>\n.*\n.*<artifactId>wagon-maven-plugin</artifactId>(\n.*){1,15}<url>scp.*</url>(\n.*){1,20}</plugin>"
        re_obj_run_on_linux = "<plugin>\r\n.*\r\n.*<artifactId>wagon-maven-plugin</artifactId>(\r\n.*){1,15}<url>scp.*</url>(\r\n.*){1,20}</plugin>"
        if os_type == 'windows':
            re_obj = re_obj_run_on_windows
        elif os_type == 'linux':
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
    
def _create_dependencies(all_dependency):
    #Add 2 flags lines to mark the first line of file and last line of maven project
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
    #Create a dict according to current_project
    print "======================Start to create the dependency dictionary======================="
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
                dependencies[item_key] = dependency_item_value[:]
                print item_key, dependency_item_value
                #Reset the key and value
                item_key = ""
                dependency_item_value = []
                continue
    print "======================Dependencies dictionary generate OK======================="

def _check_dependency_success():
    '''
    Check the all the dependency creating with out Error or FAILURE
    '''
    check_log = open(maven_project+os.sep+dependency_check_result,"r")
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

def _change_dir(project_name):
    '''
    Change the work folder according to the maven project, must be sure the folder is like "payment-pss-entity", 
    "payment-pss-common-api", and the "payment-pss" is parent folder
    '''
    if 1<=len(project_name.split("-")) <= 2:
        os.chdir(maven_project+os.sep+project_name)
    elif len(project_name.split("-")) >= 3:
        os.chdir(maven_project+os.sep+project_name.split("-")[0]+"-"+project_name.split("-")[1]+os.sep+project_name)
    else:
        print "Please check the format of maven folder %s..."%project_name

def for_test():
    global output_and_analyse_dependency,package_status,dependencies
    getostype()
    get_maven_env()        
    package_scope='payment-ac'#'payment-ac-api','all'
    prepare_maven_project()
    generate_dict_result = False
    if output_and_analyse_dependency:
        generate_dict_result = output_analyse_dependency()
    else:
        generate_dict_result = read_dict_file()    
    if generate_dict_result:
        print "Length of dependencies is %s ."%str(len(dependencies))
        print dependencies
        if package_scope.lower() == 'all':
            package()
        else:
            package(package_scope)
        print "Length of package_status is %s ."%str(len(package_status))
        print package_status    
    #remove_pom()
    if not generate_dict_result:
        print "Dependencies dictionary generate failed...exit."
        sys.exit(1)

def normal_task():
    global maven_project,target_version,output_and_analyse_dependency,dependencies,package_status
    err_msg ="""Format of arguments are not right, please check.
        usage:package.py project_folder project_version package_scope
        example:
            package all projects:
                package.py '/root/Trunk' '0.4.0-SNAPSHOT' 'all'
            package projects of payment-ac:
                package.py '/root/Trunk' '0.4.1-SNAPSHOT' 'payment-ac'
            package specified project:
                package.py 'E:\webpay_workspace_test' '0.4.1-SNAPSHOT' 'payment-ac-api'""" 
    if len(sys.argv)!=4:
        print err_msg
        sys.exit(1)
    else:
        if os.path.isdir(sys.argv[1]) and re.search("\d{1,2}\.\d{1,2}\.\d{1,2}-SNAPSHOT",sys.argv[2],re.IGNORECASE):
            maven_project = sys.argv[1]
            target_version = sys.argv[2]
            package_scope = sys.argv[3]
            getostype()
            get_maven_env()            
            prepare_maven_project()
            generate_dict_ok = False
            if output_and_analyse_dependency:
                generate_dict_ok = output_analyse_dependency()
            else:
                generate_dict_ok = read_dict_file()
            if generate_dict_ok:
                print "Length of dependencies is %s ."%str(len(dependencies))
                print dependencies
                if package_scope.lower() == 'all':
                    package()
                else:
                    package(package_scope)
                print "Length of package_status is %s ."%str(len(package_status))
                print package_status
            #Use the jenkins svn option 'clean up' to replace this method.  
            #remove_pom()
            if not generate_dict_ok:
                print "Dependencies dictionary generate failed...exit."
                sys.exit(1)
        else:
            print err_msg
            sys.exit(1)

if __name__ == "__main__":
    #set output_and_analyse_dependency as True when testing, will not output dependency log and analyse the dependency tree
    ignore_check_dependency_log = True
    output_and_analyse_dependency = True
    for_test()
    #normal_task()