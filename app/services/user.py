from app.models.user import User, UserSession
from app.services.exceptions import ServiceDataError
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound


class UserService:
    def __init__(self, db, user_id: int, update_session: bool = False):
        self.db = db
        self.user = self.get_user(user_id)

    def get_user(self, user_id: int):
        try:
            user = self.db.session.execute(
                select(User).where(User.id == user_id)
            ).scalar_one_or_none()
            return user
        except NoResultFound:
            raise

    def _assert_user(self):
        if not self.user:
            raise ServiceDataError

    def current_session(self):
        self._assert_user()
