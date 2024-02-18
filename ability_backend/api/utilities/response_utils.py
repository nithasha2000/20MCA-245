def admin_sidebar():
    response = [
        {
            "key": "view_user", 
            "value": "Manage Users", 
            "icon": "fa fa-users"
        },
        {
            "key": "job-post-widget", 
            "value": "Jobs", 
            "icon": "fa fa-eye"
        },
        {
            "key": "register-employee", 
            "value": "Register Employee", 
            "icon": "fa-solid fa-id-card"
        }
    ]
    return response
def company_sidebar():
    response = [
        {
            "key": "job-post-widget", 
            "value": "View My Posts", 
            "icon": "fa fa-eye"
        }
    ]
    return response
def job_seeker_sidebar():
    response = [
        {
            "key": "job-post-widget", 
            "value": "View Job Posts", 
            "icon": "fa fa-eye"
        },
        {
            "key": "apply-job-list", 
            "value": "Applied Jobs", 
            "icon": "fa fa-tasks"
        },
        {
            "key": "save-job-list", 
            "value": "Saved Jobs", 
            "icon": "fas fa-save"
        }
    ]
    return response

def employee_sidebar():
    response = [
        {
            "key": "app-exam-form", 
            "value": "Create Exam", 
            "icon": "fa-plus"
        },
        {
            "key": "app-exam-table", 
            "value": "View Exam", 
            "icon": "fa fa-eye"
        }
    ]
    return response