from collections import defaultdict

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import (
    StockBarsRequest,
    StockQuotesRequest,
    StockTradesRequest,
    LatestStockTradeRequest,
    LatestStockQuoteRequest,
    StockSnapshotRequest,
)
from alpaca.data.time import TimeFrame
from alpaca.data.enums import Exchange, DataFeed
from alpaca.data.models import BarSet, Quote, QuoteSet, SnapshotSet, Trade, TradeSet


def test_get_bars(reqmock, stock_client: StockHistoricalDataClient):
    # Test single symbol request

    symbol = "AAPL"
    timeframe = TimeFrame.Day
    start = "2022-02-01"
    limit = 2

    reqmock.get(
        f"https://data.alpaca.markets/v2/stocks/{symbol}/bars?timeframe={timeframe}&start={start}&limit={limit}",
        text="""
    {
        "bars": [
            {
                "t": "2022-02-01T05:00:00Z",
                "o": 174,
                "h": 174.84,
                "l": 172.31,
                "c": 174.61,
                "v": 85998033,
                "n": 732412,
                "vw": 173.703516
            },
            {
                "t": "2022-02-02T05:00:00Z",
                "o": 174.64,
                "h": 175.88,
                "l": 173.33,
                "c": 175.84,
                "v": 84817432,
                "n": 675034,
                "vw": 174.941288
            }
        ],
        "symbol": "AAPL",
        "next_page_token": "QUFQTHxEfDIwMjItMDItMDJUMDU6MDA6MDAuMDAwMDAwMDAwWg=="
    }   
        """,
    )
    request = StockBarsRequest(
        symbol_or_symbols=symbol, timeframe=timeframe, start=start, limit=limit
    )
    barset = stock_client.get_stock_bars(request_params=request)

    assert isinstance(barset, BarSet)

    assert barset[symbol][0].open == 174
    assert barset[symbol][0].high == 174.84

    assert barset.df.index.nlevels == 2

    assert reqmock.called_once


def test_raw_get_bars(reqmock, raw_stock_client: StockHistoricalDataClient):
    symbol = "AAPL"
    timeframe = TimeFrame.Day
    start = "2022-02-01"
    limit = 2

    reqmock.get(
        f"https://data.alpaca.markets/v2/stocks/{symbol}/bars?timeframe={timeframe}&start={start}&limit={limit}",
        text="""
        {
            "bars": [
                {
                    "t": "2022-02-01T05:00:00Z",
                    "o": 174,
                    "h": 174.84,
                    "l": 172.31,
                    "c": 174.61,
                    "v": 85998033,
                    "n": 732412,
                    "vw": 173.703516
                },
                {
                    "t": "2022-02-02T05:00:00Z",
                    "o": 174.64,
                    "h": 175.88,
                    "l": 173.33,
                    "c": 175.84,
                    "v": 84817432,
                    "n": 675034,
                    "vw": 174.941288
                }
            ],
            "symbol": "AAPL",
            "next_page_token": "QUFQTHxEfDIwMjItMDItMDJUMDU6MDA6MDAuMDAwMDAwMDAwWg=="
        }   
            """,
    )
    request = StockBarsRequest(
        symbol_or_symbols=symbol, timeframe=timeframe, start=start, limit=limit
    )
    raw_barset = raw_stock_client.get_stock_bars(request_params=request)

    assert raw_barset[symbol][0]["o"] == 174
    assert raw_barset[symbol][0]["h"] == 174.84

    assert reqmock.called_once


def test_multisymbol_get_bars(reqmock, stock_client: StockHistoricalDataClient):
    # test multisymbol request
    symbols = ["AAPL", "TSLA"]
    start = "2022-02-01"
    end = "2022-03-09"
    timeframe = TimeFrame.Day
    _symbols_in_url = "%2C".join(s for s in symbols)

    reqmock.get(
        f"https://data.alpaca.markets/v2/stocks/bars?timeframe={timeframe}&start={start}&end={end}&symbols={_symbols_in_url}",
        text="""
    {
        "bars": {
            "AAPL": [
                {
                    "t": "2022-03-09T05:00:00Z",
                    "o": 161.51,
                    "h": 163.41,
                    "l": 159.41,
                    "c": 162.95,
                    "v": 88496480,
                    "n": 700291,
                    "vw": 161.942117
                }
            ],
            "TSLA": [
                {
                    "t": "2022-03-09T05:00:00Z",
                    "o": 839,
                    "h": 860.56,
                    "l": 832.01,
                    "c": 858.97,
                    "v": 19227323,
                    "n": 528531,
                    "vw": 850.616587
                }
            ]
        },
        "next_page_token": null
    }   
        """,
    )

    request = StockBarsRequest(
        symbol_or_symbols=symbols, timeframe=timeframe, start=start, end=end
    )

    barset = stock_client.get_stock_bars(request_params=request)

    assert type(barset) == BarSet

    assert barset["TSLA"][0].open == 839
    assert barset["AAPL"][0].low == 159.41

    assert barset.df.index[0][1].day == 9
    assert barset.df.index.nlevels == 2


