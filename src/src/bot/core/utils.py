class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def get_cloth_msg(cloths) -> str:
    """Выдает данные по одежде"""
    msg = str()
    for cloth in cloths:
        cloth_data = f"""Наименование одежды: {cloth.get("name")}\nНорма выдачи на год: {cloth.get("count")}\n\n"""
        msg += cloth_data
    return msg
