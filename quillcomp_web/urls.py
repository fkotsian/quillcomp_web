from django.urls import path
from . import views

app_name = 'quillcomp_web'
urlpatterns = [
    path('', views.prompts, name='landing'),
    path('prompts/', views.prompts, name='prompts'),
    path('prompts/<int:prompt_id>/', views.student_responses, name='student_responses'),
    path('prompts/<int:prompt_id>/new_response/', views.new_response, name='new_response'),
]
