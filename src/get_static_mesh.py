import unreal

#import unreal_scripts.tasks.import_pipeline_ini as import_pipeline_ini
#import unreal_scripts.src.set_material as set_material

#import importlib
#importlib.reload(config)
#importlib.reload(general)

def get_static_mesh_triangles_count(static_mesh, lod_index = 0):
    sections_count = static_mesh.get_num_sections(lod_index)
    unreal.log(sections_count)
    triangles_count = 0
    for section_index in range(sections_count):
        triangles = unreal.ProceduralMeshLibrary.get_section_from_static_mesh(static_mesh, lod_index, section_index)[1]
        triangles_count += len(triangles)

    return triangles_count