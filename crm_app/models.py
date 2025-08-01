from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Roles(models.TextChoices):
        SUPERADMIN = 'superadmin', 'Super Admin'
        ADMIN = 'admin', 'Admin'
        SALES_REP = 'sales_rep', 'Sales Representative'
    
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.SUPERADMIN)

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

    # Device Choices
    class DeviceChoices(models.TextChoices):
        YES = 'Yes', 'Yes'
        NO = 'No', 'No'

    # Previous Coding experience choices
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

    # Shift choices
    class ShiftChoices(models.TextChoices):
        SEVEN_NINE_AM = '7 A.M. - 9 A.M.', '7 A.M. - 9 A.M.'
        EIGHT_TEN_AM = '8 A.M. - 10 A.M.', '8 A.M. - 10 A.M.'
        TEN_TWELVE_AM = '10 A.M. - 12 P.M.', '10 A.M. - 12 P.M.'
        ELEVEN_ONE_PM = '11 A.M. - 1 P.M.', '11 A.M. - 1 P.M.'
        TWELVE_TWO_PM = '12 P.M. - 2 P.M.', '12 P.M. - 2 P.M.'
        TWO_FOUR_PM = '2 P.M. - 4 P.M.', '2 P.M. - 4 P.M.'
        TWO_THIRTY_FOUR_THIRTY_PM = '2:30 P.M. - 4:30 P.M.', '2:30 P.M. - 4:30 P.M.'
        FOUR_SIX_PM = '4 P.M. - 6 P.M.', '4 P.M. - 6 P.M.'
        FOUR_THIRTY_SIX_THIRTY_PM = '4:30 P.M. - 6:30 P.M.', '4:30 P.M. - 6:30 P.M.'
        FIVE_SEVEN_PM = '5 P.M. - 7 P.M.', '5 P.M. - 7 P.M.'
        SIX_SEVEN_PM = '6 P.M. - 7 P.M.', '6 P.M. - 7 P.M.'
        SIX_EIGHT_PM = '6 P.M. - 8 P.M.', '6 P.M. - 8 P.M.'
        SEVEN_EIGHT_PM = '7 P.M. - 8 P.M.', '7 P.M. - 8 P.M.'

    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.NEW)
    add_date = models.DateField(auto_now_add=True, null=True)  # required by default
    parents_name = models.CharField(max_length=255)
    student_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=30)
    whatsapp_number = models.CharField(max_length=30)
    age = models.CharField(max_length=30)
    grade = models.CharField(max_length=30)
    source = models.CharField(max_length=30, choices=SourceChoices.choices)
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True)
    class_type = models.CharField(max_length=20, choices=ClassTypeChoices.choices)
    
    # All other fields are optional
    shift = models.CharField(max_length=50, choices = ShiftChoices.choices ,blank=True)
    previous_coding_experience = models.CharField(
        max_length=30, choices=CodingExperienceChoices.choices, blank=True, default=CodingExperienceChoices.NONE
    )
    last_call = models.DateField(null=True, blank=True)
    next_call = models.DateField(null=True, blank=True)
    value = models.CharField(max_length=50, blank=True)
    adset_name = models.CharField(max_length=100, blank=True)
    payment_type = models.CharField(max_length=20, choices=PaymentTypeChoices.choices, blank=True)
    device = models.CharField(max_length=5, choices=DeviceChoices.choices, blank=True)
    workshop_batch = models.CharField(max_length=100, blank=True)
    remarks = models.TextField(blank=True)
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