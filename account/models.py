import os
import uuid

from django.db import models
from django.db.models.signals import post_save
from shortuuid.django_fields import ShortUUIDField

from userauths.models import User

ACCOUNT_STATUS = (
    ("active", "Active"),
    ("pending", "Pending"),
    ("in-active", "In-active"),
)

MARITAL_STATUS = (("married", "Married"), ("single", "Single"), ("other", "Other"))

GENDER = (("male", "Male"), ("female", "Female"), ("other", "Other"))


IDENTITY_TYPE = (
    ("national_id_card", "National ID Card"),
    ("drivers_licence", "Drives Licence"),
    ("international_passport", "International Passport"),
)


def user_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s_%s" % (instance.id, ext)
    return "user_{0}/{1}".format(instance.user.id, filename)


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    account_number = ShortUUIDField(
        unique=True, length=10, max_length=25, prefix="217", alphabet="1234567890"
    )
    account_id = ShortUUIDField(
        unique=True, length=7, max_length=25, prefix="DEX", alphabet="1234567890"
    )
    pin_number = ShortUUIDField(
        unique=True, length=4, max_length=7, alphabet="1234567890"
    )
    red_code = ShortUUIDField(
        unique=True, length=10, max_length=20, alphabet="abcdefgh1234567890"
    )
    account_status = models.CharField(
        max_length=100, choices=ACCOUNT_STATUS, default="in-active"
    )
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    kyc_submitted = models.BooleanField(default=False)
    kyc_confirmed = models.BooleanField(default=False)
    recommended_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="recommended_by",
    )
    review = models.CharField(max_length=100, null=True, blank=True, default="Review")

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return f"{self.user}"


class KYC(models.Model):
    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account = models.OneToOneField(
        Account, on_delete=models.CASCADE, null=True, blank=True
    )
    full_name = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="kyc", default="default.jpg")
    marrital_status = models.CharField(choices=MARITAL_STATUS, max_length=40)
    gender = models.CharField(choices=GENDER, max_length=40)
    identity_type = models.CharField(choices=IDENTITY_TYPE, max_length=140)
    identity_image = models.ImageField(upload_to="kyc", null=True, blank=True)
    date_of_birth = models.DateField(auto_now_add=False)
    signature = models.ImageField(upload_to="kyc")

    # Address
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    # Contact Detail
    mobile = models.CharField(max_length=1000)
    fax = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user}"

    class Meta:
        ordering = ["-updated_at"]

    def save(self, *args, **kwargs) -> models.Model:
        if KYC.objects.filter(pk=self.pk).exists():
            # if updated delete previous pictures
            original_obj = KYC.objects.get(pk=self.pk)
            if original_obj.image and original_obj.image != self.image:
                if os.path.isfile(original_obj.image.path):
                    os.remove(original_obj.image.path)
            if (
                original_obj.identity_image
                and original_obj.identity_image != self.identity_image
            ):
                if os.path.isfile(original_obj.identity_image.path):
                    os.remove(original_obj.identity_image.path)
            if original_obj.signature and original_obj.signature != self.signature:
                if os.path.isfile(original_obj.signature.path):
                    os.remove(original_obj.signature.path)
        return super(KYC, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs) -> None:
        # Delete the file associated with the model instance
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        if self.identity_image:
            if os.path.isfile(self.identity_image.path):
                os.remove(self.identity_image.path)
        if self.signature:
            if os.path.isfile(self.signature.path):
                os.remove(self.signature.path)
        super(KYC, self).delete(*args, **kwargs)
