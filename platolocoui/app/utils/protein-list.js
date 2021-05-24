
/**
 * Draws a rounded rectangle using the current state of the canvas.
 * If you omit the last three params, it will draw a rectangle
 * outline with a 5 pixel border radius
 * @param {CanvasRenderingContext2D} ctx
 * @param {Number} x The top left x coordinate
 * @param {Number} y The top left y coordinate
 * @param {Number} width The width of the rectangle
 * @param {Number} height The height of the rectangle
 * @param {Number} [radius = 5] The corner radius; It can also be an object
 *                 to specify different radii for corners
 * @param {Number} [radius.tl = 0] Top left
 * @param {Number} [radius.tr = 0] Top right
 * @param {Number} [radius.br = 0] Bottom right
 * @param {Number} [radius.bl = 0] Bottom left
 * @param {Boolean} [fill = false] Whether to fill the rectangle.
 * @param {Boolean} [stroke = true] Whether to stroke the rectangle.
 */
function roundRect(ctx, x, y, width, height, radius, fill, stroke, strokeColor) {
  if (typeof stroke === 'undefined') {
    stroke = true;
  }
  if (typeof radius === 'undefined') {
    radius = 5;
  }
  if (typeof radius === 'number') {
    radius = {tl: radius, tr: radius, br: radius, bl: radius};
  } else {
    var defaultRadius = {tl: 0, tr: 0, br: 0, bl: 0};
    for (var side in defaultRadius) {
      radius[side] = radius[side] || defaultRadius[side];
    }
  }
  ctx.beginPath();
  ctx.moveTo(x + radius.tl, y);
  ctx.lineTo(x + width - radius.tr, y);
  ctx.quadraticCurveTo(x + width, y, x + width, y + radius.tr);
  ctx.lineTo(x + width, y + height - radius.br);
  ctx.quadraticCurveTo(x + width, y + height, x + width - radius.br, y + height);
  ctx.lineTo(x + radius.bl, y + height);
  ctx.quadraticCurveTo(x, y + height, x, y + height - radius.bl);
  ctx.lineTo(x, y + radius.tl);
  ctx.quadraticCurveTo(x, y, x + radius.tl, y);
  ctx.closePath();
  if (fill) {
    ctx.fill();
  }
  if (stroke) {
    ctx.stroke();
  }

}

function protListIsOverlap(beg, end, region) {
    return (beg < region[1]) && (end > region[0]);
}


function protListDivideRegoinsToDraw(regions, seqLength, width) {
    var retval = []
    var intervalCount = Math.ceil(seqLength/width);
    for (var i=0; i<intervalCount; i++) {
        retval.push([])
    }

    var curRegion = 0;
    var curInterval = 0;
    while (curInterval < intervalCount) {
        var beg = curInterval * width+1;
        var end = Math.min((curInterval+1) * width, seqLength);
        while (curRegion < regions.length && regions[curRegion][1] < beg) { curRegion++; }
        if (curRegion >= regions.length) {
            break;
        }

        while (curRegion < regions.length && protListIsOverlap(beg, end, regions[curRegion])) {
            retval[curInterval].push([Math.max(beg, regions[curRegion][0]), Math.min(end, regions[curRegion][1])])

            if (end <= regions[curRegion][1]) {
                curInterval++;
                break;
            }

            if (curRegion < regions.length && regions[curRegion][1] < end) { curRegion++; }
        }
        if (curRegion >= regions.length) {
            break;
        }
        if (!protListIsOverlap(beg, end, regions[curRegion])) {
            curInterval++;
        }
    }
    return retval;
}


