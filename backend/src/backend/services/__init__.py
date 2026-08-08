# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃ services: init                                                                                   ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

from .admin import AdminService
from .auth import AuthService
from .cache import CacheService
from .company import CompanyService
from .eligibility import EligibilityService
from .email import EmailService
from .export import ExportService
from .interview import InterviewService
from .notification import NotificationService
from .offer_letter import OfferLetterService
from .placement import PlacementService
from .report import ReportService
from .student import StudentService

__all__ = [
    "AdminService",
    "AuthService",
    "CacheService",
    "CompanyService",
    "EligibilityService",
    "EmailService",
    "ExportService",
    "InterviewService",
    "NotificationService",
    "OfferLetterService",
    "PlacementService",
    "ReportService",
    "StudentService",
]
