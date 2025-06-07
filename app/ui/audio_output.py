import os
import base64
import requests
import streamlit as st
from dotenv import load_dotenv


class AudioOutput:
    """Generate speech using VOICEVOX (VoiceBox) engine and play it."""

    def __init__(self, base_url: str = None, speaker: int = 1) -> None:
        load_dotenv()
        self.base_url = base_url or os.environ.get("VOICEBOX_URL", "http://voicebox:50021")
        self.speaker = speaker
        # Playback speed for generated audio. Default to 1.5 if not specified.
        self.speed = float(os.environ.get("VOICEVOX_SPEED", 1.5))

    def _synthesize(self, text: str) -> bytes:
        """Request VOICEVOX to synthesize speech and return WAV bytes."""
        query = requests.post(
            f"{self.base_url}/audio_query",
            params={"speaker": self.speaker, "text": text},
        )
        query.raise_for_status()
        q = query.json()
        # Adjust playback speed based on environment variable
        q["speedScale"] = self.speed
        synthesis = requests.post(
            f"{self.base_url}/synthesis",
            params={"speaker": self.speaker},
            json=q,
        )
        synthesis.raise_for_status()
        return synthesis.content

    def speak(self, text: str) -> None:
        if not text:
            return

        # Remove newline characters to avoid them being spoken aloud
        text = text.replace("\n", " ")

        try:
            audio = self._synthesize(text)
            encoded = base64.b64encode(audio).decode("utf-8")
            audio_html = (
                f'<audio autoplay controls src="data:audio/wav;base64,{encoded}"></audio>'
            )
            st.markdown(audio_html, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"音声生成失敗: {e}")
