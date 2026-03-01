# 🌌 SolarSyst --- Interactive Solar System Simulation

**Cloud‑ready landing page + native 3D desktop simulation** --- a
real‑time, OpenGL‑powered solar system visualizer with planetary orbits,
asteroid belt, and a simulated probe.

**Download / Demo:**
https://drive.google.com/uc?export=download&id=1rhrAQ7DtaeHm0wjmyfrWu5Ne8H8QRE6Z

------------------------------------------------------------------------

## 🎯 Elevator pitch

An immersive educational 3D solar system simulation built with PyGame +
PyOpenGL and distributed via a Streamlit landing page --- perfect for
demos, classrooms, and portfolio showcases.

------------------------------------------------------------------------

## ✨ Highlights

-   Interactive camera + zoom + time scaling
-   Realistic orbital visualization (scaled)
-   Starfield, nebulae, galaxies, asteroid belt
-   Streamlit landing page for easy distribution

------------------------------------------------------------------------

## 🧭 Features

-   Planetary bodies: Mercury → Neptune
-   Earth moon + orbiting probe
-   Asteroid belt
-   On‑screen HUD (planet info, controls)
-   Keyboard & mouse interaction

------------------------------------------------------------------------

## 🔧 Repo Contents

-   `solar_system.py` --- Pygame + PyOpenGL simulation\
-   `landing.py` --- Streamlit landing page that links to downloads\
-   `requirements.txt` --- project dependencies

------------------------------------------------------------------------

## 🚀 Install & Run

``` bash
python -m venv venv
# activate venv
pip install -r requirements.txt
# run landing page (optional)
streamlit run landing.py
# run simulation (desktop)
python solar_system.py
```

**Requirements (example `requirements.txt`):**

    pygame>=2.1.0
    PyOpenGL>=3.1.6
    numpy>=1.21.0
    streamlit>=1.0

------------------------------------------------------------------------

## 📦 Packaging (Windows example)

``` bash
pip install pyinstaller
pyinstaller --onefile --windowed solar_system.py
# distribute dist/solar_system.exe
```

------------------------------------------------------------------------

## 🖼 Preview

![App Screenshot](./assets/screenshot.png)

------------------------------------------------------------------------

## 🧠 Design notes

Single-file simulation: planet data stored in dicts, rendering using
standard OpenGL sphere primitives, HUD drawn with Pygame fonts and
`glDrawPixels`. Time advanced via an `angle` state variable; adjustable
`time_scale`.

------------------------------------------------------------------------

## ⚠️ Troubleshooting

-   Ensure system has OpenGL drivers.
-   Install `PyOpenGL_accelerate` for better performance on Windows.
-   If rendering fails, update `pygame` and `PyOpenGL`.

------------------------------------------------------------------------

## 🤝 Contributing

PRs welcome: add textures, package installers, more physics realism, or
platform builds.

------------------------------------------------------------------------

## 📜 License

MIT (recommended)
