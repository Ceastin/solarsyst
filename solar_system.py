import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random
import numpy as np

# Initialize Pygame and OpenGL
pygame.init()
WIDTH, HEIGHT = 1024, 768
display = (WIDTH, HEIGHT)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Set up OpenGL
gluPerspective(45, WIDTH / HEIGHT, 0.1, 5000.0)
glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, 0, 1))  # Sun at origin
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.1, 0.1, 0.1, 1))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# Texture loader for solid colors
def load_texture(color):
    image = pygame.Surface((1, 1))
    image.fill((int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)))
    data = pygame.image.tostring(image, "RGBA", 1)
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 1, 1, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    return texture

# Planet textures as solid colors mimicking real appearances
planet_textures = {
    "Sun": load_texture((1.0, 0.9, 0.0)),          # Bright yellow
    "Mercury": load_texture((0.7, 0.7, 0.7)),      # Gray
    "Venus": load_texture((1.0, 0.8, 0.5)),        # Yellowish-orange
    "Earth": load_texture((0.0, 0.5, 1.0)),        # Blue
    "Earth_night": load_texture((0.0, 0.2, 0.4)),  # Dark blue with lights
    "Mars": load_texture((1.0, 0.3, 0.3)),         # Reddish
    "Jupiter": load_texture((1.0, 0.7, 0.4)),      # Orange-brown
    "Saturn": load_texture((1.0, 0.9, 0.6)),       # Pale yellow
    "Uranus": load_texture((0.5, 0.9, 1.0)),       # Cyan
    "Neptune": load_texture((0.0, 0.3, 1.0)),      # Deep blue
    "Moon": load_texture((0.8, 0.8, 0.8)),         # Light gray
    "Rings": load_texture((0.9, 0.8, 0.7)),        # Light beige
    "Asteroid": load_texture((0.6, 0.5, 0.4)),     # Brownish-gray
    "Probe": load_texture((0.5, 0.5, 0.5)),        # Metallic gray
    "Galaxy": load_texture((0.8, 0.8, 1.0))        # Pale purple-blue
}

# Planet data with realistic proportions (scaled for visualization)
planets = [
    {"name": "Mercury", "a": 58, "e": 0.2056, "speed": 0.04787, "size": 2.44, "texture": planet_textures["Mercury"], "color": (0.8, 0.8, 0.8), "moons": [], "trail": [], "label": False},
    {"name": "Venus", "a": 108, "e": 0.0068, "speed": 0.03502, "size": 6.05, "texture": planet_textures["Venus"], "color": (1, 0.8, 0.5), "moons": [], "trail": [], "label": False},
    {"name": "Earth", "a": 150, "e": 0.0167, "speed": 0.02978, "size": 6.37, "texture": planet_textures["Earth"], "color": (0, 0.5, 1), "moons": [{"radius": 5, "speed": 0.1, "size": 1.74, "texture": planet_textures["Moon"], "name": "Moon", "label": False}], "trail": [], "label": False},
    {"name": "Mars", "a": 228, "e": 0.0934, "speed": 0.02413, "size": 3.39, "texture": planet_textures["Mars"], "color": (1, 0.3, 0.3), "moons": [], "trail": [], "label": False},
    {"name": "Jupiter", "a": 778, "e": 0.0484, "speed": 0.01307, "size": 69.91, "texture": planet_textures["Jupiter"], "color": (1, 0.7, 0.4), "moons": [], "trail": [], "label": False},
    {"name": "Saturn", "a": 1430, "e": 0.0541, "speed": 0.00969, "size": 58.23, "texture": planet_textures["Saturn"], "color": (1, 0.9, 0.6), "moons": [], "trail": [], "rings": True, "label": False},
    {"name": "Uranus", "a": 2870, "e": 0.0472, "speed": 0.00681, "size": 25.36, "texture": planet_textures["Uranus"], "color": (0.5, 0.9, 1), "moons": [], "trail": [], "label": False},
    {"name": "Neptune", "a": 4500, "e": 0.0086, "speed": 0.00543, "size": 24.62, "texture": planet_textures["Neptune"], "color": (0, 0.3, 1), "moons": [], "trail": [], "label": False}
]

# Scale down astronomical units for visualization
for planet in planets:
    planet["a"] /= 25
    planet["size"] /= 10
    planet["speed"] *= 10

# Starfield, nebulae, galaxies, etc.
stars = [{"pos": (random.uniform(-1000, 1000), random.uniform(-1000, 1000), random.uniform(-1000, 1000)), "size": random.uniform(1, 3), "color": (random.uniform(0.5, 1), random.uniform(0.5, 1), random.uniform(0.5, 1))} for _ in range(2000)]
nebulae = [{"pos": (random.uniform(-500, 500), random.uniform(-500, 500), random.uniform(-500, 500)), "size": random.uniform(50, 100), "color": (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1), 0.1)} for _ in range(5)]
galaxies = [{"pos": (random.uniform(-800, 800), random.uniform(-800, 800), random.uniform(-800, 800)), "size": random.uniform(20, 50), "texture": planet_textures["Galaxy"]} for _ in range(3)]
asteroids = [{"a": random.uniform(70, 80), "e": random.uniform(0, 0.1), "speed": random.uniform(0.01, 0.02), "size": random.uniform(0.2, 0.5), "angle": random.uniform(0, 2 * math.pi), "name": "Asteroid", "label": False} for _ in range(200)]
probe = {"radius": 6, "speed": 0.05, "size": 0.5, "texture": planet_textures["Probe"], "angle": 0, "name": "Probe", "label": False}

