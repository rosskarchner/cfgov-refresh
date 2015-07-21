'use strict';

var gulp = require( 'gulp' );
var sourcemaps = require( 'gulp-sourcemaps' );
var less = require( 'gulp-less' );
var header = require( 'gulp-header' );
var autoprefixer = require( 'gulp-autoprefixer' );
var pkg = require( '../config' ).pkg;
var banner = require( '../config' ).banner;
var config = require( '../config' ).styles;
var handleErrors = require( '../utils/handleErrors' );
var browserSync = require( 'browser-sync' );

gulp.task( 'styles', function() {
  return gulp.src( config.cwd + config.src )
    .pipe( sourcemaps.init() )
    .pipe( less( config.settings ) )
    .on( 'error', handleErrors )
    .pipe( autoprefixer( {
      browsers: [ 'last 2 version' ]
    } ) )
    .pipe( header( banner, { pkg: pkg } ) )
    .pipe( sourcemaps.write( '.' ) )
    .pipe( gulp.dest( config.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
} );
