from splinter import Browser
import siteExtractor as extractor
import argparse
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
from pprint import pprint
import argparse
import operator
import os
import validators
import time

def submitForm(url, browser, password, passFormName, submitFormName):
	browser.visit(url)
	browser.find_by_name(passFormName).first.fill(password)
	browser.find_by_name(submitFormName).first.click()
	formHTML = browser.html
	return formHTML

def text2links(inputText, findVal):
	infoList = []

	for link in BeautifulSoup(inputText, parse_only=SoupStrainer("a"), features="html.parser"):
	    if link.has_attr("href"):
	        if findVal in link["href"]:
	        	infoList.append(link["href"])

	#remove all args in future. Maybe implement.
	'''
	if args["separator"]:
		urlList = infoList
		infoList = []
		for link in urlList:
			if args["separator"] in link:
				head, sep, tail = link.partition(args["separator"])
				infoList.append(tail)
	'''

	return infoList


def main(args):
	inputURLs = extractor.toList(args["input"])
	browser = Browser()
	for url in inputURLs:
		rawHTML = submitForm(url, browser, args["password"], "Pass1", "Submit0")
		print(text2links(rawHTML, args["find"]))
	browser.quit()


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", required=True, help="Input url.")
	parser.add_argument("-p", "--password", required=True, help="Input password.")
	parser.add_argument("-o", "--output", required=False, help="""Outputs list of urls 
		or info in text file. Will use input folder if unspecified, or output to console.""")
	parser.add_argument("-f", "--find", required=True, help="Finds links containing string.")
	'''parser.add_argument("-s", "--separator", required=False, help="""Finds useful information 
		after separator e.g. unencrypted site files.""")'''
	args = vars(parser.parse_args())

	main(args)