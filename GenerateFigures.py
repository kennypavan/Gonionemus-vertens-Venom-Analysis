import pandas as pd
import matplotlib.pyplot as plt

toxin_file = pd.read_csv("Data/BLASTx_ToxinProt/diamond-toxin-out-with-tpm.txt",sep='\t', header=None)
toxin_file.columns = ['qseqid','sseqid','pident','length','mismatch','gapopen','qstart','qend','sstart','send','evalue','bitscore','TPM']

toxin_tpm_1 = toxin_file[toxin_file["TPM"] >= 1]

toxin_tpm_1.plot.scatter(x="length", y="TPM", alpha=0.5)

plt.savefig('Data/BLASTx_ToxinProt/length-tpm-scatter.png')

toxin_tpm_1.plot.scatter(x="pident", y="TPM", alpha=0.5)

plt.savefig('Data/BLASTx_ToxinProt/pident-tpm-scatter.png')

toxin_tpm_1.plot.scatter(x="pident", y="length", alpha=0.5)

plt.savefig('Data/BLASTx_ToxinProt/pident-length-scatter.png')
