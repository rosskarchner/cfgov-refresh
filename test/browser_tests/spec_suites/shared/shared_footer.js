'use strict';

var Footer = require( '../../page_components/footer.js' );

describe( 'The Footer Component', function() {
  var _component;
  var _linkLookupArray = ['accessibility',
                          'foia',
                          'office of inspector general',
                          'open government',
                          'plain writing',
                          'privacy, policy & legal notices',
                          'tbd content',
                          'usa.gov'
                        ];

  beforeEach( function() {
    _component = new Footer();
    _component.get();
  } );

  it( 'should properly load in a browser', function() {
      expect( _component.footer.isPresent() ).toBe( true );
    }
  );

  it( 'should include navList', function() {
      expect( _component.navList.isPresent() ).toBe( true );
    }
  );

  it( 'should include navLinks and navLinks should be valid', function() {
      _component.navLinks.count().then( function( count ){
        expect( count > 0 ).toBe( true );
      } );

      _component.navLinks.each( function( element, index ) {
        element.getText().then( function ( text ) {
          expect( _linkLookupArray.indexOf( text.toLowerCase() ) > 0 ).toBe( true );
        } )
      } );
  } );

  it( 'should include post', function() {
      expect( _component.post.isPresent() ).toBe( true );
    }
  );

  it( 'should include shareList', function() {
      expect( _component.shareList.isPresent() ).toBe( true );
    }
  );

  it( 'should include officialWebsite', function() {
      expect( _component.officialWebsite.isPresent() ).toBe( true );
    }
  );

} );
