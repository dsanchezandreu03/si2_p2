#!/usr/bin/env python3
import os
import time
import argparse
import statistics

import os, sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def load_env_file(env_path: str) -> None:
    """
    Carga un fichero tipo 'env' al estilo KEY=VALUE (aunque tenga espacios alrededor del '='),
    y mete las variables en os.environ.
    Ignora comentarios y líneas vacías.
    """
    if not env_path:
        return
    if not os.path.exists(env_path):
        raise FileNotFoundError(f"No existe el env: {env_path}")

    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
                value = value[1:-1]

            os.environ[key] = value

def setup_django() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "visaSite.settings")
    import django
    django.setup()

def one_run() -> float:
    from visaAppRPCFrontend.models import Tarjeta

    pks = list(Tarjeta.objects.values_list("pk", flat=True)[:1000])

    start = time.time()
    for pk in pks:
        _ = Tarjeta.objects.get(pk=pk)
    end = time.time()

    return end - start

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", default="",
                        help="Ruta al fichero env (ej: /ruta/a/P1-base/env)")
    parser.add_argument("--runs", type=int, default=1,
                        help="Número de repeticiones (ej: 7)")
    args = parser.parse_args()

    if args.env:
        load_env_file(args.env)

    setup_django()

    times = []
    for i in range(args.runs):
        t = one_run()
        times.append(t)
        print(f"Run {i+1}: {t:.6f} s")

    if args.runs >= 2:
        mean = statistics.mean(times)
        stdev = statistics.stdev(times)  
        print(f"MEDIA: {mean:.6f} s")
        print(f"DESV_STD: {stdev:.6f} s")

if __name__ == "__main__":
    main()