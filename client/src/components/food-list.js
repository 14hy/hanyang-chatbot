import { LitElement, html } from 'lit-element'

class FoodList extends LitElement {	
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
			
		`
	}
}

customElements.define(`food-list`, FoodList)

const style = html`
<style>

</style>
`
