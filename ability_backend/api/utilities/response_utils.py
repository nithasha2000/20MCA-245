def admin_sidebar():
    response = [
        {
            "key": "view_user", 
            "value": "View Users", 
            "icon": "fa fa-eye"
        },
    ]
    return response
def company_sidebar():
    response = [
        {
            "key": "job-post-widget", 
            "value": "View My Posts", 
            "icon": "fa fa-eye"
        },
        {
            "key": "job-post", 
            "value": "Add My Posts", 
            "icon": "fa fa-plus"
        }
    ]
    return response