from abc import ABC, abstractmethod

from src.wrapper.domain.sequencedata import SequenceData, AminoAcidData
import src.wrapper.utils.shannonutils as su

import src.wrapper.utils.fastautils as fu


class Method(ABC):
    def __init__(self):
        self.shannon_range = 10

    class MethodRecord:
        def __init__(self):
            self.header = None
            self.ranges = []  # tuples (beg, end)
            self.labels = []

    @abstractmethod
    def set_params(self, parameters):
        ...

    @abstractmethod
    def identify(self, protein_list, proteins):
        ...

    @abstractmethod
    def parse_output(self, protein_list, proteins):
        ...

    def create_sequence_data(self, sequence, output):
        sequence_data = SequenceData()
        sequence_data.uniprot_id = fu.get_uniprot_id(sequence.header)

        for i in range(len(sequence.sequence)):
            aa_data = AminoAcidData()
            aa_data.position = i+1
            aa_data.score = su.compute_entropy(sequence.sequence[int(max(0, int(i-(self.shannon_range/2)))):int(min(len(sequence.sequence)-1, int(i+(self.shannon_range/2))))])
            sequence_data.amino_acids.append(aa_data)

        return sequence_data

    def get_cb_aa(self, sequence):
        retval = ''
        counts = {}
        for aa in sequence:
            if aa in counts:
                counts[aa] += 1
            else:
                counts[aa] = 1

        for k, v in counts.items():
            if v / len(sequence) > 0.2:
                retval += k

        return retval

    def create_fasta_from_sequences(self, sequences):
        input = ''
        for sequence in sequences:
            input += "{0}\n".format(sequence['header'])
            input += "{0}\n".format(sequence['sequence'])

        return input

    def create_fasta(self, sequence, short_header=False):
        input = ''
        input += "{0}\n".format(sequence.header)
        input += "{0}\n".format(sequence.sequence)
        return input

    def fill_sequence_data(self, record, sequence_data):
        for j in range(len(record.ranges)):
            for i in range(record.ranges[j][0]-1, record.ranges[j][1]):
                sequence_data.amino_acids[i].is_lcr = 1
                if j < len(record.labels):
                    sequence_data.amino_acids[i].labels.append(record.labels[j])

    def fill_output(self, record, output_frame):
        '''
        123;1;0;;2.346346346
        123;2;0;;2.346346346
        123;3;0;;2.346346346
        123;4;0;;2.346346346
        123;5;0;;2.346346346
        123;6;0;;2.346346346
        123;7;1;cast:A;0.346346346
        123;8;1;cast:A;0.346346346
        123;9;1;cast:A;0.346346346
        123;10;1;cast:A seg;0.346346346
        123;11;1;cast:A seg;0.346346346
        123;12;1;cast:A seg;0.346346346
        123;13;1;cast:A;0.346346346
        123;14;1;cast:A;0.346346346
        456;1;0;;2.346346346
        456;2;0;;2.346346346
        456;3;0;;2.346346346
        456;4;0;;2.346346346
        456;5;0;;2.346346346
        456;6;0;;2.346346346
        456;7;1;cast:A;0.346346346
        456;8;1;cast:A;0.346346346
        456;9;1;cast:A;0.346346346
        456;10;1;cast:A seg;0.346346346
        456;11;1;cast:A seg;0.346346346
        456;12;1;cast:A seg;0.346346346
        456;13;1;cast:A;0.346346346
        456;14;1;cast:A;0.346346346
        '''

        '''
        1. get table for uniprotid == 'asdf'
        2. update is_lcr and labels where the lcr is
        3. update main table
        '''

        df = output_frame.loc[output_frame.uniprot_id == fu.get_uniprot_id(record.header)].copy()

        for i in range(len(record.ranges)):
            df.loc[(df.position > record.ranges[i][0]) & (df.position < record.ranges[i][1]), 'is_lcr'] = 1
            df.loc[(df.position > record.ranges[i][0]) & (df.position < record.ranges[i][1]), 'labels'] += " {0}".format(record.labels[i])

        output_frame.update(df)

        return output_frame



