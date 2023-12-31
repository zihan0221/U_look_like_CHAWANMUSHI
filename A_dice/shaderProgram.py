import OpenGL.GL as GL
import matplotlib.pyplot as plt
import numpy as np


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

def LoadAlphabatTexture():
    img = plt.imread("ascii.png")
    tex = GL.glGenTextures(1)
    GL.glActiveTexture(GL.GL_TEXTURE1)
    GL.glBindTexture(GL.GL_TEXTURE_2D, tex)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA8,len(img[0]),len(img),0,GL.GL_RGBA, GL.GL_FLOAT,img)
    GL.glUniform1i(0, 1)

def LoadSkyboxTexture():
    img = plt.imread("sky.png")
    tex = GL.glGenTextures(1)
    GL.glActiveTexture(GL.GL_TEXTURE2)
    GL.glBindTexture(GL.GL_TEXTURE_2D, tex)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA8,len(img[0]),len(img),0,GL.GL_RGBA, GL.GL_FLOAT,img)
    GL.glUniform1i(0, 2)

def LoadACTexture():
    img = plt.imread("ac.png")
    tex = GL.glGenTextures(1)
    GL.glActiveTexture(GL.GL_TEXTURE3)
    GL.glBindTexture(GL.GL_TEXTURE_2D, tex)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA8,len(img[0]),len(img),0,GL.GL_RGBA, GL.GL_FLOAT,img)
    GL.glUniform1i(0, 3)

def LoadWATexture():
    img = plt.imread("wa.png")
    tex = GL.glGenTextures(1)
    GL.glActiveTexture(GL.GL_TEXTURE4)
    GL.glBindTexture(GL.GL_TEXTURE_2D, tex)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA8,len(img[0]),len(img),0,GL.GL_RGBA, GL.GL_FLOAT,img)
    GL.glUniform1i(0, 4)

def CreateShader(vertShaderSrc, fragShaderSrc, geomShaderSrc=None):
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
        log = GL.glGetShaderInfoLog(fragShader)
        print(str(log))
    GL.glAttachShader(programId, fragShader)

    if geomShaderSrc:
        geomShader = GL.glCreateShader(GL.GL_GEOMETRY_SHADER)
        GL.glShaderSource(geomShader, geomShaderSrc)
        GL.glCompileShader(geomShader)
        GL.glGetShaderiv(geomShader, GL.GL_COMPILE_STATUS, s)
        if s == GL.GL_FALSE:
            log = ""
            log = GL.glGetShaderInfoLog(geomShader)
            print(str(log))
        GL.glAttachShader(programId, geomShader)

    GL.glLinkProgram(programId)
    GL.glUseProgram(programId)
    return programId


lights = np.array(((-6, 10, -6), (6, 10, -6), (-6, 10, 6), (6, 10, 6)))
LIGHT_CONFIG = "#define LIGHT_NUM " + str(len(lights)) +\
    "\nvec3 lightPos[LIGHT_NUM] = {" + "".join([f"vec3({x[0]},{x[1]},{x[2]})," for x in lights]) +\
    "};vec3 lightColor = vec3(1,1,1); const float lightStr = 400;layout(location=5) uniform samplerCube shadowSampler[LIGHT_NUM];"



