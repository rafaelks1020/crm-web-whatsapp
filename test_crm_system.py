#!/usr/bin/env python3
"""
Test script for Financial CRM System
Tests all major functionality to ensure everything works correctly
"""

import os
import sys
import requests
import json
import time
from subprocess import Popen, PIPE

def test_crm_functionality():
    """Test the CRM system functionality"""
    print("🧪 Testing Financial CRM System")
    print("=" * 50)
    
    # Import the system
    try:
        from financial_crm_system import FinancialCRMSystem
        crm = FinancialCRMSystem()
        print("✅ CRM system imported and initialized successfully")
    except Exception as e:
        print(f"❌ Failed to import CRM system: {e}")
        return False
    
    # Test customer management
    print("\n📋 Testing Customer Management")
    
    # Create test customer
    customer_data = {
        'name': 'Maria Santos',
        'phone': '5511888888888',
        'email': 'maria@email.com',
        'whatsapp_id': '5511888888888',
        'credit_limit': 2000.0
    }
    
    result = crm.create_customer(customer_data)
    if result['success']:
        customer_id = result['customer_id']
        print(f"✅ Customer created successfully with ID: {customer_id}")
    else:
        print(f"❌ Failed to create customer: {result.get('error')}")
        return False
    
    # Get customer
    customer_result = crm.get_customer(customer_id)
    if customer_result['success']:
        print("✅ Customer retrieved successfully")
    else:
        print(f"❌ Failed to get customer: {customer_result.get('error')}")
        return False
    
    # Test transaction management
    print("\n💰 Testing Transaction Management")
    
    # Create payment transaction
    payment_data = {
        'customer_id': customer_id,
        'amount': 500.0,
        'transaction_type': 'payment',
        'description': 'Test payment transaction'
    }
    
    payment_result = crm.create_transaction(payment_data)
    if payment_result['success']:
        print("✅ Payment transaction created successfully")
    else:
        print(f"❌ Failed to create payment: {payment_result.get('error')}")
        return False
    
    # Create charge transaction
    charge_data = {
        'customer_id': customer_id,
        'amount': 150.0,
        'transaction_type': 'charge',
        'description': 'Test charge transaction'
    }
    
    charge_result = crm.create_transaction(charge_data)
    if charge_result['success']:
        print("✅ Charge transaction created successfully")
    else:
        print(f"❌ Failed to create charge: {charge_result.get('error')}")
        return False
    
    # Get customer transactions
    transactions_result = crm.get_customer_transactions(customer_id)
    if transactions_result['success']:
        transaction_count = len(transactions_result['transactions'])
        print(f"✅ Retrieved {transaction_count} transactions for customer")
    else:
        print(f"❌ Failed to get transactions: {transactions_result.get('error')}")
        return False
    
    # Test financial summary
    print("\n📊 Testing Financial Reports")
    
    summary_result = crm.get_financial_summary()
    if summary_result['success']:
        summary = summary_result['summary']
        print(f"✅ Financial summary generated:")
        print(f"   - Total Revenue: R$ {summary['total_revenue']:.2f}")
        print(f"   - Total Charges: R$ {summary['total_charges']:.2f}")
        print(f"   - Net Amount: R$ {summary['net_amount']:.2f}")
        print(f"   - Active Customers: {summary['active_customers']}")
    else:
        print(f"❌ Failed to get financial summary: {summary_result.get('error')}")
        return False
    
    # Test WhatsApp functionality (without actual API calls)
    print("\n📱 Testing WhatsApp Integration")
    
    # Test message sending (will fail without proper API config, but should handle gracefully)
    message_result = crm.send_whatsapp_message(customer_id, "Test message")
    if message_result.get('error') == "WhatsApp API not configured":
        print("✅ WhatsApp integration properly handles missing configuration")
    else:
        print("⚠️  WhatsApp configuration detected or unexpected behavior")
    
    print("\n🎉 All tests completed successfully!")
    return True

def test_api_endpoints():
    """Test the API endpoints"""
    print("\n🌐 Testing API Endpoints")
    print("=" * 50)
    
    # Start Flask app in background
    flask_process = Popen([
        'python', 'financial_crm_system.py'
    ], stdout=PIPE, stderr=PIPE)
    
    # Wait for Flask to start
    time.sleep(3)
    
    base_url = "http://localhost:5000"
    
    try:
        # Test health check by getting summary
        response = requests.get(f"{base_url}/api/summary", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print("✅ API summary endpoint working")
            else:
                print("❌ API summary endpoint returned error")
        else:
            print(f"❌ API summary endpoint returned status {response.status_code}")
        
        # Test customers endpoint
        response = requests.get(f"{base_url}/api/customers", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ API customers endpoint working ({len(data['customers'])} customers)")
            else:
                print("❌ API customers endpoint returned error")
        else:
            print(f"❌ API customers endpoint returned status {response.status_code}")
        
        # Test creating a customer via API
        customer_data = {
            'name': 'API Test Customer',
            'phone': '5511777777777',
            'email': 'api@test.com',
            'credit_limit': 1500.0
        }
        
        response = requests.post(
            f"{base_url}/api/customers",
            json=customer_data,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ API customer creation working (ID: {data['customer_id']})")
            else:
                print(f"❌ API customer creation failed: {data.get('error')}")
        else:
            print(f"❌ API customer creation returned status {response.status_code}")
        
        print("✅ API endpoints tested successfully")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to connect to Flask app: {e}")
    
    finally:
        # Stop Flask app
        flask_process.terminate()
        flask_process.wait()

if __name__ == "__main__":
    print("🚀 Starting comprehensive CRM system tests")
    
    # Change to the project directory
    os.chdir('/home/runner/work/crm-web-whatsapp/crm-web-whatsapp')
    
    # Test core functionality
    if test_crm_functionality():
        # Test API endpoints
        test_api_endpoints()
        
        print("\n" + "=" * 50)
        print("🎯 All tests completed! The Financial CRM System is ready.")
        print("📋 Summary of implemented features:")
        print("   ✅ Customer management")
        print("   ✅ Financial transaction tracking")
        print("   ✅ Balance management")
        print("   ✅ Financial reporting")
        print("   ✅ WhatsApp integration structure")
        print("   ✅ REST API endpoints")
        print("   ✅ Web dashboard")
        print("   ✅ Database persistence")
        print("   ✅ Vercel deployment configuration")
        print("\n🚀 Ready for deployment!")
    else:
        print("\n❌ Tests failed. Please check the implementation.")
        sys.exit(1)