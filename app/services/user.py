import datetime as dt

import arrow
from app.enums.user import SessionState
from app.model_operators.user import UserOperator
from app.models.user import User, UserSession
from app.postgres_db import DatabaseSession
from app.schemas.user import UserCreate
from app.services.exceptions import ServiceDataError
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound


class UserService:
    user_operator: UserOperator = UserOperator

    @staticmethod
    def create_users(db: DatabaseSession, users: UserCreate, commit: bool = False):
        UserService.user_operator.batch_create(db, users, commit=commit)

    def __init__(
        self,
        db: DatabaseSession,
        user_id: int,
        update_session_to_now: bool = False,
        non_deleted: bool = True,
        include_most_recent_session: bool = True,
        include_permissions: bool = True,
    ):
        self.db = db
        (
            self.user,
            self.most_recent_session,
            self.permission_ids,
            self.permission_names,
        ) = self.user_operator.get_user_by_id(
            db,
            user_id,
            non_deleted,
            include_most_recent_session=include_most_recent_session,
            include_permissions=include_permissions,
        )
        if update_session_to_now:
            self.update_session()

    def _assert_user(self):
        if not self.user:
            raise ServiceDataError

    def current_session(self):
        self._assert_user()
        return self.most_recent_session

    def update_session(self, timestamp: dt.datetime = None):

        if not timestamp:
            timestamp = arrow.utcnow().datetime

        self._assert_user()

        make_new_session = False
        if not self.most_recent_session:
            # if there isnt a recent session logged
            make_new_session = True

        elif self.most_recent_session.is_active:
            # if the recent session is still active
            self.most_recent_session.last_activity = timestamp
            self.db.session.add(self.most_recent_session)

        elif self.most_recent_session.status == SessionState.active:
            # if the recent session is NOT still active, but its status says it is.
            self.most_recent_session.status = SessionState.inactivity
            self.db.session.add(self.most_recent_session)
            make_new_session = True

        else:
            # if the recent session is not active, and correctly states as such
            make_new_session = True

        if make_new_session:
            new_session = UserSession(user_id=self.user.id)
            self.db.session.add(new_session)

        self.db.session.commit()

        if make_new_session:
            self.most_recent_session = new_session
