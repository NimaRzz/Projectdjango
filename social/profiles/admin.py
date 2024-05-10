from django.contrib import admin
from .models import Relation

class RelationAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'relation', 'created']

admin.site.register(Relation, RelationAdmin)

