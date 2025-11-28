# courses/services/stepik_client.py
import os
import time
import requests
from urllib.parse import urljoin

STEPIK_BASE = os.getenv("STEPIK_API_BASE", "https://stepik.org/api")
OAUTH_URL = os.getenv("STEPIK_OAUTH_URL", "https://stepik.org/oauth2/token/")
CLIENT_ID = os.getenv("STEPIK_CLIENT_ID")
CLIENT_SECRET = os.getenv("STEPIK_CLIENT_SECRET")

class StepikAuthError(Exception):
    pass

class StepikClient:
    def __init__(self):
        self.token = None
        self.token_expires_at = 0

    def _ensure_token(self):
        """Запрашивает токен, если он отсутствует или истёк"""
        if self.token and time.time() < self.token_expires_at - 30:
            return

        if not CLIENT_ID or not CLIENT_SECRET:
            raise StepikAuthError("STEPIK_CLIENT_ID или STEPIK_CLIENT_SECRET не указаны в .env")

        data = {
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }

        resp = requests.post(OAUTH_URL, data=data, timeout=10)
        resp.raise_for_status()
        j = resp.json()

        self.token = j["access_token"]
        self.token_expires_at = time.time() + j.get("expires_in", 3600)

    def _get(self, path, params=None):
        """Внутренний метод GET с автоматической авторизацией"""
        self._ensure_token()
        headers = {"Authorization": f"Bearer {self.token}"}

        url = urljoin(STEPIK_BASE + "/", path.lstrip("/"))
        resp = requests.get(url, params=params, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.json()

    def paginated_get(self, path, params=None, item_key="results"):
        """Автоматическая пагинация — возвращает итератор элементов"""
        if params is None:
            params = {}

        page = 1
        params = dict(params)

        while True:
            params["page"] = page
            j = self._get(path, params=params)

            # если есть ключ результата
            if item_key in j:
                for item in j[item_key]:
                    yield item
            else:
                # fallback, если Stepik возвращает списки в других ключах
                for value in j.values():
                    if isinstance(value, list):
                        for item in value:
                            yield item
                        break

            # проверяем наличие следующей страницы
            if "meta" not in j or not j["meta"].get("has_next"):
                break

            page += 1

    # -----------------------
    # Удобные методы
    # -----------------------

    def get_course(self, course_id):
        return self._get(f"courses/{course_id}")

    def get_sections(self, course_id):
        return self._get("sections", params={"course": course_id})

    def get_units(self, course_id):
        return self._get("units", params={"course": course_id})

    def get_lessons(self, lesson_ids):
        ids = ",".join(map(str, lesson_ids))
        return self._get("lessons", params={"ids": ids})
