from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views
from App_SpeechEmotionRecognition.views import LivePredictions

urlpatterns = [

path('',views.home,name='home'),
path('base/',views.base,name='base'),
path('SignIn/',views.SignIn,name='SignIn'),
path('SignUp/',views.SignUp,name='SignUp'),
path('Services/',views.Services,name='Services'),
path('ChangePassword/',views.ChangePassword,name ='ChangePassword'),
path('Logout/',views.Logout,name ='Logout'),
path('pred1/',views.pred1,name ='pred1'),
path('LivePredictions/', LivePredictions.as_view(),name='LivePredictions'),
path('RecordVoice/',views.RecordVoice,name ='RecordVoice'),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)