function protListDrawLine(ctx, ctx2d, lineNum, width, linePadding, totalLen, strokeColor, lineDistance) {
    var beg = (lineNum-1) * width+1;
    var end = lineNum * width < totalLen ? lineNum * width : totalLen;
    var lineLen = ctx.width-linePadding*2;
    var scale = lineLen / (width-1);

    ctx2d.fillStyle = strokeColor;
    ctx2d.beginPath();
    ctx2d.moveTo(linePadding, lineDistance*lineNum)
    ctx2d.lineTo(linePadding + (end-beg) * scale, lineDistance*lineNum)
    ctx2d.strokeStyle = strokeColor;
    ctx2d.stroke();
    ctx2d.font = "12px Arial";
    ctx2d.textAlign = "end";
    ctx2d.fillStyle = "#000000";
    ctx2d.fillText(beg, linePadding-6, lineDistance*lineNum+3);
    ctx2d.textAlign = "start";
    ctx2d.fillText(end, ctx.width-linePadding+6, lineDistance*lineNum+3);
    ctx2d.fillStyle = strokeColor;
}


function protListCanvasHeight(ctx, lines, lineDistance) {
    ctx.height = lines * lineDistance + lineDistance;
}


function protListDrawRegion(ctx, ctx2d, lineNum, regInterval, width, linePadding, rectHeight, strokeColor, lineDistance) {
    var totalHeight = lineDistance
    var startPos = (lineNum-1) * width + 1;
    var lineLen = ctx.width-linePadding*2;
    var scale = lineLen / (width-1);
    var x = linePadding + (regInterval[0] - startPos) * scale;
    var y =  totalHeight * lineNum - rectHeight/2;
    var w = (regInterval[1] - regInterval[0]) * scale;
    var h = rectHeight;
    roundRect(ctx2d, x,y,w,h,1,true, true, strokeColor);
}

function protListDrawLineMethods(ctx, ctx2d, lineNum, width, linePadding, totalLen, strokeColor, lineDistance) {
    var beg = 1;
    var end =  totalLen;
    var lineLen = ctx.width-linePadding*2;
    var scale = lineLen / (width-1);

    ctx2d.fillStyle = strokeColor;
    ctx2d.beginPath();
    ctx2d.moveTo(linePadding, lineDistance*lineNum)
    ctx2d.lineTo(linePadding + (end-beg) * scale, lineDistance*lineNum)
    ctx2d.strokeStyle = strokeColor;
    ctx2d.stroke();
    ctx2d.font = "12px Arial";
    ctx2d.textAlign = "end";
    ctx2d.fillStyle = "#000000";
    ctx2d.fillText(1, linePadding-6, lineDistance*lineNum+3);
    ctx2d.textAlign = "start";
    ctx2d.fillText(totalLen, ctx.width-linePadding+6, lineDistance*lineNum+3);
    ctx2d.fillStyle = strokeColor;
}

function protListDrawMethodName(ctx, ctx2d, lineNum, width, linePadding, totalLen, strokeColor, lineDistance, methodName) {
    var beg = 1;
    var end =  totalLen;
    var lineLen = ctx.width-linePadding*2;
    var scale = lineLen / (width-1);

    ctx2d.fillStyle = strokeColor;
    ctx2d.font = "12px Arial";
    ctx2d.textAlign = "start";
    ctx2d.fillStyle = "#000000";
    ctx2d.fillText(methodName, 6, lineDistance*lineNum+3);
}

function protListDrawRegionMethods(ctx, ctx2d, lineNum, regInterval, width, linePadding, rectHeight, strokeColor, lineDistance) {
    var totalHeight = lineDistance
    var startPos = 1;
    var lineLen = ctx.width-linePadding*2;
    var scale = lineLen / (width-1);
    var x = linePadding + (regInterval[0] - startPos) * scale;
    var y =  totalHeight * lineNum - rectHeight/2;
    var w = (regInterval[1] - regInterval[0]) * scale;
    var h = rectHeight;
    roundRect(ctx2d, x,y,w,h,1,true, true, strokeColor);
}

