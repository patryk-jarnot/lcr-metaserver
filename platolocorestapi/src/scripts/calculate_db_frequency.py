import src.utils.fasta as fasta
from optparse import OptionParser
import json


def get_options():
    parser = OptionParser()
    parser.add_option("-v", "--version", action="store_true", dest="version", default=False)
    parser.add_option("-i", "--input", dest="input_file", default=None,
                      help="Path to fasta database", metavar="FILE")
    parser.add_option("-o", "--output", dest="output_file", default=None,
                      help="Path to file that will contains results", metavar="FILE")
    return parser.parse_args()


def main(options, args):
    counts = {}
    total_count = 0
    with fasta.FastaSequenceReader(options.input_file) as fsr:
        for sequence in fsr.read_sequences_2():
            letters = sequence.sequence
            for l in letters:
                total_count += 1
                if l in counts:
                    counts[l] += 1
                else:
                    counts[l] = 1

    sum = 0
    tabu_list = ['B', 'J', 'O', 'U', 'X', 'Z']
    for ti in tabu_list:
        if ti in counts.keys():
            del counts[ti]
    for k, v in counts.items():
        counts[k] = v / total_count
        sum += counts[k]
        counts[k] = int(counts[k] * 10000) / 10000
        # counts[k] = "{:.6f}".format(counts[k])


    with open(options.output_file, 'w') as f:
        # f.write(str(sum))
        # f.write('\n')
        f.write(json.dumps(counts))
        # f.write(str(counts))


if __name__ == "__main__":
    options, args = get_options()
    if options.version:
        print("1.0.0")
    else:
        main(options, args)