def test_raw_multisymbol_get_bars(reqmock, raw_stock_client: StockHistoricalDataClient):
    symbols = ["AAPL", "TSLA"]
    start = "2022-02-01"
    end = "2022-03-09"
    timeframe = TimeFrame.Day
    _symbols_in_url = "%2C".join(s for s in symbols)

    reqmock.get(
        f"https://data.alpaca.markets/v2/stocks/bars?timeframe={timeframe}&start={start}&end={end}&symbols={_symbols_in_url}",
        text="""
        {
            "bars": {
                "AAPL": [
                    {
                        "t": "2022-03-09T05:00:00Z",
                        "o": 161.51,
                        "h": 163.41,
                        "l": 159.41,
                        "c": 162.95,
                        "v": 88496480,
                        "n": 700291,
                        "vw": 161.942117
                    }
                ],
                "TSLA": [
                    {
                        "t": "2022-03-09T05:00:00Z",
                        "o": 839,
                        "h": 860.56,
                        "l": 832.01,
                        "c": 858.97,
                        "v": 19227323,
                        "n": 528531,
                        "vw": 850.616587
                    }
                ]
            },
            "next_page_token": null
        }   
            """,
    )
    request = StockBarsRequest(
        symbol_or_symbols=symbols, timeframe=timeframe, start=start, end=end
    )

    raw_barset = raw_stock_client.get_stock_bars(request_params=request)

    assert raw_barset["TSLA"][0]["o"] == 839
    assert raw_barset["AAPL"][0]["l"] == 159.41

    assert reqmock.called_once


def test_get_quotes(reqmock, stock_client: StockHistoricalDataClient):
    # Test single symbol request

    symbol = "AAPL"
    start = "2022-03-09"
    limit = 2

    reqmock.get(
        f"https://data.alpaca.markets/v2/stocks/{symbol}/quotes?start={start}&limit={limit}",
        text="""
    {
        "quotes": [
            {
                "t": "2022-03-09T09:00:00.000059Z",
                "ax": "K",
                "ap": 158.65,
                "as": 1,
                "bx": "Q",
                "bp": 159.52,
                "bs": 4,
                "c": [
                    "R"
                ],
                "z": "C"
            },
            {
                "t": "2022-03-09T09:00:00.000059Z",
                "ax": "K",
                "ap": 158.8,
                "as": 1,
                "bx": "Q",
                "bp": 159.52,
                "bs": 4,
                "c": [
                    "R"
                ],
                "z": "C"
            }
        ],
        "symbol": "AAPL",
        "next_page_token": "QUFQTHwyMDIyLTAzLTA5VDA5OjAwOjAwLjAwMDA1OTAwMFp8Q0ZEQUU5QTg="
    }   
        """,
    )
    request = StockQuotesRequest(symbol_or_symbols=symbol, start=start, limit=limit)

    quoteset = stock_client.get_stock_quotes(request_params=request)

    assert isinstance(quoteset, QuoteSet)

    assert quoteset[symbol][0].ask_price == 158.65
    assert quoteset[symbol][0].bid_size == 4

    assert quoteset[symbol][0].ask_exchange == "K"

    assert quoteset.df.index.nlevels == 2

    assert reqmock.called_once


