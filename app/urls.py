from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .models import PasswordResetRequestForm # Form bạn vừa tạo ở trên
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/',views.RegisterPage, name="register"),
    path('login/',views.LoginPage,name="login"),
    path('logout/',views.LogoutPage,name="logout"),
    path('tai_lieu/',views.Tai_lieuPage, name="tai_lieu"),
    path('gioi_thieu/',views.Gioi_thieuPage,name="gioi_thieu"),
    path('user/thong_tin/', views.Thong_tin, name="thong_tin"),
    path('thanh_toan/', views.Thanh_toan, name="thanh_toan"),
    path('course/mua_khoa_hoc/', views.Mua_khoa_hoc, name="mua_khoa_hoc"),
    path('sach/mua_sach/', views.Mua_sach, name="mua_sach"),
    path('test_online/',views.Test_onlinePage, name="test_online"),
    path('vinh_danh/', views.Vinh_danhPage, name="vinh_danh"),
    path('course/', views.Khoa_hoc, name="course"),
    path('lo_trinh/', views.Lo_trinhPage, name="lo_trinh"),
    path('cap_nhat_thong_tin/', views.Cap_nhat_thong_tinPage, name="cap_nhat_thong_tin"),
    path('thay_doi_mat_khau/', views.Thay_doi_mat_khauPage, name="thay_doi_mat_khau"),
    path('flash_card/',views.Flash_CardPage, name="flash_card"),
    path('tu_hoc_flash_card/',views.FlashCardTuhocPage, name="flash_card_tu_hoc"),
    path('chatbot/response/', views.chatbot_response, name='chatbot_response'),
    path('remove_course/', views.remove_course, name='remove_course'),
    path('remove_book/', views.remove_book, name='remove_book'),
    path('search_tai_lieu/', views.Search_Tailieu, name='search_tai_lieu'),
    path('de_thi/',views.De_thiPage, name="de_thi"),
    path('search_de_thi/',views.Search_Dethi, name="search_de_thi"),
    path('sach/',views.SachPage,name="sach"),
    path('search_sach/',views.Search_Sach,name="search_sach"),
    path('password_forget/',views.Password_forget, name="password_forget"),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='app/password_forget.html', # Đường dẫn đến template của bạn
             form_class=PasswordResetRequestForm, # Form tùy chỉnh (nếu có)
             email_template_name='app/password_reset_email.html', # Template cho email
             subject_template_name='app/password_reset_subject.txt' # Template cho tiêu đề email
         ),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='app/password_reset_done.html' # Trang thông báo đã gửi email
         ),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='app/password_reset_confirm.html' # Trang nhập mật khẩu mới
         ),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='app/password_reset_complete.html' # Trang thông báo đổi mk thành công
         ),
         name='password_reset_complete'),
]
