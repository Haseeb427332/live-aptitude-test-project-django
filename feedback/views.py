from django.shortcuts import render,redirect,reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseForbidden,HttpRequest
from .models import *
import re 

# Create your views here.
#------------------------------index page ------------------------
@require_http_methods(["GET","POST"])
@login_required(login_url='userlogin')
def index(request):
    if request.user.is_superuser:
        return HttpResponseForbidden(reverse('userlogin'))
    if request.method == "GET":
        detail = registertion.objects.get(user=request.user)
        # create = Createquestions.objects.all()
        subjects = Createquestions.objects.all().values('subjects').distinct() 
        results = TestResults.objects.filter(user=request.user).values('subjects','total').distinct()
        print(results)
        context = {
            'detail':detail,
            'subjects':subjects,
            'results':results,
            }
        return render(request, "index.html", context)


@require_http_methods(["GET","POST"])
@login_required(login_url='userlogin')
def delete_all(request):
    user = request.user
    delete = TestResults.objects.filter(user=user).delete()
    return HttpResponseRedirect(reverse('index'))

# ----------------------Test page---------------------------------

@require_http_methods(["GET","POST"])
@login_required(login_url='userlogin')
def testpage(request ,test_id):
    if request.method == "GET":
        detail = registertion.objects.get(user=request.user)
        test_question = Createquestions.objects.filter(subjects=test_id)
        if test_id == "All":
            test_question = Createquestions.objects.all()
        context={'questions':test_question,'detail':detail}
        return render(request,'test.html',context)
    else:
        test_subject = test_id
        user = User.objects.get(username=request.user)
        flag = 0
        while True:
            flag += 1
            count= str(flag)
            try:
                test_question = request.POST['questions-'+count]
            except:
                break
            questions = Createquestions.objects.get(question=test_question, subjects=test_id)
            try:
                answer = request.POST['answer-'+count]
            except:
                break
            counts = 0
            try:
                choice = Createquestions.objects.get(correctanswer=answer)
                if answer == choice.correctanswer:
                    counts += 1
    
            except:
                pass

            test_results = TestResults(
                user =user,
                question=questions,
                subjects=test_subject,
                answer=answer,
                count = counts,
            )
            test_results.save()
            
        return HttpResponseRedirect(reverse('results'))

#----------------------- result page -----------------------------

@require_http_methods(["GET","POST"])
@login_required(login_url='userlogin')
def test_results(request):
    if request.method == "GET":
        detail = registertion.objects.get(user=request.user)
        n = TestResults.objects.all()
        for a in n :
            results = TestResults.objects.filter(user=request.user, subjects=a.subjects)
        for b in n:
            counted = TestResults.objects.filter(user=request.user,count=1,subjects=b.subjects)
            b.total =len(counted)
            print(b.total)
            b.save()
        context = {
            'detail':detail,
            'results':results,
            'total':len(counted)
            }
        return render(request,'testresults.html',context)

# --------------------------user info --------------------------

@require_http_methods(["GET","POST"])
@login_required(login_url='userlogin')
def user_info(request,user_id):
    if request.method == "GET":
        detail = registertion.objects.get(user=request.user)
        results = TestResults.objects.filter(user=user_id).values('subjects','total').distinct()
        print(detail)
        context = {
            'detail':detail,
            'results':results
            }
        return render(request,'userinfo.html',context)
    elif request.method == "POST":
        user_id = request.POST['u_id']
        user = User.objects.get(id=user_id)
        detail = registertion.objects.get(user=request.user)
        user.first_name = request.POST['firstname']
        user.last_name = request.POST['lastname']
        user.email=request.POST['email']
        user.username= request.POST['username']
        detail.department = request.POST['department']
        psw =request.POST['new_pass']
        print(psw)
        try:
            if len(psw) != 0:
                user.password = request.POST['new_pass']
                user.set_password(user.password)  
                print(1,request.POST['new_pass']) 
        except:
            pass
        user.save()
        detail.save()
        return HttpResponseRedirect(reverse('index'))

