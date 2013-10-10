$(function() {
	var seriesOptions = [],
		yAxisOptions = [],
		seriesCounter = 0,
		names = location.hash.slice(1).split(','),
		colors = Highcharts.getOptions().colors;

	function fetch() {
        $.each(names, function(i, name) {

		    $.get('/get/' + name, function(data) {

			    seriesOptions[i] = {
				    name: name,
				    data: data
			    };

			    seriesCounter++;

			    if (seriesCounter == names.length) {
				    createChart();
			    }
		    });
	    });
    }

    $(fetch)

	// create the chart when all data is loaded
	function createChart() {

		$('#container').highcharts('StockChart', {
		    chart: {
		    },

		    rangeSelector: {
		        selected: 4
		    },

		    yAxis: {
		    	labels: {
		    		formatter: function() {
		    			return (this.value*8/1024/1024).toFixed(1) + ' Mbps';
		    		}
		    	},
		    	plotLines: [{
		    		value: 0,
		    		width: 2,
		    		color: 'silver'
		    	}]
		    },

		    plotOptions: {
		    	series: {
		    		//compare: 'percent'
		    	}
		    },

		    tooltip: {
		    	pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',
		    	valueDecimals: 2
		    },

		    series: seriesOptions
		});
	}

});
