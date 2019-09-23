import { LitElement, html } from 'lit-element'

class BusInfo extends LitElement {	
	constructor() {
		super()
        
		this._handlers = {}
	}
    
	createRenderRoot() {
		return this
	}
    
	firstUpdated() {
		this._handlers.onClickBusInfoOut = this.clickBusInfoOut.bind(this)
	}

	render() {
		return html`
			${style}
			
		`
	}
    
	clickBusInfoOut(event) {
		const btn = document.querySelector(`.btn-shuttle`)
		if (event.target.closest(`bus-info`) || event.target.closest(`.btn-shuttle`)) {
			return
		}		
		this.classList.remove(`active`)
		btn.classList.remove(`active`)
		document.removeEventListener(`click`, this._handlers.onClickBusInfoOut)
	}
}

customElements.define(`bus-info`, BusInfo)

const style = html`
<style>
bus-info {
    position: absolute;
    bottom: -400px;
    left: 0;
    width: 100vw;
    height: 300px;
    background-color: #2562a2;
    z-index: -1;
    border-radius: 15px 15px 0 0;
    box-shadow: 0 -3px 10px 0 rgba(0, 0, 0, 0.16);

    transition: bottom 200ms ease;
}

bus-info.active {
    bottom: 40px;
}

@keyframes up {
    0% {
        bottom: -400px
    }

    100% {
        bottom: 40px;
    }
}
</style>
`
