from platolocorestapi.src.wrapper.methods.method import Method
from subprocess import Popen, PIPE
import os
import re

import logging


class Simple(Method):
    def __init__(self):
        super().__init__()
        self.output = None
        self.params = None
        self.current_header = None
        self.cur_id = 0

    def set_params(self, parameters):
        self.params = "{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11} {12} {13}".format(
                    parameters['score_mono'],
                    parameters['score_di'],
                    parameters['score_tri'],
                    parameters['score_tetra'],
                    parameters['score_penta'],
                    parameters['score_hexa'],
                    parameters['score_hepta'],
                    parameters['score_octa'],
                    parameters['score_nona'],
                    parameters['score_deca'],
                    parameters['window'],
                    parameters['num_of_rand'],
                    parameters['rand_method'],
                    parameters['stringency']
                )
        # if parameters is not None:
        #     logging.warning("Changing parameters for simple is not supported")

    def identify(self, protein_list, proteins):
        for i in range(len(proteins)):
            # for seq in sequences:
            input = self.create_fasta_from_sequences([proteins[i]])
            with open('/tmp/simple_input', 'w') as fw:
                fw.write(input)

            FNULL = open(os.devnull, 'w')
            params = "simple_net /tmp/simple_input p 3 {0} y /tmp/".format(self.params) # if self.params is None else 'cast /tmp/cast_input -tab {0}'.format(self.params)
            p = Popen(params.split(), stdout=FNULL, stdin=PIPE, stderr=FNULL)
            stdout = p.communicate()[0]

            with open('/tmp/S2', 'r') as f:
                self.output = f.read()

            self.parse_output([protein_list[i]], [proteins[i]])

    def parse_output(self, protein_list, proteins):
        method = {'method': 'SIMPLE', "regions": []}
        protein_list[0]['simple'] = []
        for line in self.output.splitlines():
            if len(re.findall('-', line)) == 2:
                range = re.findall('\d+', line)
                beg = int(range[0])
                end = int(range[1])
                protein_list[0]['regions'].append([beg, end])
                protein_list[0]['simple'].append([beg, end])
                method['regions'].append({'i': self.cur_id, 'beg': beg, 'end': end, 'description': "{0} rich region".format(self.get_cb_aa(proteins[0]['sequence'][beg:end])) })
                self.cur_id += 1

        proteins[0]['data']['wrapper'].append(method)

    # def parse_output(self, protein_list, proteins):
    #     retval = []
    #     current_record = None
    #     for line in self.output.splitlines():
    #         if len(re.findall('-', line)) == 2:
    #             range = re.findall('\d+', line)
    #             beg = int(range[0])
    #             end = int(range[1])
    #             if current_record is None or current_record.header != self.current_header:
    #                 if current_record is not None:
    #                     retval.append(current_record)
    #                 current_record = Method.MethodRecord()
    #                 current_record.header = self.current_header
    #             current_record.ranges.append((beg, end))
    #             current_record.labels.append("simple")
    #
    #     if current_record is not None:
    #         retval.append(current_record)
    #     return retval

