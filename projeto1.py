import polyscope as ps
import numpy as np
ps.set_navigation_style("free")
ps.set_up_dir("z_up")
ps.init()
ps.look_at(camera_location=(0,-5,1), target=(0,1,1))

def animar_rotacao_y(vertices, angulo):
  R = np.array([
    [np.cos(angulo), 0, -np.sin(angulo)],
    [0, 1, 0],
    [np.sin(angulo), 0, np.cos(angulo)],
  ])
  resultado = np.matmul(R, vertices.transpose()).transpose()
  return resultado

def process(vertices, dt):

  angulo = dt
  vertices = animar_rotacao_y(vertices, angulo)
  return vertices


def main(V, F):
  ps_mesh = ps.register_surface_mesh("my mesh", V, F)
  dt = 0
  def callback():
    
    nonlocal V, dt
    vertices = process(V, dt)
    dt +=  0.03

    ps_mesh.update_vertex_positions(vertices)

  ps.set_user_callback(callback)
  ps.show()


def verticesFacesObj(arquivo_obj):
  vertices = []
  faces = []
  with open(arquivo_obj, 'r') as dados:
    for linha in dados.readlines():
      linha = linha.split()
      if len(linha) == 0: continue
      if linha[0] == 'v':
        v = [float(i) for i in linha[1:]]
        vertices.append(v)
      elif linha[0] == 'f':
        f = [int(i)-1 for i in linha[1:]]
        faces.append(f)
  return {'vertices': np.array(vertices), 'faces': np.array(faces)}


ps.register_point_cloud("my points", np.array([[0,-100,0], [0,100,0],[-100, -100,-200]]))
obj = verticesFacesObj('./objFiles/teapot.obj')
vertices = obj['vertices']
faces = obj['faces']
# print(vertices)
# print(faces)
main(vertices, faces)