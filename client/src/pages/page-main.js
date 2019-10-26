import { LitElement, html } from 'lit-element'
import { say, loadXhr } from '../libs/actions.js'

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
				<img class="hanyang-icon" src="./img/logo-default.png" alt="로고 기본"/>				
			</header>
			<main>
                <!-- <bot-chat-balloon></bot-chat-balloon> -->
                <!-- <my-chat-balloon></my-chat-balloon> -->
			</main>
			<footer>
				<btn-list></btn-list>
				<div class="chat-input">
					<input type="text" id="inputText" class='text-send' placeholder='메세지를 입력해주세요' @change=${this.enterTextSend} @focus=${this.focusText} @blur=${this.blurText}></textarea>					
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
    
	async enterTextSend(event) {		
		const isEnter = event.keyCode === 13
		let text = event.target.value

		if (text.trim() === ``) {			
			return
		}

		if (isEnter) {									
			say(`my`, text)
			let res = await loadXhr({
				url: `https://hanyang-chatbot-dot-cool-benefit-185923.appspot.com/${encodeURIComponent(text)}`,
				method: `GET`,
			})
			res = JSON.parse(res)
			say(`bot`, res.answer)
			event.target.value = ``
		}
	}
    
	get clickSend() {
		return {
			async handleEvent() {				
				const inputText = document.querySelector(`#inputText`)

				if (inputText.value.trim() === ``) {
					return 
				}

				say(`my`, inputText.value)
				let res = await loadXhr({
					url: `https://hanyang-chatbot-dot-cool-benefit-185923.appspot.com/${encodeURIComponent(inputText.value)}`,
					method: `GET`,
				})
				res = JSON.parse(res)
				say(`bot`, res.answer)
				inputText.value = `` 
			},
			capture: true,
		}
	}

	get focusText() {
		const root = this
		return {
			handleEvent() {				
				root.querySelector(`.hanyang-icon`).classList.add(`active`)
				root.querySelector(`main`).classList.add(`active`)
			},
			capture: true,
		}
	}

	get blurText() {
		const root = this
		return {
			handleEvent() {				
				root.querySelector(`.hanyang-icon`).classList.remove(`active`)
				root.querySelector(`main`).classList.remove(`active`)
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
	grid-template-rows: 20vh auto 90px;
}

header {
	display: flex;
	justify-content: center;
	align-items: center;
	/* box-shadow: 3px 6px 8px 0 rgba(132, 161, 255, 0.18); */
}

header > img {
	box-sizing: border-box;
	width: 90%;
	height: 100%;
	margin-left: 10%;
	margin-right: 10%;
	margin-top: auto;
	margin-bottom: 1vh;
	position: relative;
	transition: top 0.4s ease;
	top: 0;
	object-fit: contain;
}

header > img.active {
	top: -200%;
}

header > img.up {
	animation: slide-up 0.4s ease;
}

@keyframes slide-up {
	0% {
		top: 0;
	}

	50% {
		top: -150%;
	}

	100% {
		top: 0;
	}
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
	top: 0;
	transition: top 0.3s ease;
}

main.active {
	top: -20vh;
}

main my-chat-balloon, main bot-chat-balloon {
	margin-top: 10px;
}

main > *:last-child {
	margin-bottom: 20px;
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
