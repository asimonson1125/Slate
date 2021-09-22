let a = await fetch("https://reserve.rit.edu/ServerApi.aspx/GetBrowseLocationsBookings", {
    "credentials": "include",
    "headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/json; charset=utf-8",
        "dea-CSRFToken": "1d7b2a7e-61c8-4c5c-9252-75daf22e8572",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1"
    },
    "referrer": "https://reserve.rit.edu/BrowseForSpace.aspx",
    "body": "{\"filterData\":{\"filters\":[{\"filterName\":\"StartDate\",\"value\":\"2021-09-15 12:00:00\",\"displayValue\":null,\"filterType\":3},{\"filterName\":\"EndDate\",\"value\":\"2021-09-16 12:00:00\",\"filterType\":3,\"displayValue\":\"\"},{\"filterName\":\"Locations\",\"value\":\"44\",\"displayValue\":\"Nathaniel Rochester Hall (043)\",\"filterType\":8},{\"filterName\":\"TimeZone\",\"value\":\"61\",\"displayValue\":\"Eastern Time\",\"filterType\":2}]}}",
    "method": "POST",
    "mode": "cors"
});
let b = await a.json()
b = JSON.parse(b.d)

// Python parsing
// https://pythonexamples.org/python-parse-json-string-example/