import glob from './singletonModule.js'

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


    static truncateString(str, maxLength) {
        if (str.length <= maxLength) {
            return str
        } else {
            return str.slice(0, maxLength) + '…'
        }
    }

    static arrayToXYZObject(arr) {
        return { x: arr[0], y: arr[1], z: arr[2] }
    }

    static XYZObjectToArray(obj) {
        return [obj.x, obj.y, obj.z]
    }
}

export default _