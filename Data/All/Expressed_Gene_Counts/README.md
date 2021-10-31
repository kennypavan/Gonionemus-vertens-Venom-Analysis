# Count the Numbers of Expressed Transcripts

1. Install Docker — Method highly dependent on OS. 

2. Pull the Trinity Docker image

	```docker pull trinityrnaseq/trinityrnaseq```

3. Download all necessary files used in the command below and adjust paths as necessary.

4. Run the Trinity command byway of Docker below

	```
docker run -v `pwd`:`pwd` trinityrnaseq/trinityrnaseq /usr/local/bin/util/misc/count_matrix_features_given_MIN_TPM_threshold.pl \
`pwd`/all.gene.TPM.not_cross_norm | tee `pwd`/all.gene.TPM.not_cross_norm.counts_by_min_TPM
	```

5. Generate a plot of the expressed transcripts using R by running the following command

	```
> R
> data = read.table("all.gene.TPM.not_cross_norm.counts_by_min_TPM", header=T)
> plot(data, xlim=c(-100,0), ylim=c(0,100000), t='b')

	```