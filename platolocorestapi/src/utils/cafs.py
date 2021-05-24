import hashlib
import os
from enum import Enum
import json
import time


class State(Enum):
    FINISHED = 1
    PROCESSING = 2
    NOT_FOUND = 3
    ERROR = 4


class Cafs:
    def __init__(self):
        self.db_path = '../data/cafs'
        if not os.path.isdir('../data'):
            os.mkdir('../data')
        if not os.path.isdir(self.db_path):
            os.mkdir(self.db_path)

    def create_dir(self, token):
        first_dir = "{0}/{1}".format(self.db_path, token[:2])
        second_dir = "{0}/{1}".format(first_dir, token[2:])

        if not os.path.isdir(first_dir):
            os.mkdir(first_dir)
        if not os.path.isdir(second_dir):
            os.mkdir(second_dir)

    def is_job_exists(self, token):
        if token is None:
            return None
        first_dir = "{0}/{1}".format(self.db_path, token[:2])
        second_dir = "{0}/{1}".format(first_dir, token[2:])

        if not os.path.isdir(first_dir):
            return False
        if not os.path.isdir(second_dir):
            return False
        return True

    @staticmethod
    def get_token(content):
        return hashlib.sha1(content).hexdigest()

    def get_dir_path(self, token):
        return "{0}/{1}/{2}".format(self.db_path, token[:2], token[2:])

    def set_state(self, token, state):
        with open("{0}/state".format(self.get_dir_path(token)), 'w') as f:
            f.write(state.name)

    def get_state(self, token):
        if not self.is_job_exists(token):
            return State.NOT_FOUND
        with open("{0}/state".format(self.get_dir_path(token)), 'r') as f:
            state = f.read()
            if state == State.FINISHED.name:
                return State.FINISHED
            elif state == State.PROCESSING.name:
                return State.PROCESSING
            elif state == State.NOT_FOUND.name:
                return State.NOT_FOUND
            else:
                return State.ERROR

    def get_proteins(self, token):
        if not self.is_job_exists(token):
            return None
        proteins_file_name = "{0}/proteins".format(self.get_dir_path(token))
        with open(proteins_file_name, 'r') as f:
            return json.loads(f.read())

    def set_proteins(self, token, proteins):
        if not self.is_job_exists(token):
            return None
        proteins_file_name = "{0}/proteins".format(self.get_dir_path(token))
        with open(proteins_file_name, 'w') as f:
            f.write(json.dumps(proteins))

    def get_protein(self, token, id):
        if not self.is_job_exists(token):
            return None
        proteins_file_name = "{0}/{1}".format(self.get_dir_path(token), id)
        with open(proteins_file_name, 'r') as f:
            return json.loads(f.read())

    def set_protein(self, token, protein, id):
        if not self.is_job_exists(token):
            return None
        proteins_file_name = "{0}/{1}".format(self.get_dir_path(token), id)
        with open(proteins_file_name, 'w') as f:
            f.write(json.dumps(protein))

    def set_time(self, token, is_start=True):
        if not self.is_job_exists(token):
            return None
        if is_start:
            time_file_name = "{0}/time_start".format(self.get_dir_path(token))
        else:
            time_file_name = "{0}/time_end".format(self.get_dir_path(token))
        with open(time_file_name, 'w') as f:
            f.write(str(time.time()))

    def save_name(self, token, name):
        file_name = "{0}/names".format(self.db_path)
        records = []
        try:
            with open(file_name, 'r') as f:
                for line in f:
                    if line.strip() == '':
                        continue
                    items = line.split(';')
                    rec_time = items[0]
                    if time.time() - int(rec_time) > 604800:
                        continue
                    rec_token = items[1]
                    rec_name = ";".join(items[2:]).strip()
                    if name == rec_name:
                        return False
                    records.append([rec_time, rec_token, rec_name])
        except FileNotFoundError:
            pass

        records.append([str(int(time.time())), token, name])

        with open(file_name, 'w') as f:
            for r in records:
                rec = ";".join(r)
                f.write("{0}\n".format(rec))

        job_name_file = "{0}/name".format(self.get_dir_path(token))
        with open(job_name_file, 'w') as f:
            f.write(name)

        return True

    def get_name(self, token):
        job_name_file = "{0}/name".format(self.get_dir_path(token))
        try:
            with open(job_name_file, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return None


    def get_token_by_name(self, name):
        file_name = "{0}/names".format(self.db_path)
        with open(file_name, 'r') as f:
            for line in f:
                if line.strip() == '':
                    continue
                items = line.split(';')
                rec_name = ";".join(items[2:]).strip()
                if rec_name == name:
                    return items[1]
        return None

