'use strict';

var Office = require( '../../page_objects/page_office.js' );

describe( 'The Project Catalyst Page', function() {
  var page;

  beforeEach( function() {
    page = new Office();
    page.get( 'ProjectCatalyst' );
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toBe( 'Project Catalyst' );
  } );

  it( 'should include main title', function() {
    expect( page.mainTitle.isPresent() ).toBeTruthy();
    expect( page.mainTitle.getText() ).toBe( 'Project Catalyst' );
  } );

  it( 'should include intro text', function() {
    expect( page.introText.isPresent() ).toBeTruthy();
    expect( page.introText.getText() ).toContain( 'Our mission' );
  } );
} );

describe( 'The Plain Writing Page', function() {
  var page;

  beforeEach( function() {
    page = new Office();
    page.get( 'PlainWriting' );
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toBe( 'Plain Writing' );
  } );

  it( 'should include main title', function() {
    expect( page.mainTitle.isPresent() ).toBeTruthy();
    expect( page.mainTitle.getText() ).toBe( 'Plain Writing' );
  } );

  it( 'should include intro text', function() {
    expect( page.introText.isPresent() ).toBeTruthy();
    expect( page.introText.getText() ).toContain( 'adopted plain language' );
  } );
} );
