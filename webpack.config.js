/*
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

const webpack = require('webpack');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');
const ManifestPlugin = require('webpack-manifest-plugin');
const _ = require('lodash');
const path = require('path');
const ENV = process.env;

module.exports = {
  entry: {
    vendor: 'entrypoints/vendor',
    dashboard: ['entrypoints/dashboard'].concat(getExtraModules())
      .concat(['entrypoints/dashboard/bootstrap'])
  },
  output: {
    filename: isProduction() ? '[name].[chunkhash].js' : '[name]_.js',
    path: path.join(__dirname, './src/ggrc/static/'),
    publicPath: '/static/'
  },
  module: {
    rules: [{
      test: /\.woff(\?v=\d+\.\d+\.\d+)?$/,
      loader: 'url?limit=10000&mimetype=application/font-woff'
    }, {
      test: /\.woff2(\?v=\d+\.\d+\.\d+)?$/,
      loader: 'url?limit=10000&mimetype=application/font-woff'
    }, {
      test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/,
      loader: 'url?limit=10000&mimetype=application/octet-stream'
    }, {
      test: /\.eot(\?v=\d+\.\d+\.\d+)?$/,
      loader: 'file'
    }, {
      test: /\.svg(\?v=\d+\.\d+\.\d+)?$/,
      loader: 'url?limit=10000&mimetype=image/svg+xml'
    }, {
      test: /\.css$/,
      use: ExtractTextPlugin.extract({
        fallback: "style-loader",
        use: {
          loader: "css-loader",
          options: { url: false }
        }
      })
    }, {
      test: /\.s[ca]ss$/,
      use: ExtractTextPlugin.extract({
        use: [{
          loader: "css-loader"
        }, {
          loader: "sass-loader"
        }],
        fallback: "style-loader"
      })
    }, {
      test: /wysihtml5-0\.4\.0pre\.js$/,
      loader: 'exports-loader?wysihtml5'
    }, {
      test: require.resolve('jquery'),
      use: [{
        loader: 'expose-loader',
        options: 'jQuery'
      },{
        loader: 'expose-loader',
        options: '$'
      }]
    }]
  },
  // devtool: 'eval',
  resolve: {
    modules: ['node_modules', 'bower_components', 'third_party']
      .map(function (dir) {
        return path.join(__dirname, dir);
      }),
    alias: {
      'can': 'canjs/amd/can/',
      'entrypoints': './src/ggrc/assets/javascripts/entrypoints'
    }
  },
  plugins: [
    new ExtractTextPlugin({
      filename: '[name].css',
      allChunks: true
    }),
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery',
      'window.jQuery': 'jquery',
      _: 'lodash',
      moment: 'moment'
    }),
    new webpack.DefinePlugin({
      GGRC_SETTINGS_MODULE: JSON.stringify(process.env.GGRC_SETTINGS_MODULE)
    }),
    new webpack.optimize.CommonsChunkPlugin({
      name: 'vendor'
    }),
    new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/),
    new ManifestPlugin({
      publicPath: '/static/'
    })
  ],
  stats: {
    errorDetails: true
  }
};

if (isProduction()) {
  module.exports.plugins.push(new UglifyJSPlugin());
}

function isProduction() {
  return ENV.NODE_ENV === 'production';
}

function getExtraModules() {
  var modules = ENV.GGRC_SETTINGS_MODULE.split(' ');

  return _.compact(_.map(modules, function (module) {
    var name;
    if (/^ggrc/.test(module)) {
      name = module.split('.')[0];
    }

    if (!name) {
      return '';
    }
    return './src/' + name + '/assets/javascripts';
  }));
}
