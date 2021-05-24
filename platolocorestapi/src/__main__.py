from flask import Flask, request
from flask_cors import CORS

import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func

from flask_restful import Resource, Api
import platolocorestapi.src.utils.cafs as cafs
from platolocorestapi.src.api.enrichmentmodule.enrichmentrunner import EnrichmentRunner
from platolocorestapi.src.api.wrappermodule.wrapperrunner import WrapperRunner
import platolocorestapi.src.api.query as query_parser
import platolocorestapi.src.api.aafrequency as aafrequency

import threading
import time
import json
import traceback


app = Flask(__name__)
api = Api(app)
CORS(app)

'''
method: PUT
url: 'http://127.0.0.1/query'
data: {"sequences":"","methods":{"seg_default":false,"seg_intermediary":false,"seg_strict":true,"cast":true,"flps":true,"simple":true,"gbsc":true},"enrichment":{"aafrequency":true}
response: {token: "34ouhtu34giidsjgiw3ijow3g"}

method: GET
url: 'http://127.0.0.1/jobs/:token'
data: 
response: {'status': 'FINISHED'}
possible-error: Calculation not finished yet.

method: GET
url: 'http://127.0.0.1/proteins/:token'
data: 
response: [ { "id": 1, "uniprot_id": "Q6GZX3", "header": ">sp|Q6GZX3|002L_FRG3G Uncharacterized protein 002L OS=Frog virus 3 (isolate Goorha) GN=FV3-002L PE=4 SV=1", "user_order": 1, "regions": [[10, 20],[40, 50]], "length": 100 }, { "id": 2, "uniprot_id": "Q197F8", "header": ">sp|Q197F8|002R_IIV3 Uncharacterized protein 002R OS=Invertebrate iridescent virus 3 GN=IIV3-002R PE=4 SV=1", "user_order": 2, "regions": [[10, 20],[40, 50]], "length": 100 }, { "id": 3, "uniprot_id": "P0C9H4", "header": ">sp|P0C9H4|1105L_ASFWA Protein MGF 110-5L OS=African swine fever virus (isolate Warthog/Namibia/Wart80/1980) GN=War-011 PE=3 SV=1", "user_order": 3, "regions": [[10, 20],[40, 50],[90,110],[120,150]], "length": 180 } ]
possible-error: Calculation not finished yet.

method: GET
url: 'http://127.0.0.1/proteins/:token/:id'
data: 
response: { "header":">sp|P0C9H4|1105L_ASFWA Protein MGF 110-5L OS=African swine fever virus (isolate Warthog/Namibia/Wart80/1980) GN=War-011 PE=3 SV=1", "sequence":"MGIKQYSQEELKEMALVEIAHELFEEHKKPVPFQELLNEIASLLGVAQAQAQAQAQAQAQAQAQAQAQAQAQAQAQAQAQAQAQAQAQAQAQKKEELGDRIAQFYTDLNIDGRFLALSDQTWGLRSWYPYDQLDEETQPTVKAKKKKAKKAVEEDLDLDEFEEIDEDDLDLDEVEEELDLEADDFDEEDLDEDDDDLEIEEDIIDEDDEDYDDEEEEIK", "data": { "wrapper": [ { "method": "GBSC", "regions": [{"beg":46, "end":91, "description": "tandem repeat of alanine and glutamine"}] }, { "method": "SEG", "regions": [{"beg":46, "end":91, "description": "tandem repeat of alanine and glutamine"}, {"beg":152, "end":218, "description": "Irregular low complexity region of E and D"}] }, { "method": "fLPS", "regions": [{"beg":46, "end":91, "description": "tandem repeat of alanine and glutamine"}, {"beg":152, "end":218, "description": "Irregular low complexity region of E and D"}] } ], "entropy": [3,4,3,4,3,4,3,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,3,3,2,3,2,2,3,2,3,2,3,2,3,2,3,2,2,3,2,3,2,2,2,1,0,1,0,0,1,0,0,1,0,0,0.5,0,0,0.5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], "enrichment": { "db_frequency": {"A": 0.2, "C": 0.1, "D": 0.1, "E": 0.1, "S": 0.2, "T": 0.1, "Q": 0.1, "P": 0.1}, "aa_frequency": {"Y": 0.02247191011235955, "E": 0.033707865168539325, "Q": 0.20224719101123595, "D": 0.0449438202247191, "C": 0.033707865168539325, "F": 0.07865168539325842, "V": 0.011235955056179775, "S": 0.056179775280898875, "W": 0.033707865168539325, "B": 0.011235955056179775, "H": 0.033707865168539325, "R": 0.0449438202247191, "U": 0.011235955056179775, "X": 0.02247191011235955, "G": 0.0449438202247191, "N": 0.02247191011235955, "J": 0.02247191011235955, "A": 0.2247191011235955, "T": 0.02247191011235955, "Z": 0.02247191011235955}, "phobius": { "signals": { "regions": [{"beg":46, "end":91}] }, "transmembranes": { "regions": [{"beg":146, "end":191}] }, "domains": { "regions": [{"beg":46, "end":61, "description": "N-Region"}, {"beg":66, "end":91, "description": "Cytoplasmic"},{"beg":146, "end":161, "description": "C-Region"}, {"beg":166, "end":191, "description": "non cytoplasmic"}] } } } } }
possible-error: Calculation not finished yet.
'''


