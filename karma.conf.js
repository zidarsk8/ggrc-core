// Karma configuration
// Generated on Mon Jan 12 2015 22:30:27 GMT+0000 (UTC)

module.exports = function(config) {
  var configuration = {

    // base path that will be used to resolve all patterns (eg. files, exclude)
    basePath: '',


    // frameworks to use
    // available frameworks: https://npmjs.org/browse/keyword/karma-adapter
    frameworks: ['jasmine'],


    // list of files / patterns to load in the browser
    files: [
        'src/ggrc/static/dashboard-specs.js',
        'src/ggrc/static/dashboard.js',
        'src/ggrc/static/dashboard-spec-helpers.js',
        'src/ggrc/static/dashboard-templates.js',

        // {pattern: 'src/**/assets/js_specs/**/*.js',
        //  watched: true,
        //  served: false,
        //  included: false},
        // {pattern: 'src/**/assets/javascripts/**/*.js',
        //  watched: true,
        //  served: false,
        //  included: false}
    ],


    // list of files to exclude
    exclude: [
      //'src/**/assets/js_specs/**/*_spec.js',
      //'src/**/assets/javascripts/**/*.js'
    ],


    // preprocess matching files before serving them to the browser
    // available preprocessors: https://npmjs.org/browse/keyword/karma-preprocessor
    preprocessors: {
    },


    // test results reporter to use
    // possible values: 'dots', 'progress'
    // available reporters: https://npmjs.org/browse/keyword/karma-reporter
    reporters: ['progress'],


    // web server port
    port: 9876,


    // enable / disable colors in the output (reporters and logs)
    colors: true,


    // level of logging
    // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
    logLevel: config.LOG_INFO,


    // enable / disable watching file and executing tests whenever any file changes
    autoWatch: true,


    // start these browsers
    // available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
    browsers: [/*'PhantomJS'*/],

    customLaunchers: {
        Chrome_travis_ci: {
            base: 'Chrome',
            flags: ['--no-sandbox']
        }
    },


    // Continuous Integration mode
    // if true, Karma captures browsers, runs the tests and exits
    singleRun: false
  };

  if (process.env.TRAVIS) {
      configuration.browsers = ['Chrome_travis_ci'];
  }

  config.set(configuration);
};
