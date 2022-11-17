import string

from django.db.migrations import serializer
from rest_framework import serializers

from api.models import Book, Author


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('created_at',)

    def validate_name(self, data):
        try:
            data.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError as e:
            raise serializers.ValidationError('set a correct name') from e

        if data in string.punctuation.split():
            raise serializers.ValidationError(
                ('name should not contain :, ", [, ] ,white space and comma characters')
            )
        return data


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
        read_only_fields = ('created_at')

    def validate_name(self, data):
        try:
            data.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError as e:
            raise serializers.ValidationError('set a correct name') from e

        if data in string.punctuation.split():
            raise serializers.ValidationError(
                ('name should not contain :, ", [, ] ,white space and comma characters')
            )
        return data