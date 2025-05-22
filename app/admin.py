from django.contrib import admin
from django.contrib import messages
from django.urls import path
from django.shortcuts import render
from .models import *
from django import forms
from .models import Login_User
from django.http import HttpResponseRedirect
from django.urls import reverse

admin.site.register(Customer_Comment)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Tai_lieu)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(BookOrderItem)
admin.site.register(Chatbot_message)
admin.site.register(De_thi)
admin.site.register(Sach)
admin.site.register(FlashCard_Vocabulary)
admin.site.register(Vinh_danh)

class ChoiceInline(admin.TabularInline): # Hoặc admin.StackedInline
    model = Choice
    extra = 4 # Hiển thị sẵn 4 dòng trống cho lựa chọn
    fields = ('get_choice_label', 'text', 'is_correct') # Các trường sẽ hiển thị và thứ tự của chúng
    readonly_fields = ('get_choice_label',) # Trường 'get_choice_label' sẽ là read-only
    # ordering = ('some_order_field',) # Nếu bạn có trường order riêng trong Choice model

    def get_choice_label(self, obj):
        # obj là instance của Choice
        # Chúng ta cần biết thứ tự của Choice này trong tập hợp các choices của Question
        # Đây là phần hơi phức tạp vì inline formset không dễ dàng cung cấp index trực tiếp
        # trong hàm này khi đối tượng chưa được lưu.

        # Cách tiếp cận: nếu đối tượng đã được lưu (có pk), tìm index của nó
        if obj.pk:
            try:
                # Lấy tất cả choices của question hiện tại, sắp xếp theo id (hoặc trường order nếu có)
                # Lưu ý: Điều này có thể không hoàn toàn chính xác nếu người dùng đang sắp xếp lại
                # các inline mà chưa lưu.
                question_choices = list(obj.question.choices.all().order_by('id'))
                # Tìm index của obj trong danh sách này
                index = question_choices.index(obj)
                return chr(65 + index) # 65 là mã ASCII của 'A'
            except (ValueError, AttributeError):
                # AttributeError nếu obj.question chưa được set (khi form mới)
                # ValueError nếu obj không tìm thấy (không nên xảy ra nếu obj.pk có)
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