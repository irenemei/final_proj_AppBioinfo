#Download files
string_link = https://stringdb-static.org/download/protein.links.v11.0/9606.protein.links.v11.0.txt.gz
ensembl_link = https://stockholmuniversity.box.com/shared/static/n8l0l1b3tg32wrzg2ensg8dnt7oua8ex

.PHONY : alls

alls: stringdb ensembldb degree_barplot

stringdb:
	curl $(string_link) | gunzip >> stringdb.txt

ensembldb:
	curl -L $(ensembl_link) >> ensembldb.txt 

degree_barplot: degree_barplot.py
	python3 degree_barplot.py
