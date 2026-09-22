# Rota IA — Copiloto de Diagnóstico e Co-desenho

MVP demonstrativo para apoiar facilitadores na qualificação de casos de IA em governos locais.

## O que mudou nesta versão
A classificação crítica continua baseada em **regras explícitas e auditáveis**.

Foi adicionada uma **camada generativa opcional** que, a partir de:
- relato livre do facilitador;
- campos estruturados já preenchidos;
- lacunas detectadas pelas regras;
- estágio metodológico sugerido;

gera um roteiro contextual para a próxima reunião:
- objetivo;
- pergunta de abertura;
- 5 a 7 perguntas não redundantes;
- explicação de por que cada pergunta importa;
- decisão que a conversa deve permitir;
- cuidado metodológico para o facilitador.

A IA **não altera** o estágio, a prioridade de atenção ou as regras críticas.

## Rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Configurar a camada generativa

### Opção A — mais simples para teste local
Cole temporariamente sua Gemini API key no campo protegido da barra lateral.

### Opção B — recomendada para publicação
Crie:

`.streamlit/secrets.toml`

com:

```toml
GEMINI_API_KEY = "sua_chave"
GEMINI_MODEL = "gemini-2.5-flash-lite"
```

Use `secrets.toml.example` como modelo.

**Nunca suba sua chave real para o GitHub.**

## Publicar no Streamlit Community Cloud

1. Crie um repositório no GitHub.
2. Envie:
   - `app.py`
   - `generative.py`
   - `requirements.txt`
   - `.gitignore`
   - `README.md`
3. No Streamlit Community Cloud, crie o app apontando para `app.py`.
4. Em **App settings > Secrets**, adicione:

```toml
GEMINI_API_KEY = "sua_chave"
GEMINI_MODEL = "gemini-2.5-flash-lite"
```

## Arquitetura

```text
RELATO LIVRE
    ↓
CAMPOS ESTRUTURADOS
    ↓
REGRAS EXPLÍCITAS
(estágio, atenção, lacunas)
    ↓
CAMADA GENERATIVA
(perguntas e roteiro contextual)
    ↓
FACILITADOR
(decisão humana e condução da reunião)
```

## Princípio de segurança do desenho
Não inserir dados pessoais, sensíveis, prontuários, documentos sigilosos ou informações confidenciais no protótipo.
