#!/usr/bin/env python

from optparse import OptionParser

import sys
import logging
# import pandas as pd
import numpy as np
import traceback

# try:
from src.methods.methodbuilder import MethodBuilder
from src.domain.sequence import Sequence
import src.utils.fastautils as fu
import src.utils.shannonutils as su
# except ModuleNotFoundError as e:
#     print("Use init.sh (source ./init.sh) script to initialise environment")
#     sys.exit(-1)


def parse_sequences(input_stream):
    current_sequence = None
    #for line in input_stream.readline():
    line = input_stream.readline()
    while line != "":
        if line.startswith(">"):
            if current_sequence is not None:
                if current_sequence.sequence == "":
                    logging.warning("Sequence of protein is empty. Header: {0}".format(current_sequence.header))
                else:
                    yield current_sequence
            current_sequence = Sequence()
            current_sequence.header = line.strip('\n')
        else:
            if current_sequence is None:
                raise ValueError("Input data corruption. No header found")
            current_sequence.sequence += line.strip('\n')

        line = input_stream.readline()

    if current_sequence is not None:
        if current_sequence.sequence == "":
            logging.warning("Sequence of protein is empty. Header: {0}".format(current_sequence.header))
        else:
            yield current_sequence


def get_params(options, method):
    if method == 'seg':
        return options.seg_params
    elif method == 'seg-intermediate':
        return options.seg_intermediate_params
    elif method == 'seg-strict':
        return options.seg_strict_params
    elif method == 'simple':
        return options.simple_params
    elif method == 'res':
        return options.res_params
    elif method == 'flps':
        return options.flps_params
    elif method == 'cast':
        return options.cast_params
    elif method == 'gbsc':
        return options.gbsc_params
    else:
        raise NotImplementedError("Parameters not found for method: {0}".format(method))


def get_options():
    parser = OptionParser(description="This software takes sequences from stdin in fasta format. Output is written to stdout in tabular format")
    parser.add_option("-v", "--version", action="store_true", dest="version", default=False)
    # parser.add_option("-m", "--methods", dest="methods", default='gbsc cast flps seg-strict seg-intermediary seg-relaxed simple',
    parser.add_option("-i", "--input", dest="input", default=None,
                      help="File from which sequences will be readed. If no specify then it is stdin", metavar="FILE")
    parser.add_option("-o", "--output", dest="output", default=None,
                      help="File to which output will be appending. If no specify then it is stdout", metavar="FILE")
    parser.add_option("-l", "--log", dest="log_file", default=None,
                      help="Path to log file. If no specify then it is stderr", metavar="FILE")
    parser.add_option("-m", "--methods", dest="methods", default='seg',
                      help="Methods to run. Each method should be separated with ' ' char. e.g.: \"seg seg-strict seg-intermediate simple res flps cast gbsc\"", metavar="METHODS")
    parser.add_option("--seg-params", dest="seg_params", default=None,
                      help="Params for SEG (without minuses)", metavar="PARAMS")
    parser.add_option("--seg-strict-params", dest="seg_strict_params", default=None,
                      help="Params for SEG where default parameters are strict (without minuses)", metavar="PARAMS")
    parser.add_option("--seg-intermediate-params", dest="seg_intermediate_params", default=None,
                      help="Params for SEG where default parameters are intermediate (without minuses)", metavar="PARAMS")
    parser.add_option("--simple-params", dest="simple_params", default=None,
                      help="Params for simple (without minuses)", metavar="PARAMS")
    parser.add_option("--res-params", dest="res_params", default=None,
                      help="Params for RES (without minuses)", metavar="PARAMS")
    parser.add_option("--flps-params", dest="flps_params", default=None,
                      help="Params for fLPS (without minuses)", metavar="PARAMS")
    parser.add_option("--cast-params", dest="cast_params", default=None,
                      help="Params for CAST (without minuses)", metavar="PARAMS")
    parser.add_option("--gbsc-params", dest="gbsc_params", default=None,
                      help="Params for GBSC (without minuses)", metavar="PARAMS")
    options, args = parser.parse_args()

    options.methods = options.methods.lower()

    return options, args


# cols = ["uniprot_id", "position", "is_lcr", "labels", "entropy"]


def print_header(output):
    output.write("sequence_header;position;amino_acid;is_lcr;labels;entropy\n")


def initialize_matrix(sequence):
    shannon_range = 20
    matrix = np.array([[sequence.header, i+1, sequence.sequence[i], 0, "", 0] for i in range(len(sequence.sequence))])

    for i in range(len(sequence.sequence)):
        matrix[i][5] = su.compute_entropy(sequence.sequence[int(max(0, i-(shannon_range/2))):int(min(len(sequence.sequence)-1, i+(shannon_range/2)))])

    return matrix


def update_matrix(output_matrix, output_table):
    output_table = output_table[0]
    assert(len(output_table.ranges) == len(output_table.labels))

    for i in range(len(output_table.ranges)):
        for j in range(output_table.ranges[i][0], output_table.ranges[i][1]):
            output_matrix[j][3] = 1
            output_matrix[j][4] += " {0}".format(output_table.labels[i])


def print_matrix(output, output_matrix):
    # np.savetxt(output, output_matrix, delimiter=';')
    for line in output_matrix:
        output.write(";".join(line))
        output.write("\n")


def get_version():
    return "0.9.0"


def main(options, args):
    if options.log_file is not None:
        try:
            logging.basicConfig(filename=options.log_file, format='%(asctime)s : %(levelname)s : %(message)s', datefmt="%m/%d/%Y %I:%M:%S %p", level=logging.INFO)
        except FileNotFoundError as e:
            logging.warning("Path to log file does not exists. Using stderr insstead.")
    else:
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', datefmt="%m/%d/%Y %I:%M:%S %p", level=logging.INFO)

    logging.info("Running wrapper version {0}".format(get_version()))

    if options.methods == "" or options.methods is None:
        logging.error("No method specified.")
        return None

    if options.input is not None:
        try:
            input = open(options.input, "r")
        except FileNotFoundError as e:
            logging.error("Incorrect input file path: " + str(options.input))
            return None
    else:
        input = sys.stdin

    if options.output is not None:
        try:
            output = open(options.output, "w")
        except FileNotFoundError as e:
            logging.warning("Path to output file does not exists. Using stdout instead.")
            output = sys.stdout
    else:
        output = sys.stdout

    methods = options.methods.split(" ")

    # print(output_frame)
    #
    # return None

    try:
        print_header(output)
        for sequence in parse_sequences(input):
            output_matrix = initialize_matrix(sequence)
            logging.info("Analysing sequence: {0}".format(sequence.header))
            for i in range(len(methods)):
                try:
                    params = get_params(options, methods[i])
                    methodsbuilder = MethodBuilder()
                    method = methodsbuilder.create(methods[i])
                    if params is not None:
                        method.set_params(params)
                    output_table = method.identify(sequence)
                    if len(output_table) > 0:
                        update_matrix(output_matrix, output_table)

                except NotImplementedError as e:
                    logging.error(str(e))
                except FileNotFoundError as e:
                    logging.error("Method {0} is not installed.".format(methods[i]))
            print_matrix(output, output_matrix)

    except (EOFError, ValueError) as e:
        logging.error(str(e))
        return None

    if options.input is not None:
        input.close()
    if options.output is not None:
        output.close()


if __name__ == "__main__":
    try:
        options, args = get_options()
        main(options, args)
    except Exception as e:
        logging.error("Unknown error occured: {0}".format(str(e)))


