from django.contrib import admin
from .models import (
    category, subcategory,
    TextEditorPost, TextEditorPostComment, CommentVideo, CommentImage
)


@admin.register(TextEditorPost)
class QuillPostAdmin(admin.ModelAdmin):
    pass
# Register your models here.


admin.site.register(TextEditorPostComment)
admin.site.register(CommentImage)
admin.site.register(CommentVideo)
admin.site.register(category)
admin.site.register(subcategory)
