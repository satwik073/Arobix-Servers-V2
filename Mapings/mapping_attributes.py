from Configs.configuration import Permissions, Role

role_permissions = {
    Role.SUPER_ADMIN: [
        Permissions.__CREATE__, Permissions.__READ__, Permissions.__UPDATE__, Permissions.__DELETE__,
        Permissions.__MANAGE__, Permissions.__SETTINGS__, Permissions.__USERS__, Permissions.__ROLES__,
        Permissions.__PERMISSIONS__, Permissions.__AUDIT_LOGS__, Permissions.__INTEGRATION_SETTINGS__,
        Permissions.__EXECUTE__, Permissions.__VIEW_LOGS__, Permissions.__INTEGRATIONS__, Permissions.__API_KEYS__,
        Permissions.__SECURITY__, Permissions.__COMPLIANCE__, Permissions.__ANALYTICS__, Permissions.__CUSTOMER_FEEDBACK__,
    ],
    Role.AGENCY_OWNER: [
        Permissions.__CREATE__, Permissions.__READ__, Permissions.__UPDATE__, Permissions.__DELETE__,
        Permissions.__MANAGE__, Permissions.__USERS__, Permissions.__ROLES__, Permissions.__PERMISSIONS__,
        Permissions.__AUDIT_LOGS__, Permissions.__INTEGRATION_SETTINGS__, Permissions.__VIEW_LOGS__,
    ],
    Role.AGENCY_ADMIN: [
        Permissions.__CREATE__, Permissions.__READ__, Permissions.__UPDATE__, Permissions.__DELETE__,
        Permissions.__MANAGE__, Permissions.__USERS__, Permissions.__ROLES__, Permissions.__PERMISSIONS__,
    ],
    Role.SUBACCOUNT_USER: [
        Permissions.__READ__, Permissions.__UPDATE__, Permissions.__CREATE__,Permissions.__WRITE__
    ],
    Role.SUBACCOUNT_GUEST: [
        Permissions.__READ__, Permissions.__ACCESS__,
    ],
    Role.CUSTOMER: [
        Permissions.__READ__, Permissions.__ACCESS__,
    ],
    Role.SUPPORT: [
        Permissions.__READ__, Permissions.__UPDATE__, Permissions.__CREATE__,
    ],
    Role.AUDITOR: [
        Permissions.__READ__, Permissions.__ACCESS__, Permissions.__VIEW_LOGS__,
    ],
    Role.TEAM_LEAD: [
        Permissions.__CREATE__, Permissions.__READ__, Permissions.__UPDATE__,
    ],
    Role.PRODUCT_MANAGER: [
        Permissions.__CREATE__, Permissions.__READ__, Permissions.__UPDATE__,
    ],
    Role.SALES_REPRESENTATIVE: [
        Permissions.__READ__, Permissions.__CREATE__,
    ],
    Role.DEVELOPER: [
        Permissions.__READ__, Permissions.__CREATE__, Permissions.__UPDATE__,
    ],
    Role.MARKETING_SPECIALIST: [
        Permissions.__READ__, Permissions.__CREATE__,
    ],
    Role.DATA_ANALYST: [
        Permissions.__READ__, Permissions.__ACCESS__,
    ],
    Role.HR_MANAGER: [
        Permissions.__CREATE__, Permissions.__READ__, Permissions.__UPDATE__, Permissions.__DELETE__,
        Permissions.__EMPLOYEES__, Permissions.__RECRUITMENT__, Permissions.__APPROVE_HIRING__,
        Permissions.__COMPENSATION__, Permissions.__PERFORMANCE_REVIEWS__, Permissions.__PAYROLL__,
        Permissions.__EMPLOYEE_BENEFITS__, Permissions.__TAXES__,
    ],
    Role.FINANCE_MANAGER: [
        Permissions.__CREATE__, Permissions.__READ__, Permissions.__UPDATE__, Permissions.__DELETE__,
        Permissions.__FINANCES__, Permissions.__BILLING__, Permissions.__APPROVE_EXPENSES__,
        Permissions.__TAXES__,
    ],
    Role.LEGAL: [
        Permissions.__READ__, Permissions.__CREATE__, Permissions.__UPDATE__,
        Permissions.__CONTRACTS__, Permissions.__DOCUMENTS__,
    ],
    Role.ADMINISTRATOR: [
        Permissions.__CREATE__, Permissions.__READ__, Permissions.__UPDATE__, Permissions.__DELETE__,
        Permissions.__MANAGE__, Permissions.__SETTINGS__, Permissions.__USERS__,
    ],
    Role.CONTENT_MANAGER: [
        Permissions.__CREATE__, Permissions.__READ__, Permissions.__UPDATE__,
        Permissions.__CONTENT__, Permissions.__MARKETING_CAMPAIGNS__,
    ],
    Role.INTEGRATION_MANAGER: [
        Permissions.__CREATE__, Permissions.__READ__, Permissions.__UPDATE__,
        Permissions.__INTEGRATIONS__, Permissions.__API_KEYS__,
    ],
    Role.CUSTOMER_SUPPORT: [
        Permissions.__READ__, Permissions.__CREATE__, Permissions.__UPDATE__,
        Permissions.__TICKETS__, Permissions.__COMPLAINTS__,
    ],
    Role.INTERNAL_AUDITOR: [
        Permissions.__READ__, Permissions.__AUDIT_LOGS__, Permissions.__VIEW_AUDIT_LOGS__,
    ],
    Role.PRODUCT_OWNER: [
        Permissions.__CREATE__, Permissions.__READ__, Permissions.__UPDATE__,
        Permissions.__PRODUCTS__, Permissions.__PROJECTS__,
    ],
    Role.SALES_MANAGER: [
        Permissions.__CREATE__, Permissions.__READ__, Permissions.__UPDATE__,
        Permissions.__SALES__, Permissions.__MARKETING_CAMPAIGNS__,
    ],
    Role.OPERATIONS_MANAGER: [
        Permissions.__CREATE__, Permissions.__READ__, Permissions.__UPDATE__,
        Permissions.__OPERATIONS__, Permissions.__SUPPLY_CHAIN__,
    ],
    Role.ACCOUNTANT: [
        Permissions.__CREATE__, Permissions.__READ__, Permissions.__UPDATE__,
        Permissions.__FINANCES__, Permissions.__PAYROLL__,
    ],
    Role.IT_MANAGER: [
        Permissions.__CREATE__, Permissions.__READ__, Permissions.__UPDATE__,
        Permissions.__SYSTEM_ADMIN__, Permissions.__SECURITY__, Permissions.__BACKUPS__,
    ],
    Role.MARKETING_DIRECTOR: [
        Permissions.__CREATE__, Permissions.__READ__, Permissions.__UPDATE__,
        Permissions.__MARKETING_CAMPAIGNS__, Permissions.__CONTENT__,
    ],
    Role.BUSINESS_ANALYST: [
        Permissions.__READ__, Permissions.__ANALYTICS__, Permissions.__REPORTS__,
    ],
    Role.CUSTOMER_RELATIONS_MANAGER: [
        Permissions.__CREATE__, Permissions.__READ__, Permissions.__UPDATE__,
        Permissions.__CUSTOMER_FEEDBACK__, Permissions.__CUSTOMER_SUCCESS_MANAGER__,
    ],
    Role.PROCUREMENT_MANAGER: [
        Permissions.__READ__, Permissions.__CREATE__, Permissions.__UPDATE__,
        Permissions.__SUPPLY_CHAIN__, Permissions.__ORDERS__,
    ],
    Role.SECURITY_ADMIN: [
        Permissions.__READ__, Permissions.__SECURITY__, Permissions.__ACCESS_CONTROL__,
    ],
    Role.DATA_SCIENTIST: [
        Permissions.__READ__, Permissions.__ANALYTICS__, Permissions.__REPORTS__,
    ],
    Role.SYSTEM_ADMIN: [
        Permissions.__CREATE__, Permissions.__READ__, Permissions.__UPDATE__, Permissions.__DELETE__,
        Permissions.__SYSTEM_ADMIN__, Permissions.__SECURITY__, Permissions.__BACKUPS__,
    ],
    Role.UX_UI_DESIGNER: [
        Permissions.__READ__, Permissions.__CREATE__, Permissions.__UPDATE__,
        Permissions.__PROJECTS__, Permissions.__USER_PROFILE__,
    ],
    Role.BUSINESS_DEVELOPER: [
        Permissions.__READ__, Permissions.__CREATE__, Permissions.__UPDATE__,
        Permissions.__PARTNERSHIPS__, Permissions.__SALES__,
    ],
    Role.SOCIAL_MEDIA_MANAGER: [
        Permissions.__READ__, Permissions.__CREATE__, Permissions.__UPDATE__,
        Permissions.__CONTENT__, Permissions.__MARKETING_CAMPAIGNS__,
    ],
    Role.COMPLIANCE_OFFICER: [
        Permissions.__READ__, Permissions.__COMPLIANCE__, Permissions.__SECURITY__,
    ],
    Role.QUALITY_ASSURANCE: [
        Permissions.__READ__, Permissions.__CREATE__, Permissions.__UPDATE__,
        Permissions.__PROJECTS__, Permissions.__TESTING__,
    ],
    Role.DEVOPS_ENGINEER: [
        Permissions.__READ__, Permissions.__CREATE__, Permissions.__UPDATE__,
        Permissions.__SECURITY__, Permissions.__SYSTEM_ADMIN__,
    ],
    Role.SYSTEM_ARCHITECT: [
        Permissions.__READ__, Permissions.__CREATE__, Permissions.__UPDATE__,
        Permissions.__SYSTEM_ADMIN__, Permissions.__SECURITY__,
    ],
    Role.CUSTOMER_SUCCESS_MANAGER: [
        Permissions.__READ__, Permissions.__CREATE__, Permissions.__UPDATE__,
        Permissions.__CUSTOMER_FEEDBACK__, Permissions.__CUSTOMER_SUCCESS_MANAGER__,
    ],
    Role.SOFTWARE_ENGINEER: [
        Permissions.__READ__, Permissions.__CREATE__, Permissions.__UPDATE__,
        Permissions.__PROJECTS__, Permissions.__SYSTEM_ADMIN__,
    ],
}
