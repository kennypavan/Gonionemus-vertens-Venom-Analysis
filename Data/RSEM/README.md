# Estimating Transcript Abundance

1. Install Docker — Method highly dependent on OS. 

2. Pull the Trinity Docker image

	```docker pull trinityrnaseq/trinityrnaseq```
	
3. Run the Trinity command below

	```docker run -v `pwd`:`pwd` trinityrnaseq/trinityrnaseq /usr/local/bin/util/align_and_estimate_abundance.pl  --transcripts `pwd`/Trinity.fasta --seqType fq --left `pwd`/MV-ALL-R1.fastq.gz --right `pwd`/MV-ALL-R2.fastq.gz --est_method RSEM --aln_method bowtie --trinity_mode --prep_reference --thread_count 59 --output_dir `pwd`/rsem_outdir```