def test_raw_get_quotes(reqmock, raw_stock_client: StockHistoricalDataClient):
    symbol = "AAPL"
    start = "2022-03-09"
    limit = 2

    reqmock.get(
        f"https://data.alpaca.markets/v2/stocks/{symbol}/quotes?start={start}&limit={limit}",
        text="""
       {
           "quotes": [
               {
                   "t": "2022-03-09T09:00:00.000059Z",
                   "ax": "K",
                   "ap": 158.65,
                   "as": 1,
                   "bx": "Q",
                   "bp": 159.52,
                   "bs": 4,
                   "c": [
                       "R"
                   ],
                   "z": "C"
               },
               {
                   "t": "2022-03-09T09:00:00.000059Z",
                   "ax": "K",
                   "ap": 158.8,
                   "as": 1,
                   "bx": "Q",
                   "bp": 159.52,
                   "bs": 4,
                   "c": [
                       "R"
                   ],
                   "z": "C"
               }
           ],
           "symbol": "AAPL",
           "next_page_token": "QUFQTHwyMDIyLTAzLTA5VDA5OjAwOjAwLjAwMDA1OTAwMFp8Q0ZEQUU5QTg="
       }   
           """,
    )
    request = StockQuotesRequest(symbol_or_symbols=symbol, start=start, limit=limit)
    raw_quoteset = raw_stock_client.get_stock_quotes(request_params=request)

    assert raw_quoteset[symbol][0]["ap"] == 158.65
    assert raw_quoteset[symbol][0]["bs"] == 4

    assert raw_quoteset[symbol][0]["ax"] == "K"

    assert reqmock.called_once


def test_multisymbol_quotes(reqmock, stock_client: StockHistoricalDataClient):

    # test multisymbol request
    symbols = ["AAPL", "TSLA"]
    start = "2022-03-09"
    _symbols_in_url = "%2C".join(s for s in symbols)

    reqmock.get(
        f"https://data.alpaca.markets/v2/stocks/quotes?start={start}&symbols={_symbols_in_url}",
        text="""
    {
        "quotes": {
            "AAPL": [
                {
                    "t": "2022-03-09T09:00:00.000059Z",
                    "ax": "K",
                    "ap": 158.65,
                    "as": 1,
                    "bx": "Q",
                    "bp": 159.52,
                    "bs": 4,
                    "c": [
                        "R"
                    ],
                    "z": "C"
                }
            ],
            "TSLA": [
                {
                    "t": "2022-03-09T09:00:00.000805Z",
                    "ax": "K",
                    "ap": 830,
                    "as": 1,
                    "bx": "P",
                    "bp": 840.75,
                    "bs": 1,
                    "c": [
                        "R"
                    ],
                    "z": "C"
                }
            ]
        },
        "next_page_token": null
    }   
        """,
    )

    request = StockQuotesRequest(symbol_or_symbols=symbols, start=start)

    quoteset = stock_client.get_stock_quotes(request_params=request)

    assert isinstance(quoteset, QuoteSet)

    assert quoteset["AAPL"][0].ask_size == 1
    assert quoteset["TSLA"][0].bid_price == 840.75

    assert quoteset["AAPL"][0].bid_exchange == "Q"

    assert quoteset.df.index.nlevels == 2

    assert reqmock.called_once


def test_raw_multisymbol_quotes(reqmock, raw_stock_client: StockHistoricalDataClient):
    # test multisymbol request
    symbols = ["AAPL", "TSLA"]
    start = "2022-03-09"
    _symbols_in_url = "%2C".join(s for s in symbols)

    reqmock.get(
        f"https://data.alpaca.markets/v2/stocks/quotes?start={start}&symbols={_symbols_in_url}",
        text="""
       {
           "quotes": {
               "AAPL": [
                   {
                       "t": "2022-03-09T09:00:00.000059Z",
                       "ax": "K",
                       "ap": 158.65,
                       "as": 1,
                       "bx": "Q",
                       "bp": 159.52,
                       "bs": 4,
                       "c": [
                           "R"
                       ],
                       "z": "C"
                   }
               ],
               "TSLA": [
                   {
                       "t": "2022-03-09T09:00:00.000805Z",
                       "ax": "K",
                       "ap": 830,
                       "as": 1,
                       "bx": "P",
                       "bp": 840.75,
                       "bs": 1,
                       "c": [
                           "R"
                       ],
                       "z": "C"
                   }
               ]
           },
           "next_page_token": null
       }   
           """,
    )
    request = StockQuotesRequest(symbol_or_symbols=symbols, start=start)

    # raw data client
    raw_quoteset = raw_stock_client.get_stock_quotes(request_params=request)

    assert raw_quoteset["AAPL"][0]["ap"] == 158.65
    assert raw_quoteset["TSLA"][0]["bs"] == 1

    assert raw_quoteset["AAPL"][0]["ax"] == "K"

    assert reqmock.called_once


