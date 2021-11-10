# Reads from GV Transcriptome runs 2 & 3.
All reads of samples MV1 - MV5 from runs 2 and 3 were concatenated together using the commands below.

```
cat MV1A_R1_001.fastq.gz MV2A_R1_001.fastq.gz MV3A_R1_001.fastq.gz MV4A_R1_001.fastq.gz MV5A_R1_001.fastq.gz MV1B_R1_001.fastq.gz MV2B_R1_001.fastq.gz MV3B_R1_001.fastq.gz MV4B_R1_001.fastq.gz MV5B_R1_001.fastq.gz > MV-ALL-R1.fastq.gz
```


```
cat MV1A_R2_001.fastq.gz MV2A_R2_001.fastq.gz MV3A_R2_001.fastq.gz MV4A_R2_001.fastq.gz MV5A_R2_001.fastq.gz MV1B_R2_001.fastq.gz MV2B_R2_001.fastq.gz MV3B_R2_001.fastq.gz MV4B_R2_001.fastq.gz MV5B_R2_001.fastq.gz > MV-ALL-R2.fastq.gz
```