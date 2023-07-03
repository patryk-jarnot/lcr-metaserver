
class WrapperMethodRequest:
    def __init__(self):
        self.method = None
        self.parameters = None

    @staticmethod
    def from_json(json):
        retval = WrapperMethodRequest()
        retval.method = json['method']
        if "parameters" in json:
            retval.parameters = json['parameters']
        return retval


class WrapperRequest:
    def __init__(self):
        self.methods = []

    @staticmethod
    def from_json(json):
        retval = WrapperRequest()
        for item in json:
            retval.methods.append(WrapperMethodRequest.from_json(item))
        return retval


class EnrichmentMethodRequest:
    def __init__(self):
        self.method = None
        self.parameters = None

    @staticmethod
    def from_json(json):
        retval = WrapperMethodRequest()
        retval.method = json['method']
        if "parameters" in json:
            retval.parameters = json['parameters']
        return retval


class EnrichmentRequest:
    def __init__(self):
        self.methods = []

    @staticmethod
    def from_json(json):
        retval = EnrichmentRequest()
        for item in json:
            retval.methods.append(EnrichmentMethodRequest.from_json(item))
        return retval


class Protein:
    def __init__(self):
        self.header = None
        self.sequence = None


class SequenceRequest:
    def __init__(self):
        self.fasta = None
        self.proteins = None
        self.wrapper = None
        self.enrichment = None

    @staticmethod
    def from_json(json):
        retval = SequenceRequest()
        retval.fasta = json['fasta']
        if "wrapper" in json:
            retval.wrapper = WrapperRequest.from_json(json['wrapper'])
        if "enrichment" in json:
            retval.enrichment = EnrichmentRequest.from_json(json['enrichment'])
        return retval


'''
{
    "fasta": ">sp|ASD2RW4|dupa\nASDFQWERWQGHSQQQQQQQQQQQQQQQQQQQQQQQQAQAQAQAQAQAQAQAQAQAQAFHSTHRAGHADFHBFH",
    "wrapper": [{"method": "seg", "parameters": "-help"}, {"method": "gbsc"}],
    "enrichment": [{"method": "aafrequency"}]
}
'''

