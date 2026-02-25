"""
Test script for n8n-compatible APIs

Demonstrates both random number and enrollment prediction APIs
locally before deploying to Posit Connect.

Usage:
    uv run python test_n8n_apis.py
"""

import requests
import json
import time


def test_random_number_api():
    """Test the random number generator API."""
    print("=" * 70)
    print("Testing Random Number Generator API")
    print("=" * 70)

    url = "http://localhost:8000/model"
    headers = {"Content-Type": "application/json"}

    # Test 1: Basic request
    print("\n1. Basic request (min=1, max=100)...")
    payload = {"data": {"min": 1, "max": 100}}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()

        print(f"   Status: {response.status_code}")
        print(f"   Number: {result['result']['number']}")
        print(f"   Timing: {result['timing']['model_time_ms']}ms")
        print(f"   Platform: {result['release']['harness_version']}")
        print("   ✓ Test passed")
    except requests.exceptions.ConnectionError:
        print("   ✗ Connection error - is the API running?")
        print("   Start with: uv run python n8n_demo_api.py")
        return False
    except Exception as e:
        print(f"   ✗ Test failed: {e}")
        return False

    # Test 2: Different range
    print("\n2. Different range (min=1000, max=2000)...")
    payload = {"data": {"min": 1000, "max": 2000}}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()

        number = result['result']['number']
        print(f"   Number: {number}")

        # Validate range
        if 1000 <= number <= 2000:
            print("   ✓ Number in expected range")
        else:
            print(f"   ✗ Number outside range: {number}")
            return False
    except Exception as e:
        print(f"   ✗ Test failed: {e}")
        return False

    # Test 3: Health check
    print("\n3. Health check...")
    try:
        response = requests.get("http://localhost:8000/health")
        response.raise_for_status()
        health = response.json()

        print(f"   Status: {health['status']}")
        print(f"   Service: {health['service']}")
        print("   ✓ Health check passed")
    except Exception as e:
        print(f"   ✗ Test failed: {e}")
        return False

    print("\n" + "=" * 70)
    print("✓ All Random Number API tests passed!")
    print("=" * 70)
    return True


def test_enrollment_api():
    """Test the enrollment prediction API."""
    print("\n" + "=" * 70)
    print("Testing Clinical Trial Enrollment Prediction API")
    print("=" * 70)

    url = "http://localhost:8001/model"
    headers = {"Content-Type": "application/json"}

    # Test 1: High-performing site
    print("\n1. High-performing site prediction...")
    payload = {
        "data": {
            "phase": "Phase II",
            "therapeutic_area": "Oncology",
            "country": "USA",
            "site_type": "Academic Medical Center",
            "investigator_experience_years": 20,
            "site_staff_count": 25,
            "prior_trials_completed": 30,
            "patient_database_size": 20000,
            "target_per_site": 50
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()

        print(f"   Status: {response.status_code}")
        print(f"   Probability: {result['result']['success_probability']*100:.1f}%")
        print(f"   Prediction: {result['result']['prediction']}")
        print(f"   Risk Level: {result['result']['risk_level']}")
        print(f"   Timing: {result['timing']['model_time_ms']}ms")
        print("   ✓ Test passed")
    except requests.exceptions.ConnectionError:
        print("   ✗ Connection error - is the API running?")
        print("   Start with: uv run python n8n_enrollment_api.py")
        return False
    except Exception as e:
        print(f"   ✗ Test failed: {e}")
        return False

    # Test 2: Challenging site
    print("\n2. Challenging site prediction...")
    payload = {
        "data": {
            "phase": "Phase III",
            "therapeutic_area": "Neurology",
            "country": "Spain",
            "site_type": "Community Hospital",
            "investigator_experience_years": 3,
            "site_staff_count": 5,
            "prior_trials_completed": 2,
            "patient_database_size": 1000,
            "target_per_site": 200
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()

        print(f"   Probability: {result['result']['success_probability']*100:.1f}%")
        print(f"   Prediction: {result['result']['prediction']}")
        print(f"   Risk Level: {result['result']['risk_level']}")
        print("   ✓ Test passed")
    except Exception as e:
        print(f"   ✗ Test failed: {e}")
        return False

    # Test 3: Health check
    print("\n3. Health check...")
    try:
        response = requests.get("http://localhost:8001/health")
        response.raise_for_status()
        health = response.json()

        print(f"   Status: {health['status']}")
        print(f"   Model Loaded: {health['model_loaded']}")
        print("   ✓ Health check passed")
    except Exception as e:
        print(f"   ✗ Test failed: {e}")
        return False

    print("\n" + "=" * 70)
    print("✓ All Enrollment API tests passed!")
    print("=" * 70)
    return True


def print_deployment_instructions():
    """Print next steps for deployment."""
    print("\n" + "=" * 70)
    print("Next Steps: Deploy to Posit Connect")
    print("=" * 70)

    print("\n1. Configure Posit Connect:")
    print("   rsconnect add --account myaccount --name myserver \\")
    print("     --server https://connect.example.com --api-key YOUR_KEY")

    print("\n2. Deploy Random Number API:")
    print("   rsconnect deploy fastapi --entrypoint n8n_demo_api:app \\")
    print("     --name random-number-api .")

    print("\n3. Deploy Enrollment API:")
    print("   rsconnect deploy fastapi --entrypoint n8n_enrollment_api:app \\")
    print("     --name enrollment-api .")

    print("\n4. Configure n8n:")
    print("   - Get API URL from Posit Connect dashboard")
    print("   - Create API key in Access tab")
    print("   - Update n8n HTTP Request node")
    print("   - Test workflow")

    print("\n📚 Documentation:")
    print("   - Quick Start: N8N-QUICK-START.md")
    print("   - Full Guide: POSIT-CONNECT-DEPLOYMENT.md")

    print("\n" + "=" * 70)


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("n8n API Testing Suite")
    print("=" * 70)

    print("\nThis script tests both APIs locally before deploying to Posit Connect.")
    print("Make sure to start each API in a separate terminal:")
    print("  Terminal 1: uv run python n8n_demo_api.py")
    print("  Terminal 2: uv run python n8n_enrollment_api.py")

    input("\nPress Enter when both APIs are running...")

    # Test random number API
    random_success = test_random_number_api()

    # Test enrollment API
    enrollment_success = test_enrollment_api()

    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Random Number API: {'✓ PASSED' if random_success else '✗ FAILED'}")
    print(f"Enrollment API: {'✓ PASSED' if enrollment_success else '✗ FAILED'}")

    if random_success and enrollment_success:
        print("\n🎉 All tests passed! APIs are ready for deployment.")
        print_deployment_instructions()
    else:
        print("\n⚠️  Some tests failed. Please check the error messages above.")
        print("    Make sure both APIs are running and models are trained.")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
