'use strict';

function Footer() {
  this.get = function() {
    browser.get( '/' );
  };

  this.footer = element( by.css( '.footer' ) );
  this.navList = this.footer.element( by.css( '.footer_nav-list' ) );

  this.navLinks = element.all( by.css( '.footer-middle-left .footer_list a, .footer-middle-right .footer_list a' ) );
  this.post = this.footer.element( by.css( '.footer-post' ) );
  this.shareList = this.footer.element( by.css( '.footer_share-icon-list' ) );
  this.officialWebsite = this.footer.element( by.css( '.footer_official-website' ) );
}

module.exports = Footer;
