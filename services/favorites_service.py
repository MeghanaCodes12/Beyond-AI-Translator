import json
import os


class FavoritesService:

    def __init__(self):
        self.file_path = "favorites.json"

        if not os.path.exists(self.file_path):
            self._save([])

    # LOAD FAVORITES
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

    # SAVE FAVORITES
    def _save(self, favorites):
        with open(
            self.file_path,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                favorites,
                file,
                ensure_ascii=False,
                indent=4,
            )

    # ADD FAVORITE
    def add_favorite(
        self,
        source_language,
        target_language,
        source_text,
        translated_text,
    ):
        favorites = self._load()

        # Prevent duplicate favorites
        for favorite in favorites:
            if (
                favorite.get("source_language") == source_language
                and favorite.get("target_language") == target_language
                and favorite.get("source_text") == source_text
                and favorite.get("translated_text") == translated_text
            ):
                return False

        favorite = {
            "source_language": source_language,
            "target_language": target_language,
            "source_text": source_text,
            "translated_text": translated_text,
        }

        favorites.append(favorite)

        self._save(favorites)

        return True

    # GET FAVORITES
    def get_favorites(self):
        return self._load()

    # CHECK FAVORITE
    def is_favorite(
        self,
        source_language,
        target_language,
        source_text,
        translated_text,
    ):
        favorites = self._load()

        for favorite in favorites:
            if (
                favorite.get("source_language") == source_language
                and favorite.get("target_language") == target_language
                and favorite.get("source_text") == source_text
                and favorite.get("translated_text") == translated_text
            ):
                return True

        return False