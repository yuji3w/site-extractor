import httplib2
from bs4 import BeautifulSoup, SoupStrainer
from pprint import pprint
import argparse
import operator
import os
import validators
import re



def returnInfo(url, find, seperator = False):
	http = httplib2.Http()
	status, response = http.request(url)

	infoList = []

	for link in BeautifulSoup(response, parse_only=SoupStrainer("a"), features="html.parser"):
	    if link.has_attr("href"):
	        if find in link["href"]:
	        	infoList.append(link["href"])

	#remove all args in future
	if seperator:
		urlList = infoList
		infoList = []
		for link in urlList:
			if seperator in link:
				head, sep, tail = link.partition(seperator)
				infoList.append(tail)

	if not infoList:
		#if it's empty
		print("It's empty.")
		print(response)

	return infoList


def returnImg(url):
	#For images
	http = httplib2.Http()
	status, response = http.request(url)

	infoList = []

	for link in BeautifulSoup(response, parse_only=SoupStrainer("img"), features="html.parser"):
		if "src" in link:
			if args["find"] in link["src"]:
				infoList.append(link["src"])

	if not infoList:
		urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', str(response))
		for link in urls:
			if args["find"] in link:
				infoList.append(link)
		#last ditch effort to capture all matches.

	#remove all args in future
	if args["separator"]:
		urlList = infoList
		infoList = []
		for link in urlList:
			if args["separator"] in link:
				head, sep, tail = link.partition(args["separator"])
				infoList.append(tail)

	if not infoList:
		#if it's empty
		print("It's empty.")
		print(response)

	return infoList


def returnInfo2(url):
	#This is legacy.
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

	if not infoList:
		#if it's empty
		print("It's empty.")
		print(response)

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
		for outputurl in returnImg(inputurl):#hack for now, will change later
			outputText.write(outputurl + "\n")
		outputText.write("\n\n")

def main(args):

	inputText = args["input"]
	if not validators.url(inputText):
		parseText(inputText, args["output"])
	else:
		for outputurl in returnInfo2(inputText):
				print(outputurl)

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