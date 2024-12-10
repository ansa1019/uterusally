from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class personalCalendarSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = personal_calendar
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        personal_calendar_obj = personal_calendar.objects.create(user=user, **validated_data)
        return personal_calendar_obj

    def get_user(self, obj):
        return self.context['request'].user.id


class subPersonalCalendarSerializer(serializers.ModelSerializer):
    calendar = personalCalendarSerializer(read_only=True)
    calendar_id = serializers.IntegerField(write_only=True)
    calendar_notice = serializers.SerializerMethodField('get_calendar_notice')
    class Meta:
        model = subPersonalCalendar
        fields = '__all__'

    def get_calendar_notice(self, instance):

        return "calendar_notice"


class personal_menstrualSerializer(serializers.ModelSerializer):
    calendar = personalCalendarSerializer(read_only=True)
    
    class Meta:
        model = personal_menstrual
        fields = '__all__'

        
class recommendUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = profile
        fields = '__all__'



class profileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_user')
    username = serializers.SerializerMethodField('get_username')
    subscribe = serializers.SerializerMethodField('get_subscribe')
    class Meta:
        model = profile
        fields = '__all__'

    def create(self, validated_data):
        print(self.context['request'].data)
        user = self.context['request'].user
        profile_obj = profile.objects.create(user=user, **validated_data)
        return profile_obj

    def get_user(self, instance):
        return self.context['request'].user.id

    def get_subscribe(self, instance):
        from .models import profile
        subs = []
        try:
            for sub in instance.subscribe.all():
                subs.append(sub.username)
        except:
            print(instance.subscribe)
        return subs

    def get_username(self, instance):
        return self.context['request'].user.username


class bodyProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    user_drug = serializers.SerializerMethodField('get_user_drug')
    user_order = serializers.SerializerMethodField('get_user_order')
    user_allergy = serializers.SerializerMethodField('get_user_allergy')
    class Meta:

        model = bodyProfile
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        body_profile_obj = bodyProfile.objects.create(user=user, **validated_data)
        return body_profile_obj

    def get_user(self, obj):
        return self.context['request'].user.id


    def get_user_drug(self, instance):
        if bodyProfile.objects.get(user=User.objects.get(id=self.context['request'].user.id)).medication:
            return True
        else:
            return False

    def get_user_order(self, instance):
        if bodyProfile.objects.get(user=User.objects.get(id=self.context['request'].user.id)).doctor_advice:
            return True
        else:
            return False

    def get_user_allergy(self, instance):
        if bodyProfile.objects.get(user=User.objects.get(id=self.context['request'].user.id)).allergy:
            return True
        else:
            return False


class subscribeTopicSerializer(serializers.ModelSerializer):
    topic = serializers.SerializerMethodField('get_topic')
    class Meta:
        model = subscribeTopic
        fields = '__all__'


    def get_topic(self, instance):
        subs = []
        for sub in instance.topic.all():
            subs.append(sub.name)
        return subs


class subscribeHashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = subscribeHashtag
        fields = '__all__'