def CreateDiceShader():
    vertShaderSrc = """
    #version 450 core
    layout(location=0) uniform mat4 modelTransform;
    layout(location=1) uniform mat4 viewTransform;
    layout(location=2) uniform mat4 projTransform;
    out vec2 fragTexCoord;
    out vec3 fragPos;
    out vec3 fragNorm;
    void main(){
        vec3 p[] = { vec3(-0.5, -0.5, -0.5), vec3( 0.5, -0.5, -0.5), vec3( 0.5,  0.5, -0.5), vec3(-0.5,  0.5, -0.5), vec3(-0.5, -0.5,  0.5), vec3( 0.5, -0.5,  0.5), vec3( 0.5,  0.5,  0.5), vec3(-0.5,  0.5,  0.5), };
        vec2 texp[]={ vec2(0, 0), vec2(0.25, 0), vec2(0,    1.0f/3.0f), vec2(0.25, 1.0f/3.0f), vec2(0.5f, 1.0f/3.0f), vec2(0.75, 1.0f/3.0f), vec2(1,    1.0f/3.0f), vec2(0,    2.0f/3.0f), vec2(0.25, 2.0f/3.0f), vec2(0.5f, 2.0f/3.0f), vec2(0.75, 2.0f/3.0f), vec2(1,    2.0f/3.0f), vec2(0, 1), vec2(0.25, 1), };

        int index[]={ 1,0,2, 2,0,3, 6,4,5, 7,4,6, 3,0,4, 3,4,7, 5,1,2, 6,5,2, 5,0,1, 4,0,5, 2,3,6, 6,3,7, };
        int texindex[]={ 3,2,8, 8,2,7, 9,5,4, 10,5,9, 11,6,5, 11,5,10, 4,3,8, 9,4,8, 1,2,3, 0,2,1, 8,7,13, 13,7,12 };
        vec3 normal[]={ vec3(0,0,-1), vec3(0,0,1), vec3(-1,0,0), vec3(1,0,0), vec3(0,-1,0), vec3(0,1,0), };
        vec4 modelPos = modelTransform * vec4(p[index[gl_VertexID]], 1);
        fragNorm = (modelTransform * vec4(normal[gl_VertexID/6], 0)).xyz;
        fragPos = modelPos.xyz;
        gl_Position = projTransform * viewTransform * modelPos;
        fragTexCoord = texp[texindex[gl_VertexID]];
    }
    """
    fragShaderSrc = """
    #version 450 core
    #define M_PI 3.1415926535897932384626433832795
    layout(location=3) uniform sampler2D texSampler;
    layout(location=4) uniform vec3 camPos;
    """ + LIGHT_CONFIG + """
    in vec3 fragPos;
    in vec3 fragNorm;
    out vec4 color;
    in vec2 fragTexCoord;

    float FresnelTerm(in vec3 N, in vec3 L) {
        const float n1 = 1;
        const float n2 = 1.5;
        const float inCos = max(dot(L, N), 0.0f);
        float n2n1 = n2 / n1;
        const float d = inCos * inCos - 1 + n2n1 * n2n1;
        if (d > 1e-5) {
            const float outCos = sqrt(d) / n2n1;
            float Rpara = (n1 * inCos - n2 * outCos) /
                (n1 * inCos + n2 * outCos);
            Rpara *= Rpara;
            float Rperp = (n2 * inCos - n1 * outCos) /
                (n2 * inCos + n1 * outCos);
            Rperp *= Rperp;
            return (Rpara + Rperp) * 0.5f;
        }
        return 1;
    }

    float Specular(in vec3 V, in vec3 N, in vec3 L){
        const float roughness = 0.7;
        const float a = roughness * roughness;
        const float a2 = a * a;
        const vec3 H = normalize(V + L);
        const float k = a / 2;
        const float NH = dot(N, H);
        const float NL = dot(N, L);
        const float NV = dot(N, V);
        if(NH < 0 || NL < 0) return 0;
        const float term1 = NH * NH * (a2 - 1) + 1;
        const float term2 = NL * (1 - k) + k;
        const float term3 = NV * (1 - k) + k;
        return a2 * (1.0f / (4.0 * M_PI)) / (term1 * term1 * term2 * term3);
    }

    void main(){
        vec3 texColor = texture(texSampler, fragTexCoord).xyz;
        float diffuse = 0;
        float specular = 0;
        vec3 V = normalize(camPos - fragPos);
        for(int i=0;i<LIGHT_NUM;i++){
            vec3 L2F = lightPos[i] - fragPos;
            float dist2 = dot(L2F, L2F);
            float dist = sqrt(dist2);
            vec3 L = L2F / dist;
            const float ks = FresnelTerm(fragNorm, L);
            const float kd = 1 - ks;
            const float c = max(dot(L, fragNorm), 0.1);
            float shadowDepth = texture(shadowSampler[i], L2F).r;
            //float shadow = (shadowDepth != 0.0f && dist2 > shadowDepth) ? 0 : 1;
            float shadow = dist2 > shadowDepth ? 0 : 1;
            diffuse += shadow * c * kd * lightStr / dist2;
            specular += shadow * max(Specular(V, fragNorm, L), 0) * c * ks * lightStr / dist2;
        }
        color = vec4((diffuse / M_PI) * texColor + specular * lightColor, 1);
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
    out vec3 fragPos;
    void main(){
        vec3 p[]={
            vec3(-50, 0, -50), vec3(50, 0, 50), vec3(50, 0, -50),
            vec3(-50, 0, -50), vec3(-50, 0, 50), vec3(50, 0, 50)
        };
        gl_Position = projTransform * viewTransform * vec4(p[gl_VertexID], 1);
        fragPos = p[gl_VertexID];
    }
    """
    fragShaderSrc = """
    #version 450 core
    #define M_PI 3.1415926535897932384626433832795
    layout(location=4) uniform vec3 camPos;
    """ + LIGHT_CONFIG + """
    float FresnelTerm(in vec3 N, in vec3 L) { const float n1 = 1; const float n2 = 1.5; const float inCos = max(dot(L, N), 0.0f); float n2n1 = n2 / n1; const float d = inCos * inCos - 1 + n2n1 * n2n1; if (d > 1e-5) { const float outCos = sqrt(d) / n2n1; float Rpara = (n1 * inCos - n2 * outCos) / (n1 * inCos + n2 * outCos); Rpara *= Rpara; float Rperp = (n2 * inCos - n1 * outCos) / (n2 * inCos + n1 * outCos); Rperp *= Rperp; return (Rpara + Rperp) * 0.5f; } return 1; }

    float Specular(in vec3 V, in vec3 N, in vec3 L){ const float roughness = 0.9; const float a = roughness * roughness; const float a2 = a * a; const vec3 H = normalize(V + L); const float k = a / 2; const float NH = dot(N, H); const float NL = dot(N, L); const float NV = dot(N, V); const float term1 = NH * NH * (a2 - 1) + 1; const float term2 = NL * (1 - k) + k; const float term3 = NV * (1 - k) + k; return a2 * (1.0f / (4.0 * M_PI)) / (term1 * term1 * term2 * term3); }
    in vec3 fragPos;
    out vec4 color;
    void main(){
        const vec3 texColor = vec3(0.3, 0.3, 0.3);
        float diffuse = 0;
        float specular = 0;
        vec3 V = normalize(camPos - fragPos);
        const vec3 fragNorm = vec3(0,1,0);
        for(int i=0;i<LIGHT_NUM;i++){
            vec3 L2F = lightPos[i] - fragPos;
            float dist2 = dot(L2F, L2F);
            float dist = sqrt(dist2);
            vec3 L = L2F / dist;
            const float ks = FresnelTerm(fragNorm, L);
            const float kd = 1 - ks;
            const float c = max(dot(L, fragNorm), 0.1);
            float shadowDepth = texture(shadowSampler[i], L2F).r;
            float shadow = (shadowDepth != 0.0f && dist2 > shadowDepth) ? 0 : 1;
            diffuse += shadow * c * kd * lightStr / dist2;
            specular += shadow * max(Specular(V, fragNorm, L), 0) * c * ks * lightStr / dist2;
        }
        color = vec4((diffuse / M_PI) * texColor + specular * lightColor,1);
    }
    """
    pid = CreateShader(vertShaderSrc, fragShaderSrc)
    return pid

