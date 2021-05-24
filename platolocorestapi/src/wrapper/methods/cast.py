from platolocorestapi.src.wrapper.methods.method import Method
from subprocess import Popen, PIPE
import os


class Cast(Method):
    def __init__(self):
        super().__init__()
        self.output = None
        self.params = None

    def set_params(self, parameters):
        # self.params = parameters
        self.params = "-thr {0}".format(int(parameters['threshold']))

        # if parameters is not None:
        #     self.params = self.params.replace("matrix", "-matrix")
        #     self.params = self.params.replace("thr", "-thr")

    def identify(self, protein_list, proteins):
        input = self.create_fasta_from_sequences(proteins)
        with open('/tmp/cast_input', 'w') as fw:
            fw.write(input)

        FNULL = open(os.devnull, 'w')
        # params = "cast /tmp/cast_input -tab -thr 40" if self.params is None else 'cast /tmp/cast_input -tab {0}'.format(self.params)
        params = "cast /tmp/cast_input -tab {0}".format(self.params)
        print(params)
        p = Popen(params.split(), stdout=FNULL, stdin=PIPE, stderr=FNULL)
        stdout = p.communicate()[0]

        with open('/tmp/cast_input.tab', 'r') as f:
            self.output = f.read()

        return self.parse_output(protein_list, proteins)

    def parse_output(self, protein_list, proteins):
        cur = -1
        cur_id = 0
        method = {'method': 'CAST', "regions": []}
        for line in self.output.splitlines():
            if line.startswith(">"):
                columns = line.split('\t')
                header = columns[0].strip()
                aa = columns[1]
                beg = int(columns[2])
                end = int(columns[3])
                if cur == -1 or proteins[cur]['header'].strip() != header:
                    last_cur = 0
                    if cur != -1:
                        proteins[cur]['data']['wrapper'].append(method)
                        last_cur = cur
                        cur = -1
                    method = {'method': 'CAST', "regions": []}
                    for i in range(last_cur, len(proteins)):
                        if header == proteins[i]['header'].strip():
                            cur = i
                            protein_list[cur]['CAST'] = []
                            break
                method['regions'].append({'i': cur_id, 'beg': beg, 'end': end, 'description': "{0} rich region".format(aa)})
                cur_id += 1
                protein_list[cur]['regions'].append([beg, end])
                protein_list[cur]['CAST'].append([beg, end])

        if cur != -1:
            proteins[cur]['data']['wrapper'].append(method)
