from django.shortcuts import render
from django.views.generic import View

class ProductsView(View):
    template_name = 'products/index.html'

    def get(self, request):
        return render(request, self.template_name)