# ----------------------- test Instructions page ------------------

@require_http_methods(["GET","POST"])
@login_required(login_url='userlogin')
def instructions(request,subject):
    if request.method == "GET":
        detail = registertion.objects.get(user=request.user)
        subjects = Createquestions.objects.filter(subjects=subject).values('subjects').distinct()
            
        print(subjects)
        context = {
            'detail':detail,
            'subjects':subjects
            }

        return render(request , 'instructions.html' ,context)

# --------------------user login----------------------
@require_http_methods(["GET", "POST"])
def userlogin(request):
    if request.method == "POST" :
        username = request.POST['username']
        if not username:
            messages.success(request, "Must Provide Username")
            return redirect('userlogin')
        password = request.POST['password']
        if not password:
            messages.success(request, "Must Provide Username")
            return redirect('userlogin')
        user = authenticate(request, username=username,password=password, is_superuser=False)
        if not user:
            messages.success(request, "Invalid Credentials")
            return redirect('userlogin')
        login(request,user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request , 'userlogin.html')

@require_http_methods(["GET","POST"])
def Forgot_password(request):
    if request.method =="POST":
        email = request.POST['email']
        new_password = request.POST['new_password']
        try:
            mail = User.objects.get(email=email)
            print(mail)
            if mail:
                mail.password = new_password
                print(mail.password)
                mail.set_password(mail.password)
                mail.save()
                return HttpResponseRedirect(reverse('userlogin'))
        except:
            messages.success(request, 'Invalid Email Id.    Please Check Your Email !!!!')
            return HttpResponseRedirect(reverse('forgotpassword'))   
    else:
        return render(request,'forgotpassword/checkmail.html')
    

#--------------------------logout ------------------- 
@require_http_methods(["GET"])
def logout_view(request):
    logout(request)
    return redirect('userlogin')
