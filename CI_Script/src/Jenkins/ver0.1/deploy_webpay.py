#!/usr/bin/python
#ver0.2
import sys,os,shutil,time,stat

#for offical using =========>
##source_folder = ""
##web_home = r"/home/tomcat/"
##service_home = r"/home/payment/"
#for offical using <=========

#for debug =========>
source_folder = r"/root/Webpay-package-files/0.3.4/2015-01-09_18-10-00"
web_home = r"/root/.jenkins/workspace/"
service_home = r"/root/.jenkins/workspace/"
#for debug <=========


#Add the backup folder under the source folder
backup_folder = source_folder+os.sep + "backup"
if (not os.path.exists(backup_folder)):
    os.mkdir(backup_folder)

jar_folder = "deploy/"
war_folder = "webapps/"
cmd_file = "bin/"

sub_web_directory = \
{
 "payment-boss" : "apache-tomcat-boss/",
 "payment-cashier" : "apache-tomcat-cashier/",
 "payment-merchant" : "apache-tomcat-merchant/",
 "payment-pre" : "apache-tomcat-pre/"
}

sub_service_directory = \
{
 "payment-ac" : "payment-ac/",
 "payment-account" : "payment-account/",
 "payment-ams" : "payment-ams/",
 "payment-channel" : "payment-channel/",
 "payment-cm" : "payment-cm/",
 "payment-cms" : "payment-cms/",
 "payment-mas" : "payment-mas/",
 "payment-pe" : "payment-pe/",
 "payment-pss" : "payment-pss/",
 "payment-rcs" : "payment-rcs/",
 "payment-report" : "payment-report/",
 "payment-route" : "payment-route/",
 "payment-security" : "payment-security/",
 "payment-settle" : "payment-settle/",
 "payment-tasks" : "payment-tasks/"
}

# Deploy one service or one web application
def deploy_specified(sub_sc):
    #Service
    if sub_sc in sub_service_directory.keys():
        target_jar_deploy_folder = service_home+sub_service_directory[sub_sc]+jar_folder
        print "Target deploy folder is %s"%target_jar_deploy_folder
        target_jar_cmd_folder = service_home+sub_service_directory[sub_sc]+cmd_file
        print "Target cmd folder is %s"%target_jar_cmd_folder
        source_sub_folder = source_folder+os.sep+sub_sc
        if os.path.exists(source_sub_folder):
            if (os.path.exists(target_jar_deploy_folder)):
                #bckup action will remove the folder
                #time_prefix = time.strftime('%Y-%m-%d_%H-%M-%S')
                backup_sub_folder = backup_folder + os.sep + sub_sc
                if not os.path.exists(backup_sub_folder):
                    print "The backup folder not exists, copy the files in target folder to backup folder..."
                    shutil.move(target_jar_deploy_folder, backup_sub_folder)
                else:
                    print "File already exist, no need to move again, but only clean the target folder"
                    shutil.rmtree(target_jar_deploy_folder)
            #Copy jar folder to target path
            shutil.copytree(source_sub_folder,target_jar_deploy_folder)
##            #End the process
##            endprocess(sub_sc)
##            #Restart the service
##            restart_command = target_jar_cmd_folder + "restart.sh"
##            os.chmod(restart_command,stat.S_IRWXU+stat.S_IRWXG+stat.S_IRWXO)
##            os.popen("sh " + restart_command)
        else:
            print "The source folder: " + source_folder+os.sep+sub_sc + " not exist!"

    #Web application
    elif sub_sc in sub_web_directory.keys():
        target_war_deploy_folder = web_home+sub_web_directory[sub_sc]+war_folder
        print "Target deploy folder is %s"%target_war_deploy_folder
        target_war_cmd_folder = web_home+sub_web_directory[sub_sc]+cmd_file
        print "Target cmd folder is %s"%target_war_cmd_folder
        source_sub_folder = source_folder + os.sep + sub_sc
        if os.path.exists(source_sub_folder):
            source_file = os.listdir(source_sub_folder)
            if len(source_file) > 1:
                print "More than one war package!"
            else:
                temp = source_file.split('.war')[0]
                if (os.path.exists(target_war_deploy_folder)):
                    #backup action will remove the folder
                    backup_sub_folder = backup_folder + os.sep + sub_sc
                    #shutil.move(target_war_deploy_folder + temp,backup_sub_folder)
                    shutil.rmtree(target_war_deploy_folder + temp)
                    shutil.rmtree(web_home+sub_web_directory[sub_sc] + "work/Catalina/localhost/" + temp)
                    if not os.path.exists(backup_sub_folder):
                        print "The backup folder not exists, copy the files in target folder to backup folder..."
                        shutil.move(target_war_deploy_folder + source_file,backup_sub_folder)
                    else:
                        print "File already exist, no need to move again, but only clean the target folder"
                        shutil.rmtree(target_war_deploy_folder)
                #Copy war file to target path
                shutil.copy(source_sub_folder + os.sep + sub_sc + os.sep + source_file,target_war_deploy_folder)
##                #End the process
##                endprocess(sub_sc)
##                #Restart the web
##                restart_command = target_war_cmd_folder + "startup.sh"
##                os.chmod(restart_command,stat.S_IRWXU+stat.S_IRWXG+stat.S_IRWXO)
##                os.popen("sh " + restart_command)

        else:
            print "The source folder: " + source_folder + os.sep + sub_sc + " not exist!"
    else:
        print "There's no such service or web application: " + sub_sc


def endprocess(sub_sc):
    if sub_sc in sub_service_directory.keys():
        sub_sc = sub_service_directory[sub_sc]
    elif sub_sc in sub_web_directory.keys():
        sub_sc = sub_web_directory[sub_sc]
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


# Deploy all service or web application
def deploy_all():
    #Service
    for sub_service in sub_service_directory.keys():
        deploy_specified(sub_service)

    #Web application
    for sub_web in sub_web_directory.keys():
        deploy_specified(sub_web)

if __name__ == "__main__":
    #1:source_folder,2:sub_sc
    source_folder = sys.argv[1]
    if sys.argv[2] == 'all':
        deploy_all()
    else:
        deploy_specified(sys.argv[2])