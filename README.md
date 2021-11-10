

# Gonionemus vertens
Venomics and transcriptome analysis pipeline and corresponding data. <br><br>

## Raw Data
Mi-Seq raw fq paired data can be downloaded from the following links. Two distinct Mi-Seq runs were performed on 5 individual GV samples resulting in 10 pairs of forward and reverse reads. The individual reads were then concatenated into holistic forward and reverse files which can be downloaded below.  

<a href="http://gaynorlab.com/cq/gv/MV-ALL-R1.fastq.gz" target="_blank">Forward</a> - (5.3 Gb)

<a href="http://gaynorlab.com/cq/gv/MV-ALL-R2.fastq.gz" target="_blank">Reverse</a> - (7.1 Gb)

<br>

## Analysis Reproduction Steps
The results of this analysis are reproducible by following the steps below. <br><br>


1. Install the project prerequisite dependencies Docker, Fastqc, R, and Python3. 

2. Download raw data Mi-Seq data files from the links above.

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
	sudo docker run -v `pwd`:`pwd` trinityrnaseq/trinityrnaseq /usr/local/bin/util/TrinityStats.pl \
	`pwd`/Trinity.fasta > stats.txt
	```

5. Perform FASTQC on trimmed reads. (found in the trinity_out directory)
	```
	fastqc [trimmed-reads-filename.fasta.gz]
	```

6. Estimate Transcript Abundance.
	```
	docker run -v `pwd`:`pwd` trinityrnaseq/trinityrnaseq /usr/local/bin/util/align_and_estimate_abundance.pl \
	--transcripts `pwd`/Trinity.fasta \
	--seqType fq \
	--left `pwd`/MV-ALL-R1.fastq.gz \
	--right `pwd`/MV-ALL-R2.fastq.gz \
	--est_method RSEM \
	--aln_method bowtie \
	--trinity_mode \
	--prep_reference \
	--thread_count 59 \
	--output_dir `pwd`/rsem_outdir
	```

7. Build Expression Matrix.
	```
	docker run -v `pwd`:`pwd` trinityrnaseq/trinityrnaseq /usr/local/bin/util/abundance_estimates_to_matrix.pl  \
	--gene_trans_map `pwd`/Trinity.fasta.gene_trans_map  \
	--est_method RSEM  \
	--out_prefix `pwd`/all \
	--name_sample_by_basedir \
	`pwd`/rsem_outdir/RSEM.isoforms.results
	```

8. Count the Numbers of Expressed Transcripts.
	
	8a. Create a counts file.
	``` 
	docker run -v `pwd`:`pwd` trinityrnaseq/trinityrnaseq /usr/local/bin/util/misc/count_matrix_features_given_MIN_TPM_threshold.pl \
	`pwd`/all.gene.TPM.not_cross_norm | tee `pwd`/all.gene.TPM.not_cross_norm.counts_by_min_TPM
	```

	8b. Generate a plot of the counts.
	```
	> R
	> data = read.table("all.gene.TPM.not_cross_norm.counts_by_min_TPM", header=T)
	> plot(data, xlim=c(-100,0), ylim=c(0,100000), t='b')

	```

9. Perform BLASTx via Diamond against the NR database.
 

	9a. Add TPM expression values to results file using MergeBlastTPM python script. (python3 MergeBlastTPM.py --help for options)
	```
	python3 MergeBlastTPM.py \
	-b Data/All/BLASTx_NR/diamond-out.txt \
	-t Data/All/Matrix/all.isoform.TPM.not_cross_norm -o Data/All/BLASTx_NR/diamond-out-with-tpm.txt
	```

	9b. Annotate the results 


10. Perform BLASTx via Diamond against the Uniprot Toxin and Venom Database. 


	10a. Add TPM expression values to results file using MergeBlastTPM python script. (python3 MergeBlastTPM.py --help for options)
	```
	python3 MergeBlastTPM.py \
	-b Data/All/BLASTx_ToxinProt/diamond-toxin-out.txt \
	-t Data/All/Matrix/all.isoform.TPM.not_cross_norm -o Data/All/BLASTx_ToxinProt/diamond-toxin-out-with-tpm.txt
	```

	10b. Annotate the results


11. Filter based on expression values using awk. TPM >= 1. 	
	```
	#list
	awk '{ if ($13 >= 1) { print } }' FS='\t' diamond-toxin-out-with-tpm.txt
	
	#count
	awk '{ if ($13 >= 1) { print } }' FS='\t' diamond-toxin-out-with-tpm.txt | wc -l
	```

12. Import nr db results to SQL database.

13. Create toxin db with the structure below, then import data using sql load file function directly from toxin flat files.
	```sql
	--
	-- Table structure for table `annotation_results`
	--

	CREATE TABLE `annotation_results` (
	  `id` int(12) NOT NULL,
	  `qseqid` varchar(32) DEFAULT NULL,
	  `symbol` varchar(16) DEFAULT NULL,
	  `go_name` varchar(128) DEFAULT NULL,
	  `go_id` varchar(32) DEFAULT NULL,
	  `go_aspect` varchar(32) DEFAULT NULL,
	  `taxon_name` varchar(64) DEFAULT NULL,
	  `name` varchar(128) DEFAULT NULL,
	  `assigned_by` varchar(16) DEFAULT NULL
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	-- --------------------------------------------------------

	--
	-- Table structure for table `blast_results`
	--

	CREATE TABLE `blast_results` (
	  `id` int(12) NOT NULL,
	  `qseqid` varchar(32) DEFAULT NULL,
	  `symbol` varchar(32) DEFAULT NULL,
	  `sseqid` varchar(64) DEFAULT NULL,
	  `pident` float DEFAULT NULL,
	  `length` int(5) DEFAULT NULL,
	  `mismatch` int(5) DEFAULT NULL,
	  `gapopen` int(5) DEFAULT NULL,
	  `qstart` int(5) DEFAULT NULL,
	  `qend` int(5) DEFAULT NULL,
	  `sstart` int(5) DEFAULT NULL,
	  `send` int(5) DEFAULT NULL,
	  `evalue` double DEFAULT NULL,
	  `bitscore` int(5) DEFAULT NULL,
	  `tpm` float DEFAULT NULL
	) ENGINE=InnoDB DEFAULT CHARSET=latin1;

	--
	-- Indexes for table `annotation_results`
	--
	ALTER TABLE `annotation_results`
	  ADD PRIMARY KEY (`id`),
	  ADD KEY `qseqid` (`qseqid`),
	  ADD KEY `symbol` (`symbol`),
	  ADD KEY `go_name` (`go_name`),
	  ADD KEY `go_aspect` (`go_aspect`),
	  ADD KEY `name` (`name`);

	--
	-- Indexes for table `blast_results`
	--
	ALTER TABLE `blast_results`
	  ADD PRIMARY KEY (`id`),
	  ADD KEY `qseqid` (`qseqid`),
	  ADD KEY `tpm` (`tpm`),
	  ADD KEY `evalue` (`evalue`),
	  ADD KEY `pident` (`pident`),
	  ADD KEY `sseqid` (`sseqid`),
	  ADD KEY `bitscore` (`bitscore`),
	  ADD KEY `length` (`length`),
	  ADD KEY `symbol` (`symbol`);
	
	```

14. Filter by expression, GO, eval, etc...

15. Generate figures.


<br>

<br>

<br>


## ToxProt Results

| Metric | Total | Query |
|--|--|--|
| Total BLAST Hits| 10896 | ```SELECT COUNT(qseqid) FROM blast_results``` |
| Total BLAST Hits TPM >= 1| 3836 | ```SELECT COUNT(qseqid) FROM blast_results WHERE TPM >= 1``` |
| IsoForm Transcripts| 1415 | ```SELECT COUNT(DISTINCT(qseqid)) FROM blast_results``` |
| IsoForm Transcripts TPM >= 1| 478 | ```SELECT COUNT(DISTINCT(qseqid)) FROM blast_results WHERE TPM >= 1``` |
| Unique Transcripts| 493 | ```SELECT COUNT(DISTINCT(qseqid_unique)) FROM blast_results``` |
| Unique Transcripts TPM >= 1| 311 | ```SELECT COUNT(DISTINCT(qseqid_unique)) FROM blast_results WHERE TPM >= 1``` |
| Venomix Toxin Groups| --- |  |



<br>

<br>

<br>

## In Progress

```sql

#IsoForm Best by Evalue
SELECT * from blast_results AS A WHERE A.tpm>=1 
AND A.evalue = (SELECT evalue FROM blast_results WHERE qseqid=A.qseqid ORDER BY evalue DESC LIMIT 1)

#IsoForm Best matches
SELECT *, count(qseqid) as transcript_count from blast_results AS A 
WHERE A.evalue = (SELECT evalue FROM blast_results WHERE qseqid=A.qseqid ORDER BY evalue DESC LIMIT 1) 
AND A.tpm>=1 GROUP BY qseqid ORDER BY tpm DESC;


#Best by Evalue
SELECT * from blast_results AS A WHERE A.tpm>=1 
AND A.evalue = (SELECT evalue FROM blast_results WHERE qseqid_unique=A.qseqid_unique ORDER BY evalue DESC LIMIT 1)

#Best matches
SELECT *, count(qseqid_unique) as transcript_count FROM blast_results AS A 
WHERE A.evalue = (SELECT evalue FROM blast_results WHERE qseqid_unique=A.qseqid_unique ORDER BY evalue DESC LIMIT 1) 
AND A.tpm>=1 GROUP BY qseqid_unique ORDER BY tpm DESC;


```