def CreateShadowShader():
    vertShaderSrc = """
    #version 450 core
    layout(location=0) uniform mat4 modelTransform;
    void main(){
        vec3 p[] = { vec3(-0.5, -0.5, -0.5), vec3( 0.5, -0.5, -0.5), vec3( 0.5,  0.5, -0.5), vec3(-0.5,  0.5, -0.5), vec3(-0.5, -0.5,  0.5), vec3( 0.5, -0.5,  0.5), vec3( 0.5,  0.5,  0.5), vec3(-0.5,  0.5,  0.5), };
        int index[]={ 1,0,2, 2,0,3, 6,4,5, 7,4,6, 3,0,4, 3,4,7, 5,1,2, 6,5,2, 5,0,1, 4,0,5, 2,3,6, 6,3,7, };
        gl_Position = modelTransform * vec4(p[index[gl_VertexID]], 1); 
    }
    """

    geomShaderSrc = """
    #version 450 core
    layout(triangles) in;
    layout(triangle_strip, max_vertices=18) out;
    layout(location=1) uniform mat4 viewProj[6];
    out vec3 fragPos;
    void main(){
        for(int face=0;face<6;face++){
            gl_Layer=face;
            for(int i=0;i<3;i++){
                gl_Position = viewProj[face] * gl_in[i].gl_Position;
                fragPos = gl_in[i].gl_Position.xyz;
                EmitVertex();
            }
            EndPrimitive();
        }
    }
    """
    fragShaderSrc = """
    #version 450 core
    layout(location=7) uniform vec3 lightPos;
    in vec3 fragPos;
    out float color;
    void main(){
        vec3 dist = lightPos - fragPos;
        color = dot(dist, dist);
    }
    """
    pid = CreateShader(vertShaderSrc, fragShaderSrc, geomShaderSrc)
    return pid

