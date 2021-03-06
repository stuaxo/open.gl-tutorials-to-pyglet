# Tutorial: https://open.gl/drawing
# Original Sample Code: https://github.com/Overv/Open.GL/blob/master/content/code/c2_color_triangle.txt

import pyglet
from pyglet.gl import *
from ctypes import *
import math, time


window = pyglet.window.Window(800, 600, "OpenGL")
window.set_location(100, 100)


# Shaders (Vertex and Fragment shaders)
vertexSource = """
#version 130

in vec2 position;
in vec3 color;

out vec3 Color;

void main()
{
	Color = color;
	gl_Position = vec4(position, 0.0, 1.0);
}
"""
fragmentSource = """
#version 130

in vec3 Color;

out vec4 outColor;

void main()
{
	outColor = vec4(Color, 1.0);
}
"""


# Vertex Input
## Vertex Array Objects
vao = GLuint()
glGenVertexArrays(1, pointer(vao))
glBindVertexArray(vao)

## Vertex Buffer Object
vbo = GLuint()
glGenBuffers(1, pointer(vbo)) # Generate 1 buffer

vertices = [0.0, 0.5, 1.0, 0.0, 0.0,
			0.5, -0.5, 0.0, 1.0, 0.0,
			-0.5, -0.5, 0.0, 0.0, 1.0]
## Convert the verteces array to a GLfloat array, usable by glBufferData
vertices_ctype = (GLfloat * len(vertices))(*vertices)

## Upload data to GPU
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices_ctype), vertices_ctype, GL_STATIC_DRAW)


# Compile shaders and combining them into a program
## Create and compile the vertex shader
count = len(vertexSource)
src = (c_char_p * count)(*vertexSource)
vertexShader = glCreateShader(GL_VERTEX_SHADER)
glShaderSource(vertexShader, count, cast(pointer(src), POINTER(POINTER(c_char))), None)
glCompileShader(vertexShader)

## Create and compile the fragment shader
count = len(fragmentSource)
src = (c_char_p * count)(*fragmentSource)
fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
glShaderSource(fragmentShader, count, cast(pointer(src), POINTER(POINTER(c_char))), None)
glCompileShader(fragmentShader)

## Link the vertex and fragment shader into a shader program
shaderProgram = glCreateProgram()
glAttachShader(shaderProgram, vertexShader)
glAttachShader(shaderProgram, fragmentShader)
glBindFragDataLocation(shaderProgram, 0, "outColor")
glLinkProgram(shaderProgram)
glUseProgram(shaderProgram)


# Making the link between vertex data and attributes
posAttrib = glGetAttribLocation(shaderProgram, "position")
glEnableVertexAttribArray(posAttrib)
glVertexAttribPointer(posAttrib, 2, GL_FLOAT, GL_FALSE,
						5*sizeof(GLfloat), 0)

colAttrib = glGetAttribLocation(shaderProgram, "color")
glEnableVertexAttribArray(colAttrib)
glVertexAttribPointer(colAttrib, 3, GL_FLOAT, GL_FALSE,
                       5*sizeof(GLfloat), 2*sizeof(GLfloat))


@window.event
def on_draw():
	# Set clear color
	glClearColor(0.0, 0.0, 0.0, 1.0)
	# Clear the screen to black
	glClear(GL_COLOR_BUFFER_BIT)

	# Draw a triangle from the 3 vertices
	glDrawArrays(GL_TRIANGLES, 0, 3)

@window.event
def on_key_press(symbol, modifiers):
    pass

@window.event
def on_key_release(symbol, modifiers):
    pass

def update(dt):
	pass
pyglet.clock.schedule(update)


pyglet.app.run()
