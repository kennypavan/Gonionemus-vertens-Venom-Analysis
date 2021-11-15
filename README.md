



# Gonionemus vertens Venom and Toxin Analysis
Pipeline and corresponding data. <br><br>

## Raw Data
Mi-Seq raw fq paired data can be downloaded from the following links. Two distinct Mi-Seq runs were performed on 5 individual GV samples resulting in 10 pairs of forward and reverse reads. The individual reads were then concatenated into holistic forward and reverse files which can be downloaded below.  

<a href="http://gaynorlab.com/cq/gv/MV-ALL-R1.fastq.gz" target="_blank">Forward</a> - (5.3 Gb)

<a href="http://gaynorlab.com/cq/gv/MV-ALL-R2.fastq.gz" target="_blank">Reverse</a> - (7.1 Gb)

<br>

## Analysis Reproduction Steps
The results of this analysis are reproducible by following the steps below. <br><br>


1. Install the project prerequisite dependencies Docker, Fastqc, R, MYSQL, and Python3. *Depending on your OS, this process can vary. Please search the proper commands for your OS.*


2. Download raw data Mi-Seq data files from the links above.
	```
	wget http://gaynorlab.com/cq/gv/MV-ALL-R1.fastq.gz
	wget http://gaynorlab.com/cq/gv/MV-ALL-R2.fastq.gz
	```

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

9. Perform BLASTx via Diamond against the Uniprot Toxin and Venom Database. 


	9a. Download Venom and Toxin database 
	```
	wget https://www.uniprot.org/uniprot/?query=taxonomy%3A%22Metazoa+[33208]%22+and+(keyword%3Atoxin+OR+annotation%3A(type%3A%22tissue+specificity%22+venom))+AND+reviewed%3Ayes toxins.fasta.gz
	```		

	9b. Pull the Diamond Docker image

	```
	docker pull buchfink/diamond
	```
		
	9c. Import db index to Diamond 
	```
	docker run --rm -v `pwd`:`pwd` buchfink/diamond makedb --in `pwd`/toxins.fasta.gz -d `pwd`/toxins
	```

	9d. Run the Diamond process via docker

	```
	docker run --rm -v `pwd`:`pwd` buchfink/diamond blastx -q `pwd`/Trinity.fasta -d `pwd`/toxins -o `pwd`/diamond-toxin-out.txt -c1 -b19  > output.txt &
	```


	9e. Add TPM expression values to results file using MergeBlastTPM python script. (python3 MergeBlastTPM.py --help for options)
	```
	python3 MergeBlastTPM.py \
	-b Data/BLASTx_ToxinProt/diamond-toxin-out.txt \
	-t Data/Matrix/all.isoform.counts.matrix -o Data/BLASTx_ToxinProt/diamond-toxin-out-with-tpm-normalized.txt
	```

	9f. Generate annotation file for the BLASTx results
	```
	python3 AnnotateBlastResults.py
	```