function countMethods(prot) {
    var j = 0;
    if (typeof prot.SEG !== 'undefined') {
        j++;
    }
    if (typeof prot.SEG_strict !== 'undefined') {
        j++;
    }
    if (typeof prot.SEG_intermediate !== 'undefined') {
        j++;
    }
    if (typeof prot.CAST !== 'undefined') {
        j++;
    }
    if (typeof prot.fLPS !== 'undefined') {
        j++;
    }
    if (typeof prot.fLPS_strict !== 'undefined') {
        j++;
    }
    if (typeof prot.simple !== 'undefined') {
        j++;
    }
    if (typeof prot.GBSC !== 'undefined') {
        j++;
    }
    return j;
}

function proteinListAddMethods(ctx, prot, maxLen) {
    var colours = ["#003f5c" ,"#2f4b7c" ,"#665191" ,"#a05195" ,"#d45087" ,"#f95d6a" ,"#ff7c43" ,"#ffa600"];
    var linePaddingWidth = 100;
    var ctx2d = ctx.getContext('2d')
    var last_end = 0;
    var cur_region = 0;
    var lineLen = prot.length;
    if (maxLen > -1)
        lineLen = maxLen;
    var rectHeight = 12;
    var lineDistance = 16;
    var strokeColor = '#A7CCFF';
    ctx2d.strokeStyle = strokeColor;
    ctx2d.fillStyle = strokeColor;

    protListCanvasHeight(ctx, countMethods(prot), lineDistance);
    var j = 0;
    if (typeof prot.SEG !== 'undefined') {
        protListDrawMethodName(ctx, ctx2d, j+1, lineLen, linePaddingWidth, prot.length, colours[j], lineDistance, 'SEG');
        protListDrawLineMethods(ctx, ctx2d, j+1, lineLen, linePaddingWidth, prot.length, colours[j], lineDistance);
        for (var k=0; k<prot.SEG.length; k++) {
            protListDrawRegionMethods(ctx, ctx2d, j+1, prot.SEG[k], lineLen, linePaddingWidth, rectHeight, colours[j], lineDistance)
        }
        j++;
    }
    if (typeof prot.SEG_strict !== 'undefined') {
        protListDrawMethodName(ctx, ctx2d, j+1, lineLen, linePaddingWidth, prot.length, colours[j], lineDistance, 'SEG-strict');
        protListDrawLineMethods(ctx, ctx2d, j+1, lineLen, linePaddingWidth, prot.length, colours[j], lineDistance);
        for (var k=0; k<prot.SEG_strict.length; k++) {
            protListDrawRegionMethods(ctx, ctx2d, j+1, prot.SEG_strict[k], lineLen, linePaddingWidth, rectHeight, colours[j], lineDistance)
        }
        j++;
    }
    if (typeof prot.SEG_intermediate !== 'undefined') {
        protListDrawMethodName(ctx, ctx2d, j+1, lineLen, linePaddingWidth, prot.length, colours[j], lineDistance, 'SEG-intermed.');
        protListDrawLineMethods(ctx, ctx2d, j+1, lineLen, linePaddingWidth, prot.length, colours[j], lineDistance);
        for (var k=0; k<prot.SEG_intermediate.length; k++) {
            protListDrawRegionMethods(ctx, ctx2d, j+1, prot.SEG_intermediate[k], lineLen, linePaddingWidth, rectHeight, colours[j], lineDistance)
        }
        j++;
    }
    if (typeof prot.CAST !== 'undefined') {
        protListDrawMethodName(ctx, ctx2d, j+1, lineLen, linePaddingWidth, prot.length, colours[j], lineDistance, 'CAST');
        protListDrawLineMethods(ctx, ctx2d, j+1, lineLen, linePaddingWidth, prot.length, colours[j], lineDistance);
        for (var k=0; k<prot.CAST.length; k++) {
            protListDrawRegionMethods(ctx, ctx2d, j+1, prot.CAST[k], lineLen, linePaddingWidth, rectHeight, colours[j], lineDistance)
        }
        j++;
    }
    if (typeof prot.fLPS !== 'undefined') {
        protListDrawMethodName(ctx, ctx2d, j+1, lineLen, linePaddingWidth, prot.length, colours[j], lineDistance, 'fLPS');
        protListDrawLineMethods(ctx, ctx2d, j+1, lineLen, linePaddingWidth, prot.length, colours[j], lineDistance);
        for (var k=0; k<prot.fLPS.length; k++) {
            protListDrawRegionMethods(ctx, ctx2d, j+1, prot.fLPS[k], lineLen, linePaddingWidth, rectHeight, colours[j], lineDistance)
        }
        j++;
    }
    if (typeof prot.fLPS_strict !== 'undefined') {
        protListDrawMethodName(ctx, ctx2d, j+1, lineLen, linePaddingWidth, prot.length, colours[j], lineDistance, 'fLPS-strict');
        protListDrawLineMethods(ctx, ctx2d, j+1, lineLen, linePaddingWidth, prot.length, colours[j], lineDistance);
        for (var k=0; k<prot.fLPS_strict.length; k++) {
            protListDrawRegionMethods(ctx, ctx2d, j+1, prot.fLPS_strict[k], lineLen, linePaddingWidth, rectHeight, colours[j], lineDistance)
        }
        j++;
    }
    if (typeof prot.simple !== 'undefined') {
        protListDrawMethodName(ctx, ctx2d, j+1, lineLen, linePaddingWidth, prot.length, colours[j], lineDistance, 'SIMPLE');
        protListDrawLineMethods(ctx, ctx2d, j+1, lineLen, linePaddingWidth, prot.length, colours[j], lineDistance);
        for (var k=0; k<prot.simple.length; k++) {
            protListDrawRegionMethods(ctx, ctx2d, j+1, prot.simple[k], lineLen, linePaddingWidth, rectHeight, colours[j], lineDistance)
        }
        j++;
    }
    if (typeof prot.GBSC !== 'undefined') {
        protListDrawMethodName(ctx, ctx2d, j+1, lineLen, linePaddingWidth, prot.length, colours[j], lineDistance, 'GBSC');
        protListDrawLineMethods(ctx, ctx2d, j+1, lineLen, linePaddingWidth, prot.length, colours[j], lineDistance);
        for (var k=0; k<prot.GBSC.length; k++) {
            protListDrawRegionMethods(ctx, ctx2d, j+1, prot.GBSC[k], lineLen, linePaddingWidth, rectHeight, colours[j], lineDistance)
        }
        j++;
    }
}


