// width and height of map
//var width = 960, height = 550;

// define map projection
var projection = d3.geo.albersUsa().scale(1100);

// define path generator
var path = d3.geo.path().projection(projection);

// create SVG element
var svg = d3.select("#map-container").append("svg")
    .attr("width", "100%")
    .attr("height", "100%");

// create tooltip element to display detailed information about the state when mouse hovers a state
var tooltip = d3.select("#map-container").append("div")
    .attr("id", "tooltip")
    .style("display","none");

//var g = svg.append("g");

var map = svg.append("g")
    .attr("class", "map");
