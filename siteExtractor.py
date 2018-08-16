import httplib2
from bs4 import BeautifulSoup, SoupStrainer
from pprint import pprint
import argparse
import operator
import os
import validators


def returnInfo(url):
	http = httplib2.Http()
	status, response = http.request(url)

	infoList = []

	for link in BeautifulSoup(response, parse_only=SoupStrainer("a"), features="html.parser"):
	    if link.has_attr("href"):
	        if args["find"] in link["href"]:
	        	infoList.append(link["href"])

	#remove all args in future
	if args["separator"]:
		urlList = infoList
		infoList = []
		for link in urlList:
			if args["separator"] in link:
				head, sep, tail = link.partition(args["separator"])
				infoList.append(tail)

	return infoList

def toList(inputText):
	urlList = []
	if not validators.url(inputText):
		inputDir = inputText
		inputText = open(inputText,"r")
		inputText = inputText.read().splitlines()
		for inputurl in inputText:
			urlList.append(inputurl)
	else:
		urlList.append(inputText)
	return urlList

def parseText(inputText, outputText):
	inputDir = inputText
	inputText = open(inputText,"r")
	inputText = inputText.read().splitlines()
	outputText = open(outputText,"w+") if outputText else open(
		os.path.join(os.path.dirname(inputDir),"outputInfo.txt"),"w+")
	for inputurl in inputText:
		for outputurl in returnInfo(inputurl):
			outputText.write(outputurl + "\n")
		outputText.write("\n\n")

def main(args):

	inputText = args["input"]
	if not validators.url(inputText):
		parseText(inputText, args["output"])
	else:
		for outputurl in returnInfo(inputText):
				print(outputurl + "\n")

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", required=True, help="Input list of urls in text file or url.")
	parser.add_argument("-o", "--output", required=False, help="""Outputs list of urls 
		or info in text file. Will use input folder if unspecified, or output to console.""")
	parser.add_argument("-f", "--find", required=True, help="Finds links containing string.")
	parser.add_argument("-s", "--separator", required=False, help="""Finds useful information 
		after separator e.g. unencrypted site files.""")
	args = vars(parser.parse_args())

	main(args)