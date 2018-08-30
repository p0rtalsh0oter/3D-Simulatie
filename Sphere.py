# author: Somsubhra Bairi (201101056)

# Draw sphere with QUAD_STRIP
# Controls: UP/DOWN - scale up/down
#           LEFT/RIGHT - rotate left/right
#           F1 - Toggle surface as SMOOTH or FLAT
#           F11 - Toggle fullscreen

# Python imports
from math import *
import glfw

# OpenGL imports for python
try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
except:
    print("OpenGL wrapper for python not found")

# Define constants
TITLE = "Sphere"

# Define variables
w_width = 700
w_height = int(w_width / 16 * 9)
up = False
down = False
left = False
right = False


# Last time when sphere was re-displayed
last_time = 0

# The window resize callback function.
# This will be called by glfw whenever the width or height is altered
def window_resize(window, width, height):
    glViewport(0,0, width, height)

# The key callback function. This will be called by glfw whenever something
# happens with a key
def key_callback(window, key, scancode, action, mode):
    global up
    global down
    global left
    global right
    # Check if a key is held down.
    if action == glfw.PRESS:
        if key == glfw.KEY_UP:
            up = True
    # Check if a key is released.
    if action == glfw.RELEASE:
        if key == glfw.KEY_UP:
            up = False
    # I'm not sure about this one.
    if action == glfw.REPEAT:
        pass
        
        
        

    
# The sphere class
class Sphere:

    # Constructor for the sphere class
    def __init__(self, radius):

        # Radius of sphere
        self.radius = radius

        # Number of latitudes in sphere
        self.lats = 100

        # Number of longitudes in sphere
        self.longs = 100

        self.user_theta = 0
        self.user_height = 0

        # Direction of light
        self.direction = [0.0, 2.0, -1.0, 1.0]

        # Intensity of light
        self.intensity = [0.7, 0.7, 0.7, 1.0]

        # Intensity of ambient light
        self.ambient_intensity = [0.3, 0.3, 0.3, 1.0]

        # The surface type(Flat or Smooth)
        self.surface = GL_FLAT

        self.full_screen = False

    # Initialize
    def init(self):

        # Set background color to black
        glClearColor(0.0, 0.0, 0.0, 0.0)

        self.compute_location()

        # Set OpenGL parameters
        glEnable(GL_DEPTH_TEST)

        # Enable lighting
        glEnable(GL_LIGHTING)

        # Set light model
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, self.ambient_intensity)

        # Enable light number 0
        glEnable(GL_LIGHT0)

        # Set position and intensity of light
        glLightfv(GL_LIGHT0, GL_POSITION, self.direction)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.intensity)

        # Setup the material
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    # Compute location
    def compute_location(self):
        x = 2 * cos(self.user_theta)
        y = 2 * sin(self.user_theta)
        z = self.user_height
        d = sqrt(x * x + y * y + z * z)

        # Set matrix mode
        glMatrixMode(GL_PROJECTION)

        # Reset matrix
        glLoadIdentity()
        glFrustum(-d * 0.5, d * 0.5, -d * 0.5, d * 0.5, d - 1.1, d + 1.1)


        # Set camera
        gluLookAt(x, y, z, 0, 0, 0, 0, 0, 1)

    # Display the sphere
    def display(self):
        

        # Set shade model
        glShadeModel(self.surface)

        self.draw()

    # Update the sphere
    def update(self):
        global up
        global down
        global left
        global right
        if up:
            self.user_height += 0.1
        if down:
            self.user_height -= 0.1
        if left:
            self.user_theta += 0.1
        if right:
            self.user_theta -= 0.1
            
        

    # Draw the sphere
    def draw(self):
        for i in range(0, self.lats + 1):
            lat0 = pi * (-0.5 + float(float(i - 1) / float(self.lats)))
            z0 = sin(lat0)
            zr0 = cos(lat0)

            lat1 = pi * (-0.5 + float(float(i) / float(self.lats)))
            z1 = sin(lat1)
            zr1 = cos(lat1)

            # Use Quad strips to draw the sphere
            glBegin(GL_QUAD_STRIP)

            for j in range(0, self.longs + 1):
                lng = 2 * pi * float(float(j - 1) / float(self.longs))
                x = cos(lng)
                y = sin(lng)
                glNormal3f(x * zr0, y * zr0, z0)
                glVertex3f(x * zr0, y * zr0, z0)
                glNormal3f(x * zr1, y * zr1, z1)
                glVertex3f(x * zr1, y * zr1, z1)

            glEnd()

    # Keyboard controller for sphere
##    def special(self, key, x, y):
##
##        # Scale the sphere up or down
##        if key == GLUT_KEY_UP:
##            self.user_height += 0.1
##        if key == GLUT_KEY_DOWN:
##            self.user_height -= 0.1
##
##        # Rotate the cube
##        if key == GLUT_KEY_LEFT:
##            self.user_theta += 0.1
##        if key == GLUT_KEY_RIGHT:
##            self.user_theta -= 0.1
##
##        # Toggle the surface
##        if key == GLUT_KEY_F1:
##            if self.surface == GL_FLAT:
##                self.surface = GL_SMOOTH
##            else:
##                self.surface = GL_FLAT
##        if key == GLUT_KEY_F11:
##            if not self.full_screen:
##                glutFullScreen()
##                self.full_screen = True
##            else:
##                glutReshapeWindow(w_width, w_height)
##                glutPositionWindow(50, 100)
##                self.full_screen = False
            

##        self.compute_location()
##        glutPostRedisplay()

    # The idle callback
##    def idle(self):
##        global last_time
##        time = glutGet(GLUT_ELAPSED_TIME)
##
##        if last_time == 0 or time >= last_time + 40:
##            last_time = time
##            glutPostRedisplay()

    # The visibility callback
##    def visible(self, vis):
##        if vis == GLUT_VISIBLE:
##            glutIdleFunc(self.idle)
##        else:
##            glutIdleFunc(None)


# The main function
def main():
    
    # Initialize the OpenGL pipeline
    #glutInit(sys.argv)

    # Set OpenGL display mode
    #glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)

    # Set the Window size and position
    #glutInitWindowSize(w_width, w_height)
    #glutInitWindowPosition(50, 100)

    # Create the window with given width, height and title
    if not glfw.init():
        return

    window = glfw.create_window(w_width, w_height, TITLE, None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, window_resize)
    glfw.set_key_callback(window, key_callback)
    
    #glfw.set_window_aspect_ratio(window, 16, 9)
    # Instantiate the sphere object
    s = Sphere(1.0)

    s.init()

    # Set the callback function for display
    #glutDisplayFunc(s.display)

    # Set the callback function for the visibility
    #glutVisibilityFunc(s.visible)

    # Set the callback for special function
    #glutSpecialFunc(s.special)

    # Run the OpenGL main loop
    #glutMainLoop()

    #Main loop
    while not glfw.window_should_close(window):
        #Update
        glfw.poll_events()
        s.update()

        #Render
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(1.0, 1.0, 1.0)
        s.display()
        #Swaps the front and back buffer
        glfw.swap_buffers(window)

    glfw.terminate()


# Call the main function
if __name__ == '__main__':
    main()
