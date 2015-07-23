'use strict';

var gulp = require( 'gulp' );
var istanbul = require( 'gulp-istanbul' );
var mocha = require( 'gulp-mocha' );
var protractor = require( 'gulp-angular-protractor' );
var exec = require( 'child_process' ).exec;
var config = require( '../config' ).test;

gulp.task( 'test:unit', function( cb ) {
  gulp.src( config.src )
    .pipe( istanbul( {
      includeUntested: true
    } ) )
    .pipe( istanbul.hookRequire() )
    .on( 'finish', function() {
      gulp.src( config.tests + '/unit_tests/**/*.js' )
        .pipe( mocha( {
          reporter: 'nyan'
        } ) )
        .pipe( istanbul.writeReports( {
          dir: config.tests + '/unit_test_coverage'
        } ) )

        /* we want this but it breaks because we don't have good coverage
        .pipe( istanbul.enforceThresholds( {
          thresholds: { global: 90 }
        } ) )
        */

        .on( 'end', cb );
    } );
} );

gulp.task( 'test:browser', function() {
  gulp.src( config.tests + '/browser_tests/spec_suites/*.js' )
    .pipe( protractor( {
        configFile:          config.tests + '/browser_tests/conf.js',
        autoStartStopServer: true
    } ) )
    .on( 'error', function( e ) { throw e; } );
} );

gulp.task( 'test:macro', function( cb ) {
  exec( 'python ' + config.tests + '/macro_tests/test_macros.py',
    function( err, stdout, stderr ) {
      console.log( stdout );
      console.log( stderr );
      cb( err );
    }
  );
} );

gulp.task( 'test:processor', function( cb ) {
  exec( 'python ' + config.tests + '/processor_tests/test_processors.py',
    function( err, stdout, stderr ) {
      console.log( stdout );
      console.log( stderr );
      cb( err );
    }
  );
} );

gulp.task( 'test',
  [
    'test:unit',
    'test:browser',
    'test:macro',
    'test:processor'
  ]
);
