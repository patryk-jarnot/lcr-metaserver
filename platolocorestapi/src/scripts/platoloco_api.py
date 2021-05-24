from optparse import OptionParser
import requests
import json
import time


def send_query(url):
    url = "http://{0}/restapi/query".format(url)
    data = '{"name":"","sequences":">sp|Q6GZX3|002L_FRG3G Uncharacterized protein 002L OS=Frog virus 3 (isolate Goorha) GN=FV3-002L PE=4 SV=1\\nSIIGATRLQNDKSDTYSAGPCYAGGCSAFTPRGTCGKDWDLGEQTCASGFCTSQPLCARKKTQVCGLRYSSKGKDPLVSAEWDSRGAPYVRCTYDADLIDTQAQVDQFVSMFGESPSLERYCMRGVKNTAGELVSRVSSDADPAGGWCRKWYSAHRGPDQDAALGSFCIKNPGAADCCINRASDPVYQKVKTLHAYPDQCWYVPCAADVGELKMGTQRDTPTNCPTQVCQIVFNMLDGSVTMDDVKNTINCDFSKYVPPPPPPKPTPPTPPTPPTPPTPPTPPTPPTPRPVHNRKMFFVAGAVLVAILISTVRW\\n>sp|P14922|CYC8_YEAST General transcriptional corepressor CYC8 OS=Saccharomyces cerevisiae (strain ATCC 204508 / S288c) GN=CYC8 PE=1 SV=2\\nNPGGEQTIMEQPAQQQQQQQQQQQQQQQQAAVPQQPLDPLTQSTAETWLSIASLAETLGGDRAAMAYDATLQFNPSSAKALTSLAHLYRSRDMFQRAAELYERALLVNPELSDVWATLHCYLMLDDLQRAYNAYQQALYHLSNPNVPKLWHGIGILYDRYGSLDYAEEAFAKVLELDHFEKANEIYFRLGIIYKHQGKWSQALECFRYILPQPPAPLQEWDIWFQLGSVLESMGEWGAKEAYEHVLAQNQHHAKVLQQLGCLYGMSNVQFYDPQKALDYLLKSLEADPSDATTWYLGRVHMIRTDYTAAYDAFQQAVNRDSRNPIFWCSIGVLYYQISQYRDALDAYTRAIRLNYISEVWYDLGTLYETCNNQLSDALDAYKQAARLDVNNVHIRERLEALTKQLENPGNINKNGAPTNASPAPPPVILQPTLQPNDQGNPLNTRISAQSANATASMVQQQHPAQQTPINSSTMYSNGASPQLQAQAQAQAQAQAQAQAQAQAQAQAQAQAQAQAQAQAQAQAQAQAHAQAQAQAQAQAQAQAQAQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQLQPLPRQQLQQKGSVQMLNPQQGQPYITQPTVIQAHQLQPFSTQAMEHPQSSQLPPQQQQLQSVQHPQQLQGPQAQAPQPLIQHNVEQNVLPQKRYMEGAIHTLVDAAVSSSTHTENNTKSPRQPTHAIPTAPATGITNAEPQVKKQKLNSPNSNINKLVNTATSIEENAKSEVSNQSPAVVESNTNNTSEEKPVKANSIPSVIGAQEPPQEASPAEEATKAASVSPSTKPLNTEPESSSVQPTVSSESTTKANDQSTAETIELSTATVPAEASPVEDEVRQHSKEENGTTEASAPSTEEAEPAASRDEKQQDETAATTITVIKPTLETMETVKEEAKMREEEQTSQEKSPQENTLPRENVVRQVEEENYDD\\n>sp|Q1ZXH2|FHKB_DICDI Probable serine/threonine-protein kinase fhkB OS=Dictyostelium discoideum GN=fhkB PE=3 SV=1\\nSQDIQTQNSYSDELYSSQIYSTQQPQQPQQQPQQQQSTFSSQQSQSSSYDFIYSTPQIHQNSQNSQFSQNPLYDDFIHSTQNSYSQRVSSQRSYSQKSSSSQISFSQIPSSQIQSSQISSQIHSSQIPSSQNQSSQKSQFSFSQIPSSQIPSSQKRFFQSQNDDFVPSSQVTSLQDILPQPIQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQCQPQQQQTQQQQQQQQQQQQQQQQQQQQQQQQQTQQQQQQPQEDDDDYDDYDGYDNYEDFVYNEGEEGEEDYEDYEQENDDDDEDEDDDDDDDDDDDDEEEEEESQQQHIRSRALQSRSSQSRPLLRSGFKSPISRLSQTTSPEYIYISSQSNTHTNQLGQSSQQTNSPNVHFNSLQQKKKQQQQQQQQQQQQQQQQQQQQQQQQQQSQQIIGSQSSQSSQLPPTQPPVEVPVNLGRLIPINASHIPINLNLKREDRIVGRSSSCDARLIDNYLTISGKHCEIYRADNLTCLKHIPLCKDKTDCHKNFGMLIVHDISNGSYINGELIGNGKTRILRSDDILSLGHPSGDLKFIFESEFQFNFILDIKDNVNNLNENDYKKLRTAYDNARIENKNCALRDYYFVKEIGSGGYGIVYEGLYKLNGKRVAIKHIDLLKGSTSKSMELVSKEYNALKNIKHRNVIEFFDIVFSSTDCFFIVELATNDLSNLLRKRCVDDDIKRICKQLLLGFNYLHNLGIVHRDLKPENILYNEFKQGFSIKITDFGLSSFVEESQYQTFCGTPLFFAPEVIANNFFSNGYGKSCDLWSIGVTLYLSLCKYKPFIVDCRDLYHSFIGNLGFTSKKWAKISNYAKDLVRRLLVIDPEHRITIKEALNHPWFTQDRRFFKKYPKHYKRAQPKTQFFVECFNVYYDLKSETGFICFREHFDNLETNYALFKQNFDNNNNNNNNNNNNNNNNNNNNNNNNINNNNNNINNNNINNNNNNNNNNNNNTNTNNINNNNNNYNNSHNHNNNHNHNHNLNNHNHNNNHHHNHNHNHNHNHNHNHNHNHNHNHNHNHNNHNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNYYNNNINNINNNINNNINNNNNYHQQYTQHTM","methods":{"seg_default":true,"seg_intermediate":true,"seg_strict":true,"cast":true,"flps":true,"flps_strict":true,"simple":true,"gbsc":true},"enrichment":{"pfam":true,"phobius":true,"aafrequency":true},"params":{"seg":{"window":12,"k1":2.2,"k2":2.5},"cast":{"threshold":40,"matrix":1},"flps":{"min_tract_len":15,"max_tract_len":500,"pval":0.001,"regions":{"single":true,"multiple":true,"whole":false}},"simple":{"score_mono":1,"score_di":1,"score_tri":1,"score_tetra":1,"score_penta":1,"score_hexa":1,"score_hepta":1,"score_octa":1,"score_nona":1,"score_deca":1,"window":11,"num_of_rand":100,"rand_method":3,"stringency":0.9},"gbsc":{"score":3,"distance":7}}}'

    response = requests.put(url, data=data)

    return json.loads(response.text)['token']


