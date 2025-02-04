import uuid
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Enum,
    Boolean,
    JSON,
    Integer,
    Float,
    Text,
    Index
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Configs.configuration import (
    SubscriptionTier,
    PrivacyLevel,
    AccountStatus,
    Role,
    LanguagePreference
)
from Database.base_class import Base


class SubAccount(Base):
    __tablename__ = "sub_account"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    connectAccountId = Column(String, default="", nullable=False)
    name = Column(String, nullable=False)
    subAccountLogo = Column(String, nullable=True)
    createdAt = Column(DateTime, default=func.now(), nullable=False)
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    companyEmail = Column(String, unique=True, nullable=False)
    companyPhone = Column(String, nullable=False)
    goal = Column(Integer, default=5, nullable=False)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    zipCode = Column(String, nullable=True)
    state = Column(String, nullable=True)
    country = Column(String, nullable=True)

    agencyId = Column(UUID(as_uuid=True), ForeignKey("agencies.id", ondelete="CASCADE"), nullable=False)
    agency = relationship("Agency", back_populates="subAccounts")

    isActive = Column(Boolean, default=True, nullable=False)
    subscriptionStatus = Column(Enum(SubscriptionTier), default=SubscriptionTier.FREE, nullable=False)
    miscdata = Column(JSON, default={}, nullable=True)
    preferences = Column(JSON, default={"theme": "default", "currency": "USD"}, nullable=True)
    notificationSettings = Column(JSON, default={"email": True, "sms": False, "push": True}, nullable=True)
    integrations = Column(JSON, default={"crm": None, "email_marketing": None}, nullable=True)
    auditLogs = Column(JSON, default=[], nullable=True)
    revenue = Column(Float, default=0.0, nullable=True)
    tags = Column(JSON, default=[], nullable=True)
    taxId = Column(String, nullable=True)
    billingAddress = Column(String, nullable=True)
    termsAndConditions = Column(String, nullable=True)
    privacyPolicy = Column(String, nullable=True)

    employeeCount = Column(Integer, nullable=True)
    revenueForecast = Column(Float, default=0.0, nullable=True)
    annualGrowthRate = Column(Float, default=0.0, nullable=True)
    businessSector = Column(String, nullable=True)
    companyWebsite = Column(String, nullable=True)
    externalResources = Column(JSON, default=[], nullable=True)
    contractStartDate = Column(DateTime, nullable=True)
    contractEndDate = Column(DateTime, nullable=True)
    serviceLevelAgreement = Column(Text, nullable=True)

    sidebarOptions = relationship("SubAccountSidebarOption", back_populates="subAccount", cascade="all, delete-orphan")
    permissions = relationship("Permissions", back_populates="subAccount", cascade="all, delete-orphan")
    funnels = relationship("Funnel", back_populates="subAccount", cascade="all, delete-orphan")
    media = relationship("Media", back_populates="subAccount", cascade="all, delete-orphan")
    contacts = relationship("Contact", back_populates="subAccount", cascade="all, delete-orphan")
    triggers = relationship("Trigger", back_populates="subAccount", cascade="all, delete-orphan")
    automations = relationship("Automation", back_populates="subAccount", cascade="all, delete-orphan")
    pipelines = relationship("Pipeline", back_populates="subAccount", cascade="all, delete-orphan")
    tags = relationship("Tag", back_populates="subAccount", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="subAccount", cascade="all, delete-orphan")
    subscription = relationship("Subscription", back_populates="subAccount", uselist=False)


    externalPartners = relationship("ExternalPartner", back_populates="subAccounts", secondary="sub_account_external_partner_association")
    subAccountTeamMembers = relationship("User", back_populates="subAccount", secondary="sub_account_user_association")

    performanceMetrics = Column(JSON, default={"user_growth": 0, "revenue_growth": 0}, nullable=True)
    # Indexes for faster querying
    __table_args__ = (
        Index("idx_sub_account_name", "name"),
        Index("idx_agency_id", "agencyId"),
        # Index("idx_subscription_status", "subscriptionStatus"),
        # Index("idx_subscription_plan", "subscriptionStatus"),
    )
