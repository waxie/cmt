
from rest_framework import serializers


class BasicField(serializers.RelatedField):

        def to_representation(self, value):
            return value.name

        def get_queryset(self):
            #print dir(self)
            print 'PEP'
            print self.parent.fields
            return []