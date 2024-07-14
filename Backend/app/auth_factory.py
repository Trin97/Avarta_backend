from abc import ABC, abstractmethod
from app.user_auth import UserAuth

class AuthFactory(ABC):
    @abstractmethod
    def create_user_auth(self) -> UserAuth:
        pass
