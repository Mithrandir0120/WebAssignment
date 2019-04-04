from django.db import models


class EnumField(models.Field):
    # Comes from https://stackoverflow.com/a/9633015
    def __init__(self, *args, **kwargs):
        super(EnumField, self).__init__(*args, **kwargs)
        if not self.choices:
            raise AttributeError('EnumField requires `choices` attribute.')

    def db_type(self, connection):
        return "enum(%s)" % ','.join("'%s'" % k for (k, _) in self.choices)


# Create your models here.
class UserType_1622441019(models.Model):
    userType = models.CharField(max_length=20)

    def __str__(self):
        return self.userType


class PrviderType_1622441019(models.Model):
    prviderType = models.CharField(max_length=20)

    def __str__(self):
        return self.prviderType


class Admin_1622441019(models.Model):
    adminID = models.AutoField(db_column='adminID', primary_key=True)
    emailAddress = models.EmailField(db_column='emailAddress', max_length=80, blank=False, null=True)
    firstName = models.CharField(db_column='firstName', max_length=40, blank=True, null=True)
    lastName = models.CharField(db_column='lastName', max_length=40, blank=True, null=True)
    password = models.CharField(db_column='password', max_length=400, blank=True, null=True)

    class Meta:
        db_table = 'admin'


class User_1622441019(models.Model):
    userID = models.AutoField(db_column='userID', primary_key=True)
    emailAddress = models.EmailField(db_column='emailAddress', max_length=80, blank=False, null=True)
    firstName = models.CharField(db_column='firstName', max_length=40, blank=True, null=True)
    lastName = models.CharField(db_column='lastName', max_length=40, blank=True, null=True)
    phoneNumber = models.CharField(db_column='phoneNumber', max_length=45, blank=True, null=True)
    userType = EnumField(choices=(('Please choose your user type', 'Please choose your user type'),
                                  ('Member', 'Member'), ('Volunteer', 'Volunteer')), default=0)
    password = models.CharField(max_length=400, blank=True, null=True)

    class Meta:
        db_table = 'user'


class Issue_1622441019(models.Model):
    issueID = models.AutoField(db_column='issueID', primary_key=True)
    issueName = models.CharField(db_column='issueName', max_length=60, blank=True, null=True)
    address = models.CharField(db_column='address', max_length=80, blank=True, null=True)
    phoneNumber = models.CharField(db_column='phoneNumber', max_length=45, blank=True, null=True)
    emailAddress = models.CharField(db_column='emailAddress', max_length=80, blank=True, null=True)
    issueDetail = models.CharField(db_column='issueDetail', max_length=600, blank=True, null=True)
    issueType = EnumField(choices=(('Please choose your Type', 'Please choose your type'), ('Water', 'Water'),
                                   ('Electronic', 'Electronic'), ('Car', 'Car'), ('Air', 'Air'), ('Fire', 'Fire'),
                                   ('House', 'House'), ('Clean', 'Clean')), default=0)

    class Meta:
        db_table = 'issue'


class Provider_1622441019(models.Model):
    providerID = models.AutoField(db_column='providerID', primary_key=True)
    providerName = models.CharField(db_column='providerName', max_length=60, blank=True, null=True)
    phoneNumber = models.CharField(db_column='phoneNumber', max_length=45, blank=True, null=True)
    emailAddress = models.CharField(db_column='emailAddress', max_length=80, blank=True, null=True)
    providerPrice = models.CharField(db_column='providerPrice', max_length=6, blank=True, null=True)
    providerType = EnumField(choices=(('Please choose your Type', 'Please choose your type'), ('Water', 'Water'),
                                   ('Electronic', 'Electronic'), ('Car', 'Car'), ('Air', 'Air'), ('Fire', 'Fire'),
                                   ('House', 'House'), ('Clean', 'Clean')), default=0)

    class Meta:
        db_table = 'provider'
