import { LitElement, html } from 'lit-element'

import { scrollToLast } from '../libs/actions.js'

class MyChatBalloon extends LitElement {
	constructor() {
		super()
	}
	
	createRenderRoot() {
		return this
	}	

	render() {
		return html`
			${style}
			<div class="my-chat">
				<div class='chat-wrap'>
					<!-- <div class='chat-content'>TEST</div> -->
					<!-- <div class='chat-content-continue'>TEST</div> -->
				</div>
			</div>
		`
	}

	chat(text, _class = `chat-content`) {
		const isNoChat = this.querySelector(`.chat-wrap`).childElementCount === 0

		if(isNoChat) {
			this.makeChatBallon(text, _class)
			return
		}

		this.makeChatBallon(text, `${_class}-continue`)
	}

	makeChatBallon(text, _class = `chat-content`) {
		const div = document.createElement(`div`)		
		div.classList.add(_class)
		div.innerHTML = text

		const time = document.createElement(`span`)
		time.classList.add(`chat-time`)
		time.textContent = this.getTime

		div.appendChild(time)
		this.querySelector(`.chat-wrap`).appendChild(div)
		scrollToLast()
	}

	get getTime() {
		const date = new Date()
		const amPm = date.getHours() > 12 ? `오후` : `오전`
		const hours = date.getHours() > 12 ? date.getHours() - 12 : date.getHours()
		const minutes = date.getMinutes()

		return `${amPm} ${hours}시 ${minutes}분`
	}
}

customElements.define(`my-chat-balloon`, MyChatBalloon)

const style = html`
<style>
.my-chat {
	width: 100%;
	display: grid;
	grid-template-rows: 1fr;
	grid-template-columns: 1fr;
	min-height: 30px;
	box-sizing: border-box;
	float: right;
}	

.my-chat .chat-wrap {
	padding-top: 5px;
	padding-bottom: 5px;
	z-index: 5;

	display: grid;
	grid-template-rows: 1fr;
	grid-row-gap: 10px;
}

.my-chat .chat-content, .my-chat .chat-content-continue {
	display: inline-block;
	position: relative;
	min-height: 28px;
	min-width: 20px;
	width: fit-content;
	max-width: calc(80vw - 65px);
	background-color: #2562a2;
	padding: 5px 10px 5px 10px;
	box-sizing: border-box;
	font-size: 13px;
	color: white;
	margin-right: 20px;
	margin-left: auto;

	box-shadow: 3px 6px 8px 0 rgba(132, 161, 255, 0.18);
    padding-left: 15px;
    padding-right: 15px;
	font-family: 'Noto-sans';
	
	animation: slide 0.3s ease-out;
}

.my-chat .chat-content {
	border-radius: 15px 2px 16px 15px;
}

.my-chat .chat-content-continue {
	border-radius: 15px 10px 15px 15px;
}

.my-chat .chat-time {
	position: absolute;
    bottom: 0px;
    left: -60px;
    color: #727272;
    font-size: 6px;
}

::selection {
	background-color: yellow;
}

@keyframes slide {
	0% {
		right: -100%;
		opacity: 0;
	}

	75% {
		opacity: 0;
	}

	100% {
		right: 0%;
		opacity: 1;
	}
}
</style>
`
