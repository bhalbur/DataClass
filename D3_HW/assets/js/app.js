//SET UP SVG Properties
var svgWidth = 1000;
var svgHeight = 600;

var margin = {
  top: 50,
  right: 10,
  bottom: 50,
  left: 10
};

var height = svgHeight - margin.top - margin.bottom;
var width = svgWidth - margin.left - margin.right;

//IMPORT DATA


povcare = []

d3.csv("assets/data/data.csv").then(function(data) {
  console.log(data[0].poverty);
  povcare = data.map(row => [parseFloat(row.poverty), parseFloat(row.healthcare), row.abbr]) 
	console.log(povcare); 


buildChart()
});


function buildChart(){

	// append svg and group
	var svg = d3.select("#chart")
	  .append("svg")
	  .attr("height", svgHeight)
	  .attr("width", svgWidth);

	var chartGroup = svg.append("g")
	  .attr("transform", `translate(${margin.left}, ${margin.top})`);

	// scales
	var xScale = d3.scaleLinear()
	  .domain([0, d3.max(povcare,function (d) {return d[0]})])
	  .range([10, width]);

	var yScale = d3.scaleLinear()
	  .domain([0, d3.max(povcare,function (d) {return d[1]})])
	  .range([height, 0]);



	// append circles to data points, add transitions
	// Hint:  You may have to alter this code for the transition on page load

	var div = d3.select("body").append("div") 
	    .attr("class", "tooltip")       
	    .style("opacity", 0);


	var circlesGroup = chartGroup.selectAll("circle")
	  .data(povcare)
	  .enter();

  	circlesGroup
	  .append("circle")
	  .attr("r", "15")
	  .attr("fill", "red")
	  .transition()
  	  .duration(800)
	  .attr("cx", d => xScale(d[0]))
	  .attr("cy", d => yScale(d[1]));

	circlesGroup
		.append('text')
		.transition()
		.duration(800)
	  .attr("x", d => xScale(d[0]) -9)
	  .attr("y", d => yScale(d[1]) +9)
	  .text(d => d[2]);


};

/*

	circlesGroup.on('mouseover', expand);
	circlesGroup.on('mouseout', contract);

	function tooltip_show(d){    
	  div.transition()    
	      .duration(200)    
	      .style("opacity", .9);    
	  div .html(` pizzas`)  
	      .style("left", (d3.event.pageX - 55) + "px")   
	      .style("top", (d3.event.pageY - 50) + "px");  
	  };

	function tooltip_hide(d) {
	  div.transition()    
	  .duration(500)    
	  .style("opacity", 0); 
	  };


	function expand(){
	  d3.select(this)
	  .transition()
	  .attr('r','15')
	  .duration(300);
	  tooltip_show(this);
	}

	function contract(){
	  d3.select(this)
	  .transition()
	  .attr('r','10')
	  .duration(300);
	  tooltip_hide(this);
	}

};*/
// YOUR CODE HERE
