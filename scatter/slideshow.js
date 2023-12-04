async function doNothing() { }

class Slide {
    constructor(buttonId, elementId, promise) {
        this.button = document.getElementById(buttonId)
        this.element = document.getElementById(elementId)
        this.promise = promise;
    }

    // Getter and setter for the 'button' property
    get button() {
        return this._button;
    }

    set button(newButton) {
        this._button = newButton ? newButton : {
            addEventListener: () => { },
            removeEventListener: () => { },
            disabled: undefined,
            classList: {
                add: () => { },
                remove: () => { },
            },
            parentNode: {
                classList: {
                    add: () => { },
                    remove: () => { },
                }
            }
        };
    }

    // Getter and setter for the 'element' property
    get element() {
        return this._element;
    }

    set element(newElement) {
        this._element = newElement ? newElement : {
            style: { visibility: null }
        };
    }

    // Getter and setter for the 'promise' property
    get promise() {
        return this._promise;
    }

    set promise(newPromise) {
        this._promise = newPromise ? newPromise : doNothing;
    }
}

class SlideShow {

    constructor(slides) {
        this._slides = slides
        this.reset()
    }

    reset() {
        this._currentStep = 0
        
        // function to handle key events and button click
        const _this_ = this
        this.handleInteraction = (event) => {
            if (event.target.disabled) {
                return
            }
            _this_.bump()
        }

        // attach event listeners
        this._slides.forEach(s => {
            s.button.addEventListener('click', this.handleInteraction)
        })
        // document.addEventListener('keypress', this.handleInteraction)
    }

    close() {
        // detach event listeners
        // document.removeEventListener('keypress', this.handleInteraction)
        this._slides.forEach(s => {
            s.button.removeEventListener('click', this.handleInteraction)
            s.button.disabled = true
            s.button.parentNode.classList.add('disabled')
        })
        this._currentStep = this._slides.length
    }

    // function to show or hide slides based on the current step
    updateSlides() {
        for (let index = 0; index < this._slides.length; index++) {
            this._slides[index].element.style.visibility = index <= this._currentStep ? 'visible' : 'hidden'
        }
    }

    // function to set buttons properties based on the current step
    updateButtons() {
        this._slides.forEach(s => {
            s.button.disabled = true
            s.button.parentNode.classList.add('disabled')
            s.button.classList.remove('btn-primary')
            s.button.classList.add('btn-light')
        })
        if (this._currentStep < this._slides.length) {
            const b = this._slides[this._currentStep].button
            b.disabled = false
            b.parentNode.classList.remove('disabled')
            b.classList.remove('btn-light')
            b.classList.add('btn-primary')
        }
    }

    // function to execute a step
    async bump() {
        if (this._currentStep < 0 || this._slides.length <= this._currentStep) {
            return
        }
        // disable all buttons during slide bump
        this._slides.forEach(s => s.button.disabled = true) 
        // show what needs to be shown
        this.updateSlides()
        // wait for promise to be done
        await this._slides[this._currentStep].promise()
        // BUMP!
        this._currentStep++
        // update display to show were we are now
        this.updateButtons() // button associated with current step will be re-enabled

        if (this._slides.length <= this._currentStep) {
            // FINITO !!
            this.close()
        }
        return
    }
}

export { Slide, SlideShow }