bl_info = {
    "name": "Add Fog",
    "blender": (2, 80, 0),
    "category": "Object",
    "description": "Adds a fog to the selected object with a button in the N-panel",
}

import bpy

# Define the addon class to add fog material
class OBJECT_OT_add_fog_material(bpy.types.Operator):
    bl_idname = "object.add_fog"
    bl_label = "Add Fog"
    bl_description = "Adds a fog material to the selected object"

    def execute(self, context):
        # Ensure an object is selected
        obj = context.object
        if obj is None:
            self.report({'ERROR'}, "No object selected")
            return {'CANCELLED'}

        # Create a new material
        fog_material = bpy.data.materials.new(name="FogMaterial")
        fog_material.use_nodes = True
        nodes = fog_material.node_tree.nodes
        links = fog_material.node_tree.links

        # Clear default nodes
        nodes.clear()

        # Add nodes
        tex_coord_node = nodes.new(type='ShaderNodeTexCoord')
        mapping_node = nodes.new(type='ShaderNodeMapping')
        noise_texture_node = nodes.new(type='ShaderNodeTexNoise')
        color_ramp_node = nodes.new(type='ShaderNodeValToRGB')
        principled_volume_node = nodes.new(type='ShaderNodeVolumePrincipled')
        volume_scatter_node = nodes.new(type='ShaderNodeVolumeScatter')
        mix_shader_node = nodes.new(type='ShaderNodeMixShader')
        output_node = nodes.new(type='ShaderNodeOutputMaterial')

        # Set node locations for organization
        tex_coord_node.location = (-800, 0)
        mapping_node.location = (-600, 0)
        noise_texture_node.location = (-400, 0)
        color_ramp_node.location = (-200, 0)
        principled_volume_node.location = (0, 200)
        volume_scatter_node.location = (0, -200)
        mix_shader_node.location = (200, 0)
        output_node.location = (400, 0)

        # Configure node properties
        mapping_node.inputs['Scale'].default_value = (1.0, 1.0, 1.0)
        noise_texture_node.inputs['Scale'].default_value = 5.0
        noise_texture_node.inputs['Detail'].default_value = 15.0
        principled_volume_node.inputs['Density'].default_value = 0.04
        principled_volume_node.inputs['Anisotropy'].default_value = 0.65
        volume_scatter_node.inputs['Density'].default_value = 0.0
        volume_scatter_node.inputs['Anisotropy'].default_value = 0.65

        # Set up color ramp points (black at 0 and white at 1)
        color_ramp_node.color_ramp.elements[0].position = 0.0
        color_ramp_node.color_ramp.elements[0].color = (0, 0, 0, 1)  # Black color
        color_ramp_node.color_ramp.elements[1].position = 1.0
        color_ramp_node.color_ramp.elements[1].color = (1, 1, 1, 1)  # White color

        # Link nodes
        links.new(tex_coord_node.outputs['Generated'], mapping_node.inputs['Vector'])
        links.new(mapping_node.outputs['Vector'], noise_texture_node.inputs['Vector'])
        links.new(noise_texture_node.outputs['Fac'], color_ramp_node.inputs['Fac'])
        links.new(color_ramp_node.outputs['Color'], volume_scatter_node.inputs['Density'])  # Connect only to volume scatter density
        links.new(principled_volume_node.outputs['Volume'], mix_shader_node.inputs[1])
        links.new(volume_scatter_node.outputs['Volume'], mix_shader_node.inputs[2])
        links.new(mix_shader_node.outputs['Shader'], output_node.inputs['Volume'])

        # Assign the material to the selected object
        if obj.data.materials:
            obj.data.materials[0] = fog_material
        else:
            obj.data.materials.append(fog_material)

        return {'FINISHED'}

# Panel class to add the button in the N-panel (3D Viewport sidebar)
class OBJECT_PT_add_fog_panel(bpy.types.Panel):
    bl_label = "Fog Material"
    bl_idname = "OBJECT_PT_add_fog_panel"
    bl_space_type = 'VIEW_3D'             # 3D Viewport
    bl_region_type = 'UI'                 # Sidebar (N-panel)
    bl_category = "Add Fog"             # Tab in the N-panel

    def draw(self, context):
        layout = self.layout
        layout.operator("object.add_fog")
        layout.separator()  # Adds a blank line
        layout.label(text="Adds a fog material to the selected object")
        layout.separator()  # Adds a blank line
        layout.label(text="CREATED BY - 01k")

# Register and unregister the classes
def register():
    bpy.utils.register_class(OBJECT_OT_add_fog_material)
    bpy.utils.register_class(OBJECT_PT_add_fog_panel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_fog_material)
    bpy.utils.unregister_class(OBJECT_PT_add_fog_panel)

if __name__ == "__main__":
    register()
