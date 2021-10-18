# FASTQC Instructions
Perform this step pre and post trim.

1. Download MV forward and reverse reads server.

2. Install FASTQC. If using apt, the install will be as follows:

	```apt-get install -y fastqc```
	
3. Run the FASTQC command for each file. (forward and reverse; pre and post trim)

	```fastqc  MV-ALL-R1.fastq.gz```
	```fastqc  MV-ALL-R2.fastq.gz```

4. Examine html output by opening the html generated files in any web browser. 