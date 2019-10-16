const MonacoWebpackPlugin = require('monaco-editor-webpack-plugin')

module.exports = {
  configureWebpack: {
    devtool: 'source-map',
    plugins: [
      new MonacoWebpackPlugin()
    ]
  },
  productionSourceMap: false,
  publicPath: process.env.NODE_ENV === 'production'
    ? './dist'
    : '/',
  outputDir: '../lyrebird_bugit/dist',
  devServer: {
    proxy: 'http://localhost:9090'
  }
}
