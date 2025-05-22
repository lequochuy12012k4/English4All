from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse,HttpResponseForbidden
from django.contrib.auth.models import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
from django.conf import settings
import logging
import json
from django.utils import timezone
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from english_web.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
from django.core import serializers
from datetime import *
from django.db import transaction
from django.utils import timezone

logger = logging.getLogger(__name__)

def home(request):
    courses = Course.objects.all()
    teachers = Teacher.objects.all()
    customer_comments = Customer_Comment.objects.all()
    if request.method == "POST":
        name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        school = request.POST.get('school')
        certificate = request.POST.get('certificate')
        target = request.POST.get('target')
        date_mon_year = datetime.now()
        data = {
            'name': name,
            'email': email,
            'phone_number': phone_number,
            'school': school,
            'certificate': certificate,
            'target': target
        }
        link = ''

        msg = '''
            𝐄𝐧𝐠𝐥𝐢𝐬𝐡𝟒𝐀𝐥𝐥
            Địa chỉ: 96𝐴 Đ. 𝑇𝑟𝑎̂̀𝑛 𝑃ℎ𝑢́, 𝑃. 𝑀𝑜̣̂ 𝐿𝑎𝑜, 𝐻𝑎̀ Đ𝑜̂𝑛𝑔, 𝐻𝑎̀ 𝑁𝑜̣̂𝑖
            Số điện thoại: 012345679
            Email: english4all@gmail.com

            {}
            Kính gửi: {},

            Chúng tôi hy vọng bạn vẫn khỏe. Chúng tôi viết thư này để thông báo cho bạn về các tài nguyên học tập tiếng Anh mới nhất, chương trình khuyến mãi đặc biệt và thông tin về khóa học.
            Tại English4All, chúng tôi cam kết cung cấp cho bạn những tài liệu và nguồn lực tốt nhất để giúp bạn thành công trong hành trình học tiếng Anh của mình. Chúng tôi tin rằng sẽ giúp bạn đã điểm cao trong kỳ thi.
            Để biết thêm thông tin về [chủ đề của thư], vui lòng truy cập trang web của chúng tôi tại {} hoặc liên hệ với chúng tôi theo số: 0123456789.
            Cảm ơn bạn đã là một phần của cộng đồng English4All. Chúng tôi đánh giá cao sự hỗ trợ liên tục của bạn và mong muốn giúp bạn đạt được mục tiêu học tiếng Anh của mình.
            Trân trọng!

            Đội ngũ English4All

            Họ và tên: {}
            Email: {}
            Số điện thoại: {}
            Trường học: {}
            Chứng chỉ: {}
            Mục tiêu: {}

            Đây là English4All - Bài tập lớn CNPM nhóm 01

        '''.format(
            date_mon_year.strftime("%A, %d %B %Y"),
            data['name'],
            link,

            data['name'],
            data['name'],
            data['email'],
            data['phone_number'],
            data['school'],
            data['certificate'],
            data['target']
        )

        subject = "English4All"
        sender = "lequochuy12012k4@gmail.com"
        send_mail(
            subject,
            msg,
            sender,
            [f'{email}']

        )

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        thanh_toan_items = order.get_thanh_toan_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        user_not_login = "show"
        user_login = "hidden"
        items = []
        order = {'get_thanh_toan_items':0, 'get_thanh_toan_total':0}
        thanh_toan_items = order['get_thanh_toan_items']
    context = {
        'courses':courses,
        'teachers':teachers,
        'customer_comments': customer_comments,
        'user_not_login':user_not_login,
        'user_login':user_login,
        'thanh_toan_items': thanh_toan_items,
    }
    
    return render(request,'app/home.html',context)

