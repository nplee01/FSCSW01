
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

  // var rsiValue = undefined;

  var run_id = document.getElementById("myVar").value;
  $.getJSON("../../runtest/rpc/GetResultsData/" + run_id, res_data => {
    if(res_data.status == "OK"){
      $.getJSON("../../runtest/rpc/GetResultsSummary/" + run_id, res_summ => {
        if(res_summ.status == "OK"){
          // console.log(res.data[Object.keys(res.data)[0]].RSI);
          // rsiValue = res.data[Object.keys(res.data)[0]].RSI;
          // rsiGraph(res_data.data[Object.keys(res_data.data)[0]].RSI, res_summ.data[Object.keys("RSIOB")], res_summ.data[Object.keys("RSIOS")]);
          rsiGraph(res_data.data, res_summ.data);
          // console.log(res.data)
          // console.log(res.data);
          chart.data = res_data.data;
        } else {
          alert("Sorry, please try again later. Summary failed to be retrieved.");
        }
      })
    }else{
      alert("Sorry, please try again later. Data failed to be retrieved.");
    }
  })


  // the following line makes value axes to be arranged vertically.
  chart.leftAxesContainer.layout = "vertical";
  
  // uncomment this line if you want to change order of axes
  // chart.bottomAxesContainer.reverseOrder = true;
  
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
  series.tooltipText = "Date: {dateX.formatDate('yyyy-MM-dd')}\nOpen: {openValueY.value}\nClose: {valueY.value}\nHigh: {highValueY.value}\nLow: {lowValueY.value}";
  series.name = "MSFT";
  series.defaultState.transitionDuration = 0;
  
  // series.fill = am4core.color("rgb(15, 148, 0)");
  // series.stroke = am4core.color("rgb(15, 148, 0)");
  // series.tooltip.getFillFromObject = false;
  // series.tooltip.background.fill = am4core.color("rgb(15, 148, 0)");

  // Close series
  // var seriesL = chart.series.push(new am4charts.LineSeries());
  // seriesL.dataFields.dateX = "Date";
  // seriesL.dataFields.valueY = "Close";
  // seriesL.stroke = am4core.color("black");
  // seriesL.tooltip.getFillFromObject = false;
  // seriesL.tooltip.background.fill = am4core.color("black");
  // seriesL.tooltipText = "Close: {valueY.value}";
  // seriesL.name = "MSFT: Value";
  // seriesL.defaultState.transitionDuration = 0;

  // Buy and Sell TODO TODO TODO TODO
  // Create series
  var enterLongSeries = chart.series.push(new am4charts.LineSeries());
  enterLongSeries.dataFields.dateX = "Date";
  enterLongSeries.dataFields.valueY = "enterLong";
  enterLongSeries.tooltipText = "Enter long: {valueY.value}";
  enterLongSeries.clustered = false;
  enterLongSeries.strokeOpacity = 0;
  
  var exitLongSeries = chart.series.push(new am4charts.LineSeries());
  exitLongSeries.dataFields.dateX = "Date";
  exitLongSeries.dataFields.valueY = "exitLong";
  exitLongSeries.tooltipText = "Exit long: {valueY.value}";
  enterLongSeries.clustered = false;
  exitLongSeries.strokeOpacity = 0;
  
  // Add a bullet
  var bullet = enterLongSeries.bullets.push(new am4charts.Bullet());

  // Add a triangle to act as am arrow : ENTER LONG
  var arrow = bullet.createChild(am4core.Triangle);
  arrow.horizontalCenter = "middle";
  arrow.verticalCenter = "middle";
  arrow.strokeWidth = 0;
  arrow.fill = am4core.color("green");
  arrow.direction = "top";
  arrow.width = 12;
  arrow.height = 12;

  // Add a bullet
  var bullet2 = exitLongSeries.bullets.push(new am4charts.Bullet());

  // Add a triangle to act as am arrow : EXIT LONG
  var arrow2 = bullet2.createChild(am4core.Triangle);
  arrow2.horizontalCenter = "middle";
  arrow2.verticalCenter = "middle";
  arrow2.rotation = 180;
  arrow2.strokeWidth = 0;
  arrow2.fill = am4core.color("red");
  arrow2.direction = "top";
  arrow2.width = 12;
  arrow2.height = 12;


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
  
  // Series for SMA
  var seriesBase = chart.series.push(new am4charts.LineSeries());
  seriesBase.dataFields.dateX = "Date";
  seriesBase.dataFields.valueY = "SMA";
  seriesBase.tooltipText = "Baseline SMA: {valueY.value}";
  seriesBase.name = "MSFT: Value";
  seriesBase.defaultState.transitionDuration = 0;
  seriesBase.stroke = am4core.color("rgb(65, 112, 216)");
  seriesBase.tooltip.getFillFromObject = false;
  seriesBase.tooltip.background.fill = am4core.color("rgb(65, 112, 216)");

  // Series for SMA_S
  var seriesS = chart.series.push(new am4charts.LineSeries());
  seriesS.dataFields.dateX = "Date";
  seriesS.dataFields.valueY = "SMA_S";
  seriesS.tooltipText = "SMA slow: {valueY.value}";
  seriesS.name = "MSFT: Value";
  seriesS.defaultState.transitionDuration = 0;
  seriesS.stroke = am4core.color("red");
  seriesS.tooltip.getFillFromObject = false;
  seriesS.tooltip.background.fill = am4core.color("red");

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
  seriesF.tooltipText = "SMA fast: {valueY.value}";
  seriesF.name = "MSFT: Value";
  seriesF.defaultState.transitionDuration = 0;
  seriesF.stroke = am4core.color("green");
  seriesF.tooltip.getFillFromObject = false;  
  seriesF.tooltip.background.fill = am4core.color("green");

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

  // Second chart: RSI
  // TODO: Only generate if there is RSI in the data
  // console.log(chart.data);
  // setTimeout(() => {
  //   if (rsiValue !== undefined) {
  //     var valueAxis2 = chart.yAxes.push(new am4charts.ValueAxis());
  //     valueAxis2.tooltip.disabled = true;
  //     // height of axis
  //     valueAxis2.height = am4core.percent(35);
  //     valueAxis2.zIndex = 3
  //     // this makes gap between panels
  //     valueAxis2.marginTop = 30;
  //     valueAxis2.renderer.baseGrid.disabled = true;
  //     valueAxis2.renderer.inside = true;
  //     valueAxis2.renderer.labels.template.verticalCenter = "bottom";
  //     valueAxis2.renderer.labels.template.padding(2, 2, 2, 2);
  //     //valueAxis.renderer.maxLabelPosition = 0.95;
  //     valueAxis2.renderer.fontSize = "0.8em"
      
  //     valueAxis2.renderer.gridContainer.background.fill = am4core.color("#000000");
  //     valueAxis2.renderer.gridContainer.background.fillOpacity = 0.05;
  
  //     var series2 = chart.series.push(new am4charts.LineSeries());
  //     series2.dataFields.dateX = "Date";
  //     series2.clustered = false;
  //     series2.dataFields.valueY = "RSI";
  //     series2.yAxis = valueAxis2;
  //     series2.tooltipText = "RSI: {valueY.value}";
  //     series2.name = "Series 2";
  //     series2.defaultState.transitionDuration = 0;
  //   }
  // }, 10000);

  
