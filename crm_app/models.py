from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Roles(models.TextChoices):
        SUPERADMIN = 'superadmin', 'Super Admin'
        ADMIN = 'admin', 'Admin'
        SALES_REP = 'sales_rep', 'Sales Representative'
    
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.SALES_REP)

    def is_superadmin(self):
        return self.role == self.Roles.SUPERADMIN
    
    def is_admin(self):
        return self.role == self.Roles.ADMIN
    
    def is_sales_rep(self):
        return self.role == self.Roles.SALES_REP


class Course(models.Model):
    course_name = models.CharField(max_length=255)

    def __str__(self):
        return self.course_name


class Lead(models.Model):
    # Status choices
    class StatusChoices(models.TextChoices):
        NEW = 'New', 'New'
        OPEN = 'Open', 'Open'
        AVERAGE = 'Average', 'Average'
        FOLLOWUP = 'Followup', 'Followup'
        INTERESTED = 'Interested', 'Interested'
        INPROGRESS = 'inProgress', 'In Progress'
        ACTIVE = 'Active', 'Active'
        CONVERTED = 'Converted', 'Converted'
        LOST = 'Lost', 'Lost'
        JUNK = 'Junk', 'Junk'

    # class type choices
    class ClassTypeChoices(models.TextChoices):
        PHYSICAL = 'Physical', 'Physical'
        ONLINE = 'Online', 'Online'

    # Payment type choices
    class PaymentTypeChoices(models.TextChoices):
        CASH = 'Cash', 'Cash'
        ONLINE = 'Online', 'Online'
        BANK_TRANSFER = 'Bank Transfer', 'Bank Transfer'    
        CHEQUE = 'Cheque', 'Cheque'

    #Device Choices
    class DeviceChoices(models.TextChoices):
        YES = 'Yes', 'Yes'
        NO = 'No', 'No'

    # Coding experience choices
    class CodingExperienceChoices(models.TextChoices):
        NONE = 'None', 'None'
        BASIC_PYTHON = 'Basic Python', 'Basic Python'
        INTERMEDIATE_CPP = 'Intermediate C++', 'Intermediate C++'
        ARDUINO = 'Arduino', 'Arduino'
        SOME_LINUX = 'Some Linux', 'Some Linux'
        ADVANCED_PYTHON = 'Advanced Python', 'Advanced Python'
        BASIC_JAVA = 'Basic Java', 'Basic Java'
        OTHER = 'Other', 'Other'

    # Source choices
    class SourceChoices(models. TextChoices):
        WHATSAPP_VIBER = 'WhatsApp/Viber', 'WhatsApp/Viber'
        FACEBOOK = 'Facebook', 'Facebook'
        WEBSITE  = 'Website', 'Website'
        EMAIL = 'Email', 'Email'
        OFFICE_VISIT = 'Office Visit', 'Office Visit'
        DIRECT_CALL = 'Direct Call', 'Direct Call'
        LINKEDIN = 'LinkedIn', 'LinkedIn'
        OTHER = 'Other', 'Other'

    # Main fields
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.NEW)
    add_date = models.DateField(auto_now_add=True, null=True)
    parents_name = models.CharField(max_length=255, blank=True)
    student_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    whatsapp_number = models.CharField(max_length=30, blank=True)
    age = models.CharField(max_length=30, blank=True)
    grade = models.CharField(max_length=30, blank=True)
    source = models.CharField(max_length=30, choices=SourceChoices.choices, blank=True)
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True)
    class_type = models.CharField(max_length=20, choices=ClassTypeChoices.choices, blank=True)
    shift = models.CharField(max_length=50, blank=True)
    previous_coding_experience = models.CharField(max_length=30, choices=CodingExperienceChoices.choices, blank=True)
    last_call = models.DateField(null=True, blank=True)
    next_call = models.DateField(null=True, blank=True)
    value = models.CharField(max_length=50, blank=True)
    adset_name = models.CharField(max_length=100, blank=True)
    payment_type = models.CharField(max_length=20, choices=PaymentTypeChoices.choices, blank=True)
    device = models.CharField(max_length=5, choices=DeviceChoices.choices, blank=True)
    workshop_batch = models.CharField(max_length=100, blank=True)
    remarks = models.TextField(blank=True)

    # Address fields (all optional)
    address_line_1 = models.CharField(max_length=255, blank=True)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    county = models.CharField(max_length=100, blank=True)
    post_code = models.CharField(max_length=20, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student_name

    @property
    def is_converted(self):
        return self.status == self.StatusChoices.CONVERTED


class Enrollment(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='enrollments', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    total_payment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    first_installment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    second_installment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    third_installment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    last_pay_date = models.DateField(null=True, blank=True)
    payment_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.lead.student_name} - {self.course.course_name if self.course else ''}"