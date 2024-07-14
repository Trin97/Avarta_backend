from app.auth_factory import AuthFactory
from app.user_auth import UserAuth

class UserAuthFactory(AuthFactory):
    def create_user_auth(self) -> UserAuth:
        return UserAuth()
