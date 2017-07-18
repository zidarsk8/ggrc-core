/*
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

const webpack = require('webpack');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');
const _ = require('lodash');
const path = require('path');
const GGRC = {
  get_dashboard_modules: function () {
    return _.compact(_.map(process.env.GGRC_SETTINGS_MODULE.split(' '), function (module) {
      var name;
      if (/^ggrc/.test(module)) {
        name = module.split('.')[0];
      }
      if (module === 'development') {
        name = 'ggrc';
      }
      if (!name) {
        return '';
      }
      return './src/' + name + '/assets/assets';
    }));
  }
};

module.exports = {
  entry: {
    vendor: 'ggrc/vendor',
    dashboard: GGRC.get_dashboard_modules()
  },
  output: {
    filename: '[name]_.js',
    path: path.join(__dirname, './src/ggrc/assets/stylesheets/'),
    publicPath: '/src/ggrc/static/'
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
      loader: ExtractTextPlugin.extract(['style-loader', 'css-loader'])
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
    }]
  },
  devtool: 'eval',
  resolve: {
    modules: ['node_modules', 'bower_components', 'third_party']
      .map(function (dir) {
        return path.join(__dirname, dir);
      }),
    alias: {
      'can': 'canjs/amd/can/',
      'ggrc': './src/ggrc/assets/javascripts'
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
    new webpack.optimize.CommonsChunkPlugin({
      name: 'vendor'
    }),
    new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/),
    new UglifyJSPlugin()
  ],
  stats: {
    errorDetails: true
  }
};
