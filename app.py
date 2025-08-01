"""
Vercel deployment entry point for Financial CRM System
"""
from financial_crm_system import app

# Vercel expects the Flask app to be available at the module level
if __name__ == '__main__':
    app.run()