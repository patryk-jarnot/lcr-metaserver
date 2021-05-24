import platolocorestapi.src.utils.fasta as fasta
import io


class Query:
    def __init__(self, query):
        self.query = query

    def apply(self, protein_list, proteins):
        with fasta.FastaSequenceReader(fasta_handler=io.StringIO(self.query['sequences'])) as fsr:
            i = 0
            for sequence in fsr.read_sequences_2():
                i += 1
                print('header')
                print(sequence.header)

                prot = {}
                prot['id'] = i
                prot['uniprot_id'] = sequence.uniprot_id
                prot['header'] = sequence.header
                prot['user_order'] = i
                prot['regions'] = []
                prot['methods'] = []
                prot['length'] = len(sequence.sequence)
                protein_list.append(prot)

                prot_details = {}
                prot_details['id'] = i
                prot_details['uniprot_id'] = sequence.uniprot_id
                prot_details['header'] = sequence.header
                prot_details['sequence'] = sequence.sequence
                prot_details['pfam'] = self.query['enrichment']['pfam']
                prot_details['aafrequency'] = self.query['enrichment']['aafrequency']
                prot_details['data'] = {'wrapper': [], 'entropy': [], 'enrichment': {
                        "db_frequency": {'M': 0.024166, 'A': 0.082623, 'F': 0.038642, 'S': 0.066091, 'E': 0.067410, 'D': 0.054627, 'V': 0.068698, 'L': 0.096556, 'K': 0.058258, 'Y': 0.029207, 'R': 0.055366, 'P': 0.047242, 'N': 0.040605, 'W': 0.010945, 'Q': 0.039325, 'C': 0.013776, 'G': 0.070818, 'I': 0.059345, 'H': 0.022744, 'T': 0.053510},
                        "aa_frequency": {},
                        "phobius":
                            {
                            }
                    }
                }
                proteins.append(prot_details)

