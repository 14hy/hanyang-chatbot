import store from './store'

function actionCreator(action) {
	return function() {
		let state = store.getState()
		state = action(state, ...arguments)
		store.setState(state)
	}
}

// ===================================================== Code Structure

export const say = actionCreator(async (state, talker , text, _class) => {
	const main = document.querySelector(`main`)
	const lastChat = document.querySelector(`main > *:last-child`) || false
	const isSay = lastChat && lastChat.localName === `${talker}-chat-balloon`	
	const chatBalloon = document.createElement(`${talker}-chat-balloon`)
	
	if(isSay) {
		lastChat.chat(text, _class)
		return state	
	} 	
	
	await main.appendChild(chatBalloon)
	chatBalloon.chat(text, _class)

	return state
})

export const scrollToLast = actionCreator(state => {
	const main = document.querySelector(`main`)

	main.scrollTop = main.scrollHeight

	return state
})

export const loadXhr = obj => new Promise((resolve, reject) => {
	const req = new XMLHttpRequest()

	if (!req) {
		throw new Error(`No exist XHR`)
	}

	req.open(obj.method, obj.url)	

	req.setRequestHeader(`x-requested-with`, `XMLHttpRequest`)
	req.onreadystatechange = () => {
		if (req.readyState === XMLHttpRequest.DONE) {
			if (req.status === 200 || req.status === 201) {
				resolve(req.responseText)			
			} else {
				reject(req.statusText)
			}
		}
	}
	req.send(obj.body || null)
})
