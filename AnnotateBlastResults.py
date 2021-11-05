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
	go = 0 

	for line in lines:
		if line[0] == "TRINITY_DN3288_c1_g1_i6":
			go = 1
		
		if go == 1:
			annotationFile.write(annotationSearch(line[1].split('|')[1],line[0]))
			print(line[0]+":"+str(go))

	annotationFile.close()
	print("done")


def annotateTranscriptome():
	file = open("Data/All/BLASTx_NR/diamond-out-with-tpm.txt",'r')
	lines = csv.reader(file, delimiter='\t')
	
	annotationFile = open("Data/All/BLASTx_NR/NR-annotations.txt", "a")  # append mode

	#only annotate with TPM >=1
	for line in lines:
		annotationFile.write(annotationSearch(line[1].split('|')[1],line[0]))

	annotationFile.close()
	print("done")



if __name__ == '__main__':

	#~30 seconds for every 5000 blast hits. Uncomment to run
	# MapIDs() 

	# Uncomment to run
	# annotateToxins() 

	# Uncomment to run
	# annotateTranscriptome() 