function proteinListAddRanges(ctx, prot) {
    var colours = ["#003f5c" ,"#2f4b7c" ,"#665191" ,"#a05195" ,"#d45087" ,"#f95d6a" ,"#ff7c43" ,"#ffa600"];
    var linePaddingWidth = 100;
    var ctx2d = ctx.getContext('2d')
    var last_end = 0;
    var cur_region = 0;
    var lineLen = 60;
    var rectHeight = 12;
    var lineDistance = 16;
    var strokeColor = '#A7CCFF';
    ctx2d.strokeStyle = strokeColor;
    ctx2d.fillStyle = strokeColor;


    regionsToDraw = protListDivideRegoinsToDraw(prot.regions, prot.length, lineLen);
    protListCanvasHeight(ctx, regionsToDraw.length, lineDistance);

    for (var j=0; j<regionsToDraw.length; j++) {
        protListDrawLine(ctx, ctx2d, j+1, lineLen, linePaddingWidth, prot.length, colours[0], lineDistance);
        var regsInterval = regionsToDraw[j];
        if (regsInterval.length == 0) {
            continue;
        }
        for (var k=0; k<regsInterval.length; k++) {
            protListDrawRegion(ctx, ctx2d, j+1, regsInterval[k], lineLen, linePaddingWidth, rectHeight, colours[0], lineDistance)
        }
    }
}



