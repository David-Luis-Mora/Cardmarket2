from .serializers import BaseSerializer


class CardSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': str(instance.pk),
            'name': instance.name,
            'mana_cost': instance.mana_cost,
            'type_line': instance.type_line,
            'text': instance.text,
            'power': instance.power,
            'toughness': instance.toughness,
            'loyalty': instance.loyalty,
            'colors': instance.colors.split(',') if instance.colors else [],
            'image_uris': self.build_url(instance.image_uris) if instance.image_uris else None,
            'quantity': instance.quantity,
            'rarity': instance.rarity,
            'price': instance.price,
            'set_name': instance.set_name,
            'set_code': instance.set_code,
            'release_date': instance.release_date.isoformat() if instance.release_date else None,
        }
