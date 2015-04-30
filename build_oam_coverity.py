mport sys
import os
sys.path.append('/opt/swe/tools/in/projects/lte_project-1.0/bin/coverityClasses')
from Services import Services
from DefectServices import DefectService
from ConfigurationServices import ConfigurationService
from CoverityActions import CoverityActions
from CoverityActions import FatalException
from CoverityActions import WarningException
from CoverityActions import set_cov_bin
import logging
import traceback
import time
import suds

COV_BIN = None 


# Useful functions.

def start_cs(commitServer, httpPort, userName, userPassword):
	cs = ConfigurationService("http://" + commitServer, httpPort)
	cs.setSecurity(userName, userPassword)
	# print("Configuration Services started...")
	return cs

def start_ds(commitServer, httpPort, userName, userPasswordv):
	ds = DefectService("http://" + commitServer, httpPort)
	ds.setSecurity(userName, userPassword)
	# print("Defects Services started...")
	return ds
    
def notify_error(cs, sendMail, subscriberList, message, covStream):
        global userName
        global hostName
	print (message)
	if sendMail == "on":
                message = str(message)+"<br><i>Run started by "+userName+" on "+hostName+".</i>"
		for subscriber in subscriberList:
			subject = "Coverity status on " + covStream + " stream: UNSUCCESSFUL!"
			cs.notify(subscriber, subject, message)
			
def notify_success(cs, sendMail, subscriberList, message, covStream):
	global userName
	global hostName
	# print (message)
	if sendMail == "on":
		message	= str(message)+"<br><i>Run started by "+userName+" on "+hostName+".</i>"
		for subscriber in subscriberList:
			subject = "Coverity status on " + covStream + " stream"
			cs.notify(subscriber, subject, message)
			
def print_variables(name, value):
	print (name+" "*(20-len(name))+value)
	
def print_option(option, description):
	print ("\t\t"+option+" "*(25-len(option))+description)
	
def make_folder_path(folder):
	if not os.path.isdir(folder):
		os.makedirs(folder)
		
def get_script_name():
	script_path = sys.argv[0]
	script_name = ''
	flag = 0
	for i in script_path:
		if flag:script_name+=i
		if i == '/':
			script_name = ''
			flag=1
	return "./"+script_name
		
def coverityHelp():
	print ("\nUsage:\n %s <coverity_action> <build_options> <other_options>" % (get_script_name()))
	print ("or:\n %s <build_options>\n" % (get_script_name()))
	print("   Where:")
	print ("\t<build_options> are:")
	print("\t\tthe valid options for build_enboamNG.pl script\n")	
	print ("\t<coverity actions> are:")
	print_option("full", "build and analyze with Coverity")
	print_option("clean_config", "clean your compiler configuration")
	print_option("configure", "generates configuration files containing the compilers information")
	print_option("build", "build with Coverity")	
	print_option("analyze", "analyze build results")
	print_option("add_project_and_stream", "add project and stream in Coverity Conect")
	print_option("commit_defects", "commit found defects to the central instance of Coverity Conect")
	print_option("colect_warnings", "collect warnings from last build")
	print_option("generate_report", "generate report from last build")
	print_option("get_ccm_delta","extract CCM differences") 
	print_option("get_defects_delta", "generate report containing the added and removed defects")
	print ("\n\t<other_options> are:")
	print_option("-mode", "mode to be used in the run: dev or stream_guard; default is dev")
	print_option("-commitServer", "machine where the results will be commited; default is the CoverityServer: mrclin79")
	print_option("-commitPort", "port of the machine where the results are commited; default is 9090")
	print_option("-httpPort", "port of the machine where the results are can be seen; default is 8080")
	print_option("-userPassword", "password to be used at commit; default is alcatel1234")	
	print_option("-sendMail", "decide if you want to receive report emails or not; default is on")
	print_option("-subscriberList", "list of users to wich the report will be sent; default is the user that starts the run")
	print_option("-excludeFile", "path to a file containing the sources that have to be removed from CCM computation")
	print_option("-compilerFile", "list of compilers to be used")
	print_option("-fullReport", "used to generate a report file that contains CCM delta and Build Warnings; default is no")
	print_option("-buildBot", "[no/yes] option used for compatibility with buildBot mechanism. Mandatory stream and baseline options are required. Mode will be stream_guard ")
	print_option("-stream", "Stream name.Must be valid CC stream without @/enba_pvob part. Must be used toghether with baseline option")
	print_option("-baseline", "Baseline. Must be used toghether with stream option") 
	print("\nExamples:")
	print ("\t%s configure -p ll133 -t ppc -n -C -J 4 -b eccm2" % get_script_name())
	print ("\t%s full -p ll133 -t ppc -n -C -J 4 -b eccm2" % get_script_name())
	print ("\t%s -p ll133 -t ppc -n -C -J 4 -b eccm2" % get_script_name())
	print ("\t%s -p ll133 -t ppc -n -C -J 4 -b eccm2 -mode stream_guard -commitServer 135.243.29.xyz" % get_script_name())
	print ("\t%s full -p ll133 -t ppc -n -C -J 4 -b eccm2 -subscriberList user1,user2 " % get_script_name())
	print ("\nExit binary code: 0000 succesful; 0001 runtime error; 0010 fatal error; 0100 new defects; 1000 removed defects > new defects. Exit code can be a sum of these values.")

