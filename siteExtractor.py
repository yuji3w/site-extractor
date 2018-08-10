import httplib2
from bs4 import BeautifulSoup, SoupStrainer
from pprint import pprint
import argparse
import operator
import os
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True, help="Input list of urls in text file.")
parser.add_argument("-o", "--output", required=False, help="""Outputs list of urls 
	or info in text file. Will use input folder if unspecified.""")
parser.add_argument("-f", "--find", required=True, help="Finds links containing string.")
parser.add_argument("-s", "--separator", required=False, help="""Finds useful information 
	after separator e.g. unencrypted site files.""")
args = vars(parser.parse_args())

inputText = open(args["input"],"r")
inputText = inputText.read().splitlines()
outputText = open(args["output"],"w+") if args["output"] else open(
	os.path.join(os.path.dirname(args["input"]),"outputInfo.txt"),"w+")


def returnInfo(url):
	http = httplib2.Http()
	status, response = http.request(url)

	infoList = []

	for link in BeautifulSoup(response, parse_only=SoupStrainer("a"), features="html.parser"):
	    if link.has_attr("href"):
	        if args["find"] in link["href"]:
	        	infoList.append(link["href"])

	if args["separator"]:
		urlList = infoList
		infoList = []
		for link in urlList:
			if args["separator"] in link:
				head, sep, tail = link.partition(args["separator"])
				infoList.append(tail)

	return infoList

for inputurl in inputText:
	for outputurl in returnInfo(inputurl):
		outputText.write(outputurl + "\n")
	outputText.write("\n\n")
