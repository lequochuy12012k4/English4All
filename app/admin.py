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