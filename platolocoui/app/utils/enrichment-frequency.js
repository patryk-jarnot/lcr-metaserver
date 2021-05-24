

function enrichmentPushData(data, label, db_freq) {
        if (label in db_freq) {
            data.push(db_freq[label])
        }
        else {
            data.push(0)
        }
}


function enrichmentGetLabels(aaFreq, swissFreq) {
    var labels = []
    for (var key in swissFreq) {
        if (!(labels.indexOf(key) >= 0)) {
            labels.push(key)
        }
    }
    for (var key in aaFreq) {
        if (!(labels.indexOf(key) >= 0)) {
            labels.push(key)
        }
    }
    labels.sort()
    return labels;
}


function enrichmentToChartData(enrichment) {
    var data = [[],[],[],[], []]
    var labels = enrichmentGetLabels(enrichment.aa_frequency, enrichment.swiss_frequency)

    for (var i=0; i<labels.length; i++) {
        enrichmentPushData(data[0], labels[i], enrichment.aa_frequency);
        enrichmentPushData(data[1], labels[i], enrichment.swiss_frequency);
        enrichmentPushData(data[2], labels[i], enrichment.next_frequency);
        enrichmentPushData(data[3], labels[i], enrichment.dis_frequency);
        enrichmentPushData(data[4], labels[i], enrichment.pdb_frequency);
    }
    return [labels, data]
}


function enrichmentGetAaFreq(sequence) {
    var tabu_list = ['B', 'J', 'O', 'U', 'X', 'Z']
    counts = {}
    total_count = 0
    for (var i in sequence) {
        l = sequence[i]
        if (l in tabu_list) {
            continue;
        }
        total_count += 1
        if (l in counts) {
            counts[l] += 1
        }
        else {
            counts[l] = 1
        }
    }

    for (var k in counts) {
        var frequency = counts[k] / total_count
        counts[k] = Math.round(frequency * 10000) / 10000
    }
    return counts;
}


function recalculateSequenceFreq(sequence, enrichment) {
    var localAaFreq = enrichmentGetAaFreq(sequence);
    var labels = enrichmentGetLabels(enrichment.aa_frequency, enrichment.swiss_frequency)
    data = [];
    for (var i=0; i<labels.length; i++) {
        enrichmentPushData(data, labels[i], localAaFreq);
    }
    return data;
}


function aafreqAddRowCsv(label, dbName, frequencies) {
    var freq = 0;
    if (label in frequencies) {
    freq = frequencies[label]
    }
    return label + ";" + dbName + ";" + freq + "\n";
}


function aafreqCreateCsv(enrichment, sequence, begin, end) {
    var localAaFreq = enrichmentGetAaFreq(sequence.substring(begin, end));
    var labels = enrichmentGetLabels(enrichment.aa_frequency, enrichment.swiss_frequency)
    data = "Amino acid;Database;Frequency\n";

    for (var i=0; i<labels.length; i++) {
        data += aafreqAddRowCsv(labels[i], "Sequence", localAaFreq);
        data += aafreqAddRowCsv(labels[i], "SwissProt", enrichment.swiss_frequency);
        data += aafreqAddRowCsv(labels[i], "nextProt", enrichment.next_frequency);
        data += aafreqAddRowCsv(labels[i], "DisProt", enrichment.dis_frequency);
        data += aafreqAddRowCsv(labels[i], "PDB", enrichment.pdb_frequency);
    }
    return data;
}

