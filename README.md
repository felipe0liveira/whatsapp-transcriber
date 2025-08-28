# WhatsApp Transcriber

Um script Python para transcrever mensagens de áudio do WhatsApp usando OpenAI Whisper.

## 📝 Descrição

Este projeto permite transcrever automaticamente mensagens de áudio de conversas exportadas do WhatsApp. O script:

- Extrai arquivos ZIP exportados do WhatsApp
- Identifica mensagens de áudio (.opus)
- Transcreve o áudio usando o modelo Whisper da OpenAI
- Integra as transcrições no histórico da conversa
- Gera um arquivo final com o chat incluindo as transcrições

## 🚀 Funcionalidades

- ✅ Transcrição automática de mensagens de áudio
- ✅ Suporte a múltiplos tamanhos de modelo Whisper
- ✅ Detecção automática de GPU/CPU
- ✅ Logs detalhados do processo
- ✅ Preservação do formato original do chat
- ✅ Suporte a idioma português

## 📋 Pré-requisitos

- Python 3.11 ou superior
- [uv](https://docs.astral.sh/uv/) (gerenciador de pacotes Python)

### Instalação do uv

Se você ainda não tem o `uv` instalado:

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## 🛠️ Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/felipe0liveira/whatsapp-transcriber.git
cd whatsapp-transcriber
```

2. **Crie um ambiente virtual:**
```bash
uv venv
```

3. **Ative o ambiente virtual:**
```bash
# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

4. **Instale as dependências:**
```bash
uv sync
```

## 📱 Como exportar o chat do WhatsApp

1. Abra o WhatsApp no seu celular
2. Vá para a conversa que deseja transcrever
3. Toque nos três pontos (⋮) no canto superior direito
4. Selecione "Mais" → "Exportar conversa"
5. Escolha "Incluir mídia"
6. Salve o arquivo ZIP gerado

## 🎯 Como usar

1. **Coloque o arquivo ZIP exportado na pasta `data/`:**
```bash
mkdir -p data
# Copie seu arquivo .zip para a pasta data/
```

2. **Edite o arquivo `main.py` (se necessário):**
Modifique a linha final para apontar para seu arquivo ZIP:
```python
if __name__ == "__main__":
    main(zip_path="data/SEU_ARQUIVO.zip", model_size="medium")
```

3. **Execute o script:**
```bash
make run
```

## ⚙️ Configurações

### Tamanhos de modelo disponíveis

Você pode escolher diferentes tamanhos de modelo Whisper:

- `tiny` - Mais rápido, menor precisão
- `base` - Balanceado
- `small` - Boa precisão, velocidade razoável
- `medium` - **Padrão** - Boa precisão
- `large` - Melhor precisão, mais lento

### Monitoramento de GPU

Para verificar se sua GPU está sendo utilizada:

```bash
make monitor
```

## 📁 Estrutura de saída

Após a execução, você encontrará:

```
output/
├── chat.txt                    # Chat com transcrições integradas
└── whatsapp_chat/             # Arquivos extraídos do ZIP
    ├── _chat.txt              # Chat original
    ├── *.opus                 # Arquivos de áudio
    └── *.jpg                  # Imagens (se houver)
```

## 🔧 Solução de problemas

### Erro de GPU/CUDA

Se você tiver problemas com CUDA, o script automaticamente utilizará a CPU:

```
🖥️ Running on CPU
```

### Erro de codificação

Se houver problemas com caracteres especiais, verifique se os arquivos estão em UTF-8.

### Dependências

Se houver problemas com as dependências, tente:

```bash
uv sync --reinstall
```

## 📊 Log de execução

O script gera logs detalhados em:
- Console (stdout)
- Arquivo `transcription.log`

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🙏 Agradecimentos

- [OpenAI Whisper](https://github.com/openai/whisper) - Modelo de transcrição de áudio
- [uv](https://github.com/astral-sh/uv) - Gerenciador de pacotes Python rápido