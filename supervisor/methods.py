from supervisor.models import TA
from studentportal.models import Project
from supervisor.decorators import supervisor_logged_in
from credentials import SG_USERS, CW_USERS, FULL_USERS


@supervisor_logged_in
def filtered_projects(request, **kwargs):
    queryset = None
    user=TA.objects.filter(email=request.user.email).first()
    if user==None:
        queryset = Project.objects.none()
    elif user.sg_access and user.cw_access: 
        queryset = Project.objects.filter(**kwargs)
    elif user.sg_access:
        queryset = Project.objects.filter(category__name='SG', **kwargs)
    elif user.cw_access:
        queryset = Project.objects.filter(category__name='CW', **kwargs)
    else:
        queryset = Project.objects.none()
    return queryset
