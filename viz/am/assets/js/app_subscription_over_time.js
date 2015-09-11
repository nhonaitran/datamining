// define map projection
var projection = d3.geo.albersUsa().scale(1100);

// define path generator
var path = d3.geo.path().projection(projection);

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

function sizeChange() {
    // resize the map to fit within container
    d3.select(".map")
        .attr("transform", "translate(0,60) scale(" + $("#map-container").width()/1000 + ")");

    //$("svg").height($("#map-container").width()*0.618);
}

function circleSize(d){
    return Math.sqrt( 0.0005 * Math.abs(d) );
};

function createLegend(){
    var legend = svg.append("g")
        .attr("id","legend")
        .attr("transform","translate(" + $("#map-container").width() * 0.55 + ",10)");

    legend.append("circle").attr("class","loss").attr("r",5).attr("cx",1).attr("cy",30)
    legend.append("text").text("# of subscribers").attr("x",10).attr("y",33);

    var sizes = [ 100000, 1000000, 10000000 ];
    for ( var i in sizes ){
        legend.append("circle")
            .attr( "r", circleSize( sizes[i] ) )
            .attr( "cx", 80 + circleSize( sizes[sizes.length-1] ) )
            .attr( "cy", 2 * circleSize( sizes[sizes.length-1] ) - circleSize( sizes[i] ) )
            .attr("vector-effect","non-scaling-stroke");
        legend.append("text")
            .text( (sizes[i] / 1000000) + "M" + (i == sizes.length-1 ? " members" : "") )
            .attr( "text-anchor", "middle" )
            .attr( "x", 80 + circleSize( sizes[sizes.length-1] ) )
            .attr( "y", 2 * ( circleSize( sizes[sizes.length-1] ) - circleSize( sizes[i] ) ) + 5 )
            .attr( "dy", 13)
    }
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
            .attr("r", function(d){ return Math.sqrt(parseInt(d.population)*0.0005); })
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
