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

  this.mainTitle = element( by.css( 'main > .wrapper > \
                                     div > section > h1' ) );

  this.introText = element( by.css( 'main > .wrapper > \
                                     div > section > section > \
                                     section > div') );

  // TODO: Include show_subscription when page that uses this value is found.
  // this.subscription = element( by.css( '') );

  this.topStoryHead = element( by.css( 'main > .wrapper > \
                                        div > section > section:nth-child(3) > \
                                        h2' ) );

  this.topStoryDesc = element( by.css( 'main > .wrapper > \
                                        div > section > section:nth-child(3) > \
                                        div > div:nth-child(1) > \
                                        p.short-desc' ) );

  this.topStoryLinks = element( by.css( 'main > .wrapper > \
                                         div > section > section:nth-child(3) > \
                                         div > div > ul' ) );

  // Check resources against /office-of-financial-education/
  // TODO: Include resource_title when page that uses this value is found.
  // this.resourceTitle = element( by.css( '' ) );

  this.resourceImg = element( by.css( 'main > .wrapper > \
                                       div > section > section:nth-child(4) > \
                                       div:nth-child(2) > div > \
                                       .media_image' ) );

  this.resourceTitle = element( by.css( 'main > .wrapper > \
                                         div > section > section:nth-child(4) > \
                                         div:nth-child(2) > .media_body > \
                                         h2' ) );

  this.resourceDesc = element( by.css( 'main > .wrapper > \
                                        div > section > section:nth-child(4) > \
                                        div:nth-child(2) > .media_body > \
                                        .short-desc' ) );

  this.resourceLink = element( by.css( 'main > .wrapper > \
                                        div > section > section:nth-child(4) > \
                                        div:nth-child(2) > .media_body > \
                                        a' ) );

  // Check subpages against /plain-writing/
  this.subpages = element( by.css( 'main > .wrapper > \
                                    div > section > section > h1' ) );


}

module.exports = OfficePage;
