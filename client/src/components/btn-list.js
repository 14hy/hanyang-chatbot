import { LitElement, html } from 'lit-element'

import { say } from '../libs/actions.js'

class BtnList extends LitElement {	
	constructor() {
		super()
	}
    
	createRenderRoot() {
		return this
	}

	render() {
		return html`
            <link rel="stylesheet" href="css/framework7.bundle.min.css">
			${style}
			<ul id="btnList">
                <button class="btn-food col button button-raised button" @click=${this.clickFood}>학식</button>
                <button class="btn-book col button button-raised button">도서</button>
                <button class="btn-shuttle col button button-raised button">셔틀</button>
			</ul>
		`
	}

	get clickFood() {
		return {
			handleEvent() {				
				say(`bot`, `어디에서 학식을 먹고 싶냥?`)
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
}

#btnList button {
    color: #2699fb;
    box-shadow: 0 -3px 10px 0 rgba(0, 0, 0, 0.16);
}
</style>
`
