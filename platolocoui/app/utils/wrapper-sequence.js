

function wrapperGetIntervals(regions, sequence) {
    var retval = [];
    for (var i=0; i<regions.length; i++) {
        retval.push({"x":regions[i].beg, "y":regions[i].end});
    }
    return retval;
}


function wrapperAddIntervals(ft, wrapper, sequence) {
    var colours = ["#003f5c" ,"#2f4b7c" ,"#665191" ,"#a05195" ,"#d45087" ,"#f95d6a" ,"#ff7c43" ,"#ffa600"];

    for (var i=0; i<wrapper.length; i++) {
        ft.addFeature({
            data: wrapperGetIntervals(wrapper[i].regions, sequence),
            name: wrapper[i].method.replace('_', '-'),
            className: wrapper[i].method, //can be used for styling
            color: colours[i],
            type: "rect" // ['rect', 'path', 'line']
        });
    }
}


function createGaps(seqList) {
    for (var i=0; i<seqList.length; i+=10) {
        if (i % 60 == 0) {
            seqList[i] = "<br/>" + seqList[i];
        } else if (i % 10 == 0) {
            seqList[i] = " " + seqList[i];
        }
    }
    return seqList;
}


function highlightSequence(seqList, intervals) {
    var htmlBegin = '<font color=red>';
    var htmlEnd = '</font>';

    for (var i=intervals.length-1; i>=0; i--) {
        seqList[intervals[i].beg-1] = htmlBegin + seqList[intervals[i].beg - 1]
        seqList[intervals[i].end-1] = seqList[intervals[i].end - 1] + htmlEnd;
    }
    return seqList;
}


function processMethods(requestData) {
    var wrapper = requestData.data.wrapper;
    var retval = [];
    for (var i=0; i<wrapper.length; i++) {
        var regions = wrapper[i].regions;
        var method = wrapper[i].method;
        var seqList = (' ' + requestData.sequence).slice(1).split("");
        retval.push({"method": method, "sequence": seqList.join(""), "regions": regions})
    }
    return retval;
}


function wrapperIsOverlap(region1, region2) {
    return (region1.beg <= region2.end) && (region1.end >= region2.beg) || ((region2.beg <= region1.end) && (region2.end >= region1.beg));
}


function mergeMethodRegions(method) {
    var regions = []
    for (var i=0; i<method.regions.length; i++) {
        var isOverlap = false;
        for (var j=0; j<regions.length; j++) {
            if (wrapperIsOverlap(method.regions[i], regions[j])) {
                regions[j] = {'beg': Math.min(method.regions[i].beg, regions[j].beg), 'end': Math.max(method.regions[i].end, regions[j].end)}
                isOverlap = true;
            }
        }
        if (!isOverlap) {
            regions.push(method.regions[i]);
        }
    }
    return regions;
}


function wrapContains(ilist, ielem) {
    for (var i=0; i<ilist.length; i++) {
        if ( (ilist[i].beg == ielem.beg) && (ilist[i].end == ielem.end) ) {
            return true;
        }
    }
    return false;
}


function mergeRegions(methods, type, maxLen) {
    retval = null
    selectedMethods = []
    for (var i=0; i<methods.length; i++) {
        if (methods[i].isSelected == true) {
            selectedMethods.push(methods[i]);
        }
    }
    if (type == "intersection") {
        for (var i=0; i<selectedMethods.length; i++) {
            var retval_new = []
            methodRegions = mergeMethodRegions(selectedMethods[i])
            if (retval == null) {
                retval = methodRegions;
                continue;
            }

            retvalit = 0;
            methodsit = 0;
            for (var l=0; l<methodRegions.length; l++) {
                for (var k=0; k<retval.length; k++) {
                    if (wrapperIsOverlap(retval[k], methodRegions[l])) {
                        var beg = Math.max(retval[k].beg, methodRegions[l].beg);
                        var end = Math.min(maxLen, Math.min(retval[k].end, methodRegions[l].end));
                        retval_new.push({'beg': beg, 'end': end})
                    }
                }
            }
            retval = retval_new.slice();
        }
    }
    else if (type == "sum") {
        var highlightChars = new Array(maxLen).fill(false);
        for (var i=0; i<selectedMethods.length; i++) {
            var method = selectedMethods[i];
            for (var j=0; j<method.regions.length; j++) {
                var region = method.regions[j];
                for (var k=region.beg; k<region.end && k < highlightChars.length; k++) {
                    highlightChars[k] = true;
                }
            }
        }
        var retval = []
        var curItem = {'beg': -1, 'end': -1}
        for (var i=0; i<highlightChars.length; i++) {
            if (curItem.beg == -1 && highlightChars[i]) {
                curItem.beg = i;
            }
            if (curItem.end == -1 && !highlightChars[i]) {
                curItem.end = i;
                retval.push(curItem);
                curItem = {'beg': -1, 'end': -1}
            }
        }
        if (curItem.beg != -1 && curItem.end == -1) {
            curItem.end = highlightChars.length;
            retval.push(curItem);
        }
    }
    if (retval == null) {
        retval = []
    }


    return retval;
}


function createConsensusSequence(sequence, methods, type) {
    var seqList = sequence.split("");
    var regions = mergeRegions(methods, type, sequence.length)
    seqList = highlightSequence(seqList, regions)
    seqList = createGaps(seqList);
    return { sequence: seqList.join(""), regions: regions };
}





