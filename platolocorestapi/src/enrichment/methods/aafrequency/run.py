import json


class AAFrequency:
    def __init__(self, sequence, aa_frequency_db_path, output_dict):
        self.output = None
        self.sequence = sequence
        self.frequency = {}
        self.output_dict = output_dict
        self.aa_frequency_db_path = aa_frequency_db_path

    def read_db(self):
        with open(self.aa_frequency_db_path) as f:
            return json.loads(f.read())

    def count_frequncy(self):
        if self.sequence.header not in self.output_dict:
            self.output_dict[self.sequence.header] = {}

        self.output_dict[self.sequence.header]["frequency_db"] = self.read_db()
        self.output_dict[self.sequence.header]["aa_frequency"] = {i: self.sequence.sequence.count(i) / len(self.sequence.sequence) for i in set(self.sequence.sequence)}

    def parse_output(self):
        return json.dumps({"frequency_db": self.read_db(), "aa_frequency": self.frequency})
