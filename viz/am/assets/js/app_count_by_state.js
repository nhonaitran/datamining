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

// define quantile scale to map data values into buckets of color
var numColorClasses = 9,
    selectedColorScheme = "YlOrRd"
var colorScheme = colorbrewer[selectedColorScheme];
var color = d3.scale.quantile()
    .range(colorScheme[numColorClasses]);

var fields = [ "Code", "1990-advanced", "1990-bachelors", "1990-hs",
"1990-not-hs", "2000-advanced", "2000-bachelors", "2000-hs",
"2006-advanced", "2006-bachelors", "2006-hs", "2007-advanced",
"2007-bachelors", "2007-hs", "2008-advanced", "2008-bachelors",
"2008-hs", "2009-advanced", "2009-bachelors", "2009-hs"];
var field = "1990-hs";

function sizeChange() {
    // resize the map to fit within container
    d3.select(".map")
        .attr("transform", "translate(0,60) scale(" + $("#map-container").width()/1000 + ")");

    //$("svg").height($("#map-container").width()*0.618);
}

function drawChoropleth(us, features) {
    map.selectAll("path")
        .data(features)
        .enter().append("path")
            .attr("class", function(d,i) { return d.id;})
            .attr("d", path)
            .style("opacity", 1.0)
            .on("mouseover", function(d){
                d3.select(this).transition().duration(300).style("opacity", 0.75);
                setTooltipContent(d.data);
                tooltip
                .style( {
                    "display" : "block",
                    "top" : (d3.event.pageY - 200) + "px",
                    "left" : (d3.event.pageX - $("#map-container").width()/2) + "px"
                })
            })
            .on("mouseout", function(){
                d3.select(this).transition().duration(300).style("opacity", 1.0);
                tooltip.style("display","none");
            });

    map.append("path")
        .datum(topojson.feature(us, us.objects.land))
        .attr("class", "land")
        .attr("d", path)
        .style("opacity", 1.0);
}

function colorStates(field, scale) {
    d3.selectAll(".map path")
    .attr("fill", function(d) {
        return d.data ? color(d.data[field]) : "#333";
    });
}

function createLegend(color) {
    var legend_group = svg.append("g")
        .attr("id","legend")
        .attr("transform", "translate(" + $("#map-container").width() * 0.87 + "," + $("#map-container").height()/3 + ")");

    var legend = legend_group.selectAll("g.legend")
        .data(color.range())
        .enter().append("g")
            .attr("id", "legend");

    var l_w = 30, l_h = 30;
    legend.append("rect")
        .attr("x", 20)
        .attr("y", function(d,i){ return (i * l_h) - 2 * l_h; })
        .attr("width", l_w)
        .attr("height", l_h)
        .style("fill", function(d,i){ return d; })
        .style("opacity", 0.9);

    legend.append("text")
        .attr("x", 55)
        .attr("y", function(d, i){ return (i*l_h) - l_h - 10; })
        .text(function(d,i){
            var extent = color.invertExtent(d);
            var format = d3.format("0.1f");
            return format(+extent[0]) + "+"; // + "-" + format(+extent[1]);
        });
}

function setTooltipContent(data) {
    var html = data ?
    "<strong>" + data['State'] + " : " + data['1990-hs'] + "</strong><br>" +
    "Female : <br>" +
    "Male : " :
    "Data Not Available";
    tooltip.html( html );
}

function render(error, us, education) {
    if (error) throw error;

    var dataById = {}, features;

    education.forEach(function(d) {
        fields.forEach(function(field) {
            d[field] = parseFloat(d[field]);
        });
        dataById[d.Code] = d;
    });

    features = topojson.feature(us, us.objects.states).features;
    features.forEach(function(d) {
        d.data = dataById[d.id];
    });

    // set input domain for color scale
    color.domain(d3.extent(education, function(d, i){ return d[field]; }));

    drawChoropleth(us, features);   //bind data and create one path per GeoJSON feature
    colorStates(field, color);      //set scaled color based on education data
    createLegend(color);            //render visualization legend
}

queue()
    .defer(d3.json, "assets/json/us.json")         //load GeoJSON us states map data
    .defer(d3.csv, "assets/data/education.csv")    //load education data
    .await(render);
