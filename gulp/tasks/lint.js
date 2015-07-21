'use strict';

var gulp = require( 'gulp' );
var eslint = require( 'gulp-eslint' );
var config = require( '../config' ).lint;
var handleErrors = require( '../utils/handleErrors' );


/**
 * Lints all the js files for errors
 */
gulp.task( 'lint', [
  'lint:gulp',
  'lint:src'
] );


/**
 * Lints the gulpfile for errors
 */
gulp.task( 'lint:gulp', function() {
  gulp.src( config.gulp )
    .pipe( eslint() )
    .pipe( eslint.format() )
    .on( 'error', handleErrors );
} );


/**
 * Lints the source js files for errors
 */
gulp.task( 'lint:src', function() {
  gulp.src( config.src )
    .pipe( eslint() )
    .pipe( eslint.format() )
    .on( 'error', handleErrors );
} );
