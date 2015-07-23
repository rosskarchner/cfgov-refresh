'use strict';

var gulp = require( 'gulp' );
var changed = require( 'gulp-changed' );
var config = require( '../config' ).copy;
var handleErrors = require( '../utils/handleErrors' );
var browserSync = require( 'browser-sync' );

gulp.task( 'copy:files', function() {
  return gulp.src( config.files.src )
    .pipe( changed( config.files.dest ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( config.files.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
} );

gulp.task( 'copy:legacy', function() {
  return gulp.src( config.legacy.src )
    .pipe( changed( config.legacy.dest ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( config.legacy.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
} );

gulp.task( 'copy:js', function() {
  return gulp.src( config.js.src )
    .pipe( changed( config.js.dest ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( config.js.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
} );

gulp.task( 'copy:icons', function() {
  return gulp.src( config.icons.src )
    .pipe( changed( config.icons.dest ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( config.icons.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
} );

gulp.task( 'copy:pdfcss', function() {
  return gulp.src( config.pdfcss.src )
    .pipe( changed( config.pdfcss.dest ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( config.pdfcss.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
} );

gulp.task( 'copy:pdffonts', function() {
  return gulp.src( config.pdffonts.src )
    .pipe( changed( config.pdffonts.dest ) )
    .on( 'error', handleErrors )
    .pipe( gulp.dest( config.pdffonts.dest ) )
    .pipe( browserSync.reload( {
      stream: true
    } ) );
} );

gulp.task( 'copy',
  [
    'copy:files',
    'copy:legacy',
    'copy:js',
    'copy:icons',
    'copy:pdfcss',
    'copy:pdffonts'
  ]
);
