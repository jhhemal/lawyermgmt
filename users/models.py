from django.db import models
from django.contrib.auth.models import AbstractUser

def upload_directory(instance, filename):
    return f"profile/{instance.username}/{filename}"


class Category(models.Model):
    name = models.CharField(verbose_name='Lawyer Category', max_length=50)

    def __str__(self):
        return self.name

### Create your models here.


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'admin'),
        (2, 'lawyer'),
        (3, 'clients'),
    )
    mobile_no = models.CharField("Mobile Number", max_length=11)
    address = models.TextField("Address")
    category = models.ForeignKey(Category, verbose_name='Select Lawyer Category', on_delete=models.CASCADE, blank=True, null=True)
    membership_id = models.CharField("Bar Membership ID", max_length=15, blank=True, null=True)
    image = models.ImageField("Profile Picture", upload_to=upload_directory, default='default.jpg')
    user_type = models.PositiveIntegerField(choices=USER_TYPE_CHOICES, default=1, blank=True, null=True)
    bio = models.TextField("Bio", null=True, blank=True)
    exp = models.CharField("Experience", max_length=2, null=True, blank=True)
    fee = models.CharField("Consultaion Fee", max_length=100, null=True, blank=True)

class ExpertArea(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Title', max_length=20)

    def __str__(self):
        return self.title

class Booking(models.Model):
    """
    docstring
    """
    PAYMENT_METHOD_CHOICES = (
        ('bKash', 'bKash'),
        ('Rocket', 'Rocket'),
        ('Nagad', 'Nagad'),
        ('DBBL', 'DBBL'),
        ('Skrill', 'Skrill'),
        ('Aqua', 'Aqua')
    )

    STATUS_OPTION_CHOICES = (
        ('Approved', 'Approved'),
        ('Pending', 'Pending')
    )

    SERVICE_OPTION_CHOICES = (
        ('Phone', 'Phone'),
        ('Email', 'Email'),
        ('Office', 'Office'),
    )
    client = models.ForeignKey(User, verbose_name='Client', related_name='client', on_delete=models.CASCADE, null=True, blank=True)
    lawyer = models.ForeignKey(User, verbose_name='Lawyer', related_name='lawyer', on_delete=models.DO_NOTHING)
    date = models.DateField(verbose_name='Date Time Field')
    service = models.CharField("Get Service By",max_length=6, choices=SERVICE_OPTION_CHOICES, default='Phone')
    payment_method = models.CharField(max_length=6, choices=PAYMENT_METHOD_CHOICES, default='bKash')
    trxnid = models.CharField(max_length=50, null=True)
    amount = models.FloatField('Paid Amount', default=0)
    status = models.CharField(max_length=8, choices=STATUS_OPTION_CHOICES, default='Pending', null=True, blank=True)

    def __str__(self):
        return f"{self.client.username}'s booking Lawyer: {self.lawyer.username}"


class Review(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    review = models.TextField(verbose_name="Write Your review")