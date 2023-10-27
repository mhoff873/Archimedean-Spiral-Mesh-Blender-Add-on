import bpy
import numpy as np
from math import pi, cos, sin, sqrt

bl_info = {
    "name": "Archimedean Spiral Mesh",
    "author": "Mason Hoffman",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Add > Mesh > Mason's Meshes",
    "description": "Adds a new Archimedean Spiral Mesh",
    "warning": "", 
    "doc_url": "",  
    "category": "Add Mesh",
}

def calculate_final_angle(a, b, desired_length, steps=1000):
    total_length = 0
    theta = 0
    d_theta = 0.1  # Small step in theta

    for _ in range(steps):
        # Compute the infinitesimal arc length dL and add it to total_length
        r = a + b * theta
        dr_dtheta = b
        dL = sqrt((r * d_theta)**2 + (dr_dtheta * d_theta)**2)
        total_length += dL
        theta += d_theta

        # Check if we've reached or exceeded the desired length
        if total_length >= desired_length:
            break

    return theta

def create_archimedean_spiral(a, distance_between_rings, n, vertices, tube_radius, ring_density):
    b = distance_between_rings / np.pi  # Adjust the distance between rings
    
    # Calculate the final angle for the given length
    theta_f = calculate_final_angle(a, b, n)
    num_rings = int(n * ring_density)  # Number of discrete rings
    theta = np.linspace(0, theta_f, num_rings)

    spiral_vertices = []
    spiral_faces = []

    for i in range(num_rings):
        angle = theta[i]
        r = a + b * angle

        # Position at this point
        x = r * cos(angle)
        y = r * sin(angle)

        # Tangent direction
        dx = cos(angle) - r * sin(angle)
        dy = sin(angle) + r * cos(angle)

        # Normalize derivative to get tangent
        length = sqrt(dx**2 + dy**2)
        tangent = np.array([dx / length, dy / length, 0])

        # Choose an arbitrary up vector
        up = np.array([0, 0, 1])

        # Compute normal and binormal
        normal = np.cross(up, tangent)
        binormal = np.cross(tangent, normal)

        # Create a ring of vertices
        loop_start = len(spiral_vertices)
        for j in range(vertices):
            theta_vertex = (2 * pi * j) / vertices
            vertex_dir = cos(theta_vertex) * normal + sin(theta_vertex) * binormal
            vertex_pos = np.array([x, y, 0]) + tube_radius * vertex_dir
            spiral_vertices.append(tuple(vertex_pos))

            # Connect vertices to form faces
            if i > 0:
                prev_loop_start = loop_start - vertices
                next_j = (j + 1) % vertices  # Wrap around to start of ring
                face = (prev_loop_start + j, prev_loop_start + next_j,
                        loop_start + next_j, loop_start + j)
                spiral_faces.append(face)

    # Cap the ends of the tube
    if num_rings > 1:
        # Cap the start
        start_face = [i for i in range(vertices)]
        spiral_faces.append(tuple(start_face))

        # Cap the end
        end_face = [len(spiral_vertices) - i - 1 for i in range(vertices)]
        spiral_faces.append(tuple(end_face))

    # Create the mesh
    mesh = bpy.data.meshes.new(name="SpiralMesh")
    obj = bpy.data.objects.new("Spiral", mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # Assign vertices and faces to the mesh
    mesh.from_pydata(spiral_vertices, [], spiral_faces)
    mesh.update()

class MyCustomMeshesMenu(bpy.types.Menu):
    bl_idname = "VIEW3D_MT_mesh_mason_meshes"
    bl_label = "Mason's Meshes"

    def draw(self, context):
        layout = self.layout
        layout.operator("mesh.spiral_add", text="Archimedean Spiral")

class SpiralOperator(bpy.types.Operator):
    """Add an Archimedean Spiral Mesh to simulate a coiled tube"""
    bl_idname = "mesh.spiral_add"
    bl_label = "Archimedean Spiral Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    a: bpy.props.FloatProperty(name="Spiral Start", default=5.0)
    b: bpy.props.FloatProperty(name="Spiral Gap", default=0.51)
    n: bpy.props.FloatProperty(name="Spiral Length", default=5.0)
    tube_radius: bpy.props.FloatProperty(name="Ring Radius", default=0.5, min=0.1)
    vertices: bpy.props.IntProperty(name="Ring Vertices", default=32, min=3, max=256)
    ring_density: bpy.props.FloatProperty(name="Ring Density", default=10.0, min=1.0)

    def execute(self, context):
        create_archimedean_spiral(self.a, self.b, self.n, self.vertices, self.tube_radius, self.ring_density)
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.menu("VIEW3D_MT_mesh_mason_meshes")

def register():
    bpy.utils.register_class(SpiralOperator)
    bpy.utils.register_class(MyCustomMeshesMenu)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

def unregister():
    bpy.utils.unregister_class(SpiralOperator)
    bpy.utils.unregister_class(MyCustomMeshesMenu)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()