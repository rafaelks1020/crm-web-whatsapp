"""
Financial CRM System with WhatsApp Integration
Sistema CRM Financeiro com Integração WhatsApp

A comprehensive CRM system for managing financial data and customer relationships
through WhatsApp communication.
"""

import os
import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from flask import Flask, request, jsonify, render_template_string
import requests
from functools import wraps

# Data Models
@dataclass
class Customer:
    """Customer data model"""
    id: Optional[int] = None
    name: str = ""
    phone: str = ""
    email: str = ""
    whatsapp_id: str = ""
    created_at: str = ""
    status: str = "active"  # active, inactive, blocked
    credit_limit: float = 0.0
    current_balance: float = 0.0

@dataclass
class Transaction:
    """Financial transaction data model"""
    id: Optional[int] = None
    customer_id: int = 0
    amount: float = 0.0
    transaction_type: str = ""  # payment, charge, refund, credit
    description: str = ""
    status: str = "pending"  # pending, completed, failed, cancelled
    created_at: str = ""
    processed_at: str = ""

@dataclass
class WhatsAppMessage:
    """WhatsApp message data model"""
    id: Optional[int] = None
    customer_id: int = 0
    message_type: str = ""  # text, media, template
    content: str = ""
    direction: str = ""  # inbound, outbound
    status: str = "sent"  # sent, delivered, read, failed
    created_at: str = ""

class DatabaseManager:
    """Database management for the CRM system"""
    
    def __init__(self, db_path: str = "crm_database.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT UNIQUE NOT NULL,
                email TEXT,
                whatsapp_id TEXT,
                created_at TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                credit_limit REAL DEFAULT 0.0,
                current_balance REAL DEFAULT 0.0
            )
        ''')
        
        # Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                transaction_type TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'pending',
                created_at TEXT NOT NULL,
                processed_at TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        ''')
        
        # WhatsApp messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS whatsapp_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                message_type TEXT NOT NULL,
                content TEXT NOT NULL,
                direction TEXT NOT NULL,
                status TEXT DEFAULT 'sent',
                created_at TEXT NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Any]:
        """Execute a database query and return results"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.commit()
        conn.close()
        return results
    
    def execute_insert(self, query: str, params: tuple = ()) -> int:
        """Execute an insert query and return the last row ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(query, params)
        last_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return last_id

class WhatsAppAPI:
    """WhatsApp Business API integration"""
    
    def __init__(self):
        self.api_url = os.getenv('WHATSAPP_API_URL', '')
        self.access_token = os.getenv('WHATSAPP_ACCESS_TOKEN', '')
        self.phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID', '')
    
    def send_message(self, to: str, message: str, message_type: str = "text") -> Dict:
        """Send a WhatsApp message"""
        if not self.api_url or not self.access_token:
            return {"success": False, "error": "WhatsApp API not configured"}
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": message_type,
            "text": {"body": message}
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/{self.phone_number_id}/messages",
                headers=headers,
                json=payload
            )
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_template_message(self, to: str, template_name: str, components: List = None) -> Dict:
        """Send a WhatsApp template message"""
        if not self.api_url or not self.access_token:
            return {"success": False, "error": "WhatsApp API not configured"}
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": "pt_BR"},
                "components": components or []
            }
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/{self.phone_number_id}/messages",
                headers=headers,
                json=payload
            )
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}

