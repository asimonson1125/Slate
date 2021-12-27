from sanitizer import isCalendar
import staticCalendars
import availabilityHandler

"""
the main, haha.
"""


def get_cals(urls):
    problems = []
    calendars = []
    out = ""
    for i in range(len(urls)):
        try:
            calendar = isCalendar(urls[i])
            if(calendar):
                assert calendar.get("CALSCALE", "GREGORIAN") == "GREGORIAN", problems.append(
                    "In calendar at " + urls[i] + ": non-gregorian calendar detected")
                calendars.append(calendar)
            else:
                problems.append(
                    'Calendar could not be found at "' + urls[i] + '".')
        except Exception as e:
            problems.append(e)
    # prompt user with errors
    for i in problems:
        out += "<p>" + str(i) + "</p>"
    if out != "":
        return out
    return calendars


def max_score(scores):
    sum = 0
    for score in scores:
        sum += score
    return sum


def run(calendars, scores, start, end, interval, length):
    out = outHead()
    grid = "<div class='hoverBox'>"
    times = availabilityHandler.timesBetween(start, end, interval)
    for time in times:
        availabilities = availabilityHandler.availableFor(
            calendars, time, time + length)
        score = availabilityHandler.availabilityScore(
            availabilities, scores)
        grid += "<div class='roll'><div class='container'><div class='moreInfo'><h3>" + \
            time.strftime("%d/%m/%Y - %I:%M:%S") + " to " + (time + length).strftime(
                "%I:%M:%S") + "</h3><p>Score: " + str(score) + "</p><h4>Unavailable:</h4><ul>"
        for i in range(len(availabilities)):
            if availabilities[i][1] == False:
                grid += "<li>" + \
                    availabilities[i][0].name + \
                        ", score: " + str(scores[i]) + "</li>"
        grid += "</div></div></div>"
    grid += "</div>"
    out += grid
    out += outClose()
    return out


def outHead():
    return """<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" type="text/css" href="../static/css/style.css">
</head>
<body>"""


def outClose():
    return """</body>
    </html>"""
