// singletonModule.js

class Singleton {
    _dataStructure = {
        width: undefined,
        height: undefined,
        MIN: undefined,
        MAX: undefined,
        ε: undefined,
    };

    constructor() {
        this._dataStructure.width = null
        this._dataStructure.height = null
        this._dataStructure.MIN = 0
        this._dataStructure.MAX = 256
        this._dataStructure.ε = (() => {
            let ε = Number.EPSILON
            let c = 0;
            while (this._dataStructure.MAX - ε == this._dataStructure.MAX) {
                ε *= 2
                c++
            }
            console.log(`MIN = ${this._dataStructure.MIN}, MAX = ${this._dataStructure.MAX}, ε = ${this._dataStructure.ε} (in ${c} iterations)`)
            return ε
        })()
    }

    get MIN() {
        return this._dataStructure.MIN;
    }

    get MAX() {
        return this._dataStructure.MAX;
    }

    get EPSILON() {
        return this._dataStructure.ε;
    }

    get width() {
        return this._dataStructure.width;
    }

    set width(newWidth) {
        this._dataStructure.width = newWidth;
    }

    get height() {
        return this._dataStructure.height;
    }

    set height(newHeight) {
        this._dataStructure.height = newHeight;
    }
}

// Create a single instance of the Singleton class
const glob = new Singleton();

// Export the instance to make it accessible in other modules
export default glob;
