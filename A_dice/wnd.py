import numpy as np
import quaternion
import OpenGL.GLUT as GLUT
import OpenGL.GL as GL
import camera
import shaderProgram
import dice
import physicsSolver


class Wnd:
    def __init__(self):
        GLUT.glutInit()
        GLUT.glutInitDisplayMode(
            GLUT.GLUT_DOUBLE | GLUT.GLUT_RGBA | GLUT.GLUT_DEPTH)
        GLUT.glutInitWindowSize(800, 600)
        GLUT.glutCreateWindow(b"Roll a Dice!")
        GLUT.glutDisplayFunc(self.__DisplayFunc)
        GLUT.glutKeyboardFunc(self.__KeyboardFunc)
        GL.glClearColor(0, 0, 0, 1)
        GL.glEnable(GL.GL_CULL_FACE)
        GL.glEnable(GL.GL_DEPTH_TEST)
        self.m_camera = camera.Camera()
        self.__CreateObject()
        self.__CreateShader()
        self.__Redraw(0)
        GLUT.glutMainLoop()

    def __CreateShader(self):
        self.m_diceShader = shaderProgram.CreateDiceShader()
        GL.glUniformMatrix4fv(2, 1, GL.GL_TRUE, self.m_camera.GetProjectionMatrix())
        self.m_planeShader = shaderProgram.CreatePlaneShader()
        GL.glUniformMatrix4fv(2, 1, GL.GL_TRUE, self.m_camera.GetProjectionMatrix())
        self.timer = 0

    def __CreateObject(self):
        self.dice = dice.Dice()
        self.dice.m_pos[1] = 5
        self.dice.m_pos[2] = -3
        self.dice.m_rot = quaternion.from_euler_angles((1, 1, 1))

    def __Redraw(self, t):
        GLUT.glutPostRedisplay()
        GLUT.glutTimerFunc(16, self.__Redraw, 0)

    def __DisplayFunc(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        physicsSolver.SolveDiceAndPlane(self.dice, 0.06)
        GL.glUseProgram(self.m_diceShader)
        viewMatrix = self.m_camera.GetViewMatrix()
        GL.glUniformMatrix4fv(1, 1, GL.GL_TRUE, viewMatrix)
        # Draw Dice
        self.dice.Draw()

        GL.glUseProgram(self.m_planeShader)
        GL.glUniformMatrix4fv(1, 1, GL.GL_TRUE, viewMatrix)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 6)
        GLUT.glutSwapBuffers()

    def __KeyboardFunc(self, c, x, y):
        if c == b'a':
            right = self.m_camera.GetRightward()
            self.m_camera.m_pos -= 0.1 * right
        elif c == b'd':
            right = self.m_camera.GetRightward()
            self.m_camera.m_pos += 0.1 * right
        elif c == b'w':
            forward = self.m_camera.GetForward()
            self.m_camera.m_pos += 0.1 * forward
        elif c == b's':
            forward = self.m_camera.GetForward()
            self.m_camera.m_pos -= 0.1 * forward
        elif c == b'k':
            self.m_camera.m_pitch += 0.1
        elif c == b'j':
            self.m_camera.m_pitch -= 0.1
        elif c == b'h':
            self.m_camera.m_yaw -= 0.1
        elif c == b'l':
            self.m_camera.m_yaw += 0.1
        elif c == b'e':
            self.m_camera.m_pos[1] += 0.1
        elif c == b'q':
            self.m_camera.m_pos[1] -= 0.1
        elif c == b'p':
            self.dice.m_pos[1] = 5
            self.dice.m_vel[0] = 1
