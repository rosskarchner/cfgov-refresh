'use strict';

var gulp = require( 'gulp' );

gulp.task( 'build',
  [
    'lint:src',
    'test:unit',
    'styles',
    'scripts',
    'images',
    'copy'
  ]
);

gulp.task( 'default', [ 'build' ] );
