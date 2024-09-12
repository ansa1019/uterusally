from django.db import models
from django.contrib.auth.models import User
from content.models import category
from django.utils.timezone import now
# Create your models here.


class profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255, default="Anonymous")
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    user_image = models.ImageField(upload_to='user_image/', null=True, blank=True)
    nickname = models.CharField(max_length=255, unique=True, null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    page_music = models.FileField(upload_to='user_page_music/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True, blank=True, null=True)
    is_rd = models.BooleanField(default=False) # 是否為營養師
    subscribe = models.ManyToManyField(User, related_name="subscribe", blank=True)

    def __str__(self):
        if self.nickname:
            nickname = self.nickname
        else:
            nickname = "Anonymous"
        return "使用者名稱:\t" + self.user.username + "\t暱稱:\t" + nickname


class bodyProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    height = models.PositiveIntegerField(null=True, blank=True)
    weight = models.PositiveIntegerField(null=True, blank=True)
    family_planning = models.CharField(max_length=255, null=True, blank=True)
    expecting = models.CharField(max_length=255, null=True, blank=True)
    medical_history = models.CharField(max_length=255, null=True, blank=True)
    other_medical_history = models.TextField(null=True, blank=True)
    medication = models.CharField(max_length=255, null=True, blank=True)
    doctor_advice = models.TextField(null=True, blank=True)
    allergy = models.CharField(max_length=255, null=True, blank=True)
    marriage = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True, blank=True, null=True)

    def __str__(self):
        return "使用者名稱:\t" + self.user.username

personal_calendar_type = (
    ('menstruation', '月經'),
    ('miscarriage period', '小產期'),
    ('pregnancy', '懷孕期'),
    ('menopause', '更年期'),
    ('postpartum_period', '產後期'),
)


class personal_calendar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, null=True, blank=True, choices=personal_calendar_type) # 月經、排卵、安全期
    cycle = models.IntegerField(default=0) # 週期
    date = models.DateField(blank=True, null=True) # 日期
    cycle_days = models.IntegerField(default=0) # 週期天數

    def __str__(self):
        try:
            t = "\t類型:\t" + self.type
        except:
            t = "\t類型:\tNone"
        return "使用者名稱:\t" + self.user.username + t


class subPersonalCalendar(models.Model):
    calendar = models.ForeignKey(personal_calendar, on_delete=models.CASCADE)
    dict = models.JSONField(null=True, blank=True) # detail

    def __str__(self):
        return "使用者名稱:\t" + self.calendar.user.username + "\t類型:\t" + self.calendar.type


class subscribeTopic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ManyToManyField(category, related_name="topic", blank=True)

    def __str__(self):
        return "使用者名稱:\t" + self.user.username


class subscribeHashtag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hashtag = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return "使用者名稱:\t" + self.user.username