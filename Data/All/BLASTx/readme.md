# Diamond Run Instructions

1. Download NR database (~112Gb)

	```wget https://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nr.gz```

2. Pull the Diamond Docker image

	```docker pull buchfink/diamond```
	
3. Import db index to Diamond (requires ~200gb free HD space)

	```docker run --rm -v `pwd`:`pwd` buchfink/diamond makedb --in `pwd`/nr.gz -d `pwd`/nr```

4. Run the Diamond process via docker

	```docker run --rm -v `pwd`:`pwd` buchfink/diamond blastx -q `pwd`/Trinity.fasta -d `pwd`/nr1 -o `pwd`/diamond-out.txt -c1 -b19  > output.txt &```


