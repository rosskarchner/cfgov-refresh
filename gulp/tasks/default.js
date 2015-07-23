'use strict';

var gulp = require( 'gulp' );

gulp.task( 'build',
  [
    'styles',
    'scripts',
    'images',
    'copy'
  ]
);

gulp.task( 'default', [ 'build' ] );
