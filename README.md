# Slate
Event scheduling, simplified

## What's the point of events without turnout?
Scheduling events can be tricky - with so many participants, having everyone sift through their calendars to find times when most people can attend is a little tedious at best and a logistical nightmare at worst.

Slate streamlines this process by collecting calendar data from participants and automatically determining the best times to meet.\

## Current Functionality
* Input a collection of urls representing ics calendar files
* Output availability scores over a time period representing  how many people can come

## Goals
* Users can add their Google and Apple calendars to their profile
* Users can select participants and view their shared availabilities as determined by their calendars compiled into a single documemt
* Coordinators can filter availability options by time of the day and days of the week
* Filter by required attendance - exclude all times that essential participants (like event locations or guest speakers) can't make.

## Stretch targets
* If an event has a location, subtract availability times following events also with location data by determining travel time + gradient for margin of error

## Known bugs
* Events created with a timezone different from the calendar default are misrepresented (ical lib bug)