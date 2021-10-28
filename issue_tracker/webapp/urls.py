from django.urls import path
from webapp import views as webview

app_name = "webapp"

urlpatterns = [
    path('', webview.IndexView.as_view(), name='index'),
    path('issue/<int:issue_pk>/', webview.IssueView.as_view(), name='issue_detail'),
    path('issue/add/', webview.AddIssue.as_view(), name="issue_add"),
    path('issue/edit/<int:pk>/', webview.UpdateIssue.as_view(), name="issue_update"),
    path('issue/delete/<int:pk>', webview.DeleteIssue.as_view(), name="issue_delete"),
    path('projects-list/', webview.ProjectListView.as_view(), name='project_list'),
    path('detailed/<int:pk>', webview.ProjectDetailedView.as_view(), name='project_detail'),
    path('project/add', webview.ProjectCreateView.as_view(), name='project_add'),
    path('project/<int:pk>/issue/add', webview.ProjectCreateIssue.as_view(), name='project_add_issue')
]