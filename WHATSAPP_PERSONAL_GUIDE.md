# Integração WhatsApp Pessoal - Guia de Configuração

Este guia explica como configurar e usar a integração com WhatsApp pessoal no Sistema CRM Financeiro.

## 🔧 Configuração do WhatsApp Pessoal

### 1. Configuração via Variáveis de Ambiente

Configure as seguintes variáveis no arquivo `.env`:

```bash
# Configuração do Provedor WhatsApp
WHATSAPP_PROVIDER=personal  # Define como provedor principal

# API WhatsApp Pessoal (opcional - para integração com sua própria API)
PERSONAL_WHATSAPP_API_URL=https://sua-api-whatsapp.com/send
PERSONAL_WHATSAPP_API_KEY=sua_chave_api_aqui

# Configurações de timeout
WHATSAPP_WEB_TIMEOUT=30
WHATSAPP_WEB_WAIT_TIME=10
```

### 2. Opções de Integração

O sistema suporta diferentes formas de integração com WhatsApp pessoal:

#### Opção A: API Própria (Recomendado para Produção)
- Configure `PERSONAL_WHATSAPP_API_URL` com sua API
- Configure `PERSONAL_WHATSAPP_API_KEY` com sua chave
- O sistema enviará requisições POST para sua API

#### Opção B: Modo Simulação (Para Desenvolvimento)
- Deixe as configurações de API vazias
- O sistema simulará o envio das mensagens
- Útil para testes e desenvolvimento

## 📱 Uso da API

### Verificar Status do WhatsApp

```bash
curl -X GET http://localhost:5000/api/whatsapp/status
```

Resposta:
```json
{
  "success": true,
  "provider": "PersonalWhatsAppProvider",
  "provider_type": "personal",
  "configured": true
}
```

### Enviar Mensagem

```bash
curl -X POST http://localhost:5000/api/whatsapp/send \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "message": "Olá! Esta é uma mensagem do seu CRM."
  }'
```

### Enviar Lembrete de Pagamento

```bash
curl -X POST http://localhost:5000/api/whatsapp/reminder \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "amount": 150.00
  }'
```

## 🔌 Implementação de API Própria

Para integrar com sua própria API de WhatsApp, sua API deve aceitar requisições POST com o seguinte formato:

### Endpoint da Sua API
```
POST https://sua-api-whatsapp.com/send
```

### Headers
```
Authorization: Bearer sua_chave_api_aqui
Content-Type: application/json
```

### Payload
```json
{
  "phone": "+5511999999999",
  "message": "Texto da mensagem",
  "type": "text"
}
```

### Resposta Esperada
```json
{
  "success": true,
  "message_id": "msg_12345",
  "status": "sent"
}
```

## 📋 Bibliotecas Recomendadas

Para implementar sua própria API de WhatsApp, você pode usar:

### Node.js
```bash
npm install whatsapp-web.js
npm install qrcode-terminal
```

### Python
```bash
pip install selenium
pip install webdriver-manager
```

### Outras Opções
- **whatsapp-python**: Wrapper Python para WhatsApp Web
- **whatsapp-api**: APIs open source para WhatsApp
- **Twilio WhatsApp API**: Solução comercial (se permitido)

## 🚀 Exemplo de Implementação (Node.js)

Aqui está um exemplo básico de como implementar uma API WhatsApp usando Node.js:

```javascript
const { Client } = require('whatsapp-web.js');
const express = require('express');
const qrcode = require('qrcode-terminal');

const app = express();
app.use(express.json());

const client = new Client();

client.on('qr', (qr) => {
    qrcode.generate(qr, {small: true});
});

client.on('ready', () => {
    console.log('WhatsApp Client is ready!');
});

app.post('/send', async (req, res) => {
    const { phone, message } = req.body;
    
    try {
        const chatId = phone.includes('@c.us') ? phone : `${phone}@c.us`;
        await client.sendMessage(chatId, message);
        
        res.json({
            success: true,
            message_id: `msg_${Date.now()}`,
            status: 'sent'
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

app.listen(3000, () => {
    console.log('WhatsApp API running on port 3000');
});

client.initialize();
```

## 🔄 Alternando Entre Provedores

Você pode alternar entre WhatsApp Business e Personal definindo a variável:

```bash
# Para WhatsApp Pessoal
WHATSAPP_PROVIDER=personal

# Para WhatsApp Business
WHATSAPP_PROVIDER=business
```

## 🛠️ Troubleshooting

### Problema: Mensagens não são enviadas
- Verifique se `PERSONAL_WHATSAPP_API_URL` está correto
- Verifique se `PERSONAL_WHATSAPP_API_KEY` está válida
- Verifique os logs do sistema

### Problema: API não responde
- Verifique se sua API WhatsApp está rodando
- Teste a API diretamente com curl
- Verifique as configurações de timeout

### Problema: Formato de telefone
- O sistema automaticamente adiciona +55 para números brasileiros
- Use o formato internacional: +5511999999999

## 📞 Suporte

Para mais informações sobre a integração WhatsApp pessoal:
1. Verifique os logs do sistema
2. Teste com o modo simulação primeiro
3. Implemente sua API gradualmente
4. Use a API de status para monitorar a conexão

---

Esta integração permite que você use seu próprio WhatsApp com total controle sobre as mensagens enviadas pelo seu CRM.