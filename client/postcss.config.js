module.exports = {
	plugins: [
		require(`autoprefixer`)({ grid: true, browsers: [`last 4 versions`, `ie 11`] }),
	],
}
