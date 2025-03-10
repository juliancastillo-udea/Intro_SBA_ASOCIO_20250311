import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parámetros de la simulación
Nx = 32        # número de puntos en x
Ny = 32        # número de puntos en y
Lx = 2.0       # Maximo en x
Ly = 2.0       # Maximo en y
c = 1.0         # velocidad de propagación de la onda
dx = Lx / (Nx - 1) # tamaño de la malla en x
dy = Ly / (Ny - 1) # tamaño de la malla en y
dt = 0.005      # paso de tiempo
steps = 300     # cuántos pasos de tiempo simularemos

# Crear malla
x = np.linspace(0, Lx, Nx)
y = np.linspace(0, Ly, Ny)
X, Y = np.meshgrid(x, y)

# Arrays para la altura de la onda en cada instante
u_n = np.zeros((Ny, Nx))   # estado en tiempo n
u_nm1 = np.zeros((Ny, Nx)) # estado en tiempo n-1
u_np1 = np.zeros((Ny, Nx)) # estado en tiempo n+1

# Condición inicial: una perturbación (gota) en el centro
cx = Nx // 2
cy = Ny // 2

# Por ejemplo, un pico gaussiano en el centro para simular la perturbación
sigma = 0.05
for j in range(Ny):
    for i in range(Nx):
        dist_sq = ((i - cx) * dx)**2 + ((j - cy) * dy)**2
        u_n[j, i] = np.exp(-dist_sq / (2 * sigma**2))

# Asumimos u_nm1 = u_n para un arranque en reposo o, 
# alternativamente, podemos dejarlo en ceros para indicar que antes no había perturbación
u_nm1[:] = u_n[:]

# Coeficiente para el método de diferencias finitas
coef = (c * dt / dx)**2

# Función para actualizar la simulación
def update(frame):
    global u_n, u_nm1, u_np1
    
    # Recorremos la malla interna (excluyendo bordes para no salirnos)
    for j in range(1, Ny - 1):
        for i in range(1, Nx - 1):
            # Aproximación de la segunda derivada (2D) usando diferencias finitas
            dudx2 = u_n[j, i-1] - 2*u_n[j, i] + u_n[j, i+1]
            dudy2 = u_n[j-1, i] - 2*u_n[j, i] + u_n[j+1, i]
            
            # Ecuación de onda discreta
            u_np1[j, i] = (2*u_n[j, i] - u_nm1[j, i] 
                           + coef * (dudx2 + dudy2))
    
    # Condiciones de frontera simples (bordes fijos: u=0)
    u_np1[0, :] = 0
    u_np1[-1, :] = 0
    u_np1[:, 0] = 0
    u_np1[:, -1] = 0
    
    # Intercambiar referencias para avanzar en el tiempo
    u_nm1, u_n, u_np1 = u_n, u_np1, u_nm1
    
    # Actualizar los datos de la superficie en la gráfica
    # devuelto como lista para que FuncAnimation sepa qué actualizar
    surface.set_array(u_n)
    return [surface]

# Crear la figura y el objeto de imagen
fig, ax = plt.subplots()
surface = ax.imshow(u_n, cmap='viridis', origin='lower',
                    extent=[0, Lx, 0, Ly], vmin=-0.5, vmax=1.0)
ax.set_title("Caída de una gota - Simulación de onda 2D")
ax.set_xlabel("x")
ax.set_ylabel("y")

# Crear la animación
ani = animation.FuncAnimation(fig, update, frames=steps, interval=30, blit=True)

plt.colorbar(surface, ax=ax, fraction=0.026, pad=0.04, label="Altura")
plt.show()
