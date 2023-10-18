def get_stamp_obj(self, model):
    stamp_id = self.request.session.get("stamp", None)
    stamp_obj = model.objects.filter(id=stamp_id).first() if stamp_id else None
    return stamp_obj if stamp_obj else None
