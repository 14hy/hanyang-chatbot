import createStore from './redux-zero.js'

const initialState = {
	info: [] , 
	router: {
		login: {
			requireLogin: false,
		},
	},
	login: false,
}
const store = createStore(initialState)

export default store
