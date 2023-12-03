class SlideShow {

    constructor(promises) {
        this.promises = promises
        this.currentStep = 0
        this.slides = {
            show_plot: document.getElementById('scatter-plot-container'),
            show_regression_plane: { style: { visibility: null } },
            show_flat_plot: document.getElementById('scatter-plot2-container'),
            show_flat_image: document.getElementById('generated-image'),
        }
        // buttons for slideshow: show plot ▷ show regression plane ▷ show flat plot ▷ show flat image
        this.slideshowButtons = Array.from(document.getElementsByClassName('slideshowButton'))

        // function to handle key events and button click
        const _this_ = this
        this.handleInteraction = (event) => {
            if (event.target.disabled) {
                return
            }
            _this_.bump()
        }

        // attach event listeners
        this.slideshowButtons.forEach(b => b.addEventListener('click', this.handleInteraction))
        // document.addEventListener('keypress', this.handleInteraction)
    }

    disable() {
        // detach event listeners
        // document.removeEventListener('keypress', this.handleInteraction)
        this.slideshowButtons.forEach(b => {
            b.removeEventListener('click', this.handleInteraction)
            b.disabled = true
        })
        this.currentStep = this.slideshowButtons.length
    }

    // function to show or hide slides based on the current step
    updateSlides() {
        Object.keys(this.slides).map((slide, index) => {
            this.slides[slide].style.visibility = index < this.currentStep ? 'visible' : 'hidden'
        })
    }

    // function to set buttons properties based on the current step
    updateButtons() {
        this.slideshowButtons.forEach(b => {
            b.disabled = true
            b.classList.remove('btn-secondary')
            b.classList.add('btn-light')
        })
        if (this.currentStep < this.slideshowButtons.length) {
            const theButtonForThisStep = this.slideshowButtons[this.currentStep]
            theButtonForThisStep.disabled = false
            theButtonForThisStep.classList.remove('btn-light')
            theButtonForThisStep.classList.add('btn-secondary')
        }
    }

    // function to execute a step
    async bump() {
        if (this.slideshowButtons.length < this.currentStep) {
            return
        }
        console.log(`bump slideshow (${this.currentStep})`)
        switch (this.currentStep) {
            default:
                if (this.promises[this.currentStep] !== null) {
                    this.slideshowButtons.forEach(b => { b.disabled = true }) // you cannot click anymore
                    console.log(`AWAIT promise ${this.currentStep}`)
                    await this.promises[this.currentStep]()
                    console.log(`DONE promise ${this.currentStep}`)
                } else {
                    console.log(`no promise for step ${this.currentStep}`)
                }
                this.updateButtons()
                this.updateSlides()
                break
        }
        // do bump
        this.currentStep++
        if (this.slideshowButtons.length < this.currentStep) {
            console.log("slideshow is done")
            this.disable()
        }
        return
    }
}

export default SlideShow