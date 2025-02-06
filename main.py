from fastapi import FastAPI
from Core.config_parameters import settings
from Database.database_settings import engine  # Make sure your database engine is set up
from Database.base_class import Base  # Ensure Base class is correctly imported with models
from Routes.routing_support import router as user_router  # Import the user router
from Users.Models.user_model import User
from Agency.Models.agency_model import Agency
from Subaccount.Model.subAccount_model import SubAccount
from History.Models.security_code_history_model import PasswordHistory
from Pipelines.Model.pipeline_model import Pipeline
from Lane.Model.lane_model import Lane
from Organizations.Models.organization_model import Organization
from Permissions.Model.permission_model import Permissions
from Tag.Model.tag_model import Tag
from Trigger.Model.trigger_model import Trigger
from Automation.Model.automation_model import Automation
from Action.Model.action_model import Action
from AgencySidebarOption.Model.agency_sidebar_model import AgencySidebarOption
from Automation_Instance.Model.automation_instance_model import AutomationInstance
from Funnel.Model.funnel_model import Funnel
from ClassName.Model.classname_model import ClassName
from Contact.Model.contact_model import Contact
from Funnel_Page.Model.funnel_page_model import FunnelPage
from Invitation.Model.invitation_model import Invitation
from Media.Model.media_model import Media
from Notification.Model.notification_model import Notification
from Subaccount_Sidebar_Option.Model.subaccount_sidebar_model import SubAccountSidebarOption
from Subscription.Model.subscription_model import Subscription
from Ticket.Model.ticket_model import Ticket
from Tag_to_Ticket.Model.tag_to_ticket_model import TagToTicket
from Add_Ons.Model.add_ons_model import AddOns
from External_Partners.external_partners import ExternalPartner
from Projects.Model.project_model import Project
app = FastAPI()
from dotenv import load_dotenv
load_dotenv()  # This loads the environment variables from the .env file

# Include the user router
app.include_router(user_router, prefix="/api/v1", tags=["Users"])

@app.get("/")
async def default():
    return {"message": "Welcome to the FastAPI application"}

@app.on_event("startup")
async def startup():
    print(f"Starting application in {settings.ENV} environment...")
    # This will create all tables defined in your models
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()
