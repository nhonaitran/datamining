// define map projection
var projection = d3.geo.albersUsa().scale(1100);

// define path generator
var path = d3.geo.path().projection(projection);

// define the scale for the size of the bubble
var radius = d3.scale.sqrt().domain([0, 1e6]).range([0, 15]);

// create SVG element
var svg = d3.select("#map-container").append("svg")
    .attr("width", "100%")
    .attr("height", "600");

// create tooltip element to display detailed information about the state when mouse hovers a state
var tooltip = d3.select("#map-container").append("div")
    .attr("id", "tooltip")
    .style("display","none");

var map = svg.append("g")
    .attr("id", "map")
    .attr("class", "map");

var width = $("#map-container").width();
var height = $("#map-container").height();

function sizeChange() {
    // resize the map to fit within container
    d3.select(".map")
        .attr("transform", "translate(0,60) scale(" + width/900 + ")");

    //$("svg").height($("#map-container").width()*0.618);
}

function createLegend(){
    var legend = svg.append("g")
        .attr("class", "legend")
        .attr("transform", "translate(" + (width - 75) + "," + (height - 60) + ")")
        .selectAll("g")
        .data([1e6, 5e6, 1e7])
        .enter().append("g");

    legend.append("circle")
        .attr("cy", function(d) { return -radius(d); })
        .attr("r", radius);

    legend.append("text")
        .attr("y", function(d) { return -2 * radius(d); })
        .attr("dy", "1.3em")
        .text(d3.format(".1s"));
}

function setTooltipContent(d){
    var format = d3.format("0,000");
    var html = "<center><strong>" + d.place + "</strong><br/>" +
    "<span>" + format(d.population) + " members</span></center>";
    tooltip.html( html );
}

function drawCitiesInfo(data) {
    //draw city points
    map.selectAll("circle")
        .data(data)
        .enter().append("circle")
            .attr("cx", function(d){ return projection([d.lon, d.lat])[0]; })
            .attr("cy", function(d){ return projection([d.lon, d.lat])[1]; })
            .attr("r", function(d){ return radius(d.population); })
            .attr("vector-effect","non-scaling-stroke")
            .attr("class", "loss")
            .on("mousemove", function(d){
                hoverData = d;
                setTooltipContent(d);
                tooltip
                .style( {
                    "display" : "block",
                    "top" : (d3.event.pageY - 200) + "px",
                    "left" : (d3.event.pageX - $("#map-container").width()/2) + "px"
                })
            })
            .on("mouseout", function(){
                hoverData = null;
                tooltip.style("display","none");
            });
}

function drawChoropleth(us) {
    map.selectAll("path")
    .data(topojson.feature(us, us.objects.states).features)
    .enter()
    .append("path")
        .attr("vector-effect","non-scaling-stroke")
        .attr("class","land-fill")
        .attr("d", path);

    map.append("path")
    .datum(topojson.mesh(us, us.objects.states, function(a, b) { return a !== b; }))
        .attr("class", "state-boundary")
        .attr("vector-effect","non-scaling-stroke")
        .attr("d", path);
}

function render(error, us, data) {
    if (error) throw error;
    drawChoropleth(us);
    drawCitiesInfo(data);
    createLegend();
}

queue()
    .defer(d3.json, "assets/json/us.json")         //load GeoJSON us states map data
    .defer(d3.csv, "assets/data/us-cities.csv")    //load info about top 50 cities data
    .await(render);
