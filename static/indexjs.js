    
    OANDA.baseURL = "https://api-fxpractice.oanda.com";
	OANDA.auth.token = 'b47aa58922aeae119bcc4de139f7ea1e-27de2d1074bb442b4ad2fe0d637dec22';
	OANDA.auth.enabled = true;
	var account_id = 3922748;
    var currency_pair = "USD_JPY";

    /*setup editor*/
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.getSession().setMode("ace/mode/python");
    editor.getSession().setTabSize(4);
    editor.setValue("def initialize(context):\n    # set data and variables used in your trading algorithm\n    context.units = 1000\n\ndef handle_data(context):\n    # handles a data event\n    # put your algorithm here and make trades\n    \n    print context.units\n");

    /* start and stop functions */
    $("#start").click(function(){
        var data = {};
        data['code'] = editor.getValue();
        var url = '/start/';

        alert(JSON.stringify(data));

        $.ajax({
          type: "POST",
          url: url,
          data: JSON.stringify(data),
          contentType: 'application/json; charset=utf-8',
          dataType: 'json'
        });
    });

    $("#stop").click(function(){
        var url = '/stop/';

        alert("starting to stop");

        $.ajax({
          type: "POST",
          url: url,
          contentType: 'application/json; charset=utf-8',
          success: function(response) {
            alert("stopped");
          }
        });
    });

    /* charts for candlesticks and portfolio value */
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

            $('#candlestick-chart').highcharts('StockChart', {
                chart : {
                    events : {
                        load : function() {
                            var series = this.series[0];
                            setInterval(function() {
                                getHistory();
                                if (lasttick.toString() != newtick.toString()) {
                                    series.addPoint(newtick, true, true);
                                    lasttick = newtick;
                                }
                            }, 3000);
                        }
                    }
                },

                title : {
                    text : 'Currency Pair Price'
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
	                            	
	                            	series.addPoint([x, y], true, true);
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
