


let availableYears = []
let chosen_year;

let fullTime = false
let selected_race;
let selected_series;
let selected_year;

let highToLow = false

let the_race_data 
let the_driver_data 


document.getElementById("full-time").checked = false;


function set_fullTime(){
    const fullTimeCheck = document.getElementById('full-time')

    if (fullTimeCheck.checked == true){
        fullTime = true;
      } else {
        fullTime = false
      }

    get_rankings(selected_series, selected_year, selected_race)


}


function updateYears(availableYears, series) {

    const years_container = document.getElementById('year')
    years_container.innerHTML = "";

    availableYears.forEach(year => {
        const years_option = document.createElement('a')
        const year_holder = document.createElement('h2')
        years_option.innerText = year
        years_option.onclick = () => {
            // chosen_year = year; // Update chosen_year
            update_url(series, year);
        };
        // years_option.setAttribute('onclick', update_url(series, year))
        year_holder.append(years_option)
        years_container.append(year_holder)

    });




}






function setSeries(the_series) {

    if (the_series == "NascarCup") {
        availableYears = ['2025', '2024', '2023', '2022', '2021', '2020', '2019', '2018', '2017']
        chosen_year = availableYears[0]
    }
    if (the_series == "NascarXfinity") {
        availableYears = ['2025', '2024', '2023', '2022', '2021', '2020', '2019', '2018', '2017']
        chosen_year = availableYears[0]
    }


    update_url(the_series, chosen_year)
    updateYears(availableYears, the_series)


}




function parse_url() {

    const params = new URLSearchParams(window.location.search);
    const series = params.get("series") || "";
    const year = params.get("year") || "";
    setSeries(series)



    return { series, year };


}



function update_url(series, year) {
    const params = new URLSearchParams(window.location.search);
    params.set("series", series);
    params.set("year", year);


    // Update the URL without reloading the page
    window.history.pushState({}, "", `${window.location.pathname}?${params.toString()}`);

    console.log("Updated URL:", window.location.href);
    get_races(series, year)

}






let { series, year } = parse_url()
setSeries(series);

let races_data
let race_names = []

function get_races(series, year) {
    console.log(series, year)

    console.log(`/data/${series}/${year}/races.json`)

    fetch(`/data/${series}/${year}/races.json`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json()
        })
        .then(data => {
            races_data = data
            race_names = Object.keys(data)
            race_names.splice(0, 0, 'All')
            const race_container = document.getElementById('races')
            race_container.innerHTML = "";
            console.log(race_names)

            race_names.forEach(race => {

                const race_option = document.createElement('a')
                const race_holder = document.createElement('h2')
                race_option.innerText = race
                race_option.onclick = () => {
                    // chosen_year = year; // Update chosen_year
                    get_rankings(series, year, race);
                };
                // years_option.setAttribute('onclick', update_url(series, year))
                race_holder.append(race_option)
                race_container.append(race_holder)



            });

            get_rankings(series, year, race_names[0])
            selected_series = series
            selected_year = year





            
            
            
            
            
            
            
        })
        .catch(error => {
            console.error('Error:', error);
        });


        } 










let ordered_drivers;
function get_rankings(series, year, chosen_race) {
    document.getElementById('race-title').innerText = chosen_race

    selected_race = chosen_race

    if (chosen_race === "All") {
        fetch_driver_data(series, year)

    } else {
        fetch_race_data(series, year, chosen_race)


    }


    async function fetch_race_data(series, year, race) {
        const response = await fetch(`data/${series}/${year}/races.json`);
        if (!response.ok) {
            return Promise.reject('Network response was not ok');
        }
        let race_data = await response.json();
        race_data = race_data[race];
    
        const response_drivers = await fetch(`data/${series}/${year}/drivers.json`);
        if (!response_drivers.ok) {
            return Promise.reject('Network response was not ok');
        }
        const driver_data = await response_drivers.json();
    
        // Sort drivers by Elo rating
        let ordered_drivers_array = Object.values(race_data).sort((a, b) => b.elo_after - a.elo_after);
    
        // Apply full-time filter if needed
        if (fullTime) {
            ordered_drivers_array = ordered_drivers_array.filter(driver => {
                const driver_id_str = String(driver.driver_id);
                return driver_data[driver_id_str]?.full_time === true;
            });
        }
    
        // Add placement property to each driver
        ordered_drivers_array = ordered_drivers_array.map((driver, index) => ({
            ...driver,
            placement: index + 1
        }));
    
        console.log(ordered_drivers_array);
        generate_table(ordered_drivers_array, ordered_drivers_array);
    }


    async function fetch_driver_data(series, year){
        const response = await fetch(`data/${series}/${year}/drivers.json`);
        if (!response.ok) {
            return Promise.reject('Network response was not ok');
        }
        const driver_data = await response.json();

        if (fullTime == false){



            const ordered_drivers_array = Object.values(driver_data).sort((a, b) => b.elo - a.elo);

            // Create a new object where the keys are rankings
            const ordered_drivers = ordered_drivers_array.reduce((acc, player, index) => {
                acc[index + 1] = player; // index + 1 to start rankings from 1
                return acc;
            }, {});
            
            console.log(ordered_drivers_array)

            let elo_rankings = []
            generate_table(ordered_drivers_array, 'All')





        } else if (fullTime == true){


            const full_time_drivers = Object.values(driver_data).filter(player => player.full_time)
            const sorted_full_time = Object.values(full_time_drivers).sort((a, b) => b.elo - a.elo);

            console.log(sorted_full_time)
            generate_table(sorted_full_time, 'All')






        }











    }










}




