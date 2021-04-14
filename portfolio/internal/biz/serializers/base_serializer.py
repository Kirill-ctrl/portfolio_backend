class BaseSerializer:
    @classmethod
    def serialize(cls, obj, format_ser: str) -> dict:
        serializer = cls._get_serializer(format_ser)
        return serializer(obj)

    @classmethod
    def _get_serializer(cls, format_ser: str):
        raise NotImplemented