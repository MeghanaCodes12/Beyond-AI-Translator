import asyncio
import flet as ft
import os
import tempfile

from services.favorites_service import FavoritesService
from services.history_service import HistoryService
from services.settings_service import SettingsService
from ui.components.buttons import NatureButton
from services.gemini_service import (
    GeminiService,
    GeminiQuotaError,
)
from data.languages import Languages

class TranslatorPanel(ft.Container):

    def __init__(self, app_page):
        self.app_page = app_page
        self.clipboard = ft.Clipboard()
        
        # SERVICES
        self.gemini_service = None
        
        self.favorites_service = FavoritesService()
        self.history_service = HistoryService()
        self.settings_service = SettingsService()
        self.tts_voices = {
            "Hindi": "hi-IN-SwaraNeural",
            "Telugu": "te-IN-ShrutiNeural",
            "Tamil": "ta-IN-PallaviNeural",
            "Kannada": "kn-IN-SapnaNeural",
            "Malayalam": "ml-IN-SobhanaNeural",
        }
        self.edge_tts_voices = None
        self.speech_playing = False

        # LANGUAGE FIELDS
        self.from_language = ft.TextField(
            label="From Language",
            hint_text="English",
            value="English",
            expand=True,
            border_radius=12,
            border_width=1,
            content_padding=16,
        )

        self.to_language = ft.TextField(
            label="To Language",
            hint_text="Telugu",
            value="Telugu",
            expand=True,
            border_radius=12,
            border_width=1,
            content_padding=16,
        )

        # SOURCE LANGUAGE PICKER
        self.source_picker = ft.IconButton(
            icon=ft.Icons.LANGUAGE,
            tooltip="Choose source language",
            on_click=lambda e: self._show_language_dialog(
                is_source=True
            ),
        )
        
        # TARGET LANGUAGE PICKER
        self.target_picker = ft.IconButton(
            icon=ft.Icons.LANGUAGE,
            tooltip="Choose target language",
            on_click=lambda e: self._show_language_dialog(
                is_source=False
            ),
        )

        # INPUT
        self.input_text = ft.TextField(
            label="Enter Text",
            hint_text="Type or paste your text here...",
            multiline=True,
            min_lines=5,
            max_lines=8,
            expand=True,
            border_radius=16,
            content_padding=16,
            on_change=self.on_input_change,
        )

        # OUTPUT
        self.output_text = ft.TextField(
            label="Translation",
            multiline=True,
            min_lines=5,
            max_lines=8,
            expand=True,
            read_only=True,
            border_radius=16,
            content_padding=16,
        )

        # TRANSLATE BUTTON
        self.translate_button = NatureButton(
            "🌿 Translate",
            on_click=self.translate,
        )
        
        # SWAP BUTTON
        self.swap_button = ft.IconButton(
            icon=ft.Icons.SWAP_HORIZ,
            tooltip="Swap languages",
            on_click=self.swap_languages,
        )

        # COPY BUTTON
        self.copy_button = ft.TextButton(
            content=ft.Text(
                "📋",
                size=20,
            ),
            tooltip="Copy translation",
            on_click=self.copy_translation,
        )

        # SPEAK BUTTON
        self.speak_button = ft.IconButton(
            icon=ft.Icons.VOLUME_UP,
            icon_size=24,
            tooltip="Speak",
            on_click=self.speak_translation,
        )

        # FAVORITE BUTTON
        self.favorite_button = ft.TextButton(
            content=ft.Text(
                "⭐",
                size=27,
            ),
            tooltip="Save to favorites",
            on_click=self.save_favorite,
        )

        # STATUS
        self.status_text = ft.Text(
            "",
            size=14,
        )

        # MAIN CONTENT
        # Scroll is important because the buttons at the bottom
        # were hidden when the application window was small.
        translator_content = ft.Column(
            spacing=10,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[

                # TITLE
                ft.Text(
                    "Translator",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                ),

                # LANGUAGE ROW
                ft.Row(
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            content=self.from_language,
                            expand=True,
                        ),
                        self.source_picker,
                        
                        ft.Container(
                            width=48,
                            height=48,
                            border_radius=24,
                            content=self.swap_button,
                        ),
                        
                        ft.Container(
                            content=self.to_language,
                            expand=True,
                        ),
                        
                        self.target_picker,
                    ],
                ),
                
                #GAP AFTER LANGUAGE ROW
                ft.Container(height=4),
                
                # INPUT
                self.input_text,
                
                # GAP BEFORE TRANSLATE BUTTON
                ft.Container(height=6),
                
                # TRANSLATE
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        self.translate_button,
                    ],
                ),
                
                # GAP AFTER TRANSLATE BUTTON
                ft.Container(height=6),

                # STATUS
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        self.status_text,
                    ],
                ),

                # OUTPUT
                self.output_text,

                # OUTPUT ACTIONS
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    spacing=4,
                    controls=[
                        self.copy_button,
                        self.speak_button,
                        self.favorite_button,
                    ],
                ),
            ],
        )

        # BUILD PANEL
        super().__init__(
            expand=True,
            padding=16,
            content=translator_content,
        )
        
    # LANGUAGE SELECTION
    def select_source_language(self, e):
        language = e.control.data
        if language == "__other_language__":
            self._show_language_dialog(
                is_source=True
            )
            return
        
        self.from_language.value = e.control.data
        self.status_text.value = ""
        self.update()

    def select_target_language(self, e):
        language = e.control.data
        if language == "__other_language__":
            self._show_language_dialog(
                is_source=False
            )
            return
        
        self.to_language.value = e.control.data
        self.status_text.value = ""
        self.update()

    def swap_languages(self, e):

        # Swap languages
        source_language = self.from_language.value
        target_language = self.to_language.value

        self.from_language.value = target_language
        self.to_language.value = source_language

        # Swap input and translation
        source_text = self.input_text.value
        translated_text = self.output_text.value

        self.input_text.value = translated_text
        self.output_text.value = source_text

        # Reset favorite state
        self.favorite_button.content.value = "⭐"

        # Clear status
        self.status_text.value = ""

        self.update()
    

    # TRANSLATION
    async def translate(self, e):
        # READ VALUES
        text = (
            self.input_text.value or ""
        ).strip()

        from_language = (
            self.from_language.value or ""
        ).strip()

        to_language = (
            self.to_language.value or ""
        ).strip()

        # VALIDATE TEXT
        if not text:
            self.output_text.value = (
                "Please enter some text."
            )
            self.status_text.value = ""
            self.update()
            return

        # VALIDATE LANGUAGES
        if not from_language or not to_language:
            self.output_text.value = (
                "Please select both languages."
            )
            self.status_text.value = ""
            self.update()
            return

        # DISABLE TRANSLATE BUTTON
        self.translate_button.disabled = True
        self.translate_button.content.value = "⏳ Translating..."
        self.output_text.value = (
            "Translating..."
        )

        self.status_text.value = ""
        self.update()

        # CALL GEMINI WITHOUT BLOCKING FLET UI
        try:
            if self.gemini_service is None:
                self.gemini_service = await asyncio.to_thread(
                    GeminiService
                )
            result = await asyncio.to_thread(
                self.gemini_service.translate,
                text=text,
                from_language=from_language,
                to_language=to_language,
            )

            # SUCCESS
            self.output_text.value = result

            # AUTO COPY TRANSLATION
            if self.settings_service.get(
                "auto_copy",
                False,
            ):
                try:
                    await self.clipboard.set(result)
                    self.status_text.value = (
                        "✓ Translation completed • Copied!"
                    )

                except Exception as copy_error:
                    print(
                        f"Auto-copy error: {copy_error}"
                    )

                    self.status_text.value = (
                        "✓ Translation completed"
                    )

                else:
                    self.status_text.value = (
                        "✓ Translation completed"
                    )

            # SAVE HISTORY
            try:
                await asyncio.to_thread(
                    self.history_service.add_history,
                    source_language=from_language,
                    target_language=to_language,
                    source_text=text,
                    translated_text=result,
                )

            except Exception as history_error:
                print(
                    f"History error: {history_error}"
                )

        except GeminiQuotaError as error:
            if error.retry_seconds:
                self.output_text.value = (
                    "⚠ Gemini translation limit reached.\n\n"
                    f"Please try again in about "
                    f"{error.retry_seconds} seconds."
                )
                self.status_text.value = (
                    f"⚠ Gemini limit reached. "
                    f"Retry in {error.retry_seconds}s."
                )
            else :
                self.output_text.value = (
                    "⚠ Gemini translation limit reached.\n\n"
                    "Please try again later."
                )
                self.status_text.value = (
                    "⚠ Gemini quota limit reached."
                )
        except Exception as error:
            print(
                f"Gemini error: {error}"
            )
            self.output_text.value = (
                "Translation failed.\n\n"
                "Please check your internet connection "
                "and try again."
            )
            self.status_text.value = (
                "⚠ Translation failed."
            )

        finally:
            # ALWAYS RESTORE TRANSLATE BUTTON
            # This runs for BOTH success and failure.
            self.translate_button.disabled = False

            self.translate_button.content.value = "🌿 Translate"

            self.update()

    # COPY TRANSLATION
    async def copy_translation(self, e):
        text = (
            self.output_text.value or ""
        ).strip()

        if not text:
            self.status_text.value = (
                "Nothing to copy."
            )
            self.update()
            return

        # DON'T COPY PLACEHOLDER TEXT
        if text in (
            "Translating...",
            "Please enter some text.",
            "Please select both languages.",
        ):
            self.status_text.value = (
                "There is no completed translation to copy."
            )
            self.update()
            return

        try:
            await self.page.clipboard.set(
                text
            )
            self.status_text.value = (
                "✓ Translation copied!"
            )
            self.update()

        except Exception as error:
            print(
                f"Clipboard error: {error}"
            )
            self.status_text.value = (
                "Unable to copy translation."
            )
            self.update()
            
    # SPEAK TRANSLATION
    def speak_translation(self, e):

        if self.speech_playing:
            self.stop_speech()
            return
        
        # CHECK SETTINGS
        speech_enabled = (
            self.settings_service.get(
                "speech_enabled",
                True,
            )
        )
        
        # SPEECH DISABLED
        if not speech_enabled:
            print(
                "Speech is disabled. Not speaking."
            )
            self.status_text.value = (
                "🔇 Speech is disabled in Settings."
            )
            self.update()
            return

        # GET TRANSLATION
        text = (
            self.output_text.value or ""
        ).strip()

        # VALIDATE
        if not text:
            self.status_text.value = (
                "There is no translation to speak."
            )
            self.update()
            return

        # DON'T SPEAK PLACEHOLDER TEXT
        if text in (
            "Translating...",
            "Please enter some text.",
            "Please select both languages.",
        ):
            self.status_text.value = (
                "Please wait for the translation first."
            )
            self.update()
            return

        # SHOW SPEAKING STATE
        self.speech_playing = True
        self.speak_button.icon = ft.Icons.STOP
        self.speak_button.tooltip = "Stop speech"
        self.speak_button.on_click = self.stop_speech
        
        # SHOW STATUS
        self.status_text.value = (
            "🔊 Speaking..."
        )
        self.app_page.update()

        # SPEAK IN BACKGROUND
        self.app_page.run_thread(
            self._speak_text,
            text,
        )

    # PYTTSX3 WORKER
    def _speak_text(self, text):
        
        import pyttsx3
        import pygame
        
        try:
            language = (
                self.to_language.value or "English"
            ).strip()
    
            ### ENGLISH → PYTTSX3
            if language == "English":
                engine = pyttsx3.init()
                voices = engine.getProperty("voices")
                if voices:
                    engine.setProperty(
                        "voice",
                        voices[0].id,
                    )
                engine.setProperty(
                    "rate",
                    150,
                )
                engine.setProperty(
                    "volume",
                    1.0,
                )
                
                engine.say(text)
                engine.runAndWait()
                engine.stop()
                
            ### OTHER LANGUAGES → EDGE TTS
            else:
                voice = self._find_tts_voice(language)
                if not voice:
                    self.status_text.value = (
                        f"🔊 Speech voice not available for {language}."
                    )
                    self.app_page.update()
                    return

                asyncio.run(
                    self._generate_edge_speech(
                        text,
                        voice,
                    )
                )
            self.speech_playing = False
            
            self.speak_button.icon = ft.Icons.VOLUME_UP
            self.speak_button.tooltip = "Speak"
            self.speak_button.on_click = self.speak_translation
            
            self.status_text.value = "✓ Speech completed"
            self.app_page.update()
            
        except Exception as error:
            print(
                f"Speech error: {error}"
            )
            
            self.speech_playing = False

            self.speak_button.icon = ft.Icons.VOLUME_UP
            self.speak_button.tooltip = "Speak"
            self.speak_button.on_click = self.speak_translation
            
            self.status_text.value = (
                "Unable to speak the translation."
            )
            self.app_page.update()
            
    def _find_tts_voice(self, language):
        
        import edge_tts
        
        """
        Find an Edge TTS voice for the selected language.
        This is independent of Languages.common.
        The user can type any language into the language field.
        """
        
        language_lower = (
            language or ""
        ).strip().lower()
        
        if not language_lower:
            return None
        
        #Existing known voices
        if language_lower in {
            key.lower(): value
            for key, value in self.tts_voices.items()
        }:
            return {
                key.lower(): value
                for key, value in self.tts_voices.items()
            }[language_lower]
        
        # Language name -> Locale prefix.
        # This is ONLY for TTS.
        # It does NOT affect Languages.common.
        language_locales = {
            "english": "en",
            "hindi": "hi",
            "telugu": "te",
            "tamil": "ta",
            "kannada": "kn",
            "malayalam": "ml",
            "marathi": "mr",
            "bengali": "bn",
            "gujarati": "gu",
            "punjabi": "pa",
            "urdu": "ur",
            "spanish": "es",
            "french": "fr",
            "german": "de",
            "italian": "it",
            "portuguese": "pt",
            "russian": "ru",
            "japanese": "ja",
            "korean": "ko",
            "chinese": "zh",
            "arabic": "ar",
            
            # TTS-only languages
            "swedish": "sv",
            "greek": "el",
            "dutch": "nl",
            "polish": "pl",
            "czech": "cs",
            "danish": "da",
            "norwegian": "nb",
            "finnish": "fi",
            "turkish": "tr",
            "vietnamese": "vi",
            "indonesian": "id",
            "hebrew": "he",
            "romanian": "ro",
        }
        locale_prefix = language_locales.get(
            language_lower
        )
        # If the language is not in our manual mapping,try to match it 
        #directly against Edge TTS voice locale names.
        if not locale_prefix:
            return None

    async def _generate_edge_speech(
        self,
        text,
        voice,
    ):
        import edge_tts
        import pygame
        import time
        import os
        import tempfile
        
        start_time = time.perf_counter()
        
        communicate = edge_tts.Communicate(
            text,
            voice,
        )
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3",
        ) as temp_file:
            audio_path = temp_file.name
            
        try:
            # Generate Speech
            await communicate.save(audio_path)
            generation_time = (
                time.perf_counter() - start_time
            )
            
            # Initialize pygame mixer only if needed
            mixer_start = time.perf_counter()

            if not pygame.mixer.get_init():
                pygame.mixer.init()

            # Stop any previous audio
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            
            # Load generated audio
            load_start = time.perf_counter()

            pygame.mixer.music.load(
                audio_path
            )
           
            # PLAY IMMEDIATELY
            pygame.mixer.music.play()
            
            self.speech_playing = True

            #Wait until audio finishes
            while pygame.mixer.music.get_busy():
                if not self.speech_playing:
                    break
                await asyncio.sleep(0.05)
                
            # STOP PLAYBACK
            pygame.mixer.music.stop()
            
            # Give pygame a moment to release
            # the Windows file handle.
            await asyncio.sleep(0.2)
            
            # UNLOAD AUDIO
            try:
                pygame.mixer.music.unload()
            except Exception as unload_error:
                print(
                    "TTS: unload warning:",
                    unload_error,
                )

            # Give Windows time to release
            # the MP3 file.
            await asyncio.sleep(0.2)

        finally:
           
           # CLEANUP TEMP FILE
            try:
                if os.path.exists(audio_path):
                    os.remove(audio_path)
        
            except OSError as error:
                print(
                    "TTS: could not remove temporary file:",
                    error,
                )
            self.speech_playing = False
    
    # SAVE FAVORITE
    def save_favorite(self, e):

        source_text = (
            self.input_text.value or ""
        ).strip()

        translated_text = (
            self.output_text.value or ""
        ).strip()

        source_language = (
            self.from_language.value or ""
        ).strip()

        target_language = (
            self.to_language.value or ""
        ).strip()

        # VALIDATE SOURCE
        if not source_text:
            self.show_message(
                "Nothing to save."
            )
            return

        # VALIDATE TRANSLATION
        if not translated_text:
            self.show_message(
                "Please translate the text first."
            )
            return

        # DON'T SAVE PLACEHOLDER
        if translated_text in (
            "Translating...",
            "Please enter some text.",
            "Please select both languages.",
        ):
            self.show_message(
                "Please wait for the translation first."
            )
            return

        # CHECK IF ALREADY FAVORITED
        if self.favorites_service.is_favorite(
            source_language=source_language,
            target_language=target_language,
            source_text=source_text,
            translated_text=translated_text,
        ):
            self.favorite_button.content.value = "❤️"

            self.show_message(
                "⭐ Already in favorites."
            )

            self.update()
            return

        # SAVE FAVORITE
        try:
            added = self.favorites_service.add_favorite(
                source_language=source_language,
                target_language=target_language,
                source_text=source_text,
                translated_text=translated_text,
            )

            if added:
                self.favorite_button.content.value = "❤️"

                self.show_message(
                    "⭐ Added to favorites!"
                )

            else:
                self.favorite_button.content.value = "❤️"

                self.show_message(
                    "⭐ Already in favorites."
                )

            self.update()

        except Exception as error:
            print(
                f"Favorites error: {error}"
            )

            self.show_message(
                "Could not save favorite."
            )
    
    # MESSAGE
    def show_message(self, message):
        self.status_text.value = message
        self.update()
        
    def on_input_change(self, e):
        self.favorite_button.content.value = "⭐"
        if self.status_text.value:
            self.status_text.value = ""

        self.update()
            
    def _show_language_dialog(self, is_source):

        def select_language(e):
            language = e.control.data

            if is_source:
                self.from_language.value = language
            else:
                self.to_language.value = language

            self.status_text.value = ""

            dialog.open = False
            self.page.update()
            self.update()

        language_buttons = []

        for language in Languages.common:
            language_buttons.append(
                ft.TextButton(
                    content=ft.Text(language),
                    data=language,
                    on_click=select_language,
                )
            )

        language_buttons.append(
            ft.TextButton(
                content=ft.Text("🌐 Other language..."),
                data="__other_language__",
                on_click=lambda e: self._show_other_language_dialog(
                    is_source
                ),
            )
        )

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                "Choose source language"
                if is_source
                else "Choose target language"
            ),
            content=ft.Container(
                width=350,
                height=400,
                content=ft.Column(
                    controls=language_buttons,
                    scroll=ft.ScrollMode.AUTO,
                ),
            ),
        )

        self.page.show_dialog(dialog)
    
    def _show_other_language_dialog(self, is_source):

        language_field = ft.TextField(
            label="Language",
            hint_text="Enter any language",
            autofocus=True,
            width=350,
        )

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("🌐 Enter language"),
            content=language_field,
        )

        def cancel_dialog(e):
            dialog.open = False
            self.page.update()

        def confirm_language(e):
            language = (language_field.value or "").strip()

            if not language:
                return

            if is_source:
                self.from_language.value = language
            else:
                self.to_language.value = language

            self.status_text.value = ""

            dialog.open = False
            self.page.update()
            self.update()

        dialog.actions = [
            ft.TextButton(
                "Cancel",
                on_click=cancel_dialog,
            ),
            ft.TextButton(
                "OK",
                on_click=confirm_language,
            ),
        ]

        self.page.show_dialog(dialog) 
        
    ### STOP SPEECH
    def stop_speech(self, e=None):
        
        import pygame
        
        try:
            self.speech_playing = False
            
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
                
            self.speak_button.icon = ft.Icons.VOLUME_UP
            self.speak_button.tooltip = "Speak"
            self.speak_button.on_click = self.speak_translation
            
            self.status_text.value = "⏹ Speech stopped."
            
            self.app_page.update()
        
        except Exception as error:
            print(
                f"Stop speech error: {error}"
            )