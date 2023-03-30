from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import Post,Like
from apps.comment.models import Comment

class CommentInline(admin.TabularInline):
    model = Comment
    exclude  = ('',)
    extra = 1
    

class IsRepliedFilter(SimpleListFilter):
    title = 'Replied'
    parameter_name = 'is_replied'

    def lookups(self, request, model_admin):
        return (
            ('replied', 'Replied'),
            ('not_replied', 'Not Replied'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'replied':
            return queryset.exclude(replied_to=None)
        if self.value() == 'not_replied':
            return queryset.filter(replied_to=None)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','like','tag_list','created')
    list_filter = ('created','tags')
    search_fields = ('title','text','user')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

    def like(self,obj):
        return Like.objects.filter(post=obj).count()

    inlines = [
        CommentInline,
    ]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user','post','is_replied','created')
    list_filter = (IsRepliedFilter,'created')

    def is_replied(self,obj):
        return obj.replied_to is not None
    is_replied.boolean = True

