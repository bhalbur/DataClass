var data = data;

console.log(Object.values(data[0]))

headers = Object.keys(data[0])
console.log(headers);



// YOUR CODE HERE!
tbody = d3.select('tbody');
textbox = d3.select('#datetime');
button = d3.select('#filter-btn');

searchdate = "1/2/2010"

function datematch(sighting){
	return sighting.datetime == searchdate
}


function filterTable(){
tbody.text('')
tbody.append('tr').append('td').text("Loading...")
filterdata = data.filter(datematch)
console.log(filterdata)
	setTimeout(function(){
		tbody.text('') 
		if(filterdata.length == 0){
			tbody.text('No Results Found for the given search parameters. Please ensure you enter date in M/DD/YYYY format');	
		} else{ 
		filterdata.forEach(sighting => {
			//console.log(sighting);
			var newrow = tbody.append('tr');
			Object.entries(sighting).forEach(([x,y]) => {
			newrow.append('td').text(y);

			})
		})
	}}, 500);
}

filterTable()

function inputDate(){
	searchdate = textbox.property('value');
	filterTable()
}

textbox.on('change', inputDate);
button.on('click', inputDate);