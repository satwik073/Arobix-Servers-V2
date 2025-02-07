from Mapings.mapping_attributes import role_permissions
from Configs.configuration import Role



def get_permissions_for_role(role: str):
    return role_permissions.get(role, role_permissions[Role.SUPER_ADMIN])