class FinancialCRMSystem:
    """Main Financial CRM System class"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.whatsapp = WhatsAppAPI()
    
    # Customer Management
    def create_customer(self, customer_data: Dict) -> Dict:
        """Create a new customer"""
        try:
            customer = Customer(
                name=customer_data.get('name', ''),
                phone=customer_data.get('phone', ''),
                email=customer_data.get('email', ''),
                whatsapp_id=customer_data.get('whatsapp_id', ''),
                created_at=datetime.now().isoformat(),
                credit_limit=customer_data.get('credit_limit', 0.0)
            )
            
            query = '''
                INSERT INTO customers (name, phone, email, whatsapp_id, created_at, credit_limit)
                VALUES (?, ?, ?, ?, ?, ?)
            '''
            customer_id = self.db.execute_insert(
                query, 
                (customer.name, customer.phone, customer.email, 
                 customer.whatsapp_id, customer.created_at, customer.credit_limit)
            )
            
            return {"success": True, "customer_id": customer_id}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_customer(self, customer_id: int) -> Dict:
        """Get customer by ID"""
        try:
            query = "SELECT * FROM customers WHERE id = ?"
            results = self.db.execute_query(query, (customer_id,))
            
            if results:
                customer_dict = dict(results[0])
                return {"success": True, "customer": customer_dict}
            else:
                return {"success": False, "error": "Customer not found"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_customers(self, status: str = None) -> Dict:
        """Get all customers or filter by status"""
        try:
            if status:
                query = "SELECT * FROM customers WHERE status = ? ORDER BY created_at DESC"
                results = self.db.execute_query(query, (status,))
            else:
                query = "SELECT * FROM customers ORDER BY created_at DESC"
                results = self.db.execute_query(query)
            
            customers = [dict(row) for row in results]
            return {"success": True, "customers": customers}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def update_customer_balance(self, customer_id: int, amount: float, operation: str = "add") -> Dict:
        """Update customer balance"""
        try:
            if operation == "add":
                query = "UPDATE customers SET current_balance = current_balance + ? WHERE id = ?"
            elif operation == "subtract":
                query = "UPDATE customers SET current_balance = current_balance - ? WHERE id = ?"
            else:
                query = "UPDATE customers SET current_balance = ? WHERE id = ?"
            
            self.db.execute_query(query, (amount, customer_id))
            return {"success": True}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # Transaction Management
    def create_transaction(self, transaction_data: Dict) -> Dict:
        """Create a new financial transaction"""
        try:
            transaction = Transaction(
                customer_id=transaction_data.get('customer_id'),
                amount=transaction_data.get('amount', 0.0),
                transaction_type=transaction_data.get('transaction_type', ''),
                description=transaction_data.get('description', ''),
                created_at=datetime.now().isoformat()
            )
            
            query = '''
                INSERT INTO transactions (customer_id, amount, transaction_type, description, created_at)
                VALUES (?, ?, ?, ?, ?)
            '''
            transaction_id = self.db.execute_insert(
                query,
                (transaction.customer_id, transaction.amount, transaction.transaction_type,
                 transaction.description, transaction.created_at)
            )
            
            # Update customer balance based on transaction type
            if transaction.transaction_type == "payment":
                self.update_customer_balance(transaction.customer_id, transaction.amount, "add")
            elif transaction.transaction_type == "charge":
                self.update_customer_balance(transaction.customer_id, transaction.amount, "subtract")
            
            return {"success": True, "transaction_id": transaction_id}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_customer_transactions(self, customer_id: int, limit: int = 50) -> Dict:
        """Get transactions for a specific customer"""
        try:
            query = '''
                SELECT * FROM transactions 
                WHERE customer_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            '''
            results = self.db.execute_query(query, (customer_id, limit))
            transactions = [dict(row) for row in results]
            return {"success": True, "transactions": transactions}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_financial_summary(self, days: int = 30) -> Dict:
        """Get financial summary for the last N days"""
        try:
            since_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            # Total revenue (payments)
            revenue_query = '''
                SELECT SUM(amount) as total_revenue 
                FROM transactions 
                WHERE transaction_type = 'payment' AND created_at >= ?
            '''
            revenue_result = self.db.execute_query(revenue_query, (since_date,))
            total_revenue = revenue_result[0]['total_revenue'] or 0.0
            
            # Total charges
            charges_query = '''
                SELECT SUM(amount) as total_charges 
                FROM transactions 
                WHERE transaction_type = 'charge' AND created_at >= ?
            '''
            charges_result = self.db.execute_query(charges_query, (since_date,))
            total_charges = charges_result[0]['total_charges'] or 0.0
            
            # Transaction count
            count_query = '''
                SELECT COUNT(*) as transaction_count 
                FROM transactions 
                WHERE created_at >= ?
            '''
            count_result = self.db.execute_query(count_query, (since_date,))
            transaction_count = count_result[0]['transaction_count']
            
            # Customer count
            customer_query = "SELECT COUNT(*) as customer_count FROM customers WHERE status = 'active'"
            customer_result = self.db.execute_query(customer_query)
            customer_count = customer_result[0]['customer_count']
            
            return {
                "success": True,
                "summary": {
                    "total_revenue": total_revenue,
                    "total_charges": total_charges,
                    "net_amount": total_revenue - total_charges,
                    "transaction_count": transaction_count,
                    "active_customers": customer_count,
                    "period_days": days
                }
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # WhatsApp Integration
    def send_whatsapp_message(self, customer_id: int, message: str) -> Dict:
        """Send WhatsApp message to customer"""
        try:
            # Get customer info
            customer_result = self.get_customer(customer_id)
            if not customer_result["success"]:
                return customer_result
            
            customer = customer_result["customer"]
            phone = customer.get('phone', '')
            
            if not phone:
                return {"success": False, "error": "Customer phone number not found"}
            
            # Send WhatsApp message
            whatsapp_result = self.whatsapp.send_message(phone, message)
            
            # Log message in database
            if whatsapp_result["success"]:
                query = '''
                    INSERT INTO whatsapp_messages (customer_id, message_type, content, direction, created_at)
                    VALUES (?, ?, ?, ?, ?)
                '''
                self.db.execute_insert(
                    query,
                    (customer_id, "text", message, "outbound", datetime.now().isoformat())
                )
            
            return whatsapp_result
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_payment_reminder(self, customer_id: int, amount: float = None) -> Dict:
        """Send payment reminder via WhatsApp"""
        try:
            customer_result = self.get_customer(customer_id)
            if not customer_result["success"]:
                return customer_result
            
            customer = customer_result["customer"]
            customer_name = customer.get('name', 'Cliente')
            balance = customer.get('current_balance', 0.0)
            
            if balance <= 0:
                message = f"Olá {customer_name}! Sua conta está em dia. Obrigado pela confiança! 😊"
            else:
                if amount:
                    message = f"Olá {customer_name}! Lembrando que você tem um pagamento de R$ {amount:.2f} pendente. Por favor, regularize sua situação."
                else:
                    message = f"Olá {customer_name}! Seu saldo atual é de R$ {balance:.2f}. Por favor, regularize sua situação."
            
            return self.send_whatsapp_message(customer_id, message)
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_customer_messages(self, customer_id: int, limit: int = 50) -> Dict:
        """Get WhatsApp message history for a customer"""
        try:
            query = '''
                SELECT * FROM whatsapp_messages 
                WHERE customer_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            '''
            results = self.db.execute_query(query, (customer_id, limit))
            messages = [dict(row) for row in results]
            return {"success": True, "messages": messages}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

# Flask Web Application
app = Flask(__name__)
crm = FinancialCRMSystem()

def require_auth(f):
    """Simple authentication decorator (for production, use proper authentication)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # For demo purposes, no auth required
        # In production, implement proper authentication
        return f(*args, **kwargs)
    return decorated_function

