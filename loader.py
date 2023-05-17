import pyglet
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import os

class LoadTexture:
    def __init__(self, textures):
        if not isinstance(textures, dict):
            raise ValueError("Textures must be a dictionary")
        for value in textures.values():
            if not isinstance(value, str):
                raise ValueError("All texture file paths must be strings")
        self.textures = textures

    def load_texture(self, filepath):
        textureSurface = pyglet.image.load(filepath)
        textureData = textureSurface.get_image_data().get_data('RGBA', textureSurface.width * 4)
        width, height = textureSurface.width, textureSurface.height
        texture = GLuint(0)
        glGenTextures(1, ctypes.byref(texture))
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
        return texture

    def test_texture_files(self):
        texture_ids = {}
        for texture_name, texture_path in self.textures.items():
            if not isinstance(texture_path, str):
                raise ValueError(f"Invalid texture file path for {texture_name}: {texture_path}")
            if not os.path.isfile(texture_path):
                raise ValueError(f"Invalid texture file path for {texture_name}: {texture_path}")
            texture_file, texture_ext = os.path.splitext(texture_path)
            if texture_ext.lower() not in ['.png', '.jpg', '.jpeg']:
                raise ValueError(f"Invalid texture file type for {texture_name}: {texture_ext}")
            texture_ids[texture_name] = self.load_texture(texture_path)
        return texture_ids

class Block(LoadTexture):
    def __init__(self, name, block_id, textures, position=(0, 0, 0), rotation=[0, 0, 0]):
        if not isinstance(position, tuple) or len(position) != 3:
            raise ValueError("Invalid position tuple: {}".format(position))
        if not isinstance(textures, dict) or not textures:
            raise ValueError("Invalid textures dictionary: {}".format(textures))
        if not isinstance(rotation, list) or len(rotation) != 3:
            raise ValueError("Invalid rotation list: {}".format(rotation))
        super().__init__(textures)
        self.texture_ids = self.test_texture_files()
        self.position = position
        self.rotation = rotation

    def render(self):
        x, y, z = self.position
        rx, ry, rz = self.rotation

        glDisable(GL_CULL_FACE)
        glPushMatrix()
        glTranslatef(x + 0.5, y + 0.5, z + 0.5)
        glRotatef(rx, 1, 0, 0)
        glRotatef(ry, 0, 1, 0)
        glRotatef(rz, 0, 0, 1)
        glTranslatef(-0.5, -0.5, -0.5)
        glEnable(GL_TEXTURE_2D)

        glBindTexture(GL_TEXTURE_2D, self.texture_ids["top"])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(0, 1, 0)
        glTexCoord2f(1, 0)
        glVertex3f(1, 1, 0)
        glTexCoord2f(1, 1)
        glVertex3f(1, 1, 1)
        glTexCoord2f(0, 1)
        glVertex3f(0, 1, 1)
        glEnd()

        glBindTexture(GL_TEXTURE_2D, self.texture_ids["bottom"])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(0, 0, 0)
        glTexCoord2f(1, 0)
        glVertex3f(1, 0, 0)
        glTexCoord2f(1, 1)
        glVertex3f(1, 0, 1)
        glTexCoord2f(0, 1)
        glVertex3f(0, 0, 1)
        glEnd()

        glBindTexture(GL_TEXTURE_2D, self.texture_ids["sides"])
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(0, 0, 1)
        glTexCoord2f(0, 1)
        glVertex3f(0, 1, 1)
        glTexCoord2f(1, 1)
        glVertex3f(1, 1, 1)
        glTexCoord2f(1, 0)
        glVertex3f(1, 0, 1)
        glEnd()

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(1, 0, 1)
        glTexCoord2f(0, 1)
        glVertex3f(1, 1, 1)
        glTexCoord2f(1, 1)
        glVertex3f(1, 1, 0)
        glTexCoord2f(1, 0)
        glVertex3f(1, 0, 0)
        glEnd()

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(1, 0, 0)
        glTexCoord2f(0, 1)
        glVertex3f(1, 1, 0)
        glTexCoord2f(1, 1)
        glVertex3f(0, 1, 0)
        glTexCoord2f(1, 0)
        glVertex3f(0, 0, 0)
        glEnd()

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(0, 0, 0)
        glTexCoord2f(0, 1)
        glVertex3f(0, 1, 0)
        glTexCoord2f(1, 1)
        glVertex3f(0, 1, 1)
        glTexCoord2f(1, 0)
        glVertex3f(0, 0, 1)
        glEnd()

        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

class Chunk(Block):
    def __init__(self, blocktypes, geometry=(16,16,16)):
        if not isinstance(blocktypes, list):
            raise TypeError("Blocktypes attribute must be a list")
        if not all(isinstance(block, Block) for block in blocktypes):
            raise TypeError("all elements in blocktypes list must be Block objects")
        if not isinstance(geometry, tuple):
            raise TypeError("Geometry attribute must be a tuple")
        if not all(isinstance(number, int) for number in geometry):
            raise TypeError("all elements in geometry list must be integers")
        self.geometry = geometry
        self.blocktypes = blocktypes

class Biome(Chunk):
    def __init__(self, name, type, chunks):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not isinstance(type, str):
            raise TypeError("type must be a string")
        if not isinstance(chunks, list):
            raise TypeError("chunks must be a list")
        self.name = name
        self.type = type
        self.chunks = chunks








































"""
    def render(self):
        chunk_width, chunk_height, chunk_depth = self.geometry
        chunk_dimensions = {
            "depth": divmod(chunk_depth, len(self.blocktypes))[0],
            "height": divmod(chunk_height, len(self.blocktypes))[0],
            "width": divmod(chunk_width, len(self.blocktypes))[0],
        }

        for _, block in enumerate(self.blocktypes):
            for x in range(chunk_dimensions["width"]):
                for y in range(chunk_dimensions["height"]):
                    for z in range(chunk_dimensions["depth"]):
                        concurrent_position = (x, y, z)
                        block.position = concurrent_position
                        block.render()
"""