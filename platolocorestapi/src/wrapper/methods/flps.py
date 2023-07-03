from src.wrapper.methods.method import Method
from subprocess import Popen, PIPE, STDOUT
import os


class Flps(Method):
    def __init__(self):
        super().__init__()
        self.output = None
        self.params = None
        self.query_params = {}
        self.method_name = "fLPS"

    def set_params(self, parameters):
        self.query_params = parameters
        self.params = "-m {0} -M {1} -t {2}".format(int(parameters['min_tract_len']), int(parameters['max_tract_len']), float(parameters['pval']))

    def change_params_set(self, name):
        if name == "fLPS_strict":
            self.method_name = name
            self.params = '-m 5 -M 25 -t 0.0001'
            self.query_params['regions'] = {}
            self.query_params['regions']['single'] = True
            self.query_params['regions']['multiple'] = True
            self.query_params['regions']['whole'] = False

    def identify(self, protein_list, proteins):
        input = self.create_fasta_from_sequences(proteins)
        with open('/tmp/flps_input', 'w') as fw:
            fw.write(input)

        FNULL = open(os.devnull, 'w')
        params = "fLPS {0} /tmp/flps_input".format(self.params)
        p = Popen(params.split(), stdout=PIPE, stdin=PIPE, stderr=FNULL)

        stdout = p.communicate(input=input.encode("ascii"))[0]
        self.output = stdout.decode()
        self.parse_output(protein_list, proteins)

    def parse_output(self, protein_list, proteins):
        cur = -1
        method = {'method': self.method_name, "regions": []}
        cur_id = 0
        for line in self.output.splitlines():
            columns = line.split('\t')
            if not self.query_params['regions']['single'] and columns[1] == "SINGLE":
                continue
            if not self.query_params['regions']['multiple'] and columns[1] == "MULTIPLE":
                continue
            if not self.query_params['regions']['whole'] and columns[1] == "WHOLE":
                continue
            header = columns[0].strip()
            aa = columns[7].replace('{', '').replace('}', '')
            beg = int(columns[3])
            end = int(columns[4])
            if cur == -1 or proteins[cur]['header'].split(' ')[0].strip()[1:] != header:
                last_cur = 0
                if cur != -1:
                    proteins[cur]['data']['wrapper'].append(method)
                    last_cur = cur
                    cur = -1
                method = {'method': self.method_name, "regions": []}
                for i in range(last_cur, len(proteins)):
                    if header == proteins[i]['header'].split(' ')[0].strip()[1:]:
                        cur = i
                        protein_list[cur][self.method_name] = []
                        break
            method['regions'].append({'i': cur_id, 'beg': beg, 'end': end, 'description': "{0} rich region".format(aa)})
            cur_id += 1
            protein_list[cur]['regions'].append([beg, end])
            protein_list[cur][self.method_name].append([beg, end])

        if cur != -1:
            proteins[cur]['data']['wrapper'].append(method)

