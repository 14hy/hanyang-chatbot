import i18next from 'i18next'
import locale_ko from '../_locale/ko.js'

i18next.init({
	lng: `ko`,
	debug: false,
	resources: {
		ko: {
			translation: locale_ko,
		},
	},
}).then(() => {
	const content = document.querySelectorAll(`[i18n-content]`)
	if (content) {
		content.forEach(node => {
			const key = node.getAttribute(`i18n-content`)
			node.innerHTML = i18next.t(key)
		})
	}
})
