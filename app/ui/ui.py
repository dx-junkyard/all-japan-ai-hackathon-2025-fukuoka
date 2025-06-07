import logging
import os
import requests
import streamlit as st

from voice_input import VoiceInput
from audio_output import AudioOutput

logger = logging.getLogger(__name__)

API_URL = os.environ.get("API_URL", "http://api:8000/api/v1/user-message")


class ChatUI:
    """Main chat UI handling text and voice input."""

    def __init__(self):
        self.voice = VoiceInput()
        self.audio_output = AudioOutput()

    @staticmethod
    def call_api(text: str, history) -> str:
        try:
            resp = requests.post(API_URL, json={"message": text, "history": history})
            resp.raise_for_status()
            return resp.text.strip()
        except Exception as e:
            st.error(f"送信エラー: {e}")
            return "エラーが発生しました"

    def _rerun(self):
        """Rerun Streamlit script with backward compatibility."""
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
        else:
            st.rerun()

    def run(self):
        st.set_page_config(page_title="AI チャットアプリ", page_icon="🤖")
        st.image("static/robopon.png")

        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "何かございましたか？マイクを押してお話ください。"}
            ]
        if "voice_processed" not in st.session_state:
            st.session_state.voice_processed = False

        if "last_audio" in st.session_state:
            text = self.voice.transcribe(st.session_state.pop("last_audio"))
            if text and not st.session_state.voice_processed:
                st.session_state.voice_processed = True
                st.session_state.messages.append({"role": "user", "content": text})
                reply = self.call_api(text, st.session_state.messages)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.session_state.speak_text = reply
                self._rerun()
            elif not text:
                st.session_state.voice_processed = False

        for m in st.session_state.messages:
            with st.chat_message("user" if m["role"] == "user" else "ai"):
                st.markdown(m["content"])

        if "speak_text" in st.session_state:
            self.audio_output.speak(st.session_state.pop("speak_text"))

        mic_col, rate_col = st.columns([3, 1])
        with mic_col:
            audio = self.voice.record_audio()
        with rate_col:
            if st.button("評価"):
                st.session_state.show_rating = True

        if st.session_state.get("show_rating"):
            with st.modal("評価"):
                st.markdown("★5")
                st.markdown("神対応でした。")
                if st.button("OK", key="rate_ok"):
                    st.session_state.show_rating = False

        if len(audio) > 0:
            st.session_state.last_audio = audio
            st.session_state.voice_processed = False
            self._rerun()


def main():
    ChatUI().run()


if __name__ == "__main__":
    main()
