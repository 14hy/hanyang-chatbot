import createStore from './redux-zero.js'

window.canChat = true

const initialState = {
	foodInfo: [],
}
const store = createStore(initialState)

export default store
