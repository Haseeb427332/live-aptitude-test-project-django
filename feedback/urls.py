
from django.urls import path
from . import views
urlpatterns = [
    path ('', views.index, name="index"),
    path ('login/', views.userlogin, name="userlogin"),
    path ('logout', views.logout_view, name="logout"),
    path('register',views.register_view, name='register'),
    path('adminlogin',views.admin_login, name="adminlogin"),
    path('adminpanel',views.adminpanel, name="adminpanel"),
    path ('adminlogout', views.logout_view, name="admin_logout"),
    path('userdetails/<user_id>/', views.userdetails , name ="userdetails"),
    path('createtest',views.Create_test,name='createtest'),
    path('testans',views.Test_ans , name="correctans"),
    path('delete/<q_id>/', views.Delete_questions, name="Delete"),
    path('update/<q_id>/',views.Update_questions , name="Update"),
    path('userinfo/<user_id>/' , views.user_info , name='userinfo'),
    path('instructions/<subject>',views.instructions , name="instructions"),
    path('testpage/<test_id>/',views.testpage,name="testpage"),
    path('testresults',views.test_results, name="results"),
    path('forgotpassword',views.Forgot_password,name="forgotpassword"),
    path('delete',views.delete_all,name="delete"),
    path('about',views.about,name='about'),
    path('queries',views.admincomments_view,name="queries"),
    path('deletecomments',views.delqueriers,name='delqueries')

]