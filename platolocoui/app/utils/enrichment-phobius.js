

function phobiusAddIntervals(ft, phobius) {
    if (typeof phobius.signals !== 'undefined') {
        ft.addFeature({
            data: phobiusGetIntervals(phobius.signals.regions),
            name: "signals",
            className: "signals", //can be used for styling
            color: "#346888",
            type: "rect" // ['rect', 'path', 'line']
        });
    }
    if (typeof phobius.transmembranes !== 'undefined') {
        ft.addFeature({
            data: phobiusGetIntervals(phobius.transmembranes.regions),
            name: "transmembranes",
            className: "transmembranes", //can be used for styling
            color: "#5886a5",
            type: "rect" // ['rect', 'path', 'line']
        });
    }
    if (typeof phobius.domains !== 'undefined') {
        ft.addFeature({
            data: phobiusGetIntervals(phobius.domains.regions),
            name: "domains",
            className: "domains", //can be used for styling
            color: "#7aa6c2",
            type: "rect" // ['rect', 'path', 'line']
        });
    }
}


function phobiusGetIntervals(regions) {
    var retval = [];
    for (var i=0; i<regions.length; i++) {
        retval.push({"x":regions[i].beg, "y":regions[i].end, "description":regions[i].description});
    }
    return retval;
}
