/* eslint-disable no-irregular-whitespace */
import { LitElement, html } from 'lit-element'
import { loadXhr } from '../libs/actions.js'

class BusInfo extends LitElement {
	static get properties() {
		return { 
			busTimeStation: { type: Array },
			busTimeCycle: { type: Array },
			busTimeArt: { type: Array },
		}
	}
    
	constructor() {
		super()
        
		this._handlers = {}
		this.busTimeStation = []
		this.busTimeCycle = []
		this.busTimeArt = []
	}
    
	createRenderRoot() {
		return this
	}
    
	firstUpdated() {
		this._handlers.onClickBusInfoOut = this.clickBusInfoOut.bind(this)
		this.getBusTime()				
	}

	render() {
		return html`
            ${style}
            <img class="big-hanyang" src="./img/big-hanyang.png" alt="하냥이" width="200" height="200"/>
            <div class="shuttle-title">셔틀버스 시간표</div>
            <ul class="shuttle-place">
                <li>기숙사</li>
                <li>셔틀콕</li>
                <li>한대앞역</li>
                <li>예술인</li>
                <li>셔틀콕</li>
                <li>기숙사</li>
            </ul>
            <div class="shuttle-body">
                <ul class="shuttle-line">
                    <li>한대앞역 행</li>                    
                    <li>예술인행</li>
                    <li>순환버스</li>
                </ul>
                <ul class="shuttle-time">
                    <div class="time-line-1"></div>
                    <div class="time-line-2"></div>
                    <div class="time-line-3"></div>
                    ${this.liStation()}                                    

                    ${this.liArt()}

                    ${this.liCycle()}
                </ul>
            </div>
		`
	}
    
	// eslint-disable-next-line complexity
	async getBusTime() {        
		let res = await loadXhr({
			url: `https://hanyang-chatbot-dot-cool-benefit-185923.appspot.com/service/shuttle/`,
			method: `GET`,
		})

		res = JSON.parse(res)

		this.busTimeStation = [						
			res[`dorm_station`][`status`] ? `${res[`dorm_station`][`minutes`]}분 전`: `　`,
			res[`shuttle_station`][`status`] ? `${res[`shuttle_station`][`minutes`]}분 전`: `　`, 
			res[`station_station`][`status`] ? `${res[`station_station`][`minutes`]}분 전`: `　`, 
			``, 
			res[`shuttle_station2`][`status`] ? `${res[`shuttle_station2`][`minutes`]}분 전`: `　`,             
			`...`, 
		]
		this.busTimeCycle = [
			res[`dorm_cycle`][`status`] ? `${res[`dorm_cycle`][`minutes`]}분 전`: `　`,
			res[`shuttle_cycle`][`status`] ? `${res[`shuttle_cycle`][`minutes`]}분 전`: `　`, 
			res[`station_cycle`][`status`] ? `${res[`station_cycle`][`minutes`]}분 전`: `　`, 
			res[`artin_cycle`][`status`] ? `${res[`artin_cycle`][`minutes`]}분 전`: `　`, 
			res[`shuttle_cycle2`][`status`] ? `${res[`shuttle_cycle2`][`minutes`]}분 전`: `　`,             
			`...`, 
		]
		this.busTimeArt = [
			res[`dorm_artin`][`status`] ? `${res[`dorm_artin`][`minutes`]}분 전`: `　`,
			res[`shuttle_artin`][`status`] ? `${res[`shuttle_artin`][`minutes`]}분 전`: `　`, 
			``, 
			res[`artin_artin`][`status`] ? `${res[`artin_artin`][`minutes`]}분 전`: `　`, 
			res[`shuttle_artin2`][`status`] ? `${res[`shuttle_artin2`][`minutes`]}분 전`: `　`,
			`...`, 
		]
        
		this.busTimeStation = this.busTimeStation.map(each => each === `0분 전` ? `도착 전`: each)
		this.busTimeCycle = this.busTimeCycle.map(each => each === `0분 전` ? `도착 전`: each)
		this.busTimeArt = this.busTimeArt.map(each => each === `0분 전` ? `도착 전`: each)
	}
    
	liStation() {
		return html`
        ${this.busTimeStation.map((time, index) => html`
        <li>
            <span class="basic-circle ${time.trim().length !== 0 && time !== `...` ? `circle` : ``}">${index === 3 ? ``: `●`}</span>
            <span class="time-value">${time}</span>
        </li>
        `)}
        `
	}
    
	liCycle() {
		return html`        
        ${this.busTimeCycle.map(time => html`
        <li>
            <span class="basic-circle ${time.trim().length !== 0 && time !== `...` ? `circle` : ``}">●</span>
            <span class="time-value">${time}</span>
        </li>
        `)} 
        `
	}
    
