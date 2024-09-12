from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'content'

router = DefaultRouter()
router.register('textEditorPost', viewset=textEditorPostSerializerView, basename='textEditorPostTest')
router.register('textEditorPostComment', viewset=testTextEditorPostCommentSerializerView, basename='testTextEditorPostComment')
router.register('userGetSelfComment', viewset=userGetSelfCommentView, basename='userGetSelfComment')
router.register('userGetSelfPost', viewset=userGetSelfPostView, basename='userGetSelfPost')
router.register('PostMetadataHandler', viewset=PostMetadataView, basename='PostSocialData')
router.register('category', viewset=categoryView, basename='category')
router.register('subcategory', viewset=subcategoryView, basename='subcategory')
router.register('PostGetOfficial', viewset=PostGetOfficialView, basename='PostGetOffical')
router.register('userGetBookmark', viewset=userGetBookmarkView, basename='userGetBookmark')
router.register('getTagClick', viewset=getTagClickView, basename='getTagClick')
router.register('orderByClick', viewset=orderByClickView, basename='orderByClick')
router.register('orderByClickOfficial', viewset=orderByClickOfficialView, basename='orderByClickOfficial')
router.register('hashTag', viewset=hashTagView, basename='hashTag')
router.register('queryPost', viewset=queryPostView, basename='queryPost')
router.register('getTmpPost', viewset=getTmpPostView, basename='getTmpPost')
router.register('TempOfficialPostSave', viewset=officialPostTempSaveView, basename='officialPostTempSave')
router.register('TempOfficialPostGet', viewset=getOfficialTempPostView, basename='getOfficialTempPost')
router.register('polls', viewset=pollsView, basename='polls')
router.register('option', viewset=optionView, basename='option')
router.register('vote', viewset=voteView, basename='vote')
router.register('getRecords', viewset=getRecordView, basename='getRecords')
urlpatterns = [
    path('', include((router.urls, app_name), namespace='content')),
]