def test_get_trades(reqmock, stock_client: StockHistoricalDataClient):
    # Test single symbol request
    symbol = "AAPL"
    start = "2022-03-09"
    limit = 2

    reqmock.get(
        f"https://data.alpaca.markets/v2/stocks/{symbol}/trades?start={start}&limit={limit}",
        text="""
    {
        "trades": [
            {
                "t": "2022-03-09T05:00:02.183Z",
                "x": "D",
                "p": 159.07,
                "s": 1,
                "c": [
                    "@",
                    "T",
                    "I"
                ],
                "i": 151,
                "z": "C"
            },
            {
                "t": "2022-03-09T05:00:16.91Z",
                "x": "D",
                "p": 159.07,
                "s": 2,
                "c": [
                    "@",
                    "T",
                    "I"
                ],
                "i": 168,
                "z": "C"
            }
        ],
        "symbol": "AAPL",
        "next_page_token": "QUFQTHwyMDIyLTAzLTA5VDA1OjAwOjE2LjkxMDAwMDAwMFp8RHwwOTIyMzM3MjAzNjg1NDc3NTk3Ng=="
    }  
        """,
    )

    request = StockTradesRequest(symbol_or_symbols=symbol, start=start, limit=limit)

    tradeset = stock_client.get_stock_trades(request_params=request)

    assert isinstance(tradeset, TradeSet)

    assert tradeset[symbol][0].price == 159.07
    assert tradeset[symbol][0].size == 1

    assert tradeset[symbol][0].exchange == Exchange.D

    assert tradeset.df.index.nlevels == 2

    assert reqmock.called_once


def test_raw_get_trades(reqmock, raw_stock_client: StockHistoricalDataClient):

    symbol = "AAPL"
    start = "2022-03-09"
    limit = 2

    reqmock.get(
        f"https://data.alpaca.markets/v2/stocks/{symbol}/trades?start={start}&limit={limit}",
        text="""
    {
        "trades": [
            {
                "t": "2022-03-09T05:00:02.183Z",
                "x": "D",
                "p": 159.07,
                "s": 1,
                "c": [
                    "@",
                    "T",
                    "I"
                ],
                "i": 151,
                "z": "C"
            },
            {
                "t": "2022-03-09T05:00:16.91Z",
                "x": "D",
                "p": 159.07,
                "s": 2,
                "c": [
                    "@",
                    "T",
                    "I"
                ],
                "i": 168,
                "z": "C"
            }
        ],
        "symbol": "AAPL",
        "next_page_token": "QUFQTHwyMDIyLTAzLTA5VDA1OjAwOjE2LjkxMDAwMDAwMFp8RHwwOTIyMzM3MjAzNjg1NDc3NTk3Ng=="
    }  
        """,
    )

    request = StockTradesRequest(symbol_or_symbols=symbol, start=start, limit=limit)

    # raw data client
    raw_tradeset = raw_stock_client.get_stock_trades(request_params=request)

    assert raw_tradeset[symbol][0]["p"] == 159.07
    assert raw_tradeset[symbol][0]["s"] == 1

    assert raw_tradeset[symbol][0]["x"] == "D"

    assert reqmock.called_once


def test_multisymbol_get_trades(reqmock, stock_client: StockHistoricalDataClient):
    # test multisymbol request
    symbols = ["AAPL", "TSLA"]
    start = "2022-03-09"
    end = "2022-03-09"
    _symbols_in_url = "%2C".join(s for s in symbols)

    reqmock.get(
        f"https://data.alpaca.markets/v2/stocks/trades?start={start}&symbols={_symbols_in_url}",
        text="""
    {
        "trades": {
            "AAPL": [
                {
                    "t": "2022-03-09T05:00:02.183Z",
                    "x": "D",
                    "p": 159.07,
                    "s": 1,
                    "c": [
                        "@",
                        "T",
                        "I"
                    ],
                    "i": 151,
                    "z": "C"
                }
            ],
            "TSLA": [
                {
                    "t": "2022-03-09T05:08:03.035Z",
                    "x": "D",
                    "p": 833,
                    "s": 1,
                    "c": [
                        "@",
                        "T",
                        "I"
                    ],
                    "i": 145,
                    "z": "C"
                }
            ]
        },
        "next_page_token": null
    }   
        """,
    )

    request = StockTradesRequest(symbol_or_symbols=symbols, start=start)

    tradeset = stock_client.get_stock_trades(request_params=request)

    assert isinstance(tradeset, TradeSet)

    assert tradeset["AAPL"][0].size == 1
    assert tradeset["TSLA"][0].price == 833

    assert tradeset["AAPL"][0].exchange == Exchange.D

    assert tradeset.df.index[0][1].day == 9
    assert tradeset.df.index.nlevels == 2

    assert reqmock.called_once


