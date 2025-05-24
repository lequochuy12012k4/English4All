from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm
from django import forms  
from django.forms.widgets import PasswordInput, TextInput

class Sach(models.Model):
    name = models.CharField(max_length= 10000, null=True)
    author = models.CharField(max_length= 10000, null=True)
    price = models.CharField(max_length=200,null=True)
    image = models.ImageField(null=True,blank=True)
    evaluate = models.FloatField(null=True,blank=True)
    content = models.TextField(null=True,blank=True)
    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Customer_Comment(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=False)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200,null=True)
    comment = models.TextField(max_length=10000,null=True)
    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=200, null=True)
    comment = models.TextField(max_length=10000,null=True)
    image = models.ImageField(null=True,blank=True)
    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class FlashCard_Vocabulary(models.Model):
    file_csv = models.FileField(max_length=250,null=True,blank=True,upload_to='flash_card/') 
    def FileURL(self):
        try:
            url = self.file_upload.url
        except:
            url = ''
        return url

class Vinh_danh(models.Model):
    file_csv = models.FileField(max_length=250,null=True,blank=True,upload_to='vinh_danh/') 
    def FileURL(self):
        try:
            url = self.file_upload.url
        except:
            url = ''
        return url

class Tai_lieu(models.Model):
    name = models.CharField(max_length= 10000, null=True)
    content = models.TextField(max_length=10000, null=True)
    image = models.ImageField(null=True,blank=True)
    file_upload = models.FileField(max_length=250,null=True,blank=True,upload_to='tai_lieu/') 
    def __str__(self):
        return self.name
    
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    @property 
    def FileURL(self):
        try:
            url = self.file_upload.url
        except:
            url = ''
        return url

class De_thi(models.Model):
    name = models.CharField(max_length= 10000, null=True)
    level_choices = (
        ('Cơ bản', 'Cơ bản'),
        ('Trung bình', 'Trung bình'),
        ('Nâng cao', 'Nâng cao'),
    )
    level = models.CharField(
        max_length=10,
        choices=level_choices,
        null=True,
        blank=True,
        default=''
    )
    image = models.ImageField(null=True,blank=True)
    file_upload = models.FileField(max_length=250,null=True,blank=True,upload_to='de_thi/') 
    def __str__(self):
        return self.name
    
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    @property 
    def FileURL(self):
        try:
            url = self.file_upload.url
        except:
            url = ''
        return url

class Course(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.CharField(max_length=200, null=True) # Consider using DecimalField for price for accuracy
    level_choices = (
        ('Cơ bản', 'Cơ bản'),
        ('Trung bình', 'Trung bình'),
        ('Nâng cao', 'Nâng cao'),
    )
    level = models.CharField(
        max_length=10,  # Increased slightly to accommodate 'Trung bình' if needed, though 'Nâng cao' is longest
        choices=level_choices,
        null=True,
        blank=True,
        default='Cơ bản' # Or another sensible default, or remove default if it must be set
    )
    image = models.ImageField(null=True, blank=True, upload_to='course_images/') # Added upload_to
    content = models.TextField(max_length=1000, null=True)

    # New fields
    duration = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Ví dụ: '3 tháng', '20 giờ', '6 tuần'"
    )
    video_url = models.URLField(
        max_length=500, # Increased max_length for longer URLs like YouTube share links with params
        null=True,
        blank=True,
        help_text="Link video giới thiệu khóa học (ví dụ: YouTube, Vimeo)"
    )

    def __str__(self):
        return self.name if self.name else "Unnamed Course"

    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = '' # Or a path to a default placeholder image
        return url

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_thanh_toan_items(self):
        orderitems = self.orderitem_set.all()
        bookorderitems = self.bookorderitem_set.all()
        total = sum([item.quantity for item in orderitems]) + sum([item.quantity for item in bookorderitems])
        return total

    @property
    def get_thanh_toan_total(self):
        orderitems = self.orderitem_set.all()
        bookorderitems = self.bookorderitem_set.all()
        total = sum([item.get_total for item in orderitems]) + sum([item.get_total for item in bookorderitems])
        return "{:,}".format(total)

    @property
    def get_thanh_toan_total_int(self):
        orderitems = self.orderitem_set.all()
        bookorderitems = self.bookorderitem_set.all()
        total = sum([item.get_total for item in orderitems]) + sum([item.get_total for item in bookorderitems])
        return total
    
class OrderItem(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"OrderItem: {self.course.name} in Order {self.order.id}"

    @property
    def get_total(self):
        if self.course:
            total_string = self.course.price
            total_int = int(total_string.replace(",", "")) * self.quantity
            return total_int
        else:
            return 0

class BookOrderItem(models.Model):
    book = models.ForeignKey(Sach, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"BookOrderItem: {self.book.name} in Order {self.order.id}"

    @property
    def get_total(self):
        if self.book:
            total_string = self.book.price
            total_int = int(total_string.replace(",", "")) * self.quantity
            return total_int
        else:
            return 0

class CreateLoginForm(UserCreationForm):
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Tên đăng nhập'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Mật khẩu'}))
    
