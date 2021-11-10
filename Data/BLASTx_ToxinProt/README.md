# Diamond Blastx Toxin & Venom Run Instructions

1. Download Venom and Toxin database 

	```wget https://www.uniprot.org/uniprot/?query=taxonomy%3A%22Metazoa+[33208]%22+and+(keyword%3Atoxin+OR+annotation%3A(type%3A%22tissue+specificity%22+venom))+AND+reviewed%3Ayes toxins.fasta.gz```

2. Pull the Diamond Docker image

	```docker pull buchfink/diamond```
	
3. Import db index to Diamond 

	```docker run --rm -v `pwd`:`pwd` buchfink/diamond makedb --in `pwd`/toxins.fasta.gz -d `pwd`/toxins```

4. Run the Diamond process via docker

	```docker run --rm -v `pwd`:`pwd` buchfink/diamond blastx -q `pwd`/Trinity.fasta -d `pwd`/toxins -o `pwd`/diamond-toxin-out.txt -c1 -b19  > output.txt &```