def Cap_nhat_thong_tinPage(request):
    form = EditProfile(request.POST, instance=request.user)
    if request.method == "POST":
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        thanh_toan_items = order.get_thanh_toan_items
        user_not_login = "hidden"
        user_login = "show"
        context = {
            'user': request.user,
            'user_not_login':user_not_login,
            'user_login':user_login,
            'form' : form,
            'thanh_toan_items': thanh_toan_items,
        }
        if form.is_valid():
            form.save()
            return render(request,'app/user/thong_tin.html',context)
    else:
        items = []
        order = {'get_thanh_toan_items':0, 'get_thanh_toan_total':0}
        thanh_toan_items = order['get_thanh_toan_items']
        user_not_login = "show"
        user_login = "hidden"
        context = {
            'user': request.user,
            'user_not_login':user_login,
            'user_login':user_not_login,
            'form' : form,
            'thanh_toan_items': thanh_toan_items,
        }
        return render(request,'app/user/cap_nhat_thong_tin.html',context)

def Thay_doi_mat_khauPage(request):
    form = ChangePassword(data = request.POST, user=request.user)
    if request.method == "POST":
        user_not_login = "hidden"
        user_login = "show"
        context = {
            'user': request.user,
            'user_not_login':user_not_login,
            'user_login':user_login,
            'form' : form
        }
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return render(request,'app/user/thong_tin.html',context)
    else:
        user_not_login = "show"
        user_login = "hidden"
        context = {
            'user': request.user,
            'user_not_login':user_login,
            'user_login':user_not_login,
            'form' : form
        }
        return render(request,'app/user/thay_doi_mat_khau.html',context)

def RegisterPage(request):
    form = CreateRegisterForm()
    context = {'form' : form}
    if request.method == "POST":
        form = CreateRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request,'app/register.html',context)

def LoginPage(request):
    form = CreateLoginForm()
    context = {'loginform': form}
    if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request,"Tên đăng nhập hoặc mật khẩu chưa chính xác")
    return render(request, 'app/login.html', context)

def Password_forget(request):
    form = PasswordResetRequestForm()
    context = {'form':form}
    return render(request,'app/password_forget.html', context)

def LogoutPage(request):
    logout(request)
    response = redirect('home')
    return response

def Lo_trinhPage(request):
    return render(request,'app/lo_trinh.html')

def Tai_lieuPage(request):
    tai_lieu = Tai_lieu.objects.all()
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        thanh_toan_items = order.get_thanh_toan_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        user_not_login = "show"
        user_login = "hidden"
        items = []
        order = {'get_thanh_toan_items':0, 'get_thanh_toan_total':0}
        thanh_toan_items = order['get_thanh_toan_items']  
    context = {
        'user_not_login':user_not_login,
        'user_login':user_login,
        'thanh_toan_items': thanh_toan_items,
        'tai_lieus': tai_lieu,
    }
    return render(request,'app/tai_lieu.html',context)

def De_thiPage(request):
    de_thi = De_thi.objects.all()
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        thanh_toan_items = order.get_thanh_toan_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        user_not_login = "show"
        user_login = "hidden"
        items = []
        order = {'get_thanh_toan_items':0, 'get_thanh_toan_total':0}
        thanh_toan_items = order['get_thanh_toan_items']  
    context = {
        'user_not_login':user_not_login,
        'user_login':user_login,
        'thanh_toan_items': thanh_toan_items,
        'de_this': de_thi,
    }
    return render(request,'app/de_thi.html',context)

import os
from django.conf import settings
from django.shortcuts import render
from django import forms

class AddWordForm(forms.Form):
    new_word = forms.CharField(label="Từ mới")
    new_meaning = forms.CharField(label="Nghĩa")
    new_example = forms.CharField(label="Ví dụ", widget=forms.Textarea)

import os
from django.conf import settings  # Import settings
from django.shortcuts import render
from .models import Order, FlashCard_Vocabulary  # Make sure to import the model

