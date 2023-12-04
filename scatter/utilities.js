import glob from './globals.js'

class _ {
    static truncateString(str, maxLength) {
        if (str.length <= maxLength) {
            return str
        }

        const ellipsis = '…'
        const visibleCharacters = maxLength - ellipsis.length

        const beginning = str.substring(0, visibleCharacters / 2)
        const end = str.substring(str.length - visibleCharacters / 2)

        return beginning + ellipsis + end
    }

    static truncateString0(str, maxLength) {
        if (str.length <= maxLength) {
            return str
        } else {
            return str.slice(0, maxLength) + '…'
        }
    }

    static coerce(w, min = glob.MIN, max = glob.MAX) {
        if (w < min) {
            return min
        }
        if (max < w) {
            return max - glob.EPSILON
        }
        return w
    }

    static contains(theImage, squeezeThreshold) {
        const imageArea = theImage.width * theImage.height

        // Check if squeeze is needed based on the product of width and height
        if (imageArea > squeezeThreshold) {
            const aspectRatio = theImage.width / theImage.height

            // Calculate new dimensions
            const newWidth = Math.floor(Math.sqrt(squeezeThreshold * aspectRatio))
            const newHeight = Math.floor(squeezeThreshold / newWidth)

            return { width: newWidth, height: newHeight }
        } else {
            // If squeeze is not needed, return the original dimensions
            return { width: theImage.width, height: theImage.height }
        }
    }

    static arrayToXYZObject(arr) {
        return { x: arr[0], y: arr[1], z: arr[2] }
    }

    static XYZObjectToArray(obj) {
        return [obj.x, obj.y, obj.z]
    }

    //// // Example usage:
    //// const inputValue = 75;
    //// const normalizedValue = normalizeLinearly(inputValue, [0, 100], [0, 1]);
    //// console.log('Normalized Value:', normalizedValue);
    static normalizeLinearly(value, inRange, outRange) {
        // Check if the input range has a valid width
        if (inRange[0] === inRange[1]) {
            throw new Error('Input range has zero width');
        }

        // Normalize the value from the input range to the [0, 1] range
        const normalizedValue = (value - inRange[0]) / (inRange[1] - inRange[0]);
    
        // Scale the normalized value to the output range
        const result = (normalizedValue * (outRange[1] - outRange[0])) + outRange[0];
    
        return result;
    }

    static normalizeQuadratically(value, inRange, outRange) {
        // Check if the input range has a valid width
        if (inRange[0] === inRange[1]) {
            throw new Error('Input range has zero width');
        }
    
        // Normalize the value from the input range to the [0, 1] range
        const normalizedValue = (value - inRange[0]) / (inRange[1] - inRange[0]);
    
        // Apply a quadratic transformation to the normalized value
        const transformedValue = normalizedValue * normalizedValue;
    
        // Scale the transformed value to the output range
        const result = (transformedValue * (outRange[1] - outRange[0])) + outRange[0];
    
        return result;
    }
    
}

export default _