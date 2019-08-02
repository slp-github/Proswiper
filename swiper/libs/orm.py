class ModelToDictMixin():
    def to_dict(self,exclude=None):
        if exclude is None:
            exclude=[]
        attr_dict = {}
        fields = self._meta.fields#获取到所有字段对象

        for field in fields:
            field_name = field.attname#从字段对象提取到字段名
            if field_name not in exclude:
                attr_dict[field_name]=getattr(self,field_name)#getarr获取属性值

        return attr_dict
