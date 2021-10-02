
am4core.ready(function() {

  // Themes begin
  am4core.useTheme(am4themes_kelly);
  am4core.useTheme(am4themes_animated);
  // Themes end
  
  // Create chart
  var chart = am4core.create("chartdiv", am4charts.XYChart);
  chart.padding(0, 15, 0, 15);
  
  // Load data

  // chart.dataSource.url = "https://www.amcharts.com/wp-content/uploads/assets/stock/MSFT.csv";
  // chart.dataSource.url = "static/csv/datatenaga3.csv";
  // chart.dataSource.parser = new am4core.CSVParser();
  // chart.dataSource.url = "static/json/final.json";
  // chart.dataSource.parser = new am4core.JSONParser();
  // chart.dataSource.parser.options.emptyAs = 0;
  // chart.dataSource.parser.options.useColumnNames = true;
  // chart.dataSource.parser.options.reverse = true;

  var run_id = document.getElementById("myVar").value;
  $.getJSON('runtest/rpc/GetResultsData/' + run_id, res => {
    if(res.status == 'OK'){
      console.log(res.data);
      chart.data = res.data;
    }
    // TODO: Else return a alert
  })


  // the following line makes value axes to be arranged vertically.
  chart.leftAxesContainer.layout = "vertical";
  
  // uncomment this line if you want to change order of axes
  //chart.bottomAxesContainer.reverseOrder = true;
  
  var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
  dateAxis.renderer.grid.template.location = 0;
  dateAxis.renderer.ticks.template.length = 8;
  dateAxis.renderer.ticks.template.strokeOpacity = 0.1;
  dateAxis.renderer.grid.template.disabled = true;
  dateAxis.renderer.ticks.template.disabled = false;
  dateAxis.renderer.ticks.template.strokeOpacity = 0.2;
  dateAxis.renderer.minLabelPosition = 0.01;
  dateAxis.renderer.maxLabelPosition = 0.99;
  dateAxis.keepSelection = true;
  dateAxis.minHeight = 30;
  
  dateAxis.groupData = true;
  dateAxis.minZoomCount = 5;
  
  // these two lines makes the axis to be initially zoomed-in
  // dateAxis.start = 0.7;
  // dateAxis.keepSelection = true;
  
  var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
  valueAxis.tooltip.disabled = true;
  valueAxis.zIndex = 1;
  valueAxis.renderer.baseGrid.disabled = true;
  // height of axis
  valueAxis.height = am4core.percent(65);
  
  valueAxis.renderer.gridContainer.background.fill = am4core.color("#000000");
  valueAxis.renderer.gridContainer.background.fillOpacity = 0.05;
  valueAxis.renderer.inside = true;
  valueAxis.renderer.labels.template.verticalCenter = "bottom";
  valueAxis.renderer.labels.template.padding(2, 2, 2, 2);
  
  //valueAxis.renderer.maxLabelPosition = 0.95;
  valueAxis.renderer.fontSize = "0.8em"
  
  var series = chart.series.push(new am4charts.CandlestickSeries());
  series.dataFields.dateX = "Date";
  series.dataFields.openValueY = "Open";
  series.dataFields.valueY = "Close";
  series.dataFields.lowValueY = "Low";
  series.dataFields.highValueY = "High";
  series.clustered = false;
  series.tooltipText = "open: {openValueY.value}\nlow: {lowValueY.value}\nhigh: {highValueY.value}\nclose: {valueY.value}";
  series.name = "MSFT";
  series.defaultState.transitionDuration = 0;
  
  var valueAxis2 = chart.yAxes.push(new am4charts.ValueAxis());
  valueAxis2.tooltip.disabled = true;
  // height of axis
  valueAxis2.height = am4core.percent(35);
  valueAxis2.zIndex = 3
  // this makes gap between panels
  valueAxis2.marginTop = 30;
  valueAxis2.renderer.baseGrid.disabled = true;
  valueAxis2.renderer.inside = true;
  valueAxis2.renderer.labels.template.verticalCenter = "bottom";
  valueAxis2.renderer.labels.template.padding(2, 2, 2, 2);
  //valueAxis.renderer.maxLabelPosition = 0.95;
  valueAxis2.renderer.fontSize = "0.8em"
  
  valueAxis2.renderer.gridContainer.background.fill = am4core.color("#000000");
  valueAxis2.renderer.gridContainer.background.fillOpacity = 0.05;

  var seriesL = chart.series.push(new am4charts.LineSeries());
  seriesL.dataFields.dateX = "Date";
  seriesL.dataFields.valueY = "Close";
  seriesL.tooltipText = "close: {valueY.value}";
  seriesL.name = "MSFT: Value";
  seriesL.defaultState.transitionDuration = 0;

  // var valueAxisL = chart.yAxes.push(new am4charts.ValueAxis());
  // valueAxisL.tooltip.disabled = true;
  // // height of axis
  // valueAxisL.height = am4core.percent(65);
  // valueAxisL.zIndex = 3
  // // this makes gap between panels
  // valueAxisL.marginTop = 30;
  // valueAxisL.renderer.baseGrid.disabled = true;
  // valueAxisL.renderer.inside = true;
  // valueAxisL.renderer.labels.template.verticalCenter = "bottom";
  // valueAxisL.renderer.labels.template.padding(2, 2, 2, 2);
  // //valueAxis.renderer.maxLabelPosition = 0.95;
  // valueAxisL.renderer.fontSize = "0.8em"

  // valueAxisL.renderer.gridContainer.background.fill = am4core.color("#000000");
  // valueAxisL.renderer.gridContainer.background.fillOpacity = 0.05;
  
  // Series for SMA_S
  var seriesS = chart.series.push(new am4charts.LineSeries());
  seriesS.dataFields.dateX = "Date";
  seriesS.dataFields.valueY = "SMA_S";
  seriesS.tooltipText = "sma slow: {valueY.value}";
  seriesS.name = "MSFT: Value";
  seriesS.defaultState.transitionDuration = 0;

  // var valueAxisS = chart.yAxes.push(new am4charts.ValueAxis());
  // valueAxisS.tooltip.disabled = true;
  // // height of axis
  // valueAxisS.height = am4core.percent(65);
  // valueAxisS.zIndex = 3
  // // this makes gap between panels
  // valueAxisS.marginTop = 30;
  // valueAxisS.renderer.baseGrid.disabled = true;
  // valueAxisS.renderer.inside = true;
  // valueAxisS.renderer.labels.template.verticalCenter = "bottom";
  // valueAxisS.renderer.labels.template.padding(2, 2, 2, 2);
  // //valueAxis.renderer.maxLabelPosition = 0.95;
  // valueAxisS.renderer.fontSize = "0.8em"

  // valueAxisS.renderer.gridContainer.background.fill = am4core.color("#000000");
  // valueAxisS.renderer.gridContainer.background.fillOpacity = 0.05;

  
  // Series for SMA_F
  var seriesF = chart.series.push(new am4charts.LineSeries());
  seriesF.dataFields.dateX = "Date";
  seriesF.dataFields.valueY = "SMA_F";
  seriesF.tooltipText = "sma fast: {valueY.value}";
  seriesF.name = "MSFT: Value";
  seriesF.defaultState.transitionDuration = 0;

  // var valueAxisF = chart.yAxes.push(new am4charts.ValueAxis());
  // valueAxisF.tooltip.disabled = true;
  // // height of axis
  // valueAxisF.height = am4core.percent(65);
  // valueAxisF.zIndex = 3
  // // this makes gap between panels
  // valueAxisF.marginTop = 30;
  // valueAxisF.renderer.baseGrid.disabled = true;
  // valueAxisF.renderer.inside = true;
  // valueAxisF.renderer.labels.template.verticalCenter = "bottom";
  // valueAxisF.renderer.labels.template.padding(2, 2, 2, 2);
  // //valueAxis.renderer.maxLabelPosition = 0.95;
  // valueAxisF.renderer.fontSize = "0.8em"

  // valueAxisF.renderer.gridContainer.background.fill = am4core.color("#000000");
  // valueAxisF.renderer.gridContainer.background.fillOpacity = 0.05;

  // Second chart
  var series2 = chart.series.push(new am4charts.ColumnSeries());
  series2.dataFields.dateX = "Date";
  series2.clustered = false;
  series2.dataFields.valueY = "Volume";
  series2.yAxis = valueAxis2;
  series2.tooltipText = "{valueY.value}";
  series2.name = "Series 2";
  // volume should be summed
  series2.groupFields.valueY = "sum";
  series2.defaultState.transitionDuration = 0;

  chart.cursor = new am4charts.XYCursor();
  
  var scrollbarX = new am4charts.XYChartScrollbar();
  
  var sbSeries = chart.series.push(new am4charts.LineSeries());
  sbSeries.dataFields.valueY = "Close";
  sbSeries.dataFields.dateX = "Date";
  scrollbarX.series.push(sbSeries);
  sbSeries.disabled = true;
  scrollbarX.marginBottom = 20;
  chart.scrollbarX = scrollbarX;
  scrollbarX.scrollbarChart.xAxes.getIndex(0).minHeight = undefined;

  chart.svgContainer.htmlElement.style.height = "700px";
  
  // Date format to be used in input fields
  var inputFieldFormat = "yyyy-MM-dd";
  
  document.getElementById("b1m").addEventListener("click", function() {
    var max = dateAxis.groupMax["day1"];
    var date = new Date(max);
    am4core.time.add(date, "month", -1);
    zoomToDates(date);
  });
  
  document.getElementById("b3m").addEventListener("click", function() {
    var max = dateAxis.groupMax["day1"];
    var date = new Date(max);
    am4core.time.add(date, "month", -3);
    zoomToDates(date);
  });
  
  document.getElementById("b6m").addEventListener("click", function() {
    var max = dateAxis.groupMax["day1"];
    var date = new Date(max);
    am4core.time.add(date, "month", -6);
    zoomToDates(date);
  });
  
  document.getElementById("b1y").addEventListener("click", function() {
    var max = dateAxis.groupMax["day1"];
    var date = new Date(max);
    am4core.time.add(date, "year", -1);
    zoomToDates(date);
  });
  
  document.getElementById("bytd").addEventListener("click", function() {
    var max = dateAxis.groupMax["day1"];
    var date = new Date(max);
    am4core.time.round(date, "year", 1);
    zoomToDates(date);
  });
  
  document.getElementById("bmax").addEventListener("click", function() {
    var min = dateAxis.groupMin["day1"];
    var date = new Date(min);
    zoomToDates(date);
  });
  
  dateAxis.events.on("selectionextremeschanged", function() {
    updateFields();
  });
  
  dateAxis.events.on("extremeschanged", updateFields);
  
  function updateFields() {
    var minZoomed = dateAxis.minZoomed + am4core.time.getDuration(dateAxis.mainBaseInterval.timeUnit, dateAxis.mainBaseInterval.count) * 0.5;
    document.getElementById("fromfield").value = chart.dateFormatter.format(minZoomed, inputFieldFormat);
    document.getElementById("tofield").value = chart.dateFormatter.format(new Date(dateAxis.maxZoomed), inputFieldFormat);
  }
  
  document.getElementById("fromfield").addEventListener("keyup", updateZoom);
  document.getElementById("tofield").addEventListener("keyup", updateZoom);
  
  var zoomTimeout;
  function updateZoom() {
    if (zoomTimeout) {
      clearTimeout(zoomTimeout);
    }
    zoomTimeout = setTimeout(function() {
      var start = document.getElementById("fromfield").value;
      var end = document.getElementById("tofield").value;
      if ((start.length < inputFieldFormat.length) || (end.length < inputFieldFormat.length)) {
        return;
      }
      var startDate = chart.dateFormatter.parse(start, inputFieldFormat);
      var endDate = chart.dateFormatter.parse(end, inputFieldFormat);
  
      if (startDate && endDate) {
        dateAxis.zoomToDates(startDate, endDate);
      }
    }, 500);
  }
  
  function zoomToDates(date) {
    var min = dateAxis.groupMin["day1"];
    var max = dateAxis.groupMax["day1"];
    dateAxis.keepSelection = true;
    //dateAxis.start = (date.getTime() - min)/(max - min);
    //dateAxis.end = 1;
  
    dateAxis.zoom({start:(date.getTime() - min)/(max - min), end:1});
  }

}); // end am4core.ready()