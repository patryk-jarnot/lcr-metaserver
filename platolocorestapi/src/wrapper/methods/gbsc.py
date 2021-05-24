from platolocorestapi.src.wrapper.methods.method import Method
from subprocess import Popen, PIPE, STDOUT
import os


class Gbsc(Method):
    def __init__(self):
        super().__init__()
        self.output = None
        self.params = None

    def set_params(self, parameters):
        # self.params = parameters
        self.params = "--score-threshold {0} --distance-threshold {1}".format(parameters['score'], parameters['distance'])
        # self.params = self.params.replace("score-threshold", "--score-threshold")
        # self.params = self.params.replace("distance-threshold", "--distance-threshold")

    def identify(self, protein_list, proteins):
        input = self.create_fasta_from_sequences(proteins)

        FNULL = open(os.devnull, 'w')
        # params = "gbsc --output-format=1" if self.params is None else 'gbsc --output-format=1 {0}'.format(self.params)
        params = "gbsc --output-format=1 {0}".format(self.params)
        p = Popen(params.split(), stdout=PIPE, stdin=PIPE, stderr=FNULL)

        stdout = p.communicate(input=input.encode("ascii"))[0]
        self.output = stdout.decode()
        parsed_output = self.parse_output(protein_list, proteins)
        return parsed_output

        # for record in parsed_output:
        #     output_frame = self.fill_output(record, output_frame)

        # return output_frame

    def parse_output(self, protein_list, proteins):
        retval = []
        # current_record = None
        order_id = -1
        cur_id = 0
        method = None
        for line in self.output.splitlines():
            if line.startswith(">"):
                if method is not None:
                    proteins[order_id]['data']['wrapper'].append(method)
                order_id += 1
                protein_list[order_id]['GBSC'] = []
                method = {'method': 'GBSC', "regions": []}
                # current_record = Method.MethodRecord()
                # current_record.header = line.strip("\n")
            else:
                amino_acids = line.split("|")[1]
                line_items = line.split("|")[0].split("-")
                beg = int(line_items[0].strip())
                end = int(line_items[1].strip())
                protein_list[order_id]['regions'].append([beg, end])
                protein_list[order_id]['GBSC'].append([beg, end])
                region = {'i': cur_id, 'beg': beg, 'end': end, 'description': "{0} rich repetitive region".format(amino_acids)}
                cur_id += 1
                method['regions'].append(region)
                # current_record.ranges.append((int(line_items[0].strip()), int(line_items[1].strip())))
                # current_record.labels.append("SEG")

        if method is not None:
            proteins[order_id]['data']['wrapper'].append(method)
        # if current_record is not None:
        #     retval.append(current_record)

    # def parse_output(self, protein_list, proteins):
    #     retval = []
    #     current_record = None
    #     for line in self.output.splitlines():
    #         if line.startswith(">"):
    #             if current_record is not None:
    #                 retval.append(current_record)
    #             current_record = Method.MethodRecord()
    #             current_record.header = line.strip("\n")
    #         else:
    #             line_items = line.split("-")
    #             current_record.ranges.append((int(line_items[0].strip()), int(line_items[1].strip())))
    #             current_record.labels.append("GBSC")
    #
    #     if current_record is not None:
    #         retval.append(current_record)

        return retval

