

class SequenceResponse:
    def __init__(self):
        self.composition = None

"""
{
    "header": ">sp|ASD2RW4|dupa",
    "sequence": "ASDFQWERWQGHSQQQQQQQQQQQQQQQQQQQQQQQQAQAQAQAQAQAQAQAQAQAQAFHSTHRAGHADFHBFH",
    "wrapper":
    [
        {
            "method": "gbsc",
            "intervals": [[10, 20], [40,50]],
        }
    ],
    "enrichment":
    {
        "frequency_db": {"A": 0.2, "C": 0.1, "D": 0.1, "E": 0.1, "S": 0.2, "T": 0.1, "Q": 0.1, "P": 0.1},
        "aa_frequency": {"S": 0.04054054054054054, "Q": 0.4864864864864865, "A": 0.1891891891891892, "E": 0.013513513513513514, "G": 0.02702702702702703, "H": 0.08108108108108109, "B": 0.013513513513513514, "D": 0.02702702702702703, "R": 0.02702702702702703, "T": 0.013513513513513514, "F": 0.05405405405405406, "W": 0.02702702702702703}
    }
}
"""