def run_analysis(token, query):
    cafs_handler = cafs.Cafs()
    try:
        cafs_handler.set_time(token, True)
        protein_list = []
        proteins = []
        query_parsed = json.loads(query.decode('utf-8'))
        query_parser.Query(query_parsed).apply(protein_list, proteins)
        if query_parsed['name'] != '':
            cafs_handler.save_name(token, query_parsed['name'])
        WrapperRunner().run(query_parsed['methods'], query_parsed['params'], protein_list, proteins)
        if query_parsed['enrichment']['aafrequency']:
            aafrequency.calculate_aa_frequency(proteins)
            aafrequency.read_db_frequency(proteins)
        EnrichmentRunner().run(query_parsed, protein_list, proteins)
        cafs_handler.set_proteins(token, protein_list)
        for protein in proteins:
            cafs_handler.set_protein(token, protein, protein['id'])
        cafs_handler.set_state(token, cafs.State.FINISHED)
        cafs_handler.set_time(token, False)
    except Exception as e:
        print(e)
        print(traceback.print_exc())
        cafs_handler.set_state(token, cafs.State.ERROR)


class Query(Resource):
    def put(self):
        token = cafs.Cafs.get_token(request.data)
        fs = cafs.Cafs()
        query_parsed = json.loads(request.data.decode('utf-8'))
        if query_parsed['name'].strip() != '' and fs.get_token_by_name(query_parsed['name']) is not None:
            return {'error': 'Given job name already exists'}
        fs.create_dir(token)
        fs.set_state(token, cafs.State.PROCESSING)
        threading.Thread(target=run_analysis, args=(token, request.data)).start()

        return {"token": token}


class Job(Resource):
    def get(self, token):
        cafs_handler = cafs.Cafs()
        state = cafs_handler.get_state(token)
        if state == cafs.State.NOT_FOUND:
            token = cafs_handler.get_token_by_name(token)
            state = cafs_handler.get_state(token)

        return {'status': state.name, 'token': token}


class Proteins(Resource):
    def get(self, token):
        cafs_handler = cafs.Cafs()

        return {'name': cafs_handler.get_name(token), 'proteins': cafs_handler.get_proteins(token)}


class Protein(Resource):
    def get(self, token, id):
        return cafs.Cafs().get_protein(token, id)


api.add_resource(Query, '/restapi/query')
api.add_resource(Job, '/restapi/job/<token>')
api.add_resource(Proteins, '/restapi/proteins/<token>')
api.add_resource(Protein, '/restapi/proteins/<token>/<id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5002')
    # app.run(host='127.0.0.1', port='5002')


