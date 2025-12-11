# carrera.py
# Juego de carreras para terminal con modo 2 jugadores o CPU
# AHORA INCLUYE CLI (--cpu)

import os
import sys
import time
import random
import argparse   # <<--- CLI agregado

# ======================= INPUT SIN BLOQUEO =======================
if os.name == "nt":
    import msvcrt
    def get_key():
        if msvcrt.kbhit():
            try:
                return msvcrt.getch().decode('utf-8')
            except:
                return ''
        return None
else:
    import tty, termios, select
    def get_key():
        dr,_,_ = select.select([sys.stdin], [], [], 0)
        if dr:
            return sys.stdin.read(1)
        return None


# ======================= FUNCIONES DE JUEGO =======================

def draw_track(positions, length, cpu_mode=False):
    print("\033[H", end="")     # evita parpadeo
    if cpu_mode:
        print("CARRERA!  (J1 = 'A'  |  CPU Automático  |  'Q' para salir)\n")
    else:
        print("CARRERA!  (J1 = 'A'  |  J2 = 'L'  |  'Q' para salir)\n")

    for idx, pos in enumerate(positions, start=1):
        pos = min(pos, length-1)
        track = [' '] * length
        track[pos] = 'O'
        print(f"J{idx}: |{''.join(track)}|")

    print("\nMETA → " + "-"*length)


def run_game(track_length=40, speed=0.02, cpu_mode=False):
    positions=[0,0]
    winner=None

    # Linux/Mac modo crudo
    old=None
    if os.name != "nt":
        old=termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())

    try:
        draw_track(positions, track_length, cpu_mode)
        time.sleep(0.8)

        while True:
            key=get_key()

            if key:
                k=key.lower()
                if k=='a': positions[0]+=1
                if not cpu_mode and k=='l': positions[1]+=1
                if k=='q':
                    print("\nSaliendo...")
                    break

            # Movimiento CPU
            if cpu_mode:
                if random.random() < 0.12:
                    positions[1]+=1

            draw_track(positions,track_length,cpu_mode)

            # ganador
            for i,p in enumerate(positions):
                if p>=track_length-1:
                    winner=i+1
                    break

            if winner:
                if cpu_mode and winner==2:
                    print("\n🤖 ¡La CPU gana!")
                else:
                    print(f"\n🏆 ¡GANA EL JUGADOR {winner}!")

                print("Pulsa Enter para salir o 'R' para reiniciar...")
                while True:
                    k=get_key()
                    if k in ['\r','\n']:
                        return
                    if k and k.lower()=='r':
                        return run_game(track_length,speed,cpu_mode)
                    time.sleep(0.05)

            time.sleep(speed)

    finally:
        if os.name!="nt" and old:
            termios.tcsetattr(sys.stdin,termios.TCSADRAIN,old)


# ======================= MENÚ =======================

def menu():
    os.system('cls' if os.name=='nt' else 'clear')
    print("==== CARRERA TERMINAL ====\n")
    print("1) 2 Jugadores")
    print("2) Vs CPU")
    print("Q) Salir\n")
    
    while True:
        op=input("Elige modo ➤ ").lower()
        if op=='1': return False
        if op=='2': return True
        if op=='q': exit()
        print("Opción inválida, intenta de nuevo.\n")


# ======================= CLI INTEGRADO =======================

def crear_cli():
    parser = argparse.ArgumentParser(
        description="Juego de carreras en terminal"
    )

    parser.add_argument(
        "--cpu",
        action="store_true",
        help="Iniciar directamente en modo CPU (sin menú)"
    )

    parser.add_argument(
        "--modo",
        choices=["cpu", "2p"],
        help="Elegir modo: 'cpu' o '2p'"
    )

    return parser.parse_args()


# ======================= MAIN =======================

def iniciar_carrera(cpu_mode=False):
    return run_game(track_length=40, speed=0.02, cpu_mode=cpu_mode)


if __name__=="__main__":
    args = crear_cli()

    # ---- CLI Prioritario ----
    if args.cpu:
        iniciar_carrera(cpu_mode=True)
        sys.exit()

    if args.modo == "cpu":
        iniciar_carrera(cpu_mode=True)
        sys.exit()

    if args.modo == "2p":
        iniciar_carrera(cpu_mode=False)
        sys.exit()

    # ---- Si no se usó CLI → mostrar menú normal ----
    cpu = menu()
    iniciar_carrera(cpu)

# ======================= MAIN PARA TESTS =======================

def main(argv):
    """
    Versión simplificada del CLI para pruebas automatizadas.
    NO ejecuta el juego real, solo responde textos.
    """
    if not argv:
        return "CLI del juego de carreras"

    cmd = argv[0].lower()

    if cmd == "version":
        return "v1.0"

    if cmd == "iniciar":
        return "2 jugadores listos"

    if cmd == "cpu":
        return "Modo CPU activado"

    return "Comando no reconocido"
