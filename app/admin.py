from django.contrib import admin
from .models import *
from django.utils.html import format_html

class Customer_CommentAdmin(admin.ModelAdmin): 
    list_display = ('name', 'user_display', 'email', 'short_comment') 
    search_fields = ('name', 'user__username', 'user__email', 'email', 'comment') 
    list_filter = ('user',)

    fields = ('name', 'user', 'email', 'comment')

    def user_display(self, obj):
        if obj.user:
            return obj.user.username 
        return "-"
    user_display.short_description = 'Người dùng'

    def short_comment(self, obj):
        if obj.comment:
            return (obj.comment[:75] + '...') if len(obj.comment) > 75 else obj.comment
        return "-"
    short_comment.short_description = 'Bình luận (ngắn)' 
admin.site.register(Customer_Comment, Customer_CommentAdmin)

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'comment', 'teacher_tag')
    search_fields = ('name', 'comment')

    def teacher_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px;" />'.format(obj.image.url))
        return "No Image"
    teacher_tag.short_description = 'Hình ảnh'
    fields = ('name', 'comment', 'image')
admin.site.register(Teacher, TeacherAdmin)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'price', 'duration', 'image_tag','video_url')
    list_filter = ('level',)
    search_fields = ('name', 'content')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px;" />'.format(obj.image.url))
        return "-"
    image_tag.short_description = 'Hình ảnh'
    fields = ('name', 'level', 'price', 'duration', 'image', 'content', 'video_url')
admin.site.register(Course, CourseAdmin)

class Tai_lieuAdmin(admin.ModelAdmin):
    list_display = ('name', 'content','image_tag','file_upload')
    search_fields = ('name', 'content')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px;" />'.format(obj.image.url))
        return "-"
    image_tag.short_description = 'Hình ảnh'
    fields = ('name', 'content','image','file_upload')
admin.site.register(Tai_lieu,Tai_lieuAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date_order','complete','transaction_id')
    search_fields = ('customer', 'date_order')
    fields = ('customer', 'date_order','complete','transaction_id')
admin.site.register(Order,OrderAdmin)

class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('course', 'order','date_added','quantity')
    search_fields = ('course', 'date_added')
    fields = ('name', 'user', 'email', 'comment')
admin.site.register(OrderItem,OrderItemsAdmin)

class BookOrderAdmin(admin.ModelAdmin):
    list_display = ('book', 'order','date_added','quantity')
    search_fields = ('book', 'date_added')
    fields = ('book', 'order','date_added','quantity')
admin.site.register(BookOrderItem)

class Chatbot_messageAdmin(admin.ModelAdmin):
    list_display = ('message', 'response','created_at')
    search_fields = ('message', 'response','created_at')
    fields = ('message', 'response','created_at')
admin.site.register(Chatbot_message,Chatbot_messageAdmin)

class De_thiAdmin(admin.ModelAdmin):
    list_display = ('name', 'level','image_tag','file_upload')
    search_fields = ('name',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px;" />'.format(obj.image.url))
        return "-"
    image_tag.short_description = 'Hình ảnh'
    fields = ('name', 'level','image','file_upload')
admin.site.register(De_thi,De_thiAdmin)

class SachAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'price', 'evaluate', 'content','image_tag')
    search_fields = ('name', 'content')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:100px; max-height:100px;" />'.format(obj.image.url))
        return "-"
    image_tag.short_description = 'Hình ảnh'
    fields = ('name', 'author', 'price', 'evaluate', 'content','image')
admin.site.register(Sach, SachAdmin)

class FlashCard_VocabularyAdmin(admin.ModelAdmin):
    list_display = ('file_csv',)
    fields = ('file_csv',)
admin.site.register(FlashCard_Vocabulary,FlashCard_VocabularyAdmin)

class VinhdanhAdmin(admin.ModelAdmin):
    list_display = ('file_csv',)
    fields = ('file_csv',)
admin.site.register(Vinh_danh,VinhdanhAdmin)

class ChoiceInline(admin.TabularInline): # Hoặc admin.StackedInline
    model = Choice
    extra = 4 # Hiển thị sẵn 4 dòng trống cho lựa chọn
    fields = ('get_choice_label', 'text', 'is_correct') # Các trường sẽ hiển thị và thứ tự của chúng
    readonly_fields = ('get_choice_label',) # Trường 'get_choice_label' sẽ là read-only
    # ordering = ('some_order_field',) # Nếu bạn có trường order riêng trong Choice model

    def get_choice_label(self, obj):
        if obj.pk:
            try:
                question_choices = list(obj.question.choices.all().order_by('id'))
                index = question_choices.index(obj)
                return chr(65 + index) 
            except (ValueError, AttributeError):
                return "-" # Hoặc một placeholder khác
        return "-" # Placeholder cho form mới chưa được lưu
    
    get_choice_label.short_description = 'Nhãn' # Tên cột trong admin

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'test', 'order')
    list_filter = ('test',)
    inlines = [ChoiceInline]
    search_fields = ['text']

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True

class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_limit_minutes', 'created_at')
    search_fields = ['title']
    inlines = [QuestionInline]

class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    extra = 0
    readonly_fields = ('question', 'selected_choice') # Không cho sửa trực tiếp ở đây

class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'score', 'start_time', 'end_time', 'completed')
    list_filter = ('test', 'user', 'completed')
    search_fields = ['user__username', 'test__title']
    readonly_fields = ('start_time', 'end_time') # Thời gian thường được set tự động
    inlines = [UserAnswerInline]

admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice) # Có thể không cần admin riêng nếu quản lý qua Question
admin.site.register(TestAttempt, TestAttemptAdmin)
admin.site.register(UserAnswer) # Thường được xem qua TestAttempt