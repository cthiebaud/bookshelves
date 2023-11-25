import colorSpace from 'https://cdn.jsdelivr.net/npm/color-space@latest/+esm'

function scatterFromRGBArray(rgbArray, shape, j = 10) {
    let cnt = 0
    const scatter = rgbArray.filter(rgb => (
        (rgb[0] !== 0 && rgb[1] !== 0 && rgb[2] !== 0) ||
        (rgb[0] !== 255 && rgb[1] !== 255 && rgb[2] !== 255)
    )).map(rgb => {
        // Convert RGB to HSL
        const hslColor = colorSpace.rgb.hsl(rgb)
        const h = hslColor[0]; // 0...360
        const s = hslColor[1]; // 0...100
        const l = hslColor[2]; // 0...100

        let x
        let y
        let z

        const theta = normalize(h, 0, 360, 0, 2 * Math.PI)

        if (shape === "cylinder") {
            // Convert HSL to Cartesian coordinates
            const radius = normalize(s, 0, 100, 0, j)
            x = radius * Math.cos(theta)
            y = normalize(l, 0, 100, 1, -(2 * j) + 1)
            z = radius * Math.sin(theta)
        } else {
            // radius change if the point is in the upper or lower cone
            const radius = s * (l < 50 ? l : (100 - l)) / 50
            x = normalize(radius * Math.cos(theta), -127, 128, j - 1, -j)
            y = normalize(l, 0, 100, 1, -(2 * j) + 1)
            z = normalize(radius * Math.sin(theta), -127, 128, -j, j - 1)
        }
        const scat = {
            x: x,
            y: y,
            z: z,
            color: `#${H(rgb[0])}${H(rgb[1])}${H(rgb[2])}`,
            id: `_${cnt++}`,
        }
        return scat
    })
    return scatter
}

export default scatterFromRGBArray