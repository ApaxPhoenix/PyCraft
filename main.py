import sys, os
import importlib.util
import subprocess

# List of required module names
module_names = ['OpenGL', 'PyInstaller']

# Loop over the list of module names
for name in ['OpenGL', 'PyInstaller']:
    if name in sys.modules:
        # If the module is already in sys.modules, print a message
        print(f"{name!r} already in sys.modules")
    elif (spec := importlib.util.find_spec(name)) is not None:
        # If the module can be found, import it
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        print(f"{name!r} has been found and imported")
    else:
        # If the module cannot be found, try to install it using pip
        print(f"{name!r} not found, attempting to install with pip")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", name])
            print(f"{name!r} has been installed")
        except subprocess.CalledProcessError:
            print(f"Failed to install {name!r}")

# Prompt the user whether they want to compile or interpret the main file
prompt = input("Do you want to compile or interpret the main file?\n"
               "Enter 'c' for compile or 'i' for interpret: ")

# Check the user's choice and inform them that performance might be affected
if prompt.lower() == 'c':
    print("You have chosen to compile the main file.")
    # Import and declare PyInstallerWrapper
    from installer import PyinstallerWrapper
    PyinstallerWrapper(os.path.dirname(os.path.abspath(__file__))).build()
elif prompt.lower() == 'i':
    print("You have chosen to interpret the main file. "
          "Note that this may affect performance during the compilation process.")
    # Create a variable that will initialize a instance of OpenGLWindow
    runOpenGlWindow = True
else:
    print("Invalid choice. Please enter 'c' for compile or 'i' for interpret.")











































import pygame
from loader import Block
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_PROJECTION,
    GL_MODELVIEW,
    GL_SMOOTH,
    GL_LESS,

    glEnable,
    glClear,
    glClearColor,
    glClearDepth,
    glDepthFunc,
    glShadeModel,
    glMatrixMode,
)

from OpenGL.GLU import (
    gluPerspective
)

class OpenGLWindow:
    def __init__(self, window_size):
        # Import necessary libraries
        pygame.init()

        # Set window size and initialize display settings
        self.window_size = window_size
        self.display = pygame.display.set_mode(self.window_size, pygame.DOUBLEBUF | pygame.OPENGL)

        # Initialize block instance
        self.block = Block(
            name="grass_block",
            block_id=0,
            textures={
                "top": "./textures/blocks/grass.png",
                "bottom": "./textures/blocks/dirt.png",
                "sides": "./textures/blocks/grass_side.png"
            })

        # OpenGL settings
        #glClearColor(0.529, 0.808, 0.922, 1.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45.0, float(self.window_size[0]) / float(self.window_size[1]), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # Clear screen and draw block
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.block.rotation = [(self.block.rotation[i] + 1.25) for i in range(3)]
            self.block.draw()

            # Update display and wait
            pygame.display.flip()
            pygame.time.wait(10)

if runOpenGlWindow == True:
    # Create instance of OpenGLWindow and start
    OpenGLWindow(window_size=(800, 600)).start()