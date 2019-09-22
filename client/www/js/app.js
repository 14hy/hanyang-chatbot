const routes = [
	{
		path: `/`,
		template: `<page-main class="page"></page-main>`,
		name: `home`,
		options: {
			animate: true,
		},
	},
	{
		path: `/detail/`,
		template: `<page-detail class="page"></page-detail>`,
		name: `detail`,
		options: {
			animate: true,
		},
	},
	{
		path: `(.*)`,
		url: `./index.html`,
	},
]

// Theme
let theme = `auto`
if (document.location.search.indexOf(`theme=`) >= 0) {
	theme = document.location.search.split(`theme=`)[1].split(`&`)[0]
}

// Init App
window.app = new Framework7({
	id: `com.example.mac.tour`,
	name: `맥투`,
	root: `#app`,
	theme: theme,
	routes: routes,
	touch: {
		fastClicks: true,
	},
	smartSelect: {
		setValueText: true,
		openIn: `popup`,
		closeOnSelect: true,
	},
	popover: {
		backdrop: false,
		animate: true,
	},
})

window.mainView = window.app.views.create(`.view-main`, {
	url: `/`,
})
