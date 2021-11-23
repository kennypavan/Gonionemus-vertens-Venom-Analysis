# BUSCO Instructions

1. Pull the BUSCO Docker image

	```docker pull ezlabgva/busco:v5.2.2_cv1```
	
2. Run the process via Docker. The command and paths may be different depending on your directory structure.

	```docker run -u $(id -u) -v $(pwd):/busco_wd/ -w /busco_wd/ ezlabgva/busco:v5.2.1_cv1 busco -i Trinity.fasta -o BUSCO -l metazoa_odb10 -m transcriptome```