import json
import os

class SettingsService:
    
    def __init__(self):
        self.file_path = "settings.json"
        if not os.path.exists(self.file_path):
            self._save(
                {
                    "dark_mode": False,
                    "auto_copy": False,
                    "speech_enabled": True
                }
            )
            
    ### LOAD SETTINGS
    def _load(self):
        try:
            with open(
                self.file_path,
                "r",
                encoding="utf-8",
            ) as file:
                return json.load(file)
        
        except (
            json.JSONDecodeError,
            FileNotFoundError,
        ):
            return {
                "dark_mode": False,
                "auto_copy": False,
                "speech_enabled": True,
            }
            
    ### SAVE SETTINGS
    def _save(self, settings):
        with open(
            self.file_path,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                settings,
                file,
                ensure_ascii=False,
                indent=4,
            )
            
    ### GET ALL SETTINGS
    def get_settings(self):
        return self._load()
    
    ### GET ONE SETTING
    def get(self, key, default=None):
        settings = self._load()
        return settings.get(
            key,
            default,
        )
        
    ### UPDATE ONE SETTING
    def set(self, key, value):
        settings = self._load()
        settings[key] = value
        
        
        self._save(settings)
    