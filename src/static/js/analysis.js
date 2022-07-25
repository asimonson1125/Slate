/**
 * analysis() calls all analysis
 */
function analysis() {
    percentileWeek(0);
}

function percentileWeek(percentage) {
    let t = document.getElementById('timescroll');
    const intervalsPerDay = document.querySelectorAll("#timescroll > tbody > tr").length - 1
    const hours = document.querySelectorAll("#timescroll > tbody > tr");

    const daysOfWeek = hours[0].querySelectorAll("p")

    let i = 0;
    while (daysOfWeek[i].textContent !== 'Sun') {
        i++;
    }
    dayOfWeek = (i - 7) * -1;

    // model: [Sun, Mon, Tue, Wed, Thu, Fri, Sat]
    // each of those days of the week contains x arrays, x = intervals in a day
    // each of those arrays contains a list of all of the scores that time slot has
    // ie. weeks[0][1] = [all scores for Sunday between 1am and 2am]
    let weeks = []
    for (let i = 0; i < 7; i++) {
        weeks[i] = [];
        for (let x = 0; x < intervalsPerDay; x++) {
            weeks[i][x] = [];
        }
    }
    for (let hour = 1; hour < hours.length; hour++) {
        const ofHour = hours[hour].querySelectorAll("td");
        for (let day = 0; day < ofHour.length; day++) {
            let score = ofHour[day].querySelector('.iscore');
            if (score != null) {
                weeks[(dayOfWeek + day) % 7][hour - 1].push(parseInt(score.textContent));
            }
        }
    }
    const sample = t.querySelector('.cell').parentNode.parentNode.cloneNode(true);
    if (sample.classList.contains('hidden')) {
        sample.classList.toggle('hidden');
    }
    sample.querySelector('.moreInfo').removeChild(sample.querySelector('h4'))
    sample.querySelector('.moreInfo').removeChild(sample.querySelector('ul'))
    let maxScore = sample.querySelector('p').textContent;
    maxScore = parseInt(maxScore.substring(maxScore.indexOf('/') + 2));

    const timeIntervals = t.querySelectorAll('.rowLabel');
    let table = document.getElementById('percentileTable');
    for (let i = 0; i < timeIntervals.length; i++) {
        let row = document.createElement('tr');
        let label = timeIntervals[i].cloneNode(true);
        row.appendChild(label);
        for (let day = 0; day < 7; day++) {
            let newDP = sample.cloneNode(true);
            let sum = 0;
            for(let d = 0; d < weeks[day][i].length; d++){
                sum += weeks[day][i][d];
            }
            score = sum/weeks[day][i].length;
            score = Math.round(score*1000)/1000
            const hue = 100 - Math.pow(score / maxScore, .75) * 100;
            newDP.querySelector('.roll').style.backgroundColor = `hsla(${hue}, 100%, 35%, 1)`;
            newDP.querySelector('.iscore').textContent = score;
            row.appendChild(newDP);
        }
        table.appendChild(row);
    }
}

