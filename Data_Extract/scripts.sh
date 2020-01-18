#!/usr/bin/env bash

# Divide all the protein files in 400 for distributed system
files=(PLMD-*(nN))
for ((n=1; $#files; n++)) {
  mkdir $n
  mv $files[1,111] $n
  files[1,111]=()
}

# Compress and delete the distributed proteins
folders=(*)
for ((n=1; $#folders; n++)) {
  tar -cvzf $n.tar.gz $n
  rm -rf $n
  folders[1,1]=()
}

# Fix the number of Db to download from this url - ftp://ftp.ncbi.nlm.nih.gov/blast/db/
# Only the NR ones
# Otherwise you will get an error later when extracting PSSM

# Download database from NCBI database
for i in $(seq -f "%02g" 0 131)
do
  wget -t 10 ftp://ftp.ncbi.nlm.nih.gov/blast/db/nr.$i.tar.gz
done


# Extract all the DB
for i in $(seq -f "%02g" 0 131)
do
  tar xvzf nr.$i.tar.gz
done


# Delete the zip files
for i in $(seq -f "%02g" 0 131)
do
  rm -rf nr.$i.tar.gz
done


# Download PSI BLAST installer
# ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/
# For linux
curl -O ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.9.0+-x64-linux.tar.gz
tar -xzvf ncbi-blast-2.9.0+-x64-linux.tar.gz
sudo apt-get install unzip


# Download the data (proteins in fasta format)


# Extract PSSM for single file to CHECK if its working correctly (NOT NEEDED)
/usr/local/ncbi/blast/bin/psiblast -query ./PLMD-1.seq -db /Users/dipta007/my-world/thesis/NR_new/nr -out PLMD-1.out -num_iterations 3 -out_ascii_pssm PLMD-1.pssm -inclusion_ethresh 0.001 -num_threads 4


# Extract PSSM for all the files
for i in *.seq;
do
  ~/ncbi-blast-2.9.0+/bin/psiblast -query ./$i -db ~/db/nr -out $i.out -num_iterations 3 -out_ascii_pssm $i.pssm -inclusion_ethresh 0.001 -num_threads 16;
done


# File count (NOT NEEDED)
find ./*.seq.spd3 -type f | wc -l
find * -type f | wc -l

for file in ./*; do
      if [ "${file: -5}" "==" ".hsb2" ]
        then
         echo $file
         mv "${file}" ../HSA/
      fi
done;