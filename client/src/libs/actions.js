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

	main.scrollTo(0, main.scrollHeight)

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

export const waitSend = actionCreator((state, callback) => {
	const main = document.querySelector(`main`)
	const observer = new MutationObserver(mutations => {
		mutations.forEach(async mutation => {						
			if (mutation[`addedNodes`][0][`localName`] === `my-chat-balloon`) {
				let text = await mutation[`addedNodes`][0]
				text = text.querySelector(`.chat-content`).textContent.split(`오후`)[0].split(`오전`)[0]
				callback(text)
			}			
			observer.disconnect()
		})
	})

	const config = {
		childList: true,
		subtree: true || null,
	}
	observer.observe(main, config)

	return state
})
