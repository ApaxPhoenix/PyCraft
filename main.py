import pyglet
from OpenGL.GL import *
from OpenGL.GLU import *
from loader import Chunk, Block

class MainWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(caption="Minecraft", resizable=True)
        self.batch = pyglet.graphics.Batch()
        self.blocktypes = [
            Block("grass", 1, {"top": "./textures/blocks/grass.png", "bottom": "./textures/blocks/dirt.png", "sides": "./textures/blocks/grass_side.png"}),
        ]
        self.chunk = Chunk(self.blocktypes)
        glEnable(GL_DEPTH_TEST)

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65, width / height, 0.1, 1000)
        glMatrixMode(GL_MODELVIEW)
        return pyglet.event.EVENT_HANDLED

    def on_draw(self):
        self.clear()
        glPushMatrix()
        glTranslatef(0, 0, -50)
        glRotatef(-30, 1, 0, 0)
        glRotatef(45, 0, 1, 0)
        self.chunk.render()
        glPopMatrix()

    def on_close(self):
        pyglet.app.exit()

if __name__ == '__main__':
    window = MainWindow()
    pyglet.app.run()
