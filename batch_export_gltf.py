import bpy
import os

# Export to blend file location
basedir = os.path.dirname(bpy.data.filepath)

godot_dir = os.path.join(basedir, "godot")

if not basedir:
    raise Exception("Blend file is not saved")

# Ensure the godot directory exists
if not os.path.exists(godot_dir):
    os.makedirs(godot_dir)

view_layer = bpy.context.view_layer

obj_active = view_layer.objects.active

# Select all visible objects except those with "-noexport" suffix
selection = [obj for obj in bpy.context.visible_objects if not obj.name.endswith("-noexport")]

bpy.ops.object.select_all(action='DESELECT')

for obj in selection:
    obj.select_set(True)
    # Some exporters only use the active object
    view_layer.objects.active = obj

    name = bpy.path.clean_name(obj.name)
    fn = os.path.join(godot_dir, name)

    # Export as GLTF with separate textures
    bpy.ops.export_scene.gltf(
        filepath=fn + ".gltf",
        export_format='GLTF_SEPARATE',  # Use separate textures
        use_selection=True,
        export_apply=True,  # Apply modifiers
        export_materials='EXPORT',  # Ensure materials are included
        export_texture_dir=os.path.join(godot_dir, "textures")  # Directory for textures
    )
    
    obj.select_set(False)
    
    print("Exported:", fn + ".gltf")

# Restore original selection
view_layer.objects.active = obj_active
for obj in selection:
    obj.select_set(True)