def CreateAlphabat():
    #to do
    vertShaderSrc = """
    #version 450 core
    layout(location=1) uniform int input_ascii_code;
    layout(location=3) uniform vec2 posi;
    layout(location=4) uniform float size;

    out vec2 pos;
    void main(){
        int c=input_ascii_code;
        float i,j,dd,dy,Ax,Ay,Bx,By,Cx,Cy,Dx,Dy;
        c=c-32;
        i=float(c/16);
        j=float(c%16);
        
        dd=0.05*size;
        dy=0.07*size;
        Ax=j/16.0,Ay=(i/6.0);
        Bx=(j+1)/16.0,By=(i/6.0);
        Cx=j/16.0,Cy=((i+1)/6.0);
        Dx=(j+1)/16.0,Dy=(i+1)/6.0;
        vec2 texp[]={//ascii上 0~1 0~1
            vec2(Ax, Ay), vec2(Cx, Cy), vec2(Dx,Dy),
            vec2(Dx,Dy), vec2(Bx,By), vec2(Ax,Ay)
        };
        float xx=posi.x;
        float yy=posi.y;
        Ax=xx,Ay=yy;
        Bx=xx+dd,By=yy;
        Cx=xx,Cy=(yy-dy);
        Dx=xx+dd,Dy=yy-dy;
        vec2 p[]={ //畫面上-1~1 -1~1
            vec2(Ax, Ay), vec2(Cx, Cy), vec2(Dx,Dy),
            vec2(Dx,Dy), vec2(Bx,By), vec2(Ax,Ay)
        };
        gl_Position = vec4(p[gl_VertexID], 0 , 1 );
        pos=texp[gl_VertexID];
    }
    """
    fragShaderSrc = """
    #version 450 core
    layout(location=0) uniform sampler2D texSampler;
    layout(location=2) uniform vec2 position;
    layout(location=5) uniform vec3 textColor;

    in vec2 pos;
    out vec4 color;
    void main(){
        vec3 c = texture(texSampler,pos).xyz;
        color = vec4((vec3(1)-c) * textColor, 1 - length(c));
    }
    """
    pid = CreateShader(vertShaderSrc, fragShaderSrc)
    LoadAlphabatTexture()
    return pid

def CreateSkyboxShader():
    vertShaderSrc = """
    #version 450 core
    layout(location=1) uniform mat4 viewTransform;
    layout(location=2) uniform mat4 projTransform;
    out vec3 fragPos;
    void main(){
        const float len = 28.8f;
        vec3 p[]={
            vec3(-len,-len,-len),
            vec3( len,-len,-len),
            vec3( len, len,-len),
            vec3(-len, len,-len),

            vec3(-len,-len, len),
            vec3( len,-len, len),
            vec3( len, len, len),
            vec3(-len, len, len),

        };
        int index[]={
            0,1,2,
            0,2,3,
            4,6,5,
            4,7,6,
            1,5,2,
            2,5,6,
            0,3,4,
            3,7,4,
            0,4,1,
            1,4,5,
            3,2,7,
            2,6,7
        };
        vec3 tem = (viewTransform * vec4(p[index[gl_VertexID]],0.0f)).xyz;
        gl_Position = projTransform * vec4(tem, 1.0);
        fragPos = p[index[gl_VertexID]];
    }
    """
    fragShaderSrc = """
    #version 450 core
    #define M_PI 3.1415926535897932384626433832795
    layout(location=0) uniform sampler2D texSampler;
    in vec3 fragPos;
    out vec4 color;
    void main(){
        float theta = atan(fragPos.z, fragPos.x) / (2.0*M_PI) + 0.5;
        float phi = atan(fragPos.y, length(vec2(fragPos.x,fragPos.z))) / (2.0*M_PI) + 0.5;
        color = vec4(texture(texSampler, vec2(theta, -phi)).xyz,1);
    }
    """
    pid = CreateShader(vertShaderSrc, fragShaderSrc)
    LoadSkyboxTexture()
    return pid
    
