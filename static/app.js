/*Append counties into SelectField */
$(document).ready( async function() {
    $('#counties').hide()

    //default data will be Los Angeles County California with code = 06037
    covidCases('06037')
    retrieveData()

    res = await $.get(`/demographics/06/037`);
    appendInfo(res);

    $('#State').on('change', async function (evt){
        evt.preventDefault()
        $('#counties').show()
 
        state = $('#State').val()
        response = await $.get(`/county/${state}`)    

        $('#counties_list').empty()
        for(let y=0; y < response.length; y++) {
            $('#counties_list').append(
            `<option value =${response[y][0]}> ${response[y][1]} </option>`
            )
        }
    })

})

/*Append demographic information into the Demographics Section */
function demographicsTable() {
$(document).ready(function() {
    $('#counties_list').on('change', async function(evt) {

        evt.preventDefault()
        showContents()

        state = $('#State').val()
        if (state.length < 2) {
            state = '0' + state;
        }

        county = $('#counties_list').val()
        if (county.length < 3) {
            county = '0' + county;
        }
        
        res = await $.get(`/demographics/${state}/${county}`)
        joint_code = await $.get(`/cases/${state}/${county}`)

        covidCases(joint_code[0], joint_code[1] )
        try {
        appendInfo(res)
        } catch(TypeError) {
            alert('Invalid State/County Combination')
        }
    })
})

}

//Retrieves county level covid cases and calls graph_cases function
async function covidCases(joint_code, county_name){

    if (county_name == undefined){ 
        county_name = 'Los Angeles County'
        } else {
            county_name=county_name
        }

    cases_resp = await $.get(`/cases/${joint_code}`)
    len = cases_resp["actualsTimeseries"].length

    let cases_arry = []
    let deaths_arry = []
    let dates_arry = []

    for(let y=5; y < len-1; y++ ){
        if (y%30 == 0) {
            cases = cases_resp["actualsTimeseries"][y]['cases']
            deaths = cases_resp["actualsTimeseries"][y]['deaths']
            date = cases_resp["actualsTimeseries"][y]['date']

            if(cases != null && cases != 0) {
                cases_arry.push(cases)
                deaths_arry.push(deaths)
                dates_arry.push(date)
            }
            
        }
    }
    graph_cases(cases_arry, deaths_arry, dates_arry, county_name)
}

//Draws a line graph with information from covidCases function
async function graph_cases(cases_arry, deaths_arry, dates_arry, county_name) {

    var ctx = $('#myChart');
    var ctx = document.getElementById('myChart');
    var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: dates_arry,
        datasets: [{
            label: 'Covid cases over time',
            data: cases_arry,
            borderColor: [
                'rgba(255, 159, 64, 1)'
            ]
        }, {
            label: 'Covid deaths over time',
            data: deaths_arry,
            borderColor: [
                'red'
            ]
            }]
        },
    options: {
        title: {
            display: true,
            text: `${county_name} Cases & Deaths`,
            fontSize: 30,
            fontFamily: "Segoe UI",
            fontColor: 'black',

        }
    }
})

}

//Extracts different data regarding states and appends them into a table
async function retrieveData() {

    $('#info').empty()
    resp2 = await $.get(`/states`)

    for (let y = 0; y < 53; y++) {

    riskLevelss = resp2[y]['riskLevels']['overall']
    caseDensitys = Math.round(resp2[y]['metrics']["caseDensity"])
    
    populations = resp2[y]['population']
    states = resp2[y]['state']
    casess = resp2[y]["actuals"]['cases']
    deathss = resp2[y]['actuals']['deaths']

    $('#info').append(`
        <tr>
            <td> ${states} </td>
            <td> ${casess} </td>
            <td> ${deathss} </td>
            <td> ${populations} </td>
            <td> ${caseDensitys} </td>
            <td> ${riskLevelss} </td>
        </tr>
            `)
}
$('#compare').DataTable();

}


//Helper Functions

/* Empty the demographics area */
function emptyDom() {
    $('#education').empty()
    $('#population').empty()
    $('#population_density').empty()
    $('#poverty').empty()
}

/*show or hide contents after submit button is hit*/
function showContents(){
    $('#statesData').show()
    $('.demographic').show()
}

function appendInfo(res) {
    emptyDom()
    console.log(res)
    educatedCount = res[0][1][1]
    educatedRate = Math.round((educatedCount/res[2][1][1])*100)
    povertyRate = res[1][1][1]
    population = res[2][1][1]
    population_density = res[2][1][0]

    $('#education').append(`${educatedRate}%`)
    $('#population').append(population)
    $('#population_density').append(Math.round(population_density))
    $('#poverty').append(`${povertyRate}%`)
}

demographicsTable()
