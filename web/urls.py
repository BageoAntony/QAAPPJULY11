from django.urls import path
from .views import SignInView,SignUpView,IndexView,add_answer,answer_upvote_view
urlpatterns = [
    path("",SignInView.as_view(),name="signin"),
    path("register",SignUpView.as_view(),name="signup"),
    path("index",IndexView.as_view(),name="index"),
    path("questions/<int:id>/answers/add",add_answer,name="add-answer"),
    path("answers/<int:id>/upvotes/add",answer_upvote_view,name="add-upvote")

]