def test_raw_multisymbol_get_trades(
    reqmock, raw_stock_client: StockHistoricalDataClient
):
    # test multisymbol request
    symbols = ["AAPL", "TSLA"]
    start = "2022-03-09"
    _symbols_in_url = "%2C".join(s for s in symbols)

    reqmock.get(
        f"https://data.alpaca.markets/v2/stocks/trades?start={start}&symbols={_symbols_in_url}",
        text="""
        {
            "trades": {
                "AAPL": [
                    {
                        "t": "2022-03-09T05:00:02.183Z",
                        "x": "D",
                        "p": 159.07,
                        "s": 1,
                        "c": [
                            "@",
                            "T",
                            "I"
                        ],
                        "i": 151,
                        "z": "C"
                    }
                ],
                "TSLA": [
                    {
                        "t": "2022-03-09T05:08:03.035Z",
                        "x": "D",
                        "p": 833,
                        "s": 1,
                        "c": [
                            "@",
                            "T",
                            "I"
                        ],
                        "i": 145,
                        "z": "C"
                    }
                ]
            },
            "next_page_token": null
        }   
            """,
    )
    # raw data client
    request = StockTradesRequest(symbol_or_symbols=symbols, start=start)
    raw_tradeset = raw_stock_client.get_stock_trades(request_params=request)

    assert raw_tradeset["AAPL"][0]["p"] == 159.07
    assert raw_tradeset["TSLA"][0]["s"] == 1

    assert raw_tradeset["AAPL"][0]["x"] == "D"

    assert reqmock.called_once


def test_get_latest_trade(reqmock, stock_client: StockHistoricalDataClient):
    # Test single symbol request
    symbol = "AAPL"

    reqmock.get(
        f"https://data.alpaca.markets/v2/stocks/{symbol}/trades/latest?feed=IEX",
        text="""
    {
        "symbol": "AAPL",
        "trade": {
            "t": "2022-03-18T14:02:09.722539521Z",
            "x": "D",
            "p": 161.2958,
            "s": 100,
            "c": [
                "@"
            ],
            "i": 22730,
            "z": "C"
        }
    } 
        """,
    )
    request = LatestStockTradeRequest(symbol_or_symbols=symbol, feed=DataFeed.IEX)

    trade = stock_client.get_latest_stock_trade(request_params=request)

    assert isinstance(trade, TradeSet)

    assert trade[symbol][0].price == 161.2958
    assert trade[symbol][0].size == 100

    assert trade[symbol][0].exchange == Exchange.D

    assert reqmock.called_once


def test_raw_get_latest_trade(reqmock, raw_stock_client: StockHistoricalDataClient):
    # Test single symbol request
    symbol = "AAPL"

    reqmock.get(
        f"https://data.alpaca.markets/v2/stocks/{symbol}/trades/latest",
        text="""
    {
        "symbol": "AAPL",
        "trade": {
            "t": "2022-03-18T14:02:09.722539521Z",
            "x": "D",
            "p": 161.2958,
            "s": 100,
            "c": [
                "@"
            ],
            "i": 22730,
            "z": "C"
        }
    } 
        """,
    )

    request = LatestStockTradeRequest(symbol_or_symbols=symbol)

    # raw data client
    raw_trade = raw_stock_client.get_latest_stock_trade(request)

    assert raw_trade[symbol][0]["i"] == 22730
    assert raw_trade[symbol][0]["s"] == 100

    assert raw_trade[symbol][0]["z"] == "C"

    assert reqmock.called_once


