import os
import zipfile
import whisper
from pathlib import Path
import torch
import logging
from typing import Dict, List, Tuple

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


def setup_output_directory() -> Path:
    """
    Create and return the output directory path.
    
    Returns:
        Path: The output directory path
    """
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    logger.info(f"📁 Created/using output directory: {output_dir}")
    return output_dir


def check_gpu_availability() -> None:
    """
    Check and log GPU availability information.
    """
    if torch.cuda.is_available():
        device_name = torch.cuda.get_device_name(0)
        logger.info(f"🚀 Using GPU: {device_name}")
    else:
        logger.info("🖥️ Running on CPU")


def extract_whatsapp_zip(zip_path: str, extract_path: Path) -> None:
    """
    Extract WhatsApp ZIP file to the specified path.
    
    Args:
        zip_path (str): Path to the WhatsApp ZIP file
        extract_path (Path): Directory to extract the ZIP file to
    """
    if not os.path.exists(extract_path):
        logger.info(f"📂 Extracting ZIP file to {extract_path}")
        try:
            with zipfile.ZipFile(zip_path, "r") as z:
                z.extractall(extract_path)
            logger.info("✅ ZIP file extracted successfully")
        except Exception as e:
            logger.error(f"❌ Failed to extract ZIP file: {e}")
            raise
    else:
        logger.info(f"📁 Using existing extracted folder: {extract_path}")


def load_whisper_model(model_size: str) -> whisper.Whisper:
    """
    Load and return the Whisper model.
    
    Args:
        model_size (str): Size of the Whisper model to load
        
    Returns:
        whisper.Whisper: The loaded Whisper model
    """
    logger.info(f"🔄 Loading Whisper model: {model_size}")
    try:
        model = whisper.load_model(model_size)
        logger.info("✅ Whisper model loaded successfully")
        return model
    except Exception as e:
        logger.error(f"❌ Failed to load Whisper model: {e}")
        raise


def find_audio_files(audio_folder: Path) -> List[Path]:
    """
    Find and return all OPUS audio files in the specified folder.
    
    Args:
        audio_folder (Path): Path to search for audio files
        
    Returns:
        List[Path]: List of audio file paths
    """
    audio_files = list(sorted(audio_folder.glob("*.opus")))
    logger.info(f"🎵 Found {len(audio_files)} audio files to transcribe")
    return audio_files


def transcribe_audio_files(model: whisper.Whisper, audio_files: List[Path]) -> Dict[str, str]:
    """
    Transcribe all audio files and return transcriptions.
    
    Args:
        model (whisper.Whisper): The Whisper model to use for transcription
        audio_files (List[Path]): List of audio files to transcribe
        
    Returns:
        Dict[str, str]: Dictionary mapping filename to transcription
    """
    transcriptions = {}
    total_files = len(audio_files)
    
    for i, audio_file in enumerate(audio_files, 1):
        logger.info(f"🎙️ Transcribing {audio_file.name} ({i}/{total_files})")
        
        try:
            # Transcribe audio file (assuming Portuguese language)
            result = model.transcribe(str(audio_file), language="pt")
            transcription_text = result["text"].strip()
            transcriptions[audio_file.name] = transcription_text
            
            logger.info(f"✅ Transcribed: {transcription_text[:50]}{'...' if len(transcription_text) > 50 else ''}")
        except Exception as e:
            logger.error(f"❌ Failed to transcribe {audio_file.name}: {e}")
            transcriptions[audio_file.name] = "[Transcription failed]"
    
    return transcriptions


def read_chat_file(chat_file_path: Path) -> List[str]:
    """
    Read and return the contents of the chat file.
    
    Args:
        chat_file_path (Path): Path to the chat file
        
    Returns:
        List[str]: List of chat lines
    """
    logger.info(f"📖 Reading chat file: {chat_file_path}")
    
    try:
        with open(chat_file_path, "r", encoding="utf-8") as f:
            chat_lines = f.readlines()
        logger.info(f"📄 Read {len(chat_lines)} lines from chat file")
        return chat_lines
    except Exception as e:
        logger.error(f"❌ Failed to read chat file: {e}")
        raise


def integrate_transcriptions(chat_lines: List[str], transcriptions: Dict[str, str]) -> Tuple[List[str], int]:
    """
    Integrate transcriptions into chat lines.
    
    Args:
        chat_lines (List[str]): Original chat lines
        transcriptions (Dict[str, str]): Audio transcriptions
        
    Returns:
        Tuple[List[str], int]: Final chat lines and number of transcriptions added
    """
    logger.info("🔄 Processing chat lines and integrating transcriptions")
    
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
    
    return final_lines, transcriptions_added


def write_output_file(final_lines: List[str], output_file_path: Path) -> None:
    """
    Write the final chat with transcriptions to the output file.
    
    Args:
        final_lines (List[str]): Final chat lines with transcriptions
        output_file_path (Path): Path to write the output file
    """
    logger.info(f"💾 Writing final chat file: {output_file_path}")
    
    try:
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.writelines(final_lines)
        logger.info(f"✅ Output file written successfully: {output_file_path}")
    except Exception as e:
        logger.error(f"❌ Failed to write output file: {e}")
        raise


def main(zip_path: str, output_file: str = "chat.txt", model_size: str = "small"):
    """
    Main function to transcribe WhatsApp audio messages and integrate them into the chat history.
    
    Args:
        zip_path (str): Path to the exported WhatsApp ZIP file
        output_file (str): Output file name for the final chat with transcriptions
        model_size (str): Whisper model size (tiny, base, small, medium, large)
    """
    logger.info("Starting WhatsApp chat transcription process")
    logger.info(f"Input ZIP: {zip_path}")
    logger.info(f"Output file: {output_file}")
    logger.info(f"Model size: {model_size}")

    # Setup output directory
    output_dir = setup_output_directory()
    
    # Check GPU availability
    check_gpu_availability()
    
    # Extract WhatsApp ZIP file
    extract_path = output_dir / "whatsapp_chat"
    extract_whatsapp_zip(zip_path, extract_path)
    
    # Load Whisper model
    model = load_whisper_model(model_size)
    
    # Find and transcribe audio files
    audio_folder = Path(extract_path)
    audio_files = find_audio_files(audio_folder)
    transcriptions = transcribe_audio_files(model, audio_files)
    
    # Read chat file and integrate transcriptions
    chat_file = audio_folder / "_chat.txt"
    chat_lines = read_chat_file(chat_file)
    final_lines, transcriptions_added = integrate_transcriptions(chat_lines, transcriptions)
    
    # Write output file
    output_file_path = output_dir / output_file
    write_output_file(final_lines, output_file_path)
    
    # Log final statistics
    logger.info("✅ Chat reconstruction completed!")
    logger.info("📊 Statistics:")
    logger.info(f"   - Total audio files: {len(audio_files)}")
    logger.info(f"   - Transcriptions added: {transcriptions_added}")
    logger.info(f"   - Output file: {output_file_path}")


if __name__ == "__main__":
    main(zip_path="data/bruno-ferracin.zip", model_size="medium")
