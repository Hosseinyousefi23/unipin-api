from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', )


# ------------------------------------------------------------------------


# class Role(models.Model):
# super_institution = models.ForeignKey(SuperInstitution, null=True, blank=True)
#
# def __str__(self):
# return 'salam'


# ------------------------------------------------------------------------

class SuperConductor(models.Model):
    real_name = models.CharField(max_length=100, default='Unknown')
    description = models.CharField(max_length=1000, default='Nothing')
    url_name = models.CharField(max_length=100, null=True, blank=True)
    is_formal = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='profile_image', null=True, blank=True)

    def __str__(self):
        return self.url_name


# ------------------------------------------------------------------------

class Person(SuperConductor):
    user = models.OneToOneField(User, related_name='person')
    national_id = models.CharField(max_length=100, null=True, blank=True)
    sharif_mail_address = models.EmailField(null=True, blank=True)
    interested_tags = models.ManyToManyField(Tag, blank=True)
    follows = models.ManyToManyField(SuperConductor, through='Follow', related_name='followers')

    def __str__(self):
        return self.user.username


# ------------------------------------------------------------------------

class Permission(models.Model):
    name = models.CharField(max_length=50)


# ------------------------------------------------------------------------

class Portfolio(models.Model):
    permissions = models.ManyToManyField(Permission, related_name='related_portfolios')


# ------------------------------------------------------------------------

class SuperInstitution(SuperConductor):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(Person, through='Membership')

    def __str__(self):
        return self.name


# ------------------------------------------------------------------------


class Membership(models.Model):
    institution = models.ForeignKey(SuperInstitution, related_name='membership_obj')
    person = models.ForeignKey(Person, related_name='membership_obj')
    # portfolio = models.ForeignKey(Portfolio, related_name='membership_obj')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)


# ------------------------------------------------------------------------

class University(SuperInstitution):
    def __str__(self):
        return self.name


# ------------------------------------------------------------------------

class Department(SuperInstitution):
    related_university = models.ForeignKey(University, null=True, blank=True)

    def __str__(self):
        return self.name


# ------------------------------------------------------------------------

class Studentity(models.Model):
    person = models.ForeignKey(Person, null=True, blank=True)
    department = models.ForeignKey(Department, null=True, blank=True)
    student_id = models.CharField(max_length=100)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    field_of_study = models.CharField(max_length=100)

    def __str__(self):
        return self.person.user.username + ' ' + self.student_id

    def is_graduated(self):
        if self.end_date == timezone.now:
            return True


# ------------------------------------------------------------------------


class Follow(models.Model):
    follower = models.ForeignKey(Person, related_name='following_follow_obj', on_delete=models.CASCADE)
    followed = models.ForeignKey(SuperConductor, related_name='followers_follow_obj', on_delete=models.CASCADE)
    follow_time = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.follower.url_name + ' --> ' + self.followed.url_name


# ------------------------------------------------------------------------

class Place(models.Model):
    name = models.CharField(max_length=100)


# ------------------------------------------------------------------------

class Event(models.Model):
    invited = models.ManyToManyField(Person, related_name='invite_list')
    conductor = models.ForeignKey(SuperConductor, related_name='event_list')
    creation_date = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag)
    places = models.ManyToManyField(Place)


# ------------------------------------------------------------------------

class Post(models.Model):
    is_public = models.BooleanField(default=False)
    post_type = models.CharField(choices=(
        ('normal', 'Normal'),
        ('quick', 'Quick'),
    ), default='normal', max_length=50)
    title = models.CharField(max_length=100)
    related_tags = models.ManyToManyField(Tag, blank=True)
    context = models.TextField()
    publish_time = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(SuperConductor, null=True, blank=True)
    event = models.ForeignKey(Event, null=True, blank=True)

    def __str__(self):
        return self.author.url_name + " : " + self.title

    def has_event(self):
        if self.event is None:
            return False
        return True


# ------------------------------------------------------------------------


class Group(SuperInstitution):
    is_department_group = models.BooleanField(default=False)
    related_university = models.ForeignKey(University, null=True, related_name="%(app_label)s_%(class)s_related")

    def __str__(self):
        return self.superInstitution.name
