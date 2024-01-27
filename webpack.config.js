const path = require('path');

module.exports = {
    entry: './js/index.js',
    output: {
        filename: 'index-bundle.js',
        path: path.resolve(__dirname, './static')
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                loader: "babel-loader",
                options: { presets: ["@babel/preset-env", "@babel/preset-react"] }
            },
            {
                test: /\.css$/i,
                include: path.resolve(__dirname, './js'),
                use: ['style-loader', 'css-loader', 'postcss-loader'],
            },
        ]
    }
}