from common import errors

#检查权限装饰器
def has_perm(perm_name):
    def decorator(view_func):
        def wapper(request,*args,**kwargs):
            if request.user.vip._has_perm(perm_name):
                return view_func(request,*args,**kwargs)
            else:
                raise errors.VIPPermError
        return wapper
    return decorator