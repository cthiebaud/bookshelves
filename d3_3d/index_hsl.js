import * as d3 from 'https://cdn.jsdelivr.net/npm/d3@7.8/+esm';
import { _3d } from 'https://cdn.jsdelivr.net/npm/d3-3d@0.1.3/+esm';
import colorSpace from 'https://cdn.jsdelivr.net/npm/color-space@latest/+esm'

let origin = [320, 480],
    unit = 2,
    j = 5 * unit,
    scale = 2 * j,
    scatter = [],
    yLine = [],
    xGrid = [],
    key = (d) => d.id,
    startAngle = Math.PI / 4,
    startAngleY = Math.PI / 4;

let svg = d3
    .select("svg")
    .append("g");

let grid3d = _3d()
    .shape("GRID", 20)
    .origin([320, 480])
    .rotateY(startAngleY)
    .rotateX(-startAngle)
    .scale(scale)

let point3d = _3d()
    .x((d) => d.x)
    .y((d) => d.y)
    .z((d) => d.z)
    .origin(origin)
    .rotateY(startAngleY)
    .rotateX(-startAngle)
    .scale(scale);

let yScale3d = _3d()
    .shape("LINE_STRIP")
    .origin(origin)
    .rotateY(startAngleY)
    .rotateX(-startAngle)
    .scale(scale);

function processData(data, tt) {
    /* ----------- GRID ----------- */

    let xGrid = svg.selectAll("path.grid").data(data[0], key);

    xGrid
        .enter()
        .append("path")
        .attr("class", "_3d grid")
        .attr("stroke", "gray")
        .attr("stroke-width", 0.3)
        .attr("fill", "#f7f7f7")
        .attr("fill-opacity", 0.1)
        .attr("d", grid3d.draw);

    xGrid.exit().remove();

    /* ----------- POINTS ----------- */

    let points = svg.selectAll("circle").data(data[1], key);

    points
        .enter()
        .append("circle")
        .attr("class", "_3d")
        .attr("r", 2)
        .attr("fill", d => d.color)
        .attr("opacity", ".4ì1")
        .attr("cx", posPointX)
        .attr("cy", posPointY);

    points.exit().remove();

    /* ----------- y-Scale ----------- */

    let yScale = svg.selectAll("path.yScale").data(data[2]);

    yScale
        .enter()
        .append("path")
        .attr("class", "_3d yScale")
        .attr("stroke", "#404040")
        .attr("stroke-width", 0.5)
        .attr("d", yScale3d.draw);

    yScale.exit().remove();

    d3.selectAll("._3d").sort(_3d().sort);
}

const posPointX = (d) => d.projected.x
const posPointY = (d) => d.projected.y

function init(rgbArray) {
    (xGrid = []), /*(scatter = []), */(yLine = []);
    for (let z = -j; z < j; z++) {
        for (let x = -j; x < j; x++) {
            xGrid.push([x, 1, z]);
        }
    }

    d3.range(-1, 2 * j, 1).forEach(function (d) {
        yLine.push([-j, -d, -j]);
    });

    let data = [grid3d(xGrid), point3d(rgbArray), yScale3d([yLine])];
    processData(data, 1000);
}

function normalize(value, fromSrc, toSrc, fromTarget, toTarget) {
    // Calculate the percentage of the value in the source range
    const percentage = (value - fromSrc) / (toSrc - fromSrc)

    // Map the percentage to the target range and return the result
    const normalized = (fromTarget + percentage * (toTarget - fromTarget))
    return normalized // Math.round( normal * 10) / 10
}

window.handleImageUpload = function () {
    let params = new URLSearchParams(window.location.search);
    let imageUrl = params.get('image');
    let type = params.get('type');

    if (imageUrl) {
        let img = document.getElementById('selectedImage');

        img.src = imageUrl;

        // Wait for the image to fully load
        const afterImageLoaded = () => {
            // Get the pixel data from the image
            let canvas = document.createElement('canvas');
            let ctx = canvas.getContext('2d');
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0, img.width, img.height);
            let imageData = ctx.getImageData(0, 0, img.width, img.height);

            let rgbArray = [];
            for (let i = 0; i < imageData.data.length; i += 4) {
                let rgb = [imageData.data[i], imageData.data[i + 1], imageData.data[i + 2]];
                // let lab = colorSpace.rgb.lab(rgb);
                rgbArray.push(rgb);
            }

            const H = n => n.toString(16).padStart(2, '0')

            let cnt = 0;
            scatter = []
            scatter = rgbArray.map(rgb => {
                // Convert RGB to HSL
                const hslColor = colorSpace.rgb.hsl(rgb);
                const h = hslColor[0]; // 0...360
                const s = hslColor[1]; // 0...100
                const l = hslColor[2]; // 0...100

                let x
                let y
                let z

                const theta = normalize(h, 0, 360, 0, 2 * Math.PI);

                if (type == "cylinder") {
                    // Convert HSL to Cartesian coordinates
                    const radius = normalize(s, 0, 100, 0, j);
                    x = radius * Math.cos(theta);
                    y = normalize(l, 0, 100, 1, -(2 * j) + 1);
                    z = radius * Math.sin(theta)
                } else {
                    // radius change if the point is in the upper or lower cone
                    const radius = s * (l < 50 ? l : (100 - l) ) / 50
                    x = normalize(radius * Math.cos(theta), -127, 128, j - 1, -j)
                    y = normalize(l, 0, 100, 1, -(2 * j) + 1);
                    z = normalize(radius * Math.sin(theta), -127, 128, -j, j - 1)
                }
                const qwe = {
                    x: x,
                    y: y,
                    z: z,
                    color: `#${H(rgb[0])}${H(rgb[1])}${H(rgb[2])}`,
                    id: `_${cnt++}`,
                };
                return qwe;
            })
            init(scatter);
        }

        img.addEventListener('load', () => {
            setTimeout(afterImageLoaded, 10)
        })

    } else {
        console.error("Image URL not provided in the query string.");
    }
}

document.addEventListener('DOMContentLoaded', window.handleImageUpload);
