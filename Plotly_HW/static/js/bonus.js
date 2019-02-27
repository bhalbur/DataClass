// Enter a speed between 0 and 180
0
var level = 175;

// Trig to calc meter point
var degrees = 180
0 - level,
     radius = .5;
var radians = degrees * Math.PI / 180
0;
var x = radius * Math.cos(radians);
var y = radius * Math.sin(radians);

// Path: may have to change to create a better triangle
var mainPath = 'M -.0 -0.025 L .0 0.025 L ',
     pathX = String(x),
     space = ' ',
     pathY = String(y),
     pathEnd = ' Z';
var path = mainPath.concat(pathX,space,pathY,pathEnd);

var data = [{ type: 'scatter',
   x: [0], y:[0],
    marker: {size: 28, color:'850000'},
    showlegend: false,
    name: 'speed',
    text: level,
    hoverinfo: 'text+name'},
  { values: [1,1,1,1,1,1,1,1,1,1,10],
  rotation: 90,
  text: ['9', '8', '7', '6', '5', '4', '3', '2', '1', '0'],
  textinfo: 'text',
  textposition:'inside',
  colorscale: 'Jet',
  marker: {
  	  colorscale: 'Jet',
	  colors: [0,10,20,30,40,50,60,70,80,90, 100],
	},
  hoverinfo: 'label',
  hole: .5,
  type: 'pie',
  showlegend: false
}];

var layout = {
  shapes:[{
      type: 'path',
      path: path,
      fillcolor: '850000',
      line: {
        color: '850000'
      }
    }],
  title: 'Gauge',
  Speed: 0-100,
  height: 500,
  width: 500,
  xaxis: {zeroline:false, showticklabels:false,
             showgrid: false, range: [-1, 1]},
  yaxis: {zeroline:false, showticklabels:false,
             showgrid: false, range: [-1, 1]}
};

Plotly.newPlot('gauge', data, layout);
