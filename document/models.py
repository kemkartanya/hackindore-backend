from django.db import models

from common.models import TimeStampedModelMixin, SoftDeletableModelMixin


class DocTypeChoices(models.TextChoices):
    NOC = "NOC", "Noc"
    BIRTH_CERTIFICATE = "BIRTH_CERTIFICATE", "Birth Certificate"
    DEATH_CERTIFICATE = "DEATH_CERTIFICATE", "Death Certificate"
    SAMGRA = "SAMGRA", "Samgra"


# Create your models here.
class Document(TimeStampedModelMixin, SoftDeletableModelMixin):
    file = models.FileField(upload_to='pdfs/', default=None)
    type = models.CharField(
        max_length=100,
        choices=DocTypeChoices.choices,
        default=DocTypeChoices.NOC,
    )
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE)