import { LitElement, html } from 'lit-element'
import { say } from '../libs/actions.js'

import '../components/my-chat-balloon.js'
import '../components/bot-chat-balloon.js'
import '../components/btn-list.js'

export class PageMain extends LitElement {	
	static get properties() {
		return { 
			date: { type: String },
		}
	}
    
	constructor() {
		super()    

		this.date = this.getDate
	}

	createRenderRoot() {
		return this
	}
    
	firstUpdated() {
		this.querySelector(`#inputText`).addEventListener(`keypress`, this.enterTextSend)
		say(`bot`, `안녕하냥~ 나는 너를 도울 수 있어.`)
	}

	render() {
		return html`
		<link rel="stylesheet" href="css/icons.css">
		${style}

		<div id="pageMain" class="page-content">
			<header>
				<h1>하냥이</h1>
                <div class="date">${this.date}</div>
			</header>
			<main>
                <!-- <bot-chat-balloon></bot-chat-balloon> -->
                <!-- <my-chat-balloon></my-chat-balloon> -->
			</main>
			<footer>
				<btn-list></btn-list>
				<div class="chat-input">
					<input type="text" id="inputText" class='text-send' placeholder='메세지를 입력해주세요' @change=${this.enterTextSend}></textarea>					
					<button class='btn-send' @click=${this.clickSend}><i class="f7-icons size-32">arrow_right</i></button>
				</div>
			</footer>
		</div>
        `
	}
    
	get getDate() {
		const date = new Date()
		const year = date.getFullYear()
		const month = date.getMonth() + 1
		const day = date.getDate()
		return `${year}년 ${month}월 ${day}일`
	}    
    
	enterTextSend(event) {		
		const isEnter = event.keyCode === 13

		if (event.target.value.trim() === ``) {			
			return
		}

		if (isEnter) {									
			say(`my`, event.target.value)
			event.target.value = ``
		}
	}
    
	get clickSend() {
		return {
			handleEvent() {				
				const inputText = document.querySelector(`#inputText`)

				if (inputText.value.trim() === ``) {
					return 
				}

				say(`my`, inputText.value)
				inputText.value = `` 
			},
			capture: true,
		}
	}
}

customElements.define(`page-main`, PageMain)

const style = html`
<style>
.view {
	z-index: 100;
}

#pageMain {
    border: 1px solid #595959;
    width: 100%;
    height: 100%;
    margin: 0 auto;
    padding: 0;
    border-radius: 2px;
    overflow: hidden;

    display: grid;
    grid-template-rows: 10vh auto 90px;
}

header {
    display: grid;
    grid-template-rows: 8vh 2vh;
}

header > h1 {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 5vh;
    margin-top: 3vh;
    margin-bottom: 0;
    
    font-family: 'Noto-sans';
    font-size: 16px;
    font-weight: bold;
    background-color: #f3f3f3;
	color: #c2c2c2;
	user-select: none;
}

header > .date {
    display: flex;
    justify-content: center;
    align-items: center;

    font-size: 13px;
    color: #dadada;
}

main {
	overflow-y: scroll;
	overflow-x: hidden;

    display: grid;
    grid-template-columns: 1fr;
    grid-auto-rows: min-content;
    width: 100%;
    height: auto;

	position: relative;
    z-index: 0;
}

footer {
    display: grid;
	grid-template-rows: 40px 50px;	    

	background-color: white;
	z-index: 5;
}

.chat-input {
    display: grid;
	grid-template-columns: auto 50px;
	
	background-color: white;
}

#inputText.text-send {
    border: 0;
    outline: none;
    resize: none;
    margin: 5px;
    font-size: 16px;
	font-family: 'Noto-sans';
	
    padding-left: 20px;
}

.text-send::placeholder {
    color: #e0e0e0;
}

.text-send:focus {
    outline: none;
}

.btn-send {
    display: flex;
    justify-content: center;
    align-items: center;

    background-color: transparent;
    border: 0;
    color: #2699fb;
    transition: all 0.1s ease-in;
}

.btn-send:hover {
    color: black;
}
</style>
`