# Measuring execution time of functions
def sec_to_time(var):
    		sec = int(var)

    		days = sec / 86400
    		sec -= 86400 * days

    		hrs = sec / 3600
    		sec -= 3600*hrs
		
    		mins = sec / 60
    		sec -= 60*mins
    		print "Days: %d; Hours: %d; Minutes: %d; Seconds: %d \n"%(days,hrs,mins,sec) 
	
def getTime(func,*extra):
	if len(extra) >= 1:
		start = time.time()
		returnList = func(*extra)
		elapsed = time.time() - start
		print "\nElapsed time is:"
		sec_to_time(elapsed)
		return returnList
	else:
		start = time.time()
		returnList = func()
		elapsed = time.time() - start
		print "\nElapsed time is:"
		sec_to_time(elapsed)
		return returnList

# Init Objects

services = Services()

# Accepted values for global variables
acceptedMode = ["dev", "stream_guard"]
acceptedSendMail = ["on", "off"]
acceptedOptions = ["full", "clean_config", "configure", "add_project_and_stream", "build","analyze","commit_defects", "colect_warnings", "generate_report", "get_ccm", "get_ccm_delta", "test", "get_defects_delta"]
acceptedBuildbot = ["yes", "no"]
# Check usage
if ((len(sys.argv) < 2) or (any(x in sys.argv for x in ["help", "-help", "--help", "-h", "--h"]))):
	coverityHelp()
	sys.exit(2)
else:
	coverityOption, mode, commitServer, commitPort, httpPort, userPassword, sendMail, subscriberList, excludeFile, compilerFile, fullReport, buildScript, buildBot, baseline, stream, buildOptions = services.get_options()

if coverityOption not in acceptedOptions:
	print ("")
	print ("Unknown coverity command: "+coverityOption+"! ")
	print ("")
	coverityHelp()
	sys.exit(2)

# Level 1 variables section ( independent variables )		
userName = services.get_user()
hostName = services.get_hostname()

# Error case
if subscriberList != None:
	
	subscriberList = subscriberList.strip().split(",")
else:
	# Add username to subscriber list if no other user was provided
	subscriberList = []
	subscriberList.append(userName)

if buildBot not in acceptedBuildbot:
        print ("Unknown buildBot option! Accepted options [yes/no]")
        sys.exit(2)

# Remove duplicates
subscriberList = list(set(subscriberList))

# Start CS and DS
cs1 = start_cs(commitServer, httpPort, "checkuser", "alcatel")

