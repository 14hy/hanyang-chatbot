import { LitElement, html } from 'lit-element'
import store from '../libs/store.js'

class FoodList extends LitElement {	
	static get properties() {
		return { 
			mealData: { type: Array },
		}
	}
    
	constructor() {
		super()    		
		this.mealData = store.getState().foodInfo
	}
    
	createRenderRoot() {
		return this
	}

	render() {
		return html` 
            ${style}
            <span class="chat-content">어디에서 학식을 먹고 싶냥?</span>
            <div class="food-wrap">
                <div class="list accordion-list">
                    <ul class="meal-list">
                        ${[`교직원 식당`, `학생 식당`, `기숙사 식당`, `푸드코트`, `창업보육센터`].map((li, index) => this.mealList(li, index))}
                    </ul>
                </div>
            </div>
		`
	}
    
	mealList(foodStore, index) {
		return html`
        ${this.mealData.length === 0 ? html`` : html`
        <li class="accordion-item ${index === 0 ? `item-opended accordion-item-opened` : ``}"><a href="#" class="item-content item-link">
	        <div class="item-inner">
	            <div class="item-title">${foodStore}</div>
	        </div></a>
	        <div class="accordion-item-content">
	            <div class="block">
                    ${this.foodByTime(index)}
	            </div>
	        </div>
	    </li>
        `}	    
	    `
	}
    
	foodByTime(index) {
		return html`
        ${[`분식`, `조식`, `중식`, `석식`, `중식/석식`].map(each => 
		this.mealData[index][each] 
			? html`
            <div class="meal-time">${each}</div>

            ${this.mealData[index][each].map(menu => html`
            <p class="menu">${menu[`menu`]}</p>
            <p class="price">특식 ${menu[`price`]}원</p>
            `)}            
            `
			: html``,
	)}
        `
	}
}

customElements.define(`food-list`, FoodList)

const style = html`
<style>
food-list .chat-content {    
    z-index: 20;
}

food-list .list .item-inner .item-title {
    color: #2562a2;
    font-size: 14px;
    font-family: 'Noto-sans';
    position: relative;
    overflow: visible;
}

/* food-list .list .item-inner .item-title:after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0px;
    width: 80px;
    height: 1px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.16);
} */

food-list .list ul:after, food-list .list ul:before {
    display: none;
}

.food-wrap {
    position: relative;
    z-index: 10;
    width: 70vw;
    background-color: white;
    top: -20px;
    left: 0;
    min-height: 80px;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 3px 6px 9px 0 rgba(0, 0, 0, 0.16);

    animation: slide 0.3s ease-out;
}

food-list .accordion-list {
    z-index: 10;
    position: relative;
    margin-bottom: 15px;    
}

food-list .accordion-list .item-link .item-inner {
    min-height: 40px;
    height: 40px;

}

food-list .accordion-list .item-link .item-inner:after {
    display: none;
}

food-list .accordion-item-content {
    transition-duration: 100ms;
}

food-list .list .item-content.item-link {
    min-height: 40px;
    height: 40px;    
}

food-list .meal-time {
    font-weight: bold;
    font-size: 12px;
    color: #ffaa00;        
}

food-list .meal-time:not(:first-child) {
    margin-top: 10px;
}

food-list .menu {
    margin: 0;
    font-size: 11px;
    color: #818181;
    margin-top: 5px;
}

food-list .price {
    margin: 0;
    font-size: 10px;
    color: #818181;
    opacity: 0.7;
}
</style>
`