# Web Interface Routes
@app.route('/')
def index():
    """Main dashboard"""
    summary = crm.get_financial_summary()
    customers = crm.get_customers()
    
    html_template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sistema CRM Financeiro</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { background: #25D366; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
            .card { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
            .metric { text-align: center; }
            .metric-value { font-size: 2em; font-weight: bold; color: #25D366; }
            .metric-label { color: #666; margin-top: 5px; }
            .table { width: 100%; border-collapse: collapse; }
            .table th, .table td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
            .table th { background-color: #f8f9fa; }
            .btn { background: #25D366; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; }
            .btn:hover { background: #128C7E; }
            .status-active { color: #28a745; }
            .status-inactive { color: #dc3545; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 Sistema CRM Financeiro - WhatsApp</h1>
                <p>Gerencie seus clientes e finanças com integração WhatsApp</p>
            </div>
            
            {% if summary.success %}
            <div class="card">
                <h2>Resumo Financeiro (30 dias)</h2>
                <div class="summary-grid">
                    <div class="metric">
                        <div class="metric-value">R$ {{ "%.2f"|format(summary.summary.total_revenue) }}</div>
                        <div class="metric-label">Receita Total</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">R$ {{ "%.2f"|format(summary.summary.total_charges) }}</div>
                        <div class="metric-label">Cobranças Total</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">R$ {{ "%.2f"|format(summary.summary.net_amount) }}</div>
                        <div class="metric-label">Valor Líquido</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{{ summary.summary.transaction_count }}</div>
                        <div class="metric-label">Transações</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{{ summary.summary.active_customers }}</div>
                        <div class="metric-label">Clientes Ativos</div>
                    </div>
                </div>
            </div>
            {% endif %}
            
            <div class="card">
                <h2>Clientes</h2>
                <a href="/customer/new" class="btn">Novo Cliente</a>
                {% if customers.success and customers.customers %}
                <table class="table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nome</th>
                            <th>Telefone</th>
                            <th>Saldo Atual</th>
                            <th>Status</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for customer in customers.customers[:10] %}
                        <tr>
                            <td>{{ customer.id }}</td>
                            <td>{{ customer.name }}</td>
                            <td>{{ customer.phone }}</td>
                            <td>R$ {{ "%.2f"|format(customer.current_balance) }}</td>
                            <td class="status-{{ customer.status }}">{{ customer.status }}</td>
                            <td>
                                <a href="/customer/{{ customer.id }}" class="btn">Ver</a>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <p>Nenhum cliente encontrado.</p>
                {% endif %}
            </div>
            
            <div class="card">
                <h2>API Endpoints</h2>
                <p>Use os seguintes endpoints para integração:</p>
                <ul>
                    <li><strong>GET /api/customers</strong> - Listar clientes</li>
                    <li><strong>POST /api/customers</strong> - Criar cliente</li>
                    <li><strong>GET /api/customers/{id}</strong> - Obter cliente</li>
                    <li><strong>POST /api/transactions</strong> - Criar transação</li>
                    <li><strong>GET /api/summary</strong> - Resumo financeiro</li>
                    <li><strong>POST /api/whatsapp/send</strong> - Enviar mensagem WhatsApp</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    '''
    
    return render_template_string(html_template, summary=summary, customers=customers)

# API Routes
@app.route('/api/customers', methods=['GET', 'POST'])
@require_auth
def api_customers():
    """API endpoint for customers"""
    if request.method == 'GET':
        status = request.args.get('status')
        return jsonify(crm.get_customers(status))
    
    elif request.method == 'POST':
        data = request.get_json()
        return jsonify(crm.create_customer(data))

@app.route('/api/customers/<int:customer_id>', methods=['GET'])
@require_auth
def api_customer(customer_id):
    """API endpoint for specific customer"""
    return jsonify(crm.get_customer(customer_id))

@app.route('/api/transactions', methods=['POST'])
@require_auth
def api_transactions():
    """API endpoint for creating transactions"""
    data = request.get_json()
    return jsonify(crm.create_transaction(data))

@app.route('/api/customers/<int:customer_id>/transactions', methods=['GET'])
@require_auth
def api_customer_transactions(customer_id):
    """API endpoint for customer transactions"""
    limit = request.args.get('limit', 50, type=int)
    return jsonify(crm.get_customer_transactions(customer_id, limit))

@app.route('/api/summary', methods=['GET'])
@require_auth
def api_summary():
    """API endpoint for financial summary"""
    days = request.args.get('days', 30, type=int)
    return jsonify(crm.get_financial_summary(days))

@app.route('/api/whatsapp/send', methods=['POST'])
@require_auth
def api_whatsapp_send():
    """API endpoint for sending WhatsApp messages"""
    data = request.get_json()
    customer_id = data.get('customer_id')
    message = data.get('message')
    
    if not customer_id or not message:
        return jsonify({"success": False, "error": "customer_id and message are required"})
    
    return jsonify(crm.send_whatsapp_message(customer_id, message))

@app.route('/api/whatsapp/reminder', methods=['POST'])
@require_auth
def api_payment_reminder():
    """API endpoint for sending payment reminders"""
    data = request.get_json()
    customer_id = data.get('customer_id')
    amount = data.get('amount')
    
    if not customer_id:
        return jsonify({"success": False, "error": "customer_id is required"})
    
    return jsonify(crm.send_payment_reminder(customer_id, amount))

@app.route('/webhook/whatsapp', methods=['GET', 'POST'])
def whatsapp_webhook():
    """WhatsApp webhook for receiving messages"""
    if request.method == 'GET':
        # Webhook verification
        verify_token = os.getenv('WHATSAPP_VERIFY_TOKEN', 'your_verify_token')
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode == 'subscribe' and token == verify_token:
            return challenge
        else:
            return "Forbidden", 403
    
    elif request.method == 'POST':
        # Handle incoming WhatsApp messages
        data = request.get_json()
        
        # Process webhook data (implement based on WhatsApp Business API docs)
        # This is a placeholder for handling incoming messages
        
        return jsonify({"success": True})

if __name__ == '__main__':
    # For development
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))