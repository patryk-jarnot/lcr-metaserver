import json
import logging
import sys
from optparse import OptionParser

from platolocorestapi.src.enrichment.domain.sequence import Sequence
from platolocorestapi.src.enrichment.methods.aafrequency.run import AAFrequency
from platolocorestapi.src.enrichment.methods.phobius.run import Phobius


def parse_sequences(input_stream):
    current_sequence = None
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


def get_options():
    parser = OptionParser()
    parser.add_option("-v", "--version", action="store_true", dest="version", default=False)
    parser.add_option("-a", "--aa-frequency", action="store_true", dest="is_aa_frequency", default=False)
    parser.add_option("--aa-frequency-db-path", dest="aa_frequency_db_path", default="./swissprot_frequency.txt")

    parser.add_option("-s", "--signal-peptide", action="store_true", dest="is_signal_peptide", default=False)
    parser.add_option("-t", "--transmembrane", action="store_true", dest="is_transmembrane", default=False)
    parser.add_option("-i", "--input", dest="input_path", default=None,
                      help="Path to fasta sequences", metavar="FILE")
    parser.add_option("-o", "--output", dest="output_path", default=None,
                      help="Path to file that will contains results in JSON format", metavar="FILE")
    parser.add_option("-l", "--log", dest="log_file", default=None,
                      help="Path to log file. If no specify then it is stderr", metavar="FILE")
    return parser.parse_args()


def initialize_file_handlers(options):
    if options.log_file is not None:
        try:
            logging.basicConfig(filename=options.log_file, format='%(asctime)s : %(levelname)s : %(message)s',
                                datefmt="%m/%d/%Y %I:%M:%S %p", level=logging.INFO)
        except FileNotFoundError as e:
            logging.warning("Path to log file does not exists. Using stderr insstead.")
    else:
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', datefmt="%m/%d/%Y %I:%M:%S %p",
                            level=logging.INFO)

    if options.input_path is not None:
        try:
            input = open(options.input_path, "r")
        except FileNotFoundError as e:
            logging.error("Incorrect input file path: " + str(options.input_path))
            raise e
    else:
        input = sys.stdin

    if options.output_path is not None:
        try:
            output = open(options.output_path, "w")
        except FileNotFoundError as e:
            logging.warning("Path to output file does not exists. Using stdout instead.")
            raise e
    else:
        output = sys.stdout

    return input, output


def print_dict(output_file, dictionary):
    output = json.dumps(dictionary)
    output_file.write(output)


def add_prot_to_dict(dictionary, prot_header):
    if prot_header not in dictionary.keys():
        dictionary[prot_header] = {}


def main(options, args):
    output_dict = {}

    try:
        input_file, output_file = initialize_file_handlers(options)
    except FileNotFoundError as e:
        return None

    try:
        for sequence in parse_sequences(input_file):
            logging.info("Analysing sequence: {0}".format(sequence.header))
            add_prot_to_dict(output_dict, sequence.header)
            try:
                if options.is_aa_frequency:
                    aafreq = AAFrequency(sequence, options.aa_frequency_db_path, output_dict)
                    aafreq.count_frequncy()

            except NotImplementedError as e:
                logging.error(str(e))
            try:
                if options.is_signal_peptide or options.is_transmembrane:
                    phobius = Phobius(sequence, options.is_transmembrane, options.is_signal_peptide, output_dict)
                    phobius.identify()

            except NotImplementedError as e:
                logging.error(str(e))
        print_dict(output_file, output_dict)

    except (EOFError, ValueError) as e:
        logging.error(str(e))
        return None

    if options.input_path is not None:
        input_file.close()
    if options.output_path is not None:
        output_file.close()


if __name__ == "__main__":
    options, args = get_options()
    if options.version:
        print("1.0.0")
    else:
        main(options, args)
