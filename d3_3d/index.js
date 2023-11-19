import * as d3 from 'https://cdn.jsdelivr.net/npm/d3@7.8/+esm';
import { _3d } from 'https://cdn.jsdelivr.net/npm/d3-3d@0.1.3/+esm';
import colorSpace from 'https://cdn.jsdelivr.net/npm/color-space@latest/+esm'
var origin = [300, 360],
  j = 10,
  scale = 12,
  scatter = [],
  yLine = [],
  xGrid = [],
  beta = 0,
  alpha = 0,
  key = function (d) {
    return d.id;
  },
  startAngle = Math.PI / 6,
  startAngleY = 7*Math.PI / 4;
var svg = d3
  .select("svg")
  .call(d3.drag().on("drag", dragged).on("start", dragStart).on("end", dragEnd))
  .append("g");
var color = d3.scaleOrdinal(d3.schemeCategory10);
var mx, my, mouseX, mouseY;

var grid3d = _3d()
  .shape("GRID", 20)
  .origin(origin)
  .rotateY(startAngleY)
  .rotateX(-startAngle)
  .scale(scale);

var point3d = _3d()
  .x(function (d) {
    return d.x;
  })
  .y(function (d) {
    return d.y;
  })
  .z(function (d) {
    return d.z;
  })
  .origin(origin)
  .rotateY(startAngleY)
  .rotateX(-startAngle)
  .scale(scale);

var yScale3d = _3d()
  .shape("LINE_STRIP")
  .origin(origin)
  .rotateY(startAngleY)
  .rotateX(-startAngle)
  .scale(scale);

function processData(data, tt) {
  /* ----------- GRID ----------- */

  var xGrid = svg.selectAll("path.grid").data(data[0], key);

  xGrid
    .enter()
    .append("path")
    .attr("class", "_3d grid")
    .merge(xGrid)
    .attr("stroke", "lightgreen")
    .attr("stroke-width", 0.3)
    .attr("fill", "lightgrey")
    .attr("fill-opacity", 0.9)
    .attr("d", grid3d.draw);

  xGrid.exit().remove();

  /* ----------- POINTS ----------- */

  var points = svg.selectAll("circle").data(data[1], key);

  points
    .enter()
    .append("circle")
    .attr("class", "_3d")
    .attr("opacity", 0)
    .attr("cx", posPointX)
    .attr("cy", posPointY)
    .merge(points)
    .transition()
    /* .duration(tt) */
    .attr("r", 2)
    /*.attr("stroke", function (d) {
      return d3.color(color(d.id)).darker(3);
    })*/
    .attr("fill", d => d.color)
    /* .style("fill", d => `#${d[0]}${d[1]}${d[2]}`) */
    .attr("opacity", 1)
    .attr("cx", posPointX)
    .attr("cy", posPointY);

  points.exit().remove();

  /* ----------- y-Scale ----------- */

  var yScale = svg.selectAll("path.yScale").data(data[2]);

  yScale
    .enter()
    .append("path")
    .attr("class", "_3d yScale")
    .merge(yScale)
    .attr("stroke", "black")
    .attr("stroke-width", 0.5)
    .attr("d", yScale3d.draw);

  yScale.exit().remove();

  /* ----------- y-Scale Text ----------- */
  /*
  var yText = svg.selectAll("text.yText").data(data[2][0]);

  yText
    .enter()
    .append("text")
    .attr("class", "_3d yText")
    .attr("dx", ".3em")
    .merge(yText)
    .each(function (d) {
      d.centroid = { x: d.rotated.x, y: d.rotated.y, z: d.rotated.z };
    })
    .attr("x", function (d) {
      return d.projected.x;
    })
    .attr("y", function (d) {
      return d.projected.y;
    })
    .text(function (d) {
      return d[1] <= 0 ? d[1] : "";
    });

  yText.exit().remove();
  */
  d3.selectAll("._3d").sort(_3d().sort);
}

function posPointX(d) {
  return d.projected.x;
}

