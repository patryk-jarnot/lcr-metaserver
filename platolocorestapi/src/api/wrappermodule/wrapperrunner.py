from platolocorestapi.src.wrapper.methods.methodbuilder import MethodBuilder
import platolocorestapi.src.wrapper.utils.shannonutils as su


class WrapperRunner:
    def run(self, methods, params, protein_list, proteins):
        print(methods)
        if methods['seg_default']:
            self.run_method('seg', params['seg'], protein_list, proteins)
        if methods['seg_intermediate']:
            self.run_method('SEG_intermediate', None, protein_list, proteins)
        if methods['seg_strict']:
            self.run_method('SEG_strict', None, protein_list, proteins)
        if methods['cast']:
            self.run_method('cast', params['cast'], protein_list, proteins)
        if methods['flps']:
            self.run_method('flps', params['flps'], protein_list, proteins)
        if methods['flps_strict']:
            self.run_method('flps_strict', None, protein_list, proteins)
        if methods['simple']:
            self.run_method('simple', params['simple'], protein_list, proteins)
        if methods['gbsc']:
            self.run_method('gbsc', params['gbsc'], protein_list, proteins)

    def run_method(self, method_name, params, protein_list, proteins):
        methodsbuilder = MethodBuilder()
        method = methodsbuilder.create(method_name, params)
        method.identify(protein_list, proteins)
        for protein in proteins:
            protein['data']['entropy'] = su.create_sequence_data(protein['sequence'])

