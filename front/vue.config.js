const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  // publicPath: "https://10.10.10.102/static/app", // for dev server 10.10.10.102
  publicPath: "http://0.0.0.0:8080", // for localhost dev
  // publicPath: "http://127.0.0.1:8000/static/app", // for localhost deploy
  outputDir: '../static/app/',

  chainWebpack: config => {

    config.optimization
        .splitChunks(false)
    config
        .plugin('BundleTracker')
        .use(BundleTracker, [{filename: '../front/webpack-stats.json'}])

    config.resolve.alias
        .set('__STATIC__', 'static')

    config.devServer
        .public('http://0.0.0.0:8080')
        .host('0.0.0.0')
        .port(8080)
        .hotOnly(true)
        .watchOptions({poll: 1000})
        .https(false)
        .headers({"Access-Control-Allow-Origin": ["\*"]})
  }
};