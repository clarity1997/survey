const path = require('path');
require("babel-polyfill");

module.exports = {
  mode: 'production', // 设置为生产模式 production, 开发模式 development
  entry: ["babel-polyfill", './src/index.js'],
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'static'),
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react',],
          },
        },
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],
  },
};