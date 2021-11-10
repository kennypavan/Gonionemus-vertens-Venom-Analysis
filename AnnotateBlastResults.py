import os
import csv
import time
import urllib.parse
import urllib.request
import requests
import sys
import json

def annotationSearch(productID,transcriptID):
	
	searchUrl = 'https://www.ebi.ac.uk/QuickGO/services/annotation/search?limit=100&includeFields=goName&includeFields=taxonName&includeFields=name&geneProductId='+productID
	response = requests.get(searchUrl, headers={ "Accept" : "application/json"})
	fullResponse="";

	if response.ok:
		responseBody = json.loads(response.text)
		for result in responseBody["results"]:
			fullResponse += transcriptID+"\t"+result["symbol"]+"\t"+result["goName"]+"\t"+ result["goId"]+"\t"+ result["goAspect"]+"\t"+ result["taxonName"]+"\t"+ result["name"]+"\t"+ result["assignedBy"]+"\n"

	return fullResponse

def annotateToxins():
	file = open("Data/All/BLASTx_ToxinProt/diamond-toxin-out-with-tpm.txt",'r')
	lines = csv.reader(file, delimiter='\t')
	annotationFile = open("Data/All/BLASTx_ToxinProt/toxin-annotations.txt", "a")  # append mode

	for line in lines:		
		annotationFile.write(annotationSearch(line[1].split('|')[1],line[0]))

	annotationFile.close()
	print("done")


if __name__ == '__main__':

	annotateToxins() 
