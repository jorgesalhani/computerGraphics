import polyscope as ps
import numpy as np
ps.set_navigation_style("free")
ps.set_up_dir("z_up")
ps.init()
ps.look_at(camera_location=(0,0,1), target=(0,1,1))

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


def main():
  vertices_original = np.array([
    [1,4,0],
    [-1,4,0],
    [1,4,1],
    [-1,4,1]
  ])

  faces = np.array([
    [0,1,2],
    [1,3,2]
  ])
  ps.register_point_cloud("my points", np.array([[0,0,1],[0,0,-2]]))

  ps_mesh = ps.register_surface_mesh("my mesh", vertices_original, faces)
  dt = 0
  def callback():
    
    nonlocal vertices_original, dt
    vertices = process(vertices_original, dt)
    dt +=  0.01

    ps_mesh.update_vertex_positions(vertices)

  ps.set_user_callback(callback)
  ps.show()
main()