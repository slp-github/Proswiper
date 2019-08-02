from django.shortcuts import render

# Create your views here.
from common import errors
from libs.http import render_json
from social import logics

#推荐用户接口
from social.models import Swiped
from social.permissions import has_perm
from user.models import User


def recommend(request):
    user=request.user

    rec_users=logics.recommend_user(user)
    print(rec_users)

    users=[u.to_dict() for u in rec_users]


    return render_json(data=users)

#喜欢接口
def like(request):
    user = request.user
    sid  =request.POST.get('sid')

    if sid is None:
        return render_json(code=errors.SID_ERR)

    matched = logics.like_someone(user.id ,int(sid))
    return render_json(data={'matched':matched})




@has_perm('superlike')
def superlike(request):
    user = request.user
    sid = request.POST.get('sid')
    if sid is None:
        return render_json(code=errors.SID_ERR)

    matched = logics.superlike_someone(user.id, int(sid))
    return render_json(data={'matched': matched})

def dislike(request):
    user = request.user
    sid = request.POST.get('sid')
    if sid is None:
        return render_json(code=errors.SID_ERR)

    Swiped.swipe(uid=user.id, sid=int(sid), mark='dislike')
@has_perm('rewind')
def rewind(request):
    '''
    反悔接口
    :param request:
    :return:
    '''

    user = request.user

    logics.rewind(user)

    return render_json()

@has_perm('liked_me')
def liked_me(request):
    '''
    喜欢过我接口
    :param request:
    :return:
    '''
    user = request.user

    uid_list = logics.like_me(user)

    users  =[u.to_dict() for u in User.objects.filter(id__in = uid_list)]

    return render_json(data=users)
