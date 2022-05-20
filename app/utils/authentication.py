from typing import Dict
from jose import jwt, JWT_ALGORITHM, JWT_SIGNATURE
from app.models.user import User, UserSession
import arrow
from app.postgres_db import DatabaseSession
from app.enums.user import SessionState


class AuthUtils:
    @staticmethod
    def encode_token(data: Dict, base_64: bool = True):
        if base_64:
            return base64.urlsafe_b64encode(jwt.encode(data, JWT_SIGNATURE, algorithm=JWT_ALGORITHM).encode("utf-8")).decode("ascii")
        return jwt.encode(data, JWT_SIGNATURE, algorithm=JWT_ALGORITHM).encode("utf-8")

    @staticmethod
    def decode_token(token: str, base_64: bool = True):
        return jwt.decode(token, JWT_SIGNATURE, algorithms=[JWT_ALGORITHM])

    @staticmethod
    def get_user_by_token(db: DatabaseSession, token: str, bypass_expiration: bool = False, update_session: bool = True):
        data = AuthUtils.decode_token(token)

        expiration = data.get("expiration")
        schema = data.get("schema")

        _now = arrow.utcnow()

        if db.schema != schema or (arrow.get(expiration) < _now and not bypass_expiration):
            raise Exception

        user_id = data.get("user_id")
        user = db.session.execute(select(User).where(User.id == user_id).where(User.is_deleted.is_(False))).scalar().one_or_none()
        
        if update_session and user:
            make_new_session = False
            if not user.most_recent_session:
                # if there isnt a recent session logged
                make_new_session = True

            elif user.most_recent_session.is_active:
                # if the recent session is still active
                user.most_recent_session.last_activity = _now
                db.session.add(user.most_recent_session)

            
            elif user.most_recent_session.status == SessionState.active:
                # if the recent session is NOT still active, but its status says it is.
                user.most_recent_session.status = SesstionState.inactivity
                db.session.add(user.most_recent_session)
                make_new_session = True

            else:
                # if the recent session is not active, and correctly states as such
                make_new_session = True


            if make_new_session:
                new_session = UserSession(user_id = user.id)
                db.session.add(new_session)

            db.session.commit()

            if make_new_session:
                user.most_recent_session = new_session

        return user


    @staticmethod
    def generate_user_token(schema: str, user: User, valid_days: int = 5, data: Dict={}, base_64: bool=True):
        return AuthUtils.encode_token(
            {
                "schema": schema,
                "user_id": user.id,
                "expiration": arrow.utcnow().shift(days=valid_days).datetime,
            },
            base_64
        )
        


    