for subscriber in subscriberList:
	print "\nChecking database for user "+subscriber+"..."
	if cs1.getUser(subscriber) == None:
		print "User not found! Creating user!"
		try:
		        cs1.createUser(subscriber)
		except suds.WebFault, e:
        		if str(e) ==  "Server raised fault: 'User with user name "+subscriber+" already exists.'":
                		print "User was just created!"
			else:
				print "There was a problem creating subscriber "+subscriber+": ", e
				sys.exit(2)	
	else:
		print "User found!"
	
print "\nAuthentifying with user "+userName+ "..."
cs = start_cs(commitServer, httpPort, userName, userPassword)
ds = start_ds(commitServer, httpPort, userName, userPassword)
print ("...done")

view = services.get_view()

# Treat error cases
if sendMail not in acceptedSendMail:
	notify_error(cs, sendMail, subscriberList, "ERROR: Invalid sendMail option: "+sendMail+"! Accepted sendMail values are: "+", ".join(acceptedSendMail), "undefined")	
	sys.exit(2)

if mode not in acceptedMode:
	notify_error(cs, sendMail, subscriberList, "ERROR: Invalid mode: "+mode+"! Accepted mode values are: "+", ".join(acceptedMode), "undefined")	
	sys.exit(2)

if view == None:
	notify_error(cs, sendMail, subscriberList, "ERROR: No view is mapped!", "undefined")	
	sys.exit(2)


if buildBot == "yes":
        if stream == None or baseline == None:
                notify_error(cs, sendMail, subscriberList, "ERROR: Stream and baseline are mandatory arguments in buildBot option", "undefined")
                sys.exit(2)
	else:
        	mode = "stream_guard"
		baseline = "ignore_"+baseline

if bool(stream == None)!= bool(baseline == None):
        notify_error(cs, sendMail, subscriberList, "ERROR: Stream and baseline are mandatory together!", "undefined")
	sys.exit(2)

# Print level 1 variables 
print ("\nLevel 1 variables: ")	
print_variables("Coverity Option", coverityOption)
print_variables("Mode", mode)
print_variables("Commit Server", commitServer)
print_variables("Commit Port", commitPort)
print_variables("Http Port", httpPort)
print_variables("User Name", userName)
print_variables("User Password", "*********")
print_variables("Send Mail", sendMail)
print_variables("Subscriber List", str(subscriberList))
print_variables("Build Options", buildOptions)
print_variables("View", view)
print_variables("Build Script", buildScript)
	

# Level 2 variables section ( dependent on level 1 variables )
if (buildBot == "yes") or ((stream != None) and (baseline != None)):
	if os.system("cleartool lsstream -s "+stream+"@/enba_pvob")!=0:
		notify_error(cs, sendMail, subscriberList, "ERROR: Cannot find stream "+stream+" in Clearcase!" , "undefined")
		sys.exit(2)
	project, stream, baseline = services.get_cc_details(None, stream, baseline)
else:
	project, stream, baseline  = services.get_cc_details()

# Treat error cases
acceptedProject = ["enb_lr15", "enb_lr143", "enb_lr14"]
if project not in acceptedProject:
        notify_error(cs, sendMail, subscriberList, "ERROR: Invalid project: "+project+"! Accepted project values are: "+", ".join(acceptedProject), "undefined")
        sys.exit(2)
set_cov_bin(project)
if baseline == None:
	notify_error(cs, sendMail, subscriberList, "ERROR: Baseline was not set on your code! Please create a baseline and try again...", "undefined")
	sys.exit(2)

boardType, hardwareType, transmissionType, buildType = services.get_build_configuration(buildOptions)

# Treat error cases
if boardType == None:
	notify_error(cs, sendMail, subscriberList, "ERROR: No board provided!", "undefined")
	sys.exit(2)
	
if hardwareType == None:
	notify_error(cs, sendMail, subscriberList, "ERROR: Hardware type not retrieved! May be caused by invalid/missing board option...", "undefined")
	sys.exit(2)	
	
if buildType == None:
	notify_error(cs, sendMail, subscriberList, "ERROR: Invalid build type! Must be ppc!", "undefined")
	sys.exit(2)
		
