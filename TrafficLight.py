import json
import sys
import urllib2
import time
import serial
import jenkins
# Configurations
ping_server = 30
ser = serial.Serial('COM10', 9600)
# Arduino Configuration
SUCCESS = 'b'
FAILURE = 'r'
BUILDING = 'a'
UNSTABLE = 'y'
SUCCESS2 = 'n'
FAILURE2 = 'd'
BUILDING2 = 'm'
UNSTABLE2 = 'l'
time.sleep(5)
def get_status(jobName, jenkinsUrl):
    buildStatusJson = None
    try:
        jenkinsStream = urllib2.urlopen( jenkinsUrl + jobName + "/lastBuild/api/json" )
    except:
        print "      (job name [" + jobName + "] error)"
    try:
        buildStatusJson = json.load(jenkinsStream)
    except:
        print "Failed to parse json"
    if buildStatusJson is None:
        return None
    else:
        return jobName,buildStatusJson["timestamp"], buildStatusJson["result"],
def get_status2(jobName, jenkinsUrl):
	lastBuild = None
	lastSuccess = None
	try:
		server = jenkins.Jenkins(jenkinsUrl, username='radit.pan', password='Y05SK7uSvzAK')
		jobInfo = server.get_job_info(jobName)
		lastBuild = jobInfo['lastBuild']['number']
		lastSuccess = jobInfo['lastSuccessfulBuild']['number']
	except:
		print "      (job name [" + jobName + "] error)"
	if lastBuild == lastSuccess and lastSuccess != None:
		return "SUCCESS"
	else:
		return "FAILURE"
while(1):
	status = get_status("robot-smoke-test-alpha", "http://kiosk-robot:8081/job/")
#        print status[0], status[2]
	if status is not None:
		if status[2] == "UNSTABLE":
			ser.write(UNSTABLE)
		elif status[2] == "SUCCESS":
			ser.write(SUCCESS)
		elif status[2] == "FAILURE":
			ser.write(FAILURE)
		elif status[2] is None:
			ser.write(BUILDING)

	status_processor = get_status2("alpha_kiosk-processor_build", "http://10.161.224.27:8080/")
#        print status[0], status[2]
	if status_processor is not None:
		if status_processor == "UNSTABLE":
			ser.write(UNSTABLE2)
		elif status_processor == "SUCCESS":
			ser.write(SUCCESS2)
		elif status_processor == "FAILURE":
			ser.write(FAILURE2)
		elif status_processor is None:
			ser.write(BUILDING2)
		
	
	time.sleep(ping_server)