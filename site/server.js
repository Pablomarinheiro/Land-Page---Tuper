// 1. Importar as bibliotecas necessárias
require('dotenv').config(); // Carrega as variáveis do arquivo .env
const express = require('express');
const fetch = require('node-fetch'); // Precisaremos instalar isso

const app = express();
const port = 3000;

// 2. Permitir que o servidor receba JSON
app.use(express.json());
// Servir os arquivos estáticos (como o seu index.html)
app.use(express.static('.')); 

// 3. Criar a rota "intermediária"
app.post('/api/chat', async (req, res) => {
  const API_KEY = process.env.API_KEY;
  const MODEL_NAME = "gemini-2.5-pro"; // Verifique o nome do modelo que você quer usar
  const API_URL = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL_NAME}:generateContent?key=${API_KEY}`;
  
  try {
    const apiResponse = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req.body) // Repassa o corpo da requisição do frontend
    });

    if (!apiResponse.ok) {
      const errorData = await apiResponse.json();
      // Não envie a chave de API de volta no erro!
      console.error("Erro da API do Google:", errorData);
      return res.status(apiResponse.status).json({ message: "Erro ao contatar a API externa." });
    }

    const data = await apiResponse.json();
    res.json(data); // Envia a resposta de volta para o frontend

  } catch (error) {
    console.error('Erro no servidor:', error);
    res.status(500).json({ message: 'Erro interno no servidor.' });
  }
});

// 4. Iniciar o servidor
app.listen(port, () => {
  console.log(`Servidor rodando em http://localhost:${port}`);
});