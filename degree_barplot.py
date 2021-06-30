#!/usr/bin/env python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import pathlib
import os

df = pd.read_csv('stringdb.txt', sep=' ',low_memory=False)
mydf = df[(df['combined_score'] >= '500')]
mydf[['ignore1', 'protein1']] = mydf['protein1'].str.split('.',expand=True)
mydf[['ignore2', 'protein2']] = mydf['protein2'].str.split('.',expand=True)


network = nx.from_pandas_edgelist(mydf, source = 'protein1', target = 'protein2')

#print(network.degree)
#nx.draw(network, node_size = 10, edge_color = 'gray')
high_degree = [n for n,d in network.degree if int(d) > 100]
low_degree = [n for n,d in network.degree if int(d) <= 100]


#ensembl database
ensembl_db = pd.read_csv('ensembldb.txt', sep='\t')
ensembl_db = ensembl_db.dropna()
hd_ensembl = ensembl_db[ensembl_db['Protein stable ID'].isin(high_degree)]
ld_ensembl = ensembl_db[ensembl_db['Protein stable ID'].isin(low_degree)]


hd_ensembl['Degree'] = 'high_degree'
ld_ensembl['Degree'] = 'low_degree'


final_db = pd.concat([hd_ensembl,ld_ensembl], axis=0)

plot = final_db.groupby(['Degree', 'Protein stable ID'])['Pfam ID'].count().to_frame(name="Pfam ID").reset_index()

sns.barplot(x="Degree", y="Pfam ID", palette="vlag", data=plot)
plt.savefig('protein_domains_vs_string_degree.png', dpi=300, bbox_inches='tight')

cwd=os.getcwd()
print("Plot saved in "+ cwd )