def Flash_CardPage(request):
    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        thanh_toan_items = order.get_thanh_toan_items
    else:
        items = []
        order = {'get_thanh_toan_items':0, 'get_thanh_toan_total':0}
        thanh_toan_items = order['get_thanh_toan_items']
        user_not_login = "show"
        user_login = "hidden"
    try:
        flashcard_vocab = FlashCard_Vocabulary.objects.first()  
        file_name = flashcard_vocab.file_csv.path
    except FlashCard_Vocabulary.DoesNotExist:
        context = {'error_message': 'No FlashCard Vocabulary found.'}
        return render(request, 'app/error.html', context)

    print(file_name)

    try:
        with open(file_name, 'r', encoding='utf-8-sig') as file:
            key = file.readline().strip()
            keys = key.split(",")

            data_word = []
            for line in file:
                value = line.strip()
                if not value:
                    continue
                values = value.split(",")
                index_data = {}
                for index in range(len(keys)):
                    try:
                        if keys[index] == 'id':
                            values[index] = int(values[index])

                        my_dict = {keys[index]: values[index]}
                        index_data.update(my_dict)
                    except IndexError:
                        print(f"Warning: Line '{value}' has fewer values than keys. Skipping.")
                        break 

                if index_data: 
                    data_word.append(index_data)

    except FileNotFoundError:
        context = {'error_message': f'File not found at {file_name}'}
        return render(request, 'app/error.html', context)
    if request.method == 'POST':
        form = AddWordForm(request.POST)
        if form.is_valid():
            new_word = form.cleaned_data['new_word']
            new_meaning = form.cleaned_data['new_meaning']
            new_example = form.cleaned_data['new_example']
            data_word.append({'word': new_word, 'meaning': new_meaning, 'example': new_example})
            form = AddWordForm()
    else:
        form = AddWordForm()

    context = {'user_not_login': user_not_login, 'user_login': user_login, 'data_word':data_word, 'form':form,'thanh_toan_items': thanh_toan_items,}
    return render(request,'app/flash_card.html',context)

def FlashCardTuhocPage(request):
    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        thanh_toan_items = order.get_thanh_toan_items
    else:
        user_not_login = "show"
        user_login = "hidden"
        items = []
        order = {'get_thanh_toan_items':0, 'get_thanh_toan_total':0}
        thanh_toan_items = order['get_thanh_toan_items']  
    context = {'thanh_toan_items': thanh_toan_items,'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/flash_card_tu_hoc.html',context)
def Gioi_thieuPage(request):
    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        thanh_toan_items = order.get_thanh_toan_items
    else:
        user_not_login = "show"
        user_login = "hidden"
        items = []
        order = {'get_thanh_toan_items':0, 'get_thanh_toan_total':0}
        thanh_toan_items = order['get_thanh_toan_items']  
    context = {'thanh_toan_items': thanh_toan_items,'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/gioi_thieu.html',context)

# app/views.py
from django.shortcuts import render
from .models import Test # Đảm bảo import Test
# ... (các import khác) ...

def list_tests_view(request):
    # Kiểm tra đăng nhập và chuẩn bị context user_login/user_not_login (nếu cần cho template này)
    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
    else:
        user_not_login = "show"
        user_login = "hidden"
    
    all_tests = Test.objects.all() # Lấy tất cả các bài test
    # Bạn có thể filter thêm ở đây, ví dụ: Test.objects.filter(is_active=True)

    context = {
        'tests': all_tests,
        'user_not_login': user_not_login,
        'user_login': user_login,
        # Thêm bất kỳ context nào khác mà trang list_tests.html của bạn cần
    }
    return render(request, 'app/list_tests.html', context) # Render template mới này

