from enum import Enum


class PermissionsEnum(str, Enum):
    can_create_user = "can create user"
    can_delete_user = "can delete user"
    can_edit_user = "can edit user"
    can_view_other_user_data = "can view other user data"
