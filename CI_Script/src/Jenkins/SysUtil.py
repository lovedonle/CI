# -*- coding: utf-8 -*-
#author:Dong Jie
#mail:dongjie789@sina.com
#!/usr/bin/python
import re,os,platform,shutil
__all__ = ["enum","getostype"]

def enum(**enums):
    return type('Enum',(),enums)

def getostype():
    os_types = enum(Windows = "windows",Linux = "linux", Mac = "mac")
    os_str = platform.platform().lower()
    if os_types.Windows in os_str:
        return os_types.Windows
    elif os_types.Linux in os_str:
        return os_types.Linux
    elif os_types.Mac in os_str:
        return os_types.Mac
    else:
        print "Cannot get OS type."
    
def createfolder(path,folder):
    '''TODO: consider user os.makedirs() to refactory'''
    os_type = getostype()
    os_types = enum(Windows = "windows",Linux = "linux", Mac = "mac")
    if not os.path.exists(path):
        print "Directory: %s not exist."%path
    else:
        folder = folder.strip(os.sep)
        if path.endswith(os.sep):
            folder_path = path + folder
        else:
            folder_path = path + os.sep + folder
        
        if os_type == os_types.Windows:
            if re.match("[c-g]:", folder_path, re.IGNORECASE):
                print "create folder %s"%folder_path
                if (not os.path.exists(folder_path)):
                    os.mkdir(folder_path) 
            else:
                print "folder path format is not correct:%s on %s system."%(folder_path,os_type)
        elif os_type == os_types.Linux:
            if re.match("/", folder_path, re.IGNORECASE):
                print "create folder %s"%folder_path
                if (not os.path.exists(folder_path)):
                    os.mkdir(folder_path)   
            else:
                print "folder path format is not correct:%s on %s system."%(folder_path,os_type)
        elif os_type == os_types.Mac:
            print 'create folder for mac system is TBD.'
def copyfolder(src,dst):
    '''
    copy all files from src folder to dst folder, 
    if dst folder doesn't exist, create dst,
    if dst folder exists, then will delete the old file under dst and copy new file from src to it.
    '''
    if os.path.exists(src):
        if not os.path.exists(dst):
            shutil.copytree(src, dst)
            print "Copying from %s to %s done."%(src,dst)
        for file in os.listdir(src):
            src_file = os.path.join(src,file)
            if os.path.isfile(src_file):#src is file
                shutil.copy(src_file, dst)
            if os.path.isdir(src_file):#src is folder
                copyfolder(src_file,os.path.join(dst,file))            
    else:
        print "src folder %s doesn't exists"%src
        
    