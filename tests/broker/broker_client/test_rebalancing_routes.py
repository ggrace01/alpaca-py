from requests_mock import Mocker
from alpaca.broker.client import BrokerClient
from alpaca.broker.models import Portfolio, Subscription
from alpaca.broker.requests import (
    CreatePortfolioRequest,
    CreateSubscriptionRequest,
    GetPortfoliosRequest,
)
from alpaca.common.enums import BaseURL


def test_create_portfolio(reqmock: Mocker, client: BrokerClient) -> None:
    """Test to create a portfolio."""
    reqmock.post(
        f"{BaseURL.BROKER_SANDBOX.value}/v1/rebalancing/portfolios",
        text="""
        {
            "id": "6819ecd2-db92-4688-821d-8fac2a8f4744",
            "name": "Balanced",
            "description": "A balanced portfolio of stocks and bonds",
            "status": "active",
            "cooldown_days": 7,
            "created_at": "2022-08-06T19:12:13.555858187-04:00",
            "updated_at": "2022-08-06T19:12:13.628551899-04:00",
            "weights": [
                {
                    "type": "cash",
                    "symbol": null,
                    "percent": "5"
                },
                {
                    "type": "asset",
                    "symbol": "SPY",
                    "percent": "60"
                },
                {
                    "type": "asset",
                    "symbol": "TLT",
                    "percent": "35"
                }
            ],
            "rebalance_conditions": [
                {
                    "type": "drift_band",
                    "sub_type": "absolute",
                    "percent": "5",
                    "day": null
                },
                {
                    "type": "drift_band",
                    "sub_type": "relative",
                    "percent": "20",
                    "day": null
                }
            ]
        }
        """,
    )

    portfolio_request = CreatePortfolioRequest(
        **{
            "name": "Balanced",
            "description": "A balanced portfolio of stocks and bonds",
            "weights": [
                {"type": "cash", "percent": "5"},
                {"type": "asset", "symbol": "SPY", "percent": "60"},
                {"type": "asset", "symbol": "TLT", "percent": "35"},
            ],
            "cooldown_days": 7,
            "rebalance_conditions": [
                {"type": "drift_band", "sub_type": "absolute", "percent": "5"},
                {"type": "drift_band", "sub_type": "relative", "percent": "20"},
            ],
        }
    )
    ptf = client.create_portfolio(portfolio_request)

    assert reqmock.called_once
    assert isinstance(ptf, Portfolio)


def test_get_all_portfolios(reqmock: Mocker, client: BrokerClient) -> None:
    """Test the get_all_portfolios method."""
    reqmock.get(
        f"{BaseURL.BROKER_SANDBOX.value}/v1/rebalancing/portfolios",
        text="""
        [
    {
        "id": "57d4ec79-9658-4916-9eb1-7c672be97e3e",
        "name": "My Portfolio",
        "description": "Some description",
        "status": "active",
        "cooldown_days": 2,
        "created_at": "2022-07-28T20:33:59.665962Z",
        "updated_at": "2022-07-28T20:33:59.786528Z",
        "weights": [
            {
                "type": "asset",
                "symbol": "AAPL",
                "percent": "35"
            },
            {
                "type": "asset",
                "symbol": "TSLA",
                "percent": "20"
            },
            {
                "type": "asset",
                "symbol": "SPY",
                "percent": "45"
            }
        ],
        "rebalance_conditions": [
            {
                "type": "drift_band",
                "sub_type": "absolute",
                "percent": "5",
                "day": null
            },
            {
                "type": "drift_band",
                "sub_type": "relative",
                "percent": "20",
                "day": null
            }
        ]
    },
    {
        "id": "6819ecd2-db92-4688-821d-8fac2a8f4744",
        "name": "Balanced",
        "description": "A balanced portfolio of stocks and bonds",
        "status": "active",
        "cooldown_days": 7,
        "created_at": "2022-08-06T23:12:13.555858Z",
        "updated_at": "2022-08-06T23:12:13.628551Z",
        "weights": [
            {
                "type": "cash",
                "symbol": null,
                "percent": "5"
            },
            {
                "type": "asset",
                "symbol": "SPY",
                "percent": "60"
            },
            {
                "type": "asset",
                "symbol": "TLT",
                "percent": "35"
            }
        ],
        "rebalance_conditions": [
            {
                "type": "drift_band",
                "sub_type": "absolute",
                "percent": "5",
                "day": null
            },
            {
                "type": "drift_band",
                "sub_type": "relative",
                "percent": "20",
                "day": null
            }
        ]
    },
    {
        "id": "2d49d00e-ab1c-4014-89d8-70c5f64df2fc",
        "name": "Balanced Two",
        "description": "A balanced portfolio of stocks and bonds",
        "status": "active",
        "cooldown_days": 7,
        "created_at": "2022-08-07T18:56:45.116867Z",
        "updated_at": "2022-08-07T18:56:45.196857Z",
        "weights": [
            {
                "type": "cash",
                "symbol": null,
                "percent": "5"
            },
            {
                "type": "asset",
                "symbol": "SPY",
                "percent": "60"
            },
            {
                "type": "asset",
                "symbol": "TLT",
                "percent": "35"
            }
        ],
        "rebalance_conditions": [
            {
                "type": "drift_band",
                "sub_type": "absolute",
                "percent": "5",
                "day": null
            },
            {
                "type": "drift_band",
                "sub_type": "relative",
                "percent": "20",
                "day": null
            }
        ]
    }
]
        """,
    )
    response = client.get_all_portfolios(filter=GetPortfoliosRequest())

    assert reqmock.called_once
    assert len(response) > 0
    assert isinstance(response[0], Portfolio)


def test_create_subscription(reqmock: Mocker, client: BrokerClient) -> None:
    """Test to create a portfolio subscription."""
    reqmock.post(
        f"{BaseURL.BROKER_SANDBOX.value}/v1/rebalancing/subscriptions",
        text="""
            {
                "id": "2ded098b-ee17-4f48-9496-f8b66e3627aa",
                "account_id": "bf2b0f93-f296-4276-a9cf-288586cf4fb7",
                "portfolio_id": "57d4ec79-9658-4916-9eb1-7c672be97e3e",
                "last_rebalanced_at": null,
                "created_at": "2022-08-06T19:34:43.428080852-04:00"
            }
        """,
    )
    subscription_request = CreateSubscriptionRequest(
        **{
            "account_id": "bf2b0f93-f296-4276-a9cf-288586cf4fb7",
            "portfolio_id": "57d4ec79-9658-4916-9eb1-7c672be97e3e",
        }
    )
    subscription = client.create_subscription(subscription_request)

    assert reqmock.called_once
    assert isinstance(subscription, Subscription)
