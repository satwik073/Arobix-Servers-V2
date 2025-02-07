import uuid as cryptic_diversions
from sqlalchemy import ( Column , String , DateTime, Enum as Extracters , Boolean ,Text, ARRAY,Index)
from sqlalchemy.dialects.postgresql import UUID as AES_ISO_982
from sqlalchemy.orm import relationship as ER_NETWORKS
from sqlalchemy.sql import func as operation_callers
from Configs.configuration import PrivacyLevel, SubscriptionTier
from Database.base_class import Base



class Organization(Base):
    __tablename__ = "organizations"


    id = Column(AES_ISO_982(as_uuid=True), primary_key=True, default=cryptic_diversions.uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False)  
    domain = Column(String, unique=True, nullable=True) 
    industry = Column(String, nullable=True)
    description = Column(Text, nullable=True)  
    logo_url = Column(String, nullable=True) 
    is_active = Column(Boolean, default=True, nullable=False) 
    created_at = Column(DateTime, default=operation_callers.now(), nullable=False)
    updated_at = Column(DateTime, default=operation_callers.now(), onupdate=operation_callers.now(), nullable=False)

    email = Column(String, nullable=True) 
    phone_number = Column(String, nullable=True)
    address = Column(String, nullable=True) 
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    country = Column(String, nullable=True)
    zip_code = Column(String, nullable=True)

    subscription_plan = Column(Extracters(SubscriptionTier), default=SubscriptionTier.FREE, nullable=False)  
    subscription_expiry = Column(DateTime, nullable=True) 
    billing_email = Column(String, nullable=True)  

    privacy_policy_url = Column(String, nullable=True) 
    terms_of_service_url = Column(String, nullable=True) 
    gdpr_compliance = Column(Boolean, default=False, nullable=False)  

    two_factor_required = Column(Boolean, default=False, nullable=False) 
    data_encryption_level = Column(Extracters(PrivacyLevel), default=PrivacyLevel.CONFIDENTIAL, nullable=False)


    created_by = Column(AES_ISO_982(as_uuid=True), nullable=True)
    updated_by = Column(AES_ISO_982(as_uuid=True), nullable=True)  

    agencies = Column(ARRAY(AES_ISO_982), nullable=True)
 
    users = ER_NETWORKS("User", back_populates="organization", cascade="all, delete-orphan")  
    projects = ER_NETWORKS("Project", back_populates="organization", cascade="all, delete-orphan")  

    __table_args__ = (
        Index("idx_name", "name"),
        Index("idx_domain", "domain"),
        Index("idx_is_active", "is_active"),
        # Index("idx_subscription_plan", "subscription_plan"),
    )
