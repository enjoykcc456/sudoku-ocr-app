const path = require('path')
const HtmlWebpackPlugin = require('html-webpack-plugin')

module.exports = {
  // webpack will take the files from ./src/index.tsx
  entry: {
    app: ['./src/index.tsx'],
  },
  // and output it into main.js
  output: {
    path: path.resolve(__dirname),
    filename: 'static/frontend/main.js',
  },
  resolve: {
    extensions: ['.ts', '.tsx', '.js', '.jsx'],
  },
  module: {
    rules: [
      {
        test: /\.(ts|js)x?$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
        },
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif|ico)$/,
        exclude: /node_modules/,
        use: ['file-loader?name=[name].[ext]'] // ?name=[name].[ext] is only necessary to preserve the original file name
      }
    ],
  },
  devServer: {
    // writeToDisk: true,
    watchOptions: {
      poll: true,
    },
    // proxy: {
    //   '!/static/frontend/**': {
    //     target: 'http://localhost:8000',
    //     changeOrigin: true,
    //   },
    // },
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './templates/frontend/index.html',
      favicon: './public/favicon.ico',
      inject: false
    }),
  ],
}