#--------------------- registration ----------------
@require_http_methods(["GET","POST"])
def register_view(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        if not firstname:
            messages.success( request,'firstname should be not be empty')
            return HttpResponseRedirect(reverse('register'))
        lastname = request.POST['lastname']
        if not lastname:
            messages.success(request, 'lastname should be not be empty')
            return HttpResponseRedirect(reverse('register'))
        username = request.POST['username']
        if not username:
            messages.success( request,'username should not be empty')
            return HttpResponseRedirect(reverse('register'))

        email = request.POST['email']
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not email:
            messages.success(request,'email should be not be empty')
            return HttpResponseRedirect(reverse('register'))
        elif not (re.search(regex,email)):
            messages.success(request,'invalid email')
            return HttpResponseRedirect(reverse('register'))

        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if not password1:
            messages.success(request , 'password should be not be empty')
            return HttpResponseRedirect(reverse('register'))
        if not password2:
            messages.success(request , 'password should be not be empty')
            return HttpResponseRedirect(reverse('register'))
        if password1 != password2:
            messages.success(request, 'password didnt match')
            return HttpResponseRedirect(reverse('register'))
        department = request.POST['department']
        if not department:
            messages.success(request, ' choose department')
            return HttpResponseRedirect(reverse('register'))
        semster = request.POST['semster']
        if not semster:
            messages.success(request,'choose semster')
            return HttpResponseRedirect(reverse('register'))
        try:
            name = User.objects.get(username=username)
            messages.success(request,'username already exists')
            return HttpResponseRedirect(reverse('register'))
        except:
            pass

        try:
            mail = User.objects.get(email=email)
            messages.success(request,'email already exists')
            return HttpResponseRedirect(reverse('register'))
        except:
            pass 

        user = User(
            first_name=firstname,
            last_name=lastname,
            username=username,
            email=email,
            password=password1,
        )
        user.set_password(user.password)
        user.save()
        registers = registertion(
            user=user,
            department =department,
            semester = semster
        )
        registers.save()
        return HttpResponseRedirect(reverse('userlogin'))
    else:   
        return render(request,'register.html')
# ------------------------- admin login -------------------------
@require_http_methods(["GET","POST"])
def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate (request , username=username,password=password ,is_superuser=True)
        if not user:
            messages.success(request,'invalid Crenditails')
            return HttpResponseRedirect(reverse('adminlogin'))
        login(request,user)
        return HttpResponseRedirect(reverse('adminpanel'))  
    else:
        return render(request,'admin/adminlogin.html')  

@require_http_methods(["GET"])
@login_required(login_url='adminlogin')
def adminpanel(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden(reverse('adminlogin'))
    users = User.objects.filter(is_superuser=False)
    context = {'users':users}
    return render(request,'admin/adminpanel.html',context)

@require_http_methods(["GET","POST"])
@login_required(login_url='adminlogin')
def userdetails(request,user_id):
    users = User.objects.get(id=user_id)
    detail = registertion.objects.get(user=users)
    results = TestResults.objects.filter(user=user_id).values('subjects','total').distinct()
    print(results)
    context= {'user':users,'detail':detail,'results':results,}
    return render(request,'admin/userdetails.html',context)

@require_http_methods(["GET","POST"])
@login_required(login_url='adminlogin')
def Create_test(request):
    if request.method == "POST":
        questions = request.POST['questions']
        opt1 = request.POST['opt1']
        opt2 = request.POST['opt2']
        opt3 = request.POST['opt3']
        opt4 = request.POST['opt4']
        correct_answer = request.POST['correctans']
        subjects = request.POST['subjects']
        test = Createquestions(
            question=questions,
            option1=opt1,
            option2=opt2,
            option3=opt3,
            option4=opt4,
            correctanswer=correct_answer,
            subjects=subjects,
            )
        test.save()
        return HttpResponseRedirect(reverse('createtest'))
    else:
        return render(request,'admin/create_test.html')

@require_http_methods(["GET","POST"])
@login_required(login_url='adminlogin')
def Test_ans(request):
    display = Createquestions.objects.all()
    context={'display':display}
    return render(request,'admin/testans.html',context)

@require_http_methods(["GET","POST"])
@login_required(login_url='adminlogin')
def Delete_questions(request, q_id):
    question =  Createquestions.objects.get(id=q_id)
    question.delete()
    return HttpResponseRedirect(reverse('correctans'))

@require_http_methods(["GET","POST"])
@login_required(login_url='adminlogin')
def Update_questions(request,q_id):
    question =  Createquestions.objects.get(id=q_id)
    context ={'question':question}
    if request.method == "POST":
        Update =  Createquestions.objects.get(id=q_id)
        Update.question = request.POST['questions']
        Update.option1 = request.POST['opt1']
        Update.option2 = request.POST['opt2']
        Update.option3 = request.POST['opt3']
        Update.option4 = request.POST['opt4']
        Update.correctanswer = request.POST['correctans']
        Update.subjects = request.POST['subjects']
        Update.save()
        return HttpResponseRedirect(reverse('correctans'))
    else:
        return render(request,'admin/UpdateTest.html',context)

@require_http_methods(["GET","POST"])
def about(request):
    if request.method =="POST":
        email = request.POST['email']
        comment = request.POST['comments']
        response = Queries(
            email=email,
            comments=comment,
        )
        response.save()
        return HttpResponseRedirect(reverse('about'))
    else:
        return render(request,'about.html')

@require_http_methods(["GET","POST"])
@login_required(login_url='adminlogin')
def admincomments_view(request):
    usercomments = Queries.objects.all()
    if not usercomments:
        messages.success(request,'No Queries')
    context={'usercomments':usercomments}
    return render(request,'admin/commentviews.html',context)

@require_http_methods(["GET"])
@login_required(login_url='adminlogin')
def delqueriers(request):
    Queries.objects.all().delete()
    return HttpResponseRedirect(reverse('queries'))
