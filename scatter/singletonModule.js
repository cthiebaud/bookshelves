// singletonModule.js

class Singleton {
    _dataStructure = {
        width: undefined,
        height: undefined,
    };

    constructor() {
        this._dataStructure.width = null
        this._dataStructure.height = null
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
