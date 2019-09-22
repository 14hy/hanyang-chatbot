import { LitElement, html, css } from 'lit-element'

export class AppLoading extends LitElement {
	static get styles() {        
		return css`
		:host {
			display: flex;
			position: absolute;
			top: 0;
			left: 0;
			width: 100vw;
			height: 100vh;
			margin: 0;
			padding: 0;
			justify-content: center;
			align-items: center;
		}
		`
	}

	static get properties() {
		return {
			
		}
	}
	
	constructor() {
		super()
		
	}

	render() {
		return html`
		loading...
        `
	}
}

customElements.define(`app-loading`, AppLoading)
