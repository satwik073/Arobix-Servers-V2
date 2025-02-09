from Mapings.mapping_attributes import role_permissions
from Configs.configuration import Role



def get_default_permissions(role: str):
    return role_permissions.get(role, role_permissions[Role.SUPER_ADMIN])