/* ==========================================================================
   Sliding/Pushing Menu
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );
require( './jquery/cfpb-aria-button' ).init();

var _$window = $( window );
var _$body = $( 'body' );
var _$slidingNav = $( '.sliding-nav' );
var _$slidingNavTrigger = $( '.sliding-nav_trigger' );
var _$slidingNavNav = $( '.sliding-nav_nav' );
var _$slidingNavPage = $( '.sliding-nav_page' );
var _$slidingNavPageOverlay = $( '.sliding-nav_page-overlay' );

function init() {
  _$slidingNavTrigger.click( _slidingNavTriggerClick );

  // Expanding list
  // TODO: Determine if we should actually use the cfpbAriaButton plugin.
  $( '.list-expanding_trigger' ).cfpbAriaButton();
  $( '.list-expanding_trigger' ).click( _listExpandingTriggerClick );
  $( '.list-expanding_trigger' ).keyup( _listExpandingTriggerKeyUp );

  // Hide the child lists initially.
  $( '.list-expanding_child-list' ).hide();
}

function _listExpandingTriggerClick( e ) {
  e.preventDefault();
  $( this ).next().find( '.list-expanding_child-list' ).slideToggle( 100 );
}

function _listExpandingTriggerKeyUp( e ) {
  // Return if the space key was not pressed.
  if ( e.which !== 32 ) {
    return;
  }
  e.preventDefault();
  $( this ).next().find( '.list-expanding_child-list' ).slideToggle( 100 );
}

function _slidingNavTriggerClick( e ) {
  e.preventDefault();

  // First deal with the filters button if it exists.
  if ( $( '.l-sidenav' ).hasClass( 'is-open' ) ) {
    $( '.l-sidenav-btn' ).trigger( 'click' );
  }

  if ( _$slidingNav.hasClass( 'is-open' ) ) {
    //window.setTimeout( _slidingNavDisabledDelay, 200 );
    _$slidingNav.removeClass( 'is-open' );
    _$slidingNavPageOverlay.off( 'click' );
  } else {
    _$slidingNav.addClass( 'is-open' );
    _$window.scroll( _slidingNavStopScroll );
    _$slidingNavPageOverlay.click( _slidingNavPageOverlayClick );
  }
  _$body.scrollTop( 0 );
}

function _slidingNavDisabledDelay() {
  _$slidingNavPage.removeClass( 'is-scroll-disabled' );
}

function _slidingNavPageOverlayClick( e ) {
  e.preventDefault();
  $( _$slidingNavTrigger[0] ).trigger( 'click' );
}

function _slidingNavStopScroll() {
  if ( parseInt( _$slidingNavPage.css( 'margin-right' ), 10 ) >= 0 ) {
    return;
  }
  _$slidingNavPage.addClass( 'is-scroll-disabled' );
  _$slidingNavNav.css( 'min-height', _$window.height() );
  _$window.off( 'scroll', _slidingNavStopScroll );
}

// Expose public methods.
module.exports = { init: init };