function posPointY(d) {
  return d.projected.y;
}

function init(rgbArray) {
  var cnt = 0;
  (xGrid = []), /*(scatter = []), */(yLine = []);
  for (var z = -j; z < j; z++) {
    for (var x = -j; x < j; x++) {
      xGrid.push([x, 1, z]);
      /*
      scatter.push({
        x: x,
        y: d3.randomUniform(0, -10)(),
        z: z,
        id: "point_" + cnt++
      }); */
    }
  }

  d3.range(-1, 20, 1).forEach(function (d) {
    yLine.push([-j, -d, -j]);
  });

  var data = [grid3d(xGrid), point3d(rgbArray), yScale3d([yLine])];
  processData(data, 1000);
}

function dragStart(e) {
  mx = e.x;
  my = e.y;
}

function dragged(e) {
  mouseX = mouseX || 0;
  mouseY = mouseY || 0;
  beta = ((e.x - mx + mouseX) * Math.PI) / 230;
  alpha = (((e.y - my + mouseY) * Math.PI) / 230) * -1;
  var data = [
    grid3d.rotateY(beta + startAngle).rotateX(alpha - startAngle)(xGrid),
    point3d.rotateY(beta + startAngle).rotateX(alpha - startAngle)(scatter),
    yScale3d.rotateY(beta + startAngle).rotateX(alpha - startAngle)([yLine])
  ];
  processData(data, 0);
}

function dragEnd(e) {
  mouseX = e.x - mx + mouseX;
  mouseY = e.y - my + mouseY;
}

/*
d3.selectAll("button").on("click", init);

init();
*/

function normalize(value, fromSrc, toSrc, fromTarget, toTarget) {
  // Ensure that the value is within the source range
  // value = Math.min(Math.max(value, fromSrc), toSrc);

  // Calculate the percentage of the value in the source range
  const percentage = (value - fromSrc) / (toSrc - fromSrc)

  // Map the percentage to the target range and return the result
  const normal =(fromTarget + percentage * (toTarget - fromTarget))
  return normal // Math.round( normal * 10) / 10
}

window.handleImageUpload = function () {
  var params = new URLSearchParams(window.location.search);
  var imageUrl = params.get('image');

  if (imageUrl) {
    var img = document.getElementById('selectedImage');

    img.src = imageUrl;

    // Wait for the image to fully load
    img.addEventListener('load', function () {
      // Get the pixel data from the image
      var canvas = document.createElement('canvas');
      var ctx = canvas.getContext('2d');
      canvas.width = img.width;
      canvas.height = img.height;
      ctx.drawImage(img, 0, 0, img.width, img.height);
      var imageData = ctx.getImageData(0, 0, img.width, img.height);

      // Convert pixel data to RGB then lab array
      var rgbArray = [];
      for (var i = 0; i < imageData.data.length; i += 4) {
        var rgb = [imageData.data[i], imageData.data[i + 1], imageData.data[i + 2]];
        // var lab = colorSpace.rgb.lab(rgb);
        rgbArray.push(rgb);
      }

      const h = n => n.toString(16).padStart(2, '0')

      let ii = 0;
      const colors = []
      scatter = rgbArray.map(rgb => {
        const qwe = {
          x: normalize(rgb[0], 0, 255, j-1, -j-1),
          y: normalize(rgb[1], 0, 255, 1, -20),
          z: normalize(rgb[2], 0, 255, -j, j),
          id: `_${ii++}`,
          color: `#${h(rgb[0])}${h(rgb[1])}${h(rgb[2])}`
        }
        colors.push(qwe.color)
        return qwe
      })
      colors.sort()
      console.log(colors)

      // Create 3D scatter plot
      /* createRGBScatterPlot(rgbArray); */
      init(scatter);
    });
  } else {
    console.error("Image URL not provided in the query string.");
  }
}

document.addEventListener('DOMContentLoaded', function () {
  // Call handleImageUpload on document load
  window.handleImageUpload();
});
