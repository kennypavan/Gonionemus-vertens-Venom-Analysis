# Build Transcript and Gene Expression Matrix

1. Install Docker — Method highly dependent on OS. 

2. Pull the Trinity Docker image

	```docker pull trinityrnaseq/trinityrnaseq```

3. Download all necessary files used in the command below and adjust paths as necessary.

4. Run the Trinity command byway of Docker below

	```
	docker run -v `pwd`:`pwd` trinityrnaseq/trinityrnaseq /usr/local/bin/util/abundance_estimates_to_matrix.pl  \
	--gene_trans_map `pwd`/Trinity.fasta.gene_trans_map  \
	--est_method RSEM  \
	--out_prefix `pwd`/all \
	--name_sample_by_basedir \
	`pwd`/rsem_outdir/RSEM.isoforms.results
	```
