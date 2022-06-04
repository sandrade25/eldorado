from contextvars import ContextVar

from app.enums.context import ContextEnum

context = {}


class ContextManager:
    @staticmethod
    def create_empty_context(key: ContextEnum):
        if context.get(key.value):
            return

        context[key.value] = ContextVar(key.value)

    @staticmethod
    def set(key: ContextEnum, value):
        # check if key is in contextEnum
        # if not dont allow/raise exeption

        if not context.get(key.value):
            context[key.value] = ContextVar(key.value)

        context[key.value].set(value)

    @staticmethod
    def get(key: ContextEnum, default=None):
        context_object = context.get(key.value)

        if not context_object:
            return None

        return context_object.get(default)
