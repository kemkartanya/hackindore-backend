from django.db import models
from common.models import TimeStampedModelMixin, SoftDeletableModelMixin


class EmployeeTypeChoices(models.TextChoices):
    ORDINARY = "ORDINARY", "Ordinary"
    ADMIN = "ADMIN", "Admin"


class DepartmentChoices(models.TextChoices):
    CITIZEN_SERVICES = "CITIZEN_SERVICES", "Citizen Services"
    PAYMENT_TAXES = "PAYMENT_TAXES", "Payment & Taxes"
    LICENSES_APPROVALS = "LICENSES_APPROVALS", "Licenses & Approvals"
    SERVICE_ON_REQUEST = "SERVICE_ON_REQUEST", "Service on Request"
    OTHERS = "OTHERS", "Others"


class RoleChoices(models.TextChoices):
    EMPLOYEE = "EMPLOYEE", "Employee"
    MANAGER = "MANAGER", "Manager"
    ADMIN = "ADMIN", "Admin"


# Create your models here.
class Employee(TimeStampedModelMixin, SoftDeletableModelMixin):
    email = models.CharField(max_length=100, unique=True, null=False, default="")
    mobile = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    role = models.CharField(
        max_length=100, choices=RoleChoices.choices, default=RoleChoices.EMPLOYEE
    )
    department = models.CharField(
        max_length=100,
        choices=DepartmentChoices.choices,
        default=DepartmentChoices.OTHERS,
    )
    type = models.CharField(
        max_length=100,
        choices=EmployeeTypeChoices.choices,
        default=EmployeeTypeChoices.ORDINARY,
    )