	liArt() {
		return html`
        ${this.busTimeArt.map((time, index) => html`
        <li>
            <span class="basic-circle ${time.trim().length !== 0 && time !== `...` ? `circle` : ``}">${index === 2 ? ``: `●`}</span>
            <span class="time-value">${time}</span>
        </li>
        `)}
        `
	}
    
	show() {
		const btn = document.querySelector(`.btn-shuttle`)

		this.classList.add(`active`)
		btn.classList.add(`active`)
		btn.querySelector(`.icon`).src = `./img/icon-bus-active.png`
		document.addEventListener(`click`, this._handlers.onClickBusInfoOut)
		this._handlers.intervalBusInfo = window.setInterval(this.getBusTime.bind(this), 60000)
	}
    
	hide() {
		const btn = document.querySelector(`.btn-shuttle`)

		this.classList.remove(`active`)
		btn.classList.remove(`active`)
		btn.querySelector(`.icon`).src = `./img/icon-bus.png`
		document.querySelector(`main`).removeEventListener(`scroll`, this._handlers.onScrollBusInfoOut)
		window.clearInterval(this._handlers.intervalBusInfo)
	}
    
	clickBusInfoOut(event) {
		if (event.target.closest(`bus-info`) || event.target.closest(`.btn-shuttle`)) {
			return
		}		
		this.hide()
	}
}

customElements.define(`bus-info`, BusInfo)

const style = html`
<style>
bus-info {
    position: absolute;
    bottom: -400px;
    left: 0;
    width: 100vw;
    height: 300px;
    background-color: #2562a2;
    z-index: -1;
    border-radius: 15px 15px 0 0;
    box-shadow: 0 -3px 10px 0 rgba(0, 0, 0, 0.16);

    transition: bottom 200ms ease;

    display: grid;
    grid-template-rows: 80px 30px 170px;
}

bus-info.active {
    bottom: 40px;
}

bus-info .shuttle-title {
    position: relative;
    font-size: 20px;
    color: white;   

    padding-top: 30px;
    padding-left: 25px;
}

bus-info .big-hanyang {
    position: absolute;
    right: 3vw;
    top: -163px;
    width: 200px;
    height: 200px;
}

.shuttle-place {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    margin-left: 5vw;
    margin-right: 5vw;
    padding-left: 20vw;
    color: rgba(255, 255, 255, 0.9);
    font-size: 11px;
    letter-spacing: -2px;
    text-align: center;

    border-bottom: 1px solid rgba(255, 255, 255, 0.4);
}

.shuttle-place li {
    list-style: none;
}

.shuttle-body {
    display: grid;
    grid-template-columns: 20vw 70vw;
    margin-top: 10px;
    margin-left: 5vw;
    margin-right: 5vw;    
}

.shuttle-line {
    display: grid;
    grid-template-rows: repeat(3, 1fr);    
    align-items: center;
    color: rgba(255, 255, 255, 0.8);
    font-size: 14px;    
}

.shuttle-line li {
    padding-bottom: 14px;
}

.shuttle-time {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    grid-template-rows: repeat(3, 1fr);    

    position: relative
}

.shuttle-time li {
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 10px;
    color: #A8C0DA;
    flex-flow: column;
}

.shuttle-time .time-line-1, .shuttle-time .time-line-2, .shuttle-time .time-line-3 {
    position: absolute;
    width: 84%;
    height: 1px;
    border-bottom: 1px solid #A8C0DA;
}

.time-line-1 {
    top: 11.5%;
    left: 8%;
}

.time-line-2 {
    top: 45%;
    left: 8%;
}

.time-line-3 {
    top: 78%;
    left: 8%;
}

bus-info .time-value {
    color: white;
}

@keyframes up {
    0% {
        bottom: -400px
    }

    100% {
        bottom: 40px;
    }
}

.basic-circle {
    font-size: 6px;
}

.circle {
    position: relative;
    top: -7px;
    left: 10px;
    font-size: 6px;
}

.circle:after {
    content: '';
    position: relative;
    animation: move 2s ease-in-out infinite;
    z-index: 10;
    background-image: url('img/bus-effect.png');
    background-size: 20px 20px;
    width: 20px;
    height: 20px;
    display: inline-block;
}

@keyframes move {
    0% {
        left: -12px;
        top: 7px;
        opacity: 0;
    }

    100% {
        left: calc(10vw - 15px);
        top: 7px;
        opacity: 1;
    }
}
</style>
`
