import os
import zipfile
import whisper
from pathlib import Path
import torch
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('transcription.log')
    ]
)
logger = logging.getLogger(__name__)

def main(zip_path: str, output_file: str = "chat.txt", model_size: str = "small"):
    """
    Transcribe WhatsApp audio messages and integrate them into the chat history.
    
    Args:
        zip_path (str): Path to the exported WhatsApp ZIP file
        output_file (str): Output file name for the final chat with transcriptions
        model_size (str): Whisper model size (tiny, base, small, medium, large)
    """
    logger.info("Starting WhatsApp chat transcription process")
    logger.info(f"Input ZIP: {zip_path}")
    logger.info(f"Output file: {output_file}")
    logger.info(f"Model size: {model_size}")

    # Check GPU availability and log device information
    if torch.cuda.is_available():
        device_name = torch.cuda.get_device_name(0)
        logger.info(f"🚀 Using GPU: {device_name}")
        print(f"🚀 Using GPU: {device_name}")
    else:
        logger.info("🖥️ Running on CPU")
        print("🖥️ Running on CPU")

    # Extract WhatsApp ZIP file if not already extracted
    extract_path = "whatsapp_chat"
    if not os.path.exists(extract_path):
        logger.info(f"📂 Extracting ZIP file to {extract_path}")
        print(f"📂 Extracting ZIP file to {extract_path}")
        try:
            with zipfile.ZipFile(zip_path, "r") as z:
                z.extractall(extract_path)
            logger.info("✅ ZIP file extracted successfully")
        except Exception as e:
            logger.error(f"❌ Failed to extract ZIP file: {e}")
            raise
    else:
        logger.info(f"📁 Using existing extracted folder: {extract_path}")
        print(f"� Using existing extracted folder: {extract_path}")

    # Load Whisper model
    logger.info(f"🔄 Loading Whisper model: {model_size}")
    print(f"🔄 Loading Whisper model: {model_size}")
    try:
        model = whisper.load_model(model_size)
        logger.info("✅ Whisper model loaded successfully")
    except Exception as e:
        logger.error(f"❌ Failed to load Whisper model: {e}")
        raise

    # Find and transcribe audio files
    audio_folder = Path(extract_path)
    transcriptions = {}
    
    # Get all OPUS audio files
    audio_files = list(sorted(audio_folder.glob("*.opus")))
    total_files = len(audio_files)
    logger.info(f"🎵 Found {total_files} audio files to transcribe")
    print(f"� Found {total_files} audio files to transcribe")

    for i, audio_file in enumerate(audio_files, 1):
        logger.info(f"�🎙️ Transcribing {audio_file.name} ({i}/{total_files})")
        print(f"🎙️ Transcribing {audio_file.name} ({i}/{total_files})")
        
        try:
            # Transcribe audio file (assuming Portuguese language)
            result = model.transcribe(str(audio_file), language="pt")
            transcription_text = result["text"].strip()
            transcriptions[audio_file.name] = transcription_text
            
            logger.info(f"✅ Transcribed: {transcription_text[:50]}{'...' if len(transcription_text) > 50 else ''}")
        except Exception as e:
            logger.error(f"❌ Failed to transcribe {audio_file.name}: {e}")
            transcriptions[audio_file.name] = "[Transcription failed]"

    # Read the original chat file
    chat_file = audio_folder / "_chat.txt"
    logger.info(f"📖 Reading chat file: {chat_file}")
    print(f"📖 Reading chat file: {chat_file}")
    
    try:
        with open(chat_file, "r", encoding="utf-8") as f:
            chat_lines = f.readlines()
        logger.info(f"📄 Read {len(chat_lines)} lines from chat file")
    except Exception as e:
        logger.error(f"❌ Failed to read chat file: {e}")
        raise

    # Process chat lines and integrate transcriptions
    logger.info("🔄 Processing chat lines and integrating transcriptions")
    print("🔄 Processing chat lines and integrating transcriptions")
    
    final_lines = []
    transcriptions_added = 0
    
    for line in chat_lines:
        if "<attached:" in line and ".opus" in line:
            # Extract audio file name from the attachment line
            start = line.find("<attached: ") + 11
            end = line.find(".opus") + 5
            audio_filename = line[start:end]

            # Add the original line
            final_lines.append(line)
            
            # Add transcription below the message if available
            if audio_filename in transcriptions:
                transcription = transcriptions[audio_filename]
                final_lines.append(f"    (Transcription: {transcription})\n")
                transcriptions_added += 1
                logger.debug(f"Added transcription for {audio_filename}")
        else:
            final_lines.append(line)

    # Write the final chat file with transcriptions
    logger.info(f"💾 Writing final chat file: {output_file}")
    print(f"💾 Writing final chat file: {output_file}")
    
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.writelines(final_lines)
        
        logger.info(f"✅ Chat reconstruction completed!")
        logger.info(f"📊 Statistics:")
        logger.info(f"   - Total audio files: {total_files}")
        logger.info(f"   - Transcriptions added: {transcriptions_added}")
        logger.info(f"   - Output file: {output_file}")
        
        print(f"\n✅ Chat reconstruction completed!")
        print(f"📊 Statistics:")
        print(f"   - Total audio files: {total_files}")
        print(f"   - Transcriptions added: {transcriptions_added}")
        print(f"   - Output saved to: {output_file}")
        
    except Exception as e:
        logger.error(f"❌ Failed to write output file: {e}")
        raise


if __name__ == "__main__":
    main(zip_path="data/bruno-ferracin.zip")
