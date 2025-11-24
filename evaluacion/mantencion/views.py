from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from .forms import ResponsableForm, MaquinaForm, MantencionForm
from .models import Responsable, Maquina, Mantencion
import pymysql


def login_view(request):
	error = None
	if request.method == 'POST':
		user = request.POST.get('username')
		password = request.POST.get('password')
		# try to connect to MariaDB with provided credentials
		db_settings = settings.DATABASES.get('default', {})
		host = db_settings.get('HOST', '127.0.0.1') or '127.0.0.1'
		port = int(db_settings.get('PORT', 3306) or 3306)
		dbname = db_settings.get('NAME')
		try:
			conn = pymysql.connect(host=host, port=port, user=user, password=password, database=dbname, connect_timeout=5)
			conn.close()
			# mark session as authenticated
			request.session['db_authenticated'] = True
			request.session['db_user'] = user
			return redirect('main')
		except Exception as e:
			error = 'Conexión fallida: credenciales incorrectas o DB inaccesible.'

	return render(request, 'mantencion/login.html', {'error': error})


def logout_view(request):
	request.session.pop('db_authenticated', None)
	request.session.pop('db_user', None)
	return redirect('login')


def require_db_auth(view_func):
	def wrapper(request, *args, **kwargs):
		if not request.session.get('db_authenticated'):
			return redirect('login')
		return view_func(request, *args, **kwargs)

	return wrapper


@require_db_auth
def main_view(request):
	mantenciones = Mantencion.objects.select_related('id_maquina', 'id_responsable').order_by('-fecha')[:20]
	return render(request, 'mantencion/main.html', {'mantenciones': mantenciones})


@require_db_auth
def create_responsable(request):
	if request.method == 'POST':
		form = ResponsableForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('main')
	else:
		form = ResponsableForm()
	return render(request, 'mantencion/create_responsable.html', {'form': form})


@require_db_auth
def create_maquina(request):
	if request.method == 'POST':
		form = MaquinaForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('main')
	else:
		form = MaquinaForm()
	return render(request, 'mantencion/create_maquina.html', {'form': form})


@require_db_auth
def create_mantencion(request):
	if request.method == 'POST':
		form = MantencionForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('main')
	else:
		form = MantencionForm()
	return render(request, 'mantencion/create_mantencion.html', {'form': form})


@require_db_auth
def delete_mantencion(request, pk):
	if request.method == 'POST':
		try:
			m = Mantencion.objects.get(pk=pk)
			m.delete()
		except Mantencion.DoesNotExist:
			pass
	return redirect('main')

