from contextvars import ContextVar

from app.enums.context import ContextEnum

context = {}


class ContextManager:
    @staticmethod
    def set(key: ContextEnum, value):
        # check if key is in contextEnum
        # if not dont allow/raise exeption

        if not context.get(key):
            context[key] = ContextVar(key)

        context[key].set(value)

    @staticmethod
    def get(key: ContextEnum, default=None):
        return context[key].get(default)
