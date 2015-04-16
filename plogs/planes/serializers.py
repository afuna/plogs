from rest_framework import serializers
from plogs.main.serializers import UserSerializer
from .models import Plane, Kit, Prop, Engine

class KitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kit
        fields = ('manufacturer', 'model', 'serial_number', 'registration_number')

class EngineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engine
        fields = ('manufacturer', 'model', 'horsepower', 'serial_number')

class PropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prop
        fields = ('manufacturer', 'model', 'prop_type', 'serial_number')

class PlaneSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    engine = EngineSerializer(read_only=True)
    kit = KitSerializer(read_only=True)
    prop = PropSerializer(read_only=True)

    class Meta:
        model = Plane
        fields = ('owner', 'kit', 'engine', 'prop')
