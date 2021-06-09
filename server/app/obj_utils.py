from sqlalchemy.exc import IntegrityError

from app import app

def get_objs(object_class, dict=True, relations=False):
    objs = app.session.query(object_class).all()
    if objs:
        if dict:
            return [obj.to_dict(relations) for obj in objs]
        else:
            return [obj for obj in objs]
    else:
        return []

def get_objs_with_filter(object_class, dict=True, relations=False, *args, **kwargs):
    objs = app.session.query(object_class).filter_by(*args, **kwargs).all()
    if objs:
        if dict:
            return [obj.to_dict(relations) for obj in objs]
        else:
            return [obj for obj in objs]
    else:
        return []

def get_obj_with_filter(object_class, dict=True, relations=False, *args, **kwargs):
    obj = app.session.query(object_class).filter_by(*args, **kwargs).first()
    if obj:
        if dict:
            return obj.to_dict(relations)
        else:
            return obj
    else:
        return None

def get_obj(object_class, obj_id, dict=True, relations=False):
    obj = app.session.query(object_class).filter_by(id=obj_id).first()
    if obj:
        if dict:
            return obj.to_dict(relations)
        else:
            return obj
    else:
        return None

def save_obj(object_class, data, obj_id):
    obj = app.session.query(object_class).get(obj_id)
    fill_object_from_data(obj, data, ['id'])
    app.session.add(obj)
    app.session.commit()

def create_obj(object_class, data, object=False):
    if object:
        obj=data
    else:
        obj = fill_object_from_data(object_class(), data, ['id'])
    app.session.add(obj)
    app.session.commit()
    return obj

def delete_obj(object_class, obj_id):
    obj = app.session.query(object_class).filter_by(id=obj_id).first()
    if obj:
        try:
            app.session.delete(obj)
            app.session.commit()
            return True
        except IntegrityError:
            app.session.rollback()
    return False

def delete_objs_with_filter(object_class, *args, **kwargs):
    objs = app.session.query(object_class).filter_by(*args, **kwargs).all()
    if objs:
        try:
            for obj in objs:
                app.session.delete(obj)
            app.session.commit()
            return True
        except IntegrityError:
            app.session.rollback()
    return False

def fill_object_from_data(obj, data, exclude=[]):
    attributes = [ attr for attr in data.keys() if attr not in exclude and attr in dir(obj)]
    for attribute in attributes:
        setattr(obj, attribute, data[attribute])
    return obj
