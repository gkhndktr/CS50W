from django.contrib import admin
from .models import User, product,bid,comment


# Register your models here.
admin.site.register(product)
admin.site.register(User)
admin.site.register(bid)
admin.site.register(comment)
