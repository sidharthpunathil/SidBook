from django.db import models
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify


# Create your models here.

class Profile(models.Model):
    # Blank = True (Making this field optional
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    # Every user will only have his own profile
    # When a user will be deleted the profile will also be deleted
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="No bio.", max_length=300)
    email = models.EmailField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars')
    # install pillow
    # create media root
    # find avatar.png
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()

    def get_posts_no(self):
        # Because we gave related_name='posts' in Posts > models > class Post
        return self.posts.all().count()

    def get_all_author_post(self):
        return self.posts.all()

    def get_likes_given_no(self):
        likes = self.like_set.all()
        total_liked = 0
        for item in likes:
            if item.value == 'Like':
                total_liked += 1
        return total_liked

    def get_likes_received_no(self):
        posts = self.posts.all()
        total_liked = 0
        for item in posts:
            total_liked += item.liked.all().count()
        return total_liked


    def __str__(self):
        return f"({self.user.username}{self.created.strftime('%m/%d/%Y:%H:%M:%S')})"

    def save(self, *args, **kwargs):
        ex = False
        if self.first_name and self.last_name:
            to_slug = slugify(str(self.first_name) + ' ' + str(self.last_name))
            ex = Profile.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(to_slug + " " + str(get_random_code()))
                ex = Profile.objects.filter(slug=to_slug).exists()

        else:
            to_slug = str(self.user)
        self.slug = to_slug
        # The keyword arguments are the names of the fields you’ve defined on your model.
        # https://docs.djangoproject.com/en/3.1/topics/db/models/: Overriding predefined model methods¶
        super().save(*args, **kwargs)


# STATUS_CHOICES = (
#    ('<database_name>','<the_thing_that_we_see>')
# )


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)


class Relationship(models.Model):
    # When a profile gets deleted the relationship also gets deleted
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=200, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
