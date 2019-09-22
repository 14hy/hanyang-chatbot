import store from './store'

function actionCreator(action) {
	return function() {
		let state = store.getState()
		state = action(state, ...arguments)
		store.setState(state)
	}
}

// ===================================================== Code Structure

export const countAdd = actionCreator(state => {
	state.info.count === undefined
		? state.info.count = 0
		: state.info.count++
	return state
})

// ===================================================== Router

export const renderHtml = actionCreator((state, html) => {
	const app = document.querySelector(`app-main`).shadowRoot.querySelector(`main`)

	app.innerHTML = html

	return state
})

export const get = actionCreator((state, url) => new Promise((resolve, reject) => {
	const req = new XMLHttpRequest()
	req.open(`GET`, url)
	req.send()
  
	req.onreadystatechange = function () {
		if (req.readyState === XMLHttpRequest.DONE) {
			if (req.status === 200) {
				resolve(req.response)
			} else {
				reject(req.statusText)
			}
		}
	}
}))

export const loadXhr = actionCreator((state, url, callback) => {
	const xhr = new XMLHttpRequest()

	if(!xhr) {
		throw new Error(`XHR 호출 불가`)
	}

	xhr.open(`GET`, url)
	xhr.setRequestHeader(`x-requested-with`, `XMLHttpRequest`)
	xhr.addEventListener(`readystatechange`, () => {
		if (xhr.readyState === xhr.DONE) {				
			if (xhr.status === 200 || xhr.status === 201) {
				callback(xhr.responseText)
			}
		}
	})
	xhr.send()
	return state
})
