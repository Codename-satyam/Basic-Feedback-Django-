from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Region(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name

class MediaOutlet(models.Model):
    name = models.CharField(max_length=200)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Story(models.Model):
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=520, unique=True)
    published_date = models.DateField(null=True, blank=True)
    outlet = models.ForeignKey(MediaOutlet, on_delete=models.SET_NULL, null=True, blank=True)
    url = models.URLField(help_text='Original story URL')
    excerpt = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_date', '-created_at']

class Feedback(models.Model):
    RATING_MIN = 1
    RATING_MAX = 5

    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='feedbacks')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)

    accuracy = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    bias = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    clarity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    relevance = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    comment = models.TextField(blank=True)
    anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        
    def average_score(self):
        total = (self.accuracy + self.bias + self.clarity + self.relevance)
        return total / 4.0
    def __str__(self):
        return f'Feedback for {self.story.title} - {self.average_score():.2f}'