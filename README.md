# Slate
Event scheduling, simplified

## What's the point of events without turnout?
Scheduling events can be tricky - with so many participants, having everyone sift through their calendars to find times when most people can attend is a little tedious at best and a logistical nightmare at worst.

Slate streamlines the process by collecting calendar data from participants and automatically determining the best times to meet.

## How It's Made:
 - Uses a Flask webserver with Jinja web templating 
 - Downloads participant calendars in ical format, parsed via recurring_ical_events
 - Checks each calendar's availability on each interval, with custom optimizations excluding irrelevant events
 - Math
 - Returns a calendar grid scoring each time that an event could be hosted

## Backlog
 - select low scores between times of day
 - optimize event searching algorithm
    - Make my own recurring event calculator (possibly paired with parser overhaul, removing most ical libs dependancy)
 - Improve error messages for bad urls

## Notes
 - datetime dependancy doesn't handle daylight savings to standard changes very well.  Expect an error if a time interval includes a spring forward date and the event length is less than or equal to 60 minutes
 - the Adjust for Daylight Savings tick is based on US time standards and does not reflect other international timezone alterings.  Additionally, Slate makes time adjustments at midnight, rather than 2 AM for scheduling simplicity's sake.  It's not a bug, it's a feature that makes coding easier.
 - 'transparent' events are passed over as it is assumed that the calendar's user is free during the allotted time.  However, events marked for dates and not times default to this transparent state.  I wholly expect there will be confusion over this.  If there's an 'all day event' that isn't showing up, it's probably because the event was given the 'free' tag, rather than the 'busy' tag.
 - Events that are 'all-day' are rendered in slate as 24-hour long events based on the calendar (or event) timezone.  Some calendar software visualizes this as a midnight-to-midnight event regardless of timezone, which makes no sense.  Humans suck at being precise with their times.