/*
*    main.js
*/


d3.json("data/buildings.json").then((data) => {
    
doubleBarChart("#chart1", data);
doubleBarChart("#chart2", data);

}).catch((error) => {
    console.log(error);
});

/* 
TOTAL PRODUCTION VS CONSUMPTION
--> Gráfica de Barras dobles
*/
function doubleBarChart(container, data) {

    const containerWidth = document.querySelector(container).clientWidth;

	const width = containerWidth;
	const height = 400;

	const margin = {
		left: 80,
		right: 10,
		top: 10,
		bottom: 100
	};

	const innerWidth = width - margin.left - margin.right;
	const innerHeight = height - margin.top - margin.bottom;

    d3.select(container).html("");

	const svg = d3.select(container)
		.append("svg")
		.attr("width", width)
		.attr("height", height);

	const g = svg.append("g")
		.attr("transform", `translate(${margin.left}, ${margin.top})`);

	// Formato de datos
	data.forEach(d => {
		d.height = +d.height;
		d.weight = +d.weight;
	});

	// 🔹 Subgrupos (las dos barras)
	const subgroups = ["height", "weight"];

	// 🔹 Escala X principal
	const x = d3.scaleBand()
		.domain(data.map(d => d.name))
		.range([0, innerWidth])
		.padding(0.2);

	// 🔹 Escala X interna (para separar barras)
	const xSub = d3.scaleBand()
		.domain(subgroups)
		.range([0, x.bandwidth()])
		.padding(0.1);

	// 🔹 Escala Y
	const y = d3.scaleLinear()
		.domain([0, d3.max(data, d => Math.max(d.height, d.weight))])
		.range([innerHeight, 0]);

	// 🔹 Colores
	const color = d3.scaleOrdinal()
		.domain(subgroups)
		.range(["#5B8FF9", "#bbd3fc"]);

	// 🔹 Barras
	g.append("g")
		.selectAll("g")
		.data(data)
		.enter()
		.append("g")
		.attr("transform", d => `translate(${x(d.name)},0)`)
		.selectAll("rect")
		.data(d => subgroups.map(key => ({
			key: key,
			value: d[key]
		})))
		.enter()
		.append("rect")
		.attr("x", d => xSub(d.key))
		.attr("y", d => y(d.value))
		.attr("width", xSub.bandwidth())
		.attr("height", d => innerHeight - y(d.value))
		.attr("fill", d => color(d.key));

	// 🔹 Axis X
	g.append("g")
		.attr("transform", `translate(0, ${innerHeight})`)
		.call(d3.axisBottom(x))
		.selectAll("text")
		.attr("transform", "rotate(-40)")
		.style("text-anchor", "end");

	// 🔹 Axis Y
	g.append("g")
		.call(d3.axisLeft(y));

	// 🔹 Labels
	g.append("text")
		.attr("x", innerWidth / 2)
		.attr("y", innerHeight + 80)
		.attr("text-anchor", "middle")
		.text("Buildings");

	g.append("text")
		.attr("transform", "rotate(-90)")
		.attr("x", -innerHeight / 2)
		.attr("y", -60)
		.attr("text-anchor", "middle")
		.text("Height (m)");

	
}