def CreateACShader():
    #to do
    vertShaderSrc = """
    #version 450 core
    layout(location=3) uniform vec2 posi;
    layout(location=4) uniform float size;

    out vec2 pos;
    void main(){
        float i,j,dd,dy,Ax,Ay,Bx,By,Cx,Cy,Dx,Dy;
        vec2 texp[]={// 0~1 0~1
            vec2(0.0, 0.0), vec2(0.0, 1.0), vec2(1.0,1.0),
            vec2(1.0,1.0), vec2(1.0,0.0), vec2(0.0,0.0)
        };
        dd=0.05*size;
        dy=0.07*size;
        float xx=posi.x;
        float yy=posi.y;
        Ax=xx,Ay=yy;
        Bx=xx+dd,By=yy;
        Cx=xx,Cy=(yy-dy);
        Dx=xx+dd,Dy=yy-dy;
        vec2 p[]={ //畫面上-1~1 -1~1
            vec2(Ax, Ay), vec2(Cx, Cy), vec2(Dx,Dy),
            vec2(Dx,Dy), vec2(Bx,By), vec2(Ax,Ay)
        };
        gl_Position = vec4(p[gl_VertexID], 0 , 1 );
        pos=texp[gl_VertexID];
    }
    """
    fragShaderSrc = """
    #version 450 core
    layout(location=0) uniform sampler2D texSampler;
    in vec2 pos;
    out vec4 color;
    void main(){
        vec3 c = texture(texSampler,pos).xyz;
        color = vec4(c,1);
    }
    """
    pid = CreateShader(vertShaderSrc, fragShaderSrc)
    LoadACTexture()
    return pid

def CreateWAShader():
    #to do
    vertShaderSrc = """
    #version 450 core
    layout(location=3) uniform vec2 posi;
    layout(location=4) uniform float size;

    out vec2 pos;
    void main(){
        float i,j,dd,dy,Ax,Ay,Bx,By,Cx,Cy,Dx,Dy;
        vec2 texp[]={//ascii上 0~1 0~1
            vec2(0.0, 0.0), vec2(0.0, 1.0), vec2(1.0,1.0),
            vec2(1.0,1.0), vec2(1.0,0.0), vec2(0.0,0.0)
        };
        dd=0.05*size;
        dy=0.07*size;
        float xx=posi.x;
        float yy=posi.y;
        Ax=xx,Ay=yy;
        Bx=xx+dd,By=yy;
        Cx=xx,Cy=(yy-dy);
        Dx=xx+dd,Dy=yy-dy;
        vec2 p[]={ //畫面上-1~1 -1~1
            vec2(Ax, Ay), vec2(Cx, Cy), vec2(Dx,Dy),
            vec2(Dx,Dy), vec2(Bx,By), vec2(Ax,Ay)
        };
        gl_Position = vec4(p[gl_VertexID], 0 , 1 );
        pos=texp[gl_VertexID];
    }
    """
    fragShaderSrc = """
    #version 450 core
    layout(location=0) uniform sampler2D texSampler;
    in vec2 pos;
    out vec4 color;
    void main(){
        vec3 c = texture(texSampler,pos).xyz;
        color = vec4(c,1);
    }
    """
    pid = CreateShader(vertShaderSrc, fragShaderSrc)
    LoadWATexture()
    return pid