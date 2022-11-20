from rest_framework import serializers
from api.models import Book, Author


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('created_at',)

    def validate_author(self, value):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            if request.user == value.added_by:
                return value
            else:
                raise serializers.ValidationError(
                    "permission denied!Add a book with the author's user")

        raise serializers.ValidationError(
            'something went wrong!')


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
        read_only_fields = ('created_at', 'added_by',)

    def create(self, validated_data):
        instance = super(AuthorSerializer, self).create(validated_data)
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        instance.added_by = user
        instance.save()
        return instance
