#!/bin/bash
echo "Get current time"
#current_time=`date -u "+%Y%m%d_%H-%M-%S"`
current_time=${build_start_time}
echo ${current_time}
echo "Judge the folder exist or not,create if not exist."
package_path="/data/program/jenkins_data/userContent/webpay_package_files"
if [ ! -d ${package_path} ]; then
	mkdir ${package_path}
fi
echo "Get the branch infomation..."
branch=`echo ${JOB_NAME}|sed 's/Webpay_//g'|sed 's/_.*$//g'`
if [ ! -d "${package_path}/${branch}" ]; then
	mkdir "${package_path}/${branch}"
fi
if [ ! -d "${package_path}/${branch}/${current_time}" ]; then
	mkdir "${package_path}/${branch}/${current_time}"
fi
echo "Move the jar/war files to the ${package_path}/${branch}/${current_time}."
workspace="/data/program/jenkins_data/jobs/${first_job_name}/workspace"
files=`ls ${workspace}`
for subfile in ${files}
do
  if [ ${scope} = "all" ]; then
    echo ${subfile}
    if [ -d ${workspace}/${subfile} ]; then
      mkdir "${package_path}/${branch}/${current_time}/${subfile}"
      if [ -d ${workspace}/${subfile}/target/ ]; then 
        mv -f ${workspace}/${subfile}/target/*SNAPSHOT.jar ${package_path}/${branch}/${current_time}/${subfile}
        mv -f ${workspace}/${subfile}/target/*.war ${package_path}/${branch}/${current_time}/${subfile}
      else
        mv -f ${workspace}/${subfile}/*/target/*SNAPSHOT.jar ${package_path}/${branch}/${current_time}/${subfile}
        mv -f ${workspace}/${subfile}/*/target/*.war ${package_path}/${branch}/${current_time}/${subfile}
      fi    
    fi
  fi
if [ ${scope} = "${subfile}" ]; then
  echo ${subfile}
  if [ -d ${workspace}/${subfile} ]; then
    mkdir "${package_path}/${branch}/${current_time}/${subfile}"
    if [ -d ${workspace}/${subfile}/target/ ]; then 
      mv -f ${workspace}/${subfile}/target/*SNAPSHOT.jar ${package_path}/${branch}/${current_time}/${subfile}
      mv -f ${workspace}/${subfile}/target/*.war ${package_path}/${branch}/${current_time}/${subfile}
    else
      mv -f ${workspace}/${subfile}/*/target/*SNAPSHOT.jar ${package_path}/${branch}/${current_time}/${subfile}
      mv -f ${workspace}/${subfile}/*/target/*.war ${package_path}/${branch}/${current_time}/${subfile}
    fi    
  fi
fi
done
echo "==============Package files are stored on master userContent package folder=============="