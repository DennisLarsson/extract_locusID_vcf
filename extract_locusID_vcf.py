import sys

# run like this: python3 extractIDvcf.py populations.sorted.snps.vcf cov6_spicgrp.sorted.recode.p.snps.vcf

# !!!!! don't forget to check for duplicates that slip through and remove them!
#  !!!!!! then retain only the first value in the third column, for example: 60468 from 60468:30:+
#  !!!!!! use this command: cut -f 3 output_dups_removed.txt | cut -d":"  -f 1 > wl_GNS_filtered.txt
def testFunc (word):
	if "#" in word:
		return(1)
	else:
		return(0)

input_unfilt_file = sys.argv[1] # file that has not be further filtered (populations.snps.vcf)
input_filt_sorted_file = sys.argv[2] # file that has been further filtered using populations (cov6_spicgrp.sorted.recode.p.snps.vcf)

listUnfiltChromo = []
listUnfiltPos = []
listUnfiltlocusID = []

with open (input_unfilt_file, "r") as input_unfilt: # opens original unfiltered vcf file
	for line in input_unfilt:
		match_res = testFunc(line) # identifies whether line starts with "#"
		if match_res == 0:
			listUnfiltChromo.append(line.rstrip().split("\t")[0]) # stores the chromosome ID, position in locus and locus ID (from stacks references)
			listUnfiltPos.append(line.rstrip().split("\t")[1])
			listUnfiltlocusID.append(line.rstrip().split("\t")[2])

listFiltChromo = []
listFiltPos = []

with open (input_filt_sorted_file) as input_filt_sort: # opens the populations filtered vcf file
	for line in input_filt_sort:
		match_res = testFunc(line)
		if match_res == 0:
			listFiltChromo.append(line.rstrip().split("\t")[0]) # stores the chromosome ID and position in locus 
			listFiltPos.append(line.rstrip().split("\t")[1])

F = 0
U = 0
counter=0
print("Number of SNPs in unfiltered vcf file: " + str(len(listUnfiltChromo)))
print("Number of SNPs in populations filtered vcf file: " + str(len(listFiltChromo)))

outputFile = open ("output.txt", "w") 
outputFile_mismatch = open ("output_mismatch_pos.txt", "w") 
while F < len(listFiltChromo): #goes through every locus in the populations filtered file
	while (U < len(listUnfiltChromo) and F < len(listFiltChromo) and listFiltChromo[F] != listUnfiltChromo[U]): # compares the loci between the files. If they don't match, the counter for the unfiltered file ticks up
		#outputFile.write("U:"+str(listUnfiltChromo[U])+"\n")		# if one want the loci that don't match (where removed during populations filtering) this can be uncommented
		U+=1
	while (U < len(listUnfiltChromo) and F < len(listFiltChromo) and listFiltChromo[F] == listUnfiltChromo[U]): # compares the loci between the files. If they match, the  locus info is printed to an output file and a counter ticks up
		#print(listFiltChromo[F],listUnfiltChromo[U])
		unFiltPos = listUnfiltlocusID[U].split(":")[1]
		#print(unFiltPos)
		if listFiltPos[F] == listUnfiltPos[U]:
			outputFile.write(listUnfiltChromo[U] + "\t" + listUnfiltPos[U] + "\t" + listUnfiltlocusID[U] +"\n")
			counter+=1
		else: 
			outputFile_mismatch.write(listFiltChromo[F] + "\t" + listFiltPos[F] + "\t" + listUnfiltChromo[U] + "\t" + listUnfiltPos[U] + "\t" + listUnfiltlocusID[U] +"\n")
			
		U+=1
	F+=1
outputFile_mismatch.close()
print("number of loci that matches: " + str(counter))