function generate_table(driver_data, race_data){
// Race data is "All" if its just all driver standings
    console.log('the data when it gets here', race_data)

    the_race_data = race_data
    the_driver_data = driver_data


    if (race_data == "All"){

        const table = document.getElementById('data-table')

        const tableHead = document.getElementById("table-head");
        const tableBody = document.getElementById("table-body");

        tableHead.innerText = ""

        const headers = [ 'Pos', 'Name', 'Elo', 'Races', 'Playoff Points', 'NASCAR Position' ]
        const header_stat = ["name", "elo", "race_num", "playoff_points", "position"]

        // Do Playoff points and position separate



        
        headers.forEach(header => {
            const th = document.createElement("th");
            th.textContent = header;
            
            th.onclick = () => {
                if (th.textContent != "Pos" || th.textContent != "Name"){

                // chosen_year = year; // Update chosen_year
                highToLow = !highToLow   
                sortTable(highToLow, header, race_data, driver_data);
                }
            };
            tableHead.appendChild(th);
        });

        let new_stat;
        tableBody.innerText = ""
        driver_data.forEach((driver, index) => {
            const tr = document.createElement("tr");

            const positionTd = document.createElement("td");
            positionTd.textContent = index + 1; // Position starts from 1, not 0
            tr.appendChild(positionTd);

            header_stat.forEach(stat => {
                if (stat == "playoff_points"){
                    new_stat = `${driver['playoff_points']} (${driver['playoff_rank']})`


                } else{
                    new_stat = driver[stat]
                }
                const td = document.createElement("td");
                td.textContent = new_stat || ''; // Handle undefined properties
                tr.appendChild(td);
            });


            tableBody.appendChild(tr);


        });


    
    
    } else{

        const table = document.getElementById('data-table')

        const tableHead = document.getElementById("table-head");
        const tableBody = document.getElementById("table-body");

        tableHead.innerText = ""

        const headers = [ 'Pos', 'Name', 'Elo', '+/-', 'Race Position' ]
        const header_stat = ["name", "elo_after", "delta_elo", "placement"]

        // Do Playoff points and position separate

        
        headers.forEach(header => {
            const th = document.createElement("th");
            th.textContent = header;

            if (th.textContent != "Pos" || th.textContent != "Name"){

                th.onclick = () => {
                    // chosen_year = year; // Update chosen_year
                    highToLow = !highToLow   
                    sortTable(highToLow, header, race_data, driver_data);
                };
                tableHead.appendChild(th);
            }
        });

        console.log(Object.keys(race_data))
        tableBody.innerText = ""
        Object.keys(race_data).forEach((finisher, index) => {


                const tr = document.createElement("tr");
    
                const positionTd = document.createElement("td");
                positionTd.textContent = index + 1; // Position starts from 1, not 0
                tr.appendChild(positionTd);
    
                header_stat.forEach(stat => {

                    
                    const td = document.createElement("td");
                    if(stat == 'delta_elo'){
                        if(race_data[finisher]['delta_elo'] >= 0){
                            td.classList.add('green')
                            if(race_data[finisher]['delta_elo'][0] != '+'){

                                race_data[finisher]['delta_elo'] =`+${race_data[finisher]['delta_elo']}` 
                            }

                        } else if(race_data[finisher]['delta_elo'] <= 0){

                            td.classList.add('red')


                        }

                    }
                    td.textContent = race_data[finisher][stat] || ''; // Handle undefined properties
                    tr.appendChild(td);
                });
    
    
                tableBody.appendChild(tr);


           


        });



    }


}



function sortTable(highToLow, column, race_data, driver_data){
    console.log(highToLow, column, race_data, driver_data)


    if(highToLow == true){

        if(race_data == "All"){

            if(column == "Elo"){
                new_column = "elo"
            } 
   
            if (column == "Races"){
                new_column ="race_num"
            } 
            if (column == "Playoff Points"){
                new_column ="playoff_points"
            } 
            if(column == 'NASCAR Position'){
                new_column = 'position'
            }
            
            let sorted_drivers = driver_data.sort((a, b) => a[new_column] - b[new_column]);
            console.log('sorted drivers', sorted_drivers)
            generate_table(sorted_drivers, "All")




        } else{

            if(column == "Elo"){
                new_column = "elo_after"
            } 
   
            if (column == "+/-"){
                new_column ="delta_elo"
            } 
            if (column == "Playoff Points"){
                new_column ="playoff_points"
            } 
            if(column == 'Race Position'){
                new_column = 'placement'
            }
            
            let sorted_drivers = race_data.sort((a, b) => a[new_column] - b[new_column]);
            console.log('sorted drivers', sorted_drivers)
            generate_table(sorted_drivers, race_data)








        }




    } else if(highToLow == false){

        if(race_data == "All"){

            if(column == "Elo"){
                new_column = "elo"
            } 
            if (column == "Name"){
                new_column ="name"
            } 
            if (column == "Races"){
                new_column ="race_num"
            } 
            if (column == "Playoff Points"){
                new_column ="playoff_points"
            } 
            if(column == 'NASCAR Position'){
                new_column = 'position'
            }
            
            let sorted_drivers = driver_data.sort((a, b) => a[new_column] - b[new_column]);
            sorted_drivers = sorted_drivers.reverse()
            console.log('sorted drivers', sorted_drivers)
            generate_table(sorted_drivers, "All")




        } else{

            if(column == "Elo"){
                new_column = "elo_after"
            } 
   
            if (column == "+/-"){
                new_column ="delta_elo"
            } 
            if (column == "Playoff Points"){
                new_column ="playoff_points"
            } 
            if(column == 'Race Position'){
                new_column = 'placement'
            }
            
            let sorted_drivers = race_data.sort((a, b) => a[new_column] - b[new_column]);
            sorted_drivers = sorted_drivers.reverse()

            console.log('sorted drivers', sorted_drivers)
            generate_table(sorted_drivers, race_data)










        }





    }





}