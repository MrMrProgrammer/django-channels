from rest_framework.serializers import ModelSerializer
from . import models

class MessageSerializers(ModelSerializer):
    
    class Meta:
        model = models.Message
        fields = [
            "__str__",
            "content",
            "timestamp"
        ]
