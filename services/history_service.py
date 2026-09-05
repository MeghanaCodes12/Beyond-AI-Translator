import json
import os

class HistoryService:
    
    def __init__(self):
        self.file_path = "history.json"
        if not os.path.exists(self.file_path):
            self._save([])
            
    # LOAD
    
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
            return []
        
    ## SAVE
    
    def _save(self, history):
        with open(
            self.file_path,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                history,
                file,
                ensure_ascii=False,
                indent=4,
            )
            
    ## ADD HISTORY
    
    def add_history(
        self,
        source_language,
        target_language,
        source_text,
        translated_text,
    ):
        history = self._load()
        item = {
            "source_language": source_language,
            "target_language": target_language,
            "source_text": source_text,
            "translated_text": translated_text,
        }
        
        # Newest translation goes first
        history.insert(0, item)
        self._save(history)
        
    ### GET HISTORY
    def get_history(self):
        return self._load()
    
    ### DELETE ONE
    def delete_history(self, index):
        history = self._load()
        if 0 <= index < len(history):
            history.pop(index)
            self._save(history)
            
    ### CLEAR ALL
    def clear_history(self):
        self._save([])