@login_required # Yêu cầu người dùng đăng nhập để làm test
def take_test_view(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    
    # Kiểm tra xem người dùng đã làm bài này và chưa hoàn thành không
    # Hoặc tạo một lần làm bài mới
    attempt, created = TestAttempt.objects.get_or_create(
        user=request.user,
        test=test,
        completed=False, # Chỉ lấy hoặc tạo nếu chưa hoàn thành
        defaults={'start_time': timezone.now()}
    )

    # Nếu attempt đã tồn tại và đã hoàn thành, có thể chuyển đến trang kết quả hoặc thông báo
    if not created and attempt.completed:
        # return redirect('test_result_url_name', attempt_id=attempt.id) # Chuyển đến trang kết quả
        return render(request, 'app/test_already_completed.html', {'attempt': attempt})


    # Tính thời gian còn lại nếu attempt đã tồn tại
    time_elapsed = (timezone.now() - attempt.start_time).total_seconds()
    time_remaining = (test.time_limit_minutes * 60) - time_elapsed

    if time_remaining <= 0:
        # Xử lý hết giờ nếu cần (ví dụ, tự động nộp bài)
        # Hoặc chỉ hiển thị thông báo trên template
        pass # Sẽ xử lý bằng JS trên client trước

    questions = test.questions.all().prefetch_related('choices') # Lấy câu hỏi và các lựa chọn

    context = {
        'test': test,
        'questions': questions,
        'attempt_id': attempt.id,
        'time_remaining_seconds': max(0, int(time_remaining)), # Đảm bảo không âm
    }
    return render(request, 'app/online_test.html', context)

@login_required
@transaction.atomic # Đảm bảo tất cả các thao tác DB hoặc thành công hoặc rollback
def submit_test_view(request, attempt_id):
    if request.method == 'POST':
        attempt = get_object_or_404(TestAttempt, id=attempt_id, user=request.user)

        if attempt.completed:
            # return redirect('test_result_url_name', attempt_id=attempt.id)
            return HttpResponseForbidden("Bài test này đã được nộp.")

        questions = attempt.test.questions.all()
        total_questions = questions.count()
        correct_answers = 0

        for question in questions:
            selected_choice_id = request.POST.get(f'question_{question.id}')
            if selected_choice_id:
                try:
                    selected_choice = Choice.objects.get(id=selected_choice_id, question=question)
                    UserAnswer.objects.create(
                        attempt=attempt,
                        question=question,
                        selected_choice=selected_choice
                    )
                    if selected_choice.is_correct:
                        correct_answers += 1
                except Choice.DoesNotExist:
                    # Lựa chọn không hợp lệ, có thể bỏ qua hoặc ghi log
                    pass
        attempt.correct_answers_count = correct_answers
        attempt.total_questions_at_submission = total_questions
        attempt.score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        attempt.end_time = timezone.now()
        attempt.completed = True
        attempt.save()

        # Chuyển hướng đến trang kết quả
        return redirect('test_result_url_name', attempt_id=attempt.id) # Tạo URL này ở bước sau

    return redirect('home') # Hoặc trang danh sách test

@login_required
def test_result_view(request, attempt_id):
    attempt = get_object_or_404(TestAttempt, id=attempt_id, user=request.user)
    if not attempt.completed:
        # Nếu chưa hoàn thành thì không cho xem kết quả, có thể redirect về trang test
        return redirect('take_test', test_id=attempt.test.id)
    
    context = {
        'attempt': attempt
    }
    return render(request, 'app/test_result.html', context)

import matplotlib.pyplot as plt
from io import BytesIO
import base64
import numpy as np
def Thong_tin(request):

    x_labels = ["Lần 1", "Lần 2", "Lần 3","Lần 4","Lần 5","Lần 6", "Lần 7"]
    x_toeic = np.array([1, 2, 3, 4, 5, 6, 7])
    y_toeic = np.array([100, 200, 300, 400, 500, 600, 700])

    x_ielts = np.array([1, 2, 3, 4, 5, 6, 7])
    y_ielts = np.array([400, 450, 500, 550, 600, 650, 750])

    x_thptqg = np.array([1, 2, 3, 4, 5, 6, 7])
    y_thptqg = np.array([550, 450, 670, 850, 725, 950, 900])

    plt.figure(figsize=(12, 8), facecolor="#222222")
    ax = plt.axes()
    ax.set_facecolor("#333333")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    plt.plot(x_toeic, y_toeic, color="#00FFFF", linewidth=2, marker='o', markersize=8, label="Điểm TOEIC")
    plt.plot(x_ielts, y_ielts, color="#FFC0CB", linewidth=2, marker='s', markersize=8, label="Điểm IELTS")
    plt.plot(x_thptqg, y_thptqg, color="#FFFFFF", linewidth=2, marker='^', markersize=8, label="Điểm THPTQG")  # Use a triangle marker

    plt.xlabel("Các lần thi", color="white", fontsize=14)  # Changed x label
    plt.ylabel("Điểm", color="white", fontsize=14)
    plt.title("Đồ thị điểm TOEIC, IELTS, THPTQG", color="white", fontsize=18)
    plt.legend(facecolor="#333333", edgecolor="white", labelcolor="white")
    plt.grid(True, color="#555555", linestyle='--')

    plt.ylim(0, 1000)
    plt.yticks(np.arange(0, 1001, 100), color="white")

    plt.xticks(x_toeic, x_labels, color="white")

    buffer = BytesIO()
    plt.savefig(buffer, format='png', facecolor=plt.gcf().get_facecolor())
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')

    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        thanh_toan_items = order.get_thanh_toan_items
    else:
        user_not_login = "show"
        user_login = "hidden"
        items = []
        order = {'get_thanh_toan_items':0, 'get_thanh_toan_total':0}
        thanh_toan_items = order['get_thanh_toan_items']
    context = {
        'thanh_toan_items': thanh_toan_items,
        'user_not_login':user_not_login,
        'user_login':user_login,
        'graphic': graphic
    }
    return render(request,'app/user/thong_tin.html',context)

def Thanh_toan(request):
    customer = request.user
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    bookitems = order.bookorderitem_set.all()
    items = order.orderitem_set.all()

    user_not_login = "hidden"
    user_login = "show"
    thanh_toan_items = order.get_thanh_toan_items
    total_cost = order.get_thanh_toan_total

    context = {
        'items': items,
        'bookitems': bookitems,
        'order': order,
        'user_not_login': user_not_login,
        'user_login': user_login,
        'thanh_toan_items': thanh_toan_items,
        'total_cost': total_cost,
    }
    return render(request,'app/user/thanh_toan.html',context)

def Mua_khoa_hoc(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        courseId = data['courseId']
        action = data['action']
        customer = request.user

        try:
            course = Course.objects.get(id=courseId)
        except Course.DoesNotExist:
            return JsonResponse({'error': 'Course not found'}, status=404)

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, course=course)

        if action == 'add':
            orderItem.quantity += 1
            if orderItem.quantity > 1:
                orderItem.quantity = 1 #Only allow 1 course.
        elif action == 'remove':
            orderItem.quantity -= 1

        if orderItem.quantity < 0:
            orderItem.quantity = 0
        elif orderItem.quantity == 0:
            orderItem.delete()
            return JsonResponse('deleted', safe=False)

        orderItem.save()
        return JsonResponse('added', safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400)

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def remove_course(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        try:
            order_item = OrderItem.objects.get(id=item_id, order__customer=request.user)
            order_item.delete()
            return JsonResponse({'success': True})
        except OrderItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'OrderItem not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@login_required 
def remove_book(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        try:
            book_order_item = BookOrderItem.objects.get(id=item_id, order__customer=request.user) 
            book_order_item.delete()
            return JsonResponse({'success': True})
        except OrderItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'OrderItem not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400) 

import os
from django.conf import settings
def Vinh_danhPage(request):

    if request.user.is_authenticated:
        user_not_login = "hidden"
        user_login = "show"
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        thanh_toan_items = order.get_thanh_toan_items
    else:
        items = []
        order = {'get_thanh_toan_items':0, 'get_thanh_toan_total':0}
        thanh_toan_items = order['get_thanh_toan_items']
        user_not_login = "show"
        user_login = "hidden"

    vinhdanh_rank = Vinh_danh.objects.first()

    if vinhdanh_rank is None:
        context = {
            'thanh_toan_items': thanh_toan_items,
            'user_not_login': user_not_login,
            'user_login': user_login,
            'error_message': 'No Vinh_danh rankings found.' 
        }
        return render(request, 'app/vinh_danh.html', context) 

    try:
        file_name = vinhdanh_rank.file_csv.path
    except ValueError:
        context = {
            'thanh_toan_items': thanh_toan_items,
            'user_not_login': user_not_login,
            'user_login': user_login,
            'error_message': 'No file specified for Vinh_danh rankings.'
        }
        return render(request, 'app/vinh_danh.html', context)

    data_rankings = [] 

    try:
        with open(file_name, 'r', encoding='utf-8-sig') as file:
            key = file.readline().strip()
            keys = key.split(",")

            for line in file:
                value = line.strip()
                if not value:  
                    continue

                values = value.split(",")
                index_data = {}
                for index in range(len(keys)):
                    try:
                        if keys[index] == 'score' or keys[index] == 'rank':
                            values[index] = int(values[index])

                        my_dict = {keys[index]: values[index]}
                        index_data.update(my_dict)
                    except (IndexError, ValueError) as e:
                        print(f"Error processing line: {value}. Error: {e}")
                        continue 

                if index_data:
                    data_rankings.append(index_data)

    except FileNotFoundError:
        print(f"Error: File not found at path: {file_name}")
        context = {
            'thanh_toan_items': thanh_toan_items,
            'user_not_login': user_not_login,
            'user_login': user_login,
            'error_message': f'File not found at {file_name}'
        }
        return render(request, 'app/vinh_danh.html', context)

    context = {
        'thanh_toan_items': thanh_toan_items,
        'user_not_login': user_not_login,
        'user_login': user_login,
        'data_ranking': data_rankings
    }
    return render(request, 'app/vinh_danh.html', context)

def test_api_key():
    try:
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content("Hello")
        return True, response.text
    except Exception as e:
        return False, str(e)

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        is_working, test_response = test_api_key()
        if not is_working:
            return JsonResponse({'error': f'API Key error: {test_response}'}, status=500)
            
        try:
            logger.info(f"API Key present: {bool(settings.GOOGLE_API_KEY)}")
            
            message = request.POST.get('message', '')
            logger.info(f"Received message: {message}")
            
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            
            logger.info("Google API configured")
            
            model = genai.GenerativeModel('gemini-2.0-flash')
            logger.info("Model created")
            
            context = """You are Trợ giảng English4All, an AI teaching assistant for an English learning platform. 
            You help students with:
            - English courses (TOEIC, IELTS, THPTQG)
            - Course information and pricing
            - Study materials and resources
            - Online tests and assessments
            - Learning paths and roadmaps
            
            Please respond in Vietnamese unless specifically asked in English.
            Keep responses concise and friendly."""
            
            prompt = f"{context}\n\nUser: {message}\nTrợ giảng English4All:"
            logger.info("Generating response...")
            response = model.generate_content(prompt)
            logger.info("Response generated")
            
            new_chat = Chatbot_message(message = message, response = response)
            new_chat.save()
            return JsonResponse({'response': response.text})
            
        except Exception as e:
            logger.error(f"Error in chatbot_response: {str(e)}", exc_info=True)
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def Khoa_hoc(request):
    courses = Course.objects.all()
    teachers = Teacher.objects.all()
    customer_comments = Customer_Comment.objects.all()
    keys = None
    filter_course = None

    if request.method == "POST":
        if "filter_course" in request.POST:
            filter_course = request.POST["filter_course"]
            keys = Course.objects.filter(name__contains = filter_course)

        else:
            filter_course = "" 
            keys = Course.objects.all() 
            print("filter_course key not found in POST data")

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        thanh_toan_items = order.get_thanh_toan_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        user_not_login = "show"
        user_login = "hidden"
        items = []
        order = {'get_thanh_toan_items':0, 'get_thanh_toan_total':0}
        thanh_toan_items = order['get_thanh_toan_items']

    context = {
        'courses':courses,
        'teachers':teachers,
        'customer_comments': customer_comments,
        'user_not_login':user_not_login,
        'user_login':user_login,
        'thanh_toan_items': thanh_toan_items,
        'filter_course': filter_course,
        "keys": keys,
    }
    
    return render(request,'app/course.html',context)

def Search_Tailieu(request):
    if request.method == "POST":
        search_tai_lieu = request.POST["search_tai_lieu"]
        keys = Tai_lieu.objects.filter(name__contains = search_tai_lieu)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        thanh_toan_items = order.get_thanh_toan_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_thanh_toan_items':0, 'get_thanh_toan_total':0}
        thanh_toan_items = order['get_thanh_toan_items']
        user_not_login = "show"
        user_login = "hidden"
    context = {
        'user_not_login':user_not_login,
        'user_login':user_login,
        "keys_tai_lieu":keys,
        
    }
    return render(request,'app/search_tai_lieu.html',context)

def Search_Dethi(request):
    if request.method == "POST":
        search_de_thi = request.POST["search_de_thi"]
        keys = De_thi.objects.filter(name__contains = search_de_thi)
        
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        thanh_toan_items = order.get_thanh_toan_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_thanh_toan_items':0, 'get_thanh_toan_total':0}
        thanh_toan_items = order['get_thanh_toan_items']
        user_not_login = "show"
        user_login = "hidden"
    context = {
        'user_not_login':user_not_login,
        'user_login':user_login,
        "keys_de_thi":keys,
    }
    return render(request,'app/search_de_thi.html',context)

def SachPage(request):
    books = Sach.objects.all()
    books_json = serializers.serialize('json', books)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        thanh_toan_items = order.get_thanh_toan_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_thanh_toan_items':0, 'get_thanh_toan_total':0}
        thanh_toan_items = order['get_thanh_toan_items']  
        user_not_login = "show"
        user_login = "hidden"
    
    context = {
        'user_not_login':user_not_login,
        'user_login':user_login,
        'books':books,
        'thanh_toan_items': thanh_toan_items,
        'books_json': books_json
    }
    return render(request,'app/sach.html',context)

from django.shortcuts import render
from .models import Sach

def Search_Sach(request):
    keys = []

    if request.method == "POST":
        search_sach = request.POST["search_sach"]
        keys = Sach.objects.filter(name__contains=search_sach)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        thanh_toan_items = order.get_thanh_toan_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_thanh_toan_items':0, 'get_thanh_toan_total':0}
        thanh_toan_items = order['get_thanh_toan_items']
        user_not_login = "show"
        user_login = "hidden"

    context = {
        'user_not_login': user_not_login,
        'user_login': user_login,
        "keys_sach": keys,
        'thanh_toan_items': thanh_toan_items,
    }
    return render(request, 'app/search_sach.html', context)

@login_required
def Mua_sach(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        bookId = data['bookId']
        action = data['action']
        customer = request.user

        try:
            book = Sach.objects.get(id=bookId)
        except Sach.DoesNotExist:
            print(f"Error: Book with id={bookId} not found")
            return JsonResponse({'error': 'Book not found'}, status=404)

        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        bookOrderItem, created = BookOrderItem.objects.get_or_create(order=order, book=book)
        if action == 'add':
            bookOrderItem.quantity += 1
            if bookOrderItem.quantity > 1:
                bookOrderItem.quantity = 1
        elif action == 'remove':
            bookOrderItem.quantity -= 1

        if bookOrderItem.quantity < 0:
            bookOrderItem.quantity = 0
        elif bookOrderItem.quantity == 0:
            bookOrderItem.delete()
            print(f"BookOrderItem deleted: id={bookOrderItem.id}")
            return JsonResponse('deleted', safe=False)

        bookOrderItem.save()
        print(f"BookOrderItem saved: id={bookOrderItem.id}, quantity={bookOrderItem.quantity}")

        return JsonResponse('added', safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400)
