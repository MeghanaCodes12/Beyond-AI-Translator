import os
import re

from dotenv import load_dotenv
from google import genai


load_dotenv()

class GeminiQuotaError(Exception):
    """Raised when Gemini API quota/rate limit is exceeded."""
    
    def __init__(self, retry_seconds=None):
        self.retry_seconds = retry_seconds
        
        if retry_seconds:
            message = (
                "Gemini quota limit reached."
                f"Please try again in about {retry_seconds} seconds."
            )
        else:
            message = (
                "Gemini quota limit reached."
                "Please try again later."
            )
            
        super().__init__(message)

class GeminiService:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY was not found."
            )

        self.client = genai.Client(
            api_key=api_key
        )
        
        self.preferred_models = [
            "gemini-3.6-flash",
            "gemini-3.5-flash",
            "gemini-3.5-flash-lite",
            "gemini-3.1-flash-lite",
        ]

        self.model = "gemini-3.6-flash"
        print(
            f"Gemini selected model: {self.model}"
        )

    def translate(
        self,
        text,
        from_language,
        to_language,
    ):

        prompt = f"""
Translate the following text from
{from_language} to {to_language}.

Preserve the original meaning, tone,
context, and formatting as much as possible.

Do not explain the translation.
Return only the translated text.

Text:
{text}
"""

        response = None
        last_error = None

        for model in self.preferred_models:

            try:
                print(
                    f"Trying Gemini model: {model}"
                )

                response = (
                    self.client.models.generate_content(
                        model=model,
                        contents=prompt,
                    )
                )

                print(
                    f"Gemini selected model: {model}"
                )
                break

            except Exception as error:
                last_error = error
                error_text = str(error)
                print(
                    f"Gemini model {model} failed: "
                    f"{error_text}"
                )
                # Try the next model
                continue

        # ALL MODELS FAILED
        if response is None:
            if last_error is not None:
                error_text = str(last_error)
                # 429 / QUOTA ERROR
                if (
                    "429" in error_text
                    or "RESOURCE_EXHAUSTED"
                    in error_text
                    or "quota"
                    in error_text.lower()
                ):

                    retry_seconds = (
                        self._extract_retry_seconds(
                            error_text
                        )
                    )

                    raise GeminiQuotaError(
                        retry_seconds
                    ) from last_error

                raise last_error

            raise RuntimeError(
                "No Gemini model was available."
            )

        # EMPTY RESPONSE
        if not response.text:

            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return response.text.strip()


    
    ### EXTRACT RETRY TIME
    def _extract_retry_seconds(
        self,
        error_text,
    ):
        patterns = [
            r"retry in\s+([\d.]+)s",
            (
                r"retryDelay['\"]?"
                r"\s*[:=]\s*"
                r"['\"]?([\d.]+)s"
            ),
        ]
        
        for pattern in patterns:
            match = re.search(
                pattern,
                error_text,
                re.IGNORECASE,
            )
            if match:
                try:
                    seconds = float(
                        match.group(1)
                    )
                    return max(
                        1,
                        int(round(seconds)),
                    )
                except ValueError:
                    pass
        return None