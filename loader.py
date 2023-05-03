import pygame, os
from OpenGL.GL import (
    GL_QUADS,
    GL_TEXTURE_2D,
    GL_CULL_FACE,
    GL_RGBA,
    GL_NEAREST,
    GL_TEXTURE_MIN_FILTER,
    GL_TEXTURE_MAG_FILTER,
    GL_UNSIGNED_BYTE,

    glBindTexture,
    glTexParameterf,
    glGenTextures,
    glTexImage2D,

    glBegin,
    glEnd,
    glEnable,
    glDisable,
    glPushMatrix,
    glPopMatrix,
    glTranslatef,
    glRotatef,
    glTexCoord2f,
    glVertex3f,
)

class LoadTexture:
    def __init__(self, textures):
        # Constructor that takes a dictionary of textures as input
        self.textures = textures
        # Check if the required keys are present in the textures dictionary
        if not all(key in textures for key in ["top", "bottom", "sides"]):
            print("textures is missing one or more of the keys 'top', 'bottom', or 'sides'")

    def load_texture(self, filepath):
        # Method that loads a texture from a given filepath and returns its id
        textureSurface = pygame.image.load(filepath)
        textureData = pygame.image.tostring(textureSurface, "RGBA", True)
        width, height = textureSurface.get_size()
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
        return texture

    def test_texture_files(self):
        # Method that tests if the texture files exist and are of the correct format
        texture_ids = {}
        for texture_name, texture_path in self.textures.items():
            # Check if the texture_path is a string
            if not isinstance(texture_path, str):
                raise ValueError(f"Invalid texture file path for {texture_name}: {texture_path}")
            # Check if the texture file exists
            if not os.path.isfile(texture_path):
                raise ValueError(f"Invalid texture file path for {texture_name}: {texture_path}")
            # Check if the texture file is a .png, .jpg, or .jpeg
            texture_file, texture_ext = os.path.splitext(texture_path)
            if texture_ext.lower() not in ['.png', '.jpg', '.jpeg']:
                raise ValueError(f"Invalid texture file type for {texture_name}: {texture_ext}")
            # Load the texture and add its id to the dictionary
            texture_ids[texture_name] = self.load_texture(texture_path)
        # Return the dictionary containing the texture ids
        return texture_ids

class Block(LoadTexture):
    def __init__(self, name, block_id, textures, position=(-0.45, 0, -5), rotation=[0, 0, 0]):
        # Check if position is a tuple with three elements
        if not isinstance(position, tuple) or len(position) != 3:
            raise ValueError("Invalid position tuple: {}".format(position))
        # Check if textures is a dictionary with at least one key-value pair
        if not isinstance(textures, dict) or not textures:
            raise ValueError("Invalid textures dictionary: {}".format(textures))
        # Check if rotation is a list with three elements
        if not isinstance(rotation, list) or len(rotation) != 3:
            raise ValueError("Invalid rotation list: {}".format(rotation))

        # Call the constructor of the parent class
        super().__init__(textures)

        # Load the texture files and store their IDs in a dictionary
        self.texture_ids = self.test_texture_files()

        # Set the position and rotation attributes
        self.position = position
        self.rotation = rotation

    def draw(self):
        # Defines the position and rotation of the mesh
        x, y, z = self.position
        rx, ry, rz = self.rotation

        # Disable backface culling to draw all faces of the block
        glDisable(GL_CULL_FACE)

        # Push the current matrix onto the stack
        glPushMatrix()

        # Translate to the Block's position
        glTranslatef(x + 0.5, y + 0.5, z + 0.5)

        # Rotate around the X, Y, and Z axes
        glRotatef(rx, 1, 0, 0)
        glRotatef(ry, 0, 1, 0)
        glRotatef(rz, 0, 0, 1)

        # Translate to the center of the block
        glTranslatef(-0.5, -0.5, -0.5)

        # Enable texturing
        glEnable(GL_TEXTURE_2D)

        # Draw the top face of the block
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

        # Draw the bottom face of the block
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

        # Draw the sides of the block
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

        # Disable texturing
        glDisable(GL_TEXTURE_2D)

        # Pull the current matrix onto memory
        glPopMatrix()

########## FIX THIS CLASS
class Chunk:
    def __init__(self, blocks):
        if not isinstance(blocks, list):
            raise ValueError("blocks must be a list")
        if not all(isinstance(block, Block) for block in blocks):
            raise ValueError("blocks must contain instances of the Block class only")
        self.blocks = blocks

    def add_block(self, block):
        x, y, z = block.position
        for b in self.blocks:
            bx, by, bz = b.position
            if bx == x and by == y and bz == z:
                self.blocks.remove(b)
                break
        self.blocks.append(block)

    def draw(self):
        for block in self.blocks:
            # Draw the block as a cube using OpenGL
            glBegin(GL_QUADS)
            for face in block.faces:
                for vertex in face:
                    glVertex3f(*vertex)
            glEnd()


