'use strict';

// Required for IE8 support.
require( './polyfill/event-listener.js' );
require( './polyfill/query-selector.js' );

/**
 * Makes a table row whose first table cell child is a link become the link
 * for the entire table row.
 */
function init() {
  var rows = document.querySelectorAll( '.simple-table__row-links tr' );
  for ( var i = rows.length - 1; i >= 0; i-- ) {
    _listenForRowClick( rows[i] );
  }
}

/**
 * Add a listener to a row.
 *
 * @param {HTMLElement} row A tr element in a table.
 */
function _listenForRowClick( row ) {
  // The anonymous function is needed since IE8
  // can't find the event's currentTarget otherwise.
  row.addEventListener( 'mousedown', function() {
    _rowClicked( row );
  }, false );
}

/**
 * Handle a click of a row.
 *
 * @param {HTMLElement} row A tr element in a table.
 */
function _rowClicked( row ) {
  var link = row.querySelector( 'a' );
  window.location = link.getAttribute( 'href' );
}

module.exports = { init: init };
