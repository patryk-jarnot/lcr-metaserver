import os
import json


def calculate_aa_frequency(proteins):
    tabu_list = ['B', 'J', 'O', 'U', 'X', 'Z']
    for prot in proteins:
        counts = {}
        total_count = 0
        for l in prot['sequence']:
            if l in tabu_list:
                continue
            total_count += 1
            if l in counts:
                counts[l] += 1
            else:
                counts[l] = 1

        for k, v in counts.items():
            counts[k] = v / total_count
        prot['data']['enrichment']['aa_frequency'] = counts


def read_db_entry(proteins, key, path):
    db_freq_path = path
    with open(db_freq_path, 'r') as f:
        content = f.read()
    db_freqs = json.loads(content)
    for prot in proteins:
        prot['data']['enrichment'][key] = db_freqs


def read_db_frequency(proteins):
    db_freq_path = "{0}/../../data/swiss_frequency".format(os.path.dirname(os.path.realpath(__file__)))
    read_db_entry(proteins, 'swiss_frequency', db_freq_path)

    db_freq_path = "{0}/../../data/next_frequency".format(os.path.dirname(os.path.realpath(__file__)))
    read_db_entry(proteins, 'next_frequency', db_freq_path)

    db_freq_path = "{0}/../../data/dis_frequency".format(os.path.dirname(os.path.realpath(__file__)))
    read_db_entry(proteins, 'dis_frequency', db_freq_path)

    db_freq_path = "{0}/../../data/pdb_frequency".format(os.path.dirname(os.path.realpath(__file__)))
    read_db_entry(proteins, 'pdb_frequency', db_freq_path)