class Login_User(models.Model):
    username = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.username
    
class CreateRegisterForm(UserCreationForm):
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mật khẩu'}))
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Xác nhận mật khẩu'}))
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={
                        'class':'form-control',
                        'placeholder':'Họ',
                }), 
            'last_name': forms.TextInput(attrs={
                        'class':'form-control',
                        'placeholder':'Tên',
                }), 
            'username': forms.TextInput(attrs={
                        'class':'form-control',
                        'placeholder':'Tên đăng nhập',
                }), 
            'email': forms.EmailInput(attrs={
                        'class':'form-control',
                        'placeholder':'Email',
                }),

        }

class EditProfile(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']
        widgets = {
        'first_name': forms.TextInput(attrs={
            'class':'form-control',
            
        }),
        'last_name': forms.TextInput(attrs={
            'class':'form-control',
            
        }),
        'username': forms.TextInput(attrs={
            'class':'form-control',
            
        }),
        'email': forms.EmailInput(attrs={
            'class':'form-control',
            
        }),
}
class ChangePassword(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password','new_password1','new_password2']
        widgets = {
        'old_password': forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Mật khẩu cũ',
        }),
        'new_password1': forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Tên',
        }),
        'new_password2': forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Tên đăng nhập',
        }),
}

class Chatbot_message(models.Model):
    message = models.CharField(max_length=100000)
    response = models.CharField(max_length=100000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

class PasswordResetRequestForm(PasswordResetForm): # Kế thừa để giữ nguyên logic của Django
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(attrs={
            'placeholder': 'Địa chỉ Email của bạn',
            'autocomplete': 'email',
            'class': 'form-control email-input' # Class bạn đã style
        })
    )

class Test(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tiêu đề bài test")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    time_limit_minutes = models.PositiveIntegerField(default=30, verbose_name="Thời gian làm bài (phút)")
    created_at = models.DateTimeField(auto_now_add=True)
    # Có thể thêm: is_active, scheduled_time, etc.

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Bài Test"
        verbose_name_plural = "Các Bài Test"

class Question(models.Model):
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE, verbose_name="Bài Test")
    text = models.TextField(verbose_name="Nội dung câu hỏi")
    # Có thể thêm: question_type (trắc nghiệm, điền từ), points, image, audio
    order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự") # Để sắp xếp câu hỏi

    def __str__(self):
        return f"Câu {self.order}: {self.text[:50]}... (Test: {self.test.title})"

    class Meta:
        ordering = ['order', 'id'] # Sắp xếp theo thứ tự, rồi đến ID
        verbose_name = "Câu Hỏi"
        verbose_name_plural = "Các Câu Hỏi"

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE, verbose_name="Câu Hỏi")
    text = models.CharField(max_length=255, verbose_name="Nội dung lựa chọn") # Chỉ chứa nội dung, ví dụ "Paris"
    is_correct = models.BooleanField(default=False, verbose_name="Là đáp án đúng")
    # (Không cần trường order ở đây, vì Django admin inline có cơ chế sắp xếp)

    def __str__(self):
        return self.text # Hoặc bạn có thể tùy chỉnh __str__ nếu muốn

    class Meta:
        verbose_name = "Lựa Chọn"
        verbose_name_plural = "Các Lựa Chọn"
        ordering = ['id'] # Hoặc một trường order nếu bạn thêm vào (nhưng admin inline tự xử lý thứ tự)

class TestAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Người dùng")
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="Bài Test")
    start_time = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian bắt đầu")
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="Thời gian kết thúc")
    score = models.FloatField(null=True, blank=True, verbose_name="Điểm số") # Có thể là % hoặc số câu đúng
    completed = models.BooleanField(default=False, verbose_name="Hoàn thành")
    correct_answers_count = models.PositiveIntegerField(null=True, blank=True, verbose_name="Số câu đúng")
    total_questions_at_submission = models.PositiveIntegerField(null=True, blank=True, verbose_name="Tổng số câu khi nộp")
    def __str__(self):
        return f"{self.user.username} - {self.test.title} (Điểm: {self.score})"

    class Meta:
        verbose_name = "Lần Làm Test"
        verbose_name_plural = "Các Lần Làm Test"

class UserAnswer(models.Model):
    attempt = models.ForeignKey(TestAttempt, related_name='answers', on_delete=models.CASCADE, verbose_name="Lần làm test")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Câu Hỏi")
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, verbose_name="Lựa chọn đã chọn")
    # Có thể thêm: is_correct_at_time_of_answer (nếu đáp án có thể thay đổi)

    def __str__(self):
        return f"Trả lời cho câu {self.question.id} trong lần làm {self.attempt.id}"

    class Meta:
        unique_together = ('attempt', 'question') # Mỗi câu hỏi chỉ được trả lời 1 lần trong 1 attempt
        verbose_name = "Câu Trả Lời Của Người Dùng"
        verbose_name_plural = "Các Câu Trả Lời Của Người Dùng"