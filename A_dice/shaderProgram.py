import OpenGL.GL as GL
import matplotlib.pyplot as plt


def LoadDiceTexture():
    img = plt.imread("dice.png")
    tex = GL.glGenTextures(1)
    GL.glActiveTexture(GL.GL_TEXTURE0)
    GL.glBindTexture(GL.GL_TEXTURE_2D, tex)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA8,len(img[0]),len(img),0,GL.GL_RGBA, GL.GL_FLOAT,img)
    GL.glBindTexture(GL.GL_TEXTURE_2D, tex)
    GL.glUniform1i(3, 0)


def CreateShader(vertShaderSrc, fragShaderSrc):
    programId = GL.glCreateProgram()
    vertShader = GL.glCreateShader(GL.GL_VERTEX_SHADER)
    GL.glShaderSource(vertShader, vertShaderSrc)
    GL.glCompileShader(vertShader)
    s = 0
    GL.glGetShaderiv(vertShader, GL.GL_COMPILE_STATUS, s)
    if s == GL.GL_FALSE:
        log = ""
        log = GL.glGetShaderInfoLog(vertShader)
        print(str(log))
    GL.glAttachShader(programId, vertShader)
    fragShader = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
    GL.glShaderSource(fragShader, fragShaderSrc)
    GL.glCompileShader(fragShader)
    GL.glGetShaderiv(fragShader, GL.GL_COMPILE_STATUS, s)
    if s == GL.GL_FALSE:
        log = ""
        log = GL.glGetShaderInfoLog(vertShader)
        print(str(log))
    GL.glAttachShader(programId, fragShader)
    GL.glLinkProgram(programId)
    GL.glUseProgram(programId)
    return programId

def CreateDiceShader():
    vertShaderSrc = """
    #version 450 core
    layout(location=0) uniform mat4 modelTransform;
    layout(location=1) uniform mat4 viewTransform;
    layout(location=2) uniform mat4 projTransform;
    out vec2 fragTexCoord;
    void main(){
        vec3 p[] = { vec3(-0.5, -0.5, -0.5), vec3( 0.5, -0.5, -0.5), vec3( 0.5,  0.5, -0.5), vec3(-0.5,  0.5, -0.5), vec3(-0.5, -0.5,  0.5), vec3( 0.5, -0.5,  0.5), vec3( 0.5,  0.5,  0.5), vec3(-0.5,  0.5,  0.5), };
        vec2 texp[]={ vec2(0, 0), vec2(0.25, 0), vec2(0,    1.0f/3.0f), vec2(0.25, 1.0f/3.0f), vec2(0.5f, 1.0f/3.0f), vec2(0.75, 1.0f/3.0f), vec2(1,    1.0f/3.0f), vec2(0,    2.0f/3.0f), vec2(0.25, 2.0f/3.0f), vec2(0.5f, 2.0f/3.0f), vec2(0.75, 2.0f/3.0f), vec2(1,    2.0f/3.0f), vec2(0, 1), vec2(0.25, 1), };

        int index[]={ 1,0,2, 2,0,3, 6,4,5, 7,4,6, 3,0,4, 3,4,7, 5,1,2, 6,5,2, 5,0,1, 4,0,5, 2,3,6, 6,3,7, };
        int texindex[]={ 3,2,8, 8,2,7, 9,5,4, 10,5,9, 11,6,5, 11,5,10, 4,3,8, 9,4,8, 1,2,3, 0,2,1, 8,7,13, 13,7,12 };
        vec3 normal[]={ vec3(0,0,-1), vec3(0,0,1), vec3(-1,0,0), vec3(1,0,0), vec3(0,-1,0), vec3(0,1,0), };
        gl_Position = projTransform * viewTransform * modelTransform *
            vec4(p[index[gl_VertexID]], 1);
        fragTexCoord = texp[texindex[gl_VertexID]];
    }
    """
    fragShaderSrc = """
    #version 450 core
    layout(location=3) uniform sampler2D texSampler;
    out vec3 color;
    in vec2 fragTexCoord;
    void main(){
        color = texture(texSampler, fragTexCoord).xyz;
    }
    """
    pid = CreateShader(vertShaderSrc, fragShaderSrc)
    LoadDiceTexture()
    return pid


def CreatePlaneShader():
    vertShaderSrc = """
    #version 450 core
    layout(location=1) uniform mat4 viewTransform;
    layout(location=2) uniform mat4 projTransform;
    void main(){
        vec3 p[]={
            vec3(-50, 0, -50), vec3(50, 0, 50), vec3(50, 0, -50),
            vec3(-50, 0, -50), vec3(-50, 0, 50), vec3(50, 0, 50)
        };
        gl_Position = projTransform * viewTransform * vec4(p[gl_VertexID], 1);
    }
    """
    fragShaderSrc = """
    #version 450 core
    out vec3 color;
    void main(){
        color = vec3(0.3,0.3,0.3);
    }
    """
    pid = CreateShader(vertShaderSrc, fragShaderSrc)
    return pid
