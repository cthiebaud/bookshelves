async function doNothing() { }

class Slide {
    constructor(buttonId, elementId, promise) {
        this.button = document.getElementById(buttonId)
        this.element = document.getElementById(elementId)
        this.promise = promise
    }

    // getter and setter for the 'button' property
    get button() {
        return this._button
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
        }
    }

    // getter and setter for the 'element' property
    get element() {
        return this._element
    }

    set element(newElement) {
        this._element = newElement ? newElement : {
            style: { visibility: null }
        }
    }

    // getter and setter for the 'promise' property
    get promise() {
        return this._promise
    }

    set promise(newPromise) {
        this._promise = newPromise ? newPromise : doNothing
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
        this._slides.forEach((s, i) => {
            if (i === this._currentStep) {
                s.button.disabled = false
                s.button.classList.remove('btn-light')
                s.button.classList.add('btn-primary')
                s.button.parentNode.classList.remove('disabled')
            } else {
                s.button.disabled = true
                s.button.classList.remove('btn-primary')
                s.button.classList.add('btn-light')
                s.button.parentNode.classList.add('disabled')
            }
        })
    }

    // function to execute a step
    async bump() {
        if (this._currentStep < 0 || this._slides.length <= this._currentStep) {
            return
        }
        // show what needs to be shown
        this.updateSlides()
        // disable current button while running promise
        this._slides[this._currentStep].button.disabled = true
        this._slides[this._currentStep].button.parentNode.classList.add('rotating-text')
        // wait for promise to be done
        await this._slides[this._currentStep].promise()
        this._slides[this._currentStep].button.parentNode.classList.remove('rotating-text')
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