def test_get_multisymbol_latest_trade(reqmock, stock_client: StockHistoricalDataClient):
    # Test single symbol request
    symbols = ["AAPL", "TSLA"]
    _symbols_in_url = "%2C".join(s for s in symbols)
    reqmock.get(
        f"https://data.alpaca.markets/v2/stocks/trades/latest?symbols={_symbols_in_url}",
        text="""
    {
    "trades": {
        "AAPL": {
            "t": "2022-03-18T14:02:09.722539521Z",
            "x": "D",
            "p": 161.2958,
            "s": 100,
            "c": [
                "@"
            ],
            "i": 22730,
            "z": "C"
        },
        "TSLA": {
            "t": "2022-07-15T19:59:59.405545378Z",
            "x": "V",
            "p": 720.19,
            "s": 100,
            "c": [
                "@"
            ],
            "i": 11017,
            "z": "C"
        }
        }
    }
        """,
    )
    request = LatestStockTradeRequest(symbol_or_symbols=symbols, feed=DataFeed.IEX)

    trade = stock_client.get_latest_stock_trade(request_params=request)

    assert isinstance(trade, TradeSet)

    assert trade["AAPL"][0].price == 161.2958
    assert trade["AAPL"][0].size == 100

    assert trade["AAPL"][0].exchange == Exchange.D

    assert reqmock.called_once


def test_raw_get_multisymbol_latest_trade(
    reqmock, raw_stock_client: StockHistoricalDataClient
):
    # Test single symbol request
    symbols = ["AAPL", "TSLA"]
    _symbols_in_url = "%2C".join(s for s in symbols)
    reqmock.get(
        f"https://data.alpaca.markets/v2/stocks/trades/latest?symbols={_symbols_in_url}",
        text="""
    {
    "trades": {
        "AAPL": {
            "t": "2022-03-18T14:02:09.722539521Z",
            "x": "D",
            "p": 161.2958,
            "s": 100,
            "c": [
                "@"
            ],
            "i": 22730,
            "z": "C"
        },
        "TSLA": {
            "t": "2022-07-15T19:59:59.405545378Z",
            "x": "V",
            "p": 720.19,
            "s": 100,
            "c": [
                "@"
            ],
            "i": 11017,
            "z": "C"
        }
        }
    }
        """,
    )
    request = LatestStockTradeRequest(symbol_or_symbols=symbols)

    trade = raw_stock_client.get_latest_stock_trade(request_params=request)

    assert trade["AAPL"][0]["p"] == 161.2958
    assert trade["AAPL"][0]["s"] == 100

    assert reqmock.called_once


def test_get_latest_quote(reqmock, stock_client: StockHistoricalDataClient):
    # Test single symbol request
    symbol = "AAPL"

    reqmock.get(
        f"https://data.alpaca.markets/v2/stocks/{symbol}/quotes/latest",
        text="""
    {
        "symbol": "AAPL",
        "quote": {
            "t": "2022-03-18T14:02:43.651613184Z",
            "ax": "P",
            "ap": 161.11,
            "as": 13,
            "bx": "K",
            "bp": 161.1,
            "bs": 2,
            "c": [
                "R"
            ],
            "z": "C"
        }
    }  
        """,
    )

    request = LatestStockQuoteRequest(symbol_or_symbols=symbol)

    quote = stock_client.get_latest_stock_quote(request)

    assert isinstance(quote, QuoteSet)

    assert quote[symbol][0].ask_price == 161.11
    assert quote[symbol][0].bid_size == 2

    assert quote[symbol][0].bid_exchange == "K"

    assert reqmock.called_once


def test_raw_get_latest_quote(reqmock, raw_stock_client: StockHistoricalDataClient):
    # Test single symbol request
    symbol = "AAPL"

    reqmock.get(
        f"https://data.alpaca.markets/v2/stocks/{symbol}/quotes/latest",
        text="""
    {
        "symbol": "AAPL",
        "quote": {
            "t": "2022-03-18T14:02:43.651613184Z",
            "ax": "P",
            "ap": 161.11,
            "as": 13,
            "bx": "K",
            "bp": 161.1,
            "bs": 2,
            "c": [
                "R"
            ],
            "z": "C"
        }
    }  
        """,
    )
    request = LatestStockQuoteRequest(symbol_or_symbols=symbol)
    # raw data client
    raw_quote = raw_stock_client.get_latest_stock_quote(request)

    assert raw_quote[symbol][0]["bp"] == 161.1
    assert raw_quote[symbol][0]["as"] == 13

    assert raw_quote[symbol][0]["ax"] == "P"

    assert reqmock.called_once


