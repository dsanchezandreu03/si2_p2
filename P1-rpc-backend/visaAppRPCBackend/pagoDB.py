# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# author: rmarabini
"Interface with the dataabse"
from visaAppRPCBackend.models import Tarjeta, Pago

from modernrpc.core import rpc_method
from django.forms.models import model_to_dict

@rpc_method
def verificar_tarjeta(tarjeta_data):
    """ Check if the tarjeta is registered 
    :param tarjeta_dict: dictionary with the tarjeta data
                       (as provided by TarjetaForm)
    :return True or False if tarjeta_data is not valid
    """
    if bool(tarjeta_data) is False or not\
       Tarjeta.objects.filter(**tarjeta_data).exists():
        return False
    return True

@rpc_method
def registrar_pago(pago_dict):
    """ Register a payment in the database
    :param pago_dict: dictionary with the pago data (as provided by PagoForm)
      plus de tarjeta_id (numero) of the tarjeta
    :return new pago info if succesful, None otherwise
    """
    try:
        pago = Pago.objects.create(**pago_dict)
        # get default values from pago
        pago = Pago.objects.get(pk=pago.pk)

        pago_a_devolver = model_to_dict(pago)
        pago_a_devolver['marcaTiempo'] = str(pago.marcaTiempo)
    except Exception as e:
        print("Error: Registrando pago: ", e)
        return None
    return pago_a_devolver

@rpc_method
def eliminar_pago(idPago):
    """ Delete a pago in the database
    :param idPago: id of the pago to be deleted
    :return True if succesful,
     False otherwise
     """
    try:
        pago = Pago.objects.get(id=idPago)
    except Pago.DoesNotExist:
        return False
    pago.delete()
    return True

@rpc_method
def get_pagos_from_db(idComercio):
    """ Gets pagos in the database correspondint to some idComercio
    :param idComercio: id of the comercio to get pagos from 
    :return list of pagos found
     """
    pagos = Pago.objects.filter(idComercio=idComercio)

    pagos_a_devolver = []

    for pago in pagos:
        pago_a_devolver = model_to_dict(pago)
        pago_a_devolver['marcaTiempo'] = str(pago.marcaTiempo)

        pagos_a_devolver.append(pago_a_devolver)

    return pagos_a_devolver
