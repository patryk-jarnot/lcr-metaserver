

function entropyGetIntervals(regions) {
    var retval = [];
    for (var i=0; i<regions.length; i++) {
        retval.push({"x":regions[i].beg, "y":regions[i].end});
    }
    return retval;
}

function entropyAddChart(ft, entropy) {
    data = [];
    for (var i=0; i<entropy.length; i++) {
        data.push({
            x: i,
            y:entropy[i]
        })
    }
    ft.addFeature({
        data: data,
        name: "entropy",
        className: "entropy", //can be used for styling
        color: "#004c6d",
        type: "line",
        filter: "type2",
        height: "5"
    });
}
