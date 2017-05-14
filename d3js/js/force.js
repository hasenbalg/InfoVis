//https://www.lynda.com/D3js-tutorials/Data-Visualization-D3js/162449-2.html

var   w = 1000,
      h = 600;

var circleWidth = 5;


///////////////////////////////////////////////////////////



var nodes = [];
//add each word once
for (var i = 0; i < links.length; i++) {
  if (nodes.findIndex(x => x.name==links[i].w1) === -1){
    nodes.push({ name : links[i].w1, target: [], idf: 0});
  }
}

for (var i = 0; i < nodes.length; i++) {
  for (var j = 0; j < nodes.length; j++) {
    if(nodes[i].name == links[j].w2){
        nodes[i].target.push(j);
    }
  }
}

for (var i = 0; i < nodes.length; i++) {
  var index = frequencies.findIndex(x => x.word==nodes[i].name);
  nodes[i].idf = frequencies[index].idf;
}

console.log(JSON.stringify(nodes));


/////////////////////////////////////////////////////////
// var nodes = [
//       { name: "Parent"},
//       { name: "child1"},
//       { name: "child2", target: [0]},
//       { name: "child3", target: [0]},
//       { name: "child4", target: [1]},
//       { name: "child5", target: [0, 1, 2, 3]}
// ];

var links = [];

for (var i = 0; i< nodes.length; i++) {
      if (nodes[i].target !== undefined) {
            for (var x = 0; x< nodes[i].target.length; x++ ) {
                  links.push({
                        source: nodes[i],
                        target: nodes[nodes[i].target[x]],
                        proximity: 20
                  })
            }
      }
}

var myChart = d3.select('#force')
		.append('svg')
		.attr('width', w)
		.attr('height', h)

var force = d3.layout.force()
	.nodes(nodes)
	.links([])
	.gravity(0.3)
	.charge(-1000)
	.size([w, h])
  // .linkStrength(1000)
  // .linkDistance(function(d) { return  d.proximity; })
  //.linkDistance(-10)
  //.chargeDistance(function(d) { return  d.idf * -1000; })


var link = myChart.selectAll('line')
	.data(links).enter().append('line')
	.attr('stroke', palette.gray)

var node = myChart.selectAll('circle')
	.data(nodes).enter()
	.append('g')
	.call(force.drag);

node.append('circle')
	.attr('cx', function(d) { return d.x; })
	.attr('cy', function(d) { return d.y; })
	.attr('r', function(d, i) {
		return d.idf * 10;
	} )
	.attr('fill', function(d, i) {
    return palette.blue
	})

node.append('text')
	.text(function(d) { return d.name})
	//.attr('font-family', 'Roboto Slab')
  .classed('text', true)
	// .attr('fill', function(d, i) {
	// 	return palette.yellowgreen
	// })
	.attr('x', function(d, i) {
		return d.idf;
	})
	.attr('y', function(d, i) {
		return d.idf;
	})
	.attr('text-anchor', function(d, i) {
		return 'end'
	})
	.attr('font-size',  function(d, i) {
		// return '1.8em'
    return d.idf * 1.5 + 'em'
	})

force.on('tick', function(e) {
	node.attr('transform', function(d, i) {
		return 'translate('+ d.x +', '+ d.y +')';
	})

	link
		.attr('x1', function(d) { return d.source.x })
		.attr('y1', function(d) { return d.source.y })
		.attr('x2', function(d) { return d.target.x })
		.attr('y2', function(d) { return d.target.y })
})


force.start();
