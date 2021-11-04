import os
import csv
import time
import urllib.parse
import urllib.request
import requests
import sys
import json

#maps embl to uniprot and saves
def MapIDs():

	matchURL = 'https://www.uniprot.org/uploadlists/'
	file = open("Data/All/BLASTx_NR/diamond-out-with-tpm.txt",'r')
	lines = csv.reader(file, delimiter='\t')

	query = ''
	count = 1
	overallCount = 1
	matchedResults = {}

	for line in lines:

		embl_id = line[1]
		query = query + embl_id + " "

		# chunks 
		if count % 5000 == 0:
			
			params = {
				'from': 'EMBL',
				'to': 'ID',
				'format': 'tab',
				'query': query
			}

			data = urllib.parse.urlencode(params)
			data = data.encode('utf-8')
			req = urllib.request.Request(matchURL, data)

			with urllib.request.urlopen(req) as f:
				next(f) #skip line 1 in response
				for singleLine in f:
					embl_id = singleLine.decode('utf-8').rstrip().split("\t")[0]
					uniprot_id = singleLine.decode('utf-8').rstrip().split("\t")[1]
					matchedResults[embl_id] = uniprot_id
					print (embl_id+" - "+uniprot_id)

			query = ""
			count = 1
			time.sleep(0.5) #respect api rates
			print(overallCount)
			
		count = count + 1
		overallCount = overallCount + 1

	file.close()

	#open old file and create new file
	newFile= open("Data/All/BLASTx_NR/diamond-out-with-tpm-uniprot.txt","w+")
	file = open("Data/All/BLASTx_NR/diamond-out-with-tpm.txt",'r')
	lines = csv.reader(file, delimiter='\t')
		
	for line in lines:
		if line[1] in matchedResults.keys():
			line[1] = "sp|"+matchedResults[line[1]]+"|"+line[1] #keeping with format in toxin results file.
			newFile.write("\t".join(line)+"\n")

	newFile.close()
	file.close()


def annotationSearch(productID):
	
	searchUrl = 'https://www.ebi.ac.uk/QuickGO/services/annotation/search?limit=100&includeFields=goName&includeFields=taxonName&includeFields=name&geneProductId='+productID
	response = requests.get(searchUrl, headers={ "Accept" : "application/json"})

	if response.ok:
		responseBody = json.loads(response.text)
		for result in responseBody["results"]:
			print(result["symbol"]+": \n\t"+result["goName"]+" \n\t"+ result["goId"]+" \n\t"+ result["goAspect"]+" \n\t"+ result["taxonName"]+" \n\t"+ result["name"]+" \n\t"+ result["assignedBy"])


def annotateToxins():
	return None


def annotateTranscriptome():
	return None





if __name__ == '__main__':

	#~30 seconds for every 5000 blast hits. Uncomment to run
	# MapIDs() 

	annotationSearch("Q75WF2")