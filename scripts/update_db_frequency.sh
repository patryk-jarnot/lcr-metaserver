SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

echo $SCRIPTPATH
cd $SCRIPTPATH/..
echo $(pwd)
source ./init.sh

cd platolocorestapi/data
[ -e uniprot_sprot.fasta.gz ] && rm -f uniprot_sprot.fasta.gz
wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz
[ -e uniprot_sprot.fasta ] && rm -f uniprot_sprot.fasta
gzip -d uniprot_sprot.fasta.gz
cd ../src/scripts
python3 calculate_db_frequency.py -i ../../data/uniprot_sprot.fasta -o ../../data/db_frequency
rm -f uniprot_sprot.fasta.gz
