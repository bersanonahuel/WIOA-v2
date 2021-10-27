from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from .forms import FormularioLogin

class Login(FormView):
    template_name = 'login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('index')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)

    #Django llama primero al metodo dispatch, y antes de redireccionar llama al metodo form_valid
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            #Si esta logueado, lo redirecciona a la url de success_url
            return HttpResponseRedirect(self.get_success_url())
        else:
            #Si no esta logueado, lo manda a la vista login.
            return super(Login,self).dispatch(request, *args, **kwargs)

    def form_valid(self,form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)

def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login')