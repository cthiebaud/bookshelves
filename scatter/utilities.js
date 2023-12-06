class _ {
    // static property to store the ellipsis character
    static ellipsis = '…'

    // truncate a string if it exceeds a maximum length, adding an ellipsis in the middle
    static truncateStringInTheMiddle(str, maxLength) {
        // return the original string if its length is less than or equal to the maximum length
        if (str.length <= maxLength) {
            return str
        }

        // calculate the number of visible characters on each side of the ellipsis
        const visibleCharacters = maxLength - _.ellipsis.length

        // extract the beginning and end substrings with visible characters
        const beginning = str.substring(0, Math.floor(visibleCharacters / 2))
        const end = str.substring(str.length - Math.floor(visibleCharacters / 2))

        // combine the substrings with the ellipsis in the middle to form the truncated string
        return `${beginning} ${_.ellipsis} ${end}`
    }

    // truncate a string if it exceeds a maximum length, using slice and appending an ellipsis at the end
    static truncateStringAtTheEnd(str, maxLength) {
        // return the original string if its length is less than or equal to the maximum length
        if (str.length <= maxLength) {
            return str
        }

        // use slice to get a substring up to the maximum length and append the shared ellipsis
        return str.slice(0, maxLength) + _.ellipsis
    }

    // check if image dimensions require squeezing based on a threshold
    static contains(theImage, squeezeThreshold) {
        const imageArea = theImage.width * theImage.height

        // check if squeeze is needed based on the product of width and height
        if (imageArea > squeezeThreshold) {
            const aspectRatio = theImage.width / theImage.height

            // calculate new dimensions
            const newWidth = Math.floor(Math.sqrt(squeezeThreshold * aspectRatio))
            const newHeight = Math.floor(squeezeThreshold / newWidth)

            return { width: newWidth, height: newHeight }
        } else {
            // if squeeze is not needed, return the original dimensions
            return { width: theImage.width, height: theImage.height }
        }
    }

    // convert an array to an object with properties x, y, and z
    static arrayToXYZObject(arr) {
        return { x: arr[0], y: arr[1], z: arr[2] }
    }

    // convert an object with properties x, y, and z to an array
    static XYZObjectToArray(obj) {
        return [obj.x, obj.y, obj.z]
    }

    // linearly normalize a value from one range to another
    static normalizeLinearly(value, inRange, outRange) {
        // check if the input range has a valid width
        if (inRange[0] === inRange[1]) {
            throw new Error('Input range has zero width')
        }

        // normalize the value from the input range to the [0, 1] range
        const normalizedValue = (value - inRange[0]) / (inRange[1] - inRange[0])

        // scale the normalized value to the output range
        const result = (normalizedValue * (outRange[1] - outRange[0])) + outRange[0]

        return result
    }

    // quadratically normalize a value from one range to another
    static normalizeQuadratically(value, inRange, outRange) {
        // check if the input range has a valid width
        if (inRange[0] === inRange[1]) {
            throw new Error('Input range has zero width')
        }

        // normalize the value from the input range to the [0, 1] range
        const normalizedValue = (value - inRange[0]) / (inRange[1] - inRange[0])

        // apply a quadratic transformation to the normalized value
        const transformedValue = normalizedValue * normalizedValue

        // scale the transformed value to the output range
        const result = (transformedValue * (outRange[1] - outRange[0])) + outRange[0]

        return result
    }
}

// export the utility class
export default _
