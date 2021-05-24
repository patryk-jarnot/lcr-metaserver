function pfamGetIntervals(regions, http) {
    var retval = [];
    for (var i=0; i<regions.length; i++) {
        var start = regions[i].location._attributes.start;
        var end = regions[i].location._attributes.end;
        retval.push({"x":regions[i].location._attributes.start, "y":regions[i].location._attributes.end, "description":regions[i]._attributes.accession});
    }
    return retval;
}

function pfamAddIntervals(ft, result1, http) {
    console.log(JSON.stringify(ft))

    ft.addFeature({
        data: pfamGetIntervals(result1.pfam.entry.matches.match, http),
        name: "Pfam",
        className: "pfam", //can be used for styling
        color: "#9ac6c2",
        type: "rect" // ['rect', 'path', 'line']
    });
}



function pfamFillDetails2(localScope, result) {
    localScope.pfamregions = []
    var regions = result.pfam.entry.matches.match;
    if (regions.length > 0) {
        document.getElementById('pfam_section').style.display = 'block';
        for (var i=0; i<regions.length; i++) {
            var pfamregion = {}

            pfamregion['beg'] = regions[i].location._attributes.start;
            pfamregion['end'] = regions[i].location._attributes.end;
            pfamregion['description'] = regions[i]._attributes.accession;

            localScope.pfamregions.push(pfamregion);
        }
    }
}


function pfamAddPdb(lscope, pfamregion) {
    pfamregion.pdbs = []

    var data = "<orgPdbQuery> <queryType>org.pdb.query.simple.PfamIdQuery</queryType> <description>Simple query for a list of UniprotKB Accession IDs: P50225</description> <pfamID>PF13181</pfamID> </orgPdbQuery>";

    $.post("http://www.rcsb.org/pdb/rest/search", data).done(function(data) {
        ids = data.split('\n');
        pdbIds = []
        for (i in ids) {
            pdbIds.push(ids[i].split(':')[0])
        }
        $.ajax({
            url: "http://www.rcsb.org/pdb/rest/describePDB?structureId=" + pdbIds.join(','),
            dataType: "text",
            type: "GET",
            cache: false,
        })
        .done(function(dataPdb) {
            var result1 = xml2js(dataPdb, {compact: true, spaces: 4});
            for (var i=0; i<result1.PDBdescription.PDB.length; i++) {
                var pdbItem = result1.PDBdescription.PDB[i];
                pfamregion.pdbs.push({'acc': pdbItem._attributes.structureId, 'description': pdbItem._attributes.title})
                lscope.$apply()
            }
        });
    });
}


function pfamFillDetails(http, localScope, result) {
    localScope.pfamregions = []
    var lscope = localScope;
    var regions = result.pfam.entry.matches.match;
    if (regions.length > 0) {
        for (var i=0; i<regions.length; i++) {
            var start = regions[i].location._attributes.start
            var end = regions[i].location._attributes.end;
            localScope.pfamregions.push({"beg": start, "end": end, "pfamacc": regions[i]._attributes.accession,})

            http.get('https://pfam.xfam.org/family/' + regions[i]._attributes.accession + '?output=xml').then(function(response) {
                var result1 = xml2js(response.data, {compact: true, spaces: 4});
                document.getElementById('pfam_section').style.display = 'block';
                var pfamregion = lscope.pfamregions.find(element => element.pfamacc == result1.pfam.entry._attributes.accession);
                pfamregion["description"] = result1.pfam.entry.description._cdata;

                pfamAddPdb(lscope, pfamregion);
            });
        }
    }
}
