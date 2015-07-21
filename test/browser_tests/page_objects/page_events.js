'use strict';

function EventsPage() {
  this.get = function() {
    browser.get( '/events/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };
  this.nav = element( by.css( '.nav-secondary_list' ) );
  this.hero_elem = element( by.css( '.hero' ) );
  this.hero = {
    map: this.hero_elem.element( by.css( '.hero_img' ) );
    heading: this.hero_elem.element( by.css( '.summary_heading' ) );
    date: this.hero_elem.element( by.css( '.event-meta_date' ) );
    time: this.hero_elem.element( by.css( '.event-meta_time' ) );
  };
  this.events = element.all( by.css( '.post-preview__event' ) );
  this.event_elem = this.events.first();
  this.first = {
    map: this.event_elem.element( by.css( '.post-summary-image_container img' ) ),
    heading: this.event_elem.element( by.css( '.summary_heading' ) ),
    city: this.event_elem.element( by.css( '.event-meta_city' ) ),
    state: this.event_elem.element( by.css( '.event-meta_state' ) ),
    date: this.event_elem.element( by.css( '.event-meta_date' ) ),
    time: this.event_elem.element( by.css( '.event-meta_time' ) ),
    tags: this.event_elem.element( by.css( '.tags_list' ) )
  };
}

function ArchivePage() {
  this.get = function() {
    browser.get( '/events/archive' );
  };

  this.pageTitle = function() { return browser.getTitle(); };
  this.nav = element.all( by.css( '.nav-secondary_list a' ) );
  this.events = element.all( by.css( '.post-preview__event' ) );
  this.event_elem = this.events.first();
  this.first = {
    heading: this.event_elem.element( by.css( '.summary_heading' ) ),
    city: this.event_elem.element( by.css( '.event-meta_city' ) ),
    state: this.event_elem.element( by.css( '.event-meta_state' ) ),
    date: this.event_elem.element( by.css( '.event-meta_date' ) ),
    time: this.event_elem.element( by.css( '.event-meta_time' ) ),
    tags: this.event_elem.element( by.css( '.tags_list' ) )
  };
}

module.exports = {
  EventsPage: EventsPage,
  ArchivePage: ArchivePage
};
