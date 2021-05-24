import sys
import os

FILE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULE_DIR = "%s/.." % FILE_DIR
ROOT_DIR = "%s" % MODULE_DIR
sys.path.append(os.path.abspath(MODULE_DIR))


class Protein:
    class Lcr:
        def __init__(self, protein):
            self.id = None
            self.sequence = None
            self.begin = None
            self.end = None
            self.protein = protein

        def to_fasta(self):
            if self.protein.uniprot_id is None:
                raise Exception("Protein not initialized, uniprote_id is None")

            retval = ">sp|{0}|{1}|{2}|{3}|{4}\n{5}".format(self.id, self.protein.uniprot_id, self.begin, self.end, self.protein.family, self.sequence)
            return retval

    def __init__(self):
        self.uniprot_id = None
        self.name = None
        self.family = None
        self.sequence = None
        self.lcrs = []
        self.hcr_sequence = None

    def protein_to_fasta(self):
        if self.uniprot_id is None:
            raise Exception("Protein not initialized, uniprote_id is None")
        if self.sequence is None:
            raise Exception("Sequence of proteins {0} is None".format(self.uniprot_id))

        return ">{0}\n{1}".format(self.uniprot_id, self.sequence)

    def lcrs_to_fasta(self):
        if self.uniprot_id is None:
            raise Exception("Protein not initialized, uniprote_id is None")
        if len(self.lcrs) == 0:
            raise Exception("Protein {0} does not contain LCRs".format(self.uniprot_id))

        retval = ""
        for i, lcr in enumerate(self.lcrs):
            retval += ">sp|{0}|{1}|{2}|{3}|{4}\n{5}".format(lcr.id, self.uniprot_id, lcr.begin, lcr.end, self.family, lcr.sequence)
            if i != len(self.lcrs) - 1:
                retval += "\n"
        return retval

    def hcr_to_fasta(self):
        if self.uniprot_id is None:
            raise Exception("Protein not initialized, uniprote_id is None")
        if self.hcr_sequence is None:
            raise Exception("HCR sequence of proteins {0} is None".format(self.uniprot_id))

        return ">{0}\n{1}".format(self.uniprot_id, self.hcr_sequence)


class Cluster:
    def __init__(self):
        self.id = None
        self.model = None
        self.family = None
        self.proteins = {}
        self.lcrs = {}


class LcrDomain:

    def __init__(self, id=None, id_protein=None, sequence=None, domain=None, begin=None, end=None, family=None, organism=None):
        self.id = id
        self.id_protein = id_protein
        self.id_uniprot = None
        self.sequence = sequence
        self.domain = domain
        self.begin = begin
        self.end = end
        self.family = family
        self.organism = organism
        self.cluster_data = None


class HcrDomain:

    def __init__(self, id=None, sequence=None, family=None):
        self.id = id
        self.sequence = sequence
        self.family = family


class ProtDomain:

    def __init__(self, id=None, id_swissprot=None, organism=None, hcr=None, lcrs=None):
        self.id = id
        self.id_swissprot = id_swissprot
        self.organism = organism
        self.hcr = hcr
        self.lcrs = lcrs

