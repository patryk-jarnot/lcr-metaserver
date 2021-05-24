# TMP topology and signal peptide prediction together:
# Phobius: PMID: 17483518
# Standalone version: http://phobius.sbc.su.se/data.html
import os
from subprocess import Popen, PIPE


class Phobius():
    def __init__(self, is_transmembran=True, is_signal_peptide=True):
        self.output = None
        self.is_transmembran = is_transmembran
        self.is_signal_peptide = is_signal_peptide

    def create_fasta_from_sequences(self, sequences):
        input = ''
        for sequence in sequences:
            input += "{0}\n".format(sequence['header'])
            input += "{0}\n".format(sequence['sequence'])
        return input

    def identify(self, protein_list, proteins):
        sequences = self.create_fasta_from_sequences(proteins)
        self.run(sequences, protein_list, proteins)

    def run(self, input, protein_list, proteins):
        try:
            FNULL = open(os.devnull, 'w')
            p = Popen("phobius.pl", stdout=PIPE, stdin=PIPE, stderr=FNULL)
            stdout = p.communicate(input=input.encode("ascii"))[0]
            self.output = stdout.decode()
            self.parse_output(proteins)
        except FileNotFoundError as error:
            print(error)

    def parse_output(self, proteins):
        retval = {"signals": {"regions": []},
                  "transmembranes": {"regions": []},
                  "domains": {"regions": []}}
        i = 0
        for line in self.output.splitlines():
            line = line.split()
            if line[0] != "//":
                if line[1] == "SIGNAL":
                    retval["signals"]["regions"].append({"beg": int(line[2]), "end": int(line[3])})
                elif line[1] == "DOMAIN":
                    retval["domains"]["regions"].append(
                        {"beg": int(line[2]), "end": int(line[3]),
                         "description": line[4][0] + " ".join(line[4:])[1:-1].lower()})
                elif line[1] == "TRANSMEM":
                    retval["transmembranes"]["regions"].append({"beg": int(line[2]), "end": int(line[3])})
            else:
                proteins[i]['data']['enrichment']["phobius"] = retval
                i += 1
                retval = {"signals": {"regions": []},
                          "transmembranes": {"regions": []},
                          "domains": {"regions": []}}
        return retval
