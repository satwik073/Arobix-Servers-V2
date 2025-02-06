import uuid as cryptic_diversions
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Enum as Extracters,
    Boolean,
    JSON,
    Index,
    Float,
)
from sqlalchemy.dialects.postgresql import UUID as AGN_AES_ISO_639
from sqlalchemy.orm import relationship as ER_NETWORKS
from sqlalchemy.sql import func as operation_callers
from Configs.configuration import (
    SubscriptionTier,
    __NULLABLES__,
)
from Database.base_class import Base

class Agency(Base):
    __tablename__ = "agencies"

    id = Column(AGN_AES_ISO_639(as_uuid=True), primary_key=True, default=cryptic_diversions.uuid4, nullable=False)
    connectAccountId = Column(String, default=__NULLABLES__.EMPTY_STATE, nullable=False)
    customerId = Column(String, default=__NULLABLES__.EMPTY_STATE, nullable=False)
    name = Column(String, nullable=False)
    agencyLogo = Column(String, nullable=False)
    companyEmail = Column(String, unique=True, nullable=False)
    companyPhone = Column(String, nullable=False)
    whiteLabel = Column(Boolean, default=True, nullable=False)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    zipCode = Column(String, nullable=True)
    state = Column(String, nullable=True)
    country = Column(String, nullable=True)
    goal = Column(JSON, default=lambda: {"goal_amount": 0, "subscription_type_config": SubscriptionTier.ENTERPRISE})
    createdAt = Column(DateTime, default=operation_callers.now(), nullable=False)
    updatedAt = Column(DateTime, default=operation_callers.now(), onupdate=operation_callers.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    subscription_status = Column(
        Extracters(SubscriptionTier, name="subscriptiontier_enum"),  # Added name here
        default=SubscriptionTier.FREE,
        nullable=False
    )
    annual_revenue = Column(Float, default=0.0, nullable=True)
    miscdata = Column(JSON, default={}, nullable=True)
    business_sector = Column(String, nullable=True)
    tags = Column(JSON, default=lambda: [], nullable=True)
    preferences = Column(JSON, default=lambda: {"dashboard_theme": "default", "currency": "USD"})
    notification_settings = Column(JSON, default=lambda: {"email": True, "sms": False, "push": True})
    integrations = Column(JSON, default=lambda: {"crm": None, "email_marketing": None})
    tax_id = Column(String, nullable=True)
    billing_address = Column(String, nullable=True)
    terms_and_conditions = Column(String, nullable=True)
    privacy_policy = Column(String, nullable=True)


    Users = ER_NETWORKS("User", back_populates="agency", cascade="all, delete-orphan", lazy="joined")
    subAccounts = ER_NETWORKS("SubAccount", back_populates="agency", cascade="all, delete-orphan", lazy="joined")
    sidebar_options = ER_NETWORKS("AgencySidebarOption", back_populates="agency", cascade="all, delete-orphan", lazy="joined")
    invitations = ER_NETWORKS("Invitation", back_populates="agency", cascade="all, delete-orphan", lazy="joined")
    notifications = ER_NETWORKS("Notification", back_populates="agency", cascade="all, delete-orphan", lazy="joined")
    subscriptions = ER_NETWORKS("Subscription", back_populates="agency", uselist=False, lazy="joined")
    add_ons = ER_NETWORKS("AddOns", back_populates="agency", cascade="all, delete-orphan", lazy="joined")

    # Indexes
    __table_args__ = (
        Index("idx_agency_name", "name"),
        Index("idx_subscription_status", "subscription_status"),
        Index("idx_connectAccountId", "connectAccountId"),  # Fixed typo here (connectAaccountId -> connectAccountId)
        Index("idx_customer_id", "customerId"),  # Fixed typo here (customer_id -> customerId)
    )
