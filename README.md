# unreal_scripts

## Description
Unreal Engine Python optimization scripts. Use for searching assets data information. Searching weak parts of game project. Importing assets pipeline from Blender to Unreal.
Can autoconnect free unconnected nodes(Material Expressions) of TextureSampleParameter2D in material. 
Can connect texture asset to material in form of TextureSampleParameter2D nodes chain with Factor ScalarParameter.

## Functions of Project
### tasks: 
Main launch scripts are in tasks folder

### src:
**get_asset:**
* **find_assets_data** - Return assets of specified type in path folder properties_values is list of tuple [('property', value)] is_disjunction_p (^) = True will find asset, if one of the property_value pair has been found. 
* find_assets_data_log - Find all filtered assets and write log about found results If old value is None, all values will be valid and included in find results. 
* load_asset - load asset with proper checks	
* get_asset_data_by_object_path
* get_asset_data_by_object
* get_asset_by_object_path
* get_assets_by_dirs
* **get_assets_data_by_dirs_n_classes**
* **get_textures_data_by_dirs** | materials | static_mesh | skeletal mesh
* get_materials_data_two_sided

**set_asset**
* **set_assets_properties_in_folder** - Set asset properties by values
* consolidate_assets_by_dir - Consolidate assets with the same name, stored in different dirs. 
* delete_all_in_dir - Deletes all Everything in directory. 

**get_material**
* **find_nodes_in_material** - Find nodes in material by nodes type, properties_values, is linked flag. 
* find_nodes_in_material_by_path
* find_unlinked_texture_nodes
* **get_material_all_nodes_tapython** - Getting all material nodes using TAPython plugin https://github.com/cgerchenhp/UE_TAPython_Plugin_Release. 
* get_material_all_nodes_by_path
* get_material_connections - return list of all connections in material
* **find_connections_of_node** - Find connections of node.
* **get_texture_asset_from_node**
* get_texture_node_source_path - Find texture source path by node of type inhereted by unreal.MaterialExpression. 
* get_texture_type_by_prefix_suffix_node - Reads prefix and suffix of texture asset and returns type of texture by convention.
* get_texture_parameter_name - Standardize Texture Parameter Name. 

**set_material**
* **transfer_connections** - Transfers connection between two nodes.
* transfer_texture_node
* from_TextureBase_to_TextureParameter2D - Transfers data From TextureBase To TextureSampleParameter2D.
* from_TextureSample_to_TextureParameter2D - Transfers data From TextureSample To TextureSampleParameter2D.
* from_TextureParameter_to_TextureParameter2D - Transfers data From TextureSampleParameter To TextureSampleParameter2D. 
* from_TextureParameter2D_to_TextureParameter2D
* set_texture_parameter_name - Sets correct texture parameter name by texture type. 
* **new_node_TextureSampleParameter2D** - Creates TextureSampleParameter2D node with data from node_data @node_data (DataTextureSampleParameter2D) wrapper object for node. 
* **new_node_Vector** - Creates Vector node TODO: Add more editor_properties.
* new_node_BaseColorVector - Creates Base color vector useful for multiplying with diffuse map or albedo.
* new_node_ScalarParameter_texture_factor - Creates Base color vector useful for multiplying with diffuse map or albedo. 
* new_blend_overlay_node - Creates material expression/node of blend_overlay material function call. 
* replace_parameters_space_to_underscore - Replace all white space chars in parameter names in material. 
* recompile_material_in_dirs - Recompile all materials in dir_paths after changes in material

**import_pipeline**
* **import_assets_pipeline_hybrid**
* **import_fbx_scene_n_subobjects**
* **import_fbx_default** - Default variant of importing fbx file.
* make_import_asset_tasks
* are_import_tasks_succeed
* exec_import_asset_tasks

**asset_library**
* move_assets - Moves assets by there asset_data to destination folder Will compile unsaved material.
* move_assets_in_dirs
* delete_assets - Deletes assets by assets_data.
 
**material_library**
* **auto_align_material_nodes** - Change coordinate of nodes to exclude nodes collision Auto align only works for nodes, that have been connected to material output property. 
* replace_texture_sample_to_parameters_in_materials - Replaces all TextureSamples with TextureSamplesParameter2D. 
* generate_texture_factor_multiply - Generates Group of connected nodes: Texture, Texture_Factor(Scalar_Parameter), Multiply. 
* generate_texture_factor_chain - Generates nodes chain for: Metallic, Specular, Roughness Chain is connected to output.
* generate_basecolor_vector_chain - Generates nodes chain for: Metallic, Specular, Roughness. 
* generate_gloss_texture_chain - Generates nodes chain for: Metallic, Specular, Roughness. 
* generate_convex_concave_chain - Basecolor map(Base V3) + Concave/Convex map(Blend V3) -> Blend_overlay node -> Basecolor.
* generate_bump_height_chain_v1 - First variant of realisation of linking bump map or height map Simple connection with World Position Offset. 
* generate_bump_height_chain_v2 - Second variant of realisation of linking bump map or height map https://docs.unrealengine.com/4.27/en-US/RenderingAndGraphics/Materials/HowTo/BumpOffset/. 
* generate_texture_displacement_chain
* **generate_support_nodes_n_link** - Generate nodes, needed for texture type, and link them to material output. 
* **link_textures_nodes_to_result_node** - Links texture node to result node/material output node.
* **connect_free_texture_nodes_in_materials** - Connect free unlinked texture_nodes in material with material output You can add textures nodes inside material in material editor. 
* **connect_textures_files_to_materials** - Creates expressions/nodes inside material from textures files and links nodes to material output Many textures files added to Many materials. 
* **connect_texture_files_packs** - Connects textures lists in texture_pack_paths to material_paths. 
* **connect_by_association_texture_file_dirs** - Connects textures from textures_dirs inside material in material editor from many directories, packs Connects textures with the same file name without prefix-suffix with material Connects all unlinked texture nodes inside material Using, when importing from many 3d model project FIX: Adding Convex_Concave map. 

**prefix_suffix**
* **add_prefix_suffix**
* **delete_prefix_suffix**
* **replace_prefix_suffix**
* **correct_prefix_suffix**
* delete_glb_texture_prefix
* get_prefix
* get_suffix
* get_asset_name_without_prefix_suffix
* get_asset_prefix_suffix_by_path
* delete_prefix_suffix_in_name

**collision**
* **find_no_collision_assets** - Find No Collider assets. 
* has_simple_collision - There are two types of collision.

**get_static_mesh**
* get_static_mesh_triangles_count

**lod**
* **find_no_mipmap_textures_log** - Find all textures not in Power of two mode. 
* **find_no_lods_meshes_log** - Find all meshes without lod groups.
* set_textures_mipmap_gen_settings_dirs
* set_meshes_lod_group_log
* **activate_textures_gen_mipmaps_on_dirs**
* **activate_meshes_gen_lods_on_dirs**

**naming_convention**
* AssetsPrefixConventionTable
* TextureTypesConvention
* **TextureTypesCustom**

### asset:
**texture**
* get_texture_imported_size - Get texture imported size


## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
MIT License. Open source code.

## Project status
Active