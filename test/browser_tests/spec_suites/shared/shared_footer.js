'use strict';

var Footer = require( '../../shared_components/footer.js' );

describe( 'The Footer Component', function() {
  var _sharedComponent;
  var _linkLookupArray = [ 'accessibility',
                           'foia',
                           'office of inspector general',
                           'open government',
                           'plain writing',
                           'privacy, policy & legal notices',
                           'tbd content',
                           'usa.gov'
                        ];

  beforeEach( function() {
    _sharedComponent = new Footer();
    _sharedComponent.get();
  } );

  it( 'should properly load in a browser', function() {
      expect( _sharedComponent.footer.isPresent() ).toBe( true );
    }
  );

  it( 'should include navList', function() {
      expect( _sharedComponent.navList.isPresent() ).toBe( true );
    }
  );

  it( 'should include navLinks and navLinks should be valid', function() {
    _sharedComponent.navLinks.count().then( function( count ) {
      expect( count > 0 ).toBe( true );
    } );

    _sharedComponent.navLinks.each( function( element ) {

      /* eslint-disable max-nested-callbacks */
      element.getText().then( function( text ) {
        expect( _linkLookupArray.indexOf( text.toLowerCase() ) > 0 )
        .toBe( true );
      } );

      /* eslint-enable max-nested-callbacks */
    } );

  } );

  it( 'should include post', function() {
      expect( _sharedComponent.post.isPresent() ).toBe( true );
    }
  );

  it( 'should include shareList', function() {
      expect( _sharedComponent.shareList.isPresent() ).toBe( true );
    }
  );

  it( 'should include officialWebsite', function() {
      expect( _sharedComponent.officialWebsite.isPresent() ).toBe( true );
    }
  );

} );
