const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
    // the output bundle won't be optimized for production but suitable for development
    mode: 'development',
    // the app entry point is /src/index.js
    entry: path.resolve(__dirname, 'src', 'index.js'),
    output: {
        // the output of the webpack build will be in /public directory
        path: path.resolve(__dirname, '/public'),
        // the filename of the JS bundle will be bundle.js
        filename: 'bundle.js',
        publicPath: '/',
    },
    module: {
        rules: [
            {
                // for any file with a suffix of js or jsx
                test: /\.jsx?$/,
                // ignore transpiling JavaScript from node_modules as it should be that state
                exclude: [/node_modules/, /public/],
                // use the babel-loader for transpiling JavaScript to a suitable format
                loader: 'babel-loader',
                options: {
                    // attach the presets to the loader (most projects use .babelrc file instead)
                    presets: ["@babel/env", "@babel/react"],
                    plugins: [
                        "@babel/plugin-proposal-class-properties"
                    ]
                }
            },
            {
                test: /\.s(a|c)ss$/,
                use: [
                    {
                        loader: MiniCssExtractPlugin.loader
                    },
                    {
                        loader: 'css-loader'
                    },
                    {
                        loader: 'postcss-loader'
                    },
                    {
                        loader: 'sass-loader',
                        // options: {
                        //     includePaths: [
                        //         path.resolve(__dirname, './node_modules')
                        //     ]
                        // }
                    }
                ]
            },
            { // solve @import
                test: /\.css$/,
                use: [
                    'style-loader',
                    'css-loader'
                ]
            },
            {
                test: /\.html$/,
                exclude: /index\.html/,
                loader: 'html-loader',
            },
            {
                test: /\.script\.js$/,
                loader: 'script-loader',
            },
        ],
    },
    // add a custom index.html as the template
    plugins: [new HtmlWebpackPlugin({ template: path.resolve(__dirname, 'src', 'index.html') })],
    // auto reload
    devServer: {
        historyApiFallback: true, // solve "cannot GET /*"
        // contentBase: '/',
        hot: true,
        contentBase: path.join(__dirname, '/public'), // serve your static files from here
        watchContentBase: true, // initiate a page refresh if static content changes
        proxy: [ // allows redirect of requests to webpack-dev-server to another destination
            {
                context: ['/api', '/auth'],  // can have multiple
                target: 'http://localhost:8080', // server and port to redirect to
                secure: false,
            },
        ],
        port: 6006, // port webpack-dev-server listens to, defaults to 8080
        overlay: { // Shows a full-screen overlay in the browser when there are compiler errors or warnings
            warnings: false, // defaults to false
            errors: false, // defaults to false
        },
    },
};