"""

Author: Muhammad Zohaib Anwar
License: GPL v3.0\n\n


Description:
SortmeRNA is the state-of-the-art tool for sorting the RNA into rRNA (SSU and LSU). 
This script is a wrapper around the sortmeRNA package to run on batch samples. Reads can be single end or paired-end
 

Dependencies:
1.SortmeRNA - https://github.com/biocore/sortmerna
 
Example:
python /software/CoMW/scripts/sort_rna.py -i ./data -s ./SSU_out/ -l ./LSU_out/ -m ./mRNA_out/ -t 96

"""

import subprocess
import sys
import argparse
import os
import os.path as path

parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-i", "--inputdir", help= "Fastq file directory")
#parser.add_argument("-o", "--outputdir", help= "Output directory")
parser.add_argument("-s", "--SSU", help= "SSU output directory")
parser.add_argument("-l", "--LSU", help= "LSU output directory")
parser.add_argument("-m", "--mRNA", help= "mRNA output directory")
parser.add_argument("-t", "--cpus", help= "Number of Threads to be used", type=int, default=1)

args = parser.parse_args()
if not args.inputdir: print("No input reads directory provided")
#if not args.outputdir: print "No output directory provided"
#if not (args.inputdir or args.outputdir): sys.exit(1)
if not (args.inputdir): sys.exit(1)



def merge(FileR1, FileR2):
	R1name, R1extension = os.path.splitext(FileR1)
	R2name, R2extension = os.path.splitext(FileR2)
	command = ["bash", "/data/Zohaib/AshBackToke/MetaTrans/0-Software/thirdpartytools/Sortmerna-1.9-linux-64-bin/scripts/merge-paired-reads.sh",inputdir+"/"+FileR1, inputdir+"/"+FileR2, merged_dir+"/"+R1name+"_merged.fastq"]
	#print(command)
	#subprocess.call(command)
	filter_SSU(filename = merged_dir+"/"+R1name+"_merged.fq")

def filter_SSU(filename):
	#print(inputdir)
	command = ["/software/Anaconda/envs/qiime2/bin/sortmerna","--reads", filename, "--aligned", filename.replace("merged.fq","SSU"), "--other", filename.replace("merged.fq","not_SSU"), "--paired_in", "--fastx", "--log", "--ref", dbdir+ "/silva-bac-16s-id90.fasta,"+indexdir+"/silva-bac-16s-id90-db/silva-bac-16s-db:"+dbdir+"/silva-arc-16s-id95.fasta,"+indexdir+"/silva-arc-16s-id95-db/silva-arc-16s-db:" + dbdir+"/silva-euk-18s-id95.fasta,"+indexdir+"/silva-euk-18s-id95-db/silva-euk-18s-db", "-a",str(cpus)]
	#print(command)
	subprocess.call(command)
	#not_SSU = filename.replace("merged","not_SSU")
	filter_LSU(filename = filename.replace("merged.fq","not_SSU.fq"))
	#unmerge(filename = inputdir+"/"+filename.replace("merged","SSU"))

def filter_LSU(filename):
	command = ["/software/Anaconda/envs/qiime2/bin/sortmerna","--reads", filename, "--aligned", filename.replace("not_SSU.fq","LSU"), "--other", filename.replace("not_SSU.fq","mRNA"), "--paired_in", "--fastx", "--log", "--ref", dbdir+ "/silva-bac-23s-id98.fasta,"+indexdir+"/silva-bac-23s-id98-db/silva-bac-23s-db:"+dbdir+"/silva-arc-23s-id98.fasta,"+indexdir+"/silva-arc-23s-id98-db/silva-arc-23s-db:" + dbdir+"/silva-euk-28s-id98.fasta,"+indexdir+"/silva-euk-28s-id98-db/silva-euk-28s-db", "-a",str(cpus)]
	print(command)
	subprocess.call(command)
	#unmerge(filename = inputdir+"/"+filename.replace("not_SSU","LSU"))
	#unmerge(filename = inputdir+"/"+filename.replace("not_SSU","mRNA"))	


def unmerge(filename):
	command = ["bash", "/data/Zohaib/AshBackToke/MetaTrans/0-Software/thirdpartytools/Sortmerna-1.9-linux-64-bin/scripts/unmerge-paired-reads.sh",filename,filename.replace("merged","R1"),filename.replace("merged","R2")]
	#print(command)
	#subprocess.call(command)


CoMWdir = os.path.realpath(__file__)
#dbdir =  path.abspath(path.join(__file__ ,"../../databases"))
dbdir =  "/home/tokea/software_installed_by_us/sortmerna/sortmerna-2.1-linux-64/rRNA_databases"
indexdir = "/home/tokea/software_installed_by_us/sortmerna/sortmerna-2.1-linux-64/index"
merged_dir = "/data/Zohaib/IceCave_Antonio/PilotRun/RNA_sort"
ssu_dir = "/data/Zohaib/IceCave_Antonio/PilotRun/RNA_sort/SSU"
lsu_dir =  "/data/Zohaib/IceCave_Antonio/PilotRun/RNA_sort/LSU"
mrna_dir = "/data/Zohaib/IceCave_Antonio/PilotRun/RNA_sort/mRNA"
#utildir = path.abspath(path.join(__file__ ,"../../utils"))
cpus = args.cpus
inputdir = args.inputdir
SSU_dir = ""
#outputdir = args.outputdir
#memory = args.memory

	
if __name__ == "__main__":

	R1 = []
	R2 = []
	for i in os.listdir(inputdir):
		if '_R1' in i:	
			R1.append(i)
		elif '_R2' in i:
			R2.append(i)
	for j,k in zip(R1,R2):
		#print inputdir+j, inputdir+k
		merge(FileR1 = j, FileR2 =k)
		#filter_SSU(filename = merged_dir+"/"+R1name+"_merged.fastq")	
#for i in os.listdir(merged_dir):
		#print(i)

