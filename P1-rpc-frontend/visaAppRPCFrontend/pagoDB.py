# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# author: rmarabini
"""RPC client interface (Frontend)"""

from django.conf import settings
from xmlrpc.client import ServerProxy


def verificar_tarjeta(tarjeta_data: dict) -> bool:
    """
    Comprueba remotamente si una tarjeta está registrada.

    Args:
        tarjeta_data (dict): datos de tarjeta (tal y como los produce TarjetaForm).

    Returns:
        bool: True si la tarjeta existe/valida, False en caso contrario.
    """
    with ServerProxy(settings.RPCAPIBASEURL) as proxy:
        return proxy.verificar_tarjeta(tarjeta_data)


def registrar_pago(pago_dict: dict):
    """
    Registra remotamente un pago.

    Args:
        pago_dict (dict): datos del pago (tal y como los produce PagoForm),
                          incluyendo tarjeta_id (número de tarjeta).

    Returns:
        dict | None: diccionario con los datos del pago creado (incluye marcaTiempo),
                     o None si hubo error.
    """
    with ServerProxy(settings.RPCAPIBASEURL) as proxy:
        return proxy.registrar_pago(pago_dict)


def eliminar_pago(idPago: int) -> bool:
    """
    Elimina remotamente un pago.

    Args:
        idPago (int): identificador del pago a eliminar.

    Returns:
        bool: True si se eliminó, False si no existía o falló.
    """
    with ServerProxy(settings.RPCAPIBASEURL) as proxy:
        return proxy.eliminar_pago(idPago)


def get_pagos_from_db(idComercio: str):
    """
    Obtiene remotamente la lista de pagos asociados a un comercio.

    Args:
        idComercio (str): identificador del comercio.

    Returns:
        list[dict]: lista de pagos (cada pago como diccionario, incluye marcaTiempo).
    """
    with ServerProxy(settings.RPCAPIBASEURL) as proxy:
        return proxy.get_pagos_from_db(idComercio)
