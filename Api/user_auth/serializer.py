from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from point.models import point


# 別種登入方法
# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['username'] = user.username
#         token['email'] = user.email
#         return token


class RegisterationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2']


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match"})
        return attrs

    def create(self, validated_data):
        from task.models import task, taskRecord
        user = User.objects.create(
            username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()

        point.objects.create(user=user, point=1000)
        begginer_task = task.objects.filter(type="BEGGINER")
        dayly_task = task.objects.filter(type="DAILY")
        for task in begginer_task:
            taskRecord.objects.create(user=user, task=task)
        for task in dayly_task:
            taskRecord.objects.create(user=user, task=task)

        return user


    #擋掉重複的email及暱稱


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            print(validated_data['password'])
            instance.set_password(validated_data['password'])
            instance.save()
        return instance



class VerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']