# Print level 2 variables
print ("\nLevel 2 variables: ")
print_variables("Project", project)
print_variables("Stream", stream)
print_variables("Baseline", baseline)
print_variables("Hardware Type", hardwareType)
print_variables("Board Type", boardType)
print_variables("Transmission Type", transmissionType)
print_variables("Build Type", buildType)

# Coverity variables section
covProject = "_".join([project, hardwareType, boardType, transmissionType])	
covStream = "_".join([stream, hardwareType, boardType, transmissionType])	
if project == "enb_lr15":
	covSecurityFile = "/opt/swe/local/licenses/prevent/lte/license_700.dat"
	covMetrics = "/output/METRICS.errors.xml"
elif project == "enb_lr14" or project == "enb_lr143":
        covSecurityFile = "/opt/swe/local/licenses/prevent/lte/license_55.dat"
	covMetrics = "/output/METRICS.errors.xml"
else:
        notify_error(cs, sendMail, subscriberList, "ERROR: License and covMetrics file are not defined for project "+project, "undefined")
        sys.exit(2)




covLanguage = "C/C++"


# Print Coverity variables
print ("\nCoverity variables: ")
print_variables("Coverity Project", covProject)
print_variables("Coverity Stream", covStream)
print_variables("Security File", covSecurityFile)
print_variables("Language", covLanguage)


# Coverity path variables section
# Folders
covHomeDir = "/".join(["/local", userName, "_".join([view, hardwareType, boardType, transmissionType])])
covTmpDir = "/".join([covHomeDir, "tmp"])
covLogDir = "/".join([covHomeDir, "log"])
covReportDir = "/".join([covHomeDir, "report"])
covCcmDir = "/".join([covHomeDir, "ccm"])
# Files
covConfigXml = "/".join([covHomeDir, "config/coverity_config.xml"])
covEmitLog = "/".join([covTmpDir, "build-log.txt"])
covReportFile = "/".join([covReportDir, "report_for_"+covProject])
covExportFile = "/".join([covLogDir, "exported_defects.csv"])
covBuildLog = "/".join([covLogDir, "cov_build_for_"+covProject])
covWarningsLog = "/".join([covLogDir, "warnings_for_"+covProject])
covFilteredWarningsLog = "/".join([covLogDir, "warnings_filtered_for_"+covProject])



# Print Coverity path variables
print ("\nCoverity path variables: ")
print_variables("Xml config file", covConfigXml)
print_variables("Emit Log", covEmitLog)
print_variables("Report File", covReportFile)
print_variables("Export File", covExportFile)
print_variables("Build Log", covBuildLog)
print_variables("Warnings Log", covWarningsLog)
print_variables("Filtered Warnings Log", covFilteredWarningsLog)

# Create folder paths
for folder in covHomeDir, covTmpDir, covLogDir, covReportDir, covCcmDir:
	make_folder_path(folder)
	
	

# Main Coverity functionalities 

# Init Coverity Object

coverity = CoverityActions()

# Check Coverity option 

