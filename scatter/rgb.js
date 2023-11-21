function scatterFromRGBArray(rgbArray, shape, j = 10) {
    let cnt = 0
    const scatter = rgbArray.filter(rgb => (
        (rgb[0] !== 0 && rgb[1] !== 0 && rgb[2] !== 0) ||
        (rgb[0] !== 255 && rgb[1] !== 255 && rgb[2] !== 255)
    )).map(rgb => {
        const dot = {
            x: normalize(rgb[0], 0, 255, j - 1, -j),
            y: normalize(rgb[1], 0, 255, 1, -(2 * j) + 1),
            z: normalize(rgb[2], 0, 255, -j, j - 1),
            color: `#${H(rgb[0])}${H(rgb[1])}${H(rgb[2])}`,
            id: `_${cnt++}`,
        }
        return dot
    })

    return scatter
}

export default scatterFromRGBArray