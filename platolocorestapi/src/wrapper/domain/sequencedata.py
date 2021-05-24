from io import StringIO


class AminoAcidData:
    def __init__(self):
        self.position = None
        self.labels = []
        self.is_lcr = 0
        self.score = None


class SequenceData:
    def __init__(self):
        self.uniprot_id = None
        self.delimeter = ';'
        self.amino_acids = []

    def to_csv(self, retval=None):
        if retval is None:
            retval=StringIO()
        for aa in self.amino_acids:
            retval.write("{1}{0}{2}{0}{3}{0}{4}{0}{5}\n".format(self.delimeter, self.uniprot_id.replace(';', ''), aa.position, aa.is_lcr, " ".join(aa.labels), aa.score))
        return retval

