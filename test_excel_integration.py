"""Test script for Excel integration functions."""

import json
from pathlib import Path
from excel_integration import (
    KICKSTARTER_SUCCESS_PROBABILITY,
    KICKSTARTER_SUCCESS_SUMMARY,
)

# Test campaigns
TEST_CAMPAIGNS = [
    {
        "name": "Well-Funded Tech Campaign",
        "data": {
            "goal": 50000,
            "pledged": 75000,
            "backers": 1250,
            "usd pledged": 75000,
            "category": "Technology",
            "main_category": "Technology",
            "currency": "USD",
            "country": "US",
            "deadline": "2024-12-31",
            "launched": "2024-09-01",
        },
    },
    {
        "name": "Underfunded Music Campaign",
        "data": {
            "goal": 100000,
            "pledged": 25000,
            "backers": 150,
            "usd pledged": 25000,
            "category": "Music",
            "main_category": "Music",
            "currency": "USD",
            "country": "US",
            "deadline": "2024-12-31",
            "launched": "2024-11-01",
        },
    },
    {
        "name": "Moderately Funded Film Campaign",
        "data": {
            "goal": 10000,
            "pledged": 8000,
            "backers": 85,
            "usd pledged": 8000,
            "category": "Film",
            "main_category": "Film",
            "currency": "USD",
            "country": "UK",
            "deadline": "2024-12-25",
            "launched": "2024-10-15",
        },
    },
]


def test_excel_functions():
    """Test all Excel integration functions."""
    print("=" * 80)
    print("EXCEL INTEGRATION TEST SUITE")
    print("=" * 80)
    print()

    for i, campaign in enumerate(TEST_CAMPAIGNS, 1):
        print(f"Test Case {i}: {campaign['name']}")
        print("-" * 80)

        # Convert campaign data to JSON string (as it would be in Excel)
        campaign_json = json.dumps(campaign["data"])

        try:
            # Test KICKSTARTER_SUCCESS_PROBABILITY
            probability = KICKSTARTER_SUCCESS_PROBABILITY(
                campaign_json, model_dir="./artifacts"
            )
            print(f"  Campaign JSON: {campaign_json[:50]}...")
            print(f"  Probability: {probability:.6f}")
            print(f"  Percentage: {probability * 100:.2f}%")

            # Test KICKSTARTER_SUCCESS_SUMMARY
            summary = KICKSTARTER_SUCCESS_SUMMARY(
                campaign_json, model_dir="./artifacts"
            )
            print(f"  Summary: {summary}")
            print()

        except Exception as e:
            print(f"  ❌ ERROR: {str(e)}")
            print()

    print("=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    test_excel_functions()
