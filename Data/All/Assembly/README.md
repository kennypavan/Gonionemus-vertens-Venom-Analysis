# Assembly Instructions
Server should have >150gb of free HD space, >=50gb RAM, and 60 CPUs to perform this task adequately. It's possibly to perform with more or less resources; however, please modify the Trinity parameters in step 3 to reflect your resources.

1. Install Docker — Method highly dependent on OS. 

2. Pull the Trinity Docker image

	```docker pull trinityrnaseq/trinityrnaseq```
	
3. Run the Trinity command below

	```docker run --rm -v `pwd`:`pwd` trinityrnaseq/trinityrnaseq Trinity --seqType fq --left `pwd`/MV-ALL-R1.fastq.gz --right `pwd`/MV-ALL-R2.fastq.gz --CPU 59 --max_memory 50G --trimmomatic --quality_trimming_params "ILLUMINACLIP:$TRIMMOMATIC_DIR/adapters/TruSeq3-PE.fa:2:30:10 SLIDINGWINDOW:4:3 LEADING:5 TRAILING:5 MINLEN:25" --output `pwd`/trinity_out_dir > output.txt & ```
