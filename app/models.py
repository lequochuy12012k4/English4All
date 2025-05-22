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
    name  = models.CharField(max_length=200,null=True)
    price = models.CharField(max_length=200,null=True)
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
    content = models.TextField(max_length=1000, null=True)

    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
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