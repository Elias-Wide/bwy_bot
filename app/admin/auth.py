"""Модуль аутенфиукации adminpage."""

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.core.config import settings


class AdminAuth(AuthenticationBackend):
    """Настройка бэкенда аутенфикации."""

    async def login(self, request: Request) -> bool:
        """Метод содержит логику при входе в систему."""
        form = await request.form()
        username, password = form['username'], form['password']
        if username == settings.username and password == settings.password:
            request.session.update({'token': settings.admin_auth_secret})
        return True

    async def logout(self, request: Request) -> bool:
        """Метод содержит логику выхода из системы."""
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        """Метод содержит логику аутенфикации."""
        token = request.session.get('token')
        if not token:
            return False
        return True
