class ObjectParser:
    @staticmethod
    def GetObjectNames(objects, checkbox_data=False):
        object_names = []
        for obj in objects:
            if not checkbox_data:
                object_names.append(obj.__str__())
            else:
                object_names.append({'name': obj.__str__()})

        return object_names

    @staticmethod
    def GetClassObjectByName(objects, obj_name):
        for obj in objects:
            if obj.__str__() == obj_name:
                return obj
