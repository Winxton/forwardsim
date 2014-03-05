
    OANDA.baseURL = "https://api-fxpractice.oanda.com";
  	OANDA.auth.token = 'b47aa58922aeae119bcc4de139f7ea1e-27de2d1074bb442b4ad2fe0d637dec22';
  	OANDA.auth.enabled = true;
  	var account_id = 3922748;
    var currency_pair = "USD_JPY";

    /*setup editor*/
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/clouds_midnight");
    editor.getSession().setMode("ace/mode/python");
    editor.getSession().setTabSize(4);
    editor.setValue("def initialize(context):\n    # set data and variables used in your trading algorithm\n    context.units = 1000\n\ndef handle_data(context, data):\n    # handles a data event\n    # put your algorithm here and make trades\n    mavg = context.mavg(data, timeperiod=3)\n    context.plot(mavg, 'mavg')\n\n    print context.units\n");
    /* start and stop functions */
    $("#start").click(function(){
        var data = {};
        data['code'] = editor.getValue();
        alert(JSON.stringify(data));

        $.ajax({
          type: "POST",
          url: '/start/',
          data: JSON.stringify(data),
          contentType: 'application/json; charset=utf-8',
          success: function(response){
            // create time series for candlestick charts
            console.log(response);
            
            for (var i = 0; i<response.plotnames.length; i++) {
              var plotName = response.plotnames[i];
              console.log(plotName);

              candlechart.addSeries({
                id: plotName,
                name: plotName,
                data: []
              });
            }

            // make a request for the line every few seconds
            setInterval(
              function() {
                $.ajax({
                    type: "GET",
                    url: '/get-plot-points/',
                    success: function(response) {
                      if (response.status == "task_running") {

                        var plotdata = response.data;
                        var time = Math.round(plotdata.time);
                        var time2 = new Date().getTime();
                        alert(time2);

                        // go through datapoints
                        for (data in plotdata.values) {
                          var candleplotdata = plotdata.values[data];
                          var name = candleplotdata[0];
                          var val = candleplotdata[1];

                          console.log(name);
                          console.log(time);
                          console.log(val);

                          var point = [time, val];

                          var series = candlechart.get(name);
                          console.log(point);
                          series.addPoint(point);
                        }

                      }
                    },
                    dataType: 'json'
                });
            }, 10000);

          },
          dataType: 'json'
        });
    });

    $("#stop").click(function(){
        var url = '/stop/';

        $.ajax({
          type: "POST",
          url: url,
          contentType: 'application/json; charset=utf-8',
          success: function(response) {
            alert("STOPPED");
          }
        });
    });

    /* charts for candlesticks and portfolio value */
    var candlechart;
    var rates = new Array();
    var account_value = new Array();
    var newtick;
    var lasttick;

    function getHistory() {
        OANDA.rate.history(currency_pair, {count: 1, candleFormat: "midpoint"}, function(rateHistoryResponse) {
            newtick = parseOandaHistoryToArray(rateHistoryResponse.candles[0]);
        });
    }
    
    function getAccountInfo() {

    }

    function parseOandaHistoryToArray(rate) {
        var testarray = new Array();
        testarray = [Date.parse(rate.time), rate.openMid, rate.highMid, rate.lowMid, rate.closeMid];
        return testarray
    }

    function initialize() {
    	// initialize with oanda historical candles and dynamically update
        OANDA.rate.history(currency_pair, {count: 20, candleFormat: "midpoint"}, function(rateHistoryResponse) {
            var price;
            for (var i = 0 ; i < 20; i++) {
                price = rateHistoryResponse.candles[i];
                rates.push(parseOandaHistoryToArray(price));
            }
            lasttick = rates[19];
            newtick = lasttick;

            candlechart = new Highcharts.StockChart({
                chart : {
                    renderTo: 'candlestick-chart',
                    borderRadius: 0,
                    backgroundColor: '#222222',
                    style: {
                        color: '#888888'
                    },
                    events : {
                        load : function() {
                            var series = this.series[0];
                            setInterval(function() {
                                getHistory();
                                if (lasttick.toString() != newtick.toString()) {
                                    series.addPoint(newtick, true, false);
                                    lasttick = newtick;
                                }
                            }, 5000);
                        }
                    },

                },

                title : {
                    text : 'Currency Pair Price',
                    style: {
                        color: "#94d600"
                    }
                },

                scrollbar : {
                                enabled : false
                },

                plotOptions: {
                      series: {
                         nullColor: '#444444'
                      },
                      line: {
                         dataLabels: {
                            color: '#CCC'
                         },
                         marker: {
                            lineColor: '#333'
                         }
                      },
                      spline: {
                         marker: {
                            lineColor: '#333'
                         }
                      },
                      scatter: {
                         marker: {
                            lineColor: '#333'
                         }
                      },
                      candlestick: {
                         lineColor: 'white',
                         color: 'red',
                         upColor: '#94d600'
                      }
                   },

                   rangeSelector: {
                        buttonTheme: {
                           stroke: '#888888',
                           fill: '#444444',
                           backgroundColor: '#888888'
,                           style: {
                              color: '#888888',
                              fontWeight: 'bold'
                           },
                           states: {
                              hover: {
                                 stroke: '#888888',
                                 style: {
                                    color: '#888888'
                                 }
                              },
                              select: {
                                 stroke: '#000000',
                                 style: {
                                    color: 'green'
                                 }
                              }
                           }
                        },
                        inputStyle: {
                           backgroundColor: '#888888',
                           color: 'silver'
                        },
                        labelStyle: {
                           color: 'silver'
                        }
                     },

                  navigator: {
                     handles: {
                        backgroundColor: '#888888',
                        borderColor: '#888888'
                     },
                     outlineColor: '#CCC',
                     maskFill: 'rgba(16, 16, 16, 0.5)',
                     series: {
                        color: '#888888',
                        lineColor: '#888888'
                     }
                  },



                xAxis: {
                      gridLineWidth: 0.5,
                      gridLineColor: '#888888',
                      lineColor: '#888888',
                      lineWidth: 0.5,
                      minorGridLineWidth: 0,
                      tickColor: '#888888',
                      labels: {
                         style: {
                            color: '#888888',
                            font: '11px Trebuchet MS, Verdana, sans-serif'
                         }
                      },
                      title: {
                         style: {
                            color: '#333',
                            fontWeight: 'bold',
                            fontSize: '12px',
                            fontFamily: 'Trebuchet MS, Verdana, sans-serif'

                         }            
                      }
                   },
                   yAxis: {
                      minorTickInterval: 'auto',
                      gridLineColor: '#888888',
                      lineColor: '#888888',
                      lineWidth: 0.5,
                      minorGridLineWidth: 0,
                      gridLineWidth: 0.5,
                      tickColor: '#888888',
                      labels: {
                         style: {
                            color: '#888888',
                            font: '11px Trebuchet MS, Verdana, sans-serif'
                         }
                      },
                      title: {
                         style: {
                            color: '#888888',
                            fontWeight: 'bold',
                            fontSize: '12px',
                            fontFamily: 'Trebuchet MS, Verdana, sans-serif'
                         }            
                      }
                   },

                series : [{
                    type : 'candlestick',
                    name : 'Currency Pair Price',
                    data : rates,
                }]
            });
        });

        OANDA.account.listSpecific(account_id, function(accountInfoResponse){
        	console.log(accountInfoResponse.balance);
        	console.log(accountInfoResponse.unrealizedPl);
        	console.log(accountInfoResponse.realizedPl);

        	var totalPL = accountInfoResponse.unrealizedPl + accountInfoResponse.realizedPl;

	        $('#account-value-chart').highcharts({
	            chart: {
                    borderRadius: 0,
                    backgroundColor: '#222222',
                    style: {
                        color: '#888888'
                    },
	                //type: 'spline',
	                //animation: Highcharts.svg, // don't animate in old IE
	                //marginRight: 10,
	                events: {
	                    load: function() {
	                        // set up the updating of the chart every few seconds
	                        var series = this.series[0];
	                        setInterval(function() {
	                        	OANDA.account.listSpecific(account_id, function(updatedAccountInfoResponse){
	                        		var x = new Date().getTime(); // current time

	                        		var updatedTotalPL = updatedAccountInfoResponse.unrealizedPl 
	                        							+ updatedAccountInfoResponse.realizedPl;
	                        		var y = updatedTotalPL;
	                        	series.addPoint([x, y], true, false);
	                        	});
	                        }, 5000);
	                    }
	                }
	            },
	            title: {
	                text: 'Profit & Loss'
	            },
	            xAxis: {
	                type: 'datetime',
	                //tickPixelInterval: 150
	            },
	            yAxis: {
	                title: {
	                    text: 'Account Value ($)'
	                },
	                plotLines: [{
	                    value: 0,
	                    width: 5,
	                    color: '#808080'
	                }]
	            },
	            tooltip: {
	                formatter: function() {
	                        return '<b>'+ this.series.name +'</b><br/>'+
	                        Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) +'<br/>'+
	                        Highcharts.numberFormat(this.y, 2);
	                }
	            },

                title : {
                    text : 'Currency Pair Price',
                    style: {
                        color: "#94d600"
                    }
                },

                plotOptions: {
                      series: {
                         nullColor: '#444444'
                      },
                      line: {
                         dataLabels: {
                            color: '#CCC'
                         },
                         marker: {
                            lineColor: '#333'
                         }
                      },
                      spline: {
                         marker: {
                            lineColor: '#333'
                         }
                      },
                      scatter: {
                         marker: {
                            lineColor: '#333'
                         }
                      },
                      candlestick: {
                         lineColor: 'white',
                         color: 'red',
                         upColor: '#94d600'
                      }
                   },

                rangeSelector: {
                     buttonTheme: {
                        stroke: '#444444',
                        style: {
                           color: '#444444',
                           fontWeight: 'bold'
                        },
                        states: {
                           hover: {
                              stroke: '#888888',
                              style: {
                                 color: '#888888'
                              }
                           },
                           select: {
                              stroke: '#000000',
                              style: {
                                 color: 'green'
                              }
                           }
                        }
                     },
                     inputStyle: {
                        backgroundColor: '#333',
                        color: 'silver'
                     },
                     labelStyle: {
                        color: 'silver'
                     }
                  },

                  navigator: {
                     handles: {
                        backgroundColor: '#888888',
                        borderColor: '#888888'
                     },
                     outlineColor: '#CCC',
                     maskFill: 'rgba(16, 16, 16, 0.5)',
                     series: {
                        color: '#888888',
                        lineColor: '#888888'
                     }
                  },



                xAxis: {
                      gridLineWidth: 0.5,
                      gridLineColor: '#888888',
                      lineColor: '#888888',
                      lineWidth: 0.5,
                      minorGridLineWidth: 0,
                      tickColor: '#888888',
                      labels: {
                         style: {
                            color: '#888888',
                            font: '11px Trebuchet MS, Verdana, sans-serif'
                         }
                      },
                      title: {
                         style: {
                            color: '#333',
                            fontWeight: 'bold',
                            fontSize: '12px',
                            fontFamily: 'Trebuchet MS, Verdana, sans-serif'

                         }            
                      }
                   },
                   yAxis: {
                      minorTickInterval: 'auto',
                      gridLineColor: '#888888',
                      lineColor: '#888888',
                      lineWidth: 0.5,
                      minorGridLineWidth: 0,
                      gridLineWidth: 0.5,
                      tickColor: '#888888',
                      labels: {
                         style: {
                            color: '#888888',
                            font: '11px Trebuchet MS, Verdana, sans-serif'
                         }
                      },
                      title: {
                         style: {
                            color: '#888888',
                            fontWeight: 'bold',
                            fontSize: '12px',
                            fontFamily: 'Trebuchet MS, Verdana, sans-serif'
                         }            
                      }
                   },
	            /*
	            legend: {
	                enabled: false
	            },
	            exporting: {
	                enabled: false
	            },
	            */
	            series: [{
	                name: 'Account Balance',
	                data: (function() {
	                    // generate the initial array of data
	                    var data = [],
	                        time = (new Date()).getTime(),
	                        i;
	                    for (i = -15; i <= 0; i++) {
	                        data.push({
	                            x: time + i * 5000,
	                            y: totalPL
	                        });
	                    }
	                    return data;
	                })(),
	                color: 'green',
	                negativeColor: '#BD5D55'
	            }]
	        });
        });
    }

    initialize();
