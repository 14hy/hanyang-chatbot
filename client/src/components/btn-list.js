import { LitElement, html } from 'lit-element'

import { say } from '../libs/actions.js'

import '../components/food-list.js'
import '../components/bus-info.js'

class BtnList extends LitElement {	
	constructor() {
		super()
	}
    
	createRenderRoot() {
		return this
	}

	render() {
		return html`
			${style}
			<ul id="btnList">
				<bus-info></bus-info>
                <button class="btn-food col button button-raised button" @click=${this.clickFood}>학식</button>
                <button class="btn-book col button button-raised button">도서</button>
                <button class="btn-shuttle col button button-raised button" @click=${this.clickBusInfo}>셔틀</button>
			</ul>
		`
	}

	get clickFood() {
		return {
			handleEvent() {	
				say(`my`, `학식 메뉴 알려줘~`)			
				say(`bot`, `<food-list></food-list>`, `school-food`)
			},
			capture: true,
		}
	}


	get clickBusInfo() {
		const root = this
		return {
			handleEvent(event) {
				const busInfo = root.querySelector(`bus-info`)
				const btn = event.target
				if (btn.classList.contains(`active`)) {
					busInfo.hide()
					return
				}						
				busInfo.show()
			},
			capture: true,
		}
	}
}

customElements.define(`btn-list`, BtnList)

const style = html`
<style>
#btnList {
    margin: 0;
    padding: 0;

    display: grid;
    grid-template-columns: repeat(3, 1fr);
	height: 40px;    
	
	position: relative;
}

#btnList button {
	color: #2699fb;
	background-color: white;
    box-shadow: 0 -3px 10px 0 rgba(0, 0, 0, 0.16);
}

#btnList button.active {
	background-color: #24609f;
    color: rgba(255, 255, 255, 0.8);
    border-radius: 0;
}
</style>
`
