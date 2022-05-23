import datetime as dt

import arrow
from app.enums.user import SessionState
from app.models.user import User, UserSession
from app.services.exceptions import ServiceDataError
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound


class UserService:
    def __init__(
        self, db, user_id: int, update_session_to_now: bool = False, non_deleted: bool = True
    ):
        self.db = db
        self.user = self.get_user(user_id, non_deleted)
        if update_session_to_now:
            self.update_session()

    def get_user(self, user_id: int, non_deleted: bool = True):
        stmt = select(User).where(User.id == user_id)
        if non_deleted:
            stmt = stmt.where(User.is_deleted.is_(False))

        try:
            user = self.db.session.execute(stmt).scalar_one_or_none()
            return user
        except NoResultFound:
            raise

    def _assert_user(self):
        if not self.user:
            raise ServiceDataError

    def current_session(self):
        self._assert_user()
        return self.user.most_recent_session

    def update_session(self, timestamp: dt.datetime = None):

        if not timestamp:
            timestamp = arrow.utcnow().datetime

        self._assert_user()

        make_new_session = False
        if not self.user.most_recent_session:
            # if there isnt a recent session logged
            make_new_session = True

        elif self.user.most_recent_session.is_active:
            # if the recent session is still active
            self.user.most_recent_session.last_activity = timestamp
            self.db.session.add(self.user.most_recent_session)

        elif self.user.most_recent_session.status == SessionState.active:
            # if the recent session is NOT still active, but its status says it is.
            self.user.most_recent_session.status = SessionState.inactivity
            self.db.session.add(self.user.most_recent_session)
            make_new_session = True

        else:
            # if the recent session is not active, and correctly states as such
            make_new_session = True

        if make_new_session:
            new_session = UserSession(user_id=self.user.id)
            self.db.session.add(new_session)

        self.db.session.commit()

        if make_new_session:
            self.user.most_recent_session = new_session
