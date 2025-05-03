import pygame
import sys

# ─── CONFIGURACIÓN ──────────────────────────────────────────────────────────
FPS = 60

# Conversión metros → píxeles
SCALE = 1                   # 100 px = 1 m

# Distancia a recorrer por A (en metros)
d_m = 500.0
d_px = d_m * SCALE

# Ventana
WIDTH, HEIGHT = 400 + d_px, 600

# Física
g = 9.81                      # m/s²
m1 = 2.0                      # masa bloque A (kg)
m2 = 900.0                      # masa bloque B (kg)
a = (m2 * g) / (m1 + m2)      # aceleración constante (m/s²)

# Dimensiones bloques
BW, BH = 50, 50               # ancho/alto en px

# Posiciones iniciales
x1 = 100                      # bloque A, eje X
y_table = HEIGHT // 2 + 50    # mesa (y de la superficie)
y1 = y_table - BH             # bloque A, eje Y
pulley_x = x1 + d_px + 100    # x de la polea, a la derecha de A
pulley_y = y_table - BH//2    # y de la polea

x2 = pulley_x                 # bloque B, centrado bajo polea
y2 = pulley_y + 20            # bloque B, ligeramente separado

# Estados de movimiento
v = 0.0                       # velocidad (m/s)
t = 0.0                       # tiempo transcurrido (s)
running = True

# ─── INICIALIZAR PYGAME ──────────────────────────────────────────────────────
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# ─── BUCLE PRINCIPAL ─────────────────────────────────────────────────────────
while running:
    dt = clock.tick(FPS) / 1000.0   # delta t en segundos

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    F_weight = m2 * g  # fuerza hacia abajo (N)
    # tensión en la cuerda (fuerza que siente A)
    T = (m1 * m2 * g) / (m1 + m2)  # N
    # aceleración resultante sobre A
    a = T / m1  # m/s²

    # ── Física: si A no llegó a d, seguimos moviendo ─────────────────────────
    if x1 < 100 + d_px:
        v += a * dt                  # v = v + a·dt
        dx = v * dt * SCALE         # desplazamiento en px
        x1 += dx
        y2 += dx                    # B baja la misma longitud de cuerda
        t += dt

    # ── Dibujo ────────────────────────────────────────────────────────────────
    screen.fill((240, 240, 240))

    # Mesa
    pygame.draw.rect(screen, (100, 100, 100),(0, y_table, WIDTH, HEIGHT - y_table))

    # Bloque A
    pygame.draw.rect(screen, (200, 50, 50), (x1, y1, BW, BH))

    # Polea
    pygame.draw.circle(screen, (80, 80, 80), (pulley_x, pulley_y), 30)
    pygame.draw.circle(screen, (150, 150, 150), (pulley_x, pulley_y), 25)

    # Bloque B
    pygame.draw.rect(screen, (50, 100, 200), (x2, y2, BW, BH))

    # Cuerda (línea A → polea y polea → B)
    # desde el punto medio superior de A
    start_A = (x1 + BW // 2, y1)
    # hasta el borde izquierdo de la polea
    mid_rope = (pulley_x , pulley_y-BH/2)
    # desde borde derecho de polea hasta punto medio superior de B
    end_B = (pulley_x+BW/2, y2)
    pygame.draw.line(screen, (0, 0, 0), start_A, mid_rope, 2)
    pygame.draw.line(screen, (0, 0, 0), (pulley_x + 25, pulley_y), end_B, 2)


    # Texto con tiempo y aceleración
    info = f"Bloque_rojo = {m1:.2f} kg      Bloque_Azul = {m2:2f} kg"
    info2 = f"Fuerza_Bloque_Azul = {F_weight:.2f}N      distancia = {d_m:} m"
    info3 = f"a = {a:.2f} m/s²      T = {T:.2f} N      tiempo = {t:.2f} s    velocidad = {v:.2f} m/s"
    label = font.render(info, True, (0, 0, 0))
    label2 = font.render(info2, True, (0, 0, 0))
    label3 = font.render(info3, True, (0, 0, 0))
    screen.blit(label, (10, 10))
    screen.blit(label2, (10, 30))
    screen.blit(label3, (10, 50))

    pygame.display.flip()

pygame.quit()
sys.exit()
