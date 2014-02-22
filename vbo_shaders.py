#!/usr/bin/env python
""" This is a Python implementation of the C++ version
"""
import sys
import sdl2 as sdl
import sdl2.ext as sdlx
import OpenGL.GL as gl
import numpy as np
# Serious OpenGL stuff
import OpenGL.GL as gl
from OpenGL.arrays import vbo
from OpenGL.GL import shaders
#-------------------------------------------------------------------------------
WND_SIZE = (800, 600)
WND_FLAGS = sdl.SDL_WINDOW_OPENGL | sdl.SDL_WINDOW_SHOWN
#-------------------------------------------------------------------------------
# Check if 330 is supported on this machine
VERTEX_SHADER = """#version 130
void main(){
  gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}
"""
FRAGMENT_SHADER = """#version 130
void main(){
  gl_FragColor = vec4(0,0,1,0.7);
}
"""
#-------------------------------------------------------------------------------
# A very simple opengl app
#-------------------------------------------------------------------------------
class Game(object):
    def __init__(self):
        self.window = None
        self.glcontext = None
        self.running = True
        self.vertices = np.array([
            [ 0, 1, 0 ], [ -1,-1, 0 ], [ 1,-1, 0 ],
            [ 2,-1, 0 ], [ 4,-1, 0 ], [ 4, 1, 0 ], [ 2,-1, 0 ], [ 4, 1, 0 ],
            [ 2, 1, 0 ]
        ],'f')

    def init_gl(self):
        gl.glClearColor(0,0,0,0)
        gl.glClearDepth(1.0)
        gl.glViewport(0,0,WND_SIZE[0], WND_SIZE[1])
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glLoadIdentity()
        # Compile and link shaders
        vertex_shader = shaders.compileShader(VERTEX_SHADER,
                                              gl.GL_VERTEX_SHADER)
        fragment_shader = shaders.compileShader(FRAGMENT_SHADER,
                                                gl.GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(vertex_shader, fragment_shader)
        # Send data to server
        self.vbo1 = vbo.VBO(self.vertices)

    def initialize(self):
        """ Direct translation of the C++ code
        """
        if sdl.SDL_Init(sdl.SDL_INIT_EVERYTHING) < 0:
            return False

        sdl.SDL_GL_SetAttribute(sdl.SDL_GL_DOUBLEBUFFER, 1)
        self.window = sdl.SDL_CreateWindow('PySDL2 OpenGL',
                                           sdl.SDL_WINDOWPOS_CENTERED,
                                           sdl.SDL_WINDOWPOS_CENTERED,
                                           WND_SIZE[0], WND_SIZE[1],
                                           WND_FLAGS
        )
        if not self.window: return False
        self.glcontect = sdl.SDL_GL_CreateContext(self.window)
        # Open GL
        self.init_gl()
        return True

    def start(self):
        if not self.initialize():
            sys.exit(-1)
        while self.running:
            events = sdlx.get_events()
            for event in events:
                self.process_event(event)
            self.render()
        self.cleanup()
        sys.exit(0)

    def render(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()
        # Draw stuff here
        shaders.glUseProgram(self.shader)
        try:
            self.vbo1.bind()
            try:
                gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
                gl.glVertexPointerf(self.vbo1)
                gl.glDrawArrays(gl.GL_TRIANGLES, 0, 9)
            finally:
                self.vbo1.unbind()
                gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        finally:
            shaders.glUseProgram(0)

        # Double buffering
        sdl.SDL_GL_SwapWindow(self.window)

    def cleanup(self):
        sdl.SDL_GL_DeleteContext(self.glcontext)
        sdl.SDL_DestroyWindow(self.window)
        sdl.SDL_Quit()

    def process_event(self, event):
        if event.type == sdl.SDL_KEYDOWN:
            self.key_down(event.key.keysym)
        if event.type == sdl.SDL_QUIT:
            self.exit_()

    def exit_(self):
        self.running = False

    def key_down(self, keysym):
        if keysym.sym == sdl.SDLK_q:
            self.exit_()

if __name__ == '__main__':
    game = Game()
    game.start()
