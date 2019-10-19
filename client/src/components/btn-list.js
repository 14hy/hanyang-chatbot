import { LitElement, html } from 'lit-element'

import { say, waitSend, loadXhr, getStore } from '../libs/actions.js'

import '../components/food-list.js'
import '../components/bus-info.js'
import '../components/book-info.js'

class BtnList extends LitElement {	
	constructor() {
		super()		
	}
    
	createRenderRoot() {
		return this
	}

	render() {
		return html`
			${style}
			<ul id="btnList">
				<bus-info></bus-info>
                <button class="btn-food col button button-raised button" @click=${this.clickFood}><img src="/img/icon-food.png" alt="학식 아이콘" width="20" height="20" class="icon icon-food">학식</button>
                <button class="btn-book col button button-raised button" @click=${this.clickBook}><img src="/img/icon-book.png" alt="도서 아이콘" width="25" height="25" class="icon">도서</button>
                <button class="btn-shuttle col button button-raised button" @click=${this.clickBusInfo}><img src="/img/icon-bus.png" alt="셔틀 아이콘" width="20" height="20" class="icon">셔틀</button>
			</ul>
		`
	}

	get clickBook() {
		return {
			async handleEvent() {	
				await say(`my`, `도서관 검색해줘`)			
				await say(`bot`, `학술정보관에서 검색해줄게.<br/><strong>'책 이름'</strong>을 입력해줘~`)
				waitSend(text => {
					say(`bot`, `<book-info searchText="${text}"></book-info>`)
				})				
			},
			capture: true,
		}
	}

	get clickFood() {
		const root = this
		return {
			async handleEvent() {	
				await root.initFoodInfo()
				say(`my`, `학식 메뉴 알려줘~`)			
				say(`bot`, `<food-list></food-list>`, `school-food`)
			},
			capture: true,
		}
	}


	get clickBusInfo() {
		const root = this
		return {
			handleEvent(event) {
				const busInfo = root.querySelector(`bus-info`)
				const btn = event.target
				if (btn.classList.contains(`active`)) {
					busInfo.hide()					
					btn.querySelector(`.icon`).src = `/img/icon-bus.png`
					return
				}						
				busInfo.show()
				btn.querySelector(`.icon`).src = `/img/icon-bus-active.png`
			},
			capture: true,
		}
	}

	async initFoodInfo() {
		const foodStores = [`교직원식당`, `학생식당`, `창의인재원식당`, `푸드코트`, `창업보육센터`]
    
		let res = await Promise.all(foodStores.map(foodStore => loadXhr({
			url: `https://hanyang-chatbot-dot-cool-benefit-185923.appspot.com/service/food/?restaurant=${foodStore}`,
			method: `GET`,
		})))    
		res = res.map(each => JSON.parse(each))

		getStore(store => {			
			store.setState({
				foodInfo: res,
			})
		})		
	}
}

customElements.define(`btn-list`, BtnList)

const style = html`
<style>
#btnList {
    margin: 0;
    padding: 0;

    display: grid;
    grid-template-columns: repeat(3, 1fr);
	height: 40px;    
	
	position: relative;
}

#btnList button {
	display: flex;
	align-items: center;
	color: #8B8B8B;
	background-color: #E9E9E9;
	box-shadow: 0 0px 10px 0 rgba(0, 0, 0, 0.1);
	height: 100%;
	border-radius: 0;
}

#btnList button.active {
	box-shadow: 0 -5px 10px 0 rgba(132, 161, 255, 0.2);
	background-color: #24609f;
	color: rgba(255, 255, 255, 0.8);
	border-radius: 0;
	transition: all 0.2s ease;
}

#btnList .icon {	
	display: inline-block;
	margin-right: 5px;
}

#btnList .icon-food {
	margin-bottom: 2px;
}
</style>
`
