import createStore from './redux-zero.js'
import { loadXhr } from './actions.js'

const initialState = {
	foodInfo: [],
}
const store = createStore(initialState)

initFoodInfo()

async function initFoodInfo() {
	const foodStores = [`교직원식당`, `학생식당`, `창의인재원식당`, `푸드코트`, `창업보육센터`]

	let res = await Promise.all(foodStores.map(foodStore => loadXhr({
		url: `https://hanyang-chatbot-dot-cool-benefit-185923.appspot.com/service/food/?restaurant=${foodStore}`,
		method: `GET`,
	})))    
	res = res.map(each => JSON.parse(each))

	store.setState({
		foodInfo: res,
	})
}

export default store
