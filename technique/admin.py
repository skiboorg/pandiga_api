from django.contrib import admin
from .models import *


class TechniqueTypeInline(admin.TabularInline):
    model = TechniqueType
    extra = 0


class TechniqueCategoryAdmin(admin.ModelAdmin):
    inlines = [TechniqueTypeInline]
    class Meta:
        model = TechniqueCategory


class TechniqueFilterValueInline(admin.TabularInline):
    model = TechniqueFilterValue
    extra = 0


class TechniqueFilterAdmin(admin.ModelAdmin):
    inlines = [TechniqueFilterValueInline]
    class Meta:
        model = TechniqueFilter

class TechniqueUnitImageInline(admin.TabularInline):
    model = TechniqueUnitImage
    extra = 0

class TechniqueUnitImageDocInline(admin.TabularInline):
    model = TechniqueUnitImageDoc
    extra = 0

class TechniqueUnitAdmin(admin.ModelAdmin):
    inlines = [TechniqueUnitImageInline,TechniqueUnitImageDocInline]
    class Meta:
        model = TechniqueUnit

admin.site.register(TechniqueType)
admin.site.register(TechniqueFilterValue)
admin.site.register(TechniqueFilter,TechniqueFilterAdmin)
admin.site.register(TechniqueUnit,TechniqueUnitAdmin)
# admin.site.register(TechniqueUnitImage)
# admin.site.register(TechniqueUnitFeedback)
admin.site.register(TechniqueCategory,TechniqueCategoryAdmin)
