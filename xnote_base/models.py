from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

PROFILE_IMAGES_PATH = 'profile_image'


class Tag(models.Model):
    pass
    """
    hierarchy of interest tags.

    An abstract datatype for Tags. Their job is to attach people as interested tags as well as groups
    or posts as related tags.

    Attributes:

    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', )


class SuperConductor(models.Model):
    real_name = models.CharField(max_length=100, default='Unknown')
    description = models.CharField(max_length=1000, default='Nothing')
    real_type = models.ForeignKey(ContentType)
    url_name = models.CharField(max_length=100, null=True, blank=True)
    is_formal = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to=PROFILE_IMAGES_PATH, null=True, blank=True)

    def __str__(self):
        return self.real_name


# ------------------------------------------------------------------------

class Person(SuperConductor):
    user = models.OneToOneField(User, related_name='person')
    national_id = models.CharField(max_length=100, null=True, blank=True)
    sharif_mail_address = models.EmailField(null=True, blank=True)
    interested_tags = models.ManyToManyField(Tag, blank=True)
    follows = models.ManyToManyField(SuperConductor, through='Follow', related_name='followers')


# ------------------------------------------------------------------------

class Permission(models.Model):
    pass
    """
    permission types:

    create_post,
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# ------------------------------------------------------------------------

class Portfolio(models.Model):
    permissions = models.ManyToManyField(Permission, related_name='related_portfolios')


# ------------------------------------------------------------------------

class SuperInstitution(SuperConductor):
    members = models.ManyToManyField(Person, through='Membership')

    def __str__(self):
        return self.real_name


# ------------------------------------------------------------------------


class Membership(models.Model):
    institution = models.ForeignKey(SuperInstitution, related_name='membership_obj')
    person = models.ForeignKey(Person, related_name='membership_obj')
    portfolio = models.ForeignKey(Portfolio, related_name='membership_obj')
    is_admin = models.BooleanField(default=False)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.person.real_name + " in " + self.institution.real_name


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
    related_university = models.ForeignKey(University, null=True, blank=True, related_name="related_groups")

    def __str__(self):
        return self.superInstitution.name
