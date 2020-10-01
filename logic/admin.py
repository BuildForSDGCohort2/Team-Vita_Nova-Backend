from django.contrib import admin
import logic.models as lm


# Register your models here.

class DistributorAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'user', 'active_distributor', 'departure', 'destination', 'purpose_of_travel',
                    'active_contact_number', 'mode_of_travel', 'additional_comment', 'travel_schedule', 'status')


class SenderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'user', 'distributor', 'goods_image', 'departure', 'destination', 'budget',
                    'delivery_contact_number', 'goods_category', 'description_of_goods', 'travel_schedule', 'status',
                    'accepted_terms', 'active')


admin.site.register(lm.Distributor, DistributorAdmin)
admin.site.register(lm.Sender, SenderAdmin)
