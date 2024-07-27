from django.db import models
from common.models import TimeStampedModelMixin, SoftDeletableModelMixin


class StatusChoices(models.TextChoices):
    OPEN = "OPEN", "Open"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    RESOLVED = "RESOLVED", "Resolved"
    CLOSED = "CLOSED", "Closed"


# Create your models here.
class Ticket(TimeStampedModelMixin, SoftDeletableModelMixin):
    query = models.TextField()
    assigned_to = models.ForeignKey(
        "employee.Employee",
        on_delete=models.CASCADE,
        related_name="assigned_tickets",
        null=True,
    )
    user = models.ForeignKey(
        "employee.Employee", on_delete=models.CASCADE, related_name="user_tickets"
    )
    status = models.CharField(
        max_length=100, choices=StatusChoices.choices, default=StatusChoices.OPEN
    )
