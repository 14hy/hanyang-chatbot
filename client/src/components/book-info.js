import { LitElement, html } from 'lit-element'
import { loadXhr, scrollToLast } from '../libs/actions.js'

class BookInfo extends LitElement {	
	static get properties() {
		return { 
			searchText: { type: String},
			imageSrc: { type: Array },
			title: { type: Array },
			author: { type: Array },
			publication: { type: Array },
			isCheckout: { type: Array },
			noBookMessage: { type: String },
		}
	}
    
	constructor() {
		super()
        
		this.imageSrc = []
		this.title = []
		this.author = []
		this.publication = []
		this.isCheckout = []
		this.noBookMessage = ``
	}
    
	createRenderRoot() {
		return this
	}
    
	firstUpdated() {
		this.getBookData(this.searchText)
	}
    
	updated() {
		scrollToLast()
	}

	render() {
		return html`
        ${style}
        ${this.noBookMessage}
        ${this.title.map((book, index) => html`
        <div class="book-list">
            <div class='image-wrap'><img class='book-image' src='${this.imageSrc[index]}' alt="NO_IMAGE"/></div>
            <div class='info'>
                <div class='title'>${book}</div>
                <div class='author'>${this.author[index]}</div>
                <div class='publication'>${this.publication[index]}</div>
                <div class='isCheckout'>${this.isCheckout[index] === `대출가능` ? html`<span class="can-borrow">대출 가능</span>` : html`<span class="not-borrow">대출 중</span>`}</div>
            </div>
        </div>
        `)}        
		`
	}
    
	async getBookData(text = this.searchText) {
		let res = await loadXhr({
			url: `https://lib.hanyang.ac.kr/pyxis-api/2/collections/6/search?all=k%7Ca%7C${text}&rq=BRANCH%3D9`,
			method: `GET`,
		})

		res = JSON.parse(res)
        
		if (res.code === `success.noRecord`) {
			this.noBookMessage = `검색된 결과가 없어.`
			return 
		}

		for (let i=0; i <20; i++) {
			this.title = [...this.title, res[`data`][`list`][i][`titleStatement`]]
			this.author = [...this.author, res[`data`][`list`][i][`author`]]
			this.publication = [...this.publication, res[`data`][`list`][i][`publication`]]
			this.imageSrc = [...this.imageSrc, res[`data`][`list`][i][`thumbnailUrl`] || `https://information.hanyang.ac.kr/assets/images/hy/sub/default-item-img.png`]
			this.isCheckout = [...this.isCheckout, res[`data`][`list`][i][`branchVolumes`]
				.find(each => each.name.indexOf(`ERICA`))[`cState`]]
			console.log(this.isCheckout)
		}
	}
}

customElements.define(`book-info`, BookInfo)

const style = html`
<style>
book-info {
	display: block;
	max-height: 380px;
    overflow-y: scroll;
}

book-info::-webkit-scrollbar {	
	width: 5px;
}

book-info::-webkit-scrollbar-thumb {
	background-color: rgba(0, 0, 0, 0.3);
	border-radius: 5px;
}

.book-list {
    display: grid;
    grid-template-columns: 80px auto;
    max-width: 65vw;
    height: 120px;
    overflow: hidden;
    margin-top: 5px;
}

.book-list .book-image {
    width: 80px;
    height: 120px;
}

.book-list .info {
    display: grid;
    grid-template-rows: repeat(4, auto);
    height: 120px;
    padding-left: 5px;
}

.book-list .title {
    color: #0072bc;
    font-weight: bold;

    overflow: hidden;
    text-overflow: ellipsis;
    white-space: pre-wrap;
    word-break: break-word;
    -webkit-line-clamp: 2;
    display: -webkit-box;
    -webkit-box-orient: vertical;
}

.book-list .isCheckout {
    font-weight: bold;
}

.can-borrow {
    color: green;
}

.not-borrow {
    color: red;
}
</style>
`
