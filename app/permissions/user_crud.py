from app.permissions.enum import PermissionsEnum

from app.utils.depends import Permissions


can_create_user = Permissions([PermissionsEnum.can_create_user])
can_delete_user = Permissions([PermissionsEnum.can_delete_user])
can_edit_user = Permissions([PermissionsEnum.can_edit_user])
can_view_other_user_data = Permissions([PermissionsEnum.can_view_other_user_data])
