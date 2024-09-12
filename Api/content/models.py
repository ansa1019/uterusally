from django.db import models
from django.contrib.auth.models import User
from django_quill.fields import QuillField
# Create your models here.


class category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class subcategory(models.Model):
    main = models.ForeignKey(category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class TextEditorPost(models.Model):
    title = models.CharField(max_length=100, unique=True, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    identity = models.CharField(max_length=100, unique=False, blank=True, null=True)
    content = QuillField()
    index_image = models.ImageField(upload_to='textEditorPost_index_image/', null=True, blank=True)
    like = models.ManyToManyField(User, related_name="like", blank=True)
    share = models.ManyToManyField(User, related_name="share", blank=True)
    click = models.ManyToManyField(User, related_name="click", blank=True)
    desable = models.BooleanField(default=False)
    is_official = models.BooleanField(default=False)
    is_temporary = models.BooleanField(default=False)
    category = models.ManyToManyField(subcategory, default="test subcategory", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True, null=True, blank=True)
    hashtag = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title
            # + "\tid" + str(self.id)
    
class record(models.Model):
    article = models.ForeignKey(TextEditorPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.DateTimeField(auto_now_add=True, auto_created=True, null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.start + " to " + self.end
    
class polls(models.Model):
    article = models.ForeignKey(TextEditorPost, on_delete=models.CASCADE)
    vote_name = models.CharField(max_length=255, blank=True, null=True)
    vote_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.vote_name


class option(models.Model):
    polls = models.ForeignKey(polls, on_delete=models.CASCADE)
    option_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.option_name


class vote(models.Model):
    polls = models.ForeignKey(polls, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    option = models.ForeignKey(option, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " voted for " + self.option.option_name


class hashtag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name


class TextEditorPostComment(models.Model):
    post = models.ForeignKey(TextEditorPost, on_delete=models.CASCADE, related_name="textEditorPostComments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    identity = models.CharField(max_length=100, blank=True, null=True, )
    body = models.TextField()
    images = models.ManyToManyField('CommentImage', blank=True)
    videos = models.ManyToManyField('CommentVideo', blank=True)
    desable = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, auto_created=True)
    top = models.BooleanField(default=False)

    def __str__(self):
        return 'Author:' + self.author.username + '\t'


class CommentImage(models.Model):
    post = models.ForeignKey(TextEditorPostComment, on_delete=models.CASCADE, related_name="testCommentImages")
    images = models.ImageField(upload_to='CommentImage/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)


class CommentVideo(models.Model):
    post = models.ForeignKey(TextEditorPostComment, on_delete=models.CASCADE, related_name="testCommentVideo")
    videos = models.FileField(upload_to='CommentVideo/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)


class PostCommentDetail(models.Model):
    pass




