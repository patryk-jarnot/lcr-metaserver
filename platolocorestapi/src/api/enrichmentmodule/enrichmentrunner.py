import platolocorestapi.src.enrichment.methods.phobius.run as phobius
from io import StringIO


class EnrichmentRunner:
    def __init__(self):
        pass

    def run(self, query, protein_list, proteins):
        if query['enrichment']['phobius']:
            phobius.Phobius().identify(protein_list, proteins)
