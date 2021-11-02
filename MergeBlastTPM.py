import os
import argparse
import csv

# dictonary to store TPM results
TPMResults = {}

# Opens the blastx fasta file
def openBlastFile(blastFile,outputFile):
    file = open(blastFile,'r')
    lines = csv.reader(file, delimiter='\t')
    newFile= open(outputFile,"w+")
    for row in lines:
        isoFormID = row[0]
        if isoFormID in TPMResults:
            newFile.write("\t".join(row)+"\t"+TPMResults[isoFormID]+"\n")
    newFile.close()
    print(outputFile + " created successfully")


# Opens the TPM file and adds to TPMResults
def openTPMFile(TPMFile):
    file = open(TPMFile,'r')
    lines = csv.reader(file, delimiter='\t')
    for row in lines:
        TPMResults[row[0]] = row[1]

if __name__ == '__main__':

    # require arguments
    parser = argparse.ArgumentParser(description='Merge BLAST file with TPM file.')
    requiredNamed = parser.add_argument_group('required arguments')
    requiredNamed.add_argument('-t','--tpm_file', type=open,  help='\t\tTPM file path', required=True)
    requiredNamed.add_argument('-b','--blast_file', type=open,  help='\t\tBLAST file path', required=True)
    requiredNamed.add_argument('-o','--out_file', type=ascii,  help='\t\tThe name of the newly created file', required=True)
    args = parser.parse_args()

    # confirm user entered correct args
    if args.tpm_file.name and args.blast_file.name:
        openTPMFile(args.tpm_file.name)
        openBlastFile(args.blast_file.name, args.out_file.replace("'",""))
    else:
        print('error: please see usage -h')