# Camera and simulation variables
camera_pos = [0, 50, -250]
camera_angle_x, camera_angle_y = 0, 0
selected_planet = 0
angle = 0
time_scale = 1.0
paused = False
font = pygame.font.Font(None, 24)
clock = pygame.time.Clock()

# Draw orbital path with pulsing effect
def draw_orbit(a, e, color):
    glColor4f(*color, 0.5 + 0.5 * math.sin(angle))
    glBegin(GL_LINE_LOOP)
    for i in range(100):
        nu = 2 * math.pi * i / 100
        r = a * (1 - e**2) / (1 + e * math.cos(nu))
        glVertex3f(r * math.cos(nu), 0, r * math.sin(nu))
    glEnd()

# Draw label in 3D space
def draw_label(x, y, z, name):
    glPushMatrix()
    glTranslatef(x, y + 1, z)
    glRasterPos3f(0, 0, 0)
    surface = font.render(name, True, (255, 255, 255), (0, 0, 0, 100))
    data = pygame.image.tostring(surface, "RGBA", True)
    glDrawPixels(surface.get_width(), surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, data)
    glPopMatrix()

# Draw 2D overlays (toolbar and controls)
def draw_2d():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, WIDTH, 0, HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)

    # Toolbar (bottom)
    glColor4f(0, 0, 0, 0.7)
    glBegin(GL_QUADS)
    glVertex2f(0, 0); glVertex2f(WIDTH, 0); glVertex2f(WIDTH, 100); glVertex2f(0, 100)
    glEnd()

    planet = planets[selected_planet]
    earth_speed = planets[2]["speed"]
    texts = [
        f"Planet: {planet['name']}",
        f"Distance: {planet['a'] * (1 - planet['e']**2) / (1 + planet['e'] * math.cos(angle * planet['speed'])):.1f} units",
        f"Eccentricity: {planet['e']:.4f}",
        f"Speed: {planet['speed'] * time_scale:.3f} (Rel. to Earth: {planet['speed']/earth_speed:.2f})",
        f"Size: {planet['size']:.2f} units",
        f"Time: {int(angle / 0.05)} days"
    ]
    for i, text in enumerate(texts):
        surface = font.render(text, True, (255, 255, 255))
        data = pygame.image.tostring(surface, "RGBA", True)
        glRasterPos2d(10, 85 - i * 15)
        glDrawPixels(surface.get_width(), surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, data)

    buttons = ["<<", "<", "||", ">", ">>"]
    for i, btn in enumerate(buttons):
        surface = font.render(btn, True, (255, 255, 255))
        data = pygame.image.tostring(surface, "RGBA", True)
        glRasterPos2d(500 + i * 50, 20)
        glDrawPixels(surface.get_width(), surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, data)

    # Controls box (right side)
    glColor4f(0, 0, 0, 0.7)
    glBegin(GL_QUADS)
    glVertex2f(WIDTH - 200, HEIGHT - 250); glVertex2f(WIDTH, HEIGHT - 250)
    glVertex2f(WIDTH, HEIGHT); glVertex2f(WIDTH - 200, HEIGHT)
    glEnd()

    controls = [
        "Controls:",
        "Left Drag: Rotate",
        "Right Click: Toggle Labels",
        "Mouse Wheel: Zoom",
        "1-8: Select Planet",
        "P: Pause",
        "Left/Right: Time Scale",
        "R: Reset Camera"
    ]
    for i, text in enumerate(controls):
        surface = font.render(text, True, (255, 255, 255))
        data = pygame.image.tostring(surface, "RGBA", True)
        glRasterPos2d(WIDTH - 190, HEIGHT - 20 - i * 20)
        glDrawPixels(surface.get_width(), surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, data)

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
            camera_angle_y += event.rel[0] * 0.2
            camera_angle_x = max(-90, min(90, camera_angle_x + event.rel[1] * 0.2))
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mx, my = event.pos
            for planet in planets:
                planet["label"] = not planet["label"]
                for moon in planet["moons"]:
                    moon["label"] = not moon["label"]
            for asteroid in asteroids:
                asteroid["label"] = not asteroid["label"]
            probe["label"] = not probe["label"]
        elif event.type == pygame.MOUSEWHEEL:
            camera_pos[2] = max(-500, min(-10, camera_pos[2] + event.y * 5))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                camera_pos = [0, 50, -250]; camera_angle_x = camera_angle_y = 0
            elif pygame.K_1 <= event.key <= pygame.K_8:
                selected_planet = event.key - pygame.K_1
            elif event.key == pygame.K_p:
                paused = not paused
            elif event.key == pygame.K_LEFT:
                time_scale = max(0.1, time_scale - 0.1)
            elif event.key == pygame.K_RIGHT:
                time_scale += 0.1

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluPerspective(45, WIDTH / HEIGHT, 0.1, 5000.0)
    glTranslatef(*camera_pos)
    glRotatef(camera_angle_x, 1, 0, 0)
    glRotatef(camera_angle_y, 0, 1, 0)

    # Starfield
    glDisable(GL_LIGHTING)
    for star in stars:
        glPointSize(star["size"])
        glBegin(GL_POINTS)
        glColor3f(*star["color"])
        glVertex3f(*star["pos"])
        glEnd()

    # Nebulae
    for nebula in nebulae:
        glColor4f(*nebula["color"])
        glPushMatrix()
        glTranslatef(*nebula["pos"])
        glScalef(nebula["size"], nebula["size"], nebula["size"])
        quad = gluNewQuadric()
        gluSphere(quad, 1, 10, 10)
        glPopMatrix()

    # Galaxies
    for galaxy in galaxies:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, galaxy["texture"])
        glPushMatrix()
        glTranslatef(*galaxy["pos"])
        glScalef(galaxy["size"], galaxy["size"], 0.1)
        gluDisk(gluNewQuadric(), 0, 1, 20, 1)
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)

    # Sun
    glEnable(GL_LIGHTING)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, planet_textures["Sun"])
    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    gluSphere(quad, 10, 20, 20)
    glDisable(GL_TEXTURE_2D)

    # Orbits
    for planet in planets:
        draw_orbit(planet["a"], planet["e"], planet["color"])

    # Planets and moons
    for planet in planets:
        nu = angle * planet["speed"]
        r = planet["a"] * (1 - planet["e"]**2) / (1 + planet["e"] * math.cos(nu))
        x, z = r * math.cos(nu), r * math.sin(nu)
        glPushMatrix()
        glTranslatef(x, 0, z)
        glRotatef(angle * 10, 0, 1, 0)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, planet["texture"])
        quad = gluNewQuadric()
        gluQuadricTexture(quad, GL_TRUE)
        gluSphere(quad, planet["size"], 20, 20)
        glDisable(GL_TEXTURE_2D)
        if planet["label"]:
            draw_label(x, planet["size"], z, planet["name"])

        if "rings" in planet:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, planet_textures["Rings"])
            glRotatef(30, 1, 0, 0)
            gluDisk(gluNewQuadric(), planet["size"], planet["size"] * 1.5, 20, 1)
            glDisable(GL_TEXTURE_2D)

        for moon in planet["moons"]:
            mx = x + moon["radius"] * math.cos(angle * moon["speed"])
            mz = z + moon["radius"] * math.sin(angle * moon["speed"])
            glPushMatrix()
            glTranslatef(mx - x, 0, mz - z)
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, moon["texture"])
            gluSphere(gluNewQuadric(), moon["size"], 10, 10)
            glDisable(GL_TEXTURE_2D)
            if moon["label"]:
                draw_label(mx - x, moon["size"], mz - z, moon["name"])
            glPopMatrix()
        glPopMatrix()

    # Asteroid belt
    for asteroid in asteroids:
        nu = angle * asteroid["speed"] + asteroid["angle"]
        r = asteroid["a"] * (1 - asteroid["e"]**2) / (1 + asteroid["e"] * math.cos(nu))
        x, y, z = r * math.cos(nu), random.uniform(-1, 1), r * math.sin(nu)
        glPushMatrix()
        glTranslatef(x, y, z)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, planet_textures["Asteroid"])
        gluSphere(gluNewQuadric(), asteroid["size"], 5, 5)
        glDisable(GL_TEXTURE_2D)
        if asteroid["label"]:
            draw_label(x, y + asteroid["size"], z, asteroid["name"])
        glPopMatrix()

    # Space probe
    earth = planets[2]
    nu = angle * earth["speed"]
    r = earth["a"] * (1 - earth["e"]**2) / (1 + earth["e"] * math.cos(nu))
    ex, ez = r * math.cos(nu), r * math.sin(nu)
    probe["angle"] += probe["speed"]
    px = ex + probe["radius"] * math.cos(probe["angle"])
    pz = ez + probe["radius"] * math.sin(probe["angle"])
    glPushMatrix()
    glTranslatef(px, 0, pz)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, planet_textures["Probe"])
    gluSphere(gluNewQuadric(), probe["size"], 5, 5)
    glDisable(GL_TEXTURE_2D)
    if probe["label"]:
        draw_label(px, probe["size"], pz, probe["name"])
    glPopMatrix()

    draw_2d()
    if not paused:
        angle += 0.05 * time_scale
    pygame.display.flip()
    clock.tick(60)

pygame.quit()