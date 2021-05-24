

function markerDrawBg(ctx, ctx2d, width, height) {
    ctx2d.fillRect(0, 0, width, height);
}


function markerDrawRegion(ctx, ctx2d, width, height, begin, end, max) {
    var beg = begin * (width/max);
    var e = end * (width/max) - beg;
    if ((e) < 1) {e = 1;}

    ctx2d.fillRect(beg, 0, e, height);
}


function regionMarker(ctx, width, height, begin, end, max) {
    var colours = ["#fbeec8", "#FBBA00"]


    var ctx2d = ctx.getContext('2d')

    ctx2d.strokeStyle = colours[0];
    ctx2d.fillStyle = colours[0];
    markerDrawBg(ctx, ctx2d, width, height);

    ctx2d.strokeStyle = colours[1];
    ctx2d.fillStyle = colours[1];
    markerDrawRegion(ctx, ctx2d, width, height, begin, end, max);
}


