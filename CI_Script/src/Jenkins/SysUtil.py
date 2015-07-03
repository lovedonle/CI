# -*- coding: utf-8 -*-
#author:Dong Jie
#mail:dongjie789@sina.com
#!/usr/bin/python
import re,os,platform,shutil
from ConfigParser import ConfigParser
__all__ = ["enum","getostype","read_cfg","createfolder","copyfolder","os_types"]

def enum(**enums):
    return type('Enum',(),enums)
os_types = enum(Windows = "windows",Linux = "linux", Mac = "mac")

def getostype():
    os_types = enum(Windows = "windows",Linux = "linux", Mac = "mac")
    os_str = platform.platform().lower()
    if os_types.Windows in os_str:
        print "OS type is %s"%os_types.Windows
        return os_types.Windows
    elif os_types.Linux in os_str:
        print "OS type is %s"%os_types.Linux
        return os_types.Linux
    elif os_types.Mac in os_str:
        print "OS type is %s"%os_types.Mac
        return os_types.Mac
    else:
        print "Cannot get OS type."

def read_cfg(ini_file,section,item):
    '''read configuration from ini file'''
    config = ConfigParser()
    config.readfp(open(ini_file))
    return eval(config.get(section,item))
    
def createfolder(path,folder=""):
    '''Create folder in specified absolute path, create if not exist'''
    os_types = enum(Windows = "windows",Linux = "linux", Mac = "mac")
    os_type = getostype()
    directory = os.path.join(path,folder)
    if os.path.exists(directory):
        print "Directory: %s exists."%directory
    else:
        if os_type == os_types.Windows:
            if re.match("^[c-g]:", directory, re.IGNORECASE):
                print "create folder %s"%directory
                os.makedirs(directory)
            else:
                print "folder path format is not correct:%s on %s system."%(directory,os_type)
        elif os_type == os_types.Linux:
            if re.match("/", directory, re.IGNORECASE):
                print "create folder %s"%directory
                os.makedirs(directory)
            else:
                print "folder path format is not correct:%s on %s system."%(directory,os_type)
        elif os_type == os_types.Mac:
            print 'create folder for mac system is not done.'
            
def copyfolder(src,dst):
    '''copy all files from src folder to dst folder, 
    if dst folder doesn't exist, create dst,
    if dst folder exists, then will delete the old file/folder which is the
    same name with source, and copy new file/folder from src to it.'''
    if os.path.exists(src):
        if not os.path.exists(dst):
            shutil.copytree(src, dst)
            print "Copying from %s to %s done."%(src,dst)
        else:
            for sub_file in os.listdir(src):
                src_file = os.path.join(src,sub_file)
                if os.path.isfile(src_file):#src is file
                    shutil.copy(src_file, dst)
                if os.path.isdir(src_file):#src is folder
                    copyfolder(src_file,os.path.join(dst,sub_file))            
    else:
        print "Source folder %s doesn't exist"%src       

if "__main__" == __name__:
    #print read_cfg("Jenkins.ini", "package", "exclude_project")
    createfolder(r"C:\\test\\dd\\d\\ad\\asd\\")
    createfolder(r"C:\\test\\dd\\d\\ad\\asd\\asd\\asd\\asd\asd\asd\asd","BB")