import store from './store'

function actionCreator(action) {
	return function() {
		let state = store.getState()
		state = action(state, ...arguments)
		store.setState(state)
	}
}

// ===================================================== Code Structure

export const say = actionCreator(async (state, talker ,text) => {
	const main = document.querySelector(`main`)
	const lastChat = document.querySelector(`main > *:last-child`) || false
	const isSay = lastChat && lastChat.localName === `${talker}-chat-balloon`	
	const chatBalloon = document.createElement(`${talker}-chat-balloon`)
	
	if(isSay) {
		lastChat.chat(text)
		return state	
	} 	
	
	await main.appendChild(chatBalloon)
	chatBalloon.chat(text)

	return state
})

export const scrollToLast = actionCreator(state => {
	const main = document.querySelector(`main`)

	main.scrollTop = main.scrollHeight

	return state
})