10. Create toxin db with the structure below, then import data using sql load file function directly from toxin flat files.
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
	  `qseqid_unique` varchar(32) DEFAULT NULL,
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
	  ADD KEY `qseqid_unique` (`qseqid_unique`),
	  ADD KEY `tpm` (`tpm`),
	  ADD KEY `evalue` (`evalue`),
	  ADD KEY `pident` (`pident`),
	  ADD KEY `sseqid` (`sseqid`),
	  ADD KEY `bitscore` (`bitscore`),
	  ADD KEY `length` (`length`),
	  ADD KEY `symbol` (`symbol`);
	
	```

11. After importing the data and fully populating the database, run the following SQL commands. This will populate additional fields to make search more efficient later.
	```sql
	UPDATE blast_results SET symbol = (SELECT REPLACE(SUBSTRING_INDEX(sseqid,"|",2),"sp|",""));
	UPDATE blast_results SET qseqid_unique = (SELECT REPLACE(SUBSTRING_INDEX(qseqid,"_",2),"TRINITY_",""));
	```

12. Filter SQL results by tpm and eval to find best unique and isoform matches
	```sql
	# IsoForm - Best match by eValue
	SELECT *, (SELECT name FROM annotation_results WHERE symbol = A.symbol LIMIT 1) AS candidate_name FROM blast_results AS A 
	WHERE A.tpm>=1 
	AND A.evalue = (SELECT evalue FROM blast_results WHERE qseqid=A.qseqid ORDER BY evalue ASC LIMIT 1) 
	GROUP BY qseqid ORDER BY tpm DESC;

	# Unique - Best match by eValue
	# Can possibly filter transcripts with higher TPM for ones with lower evalue.
	SELECT A.*, count(A.qseqid_unique) as transcript_count, (SELECT name FROM annotation_results WHERE symbol = A.symbol LIMIT 1) AS candidate_name 
	FROM blast_results AS A 
	WHERE A.tpm>=1
	AND A.evalue <= (SELECT evalue FROM blast_results AS B WHERE A.qseqid_unique=B.qseqid_unique ORDER BY B.evalue DESC LIMIT 1) 
	GROUP BY A.qseqid_unique ORDER BY tpm DESC

	# Unique - Best match by tpm
	# Can possibly filter transcripts with lower evalue for ones with higher tpm, c
	SELECT A.*, count(A.qseqid_unique) as transcript_count, (SELECT name FROM annotation_results WHERE symbol = A.symbol LIMIT 1) AS candidate_name 
	FROM blast_results AS A 
	WHERE A.tpm>=1
	AND A.tpm >= (SELECT tpm FROM blast_results AS B WHERE A.qseqid_unique=B.qseqid_unique ORDER BY B.tpm DESC LIMIT 1) 
	GROUP BY A.qseqid_unique ORDER BY tpm DESC

	```


13. Create database view called, 'unique_by_highest_tpm'
	```sql
	CREATE
	 ALGORITHM = UNDEFINED
	 VIEW `unique_by_highest_tpm`
	 AS SELECT A.*, count(A.qseqid_unique) as transcript_count, (SELECT name FROM annotation_results WHERE symbol = A.symbol LIMIT 1) AS candidate_name 
		FROM blast_results AS A 
		WHERE A.tpm>=1
		AND A.tpm >= (SELECT tpm FROM blast_results AS B WHERE A.qseqid_unique=B.qseqid_unique ORDER BY B.tpm DESC LIMIT 1) 
		GROUP BY A.qseqid_unique ORDER BY tpm DESC
	```


14. Query the unique_by_highest_tpm view to get truly distinct transcript ToxProt matches for the transcriptome.

	```sql
	SELECT * FROM `unique_by_highest_tpm` AS A 
	WHERE tpm >= (SELECT tpm FROM unique_by_highest_tpm AS B WHERE A.symbol=B.symbol ORDER BY B.tpm DESC LIMIT 1) 
	GROUP BY symbol 
	ORDER BY tpm DESC
	```


<br>

<br>

<br>

# Results
The results of this analysis can also be view interactively through the web UI found at <a href="https://gaynorlab.com/gv/toxins" target="_blank">gaynorlab.com/gv/toxins</a>

<br>

## Counts 
| Metric | Total | Query |
|--|--|--|
| Total BLAST Hits| 10896 | ```SELECT COUNT(qseqid) FROM blast_results``` |
| Total BLAST Hits TPM >= 1| 4897 | ```SELECT COUNT(qseqid) FROM blast_results WHERE tpm >= 1``` |
| IsoForm Transcripts| 1415 | ```SELECT COUNT(DISTINCT(qseqid)) FROM blast_results``` |
| IsoForm Transcripts TPM >= 1| 616 | ```SELECT COUNT(DISTINCT(qseqid)) FROM blast_results WHERE tpm >= 1``` |
| Unique Transcripts| 493 | ```SELECT COUNT(DISTINCT(qseqid_unique)) FROM blast_results``` |
| Unique Transcripts TPM >= 1| 367 | ```SELECT COUNT(DISTINCT(qseqid_unique)) FROM blast_results WHERE tpm >= 1``` |
| Venom Toxin Groups| 129 | ```SELECT DISTINCT (candidate_name) FROM `unique_by_highest_tpm``` |
| Unique GO Values| 126 | ```SELECT COUNT(go_name) FROM `unique_go_values``` |

<br>

<br>

## Top 25 Highly Expressed Unique Venom/Toxin Candidates
| Transcript | Candidate | Pfam | GO | 3D Protein | TPM
|--|--|--|--|--|--|

<br>

<br>

## Venom Toxin Groups

<br>

<br>


## GO in Top Venom/Toxin Candidates

<br>
![alt text](https://github.com/kennypavan/Gonionemus-vertens-Venom-Analysis/blob/main/image.jpg?raw=true)
<br>


## Figures


<br>

<br>