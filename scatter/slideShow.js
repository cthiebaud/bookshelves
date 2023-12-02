class SlideShow {

    constructor(regressionPlaneFromServerMutex) {
        this.regressionPlaneFromServerMutex = regressionPlaneFromServerMutex
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
        document.addEventListener('keypress', this.handleInteraction)
    }

    disable() {
        // dettach event listeners
        document.removeEventListener('keypress', this.handleInteraction)
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
        console.log(`bump slideshow (${this.currentStep})`)
        this.updateButtons()
        this.updateSlides()

        switch (this.currentStep) {
            case 2:
                await this.regressionPlaneFromServerMutex.waitForUnlock()

                const scatterPlot = document.getElementById('scatter-plot')
                const allTraces = scatterPlot.data

                // find index of trace-object where "name" property is "regression-plane":
                const regressionPlane = allTraces.findIndex(obj => obj.name === 'regression-plane')

                // make specified trace visible to the user:
                Plotly.restyle(scatterPlot, { "visible": true }, [regressionPlane])
                break
            case this.slideshowButtons.length:
                console.log("slideshow is done")
                this.disable()
                break
            default:
                break

        }
        // do bump
        this.currentStep++
        return
    }
}

export default SlideShow