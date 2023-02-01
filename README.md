# extract_locusID_vcf
A script to extract locus IDs from vcfs produced by populations when using a vcf file as input

Run like this: python3 extractIDvcf.py populations.sorted.snps.vcf cov6_spicgrp.sorted.recode.p.snps.vcf

!!!!! don't forget to check for duplicates that slip through and remove them!
Then retain only the first value in the third column, for example: 60468 from 60468:30:+
Use this command: cut -f 3 output_dups_removed.txt | cut -d":"  -f 1 > wl_GNS_filtered.txt
