#!/usr/bin/env python3
"""
Test script for Personal WhatsApp integration
Tests the new personal WhatsApp provider functionality
"""

import os
import sys
import json

def test_personal_whatsapp():
    """Test the personal WhatsApp functionality"""
    print("🧪 Testing Personal WhatsApp Integration")
    print("=" * 50)
    
    # Set environment to use personal WhatsApp
    os.environ['WHATSAPP_PROVIDER'] = 'personal'
    
    # Import the system
    try:
        from financial_crm_system import FinancialCRMSystem
        crm = FinancialCRMSystem()
        print("✅ CRM system imported and initialized with personal WhatsApp")
    except Exception as e:
        print(f"❌ Failed to import CRM system: {e}")
        return False
    
    # Test WhatsApp status
    print("\n📱 Testing WhatsApp Provider Status")
    status_result = crm.get_whatsapp_status()
    if status_result['success']:
        print(f"✅ WhatsApp provider: {status_result['provider']}")
        print(f"✅ Provider type: {status_result['provider_type']}")
        print(f"✅ Configured: {status_result['configured']}")
    else:
        print("❌ Failed to get WhatsApp status")
        return False
    
    # Create a test customer for WhatsApp testing
    print("\n👤 Creating test customer for WhatsApp")
    customer_data = {
        'name': 'João WhatsApp Test',
        'phone': '5511999887766',
        'email': 'joao.whatsapp@test.com',
        'credit_limit': 1500.0
    }
    
    result = crm.create_customer(customer_data)
    if result['success']:
        customer_id = result['customer_id']
        print(f"✅ Test customer created with ID: {customer_id}")
    else:
        print(f"❌ Failed to create test customer: {result.get('error')}")
        return False
    
    # Test personal WhatsApp message sending
    print("\n📤 Testing Personal WhatsApp Message Sending")
    message_result = crm.send_whatsapp_message(customer_id, "Olá! Esta é uma mensagem de teste do seu CRM usando WhatsApp pessoal.")
    
    if message_result['success']:
        print("✅ Personal WhatsApp message sent successfully")
        print(f"   Provider: {message_result.get('provider', 'unknown')}")
        if 'note' in message_result:
            print(f"   Note: {message_result['note']}")
        if 'phone' in message_result:
            print(f"   Phone: {message_result['phone']}")
    else:
        print(f"❌ Failed to send personal WhatsApp message: {message_result.get('error')}")
        return False
    
    # Test payment reminder via personal WhatsApp
    print("\n💰 Testing Payment Reminder via Personal WhatsApp")
    
    # First create a charge to test reminder
    charge_data = {
        'customer_id': customer_id,
        'amount': 250.0,
        'transaction_type': 'charge',
        'description': 'Test charge for WhatsApp reminder'
    }
    
    charge_result = crm.create_transaction(charge_data)
    if charge_result['success']:
        print("✅ Test charge created for reminder")
    else:
        print(f"❌ Failed to create test charge: {charge_result.get('error')}")
        return False
    
    # Send payment reminder
    reminder_result = crm.send_payment_reminder(customer_id, 250.0)
    if reminder_result['success']:
        print("✅ Payment reminder sent via personal WhatsApp")
        print(f"   Provider: {reminder_result.get('provider', 'unknown')}")
    else:
        print(f"❌ Failed to send payment reminder: {reminder_result.get('error')}")
        return False
    
    # Test template message functionality
    print("\n📋 Testing Template Messages via Personal WhatsApp")
    
    # Get the WhatsApp provider directly to test template
    whatsapp_provider = crm.whatsapp
    template_result = whatsapp_provider.send_template_message(
        "+5511999887766", 
        "welcome",
        [{"type": "body", "parameters": [{"text": "João"}]}]
    )
    
    if template_result['success']:
        print("✅ Template message sent via personal WhatsApp")
        print(f"   Provider: {template_result.get('provider', 'unknown')}")
    else:
        print(f"❌ Failed to send template message: {template_result.get('error')}")
        return False
    
    print("\n🎉 All personal WhatsApp tests completed successfully!")
    return True

def test_business_whatsapp():
    """Test business WhatsApp for comparison"""
    print("\n🧪 Testing Business WhatsApp Integration (for comparison)")
    print("=" * 50)
    
    # Set environment to use business WhatsApp
    os.environ['WHATSAPP_PROVIDER'] = 'business'
    
    # Import the system
    try:
        from financial_crm_system import FinancialCRMSystem
        crm_business = FinancialCRMSystem()
        print("✅ CRM system initialized with business WhatsApp")
    except Exception as e:
        print(f"❌ Failed to import CRM system: {e}")
        return False
    
    # Test WhatsApp status
    status_result = crm_business.get_whatsapp_status()
    if status_result['success']:
        print(f"✅ WhatsApp provider: {status_result['provider']}")
        print(f"✅ Provider type: {status_result['provider_type']}")
        print(f"✅ Configured: {status_result['configured']}")
        
        if not status_result['configured']:
            print("ℹ️  Business WhatsApp not configured (expected - no credentials)")
    else:
        print("❌ Failed to get WhatsApp status")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Starting Personal WhatsApp Integration Tests")
    
    # Change to the project directory
    os.chdir('/home/runner/work/crm-web-whatsapp/crm-web-whatsapp')
    
    # Test personal WhatsApp
    if test_personal_whatsapp():
        # Test business WhatsApp for comparison
        test_business_whatsapp()
        
        print("\n" + "=" * 50)
        print("🎯 Personal WhatsApp integration tests completed!")
        print("📋 Summary of personal WhatsApp features:")
        print("   ✅ Personal WhatsApp provider implementation")
        print("   ✅ Message sending via personal API")
        print("   ✅ Payment reminders via personal WhatsApp")
        print("   ✅ Template message support")
        print("   ✅ Provider status checking")
        print("   ✅ Configurable via environment variables")
        print("   ✅ Fallback simulation mode")
        print("   ✅ Integration with existing CRM API")
        print("\n🚀 Ready for personal WhatsApp integration!")
    else:
        print("\n❌ Personal WhatsApp tests failed. Please check the implementation.")
        sys.exit(1)