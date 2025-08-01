# CRM Web WhatsApp - Sistema CRM Financeiro

Este é um Sistema CRM Financeiro completo com integração WhatsApp, desenvolvido em Python Flask para gerenciar clientes, transações financeiras e comunicação via WhatsApp.

## 🚀 Funcionalidades

- **Gestão de Clientes**: Cadastro, edição e visualização de clientes
- **Controle Financeiro**: Registro de transações, pagamentos e cobranças
- **Integração WhatsApp**: Envio de mensagens e lembretes de pagamento
  - **WhatsApp Business API**: Integração oficial do Meta/Facebook
  - **WhatsApp Pessoal**: Use seu próprio WhatsApp via API personalizada
- **Dashboard**: Resumo financeiro e métricas em tempo real
- **API REST**: Endpoints para integração com outros sistemas
- **Interface Web**: Dashboard intuitivo para gerenciamento

## 🛠️ Tecnologias

- Python 3.8+
- Flask (Framework Web)
- SQLite (Banco de Dados)
- WhatsApp Business API
- HTML/CSS (Interface)

## 📦 Instalação Local

1. Clone o repositório:
```bash
git clone https://github.com/rafaelks1020/crm-web-whatsapp.git
cd crm-web-whatsapp
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

4. Execute a aplicação:
```bash
python financial_crm_system.py
```

A aplicação estará disponível em: http://localhost:5000

## ☁️ Deploy no Vercel

Este projeto está configurado para deploy automático no Vercel:

1. Faça fork deste repositório
2. Conecte sua conta Vercel ao GitHub
3. Importe o projeto no Vercel
4. Configure as variáveis de ambiente no painel do Vercel
5. O deploy será feito automaticamente

### Variáveis de Ambiente para Vercel

Configure as seguintes variáveis no painel do Vercel:

**WhatsApp Business API:**
- `WHATSAPP_API_URL`: URL da API do WhatsApp Business
- `WHATSAPP_ACCESS_TOKEN`: Token de acesso do WhatsApp
- `WHATSAPP_PHONE_NUMBER_ID`: ID do número de telefone
- `WHATSAPP_VERIFY_TOKEN`: Token de verificação do webhook

**WhatsApp Pessoal:**
- `WHATSAPP_PROVIDER`: Define o provedor (`business` ou `personal`)
- `PERSONAL_WHATSAPP_API_URL`: URL da sua API WhatsApp pessoal
- `PERSONAL_WHATSAPP_API_KEY`: Chave da sua API WhatsApp pessoal

## 📡 API Endpoints

### Clientes
- `GET /api/customers` - Lista todos os clientes
- `POST /api/customers` - Cria novo cliente
- `GET /api/customers/{id}` - Obtém cliente específico

### Transações
- `POST /api/transactions` - Cria nova transação
- `GET /api/customers/{id}/transactions` - Lista transações do cliente

### WhatsApp
- `POST /api/whatsapp/send` - Envia mensagem
- `POST /api/whatsapp/reminder` - Envia lembrete de pagamento
- `GET /api/whatsapp/status` - Status do provedor WhatsApp
- `POST /webhook/whatsapp` - Webhook para receber mensagens

### Relatórios
- `GET /api/summary` - Resumo financeiro

## 📊 Exemplos de Uso da API

### Criar Cliente
```bash
curl -X POST http://localhost:5000/api/customers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "phone": "5511999999999",
    "email": "joao@email.com",
    "credit_limit": 1000.00
  }'
```

### Criar Transação
```bash
curl -X POST http://localhost:5000/api/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "amount": 250.00,
    "transaction_type": "payment",
    "description": "Pagamento de fatura"
  }'
```

### Verificar Status do WhatsApp
```bash
curl -X GET http://localhost:5000/api/whatsapp/status
```

### Enviar Mensagem WhatsApp
```bash
curl -X POST http://localhost:5000/api/whatsapp/send \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "message": "Olá! Seu pagamento foi confirmado."
  }'
```

## 🔧 Configuração do WhatsApp

### WhatsApp Business API

1. Crie uma conta no Facebook Business
2. Configure o WhatsApp Business API
3. Obtenha o Access Token e Phone Number ID
4. Configure o webhook para receber mensagens
5. Adicione as credenciais no arquivo `.env`

### WhatsApp Pessoal

Para usar seu próprio WhatsApp (recomendado):

1. Configure `WHATSAPP_PROVIDER=personal` no arquivo `.env`
2. Implemente sua própria API WhatsApp ou use o modo simulação
3. Configure `PERSONAL_WHATSAPP_API_URL` e `PERSONAL_WHATSAPP_API_KEY`
4. Veja o arquivo [WHATSAPP_PERSONAL_GUIDE.md](WHATSAPP_PERSONAL_GUIDE.md) para instruções detalhadas

**Bibliotecas recomendadas para WhatsApp pessoal:**
- Node.js: `whatsapp-web.js`
- Python: `selenium` + `webdriver-manager`
- APIs prontas: Várias soluções open source disponíveis

## 🗄️ Estrutura do Banco de Dados

### Tabela Customers
- id, name, phone, email, whatsapp_id
- created_at, status, credit_limit, current_balance

### Tabela Transactions
- id, customer_id, amount, transaction_type
- description, status, created_at, processed_at

### Tabela WhatsApp Messages
- id, customer_id, message_type, content
- direction, status, created_at

## 🔒 Segurança

- Para produção, implemente autenticação adequada
- Use HTTPS para todas as comunicações
- Proteja as credenciais da API do WhatsApp
- Valide todas as entradas de dados

## 🤝 Contribuição

1. Faça fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## 📞 Suporte

Para suporte e dúvidas, abra uma issue no GitHub ou entre em contato.

---

Desenvolvido com ❤️ para gerenciamento financeiro e comunicação eficiente via WhatsApp.
