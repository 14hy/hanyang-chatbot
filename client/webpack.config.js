const path = require(`path`)
const MiniCssExtractPlugin = require(`mini-css-extract-plugin`)

module.exports = {
	entry: {
		"main-bundle": [`./src/main.js`],
	},
	output: {
		path: path.resolve(__dirname, `./www`),
		filename: `[name].js`,
	},
	plugins: [
		new MiniCssExtractPlugin({ filename: `css/style.css` }),
	],
	module: {
		rules: [
			{
				test: /\.m?js$/,
				exclude: /(node_modules|bower_components)\/(?!(lit-html))/,
				use: {
					loader: `babel-loader`,
					options: {
						presets: [`@babel/preset-env`],
					},
				},
			},
			{
				test: /\.js$/,
				exclude: /node_modules/,
				use: [`eslint-loader`],
			},
			{
				test: /\.(css|scss)$/,
				exclude: /node_modules/,
				use: [
					MiniCssExtractPlugin.loader, 
					/* `style-loader`, */ 
					`css-loader`, 
					`sass-loader?outputStyle=expanded`,
					`postcss-loader`,
				],
			},
			{
				test: /\.(png|svg|jpe?g|gif)$/,
				exclude: /node_modules/,
				loader: `file-loader`,
				options: {
					publicPath: `/src/`,
					name: `[name].[ext]?[hash]`,
				},
			},
			{
				test: /\.(png|svg|jpe?g|gif)$/,
				exclude: /node_modules/,
				loader: `url-loader`,
				options: {
					publicPath: `/src/`,
					name: `[name].[ext]?[hash]`,
					limit: 10000,
				},
			},
		],
	},	
	devServer: {
		hot : true,
		contentBase: path.join(__dirname, `/www`),
		watchContentBase: true,
		historyApiFallback: true,
		compress: true,
		host: `0.0.0.0`,
		disableHostCheck: true,
		port: 9000,
	},
	devtool: `inline-source-map`,
}
