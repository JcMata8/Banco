from django.shortcuts import render, redirect
from .forms import ClienteForm, CuentaForm, TransaccionForm
from django.contrib import messages
from Administracion.models import *
from decimal import Decimal


def registrar_cliente(request):

    form = ClienteForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('registrar_clientes')

    return render(request, 'registro_clientes.html', {'form': form})


def registrar_cuenta(request):

    form = CuentaForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('registrar_cuentas')

    return render(request, 'registro_cuentas.html', {'form': form})


def registrar_transaccion(request):
    if request.method == 'POST':
        
        cuenta = request.POST.get('cuenta')
        saldo = Cuenta.objects.get(numero_cuenta = cuenta)
        monto = request.POST.get('monto')
        monto = Decimal(monto)
        tipo = request.POST.get('tipo')
        descripcion = request.POST.get('descripcion')
        
        
        if tipo == 'deposito':
            saldo.saldo += monto
            saldo.save()
                
            deposito = Transaccion.objects.create(
                cuenta = saldo, 
                tipo = tipo, 
                monto = monto,
                descripcion = descripcion
            )
            
            messages.success(request, "Transacción Exitosa")
            
            
        else:
            
            if saldo.saldo < monto:
                
                messages.error(request, "No tienes suficiente saldo")
                
                return redirect("registrar_transaccion")
            

            else:
                saldo.saldo -= monto
                saldo.save()
            
            retiro = Transaccion.objects.create(
                cuenta = saldo, 
                tipo = tipo, 
                monto = monto,
                descripcion = descripcion
            )   
            
            messages.success(request, "Transacción Exitosa")
   
        return redirect('Historial_transacciones')
 
    
    form = TransaccionForm(request.POST or None)
    
    return render(request, 'registro_transaccion.html', {'form': form})



def Ver_listado_clientes(request):
    
    listado_clientes =Cliente.objects.all().order_by('nombre')
    
    return render(request, 'Ver_listado_clientes.html', {'clientes':listado_clientes})

def Self_lista_cuentas(request, dpi):
    
    cliente_id = Cuenta.objects.filter(cliente = dpi)    
    
    return render(request,'Self_lista_cuentas.html', {'cuenta':cliente_id})

def Transacciones(request, numero_cuenta):

    cuenta_origen = Cuenta.objects.get(numero_cuenta = numero_cuenta)
    saldo = Cuenta.objects.get(numero_cuenta = cuenta_origen)
    
    if request.method == 'POST':
        
        cuenta_destino = request.POST.get('cuenta')
        saldo_destino = Cuenta.objects.get(numero_cuenta = cuenta_destino)
        monto = request.POST.get('monto')
        monto = Decimal(monto)
        
        if cuenta_origen.saldo < monto:
            
            messages.error(request, "No tienes suficiente saldo")
            return redirect("Transacciones",numero_cuenta)
        
        else:
            cuenta_origen.saldo -= monto
            saldo_destino.saldo += monto
            
            cuenta_origen.save()
            saldo_destino.save()
            
            retiro = Transaccion.objects.create(
                cuenta = cuenta_origen, 
                tipo = "Retiro", 
                monto = monto,
                descripcion = "Transferencia a otra cuenta"
            )
            
            deposito = Transaccion.objects.create(
                cuenta = saldo_destino, 
                tipo = "Depósito", 
                monto = monto,
                descripcion = "Transferencia a otra cuenta"
            )
            
            messages.success(request, "Transacción Exitosa")
            
            return redirect("Transacciones",numero_cuenta)
            
    
                  
    form = TransaccionForm(request.POST or None)
    
    return render(request, 'Transacciones.html', {'form': form, 'cuenta_origen':cuenta_origen, 'saldo': saldo})

def Historial_transacciones(request):
    
    listado_transacciones =Transaccion.objects.all().order_by('fecha')
    
    return render(request, 'Historial_transacciones.html', {'transacciones':listado_transacciones})

def Historial_transacciones_individual(request, numero_cuenta):
    
    cuenta = Cuenta.objects.get(numero_cuenta = numero_cuenta)
    
    listado_transacciones =Transaccion.objects.filter(cuenta = cuenta).order_by('fecha')
    
    return render(request, 'Historial_transacciones.html', {'transacciones':listado_transacciones})










