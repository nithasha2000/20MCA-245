from django.urls import path
from .views import account_views, dashboard_views

urlpatterns = [
    path('', account_views.index),
    path('login/', account_views.login_api),
    path('logout/', account_views.logout_api),
    path('change_password/', account_views.change_password_api),
    path('register/', account_views.register_api),
    path('view-users/', dashboard_views.view_users),
    path('notifications/', dashboard_views.view_notifications),
    path('account_activation/', dashboard_views.account_activation),
    path('forgot-password/', account_views.forgot_password),
    path('verify-otp/', dashboard_views.verify_otp),
    path('dashboard-sidebar/', dashboard_views.dashboard_sidebar),
    path('job-post/', dashboard_views.job_post),
    path('view-job-list/', dashboard_views.view_job_list),
    path('apply-job/', dashboard_views.apply_job),
    path('save-job/', dashboard_views.save_job_post),
    path('save-job-list/', dashboard_views.view_save_job_post),
    path('unsave-job/', dashboard_views.unsave_job),
    path('applied-job-list/', dashboard_views.applied_job_list),
    path('unapply-job/', dashboard_views.unapply_job),
    path('view-applicants/', dashboard_views.view_applicants),
    path('download_applicant_resume/', dashboard_views.download_applicant_resume),
    path('shortlist-candidate/', dashboard_views.shortlist_candidate),
    path('mark-notifications/', dashboard_views.mark_notifications),
    path('job-post-approve/', dashboard_views.job_post_approve),
    path('job-post-filter/', dashboard_views.job_post_filter),
    path('apply-job-post-filter/', dashboard_views.apply_job_post_filter),
    path('save-job-list-filter/', dashboard_views.save_job_list_filter),
    path('exam-form/',account_views.exam_form),
    path('view-exam-list',dashboard_views.view_exam_forms)
]