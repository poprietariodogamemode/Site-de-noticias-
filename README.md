# NexusGG — Notícias de Games 🎮

Site de notícias de jogos e consoles com atualização automática a cada 30 minutos.

## Como hospedar gratuitamente no Render.com

### 1. Suba o projeto no GitHub
1. Crie uma conta em github.com (se não tiver)
2. Crie um repositório novo (ex: `nexusgg`)
3. Faça upload de todos os arquivos desta pasta

### 2. Deploy no Render.com
1. Acesse render.com e crie uma conta gratuita
2. Clique em **"New +"** → **"Web Service"**
3. Conecte seu GitHub e selecione o repositório
4. Preencha:
   - **Name:** nexusgg (qualquer nome)
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** Free
5. Clique em **"Create Web Service"**

Pronto! Em 2-3 minutos o site estará no ar em `https://seu-nome.onrender.com`

## Fontes de notícias incluídas

- IGN (Geral)
- Rock Paper Shotgun (PC)
- Kotaku (Geral)
- Eurogamer (Geral)
- Game Rant (Geral)
- The Gamer (Geral)
- VG247 (Consoles)
- Push Square (PlayStation)
- Pure Xbox (Xbox)
- Nintendo Life (Nintendo)

## Adicionar mais feeds RSS

No arquivo `app.py`, adicione na lista `FEEDS`:
```python
{"url": "https://seusite.com/feed", "categoria": "Geral"},
```

## Aviso sobre plano gratuito

O Render.com no plano free "dorme" o servidor após 15 min sem acesso.
Para manter ativo, use cron-job.org para fazer um ping no seu site a cada 10 minutos (gratuito).
