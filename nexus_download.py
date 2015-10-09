#!/usr/bin/env python2.7
 
 
__author__    = 'Bruno Bonfils, <bbonfils@opencsi.com>'
__copyright__ = "OpenCSI, Bruno Bonfils"
__licence__   = "LGPL"
__version__   = 0.1
 
 
"""
A Script to download the given version (or LATEST is no one is provided)
"""
import libxml2
import sys
import urllib
from optparse import OptionParser
import logging
 
args_options = OptionParser()
 
args_options.add_option("-g", "--group-id", dest="groupid", help="group id")
args_options.add_option("-a", "--artifact-id", dest="artifactid", help="artifact id")
args_options.add_option("-v", "--version", dest="version", help="version of artifact", default="LATEST")
args_options.add_option("-r", "--repository", dest="repository", help="Nexus repository name", default="snapshots")
args_options.add_option("-p", "--packaging", dest="packaging", help="packaging (jar, war, etc.)", default="jar")
args_options.add_option("-s", "--nexus-url", dest="server", help="nexus server")
args_options.add_option("-d", "--debug", action="store_true", dest="debug", help="Enable debugging", default=False)
 
(options, args) = args_options.parse_args()
 
if options.groupid is None or options.artifactid is None or options.repository is None or options.server is None:
    print >> sys.stderr, "At least one required option is missing"
    sys.exit(1)
 
if options.debug:
    logging.basicConfig(level=logging.DEBUG)
 
nexusQueryURL = options.server + "/service/local/artifact/maven/resolve" + \
                "?g=" + options.groupid + \
                "&a=" + options.artifactid + \
                "&v=" + options.version + \
                "&r=" + options.repository + \
                "&p=" + options.packaging
 
logging.debug("Performing request on URL: " + nexusQueryURL)
nexusAnswer = urllib.urlopen(nexusQueryURL)
 
""" TODO: improve error management """
try:
    nexusDOM = libxml2.parseDoc("".join(nexusAnswer.readlines())).xpathNewContext()
except libxml2.parserError as exception:
    logging.error("Unable to parse response")
    sys.exit(2)
 
if nexusAnswer.getcode() != 200:
    logging.error("Return code: " + str(nexusAnswer.getcode()))
    logging.debug("HTTP response: \n" + "".join(nexusAnswer.readlines()))
 
artifactURL = nexusDOM.xpathEval("//data/repositoryPath/text()[1]")[0]
fileName = str(artifactURL).split("/")[-1]
urllib.urlretrieve(options.server + "/service/local/repositories/" + options.repository + "/content" + str(artifactURL),
                   filename=fileName)