def ask_job_state(url, token):
    url = "http://{0}/restapi/job/{1}".format(url, token)

    response = requests.get(url)
    return json.loads(response.text)['status']



def get_list_of_proteins(url, token):
    url = "http://{0}/restapi/proteins/{1}".format(url, token)

    response = requests.get(url)
    return json.loads(response.text)


def get_protein_details(url, token, id):
    url = "http://{0}/restapi/proteins/{1}/{2}".format(url, token, id)

    response = requests.get(url)
    return json.loads(response.text)


def get_options():
    parser = OptionParser()
    parser.add_option("-v", "--version", action="store_true", dest="version", default=False)
    parser.add_option("-u", "--url", dest="url", default='platoloco.aei.polsl.pl',
                      help="Url to server", metavar="URL")
    return parser.parse_args()


def main(options, args):
    token = send_query(options.url)
    print(token)
    print('')

    while True:
        status = ask_job_state(options.url, token)
        print(status)
        print('')
        if status == "FINISHED":
            break
        time.sleep(1)

    response_data = get_list_of_proteins(options.url, token)
    print(response_data)
    print('')

    protein_details = get_protein_details(options.url, token, response_data['proteins'][0]['id'])
    print(protein_details)


if __name__ == "__main__":
    options, args = get_options()
    if options.version:
        print("1.0.0")
    else:
        main(options, args)

