from rest_framework import serializers

class AskSerializer(serializers.Serializer):
    Language_CHOICES = [
            ('English', 'English'), 
            ('CN', 'Simplified-Chinese'), 
            ('ZH', 'Traditional-Chinese'), 
            ('French', 'French')
    ]
    Agent_CHOICES =[
            ('Pastor','Pastor'),
            ('Priest','Priest')
    ]

    """Serializer for user ask requests."""
    title = serializers.CharField(max_length=255)
    question = serializers.CharField()
    language = serializers.ChoiceField(
        choices=Language_CHOICES,
        default = 'ZH',
    )
    bible = serializers.CharField(max_length=255, required=False, allow_blank=True)
    output = serializers.JSONField(required=False, allow_null=True)
    agent = serializers.ChoiceField(
        choices=Agent_CHOICES,
        default = 'Priest',
    )


    def create(self, validated_data):
        """Process the ask and save it to the CommonQuestion table."""
        asked = {}
        for str, value in validated_data.items():
            asked[str] = value
        print(asked)
        return asked
    
