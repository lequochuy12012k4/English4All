from django.contrib import admin
from django.urls import path
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
    path('search_sach/',views.Search_Sach,name="search_sach")
]
