'use strict';

var env = require( './environment.js' );

exports.config = {
  multiCapabilities: [
    {
      browserName: 'chrome',
      specs: [ 'spec_suites/shared/*.js' ],
    },
    {
      browserName: 'firefox',
      specs: [ 'spec_suites/shared/*.js' ],
    },
    // Large Screen only tests
    {
      browserName: 'chrome',
      chromeOptions: {
        args: [ '--lang=en',
                '--window-size=1200,900' ]
      },
      specs: [ 'spec_suites/large_screen/*.js' ]
    }
  ],

  baseUrl: env.baseUrl,

  onPrepare: function() {
    browser.ignoreSynchronization = true;
    return;
  }
};
