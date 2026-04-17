from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, viewsets, filters, status
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import BlogPost, BlogCategory, BlogComment


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'slug']


class BlogCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogComment
        fields = ['id', 'author', 'email', 'content', 'is_approved', 'created_at']
        read_only_fields = ['is_approved', 'created_at']


class BlogPostSerializer(serializers.ModelSerializer):
    category_detail = BlogCategorySerializer(source='category', read_only=True)
    destination_name = serializers.CharField(source='destination.name', read_only=True, allow_null=True)

    tags_list = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    approved_comments = serializers.SerializerMethodField()

    # Frontend-aligned aliases
    date = serializers.SerializerMethodField()
    readTime = serializers.CharField(source='read_time', read_only=True)
    img = serializers.SerializerMethodField()
    authorObj = serializers.SerializerMethodField()
    body = serializers.ListField(read_only=True)
    relatedSlugs = serializers.ListField(source='related_slugs', read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'body',
            'featured_image', 'image_url', 'img',
            'author', 'author_avatar_url', 'authorObj',
            'category', 'category_detail', 'destination', 'destination_name',
            'tags', 'tags_list',
            'date_display', 'date', 'read_time', 'readTime',
            'views', 'is_published', 'published_at', 'updated_at',
            'relatedSlugs',
            'comments_count', 'approved_comments'
        ]

    def get_tags_list(self, obj):
        return obj.get_tags_list()

    def get_comments_count(self, obj):
        return obj.comments.filter(is_approved=True).count()

    def get_approved_comments(self, obj):
        comments = obj.comments.filter(is_approved=True)
        return BlogCommentSerializer(comments, many=True).data

    def get_date(self, obj):
        if obj.date_display:
            return obj.date_display
        if obj.published_at:
            return obj.published_at.strftime('%B %-d, %Y')
        return ''

    def get_img(self, obj):
        if obj.featured_image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.featured_image.url) if request else obj.featured_image.url
        if obj.image_url:
            return obj.image_url
        if obj.featured_media_asset:
            if obj.featured_media_asset.image:
                request = self.context.get('request')
                return request.build_absolute_uri(obj.featured_media_asset.image.url) if request else obj.featured_media_asset.image.url
            if obj.featured_media_asset.image_url:
                return obj.featured_media_asset.image_url
        return None

    def get_authorObj(self, obj):
        avatar = obj.author_avatar_url
        if obj.author_avatar:
            request = self.context.get('request')
            avatar = request.build_absolute_uri(obj.author_avatar.url) if request else obj.author_avatar.url
        elif obj.author_avatar_media_asset:
            request = self.context.get('request')
            if obj.author_avatar_media_asset.image:
                avatar = request.build_absolute_uri(obj.author_avatar_media_asset.image.url) if request else obj.author_avatar_media_asset.image.url
            elif obj.author_avatar_media_asset.image_url:
                avatar = obj.author_avatar_media_asset.image_url
        return {
            'name': obj.author,
            'avatar': avatar,
        }


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogPost.objects.filter(is_published=True).select_related(
        'category', 'destination', 'featured_media_asset', 'author_avatar_media_asset'
    )
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'destination__slug']
    search_fields = ['title', 'content', 'excerpt', 'author']
    ordering_fields = ['published_at', 'views', 'title']
    ordering = ['-published_at']

    def get_permissions(self):
        # Keep blog browsing public and allow public comment submissions.
        return [AllowAny()]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_comment(self, request, slug=None):
        post = self.get_object()
        serializer = BlogCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, is_approved=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']


@api_view(['GET'])
def blog_category_labels(request):
    labels = ['All'] + list(BlogCategory.objects.order_by('name').values_list('name', flat=True))
    return Response(labels)
