import sys
import os
from src.domain.protdomain import *
import src.domain.protdomain as pd
import re


class FastaConfig:
    separator = "|"
    class_id = ">c"
    sequence_id = ">sp"


class Sequence:
    def __init__(self):
        self.id = None
        self.uniprot_id = None
        self.header = None
        self.name = None
        self.sequence = None
        self.begin = None
        self.end = None
        self.family = None


class Cluster:
    def __init__(self):
        self.id = None
        self.model = None
        self.family = None
        self.sequences = []


class FastaHeader:
    def add_lcr_header_to_protein(self, protein, header):
        header = header.strip()
        items = header.split("|")
        lcr = Protein.Lcr(protein)
        lcr.id = items[1]
        lcr.begin = int(items[3])
        lcr.end = int(items[4])
        protein.lcrs.append(lcr)

    def lcr_header_to_protein(self, header):
        header = header.strip()
        items = header.split("|")
        protein = Protein()
        protein.uniprot_id = items[2]
        protein.family = items[5]
        lcr = Protein.Lcr(protein)
        lcr.id = items[1]
        lcr.begin = int(items[3])
        lcr.end = int(items[4])
        protein.lcrs.append(lcr)
        return protein


class FastaSequenceReader:

    def __init__(self, file_name=None, fasta_handler=None):
        if file_name is not None:
            self.file_opened = True
            self.file_handler = open(file_name, "r")
        else:
            self.file_opened = False
            self.file_handler = fasta_handler

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.file_opened:
            self.close()

    def close(self):
        if self.file_handler is not None:
            self.file_handler.close()

    def read_lcrs(self):
        data = self.read_lcr()
        while data is not None:
            yield data
            data = self.read_lcr()

    def read_lcr(self):
        lcr = Protein.Lcr(Protein())
        sequence = ""
        line = self.file_handler.readline()
        if not line.startswith(">") and line != "":
            line = self.file_handler.readline()
        if line == "":
            return None
        line = line.strip()
        header = line.split("|")
        lcr.protein.uniprot_id = header[1]
        try:
            lcr.id = header[2]
            lcr.begin = int(header[3])
            lcr.end = int(header[4])
            lcr.protein.name = header[5]
        except (IndexError, ValueError) as e:
            print(e)
        last_pos = None
        line = self.file_handler.readline()
        while not line.startswith(">") and line != "":
            sequence += line.strip()
            last_pos = self.file_handler.tell()
            line = self.file_handler.readline()
        if len(line) == 0:
            return None
        if line.startswith(">"):
            self.file_handler.seek(last_pos)

        lcr.sequence = sequence

        return lcr

    def read_sequence_2(self):
        data = Sequence()
        sequence = ""
        line = self.file_handler.readline()
        if not line.startswith(">") and line != "":
            line = self.file_handler.readline()
        if line == "":
            return None
        line = line.strip()
        header = line.split("|")
        data.header = line
        if len(header) > 1:
            if re.search("^[A-Z0-9]+$", header[1]):
                data.uniprot_id = header[1]
        last_pos = None
        line = self.file_handler.readline()
        while not line.startswith(">") and line != "":
            sequence += line.strip()
            last_pos = self.file_handler.tell()
            line = self.file_handler.readline()
        # print("sequence: {0}".format(sequence))
        # if len(line) == 0:
        #     return None
        if line.startswith(">"):
            self.file_handler.seek(last_pos)

        data.sequence = sequence

        if len(data.sequence) == 0 and len(data.uniprot_id) == 0:
            return None

        # print("uniprot_id: {0}".format(data.uniprot_id))
        # print("sequence: {0}".format(data.sequence))

        return data

    def read_sequences_2(self):
        data = self.read_sequence_2()
        while data is not None:
            yield data
            data = self.read_sequence_2()


class FastaSequenceWriter:

    def __init__(self, file_name):
        self.file_name = file_name
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
        self.file_handler = open(file_name, "w")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.file_handler.close()

    def write_sequences(self, sequences):
        for seq in sequences:
            self.file_handler.write(">sp|{0}\n".format(seq.uniprot_id))
            self.file_handler.write("{0}\n".format(seq.sequence))

    def write_sequences_wo_header(self, sequences):
        i = 1
        for seq in sequences:
            self.file_handler.write(">sp|{0}\n".format(i))
            self.file_handler.write("{0}\n".format(seq))
            i += 1


