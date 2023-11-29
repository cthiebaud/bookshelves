import glob from './singletonModule.js';

class _ {
    static truncateString(str, maxLength) {
        if (str.length <= maxLength) {
            return str;
        }

        const ellipsis = '…';
        const visibleCharacters = maxLength - ellipsis.length;

        const beginning = str.substring(0, visibleCharacters / 2);
        const end = str.substring(str.length - visibleCharacters / 2);

        return beginning + ellipsis + end;
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

    static arrayToXYZObject(arr) {
        return { x: arr[0], y: arr[1], z: arr[2] };
    }

    static XYZObjectToArray(obj) {
        return [obj.x, obj.y, obj.z];
    }
}

export default _;