def test_get_snapshot(reqmock, stock_client: StockHistoricalDataClient):
    # Test single symbol request
    symbol = "AAPL"

    reqmock.get(
        f"https://data.alpaca.markets/v2/stocks/{symbol}/snapshot",
        text="""
    {
        "symbol": "AAPL",
        "latestTrade": {
            "t": "2022-03-18T14:33:58.448432206Z",
            "x": "D",
            "p": 161.1998,
            "s": 200,
            "c": [
                "@"
            ],
            "i": 39884,
            "z": "C"
        },
        "latestQuote": {
            "t": "2022-03-18T14:33:58.547942Z",
            "ax": "K",
            "ap": 161.2,
            "as": 2,
            "bx": "K",
            "bp": 161.19,
            "bs": 5,
            "c": [
                "R"
            ],
            "z": "C"
        },
        "minuteBar": {
            "t": "2022-03-18T14:32:00Z",
            "o": 161.595,
            "h": 161.63,
            "l": 161.31,
            "c": 161.365,
            "v": 195503,
            "n": 1880,
            "vw": 161.448073
        },
        "dailyBar": {
            "t": "2022-03-18T04:00:00Z",
            "o": 160.59,
            "h": 161.92,
            "l": 159.76,
            "c": 161.365,
            "v": 31749988,
            "n": 186143,
            "vw": 160.683364
        },
        "prevDailyBar": {
            "t": "2022-03-17T04:00:00Z",
            "o": 158.6,
            "h": 161,
            "l": 157.63,
            "c": 160.62,
            "v": 73839892,
            "n": 609067,
            "vw": 159.425082
        }
    }  
        """,
    )

    request = StockSnapshotRequest(symbol_or_symbols=symbol)

    snapshot = stock_client.get_stock_snapshot(request)

    assert isinstance(snapshot, SnapshotSet)

    assert snapshot[symbol].latest_trade.price == 161.1998
    assert snapshot[symbol].latest_quote.bid_size == 5
    assert snapshot[symbol].minute_bar.close == 161.365
    assert snapshot[symbol].daily_bar.volume == 31749988
    assert snapshot[symbol].previous_daily_bar.high == 161

    assert reqmock.called_once


def test_raw_get_snapshot(reqmock, raw_stock_client: StockHistoricalDataClient):
    # Test single symbol request
    symbol = "AAPL"

    reqmock.get(
        f"https://data.alpaca.markets/v2/stocks/{symbol}/snapshot",
        text="""
    {
        "symbol": "AAPL",
        "latestTrade": {
            "t": "2022-03-18T14:33:58.448432206Z",
            "x": "D",
            "p": 161.1998,
            "s": 200,
            "c": [
                "@"
            ],
            "i": 39884,
            "z": "C"
        },
        "latestQuote": {
            "t": "2022-03-18T14:33:58.547942Z",
            "ax": "K",
            "ap": 161.2,
            "as": 2,
            "bx": "K",
            "bp": 161.19,
            "bs": 5,
            "c": [
                "R"
            ],
            "z": "C"
        },
        "minuteBar": {
            "t": "2022-03-18T14:32:00Z",
            "o": 161.595,
            "h": 161.63,
            "l": 161.31,
            "c": 161.365,
            "v": 195503,
            "n": 1880,
            "vw": 161.448073
        },
        "dailyBar": {
            "t": "2022-03-18T04:00:00Z",
            "o": 160.59,
            "h": 161.92,
            "l": 159.76,
            "c": 161.365,
            "v": 31749988,
            "n": 186143,
            "vw": 160.683364
        },
        "prevDailyBar": {
            "t": "2022-03-17T04:00:00Z",
            "o": 158.6,
            "h": 161,
            "l": 157.63,
            "c": 160.62,
            "v": 73839892,
            "n": 609067,
            "vw": 159.425082
        }
    }  
        """,
    )
    request = StockSnapshotRequest(symbol_or_symbols=symbol)
    # raw data client
    raw_snapshot = raw_stock_client.get_stock_snapshot(request)

    assert raw_snapshot[symbol]["latestTrade"]["p"] == 161.1998
    assert raw_snapshot[symbol]["latestQuote"]["bs"] == 5
    assert raw_snapshot[symbol]["minuteBar"]["c"] == 161.365
    assert raw_snapshot[symbol]["dailyBar"]["v"] == 31749988
    assert raw_snapshot[symbol]["prevDailyBar"]["h"] == 161

    assert reqmock.called_once