class FastaClusterReader:

    def __init__(self, file_name):
        self.file_handler = open(file_name, "r")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.file_handler.close()

    def read_lcrs(self):
        cluster = None
        # seq = None
        cluster_id = 0
        for line in self.file_handler:
            data = line.split(FastaConfig.separator)

            if line.startswith(FastaConfig.class_id):
                if cluster is not None:
                    yield cluster
                cluster = pd.Cluster()
                # print("data: {0}".format(data))
                if len(data) > 1:
                    cluster.id = int(data[1])
                if len(data) > 2:
                    cluster.model = data[2].strip()
                if len(data) > 3:
                    cluster.family = data[3].strip()
                cluster_id += 1
                cluster.id = cluster_id

            elif line.startswith(FastaConfig.sequence_id):
                lcr = pd.Protein.Lcr(pd.Protein())
                if len(data) > 1:
                    lcr.protein.uniprot_id = data[1]
                if len(data) > 2:
                    lcr.id = data[2]
                if len(data) > 3:
                    lcr.begin = int(data[3])
                if len(data) > 4:
                    lcr.end = int(data[4])
                if len(data) > 5:
                    lcr.name = data[5]

            else:
                assert(lcr != None)
                lcr.sequence = line.strip()
                cluster.lcrs[lcr.id] = lcr
                lcr = None

        if cluster is not None:
            yield cluster

    def read(self):
        cluster = None
        seq = None
        for line in self.file_handler:
            data = line.split(FastaConfig.separator)

            if line.startswith(FastaConfig.class_id):
                if cluster is not None:
                    yield cluster
                cluster = Cluster()
                if len(data) > 1:
                    cluster.id = int(data[1])
                if len(data) > 2:
                    cluster.model = data[2].strip()
                if len(data) > 3:
                    cluster.family = data[3].strip()

            elif line.startswith(FastaConfig.sequence_id):
                seq = Sequence()
                if len(data) > 1:
                    seq.uniprot_id = data[1].split('=')[1]
                if len(data) > 2:
                    seq.uniprot_id = data[2].split('=')[1]
                if len(data) > 3:
                    seq.begin = int(data[3].split('=')[1].strip())
                if len(data) > 4:
                    seq.end = int(data[4].split('=')[1].strip())
                if len(data) > 5:
                    seq.family = data[5].split('=')[1].strip()

            else:
                assert(seq != None)
                seq.sequence = line.strip()
                cluster.sequences.append(seq)
                seq = None

        if cluster is not None:
            yield cluster


class FastaClusterWriter:

    def __init__(self, file_name=None):
        self.file_name = file_name
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
        self.file_handler = open(file_name, "w")

        # >sp|uniprot_id|id|begin|end|name
        self.lcr_header = ">sp|{0}|{1}|{2}|{3}|{4}\n"
        self.cluster_header = ">c|{0}|{1}|{2}\n"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    # def append(self, cluster):
    #     self.file_handler.write("%s;id=%d;model=%s;family=%s\n" % (FastaConfig.class_id, cluster.id, cluster.model, cluster.family))
    #     i = 1
    #     for s in cluster.sequences:
    #         self.file_handler.write("%s;id=%d;uniprot_id=%s;name=%s\n" % (FastaConfig.sequence_id, i, s.uniprot_id, s.name))
    #         self.file_handler.write("%s\n" % (s.sequence, ))
    #         i += 1

    def write_clusters_lcr(self, clusters):
        for c in clusters:
            self.append_cluster_lcr(c)

    def append_cluster_lcr(self, cluster):
        self.file_handler.write(self.cluster_header.format(cluster.id, cluster.model, cluster.family))
        for lcr in cluster.lcrs.values():
            self.file_handler.write(self.lcr_header.format(lcr.protein.uniprot_id, lcr.id, lcr.begin, lcr.end, lcr.protein.name))
            self.file_handler.write("{0}\n".format(lcr.sequence))

    def close(self):
        self.file_handler.close()


