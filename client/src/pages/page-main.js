import { LitElement, html } from 'lit-element'
import i18next from 'i18next'

import style from './page-main-css.js'

export class PageMain extends LitElement {
	static get styles() {
		return [style]
	}

	static get properties() {
		return {
			title: String,
		}
	}
	
	constructor() {
		super()
		this.title = i18next.t(`APP_NAME`)
	}

	render() {
		return html`
		<div id="pageMain">
			<header>				
				<div class="logo">Logo</div>
				<div class="title">Title</div>
			</header>
			<main>
				<div class="content">컨텐츠</div> 
			</main>
			<footer>
				<span>하단부 버튼 모음</span>
			</footer>
		</div>
        `
	}
}

customElements.define(`page-main`, PageMain)
