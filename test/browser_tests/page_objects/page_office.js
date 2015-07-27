function OfficePage() {
  this.get = function( officePage ) {
    var examplePages = {
        ProjectCatalyst: '/offices/project-catalyst/',
        OfficeOfFinancialEducation: '/offices/office-of-financial-education/',
        PlainWriting: '/offices/plain-writing/'
    };

    browser.get( examplePages[officePage] );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.mainTitle = element( by.css( '.qa-main-title' ) );

  this.introText = element( by.css( '.office_intro-text') );

  // TODO: Include show_subscription when page that uses this value is found.
  // this.subscription = element( by.css( '') );

  this.topStoryHead = element( by.css( '.qa-top-story-head' ) );

  this.topStoryDesc = element( by.css( '.qa-top-story-desc' ) );

  this.topStoryLinks = element( by.css( '.qa-top-story-links' ) );

  // Check resources against /office-of-financial-education/
  // TODO: Include resource_title when page that uses this value is found.
  // this.resourceTitle = element( by.css( '' ) );

  this.resourceImg = element( by.css( '.qa-resource-img' ) );

  this.resourceTitle = element( by.css( '.qa-resource-title' ) );

  this.resourceDesc = element( by.css( '.qa-resource-desc' ) );

  this.resourceLink = element( by.css( '.qa-resource-link' ) );

  // Check subpages against /plain-writing/
  this.subpages = element( by.css( '.qa-subpage h2' ) );


}

module.exports = OfficePage;
