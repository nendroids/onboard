# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃ schemas: init                                                                                    ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

from .application import (
    ApplicationCreateSchema,
    ApplicationSchema,
    ApplicationStatusUpdateSchema,
)
from .common import ErrorSchema, PaginationSchema
from .company import CompanyApprovalSchema, CompanySchema, CompanyUpdateSchema
from .drive import (
    DriveSchema,
    JobApprovalSchema,
    JobCreateSchema,
    JobSchema,
    JobUpdateSchema,
)
from .interview import (
    InterviewCreateSchema,
    InterviewSchema,
    InterviewUpdateSchema,
)
from .notification import NotificationSchema
from .placement import PlacementSchema
from .student import StudentSchema, StudentUpdateSchema
from .user import UserLoginSchema, UserRegisterSchema, UserSchema

__all__ = [
    "ApplicationCreateSchema",
    "ApplicationSchema",
    "ApplicationStatusUpdateSchema",
    "CompanyApprovalSchema",
    "CompanySchema",
    "CompanyUpdateSchema",
    "DriveSchema",
    "ErrorSchema",
    "InterviewCreateSchema",
    "InterviewSchema",
    "InterviewUpdateSchema",
    "JobApprovalSchema",
    "JobCreateSchema",
    "JobSchema",
    "JobUpdateSchema",
    "NotificationSchema",
    "PaginationSchema",
    "PlacementSchema",
    "StudentSchema",
    "StudentUpdateSchema",
    "UserLoginSchema",
    "UserRegisterSchema",
    "UserSchema",
]
