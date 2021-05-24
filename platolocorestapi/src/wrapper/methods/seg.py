from platolocorestapi.src.wrapper.methods.method import Method
from subprocess import Popen, PIPE, STDOUT
import os


class Seg(Method):
    def __init__(self):
        super().__init__()
        self.output = None
        self.params = None
        self.method_name = "SEG"

    def set_params(self, parameters):
        self.params = "-locut {0} -hicut {1} -window {2}".format(float(parameters['k1']), float(parameters['k2']), int(parameters['window']))

    def change_params_set(self, name):
        if name == "SEG_strict":
            self.method_name = name
            self.params = '-locut 1.5 -hicut 1.8 -window 15'
        if name == "SEG_intermediate":
            self.method_name = name
            self.params = '-locut 1.9 -hicut 2.5 -window 15'
        # self.params = parameters
        # self.params = self.params.replace("locut", "-locut")
        # self.params = self.params.replace("hicut", "-hicut")
        # self.params = self.params.replace("window", "-window")

    def identify(self, protein_list, proteins):
        input = self.create_fasta_from_sequences(proteins)

        FNULL = open(os.devnull, 'w')
        params = "segmasker" if self.params is None else 'segmasker {0}'.format(self.params)
        p = Popen(params.split(), stdout=PIPE, stdin=PIPE, stderr=FNULL)

        stdout = p.communicate(input=input.encode("ascii"))[0]
        self.output = stdout.decode()
        parsed_output = self.parse_output(protein_list, proteins)
        return parsed_output

    def parse_output(self, protein_list, proteins):
        retval = []
        order_id = -1
        cur_id = 0
        method = None
        for line in self.output.splitlines():
            if line.startswith(">"):
                if method is not None:
                    proteins[order_id]['data']['wrapper'].append(method)
                order_id += 1
                protein_list[order_id][self.method_name] = []
                method = {'method': self.method_name, "regions": []}
            else:
                line_items = line.split("-")
                beg = int(line_items[0].strip())
                end = int(line_items[1].strip())
                protein_list[order_id]['regions'].append([beg, end])
                protein_list[order_id][self.method_name].append([beg, end])
                region = {'i': cur_id, 'beg': beg, 'end': end, 'description': "{0} rich region".format(self.get_cb_aa(proteins[order_id]['sequence'][beg:end]))}
                cur_id += 1
                method['regions'].append(region)

        if method is not None:
            proteins[order_id]['data']['wrapper'].append(method)

        return retval