def test_multisymbol_get_snapshot(reqmock, raw_stock_client: StockHistoricalDataClient):
    # test multisymbol request
    symbols = ["AAPL", "QQQ"]

    _symbols_in_url = "%2C".join(s for s in symbols)

    reqmock.get(
        f"https://data.alpaca.markets/v2/stocks/snapshots?symbols={_symbols_in_url}",
        text="""
    {
        "AAPL": {
            "latestTrade": {
                "t": "2022-03-18T14:34:34.271824896Z",
                "x": "N",
                "p": 161.27,
                "s": 100,
                "c": [
                    "@",
                    "F"
                ],
                "i": 1818,
                "z": "C"
            },
            "latestQuote": {
                "t": "2022-03-18T14:34:34.186718005Z",
                "ax": "N",
                "ap": 161.27,
                "as": 1,
                "bx": "Q",
                "bp": 161.26,
                "bs": 7,
                "c": [
                    "R"
                ],
                "z": "C"
            },
            "minuteBar": {
                "t": "2022-03-18T14:33:00Z",
                "o": 161.37,
                "h": 161.39,
                "l": 161.04,
                "c": 161.2,
                "v": 239239,
                "n": 2194,
                "vw": 161.210361
            },
            "dailyBar": {
                "t": "2022-03-18T04:00:00Z",
                "o": 160.59,
                "h": 161.92,
                "l": 159.76,
                "c": 161.2,
                "v": 31989242,
                "n": 188338,
                "vw": 160.687305
            },
            "prevDailyBar": {
                "t": "2022-03-17T04:00:00Z",
                "o": 158.6,
                "h": 161,
                "l": 157.63,
                "c": 160.62,
                "v": 73839892,
                "n": 609067,
                "vw": 159.425082
            }
        },
        "QQQ": {
            "latestTrade": {
                "t": "2022-03-18T14:34:34.16829312Z",
                "x": "P",
                "p": 346.18,
                "s": 100,
                "c": [
                    "@",
                    "F"
                ],
                "i": 40267,
                "z": "C"
            },
            "latestQuote": {
                "t": "2022-03-18T14:34:34.188485Z",
                "ax": "Z",
                "ap": 346.19,
                "as": 2,
                "bx": "Z",
                "bp": 346.17,
                "bs": 9,
                "c": [
                    "R"
                ],
                "z": "C"
            },
            "minuteBar": {
                "t": "2022-03-18T14:33:00Z",
                "o": 346.54,
                "h": 346.54,
                "l": 345.96,
                "c": 346.1418,
                "v": 201396,
                "n": 2256,
                "vw": 346.154343
            },
            "dailyBar": {
                "t": "2022-03-18T04:00:00Z",
                "o": 342.805,
                "h": 347.49,
                "l": 341.55,
                "c": 346.1418,
                "v": 21970063,
                "n": 190685,
                "vw": 344.32075
            },
            "prevDailyBar": {
                "t": "2022-03-17T04:00:00Z",
                "o": 338.47,
                "h": 344.49,
                "l": 337.0406,
                "c": 344.44,
                "v": 66671636,
                "n": 597272,
                "vw": 340.878748
            }
        }
    }   
        """,
    )

    request = StockSnapshotRequest(symbol_or_symbols=symbols)
    # raw data client
    raw_snapshots = raw_stock_client.get_stock_snapshot(request)

    assert raw_snapshots["AAPL"]["latestTrade"]["p"] == 161.27
    assert raw_snapshots["AAPL"]["latestQuote"]["bs"] == 7
    assert raw_snapshots["AAPL"]["dailyBar"]["l"] == 159.76
    assert raw_snapshots["QQQ"]["minuteBar"]["c"] == 346.1418
    assert raw_snapshots["QQQ"]["dailyBar"]["v"] == 21970063
    assert raw_snapshots["QQQ"]["prevDailyBar"]["h"] == 344.49

    assert reqmock.called_once