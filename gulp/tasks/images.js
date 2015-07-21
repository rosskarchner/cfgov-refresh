'use strict';

var gulp = require( 'gulp' );
var changed = require( 'gulp-changed' );
var imagemin = require( 'gulp-imagemin' );
var config = require( '../config' ).images;
var handleErrors = require( '../utils/handleErrors' );
var browserSync = require( 'browser-sync' );

gulp.task( 'images', function() {
  return gulp.src( config.src )
    .pipe( changed( config.dest ) )
    .pipe( imagemin() )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( config.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
} );