function rsiGraph(result, summ){

  if (result[0].RSI !== undefined) {
    // .at(-1)
    firstDay = result[0].Date
    lastDay = result[result.length-1].Date
    // lastDay = result[Object.keys(result)[result.length-1]].Date
    // RSIOB = summ[Object.keys("RSIOB")]
    RSIOB = summ.RSIOB
    RSIOS = summ.RSIOS
    RSI_BASE = summ.RSI_BASE

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

    var series2 = chart.series.push(new am4charts.LineSeries());
    series2.dataFields.dateX = "Date";
    series2.clustered = false;
    series2.dataFields.valueY = "RSI";
    series2.yAxis = valueAxis2;
    series2.tooltipText = "RSI: {valueY.value}";
    series2.name = "Series 2";
    series2.stroke = am4core.color("purple");
    series2.tooltip.getFillFromObject = false;
    series2.tooltip.background.fill = am4core.color("purple");
    series2.defaultState.transitionDuration = 0;

    // Overbought
    var OBSeries = chart.series.push(new am4charts.LineSeries());
    OBSeries.dataFields.dateX = "Date";
    OBSeries.clustered = false;
    OBSeries.dataFields.valueY = "RSIOB";
    OBSeries.yAxis = valueAxis2;
    OBSeries.tooltipText = "RSI OB: {valueY.value}";
    OBSeries.name = "OBSeries";
    OBSeries.defaultState.transitionDuration = 0;
    OBSeries.strokeDasharray = 4;
    OBSeries.strokeWidth = 2
    OBSeries.stroke = am4core.color("red");
    OBSeries.tooltip.getFillFromObject = false;
    OBSeries.tooltip.background.fill = am4core.color("red");
    OBSeries.strokeOpacity = 0.7;
    OBSeries.data = [{"Date": firstDay, "RSIOB": RSIOB },  {"Date": lastDay, "RSIOB": RSIOB }];
    
    // Base
    var RSIBASESeries = chart.series.push(new am4charts.LineSeries());
    RSIBASESeries.dataFields.dateX = "Date";
    RSIBASESeries.clustered = false;
    RSIBASESeries.dataFields.valueY = "RSI_BASE";
    RSIBASESeries.yAxis = valueAxis2;
    RSIBASESeries.tooltipText = "RSI OS: {valueY.value}";
    RSIBASESeries.name = "RSIBASESeries";
    RSIBASESeries.defaultState.transitionDuration = 0;
    RSIBASESeries.strokeDasharray = 4;
    RSIBASESeries.strokeWidth = 2
    RSIBASESeries.stroke = am4core.color("black");
    RSIBASESeries.tooltip.getFillFromObject = false;
    RSIBASESeries.tooltip.background.fill = am4core.color("black");
    RSIBASESeries.strokeOpacity = 0.7;
    RSIBASESeries.data = [{"Date": firstDay, "RSI_BASE": RSI_BASE },  {"Date": lastDay, "RSI_BASE": RSI_BASE }];

    // Oversold
    var OSSeries = chart.series.push(new am4charts.LineSeries());
    OSSeries.dataFields.dateX = "Date";
    OSSeries.clustered = false;
    OSSeries.dataFields.valueY = "RSIOS";
    OSSeries.yAxis = valueAxis2;
    OSSeries.tooltipText = "RSI OS: {valueY.value}";
    OSSeries.name = "OSSeries";
    OSSeries.defaultState.transitionDuration = 0;
    OSSeries.strokeDasharray = 4;
    OSSeries.strokeWidth = 2
    OSSeries.stroke = am4core.color("green");
    OSSeries.tooltip.getFillFromObject = false;
    OSSeries.tooltip.background.fill = am4core.color("green");
    OSSeries.strokeOpacity = 0.7;
    OSSeries.data = [{"Date": firstDay, "RSIOS": RSIOS },  {"Date": lastDay, "RSIOS": RSIOS }];
  }

  // Third chart: Volume
  var valueAxis3 = chart.yAxes.push(new am4charts.ValueAxis());
  valueAxis3.tooltip.disabled = true;
  // height of axis
  valueAxis3.height = am4core.percent(35);
  valueAxis3.zIndex = 3
  // this makes gap between panels
  valueAxis3.marginTop = 30;
  valueAxis3.renderer.baseGrid.disabled = true;
  valueAxis3.renderer.inside = true;
  valueAxis3.renderer.labels.template.verticalCenter = "bottom";
  valueAxis3.renderer.labels.template.padding(2, 2, 2, 2);
  //valueAxis.renderer.maxLabelPosition = 0.95;
  valueAxis3.renderer.fontSize = "0.8em"
  
  valueAxis3.renderer.gridContainer.background.fill = am4core.color("#000000");
  valueAxis3.renderer.gridContainer.background.fillOpacity = 0.05;

  var series3 = chart.series.push(new am4charts.ColumnSeries());
  series3.dataFields.dateX = "Date";
  series3.clustered = false;
  series3.dataFields.valueY = "Volume";
  series3.yAxis = valueAxis3;
  series3.tooltipText = "Volume: {valueY.value}";
  series3.name = "Series 3";
  // volume should be summed
  series3.groupFields.valueY = "sum";
  series3.defaultState.transitionDuration = 0;

  series3.fill = am4core.color("rgb(65, 112, 216)");
  series3.stroke = am4core.color("rgb(65, 112, 216)");
  series3.tooltip.getFillFromObject = false;
  series3.tooltip.background.fill = am4core.color("rgb(65, 112, 216)");
}

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

  chart.svgContainer.htmlElement.style.height = "900px";
  
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
