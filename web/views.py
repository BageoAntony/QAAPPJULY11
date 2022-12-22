from django.shortcuts import render,redirect

# Create your views here.
from django.views.generic import CreateView,FormView,TemplateView,ListView
from .forms import LoginForm,UserRegistrationForm,QuestionForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from api.models import Questions,Answers
from django.utils.decorators import method_decorator

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid sesseion")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper


@method_decorator(signin_required,name="dispatch")
class SignUpView(CreateView):
    template_name="register.html"
    form_class=UserRegistrationForm
    success_url=reverse_lazy("signin")

@method_decorator(signin_required,name="dispatch")
class SignInView(FormView):
    template_name="login.html"
    form_class=LoginForm
    def post(self, request,*args,**kw):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("index")
            else:
                return render(request,self.template_name,{"form":form})

@method_decorator(signin_required,name="dispatch")
class IndexView(CreateView,ListView):
    template_name="index.html"
    form_class=QuestionForm
    success_url=reverse_lazy("index")
    model=Questions
    context_object_name="questions"

    def form_valid(self, form) :
        form.instance.user=self.request.user
        messages.success(self.request,"your question added successfully")
        return super().form_valid(form)
    def get_queryset(self):
        return Questions.objects.exclude(user=self.request.user).order_by('-created_date')

@signin_required
def add_answer(request,*args,**kwargs):
    id=kwargs.get("id")
    ques=Questions.objects.get(id=id)
    ans=request.POST.get("answer")
    Answers.objects.create(question=ques,answer=ans,user=request.user)
    messages.success(request,"your answer posted successfully")
    return redirect("index")

@signin_required
def answer_upvote_view(request,*args,**kwargs):
    id=kwargs.get("id")
    ans=Answers.objects.get(id=id)
    ans.upvote.add(request.user)
    return redirect("index")






