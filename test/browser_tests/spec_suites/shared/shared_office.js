var Office = require( '../../page_objects/page_office.js' );

describe( 'The offices template', function() {
  it( 'should properly load in a browser', function() {
    var page = new Office();
    page.get( 'ProjectCatalyst' );
    expect( page.pageTitle() ).toBe( 'Project Catalyst' );
  } );

  it( 'should include main title', function() {
    var page = new Office();
    page.get( 'ProjectCatalyst' );
    expect( page.mainTitle ).toBe( 'Project Catalyst' );
  } );

  it( 'should include intro text', function() {
    var page = new Office();
    page.get( 'ProjectCatalyst' );
    expect( page.introText ).toContain( 'Our mission' );
  } );

} );
