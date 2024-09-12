import bpy
import mathutils
import os

class Material_Green_Glow(bpy.types.Operator):
	bl_idname = "node.material_green_glow"
	bl_label = "Material_Green_Glow"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		mat = bpy.data.materials.new(name = "Material_Green_Glow")
		mat.use_nodes = True
		#initialize Material_Green_Glow node group
		def material_green_glow_node_group():

			material_green_glow = mat.node_tree
			#start with a clean node tree
			for node in material_green_glow.nodes:
				material_green_glow.nodes.remove(node)
			material_green_glow.color_tag = 'NONE'
			material_green_glow.description = ""

			#material_green_glow interface

			#initialize material_green_glow nodes
			#node Principled BSDF
			principled_bsdf = material_green_glow.nodes.new("ShaderNodeBsdfPrincipled")
			principled_bsdf.name = "Principled BSDF"
			principled_bsdf.distribution = 'MULTI_GGX'
			principled_bsdf.subsurface_method = 'RANDOM_WALK'
			#Base Color
			principled_bsdf.inputs[0].default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
			#Metallic
			principled_bsdf.inputs[1].default_value = 0.0
			#Roughness
			principled_bsdf.inputs[2].default_value = 0.5
			#IOR
			principled_bsdf.inputs[3].default_value = 1.5
			#Alpha
			principled_bsdf.inputs[4].default_value = 1.0
			#Normal
			principled_bsdf.inputs[5].default_value = (0.0, 0.0, 0.0)
			#Subsurface Weight
			principled_bsdf.inputs[7].default_value = 0.0
			#Subsurface Radius
			principled_bsdf.inputs[8].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
			#Subsurface Scale
			principled_bsdf.inputs[9].default_value = 0.05000000074505806
			#Subsurface Anisotropy
			principled_bsdf.inputs[11].default_value = 0.0
			#Specular IOR Level
			principled_bsdf.inputs[12].default_value = 0.5
			#Specular Tint
			principled_bsdf.inputs[13].default_value = (1.0, 1.0, 1.0, 1.0)
			#Anisotropic
			principled_bsdf.inputs[14].default_value = 0.0
			#Anisotropic Rotation
			principled_bsdf.inputs[15].default_value = 0.0
			#Tangent
			principled_bsdf.inputs[16].default_value = (0.0, 0.0, 0.0)
			#Transmission Weight
			principled_bsdf.inputs[17].default_value = 0.0
			#Coat Weight
			principled_bsdf.inputs[18].default_value = 0.0
			#Coat Roughness
			principled_bsdf.inputs[19].default_value = 0.029999999329447746
			#Coat IOR
			principled_bsdf.inputs[20].default_value = 1.5
			#Coat Tint
			principled_bsdf.inputs[21].default_value = (1.0, 1.0, 1.0, 1.0)
			#Coat Normal
			principled_bsdf.inputs[22].default_value = (0.0, 0.0, 0.0)
			#Sheen Weight
			principled_bsdf.inputs[23].default_value = 0.0
			#Sheen Roughness
			principled_bsdf.inputs[24].default_value = 0.5
			#Sheen Tint
			principled_bsdf.inputs[25].default_value = (1.0, 1.0, 1.0, 1.0)
			#Emission Color
			principled_bsdf.inputs[26].default_value = (0.0624852180480957, 1.0, 0.10521848499774933, 1.0)
			#Emission Strength
			principled_bsdf.inputs[27].default_value = 1.2000000476837158
			#Thin Film Thickness
			principled_bsdf.inputs[28].default_value = 0.0
			#Thin Film IOR
			principled_bsdf.inputs[29].default_value = 1.3300000429153442

			#node Material Output
			material_output = material_green_glow.nodes.new("ShaderNodeOutputMaterial")
			material_output.name = "Material Output"
			material_output.is_active_output = True
			material_output.target = 'ALL'
			#Displacement
			material_output.inputs[2].default_value = (0.0, 0.0, 0.0)
			#Thickness
			material_output.inputs[3].default_value = 0.0


			#Set locations
			principled_bsdf.location = (10.0, 300.0)
			material_output.location = (300.0, 300.0)

			#Set dimensions
			principled_bsdf.width, principled_bsdf.height = 240.0, 100.0
			material_output.width, material_output.height = 140.0, 100.0

			#initialize material_green_glow links
			#principled_bsdf.BSDF -> material_output.Surface
			material_green_glow.links.new(principled_bsdf.outputs[0], material_output.inputs[0])
			return material_green_glow

		material_green_glow = material_green_glow_node_group()

		return {'FINISHED'}

def menu_func(self, context):
	self.layout.operator(Material_Green_Glow.bl_idname)

def register():
	bpy.utils.register_class(Material_Green_Glow)
	bpy.types.NODE_MT_add.append(menu_func)

def unregister():
	bpy.utils.unregister_class(Material_Green_Glow)
	bpy.types.NODE_MT_add.remove(menu_func)

if __name__ == "__main__":
	register()
