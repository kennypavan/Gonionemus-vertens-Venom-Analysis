
# Gonionemus vertens
Venomics and transcriptome analysis pipeline and corresponding data. <br><br>

## Raw Data
Mi-Seq raw fq paired data can be downloaded from the following links. Two distinct Mi-Seq runs were performed on 5 individual GV samples resulting in 10 pairs of forward and reverse reads. The individual reads were then concatenated into holistic forward and reverse files which can be downloaded below.  

<a href="http://gaynorlab.com/cq/gv/MV-ALL-R1.fastq.gz" target="_blank">Forward</a> - (5.3 Gb)

<a href="http://gaynorlab.com/cq/gv/MV-ALL-R2.fastq.gz" target="_blank">Reverse</a> - (7.1 Gb)

<br>

## Analysis Reproduction Steps
The results of this analysis are reproducible by following the steps below. <br><br>


1. Install the project prerequisite dependencies Docker, Fastqc, and Python3. 

2. Download raw data Mi-Seq data files.

3. Perform FASTQC on both files.
	```
	fastqc MV-ALL-R1.fastq.gz
	fastqc MV-ALL-R2.fastq.gz
	```

4. Perform De Novo Assembly using Trinity.

	4a. Pull the Trinity Docker image.

	```
	docker pull trinityrnaseq/trinityrnaseq
	```
	
	4b. Run the Trinity command below.

	```
	docker run --rm -v `pwd`:`pwd` trinityrnaseq/trinityrnaseq Trinity \ 
	--seqType fq \
	--left `pwd`/MV-ALL-R1.fastq.gz \ 
	--right `pwd`/MV-ALL-R2.fastq.gz \ 
	--CPU 59 \ 
	--max_memory 50G \ 
	--trimmomatic \ 
	--quality_trimming_params \ "ILLUMINACLIP:$TRIMMOMATIC_DIR/adapters/TruSeq3-PE.fa:2:30:10 SLIDINGWINDOW:4:3 LEADING:5 TRAILING:5 MINLEN:25"  \
	--output `pwd`/trinity_out_dir > output.txt & 
	```

	4c. Generate an assembly stats report.

	```
	sudo docker run -v `pwd`:`pwd` trinityrnaseq/trinityrnaseq /usr/local/bin/util/TrinityStats.pl `pwd`/Trinity.fasta > stats.txt
	```

5. Perform FASTQC on trimmed reads.
6. Estimate Transcript Abundance.
7. Build Expression Matrix.
8. Count the Numbers of Expressed Transcripts.
9. Perform BLASTx via Diamond against the NR database.
 

	9a. Add TPM expression values to results file using MergeBlastTPM python script.

	9b. Annotate the results 


10. Perform BLASTx via Diamond against the Uniprot Toxin and Venom Database. 


	10a. Add TPM expression values to results file using MergeBlastTPM python script.
	
	10b. Annotate the results


11. Filter based on expression values