try:
	if coverityOption == "clean_config":
		coverity.clean_config(covHomeDir)
	elif coverityOption == "full":
		getTime(coverity.clean_config, covHomeDir)
		getTime(coverity.cov_configure, covSecurityFile, project, boardType, transmissionType, covConfigXml, compilerFile)
		getTime(coverity.cov_build, buildOptions, covTmpDir, covBuildLog, covConfigXml, buildScript, boardType, transmissionType)
		getTime(coverity.cov_analyze, project, covConfigXml, covTmpDir, covSecurityFile)
		getTime(coverity.add_project_and_stream, covProject, covStream, commitServer, commitPort, userName, userPassword)
		getTime(coverity.cov_commit_defects, baseline, covTmpDir, covStream, userName, userPassword, commitServer, commitPort, covSecurityFile)
		getTime(coverity.colect_warnings, covBuildLog, covWarningsLog, covFilteredWarningsLog)
		
		COVnbNewDefects, COVnbRemovedDefects, COVreport = getTime(coverity.get_defects_delta, cs, ds, mode, covProject, stream, hardwareType, boardType, transmissionType, userName, hostName)
		if fullReport == "yes":	
			getTime(coverity.generate_local_ccm_file, covTmpDir, covCcmDir, baseline, excludeFile, covMetrics)
			CCMmodifiedCounter, CCMremovedCounter, CCMaddedCounter, CCMreportHtml = getTime(coverity.get_ccm_delta, covCcmDir, cs, mode, covProject, stream, hardwareType, boardType, transmissionType)				
			htmlReportLink = getTime(coverity.get_fullHtml_report, COVnbNewDefects, COVnbRemovedDefects, COVreport,CCMmodifiedCounter, CCMremovedCounter, CCMaddedCounter, CCMreportHtml, covWarningsLog, stream, covReportDir, hardwareType, boardType, transmissionType, baseline)
			COVreport = getTime(coverity.insert_htmlReportLink, COVreport, htmlReportLink)
		if sendMail == "on":
			print (subscriberList , " will shortly receive an e-mail with a report on the newly introduced/removed defects... ")
			notify_success(cs, sendMail, subscriberList, COVreport, covStream)
		# Exit code is needed if there are new defects.
		# Value 0000 succesful; 0010 fatal error; 0100 new defects; 1000 removed defects > new defects. 
		exitCode = 0
		if (COVnbNewDefects > 0):
			exitCode += 4
		if (COVnbNewDefects <= COVnbRemovedDefects) and (COVnbNewDefects > 0):
			exitCode += 8		
		sys.exit(exitCode)
			
	elif coverityOption == "configure":
		getTime(coverity.cov_configure, covSecurityFile, project, boardType, transmissionType, covConfigXml, compilerFile)
	elif coverityOption == "build":
		getTime(coverity.cov_build, buildOptions, covTmpDir, covBuildLog,covConfigXml)
	elif coverityOption == "analyze":
		getTime(coverity.cov_analyze, project, covConfigXml, covTmpDir, covSecurityFile)
	elif coverityOption == "commit_defects":
		getTime(coverity.cov_commit_defects, baseline, covTmpDir, covStream, userName, userPassword, commitServer, commitPort, covSecurityFile)
	elif coverityOption == "colect_warnings":
		getTime(coverity.colect_warnings, covBuildLog, covWarningsLog, covFilteredWarningsLog)
	elif coverityOption == "generate_report":
		getTime(coverity.generate_report, covReportFile, covExportFile, covProject, commitServer, httpPort, userName, userPassword)
	elif coverityOption == "add_project_and_stream":
		getTime(coverity.add_project_and_stream, covProject, covStream, commitServer, commitPort, userName, userPassword)
	elif coverityOption == "get_ccm_delta":
		getTime(coverity.generate_local_ccm_file, covTmpDir, covCcmDir, baseline, excludeFile, covMetrics)
		CCMmodifiedCounter, CCMremovedCounter, CCMaddedCounter, CCMreportHtml = getTime(coverity.get_ccm_delta, covCcmDir, cs, mode, covProject, stream, hardwareType, boardType, transmissionType)
	elif coverityOption == "get_defects_delta":
		COVnbNewDefects, COVnbRemovedDefects, COVreport = getTime(coverity.get_defects_delta, cs, ds, mode, covProject, stream, hardwareType, boardType, transmissionType, userName, hostName)
		if sendMail == "on":	
			print (subscriberList , " will shortly receive an e-mail with a report on the newly introduced/removed defects... ")
			notify_success(cs, sendMail, subscriberList, COVreport, covStream)
	elif coverityOption == "help":
		getTime(coverity.coverityHelp)

				
except FatalException, errorMessage:
	notify_error(cs, sendMail, subscriberList, errorMessage, covStream)
	sys.exit(2)
	
except WarningException, errorMessage:
	print errorMessage
	# notify_error(cs, sendMail, userName, errorMessage, covStream)
	# sys.exit(2)

