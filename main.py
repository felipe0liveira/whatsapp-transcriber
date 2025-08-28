import os
import zipfile
import whisper
from pathlib import Path
import torch

def main(zip_path: str, output_file: str = "chat.txt", model_size: str = "small"):
    # zip_path: caminho do ZIP exportado do WhatsApp
    # output_file: saída final
    # model_size: tiny, base, small, medium, large

    if torch.cuda.is_available():
        print("GPU em uso:", torch.cuda.get_device_name(0))
    else:
        print("Rodando na CPU")

    extract_path = "whatsapp_chat"
    if not os.path.exists(extract_path):
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(extract_path)

    print("🔄 Carregando modelo Whisper...")
    model = whisper.load_model(model_size)

    audio_folder = Path(extract_path)
    transcricoes = {}

    for audio_file in sorted(audio_folder.glob("*.opus")):
        print(f"🎙️ Transcrevendo {audio_file.name}...")
        result = model.transcribe(str(audio_file), language="pt")
        transcricoes[audio_file.name] = result["text"].strip()

    chat_file = audio_folder / "_chat.txt"
    with open(chat_file, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    linhas_final = []
    for linha in linhas:
        if "<attached:" in linha and ".opus" in linha:
            # pegar nome do arquivo do anexo
            start = linha.find("<attached: ") + 11
            end = linha.find(".opus") + 5
            nome_audio = linha[start:end]

            # adicionar transcrição abaixo da mensagem
            linhas_final.append(linha)
            if nome_audio in transcricoes:
                linhas_final.append(f"    (Transcrição: {transcricoes[nome_audio]})\n")
        else:
            linhas_final.append(linha)

    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(linhas_final)

    print(f"\n✅ Conversa reconstruída salva em: {output_file}")



if __name__ == "__main__":
    main(zip_path="data/bruno-ferracin.zip")
