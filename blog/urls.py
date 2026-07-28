from django.urls import path

from .views import (
    home,
    dashboard,
    create_post,
    edit_post,
    delete_post,
    post_detail,
    author_profile,
    add_comment,
    delete_comment,
    toggle_like,
)
urlpatterns = [

    path("", home, name="home"),

    path(
        "dashboard/",
        dashboard,
        name="dashboard",
    ),

    path(
        "post/create/",
        create_post,
        name="create_post",
    ),

    path(
        "post/<int:pk>/edit/",
        edit_post,
        name="edit_post",
    ),

    path(
        "post/<int:pk>/delete/",
        delete_post,
        name="delete_post",
    ),
    path(
    "post/<slug:slug>/",
    post_detail,
    name="post_detail",
),

path(
    "author/<str:username>/",
    author_profile,
    name="author_profile",
),
path(
    "post/<slug:slug>/comment/",
    add_comment,
    name="add_comment",
),

path(
    "comment/<int:pk>/delete/",
    delete_comment,
    name="delete_comment",
),

path(
    "post/<slug:slug>/like/",
    toggle_like,
    name="toggle_like",
),
]