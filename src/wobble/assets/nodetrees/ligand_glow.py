import bpy
import mathutils
import os


# Todo: is this the best place to register materials?
from ..materials import greenglow
greenglow.register()


class LigandGlow(bpy.types.Operator):
	bl_idname = "node.ligandglow"
	bl_label = "Ligand Glow"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		#initialize boolean_andor node group
		def boolean_andor_node_group():
			boolean_andor = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Boolean AndOr")

			boolean_andor.color_tag = 'CONVERTER'
			boolean_andor.description = ""


			#boolean_andor interface
			#Socket Boolean
			boolean_socket = boolean_andor.interface.new_socket(name = "Boolean", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			boolean_socket.attribute_domain = 'POINT'

			#Socket Inverted
			inverted_socket = boolean_andor.interface.new_socket(name = "Inverted", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			inverted_socket.attribute_domain = 'POINT'

			#Socket And
			and_socket = boolean_andor.interface.new_socket(name = "And", in_out='INPUT', socket_type = 'NodeSocketBool')
			and_socket.attribute_domain = 'POINT'
			and_socket.hide_value = True

			#Socket Or
			or_socket = boolean_andor.interface.new_socket(name = "Or", in_out='INPUT', socket_type = 'NodeSocketBool')
			or_socket.attribute_domain = 'POINT'
			or_socket.hide_value = True

			#Socket Boolean
			boolean_socket_1 = boolean_andor.interface.new_socket(name = "Boolean", in_out='INPUT', socket_type = 'NodeSocketBool')
			boolean_socket_1.attribute_domain = 'POINT'


			#initialize boolean_andor nodes
			#node Group Output
			group_output = boolean_andor.nodes.new("NodeGroupOutput")
			group_output.name = "Group Output"
			group_output.is_active_output = True

			#node Group Input
			group_input = boolean_andor.nodes.new("NodeGroupInput")
			group_input.name = "Group Input"

			#node Boolean Math
			boolean_math = boolean_andor.nodes.new("FunctionNodeBooleanMath")
			boolean_math.name = "Boolean Math"
			boolean_math.operation = 'NOT'

			#node Reroute
			reroute = boolean_andor.nodes.new("NodeReroute")
			reroute.name = "Reroute"
			#node Boolean Math.001
			boolean_math_001 = boolean_andor.nodes.new("FunctionNodeBooleanMath")
			boolean_math_001.name = "Boolean Math.001"
			boolean_math_001.operation = 'AND'

			#node Boolean Math.002
			boolean_math_002 = boolean_andor.nodes.new("FunctionNodeBooleanMath")
			boolean_math_002.name = "Boolean Math.002"
			boolean_math_002.operation = 'OR'




			#Set locations
			group_output.location = (260.0, 0.0)
			group_input.location = (-400.0, 0.0)
			boolean_math.location = (60.0, -120.0)
			reroute.location = (40.0, -40.0)
			boolean_math_001.location = (-180.0, 60.0)
			boolean_math_002.location = (-180.0, -80.0)

			#Set dimensions
			group_output.width, group_output.height = 140.0, 100.0
			group_input.width, group_input.height = 140.0, 100.0
			boolean_math.width, boolean_math.height = 140.0, 100.0
			reroute.width, reroute.height = 16.0, 100.0
			boolean_math_001.width, boolean_math_001.height = 140.0, 100.0
			boolean_math_002.width, boolean_math_002.height = 140.0, 100.0

			#initialize boolean_andor links
			#boolean_math_001.Boolean -> boolean_math_002.Boolean
			boolean_andor.links.new(boolean_math_001.outputs[0], boolean_math_002.inputs[0])
			#reroute.Output -> boolean_math.Boolean
			boolean_andor.links.new(reroute.outputs[0], boolean_math.inputs[0])
			#boolean_math_002.Boolean -> reroute.Input
			boolean_andor.links.new(boolean_math_002.outputs[0], reroute.inputs[0])
			#group_input.And -> boolean_math_001.Boolean
			boolean_andor.links.new(group_input.outputs[0], boolean_math_001.inputs[1])
			#group_input.Or -> boolean_math_002.Boolean
			boolean_andor.links.new(group_input.outputs[1], boolean_math_002.inputs[1])
			#boolean_math.Boolean -> group_output.Inverted
			boolean_andor.links.new(boolean_math.outputs[0], group_output.inputs[1])
			#reroute.Output -> group_output.Boolean
			boolean_andor.links.new(reroute.outputs[0], group_output.inputs[0])
			#group_input.Boolean -> boolean_math_001.Boolean
			boolean_andor.links.new(group_input.outputs[2], boolean_math_001.inputs[0])
			return boolean_andor

		boolean_andor = boolean_andor_node_group()

		#initialize _mn_select_sec_struct_id node group
		def _mn_select_sec_struct_id_node_group():
			_mn_select_sec_struct_id = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".MN_select_sec_struct_id")

			_mn_select_sec_struct_id.color_tag = 'NONE'
			_mn_select_sec_struct_id.description = ""


			#_mn_select_sec_struct_id interface
			#Socket Selection
			selection_socket = _mn_select_sec_struct_id.interface.new_socket(name = "Selection", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			selection_socket.attribute_domain = 'POINT'
			selection_socket.description = "The calculated selection"

			#Socket Inverted
			inverted_socket_1 = _mn_select_sec_struct_id.interface.new_socket(name = "Inverted", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			inverted_socket_1.attribute_domain = 'POINT'

			#Socket And
			and_socket_1 = _mn_select_sec_struct_id.interface.new_socket(name = "And", in_out='INPUT', socket_type = 'NodeSocketBool')
			and_socket_1.attribute_domain = 'POINT'
			and_socket_1.hide_value = True

			#Socket Or
			or_socket_1 = _mn_select_sec_struct_id.interface.new_socket(name = "Or", in_out='INPUT', socket_type = 'NodeSocketBool')
			or_socket_1.attribute_domain = 'POINT'
			or_socket_1.hide_value = True

			#Socket id
			id_socket = _mn_select_sec_struct_id.interface.new_socket(name = "id", in_out='INPUT', socket_type = 'NodeSocketInt')
			id_socket.subtype = 'NONE'
			id_socket.default_value = 1
			id_socket.min_value = -2147483648
			id_socket.max_value = 2147483647
			id_socket.attribute_domain = 'POINT'
			id_socket.description = "Secondary structure component to select"


			#initialize _mn_select_sec_struct_id nodes
			#node Named Attribute.002
			named_attribute_002 = _mn_select_sec_struct_id.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_002.name = "Named Attribute.002"
			named_attribute_002.data_type = 'INT'
			#Name
			named_attribute_002.inputs[0].default_value = "sec_struct"

			#node Group Output
			group_output_1 = _mn_select_sec_struct_id.nodes.new("NodeGroupOutput")
			group_output_1.name = "Group Output"
			group_output_1.is_active_output = True

			#node Compare.012
			compare_012 = _mn_select_sec_struct_id.nodes.new("FunctionNodeCompare")
			compare_012.name = "Compare.012"
			compare_012.data_type = 'INT'
			compare_012.mode = 'ELEMENT'
			compare_012.operation = 'EQUAL'

			#node Group Input
			group_input_1 = _mn_select_sec_struct_id.nodes.new("NodeGroupInput")
			group_input_1.name = "Group Input"

			#node Group
			group = _mn_select_sec_struct_id.nodes.new("GeometryNodeGroup")
			group.name = "Group"
			group.node_tree = boolean_andor




			#Set locations
			named_attribute_002.location = (100.0, -100.0)
			group_output_1.location = (620.0, 140.0)
			compare_012.location = (260.0, 0.0)
			group_input_1.location = (80.0, 100.0)
			group.location = (420.0, 140.0)

			#Set dimensions
			named_attribute_002.width, named_attribute_002.height = 140.0, 100.0
			group_output_1.width, group_output_1.height = 140.0, 100.0
			compare_012.width, compare_012.height = 140.0, 100.0
			group_input_1.width, group_input_1.height = 140.0, 100.0
			group.width, group.height = 140.0, 100.0

			#initialize _mn_select_sec_struct_id links
			#group_input_1.id -> compare_012.A
			_mn_select_sec_struct_id.links.new(group_input_1.outputs[2], compare_012.inputs[2])
			#named_attribute_002.Attribute -> compare_012.B
			_mn_select_sec_struct_id.links.new(named_attribute_002.outputs[0], compare_012.inputs[3])
			#group_input_1.And -> group.And
			_mn_select_sec_struct_id.links.new(group_input_1.outputs[0], group.inputs[0])
			#group_input_1.Or -> group.Or
			_mn_select_sec_struct_id.links.new(group_input_1.outputs[1], group.inputs[1])
			#compare_012.Result -> group.Boolean
			_mn_select_sec_struct_id.links.new(compare_012.outputs[0], group.inputs[2])
			#group.Boolean -> group_output_1.Selection
			_mn_select_sec_struct_id.links.new(group.outputs[0], group_output_1.inputs[0])
			#group.Inverted -> group_output_1.Inverted
			_mn_select_sec_struct_id.links.new(group.outputs[1], group_output_1.inputs[1])
			return _mn_select_sec_struct_id

		_mn_select_sec_struct_id = _mn_select_sec_struct_id_node_group()

		#initialize is_sheet node group
		def is_sheet_node_group():
			is_sheet = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Is Sheet")

			is_sheet.color_tag = 'INPUT'
			is_sheet.description = ""


			#is_sheet interface
			#Socket Selection
			selection_socket_1 = is_sheet.interface.new_socket(name = "Selection", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			selection_socket_1.attribute_domain = 'POINT'
			selection_socket_1.description = "Selected atoms form part of a sheet"

			#Socket Inverted
			inverted_socket_2 = is_sheet.interface.new_socket(name = "Inverted", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			inverted_socket_2.attribute_domain = 'POINT'

			#Socket And
			and_socket_2 = is_sheet.interface.new_socket(name = "And", in_out='INPUT', socket_type = 'NodeSocketBool')
			and_socket_2.attribute_domain = 'POINT'
			and_socket_2.hide_value = True

			#Socket Or
			or_socket_2 = is_sheet.interface.new_socket(name = "Or", in_out='INPUT', socket_type = 'NodeSocketBool')
			or_socket_2.attribute_domain = 'POINT'
			or_socket_2.hide_value = True


			#initialize is_sheet nodes
			#node Group Output
			group_output_2 = is_sheet.nodes.new("NodeGroupOutput")
			group_output_2.name = "Group Output"
			group_output_2.is_active_output = True

			#node Group Input
			group_input_2 = is_sheet.nodes.new("NodeGroupInput")
			group_input_2.name = "Group Input"

			#node MN_select_sec_struct.002
			mn_select_sec_struct_002 = is_sheet.nodes.new("GeometryNodeGroup")
			mn_select_sec_struct_002.label = "Select Sec Struct"
			mn_select_sec_struct_002.name = "MN_select_sec_struct.002"
			mn_select_sec_struct_002.node_tree = _mn_select_sec_struct_id
			#Socket_1
			mn_select_sec_struct_002.inputs[2].default_value = 2




			#Set locations
			group_output_2.location = (267.00146484375, 0.0)
			group_input_2.location = (-220.0, -80.0)
			mn_select_sec_struct_002.location = (0.0, 0.0)

			#Set dimensions
			group_output_2.width, group_output_2.height = 140.0, 100.0
			group_input_2.width, group_input_2.height = 140.0, 100.0
			mn_select_sec_struct_002.width, mn_select_sec_struct_002.height = 217.00146484375, 100.0

			#initialize is_sheet links
			#mn_select_sec_struct_002.Selection -> group_output_2.Selection
			is_sheet.links.new(mn_select_sec_struct_002.outputs[0], group_output_2.inputs[0])
			#group_input_2.And -> mn_select_sec_struct_002.And
			is_sheet.links.new(group_input_2.outputs[0], mn_select_sec_struct_002.inputs[0])
			#group_input_2.Or -> mn_select_sec_struct_002.Or
			is_sheet.links.new(group_input_2.outputs[1], mn_select_sec_struct_002.inputs[1])
			#mn_select_sec_struct_002.Inverted -> group_output_2.Inverted
			is_sheet.links.new(mn_select_sec_struct_002.outputs[1], group_output_2.inputs[1])
			return is_sheet

		is_sheet = is_sheet_node_group()

		#initialize is_loop node group
		def is_loop_node_group():
			is_loop = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Is Loop")

			is_loop.color_tag = 'INPUT'
			is_loop.description = ""


			#is_loop interface
			#Socket Selection
			selection_socket_2 = is_loop.interface.new_socket(name = "Selection", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			selection_socket_2.attribute_domain = 'POINT'
			selection_socket_2.description = "Selected atoms form part of a loop, and not part of any secondary structure"

			#Socket Inverted
			inverted_socket_3 = is_loop.interface.new_socket(name = "Inverted", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			inverted_socket_3.attribute_domain = 'POINT'

			#Socket And
			and_socket_3 = is_loop.interface.new_socket(name = "And", in_out='INPUT', socket_type = 'NodeSocketBool')
			and_socket_3.attribute_domain = 'POINT'
			and_socket_3.hide_value = True

			#Socket Or
			or_socket_3 = is_loop.interface.new_socket(name = "Or", in_out='INPUT', socket_type = 'NodeSocketBool')
			or_socket_3.attribute_domain = 'POINT'
			or_socket_3.hide_value = True


			#initialize is_loop nodes
			#node Group Output
			group_output_3 = is_loop.nodes.new("NodeGroupOutput")
			group_output_3.name = "Group Output"
			group_output_3.is_active_output = True

			#node Group Input
			group_input_3 = is_loop.nodes.new("NodeGroupInput")
			group_input_3.name = "Group Input"

			#node MN_select_sec_struct.002
			mn_select_sec_struct_002_1 = is_loop.nodes.new("GeometryNodeGroup")
			mn_select_sec_struct_002_1.label = "Select Sec Struct"
			mn_select_sec_struct_002_1.name = "MN_select_sec_struct.002"
			mn_select_sec_struct_002_1.node_tree = _mn_select_sec_struct_id
			#Socket_1
			mn_select_sec_struct_002_1.inputs[2].default_value = 3




			#Set locations
			group_output_3.location = (267.00146484375, 0.0)
			group_input_3.location = (-200.0, 0.0)
			mn_select_sec_struct_002_1.location = (0.0, 0.0)

			#Set dimensions
			group_output_3.width, group_output_3.height = 140.0, 100.0
			group_input_3.width, group_input_3.height = 140.0, 100.0
			mn_select_sec_struct_002_1.width, mn_select_sec_struct_002_1.height = 217.00146484375, 100.0

			#initialize is_loop links
			#mn_select_sec_struct_002_1.Selection -> group_output_3.Selection
			is_loop.links.new(mn_select_sec_struct_002_1.outputs[0], group_output_3.inputs[0])
			#group_input_3.And -> mn_select_sec_struct_002_1.And
			is_loop.links.new(group_input_3.outputs[0], mn_select_sec_struct_002_1.inputs[0])
			#group_input_3.Or -> mn_select_sec_struct_002_1.Or
			is_loop.links.new(group_input_3.outputs[1], mn_select_sec_struct_002_1.inputs[1])
			#mn_select_sec_struct_002_1.Inverted -> group_output_3.Inverted
			is_loop.links.new(mn_select_sec_struct_002_1.outputs[1], group_output_3.inputs[1])
			return is_loop

		is_loop = is_loop_node_group()

		#initialize is_helix node group
		def is_helix_node_group():
			is_helix = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Is Helix")

			is_helix.color_tag = 'INPUT'
			is_helix.description = ""


			#is_helix interface
			#Socket Selection
			selection_socket_3 = is_helix.interface.new_socket(name = "Selection", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			selection_socket_3.attribute_domain = 'POINT'
			selection_socket_3.description = "Selected atoms form part of an helix"

			#Socket Inverted
			inverted_socket_4 = is_helix.interface.new_socket(name = "Inverted", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			inverted_socket_4.attribute_domain = 'POINT'

			#Socket And
			and_socket_4 = is_helix.interface.new_socket(name = "And", in_out='INPUT', socket_type = 'NodeSocketBool')
			and_socket_4.attribute_domain = 'POINT'
			and_socket_4.hide_value = True

			#Socket Or
			or_socket_4 = is_helix.interface.new_socket(name = "Or", in_out='INPUT', socket_type = 'NodeSocketBool')
			or_socket_4.attribute_domain = 'POINT'
			or_socket_4.hide_value = True


			#initialize is_helix nodes
			#node Group Output
			group_output_4 = is_helix.nodes.new("NodeGroupOutput")
			group_output_4.name = "Group Output"
			group_output_4.is_active_output = True

			#node Group Input
			group_input_4 = is_helix.nodes.new("NodeGroupInput")
			group_input_4.name = "Group Input"

			#node MN_select_sec_struct.002
			mn_select_sec_struct_002_2 = is_helix.nodes.new("GeometryNodeGroup")
			mn_select_sec_struct_002_2.label = "Select Sec Struct"
			mn_select_sec_struct_002_2.name = "MN_select_sec_struct.002"
			mn_select_sec_struct_002_2.node_tree = _mn_select_sec_struct_id
			#Socket_1
			mn_select_sec_struct_002_2.inputs[2].default_value = 1




			#Set locations
			group_output_4.location = (267.00146484375, 0.0)
			group_input_4.location = (-200.0, 0.0)
			mn_select_sec_struct_002_2.location = (0.0, 0.0)

			#Set dimensions
			group_output_4.width, group_output_4.height = 140.0, 100.0
			group_input_4.width, group_input_4.height = 140.0, 100.0
			mn_select_sec_struct_002_2.width, mn_select_sec_struct_002_2.height = 217.00146484375, 100.0

			#initialize is_helix links
			#mn_select_sec_struct_002_2.Selection -> group_output_4.Selection
			is_helix.links.new(mn_select_sec_struct_002_2.outputs[0], group_output_4.inputs[0])
			#group_input_4.And -> mn_select_sec_struct_002_2.And
			is_helix.links.new(group_input_4.outputs[0], mn_select_sec_struct_002_2.inputs[0])
			#group_input_4.Or -> mn_select_sec_struct_002_2.Or
			is_helix.links.new(group_input_4.outputs[1], mn_select_sec_struct_002_2.inputs[1])
			#mn_select_sec_struct_002_2.Inverted -> group_output_4.Inverted
			is_helix.links.new(mn_select_sec_struct_002_2.outputs[1], group_output_4.inputs[1])
			return is_helix

		is_helix = is_helix_node_group()

		#initialize _mn_select_sec_struct node group
		def _mn_select_sec_struct_node_group():
			_mn_select_sec_struct = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".MN_select_sec_struct")

			_mn_select_sec_struct.color_tag = 'NONE'
			_mn_select_sec_struct.description = ""


			#_mn_select_sec_struct interface
			#Socket Is Helix
			is_helix_socket = _mn_select_sec_struct.interface.new_socket(name = "Is Helix", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			is_helix_socket.attribute_domain = 'POINT'

			#Socket Is Sheet
			is_sheet_socket = _mn_select_sec_struct.interface.new_socket(name = "Is Sheet", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			is_sheet_socket.attribute_domain = 'POINT'

			#Socket Is Structured
			is_structured_socket = _mn_select_sec_struct.interface.new_socket(name = "Is Structured", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			is_structured_socket.attribute_domain = 'POINT'

			#Socket Is Loop
			is_loop_socket = _mn_select_sec_struct.interface.new_socket(name = "Is Loop", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			is_loop_socket.attribute_domain = 'POINT'

			#Socket And
			and_socket_5 = _mn_select_sec_struct.interface.new_socket(name = "And", in_out='INPUT', socket_type = 'NodeSocketBool')
			and_socket_5.attribute_domain = 'POINT'
			and_socket_5.hide_value = True


			#initialize _mn_select_sec_struct nodes
			#node Group.001
			group_001 = _mn_select_sec_struct.nodes.new("GeometryNodeGroup")
			group_001.name = "Group.001"
			group_001.node_tree = is_sheet
			#Socket_3
			group_001.inputs[1].default_value = False

			#node Group.002
			group_002 = _mn_select_sec_struct.nodes.new("GeometryNodeGroup")
			group_002.name = "Group.002"
			group_002.node_tree = is_loop
			#Socket_3
			group_002.inputs[1].default_value = False

			#node Group
			group_1 = _mn_select_sec_struct.nodes.new("GeometryNodeGroup")
			group_1.name = "Group"
			group_1.node_tree = is_helix
			#Socket_3
			group_1.inputs[1].default_value = False

			#node Boolean Math.001
			boolean_math_001_1 = _mn_select_sec_struct.nodes.new("FunctionNodeBooleanMath")
			boolean_math_001_1.name = "Boolean Math.001"
			boolean_math_001_1.hide = True
			boolean_math_001_1.operation = 'NOT'

			#node Group Output
			group_output_5 = _mn_select_sec_struct.nodes.new("NodeGroupOutput")
			group_output_5.name = "Group Output"
			group_output_5.is_active_output = True

			#node Group Input
			group_input_5 = _mn_select_sec_struct.nodes.new("NodeGroupInput")
			group_input_5.name = "Group Input"
			group_input_5.outputs[1].hide = True




			#Set locations
			group_001.location = (120.0, -60.0)
			group_002.location = (120.0, -180.0)
			group_1.location = (120.0, 60.0)
			boolean_math_001_1.location = (300.0, -140.0)
			group_output_5.location = (540.0, -60.0)
			group_input_5.location = (-160.0, -40.0)

			#Set dimensions
			group_001.width, group_001.height = 140.0, 100.0
			group_002.width, group_002.height = 140.0, 100.0
			group_1.width, group_1.height = 140.0, 100.0
			boolean_math_001_1.width, boolean_math_001_1.height = 140.0, 100.0
			group_output_5.width, group_output_5.height = 140.0, 100.0
			group_input_5.width, group_input_5.height = 140.0, 100.0

			#initialize _mn_select_sec_struct links
			#group_002.Selection -> group_output_5.Is Loop
			_mn_select_sec_struct.links.new(group_002.outputs[0], group_output_5.inputs[3])
			#group_002.Selection -> boolean_math_001_1.Boolean
			_mn_select_sec_struct.links.new(group_002.outputs[0], boolean_math_001_1.inputs[0])
			#boolean_math_001_1.Boolean -> group_output_5.Is Structured
			_mn_select_sec_struct.links.new(boolean_math_001_1.outputs[0], group_output_5.inputs[2])
			#group_1.Selection -> group_output_5.Is Helix
			_mn_select_sec_struct.links.new(group_1.outputs[0], group_output_5.inputs[0])
			#group_001.Selection -> group_output_5.Is Sheet
			_mn_select_sec_struct.links.new(group_001.outputs[0], group_output_5.inputs[1])
			#group_input_5.And -> group_1.And
			_mn_select_sec_struct.links.new(group_input_5.outputs[0], group_1.inputs[0])
			#group_input_5.And -> group_001.And
			_mn_select_sec_struct.links.new(group_input_5.outputs[0], group_001.inputs[0])
			#group_input_5.And -> group_002.And
			_mn_select_sec_struct.links.new(group_input_5.outputs[0], group_002.inputs[0])
			return _mn_select_sec_struct

		_mn_select_sec_struct = _mn_select_sec_struct_node_group()

		#initialize offset_boolean node group
		def offset_boolean_node_group():
			offset_boolean = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Offset Boolean")

			offset_boolean.color_tag = 'CONVERTER'
			offset_boolean.description = ""


			#offset_boolean interface
			#Socket Boolean
			boolean_socket_2 = offset_boolean.interface.new_socket(name = "Boolean", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			boolean_socket_2.attribute_domain = 'POINT'

			#Socket Index
			index_socket = offset_boolean.interface.new_socket(name = "Index", in_out='INPUT', socket_type = 'NodeSocketInt')
			index_socket.subtype = 'NONE'
			index_socket.default_value = 0
			index_socket.min_value = 0
			index_socket.max_value = 2147483647
			index_socket.attribute_domain = 'POINT'

			#Socket Boolean
			boolean_socket_3 = offset_boolean.interface.new_socket(name = "Boolean", in_out='INPUT', socket_type = 'NodeSocketBool')
			boolean_socket_3.attribute_domain = 'POINT'
			boolean_socket_3.hide_value = True

			#Socket Offset
			offset_socket = offset_boolean.interface.new_socket(name = "Offset", in_out='INPUT', socket_type = 'NodeSocketInt')
			offset_socket.subtype = 'NONE'
			offset_socket.default_value = 0
			offset_socket.min_value = -2147483647
			offset_socket.max_value = 2147483647
			offset_socket.attribute_domain = 'POINT'


			#initialize offset_boolean nodes
			#node Group Output
			group_output_6 = offset_boolean.nodes.new("NodeGroupOutput")
			group_output_6.name = "Group Output"
			group_output_6.is_active_output = True

			#node Group Input
			group_input_6 = offset_boolean.nodes.new("NodeGroupInput")
			group_input_6.name = "Group Input"

			#node Evaluate at Index
			evaluate_at_index = offset_boolean.nodes.new("GeometryNodeFieldAtIndex")
			evaluate_at_index.name = "Evaluate at Index"
			evaluate_at_index.data_type = 'BOOLEAN'
			evaluate_at_index.domain = 'POINT'

			#node Math
			math = offset_boolean.nodes.new("ShaderNodeMath")
			math.name = "Math"
			math.operation = 'ADD'
			math.use_clamp = False




			#Set locations
			group_output_6.location = (190.0, 0.0)
			group_input_6.location = (-344.3331298828125, -46.23834991455078)
			evaluate_at_index.location = (0.0, 0.0)
			math.location = (-160.0, 0.0)

			#Set dimensions
			group_output_6.width, group_output_6.height = 140.0, 100.0
			group_input_6.width, group_input_6.height = 140.0, 100.0
			evaluate_at_index.width, evaluate_at_index.height = 140.0, 100.0
			math.width, math.height = 140.0, 100.0

			#initialize offset_boolean links
			#evaluate_at_index.Value -> group_output_6.Boolean
			offset_boolean.links.new(evaluate_at_index.outputs[0], group_output_6.inputs[0])
			#group_input_6.Boolean -> evaluate_at_index.Value
			offset_boolean.links.new(group_input_6.outputs[1], evaluate_at_index.inputs[1])
			#group_input_6.Index -> math.Value
			offset_boolean.links.new(group_input_6.outputs[0], math.inputs[1])
			#math.Value -> evaluate_at_index.Index
			offset_boolean.links.new(math.outputs[0], evaluate_at_index.inputs[0])
			#group_input_6.Offset -> math.Value
			offset_boolean.links.new(group_input_6.outputs[2], math.inputs[0])
			return offset_boolean

		offset_boolean = offset_boolean_node_group()

		#initialize expand_boolean node group
		def expand_boolean_node_group():
			expand_boolean = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Expand Boolean")

			expand_boolean.color_tag = 'CONVERTER'
			expand_boolean.description = ""


			#expand_boolean interface
			#Socket Boolean
			boolean_socket_4 = expand_boolean.interface.new_socket(name = "Boolean", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			boolean_socket_4.attribute_domain = 'POINT'

			#Socket Boolean
			boolean_socket_5 = expand_boolean.interface.new_socket(name = "Boolean", in_out='INPUT', socket_type = 'NodeSocketBool')
			boolean_socket_5.attribute_domain = 'POINT'
			boolean_socket_5.hide_value = True

			#Socket Expand
			expand_socket = expand_boolean.interface.new_socket(name = "Expand", in_out='INPUT', socket_type = 'NodeSocketInt')
			expand_socket.subtype = 'NONE'
			expand_socket.default_value = 0
			expand_socket.min_value = -2147483647
			expand_socket.max_value = 2147483647
			expand_socket.attribute_domain = 'POINT'


			#initialize expand_boolean nodes
			#node Group Output
			group_output_7 = expand_boolean.nodes.new("NodeGroupOutput")
			group_output_7.name = "Group Output"
			group_output_7.is_active_output = True

			#node Group Input
			group_input_7 = expand_boolean.nodes.new("NodeGroupInput")
			group_input_7.name = "Group Input"

			#node Group.016
			group_016 = expand_boolean.nodes.new("GeometryNodeGroup")
			group_016.name = "Group.016"
			group_016.node_tree = offset_boolean
			#Socket_1
			group_016.inputs[0].default_value = 0

			#node Group.017
			group_017 = expand_boolean.nodes.new("GeometryNodeGroup")
			group_017.name = "Group.017"
			group_017.node_tree = offset_boolean
			#Socket_1
			group_017.inputs[0].default_value = 0

			#node Boolean Math
			boolean_math_1 = expand_boolean.nodes.new("FunctionNodeBooleanMath")
			boolean_math_1.name = "Boolean Math"
			boolean_math_1.operation = 'OR'

			#node Math
			math_1 = expand_boolean.nodes.new("ShaderNodeMath")
			math_1.name = "Math"
			math_1.operation = 'MULTIPLY'
			math_1.use_clamp = False
			#Value_001
			math_1.inputs[1].default_value = -1.0

			#node Boolean Math.001
			boolean_math_001_2 = expand_boolean.nodes.new("FunctionNodeBooleanMath")
			boolean_math_001_2.name = "Boolean Math.001"
			boolean_math_001_2.operation = 'OR'

			#node Reroute
			reroute_1 = expand_boolean.nodes.new("NodeReroute")
			reroute_1.name = "Reroute"
			#node Reroute.001
			reroute_001 = expand_boolean.nodes.new("NodeReroute")
			reroute_001.name = "Reroute.001"



			#Set locations
			group_output_7.location = (340.0, 80.0)
			group_input_7.location = (-640.0, 60.0)
			group_016.location = (-173.58670043945312, -14.669303894042969)
			group_017.location = (-180.0, -200.0)
			boolean_math_1.location = (-13.586694717407227, -14.669303894042969)
			math_1.location = (-400.0, -240.0)
			boolean_math_001_2.location = (159.99998474121094, 89.90420532226562)
			reroute_1.location = (-460.0, -180.0)
			reroute_001.location = (-300.0, 20.0)

			#Set dimensions
			group_output_7.width, group_output_7.height = 140.0, 100.0
			group_input_7.width, group_input_7.height = 140.0, 100.0
			group_016.width, group_016.height = 140.0, 100.0
			group_017.width, group_017.height = 140.0, 100.0
			boolean_math_1.width, boolean_math_1.height = 140.0, 100.0
			math_1.width, math_1.height = 140.0, 100.0
			boolean_math_001_2.width, boolean_math_001_2.height = 140.0, 100.0
			reroute_1.width, reroute_1.height = 16.0, 100.0
			reroute_001.width, reroute_001.height = 16.0, 100.0

			#initialize expand_boolean links
			#group_016.Boolean -> boolean_math_1.Boolean
			expand_boolean.links.new(group_016.outputs[0], boolean_math_1.inputs[0])
			#group_017.Boolean -> boolean_math_1.Boolean
			expand_boolean.links.new(group_017.outputs[0], boolean_math_1.inputs[1])
			#reroute_001.Output -> group_016.Boolean
			expand_boolean.links.new(reroute_001.outputs[0], group_016.inputs[1])
			#reroute_001.Output -> group_017.Boolean
			expand_boolean.links.new(reroute_001.outputs[0], group_017.inputs[1])
			#reroute_1.Output -> group_016.Offset
			expand_boolean.links.new(reroute_1.outputs[0], group_016.inputs[2])
			#reroute_1.Output -> math_1.Value
			expand_boolean.links.new(reroute_1.outputs[0], math_1.inputs[0])
			#math_1.Value -> group_017.Offset
			expand_boolean.links.new(math_1.outputs[0], group_017.inputs[2])
			#boolean_math_1.Boolean -> boolean_math_001_2.Boolean
			expand_boolean.links.new(boolean_math_1.outputs[0], boolean_math_001_2.inputs[1])
			#reroute_001.Output -> boolean_math_001_2.Boolean
			expand_boolean.links.new(reroute_001.outputs[0], boolean_math_001_2.inputs[0])
			#group_input_7.Expand -> reroute_1.Input
			expand_boolean.links.new(group_input_7.outputs[1], reroute_1.inputs[0])
			#group_input_7.Boolean -> reroute_001.Input
			expand_boolean.links.new(group_input_7.outputs[0], reroute_001.inputs[0])
			#boolean_math_001_2.Boolean -> group_output_7.Boolean
			expand_boolean.links.new(boolean_math_001_2.outputs[0], group_output_7.inputs[0])
			return expand_boolean

		expand_boolean = expand_boolean_node_group()

		#initialize _bs_smooth node group
		def _bs_smooth_node_group():
			_bs_smooth = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".bs_smooth")

			_bs_smooth.color_tag = 'NONE'
			_bs_smooth.description = ""

			_bs_smooth.is_modifier = True

			#_bs_smooth interface
			#Socket Geometry
			geometry_socket = _bs_smooth.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			geometry_socket.attribute_domain = 'POINT'

			#Socket Geometry
			geometry_socket_1 = _bs_smooth.interface.new_socket(name = "Geometry", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			geometry_socket_1.attribute_domain = 'POINT'

			#Socket Factor
			factor_socket = _bs_smooth.interface.new_socket(name = "Factor", in_out='INPUT', socket_type = 'NodeSocketFloat')
			factor_socket.subtype = 'FACTOR'
			factor_socket.default_value = 1.0
			factor_socket.min_value = 0.0
			factor_socket.max_value = 1.0
			factor_socket.attribute_domain = 'POINT'

			#Socket Iterations
			iterations_socket = _bs_smooth.interface.new_socket(name = "Iterations", in_out='INPUT', socket_type = 'NodeSocketInt')
			iterations_socket.subtype = 'NONE'
			iterations_socket.default_value = 2
			iterations_socket.min_value = 0
			iterations_socket.max_value = 2147483647
			iterations_socket.attribute_domain = 'POINT'


			#initialize _bs_smooth nodes
			#node Group Output
			group_output_8 = _bs_smooth.nodes.new("NodeGroupOutput")
			group_output_8.name = "Group Output"
			group_output_8.is_active_output = True

			#node Set Position
			set_position = _bs_smooth.nodes.new("GeometryNodeSetPosition")
			set_position.name = "Set Position"
			#Offset
			set_position.inputs[3].default_value = (0.0, 0.0, 0.0)

			#node Mix.002
			mix_002 = _bs_smooth.nodes.new("ShaderNodeMix")
			mix_002.name = "Mix.002"
			mix_002.blend_type = 'MIX'
			mix_002.clamp_factor = True
			mix_002.clamp_result = False
			mix_002.data_type = 'VECTOR'
			mix_002.factor_mode = 'UNIFORM'

			#node Position.001
			position_001 = _bs_smooth.nodes.new("GeometryNodeInputPosition")
			position_001.name = "Position.001"

			#node Blur Attribute
			blur_attribute = _bs_smooth.nodes.new("GeometryNodeBlurAttribute")
			blur_attribute.name = "Blur Attribute"
			blur_attribute.data_type = 'FLOAT_VECTOR'

			#node Group Input
			group_input_8 = _bs_smooth.nodes.new("NodeGroupInput")
			group_input_8.name = "Group Input"

			#node Group.021
			group_021 = _bs_smooth.nodes.new("GeometryNodeGroup")
			group_021.name = "Group.021"
			group_021.node_tree = _mn_select_sec_struct
			#Socket_1
			group_021.inputs[0].default_value = True

			#node Group
			group_2 = _bs_smooth.nodes.new("GeometryNodeGroup")
			group_2.name = "Group"
			group_2.node_tree = expand_boolean
			#Socket_2
			group_2.inputs[1].default_value = 1

			#node Boolean Math
			boolean_math_2 = _bs_smooth.nodes.new("FunctionNodeBooleanMath")
			boolean_math_2.name = "Boolean Math"
			boolean_math_2.operation = 'AND'

			#node Boolean Math.001
			boolean_math_001_3 = _bs_smooth.nodes.new("FunctionNodeBooleanMath")
			boolean_math_001_3.name = "Boolean Math.001"
			boolean_math_001_3.operation = 'OR'

			#node Group.001
			group_001_1 = _bs_smooth.nodes.new("GeometryNodeGroup")
			group_001_1.name = "Group.001"
			group_001_1.node_tree = expand_boolean
			#Socket_2
			group_001_1.inputs[1].default_value = 1




			#Set locations
			group_output_8.location = (600.0, 180.0)
			set_position.location = (240.384033203125, 199.23532104492188)
			mix_002.location = (-60.8000373840332, 140.0)
			position_001.location = (-300.0, 80.0)
			blur_attribute.location = (-300.0, 0.0)
			group_input_8.location = (-980.0, 40.0)
			group_021.location = (-980.0, 240.0)
			group_2.location = (-428.8221740722656, 207.7011260986328)
			boolean_math_2.location = (-365.695068359375, 403.17449951171875)
			boolean_math_001_3.location = (-113.1089859008789, 314.436767578125)
			group_001_1.location = (-659.4182739257812, 115.35264587402344)

			#Set dimensions
			group_output_8.width, group_output_8.height = 140.0, 100.0
			set_position.width, set_position.height = 140.0, 100.0
			mix_002.width, mix_002.height = 140.0, 100.0
			position_001.width, position_001.height = 140.0, 100.0
			blur_attribute.width, blur_attribute.height = 140.0, 100.0
			group_input_8.width, group_input_8.height = 140.0, 100.0
			group_021.width, group_021.height = 140.0, 100.0
			group_2.width, group_2.height = 140.0, 100.0
			boolean_math_2.width, boolean_math_2.height = 140.0, 100.0
			boolean_math_001_3.width, boolean_math_001_3.height = 140.0, 100.0
			group_001_1.width, group_001_1.height = 140.0, 100.0

			#initialize _bs_smooth links
			#blur_attribute.Value -> mix_002.B
			_bs_smooth.links.new(blur_attribute.outputs[0], mix_002.inputs[5])
			#position_001.Position -> blur_attribute.Value
			_bs_smooth.links.new(position_001.outputs[0], blur_attribute.inputs[0])
			#mix_002.Result -> set_position.Position
			_bs_smooth.links.new(mix_002.outputs[1], set_position.inputs[2])
			#position_001.Position -> mix_002.A
			_bs_smooth.links.new(position_001.outputs[0], mix_002.inputs[4])
			#group_input_8.Geometry -> set_position.Geometry
			_bs_smooth.links.new(group_input_8.outputs[0], set_position.inputs[0])
			#group_input_8.Factor -> mix_002.Factor
			_bs_smooth.links.new(group_input_8.outputs[1], mix_002.inputs[0])
			#set_position.Geometry -> group_output_8.Geometry
			_bs_smooth.links.new(set_position.outputs[0], group_output_8.inputs[0])
			#group_input_8.Iterations -> blur_attribute.Iterations
			_bs_smooth.links.new(group_input_8.outputs[2], blur_attribute.inputs[1])
			#group_021.Is Loop -> group_2.Boolean
			_bs_smooth.links.new(group_021.outputs[3], group_2.inputs[0])
			#group_021.Is Helix -> boolean_math_2.Boolean
			_bs_smooth.links.new(group_021.outputs[0], boolean_math_2.inputs[0])
			#group_2.Boolean -> boolean_math_2.Boolean
			_bs_smooth.links.new(group_2.outputs[0], boolean_math_2.inputs[1])
			#group_021.Is Sheet -> boolean_math_001_3.Boolean
			_bs_smooth.links.new(group_021.outputs[1], boolean_math_001_3.inputs[1])
			#boolean_math_2.Boolean -> boolean_math_001_3.Boolean
			_bs_smooth.links.new(boolean_math_2.outputs[0], boolean_math_001_3.inputs[0])
			#group_021.Is Structured -> group_001_1.Boolean
			_bs_smooth.links.new(group_021.outputs[2], group_001_1.inputs[0])
			#group_001_1.Boolean -> blur_attribute.Weight
			_bs_smooth.links.new(group_001_1.outputs[0], blur_attribute.inputs[2])
			#group_021.Is Sheet -> set_position.Selection
			_bs_smooth.links.new(group_021.outputs[1], set_position.inputs[1])
			return _bs_smooth

		_bs_smooth = _bs_smooth_node_group()

		#initialize fallback_boolean node group
		def fallback_boolean_node_group():
			fallback_boolean = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Fallback Boolean")

			fallback_boolean.color_tag = 'INPUT'
			fallback_boolean.description = "Computes the boolean field if the given attribute doesn't exist. If it doesn't exist it just uses the attribute instead"


			#fallback_boolean interface
			#Socket Boolean
			boolean_socket_6 = fallback_boolean.interface.new_socket(name = "Boolean", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			boolean_socket_6.attribute_domain = 'POINT'

			#Socket Name
			name_socket = fallback_boolean.interface.new_socket(name = "Name", in_out='INPUT', socket_type = 'NodeSocketString')
			name_socket.attribute_domain = 'POINT'

			#Socket Fallback
			fallback_socket = fallback_boolean.interface.new_socket(name = "Fallback", in_out='INPUT', socket_type = 'NodeSocketBool')
			fallback_socket.attribute_domain = 'POINT'


			#initialize fallback_boolean nodes
			#node Group Output
			group_output_9 = fallback_boolean.nodes.new("NodeGroupOutput")
			group_output_9.name = "Group Output"
			group_output_9.is_active_output = True

			#node Group Input
			group_input_9 = fallback_boolean.nodes.new("NodeGroupInput")
			group_input_9.name = "Group Input"

			#node Named Attribute
			named_attribute = fallback_boolean.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute.name = "Named Attribute"
			named_attribute.data_type = 'BOOLEAN'

			#node Switch
			switch = fallback_boolean.nodes.new("GeometryNodeSwitch")
			switch.name = "Switch"
			switch.input_type = 'BOOLEAN'




			#Set locations
			group_output_9.location = (276.6171569824219, 4.738137245178223)
			group_input_9.location = (-280.0, 0.0)
			named_attribute.location = (-94.73597717285156, 4.738137245178223)
			switch.location = (86.61715698242188, 4.738137245178223)

			#Set dimensions
			group_output_9.width, group_output_9.height = 140.0, 100.0
			group_input_9.width, group_input_9.height = 140.0, 100.0
			named_attribute.width, named_attribute.height = 140.0, 100.0
			switch.width, switch.height = 140.0, 100.0

			#initialize fallback_boolean links
			#named_attribute.Exists -> switch.Switch
			fallback_boolean.links.new(named_attribute.outputs[1], switch.inputs[0])
			#named_attribute.Attribute -> switch.True
			fallback_boolean.links.new(named_attribute.outputs[0], switch.inputs[2])
			#group_input_9.Fallback -> switch.False
			fallback_boolean.links.new(group_input_9.outputs[1], switch.inputs[1])
			#switch.Output -> group_output_9.Boolean
			fallback_boolean.links.new(switch.outputs[0], group_output_9.inputs[0])
			#group_input_9.Name -> named_attribute.Name
			fallback_boolean.links.new(group_input_9.outputs[0], named_attribute.inputs[0])
			return fallback_boolean

		fallback_boolean = fallback_boolean_node_group()

		#initialize _mn_constants_atom_name_peptide node group
		def _mn_constants_atom_name_peptide_node_group():
			_mn_constants_atom_name_peptide = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".MN_constants_atom_name_peptide")

			_mn_constants_atom_name_peptide.color_tag = 'NONE'
			_mn_constants_atom_name_peptide.description = ""


			#_mn_constants_atom_name_peptide interface
			#Socket Backbone Lower
			backbone_lower_socket = _mn_constants_atom_name_peptide.interface.new_socket(name = "Backbone Lower", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			backbone_lower_socket.subtype = 'NONE'
			backbone_lower_socket.default_value = 0
			backbone_lower_socket.min_value = -2147483648
			backbone_lower_socket.max_value = 2147483647
			backbone_lower_socket.attribute_domain = 'POINT'

			#Socket Backbone Upper
			backbone_upper_socket = _mn_constants_atom_name_peptide.interface.new_socket(name = "Backbone Upper", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			backbone_upper_socket.subtype = 'NONE'
			backbone_upper_socket.default_value = 0
			backbone_upper_socket.min_value = -2147483648
			backbone_upper_socket.max_value = 2147483647
			backbone_upper_socket.attribute_domain = 'POINT'

			#Socket Side Chain Lower
			side_chain_lower_socket = _mn_constants_atom_name_peptide.interface.new_socket(name = "Side Chain Lower", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			side_chain_lower_socket.subtype = 'NONE'
			side_chain_lower_socket.default_value = 0
			side_chain_lower_socket.min_value = -2147483648
			side_chain_lower_socket.max_value = 2147483647
			side_chain_lower_socket.attribute_domain = 'POINT'

			#Socket Side Chain Upper
			side_chain_upper_socket = _mn_constants_atom_name_peptide.interface.new_socket(name = "Side Chain Upper", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			side_chain_upper_socket.subtype = 'NONE'
			side_chain_upper_socket.default_value = 0
			side_chain_upper_socket.min_value = -2147483648
			side_chain_upper_socket.max_value = 2147483647
			side_chain_upper_socket.attribute_domain = 'POINT'

			#Socket Alpha Carbon
			alpha_carbon_socket = _mn_constants_atom_name_peptide.interface.new_socket(name = "Alpha Carbon", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			alpha_carbon_socket.subtype = 'NONE'
			alpha_carbon_socket.default_value = 0
			alpha_carbon_socket.min_value = -2147483648
			alpha_carbon_socket.max_value = 2147483647
			alpha_carbon_socket.attribute_domain = 'POINT'


			#initialize _mn_constants_atom_name_peptide nodes
			#node Group Input
			group_input_10 = _mn_constants_atom_name_peptide.nodes.new("NodeGroupInput")
			group_input_10.name = "Group Input"

			#node Group Output
			group_output_10 = _mn_constants_atom_name_peptide.nodes.new("NodeGroupOutput")
			group_output_10.name = "Group Output"
			group_output_10.is_active_output = True

			#node Integer.001
			integer_001 = _mn_constants_atom_name_peptide.nodes.new("FunctionNodeInputInt")
			integer_001.name = "Integer.001"
			integer_001.integer = 49

			#node Integer.004
			integer_004 = _mn_constants_atom_name_peptide.nodes.new("FunctionNodeInputInt")
			integer_004.name = "Integer.004"
			integer_004.integer = 2

			#node Integer
			integer = _mn_constants_atom_name_peptide.nodes.new("FunctionNodeInputInt")
			integer.name = "Integer"
			integer.integer = 5

			#node Integer.003
			integer_003 = _mn_constants_atom_name_peptide.nodes.new("FunctionNodeInputInt")
			integer_003.name = "Integer.003"
			integer_003.integer = 1

			#node Integer.002
			integer_002 = _mn_constants_atom_name_peptide.nodes.new("FunctionNodeInputInt")
			integer_002.name = "Integer.002"
			integer_002.integer = 4




			#Set locations
			group_input_10.location = (-200.0, 0.0)
			group_output_10.location = (260.0, 180.0)
			integer_001.location = (0.0, -50.0)
			integer_004.location = (0.0, -140.0)
			integer.location = (0.0, 40.0)
			integer_003.location = (0.0, 240.0)
			integer_002.location = (0.0, 140.0)

			#Set dimensions
			group_input_10.width, group_input_10.height = 140.0, 100.0
			group_output_10.width, group_output_10.height = 140.0, 100.0
			integer_001.width, integer_001.height = 140.0, 100.0
			integer_004.width, integer_004.height = 140.0, 100.0
			integer.width, integer.height = 140.0, 100.0
			integer_003.width, integer_003.height = 140.0, 100.0
			integer_002.width, integer_002.height = 140.0, 100.0

			#initialize _mn_constants_atom_name_peptide links
			#integer_003.Integer -> group_output_10.Backbone Lower
			_mn_constants_atom_name_peptide.links.new(integer_003.outputs[0], group_output_10.inputs[0])
			#integer_002.Integer -> group_output_10.Backbone Upper
			_mn_constants_atom_name_peptide.links.new(integer_002.outputs[0], group_output_10.inputs[1])
			#integer.Integer -> group_output_10.Side Chain Lower
			_mn_constants_atom_name_peptide.links.new(integer.outputs[0], group_output_10.inputs[2])
			#integer_001.Integer -> group_output_10.Side Chain Upper
			_mn_constants_atom_name_peptide.links.new(integer_001.outputs[0], group_output_10.inputs[3])
			#integer_004.Integer -> group_output_10.Alpha Carbon
			_mn_constants_atom_name_peptide.links.new(integer_004.outputs[0], group_output_10.inputs[4])
			return _mn_constants_atom_name_peptide

		_mn_constants_atom_name_peptide = _mn_constants_atom_name_peptide_node_group()

		#initialize _mn_select_peptide node group
		def _mn_select_peptide_node_group():
			_mn_select_peptide = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".MN_select_peptide")

			_mn_select_peptide.color_tag = 'NONE'
			_mn_select_peptide.description = ""


			#_mn_select_peptide interface
			#Socket Is Backbone
			is_backbone_socket = _mn_select_peptide.interface.new_socket(name = "Is Backbone", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			is_backbone_socket.attribute_domain = 'POINT'

			#Socket Is Side Chain
			is_side_chain_socket = _mn_select_peptide.interface.new_socket(name = "Is Side Chain", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			is_side_chain_socket.attribute_domain = 'POINT'

			#Socket Is Peptide
			is_peptide_socket = _mn_select_peptide.interface.new_socket(name = "Is Peptide", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			is_peptide_socket.attribute_domain = 'POINT'

			#Socket Is Alpha Carbon
			is_alpha_carbon_socket = _mn_select_peptide.interface.new_socket(name = "Is Alpha Carbon", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			is_alpha_carbon_socket.attribute_domain = 'POINT'


			#initialize _mn_select_peptide nodes
			#node Group Input
			group_input_11 = _mn_select_peptide.nodes.new("NodeGroupInput")
			group_input_11.name = "Group Input"

			#node Compare
			compare = _mn_select_peptide.nodes.new("FunctionNodeCompare")
			compare.name = "Compare"
			compare.data_type = 'INT'
			compare.mode = 'ELEMENT'
			compare.operation = 'GREATER_EQUAL'

			#node Compare.001
			compare_001 = _mn_select_peptide.nodes.new("FunctionNodeCompare")
			compare_001.name = "Compare.001"
			compare_001.data_type = 'INT'
			compare_001.mode = 'ELEMENT'
			compare_001.operation = 'LESS_EQUAL'

			#node Boolean Math.001
			boolean_math_001_4 = _mn_select_peptide.nodes.new("FunctionNodeBooleanMath")
			boolean_math_001_4.name = "Boolean Math.001"
			boolean_math_001_4.operation = 'AND'

			#node Compare.002
			compare_002 = _mn_select_peptide.nodes.new("FunctionNodeCompare")
			compare_002.name = "Compare.002"
			compare_002.data_type = 'INT'
			compare_002.mode = 'ELEMENT'
			compare_002.operation = 'GREATER_EQUAL'

			#node Compare.003
			compare_003 = _mn_select_peptide.nodes.new("FunctionNodeCompare")
			compare_003.name = "Compare.003"
			compare_003.data_type = 'INT'
			compare_003.mode = 'ELEMENT'
			compare_003.operation = 'LESS_EQUAL'

			#node Boolean Math.002
			boolean_math_002_1 = _mn_select_peptide.nodes.new("FunctionNodeBooleanMath")
			boolean_math_002_1.name = "Boolean Math.002"
			boolean_math_002_1.operation = 'AND'

			#node Compare.004
			compare_004 = _mn_select_peptide.nodes.new("FunctionNodeCompare")
			compare_004.name = "Compare.004"
			compare_004.data_type = 'INT'
			compare_004.mode = 'ELEMENT'
			compare_004.operation = 'GREATER_EQUAL'

			#node Named Attribute
			named_attribute_1 = _mn_select_peptide.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_1.name = "Named Attribute"
			named_attribute_1.data_type = 'INT'
			#Name
			named_attribute_1.inputs[0].default_value = "atom_name"

			#node Boolean Math.003
			boolean_math_003 = _mn_select_peptide.nodes.new("FunctionNodeBooleanMath")
			boolean_math_003.name = "Boolean Math.003"
			boolean_math_003.operation = 'AND'

			#node Group Output
			group_output_11 = _mn_select_peptide.nodes.new("NodeGroupOutput")
			group_output_11.name = "Group Output"
			group_output_11.is_active_output = True

			#node Compare.005
			compare_005 = _mn_select_peptide.nodes.new("FunctionNodeCompare")
			compare_005.name = "Compare.005"
			compare_005.data_type = 'INT'
			compare_005.mode = 'ELEMENT'
			compare_005.operation = 'LESS_EQUAL'

			#node Compare.006
			compare_006 = _mn_select_peptide.nodes.new("FunctionNodeCompare")
			compare_006.name = "Compare.006"
			compare_006.data_type = 'INT'
			compare_006.mode = 'ELEMENT'
			compare_006.operation = 'EQUAL'

			#node Group
			group_3 = _mn_select_peptide.nodes.new("GeometryNodeGroup")
			group_3.name = "Group"
			group_3.node_tree = _mn_constants_atom_name_peptide

			#node Boolean Math
			boolean_math_3 = _mn_select_peptide.nodes.new("FunctionNodeBooleanMath")
			boolean_math_3.name = "Boolean Math"
			boolean_math_3.operation = 'OR'




			#Set locations
			group_input_11.location = (-460.0, 0.0)
			compare.location = (80.0, 80.0)
			compare_001.location = (80.0, -80.0)
			boolean_math_001_4.location = (260.0, 80.0)
			compare_002.location = (80.0, -240.0)
			compare_003.location = (80.0, -400.0)
			boolean_math_002_1.location = (260.0, -240.0)
			compare_004.location = (80.0, -560.0)
			named_attribute_1.location = (-360.0, -480.0)
			boolean_math_003.location = (260.0, -560.0)
			group_output_11.location = (666.1161499023438, -263.7054748535156)
			compare_005.location = (80.0, -720.0)
			compare_006.location = (260.0, -380.0)
			group_3.location = (-411.24090576171875, -312.71807861328125)
			boolean_math_3.location = (420.0, -240.0)

			#Set dimensions
			group_input_11.width, group_input_11.height = 140.0, 100.0
			compare.width, compare.height = 140.0, 100.0
			compare_001.width, compare_001.height = 140.0, 100.0
			boolean_math_001_4.width, boolean_math_001_4.height = 140.0, 100.0
			compare_002.width, compare_002.height = 153.86517333984375, 100.0
			compare_003.width, compare_003.height = 153.86517333984375, 100.0
			boolean_math_002_1.width, boolean_math_002_1.height = 140.0, 100.0
			compare_004.width, compare_004.height = 140.0, 100.0
			named_attribute_1.width, named_attribute_1.height = 140.0, 100.0
			boolean_math_003.width, boolean_math_003.height = 140.0, 100.0
			group_output_11.width, group_output_11.height = 140.0, 100.0
			compare_005.width, compare_005.height = 140.0, 100.0
			compare_006.width, compare_006.height = 140.0, 100.0
			group_3.width, group_3.height = 369.1165771484375, 100.0
			boolean_math_3.width, boolean_math_3.height = 140.0, 100.0

			#initialize _mn_select_peptide links
			#compare_001.Result -> boolean_math_001_4.Boolean
			_mn_select_peptide.links.new(compare_001.outputs[0], boolean_math_001_4.inputs[1])
			#group_3.Backbone Lower -> compare.B
			_mn_select_peptide.links.new(group_3.outputs[0], compare.inputs[3])
			#named_attribute_1.Attribute -> compare.A
			_mn_select_peptide.links.new(named_attribute_1.outputs[0], compare.inputs[2])
			#compare.Result -> boolean_math_001_4.Boolean
			_mn_select_peptide.links.new(compare.outputs[0], boolean_math_001_4.inputs[0])
			#named_attribute_1.Attribute -> compare_001.A
			_mn_select_peptide.links.new(named_attribute_1.outputs[0], compare_001.inputs[2])
			#group_3.Backbone Upper -> compare_001.B
			_mn_select_peptide.links.new(group_3.outputs[1], compare_001.inputs[3])
			#boolean_math_001_4.Boolean -> group_output_11.Is Backbone
			_mn_select_peptide.links.new(boolean_math_001_4.outputs[0], group_output_11.inputs[0])
			#compare_003.Result -> boolean_math_002_1.Boolean
			_mn_select_peptide.links.new(compare_003.outputs[0], boolean_math_002_1.inputs[1])
			#named_attribute_1.Attribute -> compare_002.A
			_mn_select_peptide.links.new(named_attribute_1.outputs[0], compare_002.inputs[2])
			#compare_002.Result -> boolean_math_002_1.Boolean
			_mn_select_peptide.links.new(compare_002.outputs[0], boolean_math_002_1.inputs[0])
			#named_attribute_1.Attribute -> compare_003.A
			_mn_select_peptide.links.new(named_attribute_1.outputs[0], compare_003.inputs[2])
			#group_3.Side Chain Lower -> compare_002.B
			_mn_select_peptide.links.new(group_3.outputs[2], compare_002.inputs[3])
			#group_3.Side Chain Upper -> compare_003.B
			_mn_select_peptide.links.new(group_3.outputs[3], compare_003.inputs[3])
			#compare_005.Result -> boolean_math_003.Boolean
			_mn_select_peptide.links.new(compare_005.outputs[0], boolean_math_003.inputs[1])
			#named_attribute_1.Attribute -> compare_004.A
			_mn_select_peptide.links.new(named_attribute_1.outputs[0], compare_004.inputs[2])
			#compare_004.Result -> boolean_math_003.Boolean
			_mn_select_peptide.links.new(compare_004.outputs[0], boolean_math_003.inputs[0])
			#named_attribute_1.Attribute -> compare_005.A
			_mn_select_peptide.links.new(named_attribute_1.outputs[0], compare_005.inputs[2])
			#group_3.Backbone Lower -> compare_004.B
			_mn_select_peptide.links.new(group_3.outputs[0], compare_004.inputs[3])
			#group_3.Side Chain Upper -> compare_005.B
			_mn_select_peptide.links.new(group_3.outputs[3], compare_005.inputs[3])
			#boolean_math_003.Boolean -> group_output_11.Is Peptide
			_mn_select_peptide.links.new(boolean_math_003.outputs[0], group_output_11.inputs[2])
			#named_attribute_1.Attribute -> compare_006.A
			_mn_select_peptide.links.new(named_attribute_1.outputs[0], compare_006.inputs[2])
			#group_3.Alpha Carbon -> compare_006.B
			_mn_select_peptide.links.new(group_3.outputs[4], compare_006.inputs[3])
			#compare_006.Result -> group_output_11.Is Alpha Carbon
			_mn_select_peptide.links.new(compare_006.outputs[0], group_output_11.inputs[3])
			#boolean_math_002_1.Boolean -> boolean_math_3.Boolean
			_mn_select_peptide.links.new(boolean_math_002_1.outputs[0], boolean_math_3.inputs[0])
			#compare_006.Result -> boolean_math_3.Boolean
			_mn_select_peptide.links.new(compare_006.outputs[0], boolean_math_3.inputs[1])
			#boolean_math_3.Boolean -> group_output_11.Is Side Chain
			_mn_select_peptide.links.new(boolean_math_3.outputs[0], group_output_11.inputs[1])
			return _mn_select_peptide

		_mn_select_peptide = _mn_select_peptide_node_group()

		#initialize is_alpha_carbon node group
		def is_alpha_carbon_node_group():
			is_alpha_carbon = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Is Alpha Carbon")

			is_alpha_carbon.color_tag = 'INPUT'
			is_alpha_carbon.description = ""


			#is_alpha_carbon interface
			#Socket Selection
			selection_socket_4 = is_alpha_carbon.interface.new_socket(name = "Selection", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			selection_socket_4.attribute_domain = 'POINT'
			selection_socket_4.description = "True if atom is an alpha carbon of an amino acid"

			#Socket Inverted
			inverted_socket_5 = is_alpha_carbon.interface.new_socket(name = "Inverted", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			inverted_socket_5.attribute_domain = 'POINT'

			#Socket And
			and_socket_6 = is_alpha_carbon.interface.new_socket(name = "And", in_out='INPUT', socket_type = 'NodeSocketBool')
			and_socket_6.attribute_domain = 'POINT'
			and_socket_6.hide_value = True

			#Socket Or
			or_socket_5 = is_alpha_carbon.interface.new_socket(name = "Or", in_out='INPUT', socket_type = 'NodeSocketBool')
			or_socket_5.attribute_domain = 'POINT'
			or_socket_5.hide_value = True


			#initialize is_alpha_carbon nodes
			#node Group Output
			group_output_12 = is_alpha_carbon.nodes.new("NodeGroupOutput")
			group_output_12.name = "Group Output"
			group_output_12.is_active_output = True

			#node Group Input
			group_input_12 = is_alpha_carbon.nodes.new("NodeGroupInput")
			group_input_12.name = "Group Input"

			#node Group.001
			group_001_2 = is_alpha_carbon.nodes.new("GeometryNodeGroup")
			group_001_2.name = "Group.001"
			group_001_2.node_tree = fallback_boolean
			#Socket_2
			group_001_2.inputs[0].default_value = "is_alpha_carbon"

			#node Group.002
			group_002_1 = is_alpha_carbon.nodes.new("GeometryNodeGroup")
			group_002_1.name = "Group.002"
			group_002_1.node_tree = _mn_select_peptide
			group_002_1.outputs[0].hide = True
			group_002_1.outputs[1].hide = True
			group_002_1.outputs[2].hide = True

			#node Group
			group_4 = is_alpha_carbon.nodes.new("GeometryNodeGroup")
			group_4.name = "Group"
			group_4.node_tree = boolean_andor




			#Set locations
			group_output_12.location = (220.0, 0.0)
			group_input_12.location = (-200.0, 0.0)
			group_001_2.location = (-300.0, -160.0)
			group_002_1.location = (-500.0, -160.0)
			group_4.location = (20.0, 0.0)

			#Set dimensions
			group_output_12.width, group_output_12.height = 140.0, 100.0
			group_input_12.width, group_input_12.height = 140.0, 100.0
			group_001_2.width, group_001_2.height = 208.33343505859375, 100.0
			group_002_1.width, group_002_1.height = 170.44906616210938, 100.0
			group_4.width, group_4.height = 140.0, 100.0

			#initialize is_alpha_carbon links
			#group_002_1.Is Alpha Carbon -> group_001_2.Fallback
			is_alpha_carbon.links.new(group_002_1.outputs[3], group_001_2.inputs[1])
			#group_input_12.And -> group_4.And
			is_alpha_carbon.links.new(group_input_12.outputs[0], group_4.inputs[0])
			#group_input_12.Or -> group_4.Or
			is_alpha_carbon.links.new(group_input_12.outputs[1], group_4.inputs[1])
			#group_001_2.Boolean -> group_4.Boolean
			is_alpha_carbon.links.new(group_001_2.outputs[0], group_4.inputs[2])
			#group_4.Boolean -> group_output_12.Selection
			is_alpha_carbon.links.new(group_4.outputs[0], group_output_12.inputs[0])
			#group_4.Inverted -> group_output_12.Inverted
			is_alpha_carbon.links.new(group_4.outputs[1], group_output_12.inputs[1])
			return is_alpha_carbon

		is_alpha_carbon = is_alpha_carbon_node_group()

		#initialize group_pick node group
		def group_pick_node_group():
			group_pick = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Group Pick")

			group_pick.color_tag = 'INPUT'
			group_pick.description = ""


			#group_pick interface
			#Socket Is Valid
			is_valid_socket = group_pick.interface.new_socket(name = "Is Valid", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			is_valid_socket.attribute_domain = 'POINT'
			is_valid_socket.description = "Whether the pick is valid. Pick is only valid if a single item is picked in the Group ID"

			#Socket Index
			index_socket_1 = group_pick.interface.new_socket(name = "Index", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			index_socket_1.subtype = 'NONE'
			index_socket_1.default_value = 0
			index_socket_1.min_value = 0
			index_socket_1.max_value = 2147483647
			index_socket_1.attribute_domain = 'POINT'
			index_socket_1.description = "Index of picked item. Returns -1 if not a valid pick."

			#Socket Pick
			pick_socket = group_pick.interface.new_socket(name = "Pick", in_out='INPUT', socket_type = 'NodeSocketBool')
			pick_socket.attribute_domain = 'POINT'
			pick_socket.hide_value = True
			pick_socket.description = "True for the item to pick from the group. If number of picks is 0 or more than 1, not a valid pick"

			#Socket Group ID
			group_id_socket = group_pick.interface.new_socket(name = "Group ID", in_out='INPUT', socket_type = 'NodeSocketInt')
			group_id_socket.subtype = 'NONE'
			group_id_socket.default_value = 0
			group_id_socket.min_value = -2147483648
			group_id_socket.max_value = 2147483647
			group_id_socket.attribute_domain = 'POINT'
			group_id_socket.description = "Group ID inside which to pick the item"


			#initialize group_pick nodes
			#node Group Output
			group_output_13 = group_pick.nodes.new("NodeGroupOutput")
			group_output_13.name = "Group Output"
			group_output_13.is_active_output = True

			#node Group Input
			group_input_13 = group_pick.nodes.new("NodeGroupInput")
			group_input_13.name = "Group Input"

			#node Switch
			switch_1 = group_pick.nodes.new("GeometryNodeSwitch")
			switch_1.name = "Switch"
			switch_1.input_type = 'INT'
			#False
			switch_1.inputs[1].default_value = 0

			#node Index
			index = group_pick.nodes.new("GeometryNodeInputIndex")
			index.name = "Index"

			#node Accumulate Field
			accumulate_field = group_pick.nodes.new("GeometryNodeAccumulateField")
			accumulate_field.name = "Accumulate Field"
			accumulate_field.data_type = 'INT'
			accumulate_field.domain = 'POINT'

			#node Accumulate Field.002
			accumulate_field_002 = group_pick.nodes.new("GeometryNodeAccumulateField")
			accumulate_field_002.name = "Accumulate Field.002"
			accumulate_field_002.data_type = 'INT'
			accumulate_field_002.domain = 'POINT'

			#node Switch.001
			switch_001 = group_pick.nodes.new("GeometryNodeSwitch")
			switch_001.name = "Switch.001"
			switch_001.input_type = 'INT'
			#False
			switch_001.inputs[1].default_value = -1

			#node Compare.003
			compare_003_1 = group_pick.nodes.new("FunctionNodeCompare")
			compare_003_1.name = "Compare.003"
			compare_003_1.data_type = 'INT'
			compare_003_1.mode = 'ELEMENT'
			compare_003_1.operation = 'EQUAL'
			#B_INT
			compare_003_1.inputs[3].default_value = 1

			#node Reroute.001
			reroute_001_1 = group_pick.nodes.new("NodeReroute")
			reroute_001_1.name = "Reroute.001"
			#node Reroute.002
			reroute_002 = group_pick.nodes.new("NodeReroute")
			reroute_002.name = "Reroute.002"



			#Set locations
			group_output_13.location = (462.9173889160156, 0.0)
			group_input_13.location = (-472.9173889160156, 0.0)
			switch_1.location = (-120.0, -20.0)
			index.location = (-480.0, -120.0)
			accumulate_field.location = (60.0, -20.0)
			accumulate_field_002.location = (-120.0, 180.0)
			switch_001.location = (240.0, -20.0)
			compare_003_1.location = (60.0, 180.0)
			reroute_001_1.location = (-260.0, -100.0)
			reroute_002.location = (-260.0, -60.0)

			#Set dimensions
			group_output_13.width, group_output_13.height = 140.0, 100.0
			group_input_13.width, group_input_13.height = 140.0, 100.0
			switch_1.width, switch_1.height = 140.0, 100.0
			index.width, index.height = 140.0, 100.0
			accumulate_field.width, accumulate_field.height = 140.0, 100.0
			accumulate_field_002.width, accumulate_field_002.height = 140.0, 100.0
			switch_001.width, switch_001.height = 140.0, 100.0
			compare_003_1.width, compare_003_1.height = 138.9921875, 100.0
			reroute_001_1.width, reroute_001_1.height = 16.0, 100.0
			reroute_002.width, reroute_002.height = 16.0, 100.0

			#initialize group_pick links
			#switch_1.Output -> accumulate_field.Value
			group_pick.links.new(switch_1.outputs[0], accumulate_field.inputs[0])
			#compare_003_1.Result -> switch_001.Switch
			group_pick.links.new(compare_003_1.outputs[0], switch_001.inputs[0])
			#accumulate_field.Total -> switch_001.True
			group_pick.links.new(accumulate_field.outputs[2], switch_001.inputs[2])
			#reroute_001_1.Output -> accumulate_field.Group ID
			group_pick.links.new(reroute_001_1.outputs[0], accumulate_field.inputs[1])
			#reroute_001_1.Output -> accumulate_field_002.Group ID
			group_pick.links.new(reroute_001_1.outputs[0], accumulate_field_002.inputs[1])
			#reroute_002.Output -> switch_1.Switch
			group_pick.links.new(reroute_002.outputs[0], switch_1.inputs[0])
			#reroute_002.Output -> accumulate_field_002.Value
			group_pick.links.new(reroute_002.outputs[0], accumulate_field_002.inputs[0])
			#index.Index -> switch_1.True
			group_pick.links.new(index.outputs[0], switch_1.inputs[2])
			#accumulate_field_002.Total -> compare_003_1.A
			group_pick.links.new(accumulate_field_002.outputs[2], compare_003_1.inputs[2])
			#group_input_13.Group ID -> reroute_001_1.Input
			group_pick.links.new(group_input_13.outputs[1], reroute_001_1.inputs[0])
			#group_input_13.Pick -> reroute_002.Input
			group_pick.links.new(group_input_13.outputs[0], reroute_002.inputs[0])
			#switch_001.Output -> group_output_13.Index
			group_pick.links.new(switch_001.outputs[0], group_output_13.inputs[1])
			#compare_003_1.Result -> group_output_13.Is Valid
			group_pick.links.new(compare_003_1.outputs[0], group_output_13.inputs[0])
			return group_pick

		group_pick = group_pick_node_group()

		#initialize group_pick_vector node group
		def group_pick_vector_node_group():
			group_pick_vector = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Group Pick Vector")

			group_pick_vector.color_tag = 'INPUT'
			group_pick_vector.description = ""


			#group_pick_vector interface
			#Socket Is Valid
			is_valid_socket_1 = group_pick_vector.interface.new_socket(name = "Is Valid", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			is_valid_socket_1.attribute_domain = 'POINT'
			is_valid_socket_1.description = "The pick for this group is valid"

			#Socket Index
			index_socket_2 = group_pick_vector.interface.new_socket(name = "Index", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			index_socket_2.subtype = 'NONE'
			index_socket_2.default_value = 0
			index_socket_2.min_value = -2147483648
			index_socket_2.max_value = 2147483647
			index_socket_2.attribute_domain = 'POINT'
			index_socket_2.description = "Picked Index for the Group"

			#Socket Vector
			vector_socket = group_pick_vector.interface.new_socket(name = "Vector", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			vector_socket.subtype = 'NONE'
			vector_socket.default_value = (0.0, 0.0, 0.0)
			vector_socket.min_value = -3.4028234663852886e+38
			vector_socket.max_value = 3.4028234663852886e+38
			vector_socket.attribute_domain = 'POINT'
			vector_socket.description = "Picked vector for the group"

			#Socket Pick
			pick_socket_1 = group_pick_vector.interface.new_socket(name = "Pick", in_out='INPUT', socket_type = 'NodeSocketBool')
			pick_socket_1.attribute_domain = 'POINT'
			pick_socket_1.hide_value = True

			#Socket Group ID
			group_id_socket_1 = group_pick_vector.interface.new_socket(name = "Group ID", in_out='INPUT', socket_type = 'NodeSocketInt')
			group_id_socket_1.subtype = 'NONE'
			group_id_socket_1.default_value = 0
			group_id_socket_1.min_value = -2147483648
			group_id_socket_1.max_value = 2147483647
			group_id_socket_1.attribute_domain = 'POINT'

			#Socket Position
			position_socket = group_pick_vector.interface.new_socket(name = "Position", in_out='INPUT', socket_type = 'NodeSocketVector')
			position_socket.subtype = 'NONE'
			position_socket.default_value = (0.0, 0.0, 0.0)
			position_socket.min_value = -3.4028234663852886e+38
			position_socket.max_value = 3.4028234663852886e+38
			position_socket.attribute_domain = 'POINT'
			position_socket.description = "Vector field to pick vlaue for, defaults to Position"


			#initialize group_pick_vector nodes
			#node Group Output
			group_output_14 = group_pick_vector.nodes.new("NodeGroupOutput")
			group_output_14.name = "Group Output"
			group_output_14.is_active_output = True

			#node Group Input
			group_input_14 = group_pick_vector.nodes.new("NodeGroupInput")
			group_input_14.name = "Group Input"

			#node Evaluate at Index.001
			evaluate_at_index_001 = group_pick_vector.nodes.new("GeometryNodeFieldAtIndex")
			evaluate_at_index_001.name = "Evaluate at Index.001"
			evaluate_at_index_001.data_type = 'FLOAT_VECTOR'
			evaluate_at_index_001.domain = 'POINT'

			#node Switch.002
			switch_002 = group_pick_vector.nodes.new("GeometryNodeSwitch")
			switch_002.name = "Switch.002"
			switch_002.input_type = 'VECTOR'
			#False
			switch_002.inputs[1].default_value = (0.0, 0.0, 0.0)

			#node Group
			group_5 = group_pick_vector.nodes.new("GeometryNodeGroup")
			group_5.name = "Group"
			group_5.node_tree = group_pick




			#Set locations
			group_output_14.location = (-40.0, -20.0)
			group_input_14.location = (-740.0, -80.0)
			evaluate_at_index_001.location = (-380.0, -180.0)
			switch_002.location = (-220.0, -60.0)
			group_5.location = (-560.0, -20.0)

			#Set dimensions
			group_output_14.width, group_output_14.height = 140.0, 100.0
			group_input_14.width, group_input_14.height = 140.0, 100.0
			evaluate_at_index_001.width, evaluate_at_index_001.height = 132.09918212890625, 100.0
			switch_002.width, switch_002.height = 140.0, 100.0
			group_5.width, group_5.height = 140.0, 100.0

			#initialize group_pick_vector links
			#group_5.Is Valid -> switch_002.Switch
			group_pick_vector.links.new(group_5.outputs[0], switch_002.inputs[0])
			#group_5.Index -> evaluate_at_index_001.Index
			group_pick_vector.links.new(group_5.outputs[1], evaluate_at_index_001.inputs[0])
			#evaluate_at_index_001.Value -> switch_002.True
			group_pick_vector.links.new(evaluate_at_index_001.outputs[0], switch_002.inputs[2])
			#group_5.Index -> group_output_14.Index
			group_pick_vector.links.new(group_5.outputs[1], group_output_14.inputs[1])
			#group_5.Is Valid -> group_output_14.Is Valid
			group_pick_vector.links.new(group_5.outputs[0], group_output_14.inputs[0])
			#switch_002.Output -> group_output_14.Vector
			group_pick_vector.links.new(switch_002.outputs[0], group_output_14.inputs[2])
			#group_input_14.Group ID -> group_5.Group ID
			group_pick_vector.links.new(group_input_14.outputs[1], group_5.inputs[1])
			#group_input_14.Pick -> group_5.Pick
			group_pick_vector.links.new(group_input_14.outputs[0], group_5.inputs[0])
			#group_input_14.Position -> evaluate_at_index_001.Value
			group_pick_vector.links.new(group_input_14.outputs[2], evaluate_at_index_001.inputs[1])
			return group_pick_vector

		group_pick_vector = group_pick_vector_node_group()

		#initialize offset_integer node group
		def offset_integer_node_group():
			offset_integer = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Offset Integer")

			offset_integer.color_tag = 'CONVERTER'
			offset_integer.description = ""


			#offset_integer interface
			#Socket Value
			value_socket = offset_integer.interface.new_socket(name = "Value", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			value_socket.subtype = 'NONE'
			value_socket.default_value = 0
			value_socket.min_value = -2147483648
			value_socket.max_value = 2147483647
			value_socket.attribute_domain = 'POINT'

			#Socket Index
			index_socket_3 = offset_integer.interface.new_socket(name = "Index", in_out='INPUT', socket_type = 'NodeSocketInt')
			index_socket_3.subtype = 'NONE'
			index_socket_3.default_value = 0
			index_socket_3.min_value = 0
			index_socket_3.max_value = 2147483647
			index_socket_3.attribute_domain = 'POINT'

			#Socket Value
			value_socket_1 = offset_integer.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketInt')
			value_socket_1.subtype = 'NONE'
			value_socket_1.default_value = 0
			value_socket_1.min_value = -2147483648
			value_socket_1.max_value = 2147483647
			value_socket_1.attribute_domain = 'POINT'
			value_socket_1.hide_value = True

			#Socket Offset
			offset_socket_1 = offset_integer.interface.new_socket(name = "Offset", in_out='INPUT', socket_type = 'NodeSocketInt')
			offset_socket_1.subtype = 'NONE'
			offset_socket_1.default_value = 0
			offset_socket_1.min_value = -2147483648
			offset_socket_1.max_value = 2147483647
			offset_socket_1.attribute_domain = 'POINT'


			#initialize offset_integer nodes
			#node Group Output
			group_output_15 = offset_integer.nodes.new("NodeGroupOutput")
			group_output_15.name = "Group Output"
			group_output_15.is_active_output = True

			#node Group Input
			group_input_15 = offset_integer.nodes.new("NodeGroupInput")
			group_input_15.name = "Group Input"

			#node Evaluate at Index
			evaluate_at_index_1 = offset_integer.nodes.new("GeometryNodeFieldAtIndex")
			evaluate_at_index_1.name = "Evaluate at Index"
			evaluate_at_index_1.data_type = 'INT'
			evaluate_at_index_1.domain = 'POINT'

			#node Math
			math_2 = offset_integer.nodes.new("ShaderNodeMath")
			math_2.name = "Math"
			math_2.operation = 'ADD'
			math_2.use_clamp = False




			#Set locations
			group_output_15.location = (100.0, 0.0)
			group_input_15.location = (-400.0, 0.0)
			evaluate_at_index_1.location = (-60.0, 0.0)
			math_2.location = (-220.0, 0.0)

			#Set dimensions
			group_output_15.width, group_output_15.height = 140.0, 100.0
			group_input_15.width, group_input_15.height = 140.0, 100.0
			evaluate_at_index_1.width, evaluate_at_index_1.height = 140.0, 100.0
			math_2.width, math_2.height = 140.0, 100.0

			#initialize offset_integer links
			#evaluate_at_index_1.Value -> group_output_15.Value
			offset_integer.links.new(evaluate_at_index_1.outputs[0], group_output_15.inputs[0])
			#group_input_15.Index -> math_2.Value
			offset_integer.links.new(group_input_15.outputs[0], math_2.inputs[0])
			#group_input_15.Offset -> math_2.Value
			offset_integer.links.new(group_input_15.outputs[2], math_2.inputs[1])
			#math_2.Value -> evaluate_at_index_1.Index
			offset_integer.links.new(math_2.outputs[0], evaluate_at_index_1.inputs[0])
			#group_input_15.Value -> evaluate_at_index_1.Value
			offset_integer.links.new(group_input_15.outputs[1], evaluate_at_index_1.inputs[1])
			return offset_integer

		offset_integer = offset_integer_node_group()

		#initialize res_group_id node group
		def res_group_id_node_group():
			res_group_id = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Res Group ID")

			res_group_id.color_tag = 'INPUT'
			res_group_id.description = ""


			#res_group_id interface
			#Socket Unique Group ID
			unique_group_id_socket = res_group_id.interface.new_socket(name = "Unique Group ID", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			unique_group_id_socket.subtype = 'NONE'
			unique_group_id_socket.default_value = 0
			unique_group_id_socket.min_value = -2147483648
			unique_group_id_socket.max_value = 2147483647
			unique_group_id_socket.attribute_domain = 'POINT'
			unique_group_id_socket.description = "A unique Group ID for eash residue"


			#initialize res_group_id nodes
			#node Group Output
			group_output_16 = res_group_id.nodes.new("NodeGroupOutput")
			group_output_16.name = "Group Output"
			group_output_16.is_active_output = True

			#node Group Input
			group_input_16 = res_group_id.nodes.new("NodeGroupInput")
			group_input_16.name = "Group Input"

			#node Named Attribute.001
			named_attribute_001 = res_group_id.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_001.name = "Named Attribute.001"
			named_attribute_001.data_type = 'INT'
			#Name
			named_attribute_001.inputs[0].default_value = "res_id"

			#node Named Attribute.002
			named_attribute_002_1 = res_group_id.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_002_1.name = "Named Attribute.002"
			named_attribute_002_1.data_type = 'INT'
			#Name
			named_attribute_002_1.inputs[0].default_value = "atom_name"

			#node Compare.002
			compare_002_1 = res_group_id.nodes.new("FunctionNodeCompare")
			compare_002_1.name = "Compare.002"
			compare_002_1.data_type = 'INT'
			compare_002_1.mode = 'ELEMENT'
			compare_002_1.operation = 'EQUAL'
			#B_INT
			compare_002_1.inputs[3].default_value = 1

			#node Compare.001
			compare_001_1 = res_group_id.nodes.new("FunctionNodeCompare")
			compare_001_1.name = "Compare.001"
			compare_001_1.data_type = 'INT'
			compare_001_1.mode = 'ELEMENT'
			compare_001_1.operation = 'NOT_EQUAL'

			#node Boolean Math
			boolean_math_4 = res_group_id.nodes.new("FunctionNodeBooleanMath")
			boolean_math_4.name = "Boolean Math"
			boolean_math_4.operation = 'OR'

			#node Accumulate Field.001
			accumulate_field_001 = res_group_id.nodes.new("GeometryNodeAccumulateField")
			accumulate_field_001.name = "Accumulate Field.001"
			accumulate_field_001.data_type = 'INT'
			accumulate_field_001.domain = 'POINT'
			#Group Index
			accumulate_field_001.inputs[1].default_value = 0

			#node Group.001
			group_001_3 = res_group_id.nodes.new("GeometryNodeGroup")
			group_001_3.name = "Group.001"
			group_001_3.node_tree = offset_integer
			#Socket_1
			group_001_3.inputs[0].default_value = 0
			#Socket_2
			group_001_3.inputs[2].default_value = -1

			#node Math
			math_3 = res_group_id.nodes.new("ShaderNodeMath")
			math_3.name = "Math"
			math_3.operation = 'SUBTRACT'
			math_3.use_clamp = False
			#Value_001
			math_3.inputs[1].default_value = 1.0

			#node Frame
			frame = res_group_id.nodes.new("NodeFrame")
			frame.name = "Frame"
			frame.label_size = 20
			frame.shrink = True

			#node Reroute
			reroute_2 = res_group_id.nodes.new("NodeReroute")
			reroute_2.label = "subtracting 1 from the leading, but things don't work right"
			reroute_2.name = "Reroute"
			#node Reroute.001
			reroute_001_2 = res_group_id.nodes.new("NodeReroute")
			reroute_001_2.name = "Reroute.001"
			#node Reroute.002
			reroute_002_1 = res_group_id.nodes.new("NodeReroute")
			reroute_002_1.label = "In theory we can just use the trailing value instead of"
			reroute_002_1.name = "Reroute.002"
			#node Reroute.003
			reroute_003 = res_group_id.nodes.new("NodeReroute")
			reroute_003.name = "Reroute.003"


			#Set parents
			math_3.parent = frame
			reroute_2.parent = frame
			reroute_001_2.parent = frame
			reroute_002_1.parent = frame
			reroute_003.parent = frame

			#Set locations
			group_output_16.location = (900.0, 160.0)
			group_input_16.location = (-420.0, 160.0)
			named_attribute_001.location = (-240.0, 0.0)
			named_attribute_002_1.location = (-250.0, 160.0)
			compare_002_1.location = (-70.0, 160.0)
			compare_001_1.location = (-70.0, 0.0)
			boolean_math_4.location = (90.0, 160.0)
			accumulate_field_001.location = (250.0, 160.0)
			group_001_3.location = (-70.0, -160.0)
			math_3.location = (519.2361450195312, 166.28671264648438)
			frame.location = (95.0, -20.0)
			reroute_2.location = (554.4125366210938, 257.9646911621094)
			reroute_001_2.location = (739.2361450195312, 306.2867126464844)
			reroute_002_1.location = (551.13134765625, 297.3444519042969)
			reroute_003.location = (379.23614501953125, 306.2867126464844)

			#Set dimensions
			group_output_16.width, group_output_16.height = 140.0, 100.0
			group_input_16.width, group_input_16.height = 140.0, 100.0
			named_attribute_001.width, named_attribute_001.height = 140.0, 100.0
			named_attribute_002_1.width, named_attribute_002_1.height = 140.0, 100.0
			compare_002_1.width, compare_002_1.height = 140.0, 100.0
			compare_001_1.width, compare_001_1.height = 140.0, 100.0
			boolean_math_4.width, boolean_math_4.height = 140.0, 100.0
			accumulate_field_001.width, accumulate_field_001.height = 140.0, 100.0
			group_001_3.width, group_001_3.height = 140.0, 100.0
			math_3.width, math_3.height = 140.0, 100.0
			frame.width, frame.height = 436.0, 356.2867126464844
			reroute_2.width, reroute_2.height = 16.0, 100.0
			reroute_001_2.width, reroute_001_2.height = 16.0, 100.0
			reroute_002_1.width, reroute_002_1.height = 16.0, 100.0
			reroute_003.width, reroute_003.height = 16.0, 100.0

			#initialize res_group_id links
			#compare_002_1.Result -> boolean_math_4.Boolean
			res_group_id.links.new(compare_002_1.outputs[0], boolean_math_4.inputs[0])
			#named_attribute_001.Attribute -> compare_001_1.A
			res_group_id.links.new(named_attribute_001.outputs[0], compare_001_1.inputs[2])
			#named_attribute_001.Attribute -> group_001_3.Value
			res_group_id.links.new(named_attribute_001.outputs[0], group_001_3.inputs[1])
			#compare_001_1.Result -> boolean_math_4.Boolean
			res_group_id.links.new(compare_001_1.outputs[0], boolean_math_4.inputs[1])
			#named_attribute_002_1.Attribute -> compare_002_1.A
			res_group_id.links.new(named_attribute_002_1.outputs[0], compare_002_1.inputs[2])
			#group_001_3.Value -> compare_001_1.B
			res_group_id.links.new(group_001_3.outputs[0], compare_001_1.inputs[3])
			#accumulate_field_001.Leading -> math_3.Value
			res_group_id.links.new(accumulate_field_001.outputs[0], math_3.inputs[0])
			#math_3.Value -> group_output_16.Unique Group ID
			res_group_id.links.new(math_3.outputs[0], group_output_16.inputs[0])
			#boolean_math_4.Boolean -> accumulate_field_001.Value
			res_group_id.links.new(boolean_math_4.outputs[0], accumulate_field_001.inputs[0])
			return res_group_id

		res_group_id = res_group_id_node_group()

		#initialize residue_mask node group
		def residue_mask_node_group():
			residue_mask = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Residue Mask")

			residue_mask.color_tag = 'INPUT'
			residue_mask.description = ""


			#residue_mask interface
			#Socket Is Valid
			is_valid_socket_2 = residue_mask.interface.new_socket(name = "Is Valid", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			is_valid_socket_2.attribute_domain = 'POINT'
			is_valid_socket_2.description = "Group contains only one occurrance of the selected atom. None or more than one returns False"

			#Socket Index
			index_socket_4 = residue_mask.interface.new_socket(name = "Index", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			index_socket_4.subtype = 'NONE'
			index_socket_4.default_value = 0
			index_socket_4.min_value = -2147483648
			index_socket_4.max_value = 2147483647
			index_socket_4.attribute_domain = 'POINT'
			index_socket_4.description = "Index for the group's atom with specified name, returns -1 if not valid"

			#Socket Position
			position_socket_1 = residue_mask.interface.new_socket(name = "Position", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			position_socket_1.subtype = 'NONE'
			position_socket_1.default_value = (0.0, 0.0, 0.0)
			position_socket_1.min_value = -3.4028234663852886e+38
			position_socket_1.max_value = 3.4028234663852886e+38
			position_socket_1.attribute_domain = 'POINT'
			position_socket_1.description = "Position of the picked point in the group, returns (0, 0, 0) if not valid"

			#Socket Group ID
			group_id_socket_2 = residue_mask.interface.new_socket(name = "Group ID", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			group_id_socket_2.subtype = 'NONE'
			group_id_socket_2.default_value = 0
			group_id_socket_2.min_value = -2147483648
			group_id_socket_2.max_value = 2147483647
			group_id_socket_2.attribute_domain = 'POINT'

			#Socket atom_name
			atom_name_socket = residue_mask.interface.new_socket(name = "atom_name", in_out='INPUT', socket_type = 'NodeSocketInt')
			atom_name_socket.subtype = 'NONE'
			atom_name_socket.default_value = 1
			atom_name_socket.min_value = 2
			atom_name_socket.max_value = 2147483647
			atom_name_socket.attribute_domain = 'POINT'
			atom_name_socket.description = "Atom to pick from the group"

			#Socket Use Fallback
			use_fallback_socket = residue_mask.interface.new_socket(name = "Use Fallback", in_out='INPUT', socket_type = 'NodeSocketBool')
			use_fallback_socket.attribute_domain = 'POINT'
			use_fallback_socket.description = "Uses a calculated Unique Group ID as a fallback. Disabling can increase performance if pre-computing a Group ID for multiple nodes"

			#Socket Group ID
			group_id_socket_3 = residue_mask.interface.new_socket(name = "Group ID", in_out='INPUT', socket_type = 'NodeSocketInt')
			group_id_socket_3.subtype = 'NONE'
			group_id_socket_3.default_value = 0
			group_id_socket_3.min_value = -2147483648
			group_id_socket_3.max_value = 2147483647
			group_id_socket_3.attribute_domain = 'POINT'


			#initialize residue_mask nodes
			#node Compare
			compare_1 = residue_mask.nodes.new("FunctionNodeCompare")
			compare_1.name = "Compare"
			compare_1.data_type = 'INT'
			compare_1.mode = 'ELEMENT'
			compare_1.operation = 'EQUAL'

			#node Group Input
			group_input_17 = residue_mask.nodes.new("NodeGroupInput")
			group_input_17.name = "Group Input"

			#node Named Attribute
			named_attribute_2 = residue_mask.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_2.name = "Named Attribute"
			named_attribute_2.data_type = 'INT'
			#Name
			named_attribute_2.inputs[0].default_value = "atom_name"

			#node Group Output
			group_output_17 = residue_mask.nodes.new("NodeGroupOutput")
			group_output_17.name = "Group Output"
			group_output_17.is_active_output = True

			#node Group
			group_6 = residue_mask.nodes.new("GeometryNodeGroup")
			group_6.name = "Group"
			group_6.node_tree = group_pick_vector
			#Socket_5
			group_6.inputs[2].default_value = (0.0, 0.0, 0.0)

			#node Group.002
			group_002_2 = residue_mask.nodes.new("GeometryNodeGroup")
			group_002_2.name = "Group.002"
			group_002_2.node_tree = res_group_id

			#node Switch
			switch_2 = residue_mask.nodes.new("GeometryNodeSwitch")
			switch_2.name = "Switch"
			switch_2.input_type = 'INT'




			#Set locations
			compare_1.location = (40.0, 340.0)
			group_input_17.location = (-140.0, 200.0)
			named_attribute_2.location = (-140.0, 340.0)
			group_output_17.location = (420.0, 340.0)
			group_6.location = (220.0, 340.0)
			group_002_2.location = (-140.0, 60.0)
			switch_2.location = (40.0, 180.0)

			#Set dimensions
			compare_1.width, compare_1.height = 140.0, 100.0
			group_input_17.width, group_input_17.height = 140.0, 100.0
			named_attribute_2.width, named_attribute_2.height = 140.0, 100.0
			group_output_17.width, group_output_17.height = 140.0, 100.0
			group_6.width, group_6.height = 164.60528564453125, 100.0
			group_002_2.width, group_002_2.height = 140.0, 100.0
			switch_2.width, switch_2.height = 140.0, 100.0

			#initialize residue_mask links
			#named_attribute_2.Attribute -> compare_1.A
			residue_mask.links.new(named_attribute_2.outputs[0], compare_1.inputs[2])
			#group_input_17.atom_name -> compare_1.B
			residue_mask.links.new(group_input_17.outputs[0], compare_1.inputs[3])
			#group_6.Index -> group_output_17.Index
			residue_mask.links.new(group_6.outputs[1], group_output_17.inputs[1])
			#group_6.Vector -> group_output_17.Position
			residue_mask.links.new(group_6.outputs[2], group_output_17.inputs[2])
			#group_6.Is Valid -> group_output_17.Is Valid
			residue_mask.links.new(group_6.outputs[0], group_output_17.inputs[0])
			#compare_1.Result -> group_6.Pick
			residue_mask.links.new(compare_1.outputs[0], group_6.inputs[0])
			#group_input_17.Use Fallback -> switch_2.Switch
			residue_mask.links.new(group_input_17.outputs[1], switch_2.inputs[0])
			#group_input_17.Group ID -> switch_2.False
			residue_mask.links.new(group_input_17.outputs[2], switch_2.inputs[1])
			#switch_2.Output -> group_6.Group ID
			residue_mask.links.new(switch_2.outputs[0], group_6.inputs[1])
			#group_002_2.Unique Group ID -> switch_2.True
			residue_mask.links.new(group_002_2.outputs[0], switch_2.inputs[2])
			#switch_2.Output -> group_output_17.Group ID
			residue_mask.links.new(switch_2.outputs[0], group_output_17.inputs[3])
			return residue_mask

		residue_mask = residue_mask_node_group()

		#initialize _mn_topo_assign_backbone node group
		def _mn_topo_assign_backbone_node_group():
			_mn_topo_assign_backbone = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".MN_topo_assign_backbone")

			_mn_topo_assign_backbone.color_tag = 'NONE'
			_mn_topo_assign_backbone.description = ""


			#_mn_topo_assign_backbone interface
			#Socket Atoms
			atoms_socket = _mn_topo_assign_backbone.interface.new_socket(name = "Atoms", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			atoms_socket.attribute_domain = 'POINT'

			#Socket Unique Group ID
			unique_group_id_socket_1 = _mn_topo_assign_backbone.interface.new_socket(name = "Unique Group ID", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			unique_group_id_socket_1.subtype = 'NONE'
			unique_group_id_socket_1.default_value = 0
			unique_group_id_socket_1.min_value = -2147483648
			unique_group_id_socket_1.max_value = 2147483647
			unique_group_id_socket_1.attribute_domain = 'POINT'

			#Socket CA Atoms
			ca_atoms_socket = _mn_topo_assign_backbone.interface.new_socket(name = "CA Atoms", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			ca_atoms_socket.attribute_domain = 'POINT'

			#Socket Atoms
			atoms_socket_1 = _mn_topo_assign_backbone.interface.new_socket(name = "Atoms", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			atoms_socket_1.attribute_domain = 'POINT'


			#initialize _mn_topo_assign_backbone nodes
			#node Group Output
			group_output_18 = _mn_topo_assign_backbone.nodes.new("NodeGroupOutput")
			group_output_18.name = "Group Output"
			group_output_18.is_active_output = True

			#node Group Input
			group_input_18 = _mn_topo_assign_backbone.nodes.new("NodeGroupInput")
			group_input_18.name = "Group Input"

			#node Store Named Attribute.002
			store_named_attribute_002 = _mn_topo_assign_backbone.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_002.name = "Store Named Attribute.002"
			store_named_attribute_002.data_type = 'FLOAT_VECTOR'
			store_named_attribute_002.domain = 'POINT'
			#Name
			store_named_attribute_002.inputs[2].default_value = "backbone_N"

			#node Store Named Attribute.003
			store_named_attribute_003 = _mn_topo_assign_backbone.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_003.name = "Store Named Attribute.003"
			store_named_attribute_003.data_type = 'FLOAT_VECTOR'
			store_named_attribute_003.domain = 'POINT'
			#Name
			store_named_attribute_003.inputs[2].default_value = "backbone_C"

			#node Store Named Attribute.004
			store_named_attribute_004 = _mn_topo_assign_backbone.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_004.name = "Store Named Attribute.004"
			store_named_attribute_004.data_type = 'FLOAT_VECTOR'
			store_named_attribute_004.domain = 'POINT'
			#Name
			store_named_attribute_004.inputs[2].default_value = "backbone_CA"

			#node Store Named Attribute.005
			store_named_attribute_005 = _mn_topo_assign_backbone.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_005.name = "Store Named Attribute.005"
			store_named_attribute_005.data_type = 'FLOAT_VECTOR'
			store_named_attribute_005.domain = 'POINT'
			#Name
			store_named_attribute_005.inputs[2].default_value = "backbone_O"

			#node MN_topo_point_mask.005
			mn_topo_point_mask_005 = _mn_topo_assign_backbone.nodes.new("GeometryNodeGroup")
			mn_topo_point_mask_005.label = "Topology Point Mask"
			mn_topo_point_mask_005.name = "MN_topo_point_mask.005"
			mn_topo_point_mask_005.node_tree = residue_mask
			#Socket_1
			mn_topo_point_mask_005.inputs[0].default_value = 3
			#Socket_5
			mn_topo_point_mask_005.inputs[1].default_value = False

			#node MN_topo_point_mask.006
			mn_topo_point_mask_006 = _mn_topo_assign_backbone.nodes.new("GeometryNodeGroup")
			mn_topo_point_mask_006.label = "Topology Point Mask"
			mn_topo_point_mask_006.name = "MN_topo_point_mask.006"
			mn_topo_point_mask_006.node_tree = residue_mask
			#Socket_1
			mn_topo_point_mask_006.inputs[0].default_value = 2
			#Socket_5
			mn_topo_point_mask_006.inputs[1].default_value = False

			#node MN_topo_point_mask.007
			mn_topo_point_mask_007 = _mn_topo_assign_backbone.nodes.new("GeometryNodeGroup")
			mn_topo_point_mask_007.label = "Topology Point Mask"
			mn_topo_point_mask_007.name = "MN_topo_point_mask.007"
			mn_topo_point_mask_007.node_tree = residue_mask
			#Socket_1
			mn_topo_point_mask_007.inputs[0].default_value = 4
			#Socket_5
			mn_topo_point_mask_007.inputs[1].default_value = False

			#node MN_topo_point_mask.004
			mn_topo_point_mask_004 = _mn_topo_assign_backbone.nodes.new("GeometryNodeGroup")
			mn_topo_point_mask_004.label = "Topology Point Mask"
			mn_topo_point_mask_004.name = "MN_topo_point_mask.004"
			mn_topo_point_mask_004.node_tree = residue_mask
			#Socket_1
			mn_topo_point_mask_004.inputs[0].default_value = 1
			#Socket_5
			mn_topo_point_mask_004.inputs[1].default_value = False

			#node Capture Attribute
			capture_attribute = _mn_topo_assign_backbone.nodes.new("GeometryNodeCaptureAttribute")
			capture_attribute.name = "Capture Attribute"
			capture_attribute.active_index = 0
			capture_attribute.capture_items.clear()
			capture_attribute.capture_items.new('FLOAT', "Unique Group ID")
			capture_attribute.capture_items["Unique Group ID"].data_type = 'INT'
			capture_attribute.domain = 'POINT'

			#node Group
			group_7 = _mn_topo_assign_backbone.nodes.new("GeometryNodeGroup")
			group_7.name = "Group"
			group_7.node_tree = res_group_id

			#node Reroute
			reroute_3 = _mn_topo_assign_backbone.nodes.new("NodeReroute")
			reroute_3.name = "Reroute"
			#node Reroute.001
			reroute_001_3 = _mn_topo_assign_backbone.nodes.new("NodeReroute")
			reroute_001_3.name = "Reroute.001"
			#node Reroute.002
			reroute_002_2 = _mn_topo_assign_backbone.nodes.new("NodeReroute")
			reroute_002_2.name = "Reroute.002"
			#node Reroute.003
			reroute_003_1 = _mn_topo_assign_backbone.nodes.new("NodeReroute")
			reroute_003_1.name = "Reroute.003"
			#node Separate Geometry
			separate_geometry = _mn_topo_assign_backbone.nodes.new("GeometryNodeSeparateGeometry")
			separate_geometry.name = "Separate Geometry"
			separate_geometry.domain = 'POINT'

			#node Group.001
			group_001_4 = _mn_topo_assign_backbone.nodes.new("GeometryNodeGroup")
			group_001_4.name = "Group.001"
			group_001_4.node_tree = is_alpha_carbon
			#Socket_1
			group_001_4.inputs[0].default_value = True
			#Socket_3
			group_001_4.inputs[1].default_value = False




			#Set locations
			group_output_18.location = (720.0, 100.0)
			group_input_18.location = (-1200.0, 100.0)
			store_named_attribute_002.location = (-400.0, 100.0)
			store_named_attribute_003.location = (60.0, 100.0)
			store_named_attribute_004.location = (-180.0, 100.0)
			store_named_attribute_005.location = (300.0, 100.0)
			mn_topo_point_mask_005.location = (60.0, -120.0)
			mn_topo_point_mask_006.location = (-180.0, -120.0)
			mn_topo_point_mask_007.location = (300.0, -120.0)
			mn_topo_point_mask_004.location = (-400.0, -120.0)
			capture_attribute.location = (-1020.0, 100.0)
			group_7.location = (-1200.0, 0.0)
			reroute_3.location = (-440.0, -340.0)
			reroute_001_3.location = (-200.0, -340.0)
			reroute_002_2.location = (40.0, -340.0)
			reroute_003_1.location = (280.0, -340.0)
			separate_geometry.location = (540.0, 20.0)
			group_001_4.location = (540.0, -160.0)

			#Set dimensions
			group_output_18.width, group_output_18.height = 140.0, 100.0
			group_input_18.width, group_input_18.height = 140.0, 100.0
			store_named_attribute_002.width, store_named_attribute_002.height = 172.44415283203125, 100.0
			store_named_attribute_003.width, store_named_attribute_003.height = 169.44052124023438, 100.0
			store_named_attribute_004.width, store_named_attribute_004.height = 184.14559936523438, 100.0
			store_named_attribute_005.width, store_named_attribute_005.height = 169.42654418945312, 100.0
			mn_topo_point_mask_005.width, mn_topo_point_mask_005.height = 172.76019287109375, 100.0
			mn_topo_point_mask_006.width, mn_topo_point_mask_006.height = 185.9674072265625, 100.0
			mn_topo_point_mask_007.width, mn_topo_point_mask_007.height = 168.1260986328125, 100.0
			mn_topo_point_mask_004.width, mn_topo_point_mask_004.height = 178.538330078125, 100.0
			capture_attribute.width, capture_attribute.height = 140.0, 100.0
			group_7.width, group_7.height = 140.0, 100.0
			reroute_3.width, reroute_3.height = 16.0, 100.0
			reroute_001_3.width, reroute_001_3.height = 16.0, 100.0
			reroute_002_2.width, reroute_002_2.height = 16.0, 100.0
			reroute_003_1.width, reroute_003_1.height = 16.0, 100.0
			separate_geometry.width, separate_geometry.height = 140.0, 100.0
			group_001_4.width, group_001_4.height = 140.0, 100.0

			#initialize _mn_topo_assign_backbone links
			#mn_topo_point_mask_007.Is Valid -> store_named_attribute_005.Selection
			_mn_topo_assign_backbone.links.new(mn_topo_point_mask_007.outputs[0], store_named_attribute_005.inputs[1])
			#mn_topo_point_mask_006.Position -> store_named_attribute_004.Value
			_mn_topo_assign_backbone.links.new(mn_topo_point_mask_006.outputs[2], store_named_attribute_004.inputs[3])
			#mn_topo_point_mask_005.Position -> store_named_attribute_003.Value
			_mn_topo_assign_backbone.links.new(mn_topo_point_mask_005.outputs[2], store_named_attribute_003.inputs[3])
			#store_named_attribute_004.Geometry -> store_named_attribute_003.Geometry
			_mn_topo_assign_backbone.links.new(store_named_attribute_004.outputs[0], store_named_attribute_003.inputs[0])
			#store_named_attribute_003.Geometry -> store_named_attribute_005.Geometry
			_mn_topo_assign_backbone.links.new(store_named_attribute_003.outputs[0], store_named_attribute_005.inputs[0])
			#store_named_attribute_002.Geometry -> store_named_attribute_004.Geometry
			_mn_topo_assign_backbone.links.new(store_named_attribute_002.outputs[0], store_named_attribute_004.inputs[0])
			#mn_topo_point_mask_007.Position -> store_named_attribute_005.Value
			_mn_topo_assign_backbone.links.new(mn_topo_point_mask_007.outputs[2], store_named_attribute_005.inputs[3])
			#mn_topo_point_mask_006.Is Valid -> store_named_attribute_004.Selection
			_mn_topo_assign_backbone.links.new(mn_topo_point_mask_006.outputs[0], store_named_attribute_004.inputs[1])
			#mn_topo_point_mask_005.Is Valid -> store_named_attribute_003.Selection
			_mn_topo_assign_backbone.links.new(mn_topo_point_mask_005.outputs[0], store_named_attribute_003.inputs[1])
			#capture_attribute.Geometry -> store_named_attribute_002.Geometry
			_mn_topo_assign_backbone.links.new(capture_attribute.outputs[0], store_named_attribute_002.inputs[0])
			#store_named_attribute_005.Geometry -> group_output_18.Atoms
			_mn_topo_assign_backbone.links.new(store_named_attribute_005.outputs[0], group_output_18.inputs[0])
			#group_input_18.Atoms -> capture_attribute.Geometry
			_mn_topo_assign_backbone.links.new(group_input_18.outputs[0], capture_attribute.inputs[0])
			#group_7.Unique Group ID -> capture_attribute.Unique Group ID
			_mn_topo_assign_backbone.links.new(group_7.outputs[0], capture_attribute.inputs[1])
			#reroute_001_3.Output -> mn_topo_point_mask_006.Group ID
			_mn_topo_assign_backbone.links.new(reroute_001_3.outputs[0], mn_topo_point_mask_006.inputs[2])
			#capture_attribute.Unique Group ID -> reroute_3.Input
			_mn_topo_assign_backbone.links.new(capture_attribute.outputs[1], reroute_3.inputs[0])
			#reroute_3.Output -> reroute_001_3.Input
			_mn_topo_assign_backbone.links.new(reroute_3.outputs[0], reroute_001_3.inputs[0])
			#reroute_002_2.Output -> mn_topo_point_mask_005.Group ID
			_mn_topo_assign_backbone.links.new(reroute_002_2.outputs[0], mn_topo_point_mask_005.inputs[2])
			#reroute_001_3.Output -> reroute_002_2.Input
			_mn_topo_assign_backbone.links.new(reroute_001_3.outputs[0], reroute_002_2.inputs[0])
			#reroute_003_1.Output -> mn_topo_point_mask_007.Group ID
			_mn_topo_assign_backbone.links.new(reroute_003_1.outputs[0], mn_topo_point_mask_007.inputs[2])
			#reroute_002_2.Output -> reroute_003_1.Input
			_mn_topo_assign_backbone.links.new(reroute_002_2.outputs[0], reroute_003_1.inputs[0])
			#capture_attribute.Unique Group ID -> group_output_18.Unique Group ID
			_mn_topo_assign_backbone.links.new(capture_attribute.outputs[1], group_output_18.inputs[1])
			#mn_topo_point_mask_004.Is Valid -> store_named_attribute_002.Selection
			_mn_topo_assign_backbone.links.new(mn_topo_point_mask_004.outputs[0], store_named_attribute_002.inputs[1])
			#mn_topo_point_mask_004.Position -> store_named_attribute_002.Value
			_mn_topo_assign_backbone.links.new(mn_topo_point_mask_004.outputs[2], store_named_attribute_002.inputs[3])
			#store_named_attribute_005.Geometry -> separate_geometry.Geometry
			_mn_topo_assign_backbone.links.new(store_named_attribute_005.outputs[0], separate_geometry.inputs[0])
			#separate_geometry.Selection -> group_output_18.CA Atoms
			_mn_topo_assign_backbone.links.new(separate_geometry.outputs[0], group_output_18.inputs[2])
			#group_001_4.Selection -> separate_geometry.Selection
			_mn_topo_assign_backbone.links.new(group_001_4.outputs[0], separate_geometry.inputs[1])
			#reroute_3.Output -> mn_topo_point_mask_004.Group ID
			_mn_topo_assign_backbone.links.new(reroute_3.outputs[0], mn_topo_point_mask_004.inputs[2])
			return _mn_topo_assign_backbone

		_mn_topo_assign_backbone = _mn_topo_assign_backbone_node_group()

		#initialize fallback_vector node group
		def fallback_vector_node_group():
			fallback_vector = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Fallback Vector")

			fallback_vector.color_tag = 'INPUT'
			fallback_vector.description = ""


			#fallback_vector interface
			#Socket Output
			output_socket = fallback_vector.interface.new_socket(name = "Output", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			output_socket.subtype = 'NONE'
			output_socket.default_value = (0.0, 0.0, 0.0)
			output_socket.min_value = -3.4028234663852886e+38
			output_socket.max_value = 3.4028234663852886e+38
			output_socket.attribute_domain = 'POINT'

			#Socket Name
			name_socket_1 = fallback_vector.interface.new_socket(name = "Name", in_out='INPUT', socket_type = 'NodeSocketString')
			name_socket_1.attribute_domain = 'POINT'

			#Socket Fallback
			fallback_socket_1 = fallback_vector.interface.new_socket(name = "Fallback", in_out='INPUT', socket_type = 'NodeSocketVector')
			fallback_socket_1.subtype = 'NONE'
			fallback_socket_1.default_value = (0.0, 0.0, 0.0)
			fallback_socket_1.min_value = -3.4028234663852886e+38
			fallback_socket_1.max_value = 3.4028234663852886e+38
			fallback_socket_1.attribute_domain = 'POINT'


			#initialize fallback_vector nodes
			#node Group Output
			group_output_19 = fallback_vector.nodes.new("NodeGroupOutput")
			group_output_19.name = "Group Output"
			group_output_19.is_active_output = True

			#node Group Input
			group_input_19 = fallback_vector.nodes.new("NodeGroupInput")
			group_input_19.name = "Group Input"

			#node Named Attribute.001
			named_attribute_001_1 = fallback_vector.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_001_1.name = "Named Attribute.001"
			named_attribute_001_1.data_type = 'FLOAT_VECTOR'

			#node Switch
			switch_3 = fallback_vector.nodes.new("GeometryNodeSwitch")
			switch_3.name = "Switch"
			switch_3.input_type = 'VECTOR'




			#Set locations
			group_output_19.location = (260.0, 140.0)
			group_input_19.location = (-320.0, 80.0)
			named_attribute_001_1.location = (-134.38072204589844, 30.303295135498047)
			switch_3.location = (100.0, 140.0)

			#Set dimensions
			group_output_19.width, group_output_19.height = 140.0, 100.0
			group_input_19.width, group_input_19.height = 140.0, 100.0
			named_attribute_001_1.width, named_attribute_001_1.height = 147.09487915039062, 100.0
			switch_3.width, switch_3.height = 140.0, 100.0

			#initialize fallback_vector links
			#named_attribute_001_1.Attribute -> switch_3.True
			fallback_vector.links.new(named_attribute_001_1.outputs[0], switch_3.inputs[2])
			#named_attribute_001_1.Exists -> switch_3.Switch
			fallback_vector.links.new(named_attribute_001_1.outputs[1], switch_3.inputs[0])
			#group_input_19.Fallback -> switch_3.False
			fallback_vector.links.new(group_input_19.outputs[1], switch_3.inputs[1])
			#switch_3.Output -> group_output_19.Output
			fallback_vector.links.new(switch_3.outputs[0], group_output_19.inputs[0])
			#group_input_19.Name -> named_attribute_001_1.Name
			fallback_vector.links.new(group_input_19.outputs[0], named_attribute_001_1.inputs[0])
			return fallback_vector

		fallback_vector = fallback_vector_node_group()

		#initialize offset_vector node group
		def offset_vector_node_group():
			offset_vector = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Offset Vector")

			offset_vector.color_tag = 'CONVERTER'
			offset_vector.description = ""


			#offset_vector interface
			#Socket Value
			value_socket_2 = offset_vector.interface.new_socket(name = "Value", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			value_socket_2.subtype = 'NONE'
			value_socket_2.default_value = (0.0, 0.0, 0.0)
			value_socket_2.min_value = -3.4028234663852886e+38
			value_socket_2.max_value = 3.4028234663852886e+38
			value_socket_2.attribute_domain = 'POINT'

			#Socket Index
			index_socket_5 = offset_vector.interface.new_socket(name = "Index", in_out='INPUT', socket_type = 'NodeSocketInt')
			index_socket_5.subtype = 'NONE'
			index_socket_5.default_value = 0
			index_socket_5.min_value = 0
			index_socket_5.max_value = 2147483647
			index_socket_5.attribute_domain = 'POINT'

			#Socket Vector
			vector_socket_1 = offset_vector.interface.new_socket(name = "Vector", in_out='INPUT', socket_type = 'NodeSocketVector')
			vector_socket_1.subtype = 'NONE'
			vector_socket_1.default_value = (0.0, 0.0, 0.0)
			vector_socket_1.min_value = -3.4028234663852886e+38
			vector_socket_1.max_value = 3.4028234663852886e+38
			vector_socket_1.attribute_domain = 'POINT'
			vector_socket_1.hide_value = True

			#Socket Offset
			offset_socket_2 = offset_vector.interface.new_socket(name = "Offset", in_out='INPUT', socket_type = 'NodeSocketInt')
			offset_socket_2.subtype = 'NONE'
			offset_socket_2.default_value = 0
			offset_socket_2.min_value = -2147483647
			offset_socket_2.max_value = 2147483647
			offset_socket_2.attribute_domain = 'POINT'


			#initialize offset_vector nodes
			#node Group Output
			group_output_20 = offset_vector.nodes.new("NodeGroupOutput")
			group_output_20.name = "Group Output"
			group_output_20.is_active_output = True

			#node Group Input
			group_input_20 = offset_vector.nodes.new("NodeGroupInput")
			group_input_20.name = "Group Input"

			#node Evaluate at Index
			evaluate_at_index_2 = offset_vector.nodes.new("GeometryNodeFieldAtIndex")
			evaluate_at_index_2.name = "Evaluate at Index"
			evaluate_at_index_2.data_type = 'FLOAT_VECTOR'
			evaluate_at_index_2.domain = 'POINT'

			#node Math
			math_4 = offset_vector.nodes.new("ShaderNodeMath")
			math_4.name = "Math"
			math_4.operation = 'ADD'
			math_4.use_clamp = False




			#Set locations
			group_output_20.location = (300.0, 20.0)
			group_input_20.location = (-273.81378173828125, 0.0)
			evaluate_at_index_2.location = (120.0, 20.0)
			math_4.location = (-60.0, 20.0)

			#Set dimensions
			group_output_20.width, group_output_20.height = 140.0, 100.0
			group_input_20.width, group_input_20.height = 140.0, 100.0
			evaluate_at_index_2.width, evaluate_at_index_2.height = 140.0, 100.0
			math_4.width, math_4.height = 140.0, 100.0

			#initialize offset_vector links
			#group_input_20.Vector -> evaluate_at_index_2.Value
			offset_vector.links.new(group_input_20.outputs[1], evaluate_at_index_2.inputs[1])
			#evaluate_at_index_2.Value -> group_output_20.Value
			offset_vector.links.new(evaluate_at_index_2.outputs[0], group_output_20.inputs[0])
			#group_input_20.Index -> math_4.Value
			offset_vector.links.new(group_input_20.outputs[0], math_4.inputs[0])
			#group_input_20.Offset -> math_4.Value
			offset_vector.links.new(group_input_20.outputs[2], math_4.inputs[1])
			#math_4.Value -> evaluate_at_index_2.Index
			offset_vector.links.new(math_4.outputs[0], evaluate_at_index_2.inputs[0])
			return offset_vector

		offset_vector = offset_vector_node_group()

		#initialize group_info node group
		def group_info_node_group():
			group_info = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Group Info")

			group_info.color_tag = 'CONVERTER'
			group_info.description = ""


			#group_info interface
			#Socket Is First
			is_first_socket = group_info.interface.new_socket(name = "Is First", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			is_first_socket.attribute_domain = 'POINT'

			#Socket First Index
			first_index_socket = group_info.interface.new_socket(name = "First Index", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			first_index_socket.subtype = 'NONE'
			first_index_socket.default_value = 0
			first_index_socket.min_value = -2147483648
			first_index_socket.max_value = 2147483647
			first_index_socket.attribute_domain = 'POINT'
			first_index_socket.description = "Index of the first point in the group"

			#Socket Is Last
			is_last_socket = group_info.interface.new_socket(name = "Is Last", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			is_last_socket.attribute_domain = 'POINT'

			#Socket Last Index
			last_index_socket = group_info.interface.new_socket(name = "Last Index", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			last_index_socket.subtype = 'NONE'
			last_index_socket.default_value = 0
			last_index_socket.min_value = -2147483648
			last_index_socket.max_value = 2147483647
			last_index_socket.attribute_domain = 'POINT'
			last_index_socket.description = "Index of the last point in the group"

			#Socket Index in Group
			index_in_group_socket = group_info.interface.new_socket(name = "Index in Group", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			index_in_group_socket.subtype = 'NONE'
			index_in_group_socket.default_value = 0
			index_in_group_socket.min_value = -2147483648
			index_in_group_socket.max_value = 2147483647
			index_in_group_socket.attribute_domain = 'POINT'

			#Socket Size
			size_socket = group_info.interface.new_socket(name = "Size", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			size_socket.subtype = 'NONE'
			size_socket.default_value = 0
			size_socket.min_value = -2147483648
			size_socket.max_value = 2147483647
			size_socket.attribute_domain = 'POINT'
			size_socket.description = "Number of points in the group"

			#Socket Group ID
			group_id_socket_4 = group_info.interface.new_socket(name = "Group ID", in_out='INPUT', socket_type = 'NodeSocketInt')
			group_id_socket_4.subtype = 'NONE'
			group_id_socket_4.default_value = 0
			group_id_socket_4.min_value = -2147483648
			group_id_socket_4.max_value = 2147483647
			group_id_socket_4.attribute_domain = 'POINT'


			#initialize group_info nodes
			#node Group Output
			group_output_21 = group_info.nodes.new("NodeGroupOutput")
			group_output_21.name = "Group Output"
			group_output_21.is_active_output = True

			#node Group Input
			group_input_21 = group_info.nodes.new("NodeGroupInput")
			group_input_21.name = "Group Input"

			#node Accumulate Field.001
			accumulate_field_001_1 = group_info.nodes.new("GeometryNodeAccumulateField")
			accumulate_field_001_1.name = "Accumulate Field.001"
			accumulate_field_001_1.data_type = 'INT'
			accumulate_field_001_1.domain = 'POINT'
			accumulate_field_001_1.outputs[0].hide = True
			accumulate_field_001_1.outputs[1].hide = True

			#node Index
			index_1 = group_info.nodes.new("GeometryNodeInputIndex")
			index_1.name = "Index"

			#node Switch.001
			switch_001_1 = group_info.nodes.new("GeometryNodeSwitch")
			switch_001_1.name = "Switch.001"
			switch_001_1.input_type = 'INT'
			#False
			switch_001_1.inputs[1].default_value = 0

			#node Compare.002
			compare_002_2 = group_info.nodes.new("FunctionNodeCompare")
			compare_002_2.name = "Compare.002"
			compare_002_2.data_type = 'INT'
			compare_002_2.mode = 'ELEMENT'
			compare_002_2.operation = 'EQUAL'

			#node Switch.002
			switch_002_1 = group_info.nodes.new("GeometryNodeSwitch")
			switch_002_1.name = "Switch.002"
			switch_002_1.input_type = 'INT'
			#False
			switch_002_1.inputs[1].default_value = 0

			#node Accumulate Field.002
			accumulate_field_002_1 = group_info.nodes.new("GeometryNodeAccumulateField")
			accumulate_field_002_1.name = "Accumulate Field.002"
			accumulate_field_002_1.data_type = 'INT'
			accumulate_field_002_1.domain = 'POINT'
			accumulate_field_002_1.outputs[0].hide = True
			accumulate_field_002_1.outputs[1].hide = True

			#node Reroute
			reroute_4 = group_info.nodes.new("NodeReroute")
			reroute_4.name = "Reroute"
			#node Accumulate Field.003
			accumulate_field_003 = group_info.nodes.new("GeometryNodeAccumulateField")
			accumulate_field_003.name = "Accumulate Field.003"
			accumulate_field_003.data_type = 'INT'
			accumulate_field_003.domain = 'POINT'
			#Value
			accumulate_field_003.inputs[0].default_value = 1

			#node Reroute.001
			reroute_001_4 = group_info.nodes.new("NodeReroute")
			reroute_001_4.name = "Reroute.001"
			#node Boolean Math
			boolean_math_5 = group_info.nodes.new("FunctionNodeBooleanMath")
			boolean_math_5.name = "Boolean Math"
			boolean_math_5.operation = 'NOT'




			#Set locations
			group_output_21.location = (580.0, 100.0)
			group_input_21.location = (-540.0, 0.0)
			accumulate_field_001_1.location = (340.0, 140.0)
			index_1.location = (-40.0, -20.0)
			switch_001_1.location = (140.0, 80.0)
			compare_002_2.location = (-40.0, -80.0)
			switch_002_1.location = (140.0, -100.0)
			accumulate_field_002_1.location = (340.0, -78.97427368164062)
			reroute_4.location = (280.0, -300.0)
			accumulate_field_003.location = (-240.0, -80.0)
			reroute_001_4.location = (-320.0, -300.0)
			boolean_math_5.location = (-40.0, 140.0)

			#Set dimensions
			group_output_21.width, group_output_21.height = 140.0, 100.0
			group_input_21.width, group_input_21.height = 140.0, 100.0
			accumulate_field_001_1.width, accumulate_field_001_1.height = 140.0, 100.0
			index_1.width, index_1.height = 140.0, 100.0
			switch_001_1.width, switch_001_1.height = 140.0, 100.0
			compare_002_2.width, compare_002_2.height = 140.0, 100.0
			switch_002_1.width, switch_002_1.height = 140.0, 100.0
			accumulate_field_002_1.width, accumulate_field_002_1.height = 140.0, 100.0
			reroute_4.width, reroute_4.height = 16.0, 100.0
			accumulate_field_003.width, accumulate_field_003.height = 140.0, 100.0
			reroute_001_4.width, reroute_001_4.height = 16.0, 100.0
			boolean_math_5.width, boolean_math_5.height = 140.0, 100.0

			#initialize group_info links
			#reroute_4.Output -> accumulate_field_002_1.Group ID
			group_info.links.new(reroute_4.outputs[0], accumulate_field_002_1.inputs[1])
			#reroute_001_4.Output -> reroute_4.Input
			group_info.links.new(reroute_001_4.outputs[0], reroute_4.inputs[0])
			#index_1.Index -> switch_002_1.True
			group_info.links.new(index_1.outputs[0], switch_002_1.inputs[2])
			#accumulate_field_003.Total -> compare_002_2.B
			group_info.links.new(accumulate_field_003.outputs[2], compare_002_2.inputs[3])
			#switch_002_1.Output -> accumulate_field_002_1.Value
			group_info.links.new(switch_002_1.outputs[0], accumulate_field_002_1.inputs[0])
			#reroute_001_4.Output -> accumulate_field_003.Group ID
			group_info.links.new(reroute_001_4.outputs[0], accumulate_field_003.inputs[1])
			#index_1.Index -> switch_001_1.True
			group_info.links.new(index_1.outputs[0], switch_001_1.inputs[2])
			#switch_001_1.Output -> accumulate_field_001_1.Value
			group_info.links.new(switch_001_1.outputs[0], accumulate_field_001_1.inputs[0])
			#compare_002_2.Result -> switch_002_1.Switch
			group_info.links.new(compare_002_2.outputs[0], switch_002_1.inputs[0])
			#reroute_4.Output -> accumulate_field_001_1.Group ID
			group_info.links.new(reroute_4.outputs[0], accumulate_field_001_1.inputs[1])
			#group_input_21.Group ID -> reroute_001_4.Input
			group_info.links.new(group_input_21.outputs[0], reroute_001_4.inputs[0])
			#accumulate_field_001_1.Total -> group_output_21.First Index
			group_info.links.new(accumulate_field_001_1.outputs[2], group_output_21.inputs[1])
			#accumulate_field_002_1.Total -> group_output_21.Last Index
			group_info.links.new(accumulate_field_002_1.outputs[2], group_output_21.inputs[3])
			#accumulate_field_003.Total -> group_output_21.Size
			group_info.links.new(accumulate_field_003.outputs[2], group_output_21.inputs[5])
			#accumulate_field_003.Leading -> compare_002_2.A
			group_info.links.new(accumulate_field_003.outputs[0], compare_002_2.inputs[2])
			#accumulate_field_003.Trailing -> group_output_21.Index in Group
			group_info.links.new(accumulate_field_003.outputs[1], group_output_21.inputs[4])
			#accumulate_field_003.Trailing -> boolean_math_5.Boolean
			group_info.links.new(accumulate_field_003.outputs[1], boolean_math_5.inputs[0])
			#boolean_math_5.Boolean -> switch_001_1.Switch
			group_info.links.new(boolean_math_5.outputs[0], switch_001_1.inputs[0])
			#boolean_math_5.Boolean -> group_output_21.Is First
			group_info.links.new(boolean_math_5.outputs[0], group_output_21.inputs[0])
			#compare_002_2.Result -> group_output_21.Is Last
			group_info.links.new(compare_002_2.outputs[0], group_output_21.inputs[2])
			return group_info

		group_info = group_info_node_group()

		#initialize backbone_position node group
		def backbone_position_node_group():
			backbone_position = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Backbone Position")

			backbone_position.color_tag = 'INPUT'
			backbone_position.description = ""


			#backbone_position interface
			#Socket Position
			position_socket_2 = backbone_position.interface.new_socket(name = "Position", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			position_socket_2.subtype = 'NONE'
			position_socket_2.default_value = (0.0, 0.0, 0.0)
			position_socket_2.min_value = -3.4028234663852886e+38
			position_socket_2.max_value = 3.4028234663852886e+38
			position_socket_2.attribute_domain = 'POINT'

			#Socket Index
			index_socket_6 = backbone_position.interface.new_socket(name = "Index", in_out='INPUT', socket_type = 'NodeSocketInt')
			index_socket_6.subtype = 'NONE'
			index_socket_6.default_value = 0
			index_socket_6.min_value = 0
			index_socket_6.max_value = 2147483647
			index_socket_6.attribute_domain = 'POINT'
			index_socket_6.hide_value = True

			#Socket Menu
			menu_socket = backbone_position.interface.new_socket(name = "Menu", in_out='INPUT', socket_type = 'NodeSocketMenu')
			menu_socket.attribute_domain = 'POINT'

			#Socket Offset
			offset_socket_3 = backbone_position.interface.new_socket(name = "Offset", in_out='INPUT', socket_type = 'NodeSocketInt')
			offset_socket_3.subtype = 'NONE'
			offset_socket_3.default_value = 0
			offset_socket_3.min_value = -1
			offset_socket_3.max_value = 1
			offset_socket_3.attribute_domain = 'POINT'


			#initialize backbone_position nodes
			#node Group Output
			group_output_22 = backbone_position.nodes.new("NodeGroupOutput")
			group_output_22.name = "Group Output"
			group_output_22.is_active_output = True

			#node Group Input
			group_input_22 = backbone_position.nodes.new("NodeGroupInput")
			group_input_22.name = "Group Input"
			group_input_22.outputs[0].hide = True
			group_input_22.outputs[2].hide = True
			group_input_22.outputs[3].hide = True

			#node Group
			group_8 = backbone_position.nodes.new("GeometryNodeGroup")
			group_8.name = "Group"
			group_8.node_tree = residue_mask
			#Socket_5
			group_8.inputs[1].default_value = True
			#Socket_4
			group_8.inputs[2].default_value = 0

			#node Group.001
			group_001_5 = backbone_position.nodes.new("GeometryNodeGroup")
			group_001_5.name = "Group.001"
			group_001_5.node_tree = fallback_vector

			#node Index Switch
			index_switch = backbone_position.nodes.new("GeometryNodeIndexSwitch")
			index_switch.name = "Index Switch"
			index_switch.data_type = 'STRING'
			index_switch.index_switch_items.clear()
			index_switch.index_switch_items.new()
			index_switch.index_switch_items.new()
			index_switch.index_switch_items.new()
			index_switch.index_switch_items.new()
			index_switch.index_switch_items.new()
			#Item_0
			index_switch.inputs[1].default_value = ""
			#Item_1
			index_switch.inputs[2].default_value = "backbone_N"
			#Item_2
			index_switch.inputs[3].default_value = "backbone_CA"
			#Item_3
			index_switch.inputs[4].default_value = "backbone_C"
			#Item_4
			index_switch.inputs[5].default_value = "backbone_O"

			#node Menu Switch
			menu_switch = backbone_position.nodes.new("GeometryNodeMenuSwitch")
			menu_switch.name = "Menu Switch"
			menu_switch.active_index = 3
			menu_switch.data_type = 'INT'
			menu_switch.enum_items.clear()
			menu_switch.enum_items.new("backbone_N")
			menu_switch.enum_items[0].description = ""
			menu_switch.enum_items.new("backbone_CA")
			menu_switch.enum_items[1].description = ""
			menu_switch.enum_items.new("backbone_C")
			menu_switch.enum_items[2].description = ""
			menu_switch.enum_items.new("backbone_O")
			menu_switch.enum_items[3].description = ""
			#Item_0
			menu_switch.inputs[1].default_value = 1
			#Item_1
			menu_switch.inputs[2].default_value = 2
			#Item_2
			menu_switch.inputs[3].default_value = 3
			#Item_3
			menu_switch.inputs[4].default_value = 4

			#node Group.002
			group_002_3 = backbone_position.nodes.new("GeometryNodeGroup")
			group_002_3.name = "Group.002"
			group_002_3.node_tree = offset_vector

			#node Group Input.001
			group_input_001 = backbone_position.nodes.new("NodeGroupInput")
			group_input_001.name = "Group Input.001"
			group_input_001.outputs[1].hide = True
			group_input_001.outputs[3].hide = True

			#node Group.003
			group_003 = backbone_position.nodes.new("GeometryNodeGroup")
			group_003.name = "Group.003"
			group_003.node_tree = group_info

			#node Math
			math_5 = backbone_position.nodes.new("ShaderNodeMath")
			math_5.name = "Math"
			math_5.operation = 'MULTIPLY'
			math_5.use_clamp = False




			#Set locations
			group_output_22.location = (640.0, 100.0)
			group_input_22.location = (-560.0, 100.0)
			group_8.location = (-194.45651245117188, 100.0)
			group_001_5.location = (60.0, 120.0)
			index_switch.location = (-200.0, -140.0)
			menu_switch.location = (-380.0, 100.0)
			group_002_3.location = (460.0, 100.0)
			group_input_001.location = (60.0, 0.0)
			group_003.location = (60.0, -100.0)
			math_5.location = (260.0, -100.0)

			#Set dimensions
			group_output_22.width, group_output_22.height = 140.0, 100.0
			group_input_22.width, group_input_22.height = 140.0, 100.0
			group_8.width, group_8.height = 174.45651245117188, 100.0
			group_001_5.width, group_001_5.height = 141.8542938232422, 100.0
			index_switch.width, index_switch.height = 184.38287353515625, 100.0
			menu_switch.width, menu_switch.height = 140.0, 100.0
			group_002_3.width, group_002_3.height = 140.0, 100.0
			group_input_001.width, group_input_001.height = 140.0, 100.0
			group_003.width, group_003.height = 140.0, 100.0
			math_5.width, math_5.height = 140.0, 100.0

			#initialize backbone_position links
			#index_switch.Output -> group_001_5.Name
			backbone_position.links.new(index_switch.outputs[0], group_001_5.inputs[0])
			#menu_switch.Output -> index_switch.Index
			backbone_position.links.new(menu_switch.outputs[0], index_switch.inputs[0])
			#group_input_22.Menu -> menu_switch.Menu
			backbone_position.links.new(group_input_22.outputs[1], menu_switch.inputs[0])
			#group_input_001.Index -> group_002_3.Index
			backbone_position.links.new(group_input_001.outputs[0], group_002_3.inputs[0])
			#menu_switch.Output -> group_8.atom_name
			backbone_position.links.new(menu_switch.outputs[0], group_8.inputs[0])
			#group_002_3.Value -> group_output_22.Position
			backbone_position.links.new(group_002_3.outputs[0], group_output_22.inputs[0])
			#group_001_5.Output -> group_002_3.Vector
			backbone_position.links.new(group_001_5.outputs[0], group_002_3.inputs[1])
			#group_8.Position -> group_001_5.Fallback
			backbone_position.links.new(group_8.outputs[2], group_001_5.inputs[1])
			#group_8.Group ID -> group_003.Group ID
			backbone_position.links.new(group_8.outputs[3], group_003.inputs[0])
			#group_input_001.Offset -> math_5.Value
			backbone_position.links.new(group_input_001.outputs[2], math_5.inputs[0])
			#group_003.Size -> math_5.Value
			backbone_position.links.new(group_003.outputs[5], math_5.inputs[1])
			#math_5.Value -> group_002_3.Offset
			backbone_position.links.new(math_5.outputs[0], group_002_3.inputs[2])
			return backbone_position

		backbone_position = backbone_position_node_group()

		#initialize backbone_positions node group
		def backbone_positions_node_group():
			backbone_positions = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Backbone Positions")

			backbone_positions.color_tag = 'INPUT'
			backbone_positions.description = ""


			#backbone_positions interface
			#Socket O
			o_socket = backbone_positions.interface.new_socket(name = "O", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			o_socket.subtype = 'NONE'
			o_socket.default_value = (0.0, 0.0, 0.0)
			o_socket.min_value = -3.4028234663852886e+38
			o_socket.max_value = 3.4028234663852886e+38
			o_socket.attribute_domain = 'POINT'

			#Socket C
			c_socket = backbone_positions.interface.new_socket(name = "C", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			c_socket.subtype = 'NONE'
			c_socket.default_value = (0.0, 0.0, 0.0)
			c_socket.min_value = -3.4028234663852886e+38
			c_socket.max_value = 3.4028234663852886e+38
			c_socket.attribute_domain = 'POINT'

			#Socket CA
			ca_socket = backbone_positions.interface.new_socket(name = "CA", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			ca_socket.subtype = 'NONE'
			ca_socket.default_value = (0.0, 0.0, 0.0)
			ca_socket.min_value = -3.4028234663852886e+38
			ca_socket.max_value = 3.4028234663852886e+38
			ca_socket.attribute_domain = 'POINT'

			#Socket N
			n_socket = backbone_positions.interface.new_socket(name = "N", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			n_socket.subtype = 'NONE'
			n_socket.default_value = (0.0, 0.0, 0.0)
			n_socket.min_value = -3.4028234663852886e+38
			n_socket.max_value = 3.4028234663852886e+38
			n_socket.attribute_domain = 'POINT'

			#Socket Offset
			offset_socket_4 = backbone_positions.interface.new_socket(name = "Offset", in_out='INPUT', socket_type = 'NodeSocketInt')
			offset_socket_4.subtype = 'NONE'
			offset_socket_4.default_value = 0
			offset_socket_4.min_value = -2147483648
			offset_socket_4.max_value = 2147483647
			offset_socket_4.attribute_domain = 'POINT'


			#initialize backbone_positions nodes
			#node Group Output
			group_output_23 = backbone_positions.nodes.new("NodeGroupOutput")
			group_output_23.name = "Group Output"
			group_output_23.is_active_output = True

			#node Group Input
			group_input_23 = backbone_positions.nodes.new("NodeGroupInput")
			group_input_23.name = "Group Input"

			#node Group.001
			group_001_6 = backbone_positions.nodes.new("GeometryNodeGroup")
			group_001_6.name = "Group.001"
			group_001_6.node_tree = backbone_position
			#Socket_3
			group_001_6.inputs[0].default_value = 0
			#Socket_2
			group_001_6.inputs[1].default_value = 'backbone_O'

			#node Group.005
			group_005 = backbone_positions.nodes.new("GeometryNodeGroup")
			group_005.name = "Group.005"
			group_005.node_tree = backbone_position
			#Socket_3
			group_005.inputs[0].default_value = 0
			#Socket_2
			group_005.inputs[1].default_value = 'backbone_C'

			#node Group.006
			group_006 = backbone_positions.nodes.new("GeometryNodeGroup")
			group_006.name = "Group.006"
			group_006.node_tree = backbone_position
			#Socket_3
			group_006.inputs[0].default_value = 0
			#Socket_2
			group_006.inputs[1].default_value = 'backbone_CA'

			#node Group.007
			group_007 = backbone_positions.nodes.new("GeometryNodeGroup")
			group_007.name = "Group.007"
			group_007.node_tree = backbone_position
			#Socket_3
			group_007.inputs[0].default_value = 0
			#Socket_2
			group_007.inputs[1].default_value = 'backbone_N'




			#Set locations
			group_output_23.location = (320.0, -220.0)
			group_input_23.location = (-260.0, -340.0)
			group_001_6.location = (60.0, -60.0)
			group_005.location = (60.0, -220.0)
			group_006.location = (60.0, -400.0)
			group_007.location = (60.0, -560.0)

			#Set dimensions
			group_output_23.width, group_output_23.height = 140.0, 100.0
			group_input_23.width, group_input_23.height = 140.0, 100.0
			group_001_6.width, group_001_6.height = 177.7757568359375, 100.0
			group_005.width, group_005.height = 177.7757568359375, 100.0
			group_006.width, group_006.height = 177.7757568359375, 100.0
			group_007.width, group_007.height = 177.7757568359375, 100.0

			#initialize backbone_positions links
			#group_007.Position -> group_output_23.N
			backbone_positions.links.new(group_007.outputs[0], group_output_23.inputs[3])
			#group_006.Position -> group_output_23.CA
			backbone_positions.links.new(group_006.outputs[0], group_output_23.inputs[2])
			#group_005.Position -> group_output_23.C
			backbone_positions.links.new(group_005.outputs[0], group_output_23.inputs[1])
			#group_001_6.Position -> group_output_23.O
			backbone_positions.links.new(group_001_6.outputs[0], group_output_23.inputs[0])
			#group_input_23.Offset -> group_005.Offset
			backbone_positions.links.new(group_input_23.outputs[0], group_005.inputs[2])
			#group_input_23.Offset -> group_001_6.Offset
			backbone_positions.links.new(group_input_23.outputs[0], group_001_6.inputs[2])
			#group_input_23.Offset -> group_006.Offset
			backbone_positions.links.new(group_input_23.outputs[0], group_006.inputs[2])
			#group_input_23.Offset -> group_007.Offset
			backbone_positions.links.new(group_input_23.outputs[0], group_007.inputs[2])
			return backbone_positions

		backbone_positions = backbone_positions_node_group()

		#initialize backbone_vectors node group
		def backbone_vectors_node_group():
			backbone_vectors = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Backbone Vectors")

			backbone_vectors.color_tag = 'INPUT'
			backbone_vectors.description = ""


			#backbone_vectors interface
			#Socket Normal
			normal_socket = backbone_vectors.interface.new_socket(name = "Normal", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			normal_socket.subtype = 'NONE'
			normal_socket.default_value = (0.0, 0.0, 0.0)
			normal_socket.min_value = -3.4028234663852886e+38
			normal_socket.max_value = 3.4028234663852886e+38
			normal_socket.attribute_domain = 'POINT'

			#Socket Tangent
			tangent_socket = backbone_vectors.interface.new_socket(name = "Tangent", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			tangent_socket.subtype = 'NONE'
			tangent_socket.default_value = (0.0, 0.0, 0.0)
			tangent_socket.min_value = -3.4028234663852886e+38
			tangent_socket.max_value = 3.4028234663852886e+38
			tangent_socket.attribute_domain = 'POINT'

			#Socket Bitangent
			bitangent_socket = backbone_vectors.interface.new_socket(name = "Bitangent", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			bitangent_socket.subtype = 'NONE'
			bitangent_socket.default_value = (0.0, 0.0, 0.0)
			bitangent_socket.min_value = -3.4028234663852886e+38
			bitangent_socket.max_value = 3.4028234663852886e+38
			bitangent_socket.attribute_domain = 'POINT'


			#initialize backbone_vectors nodes
			#node Group Output
			group_output_24 = backbone_vectors.nodes.new("NodeGroupOutput")
			group_output_24.name = "Group Output"
			group_output_24.is_active_output = True

			#node Group Input
			group_input_24 = backbone_vectors.nodes.new("NodeGroupInput")
			group_input_24.name = "Group Input"

			#node Group.004
			group_004 = backbone_vectors.nodes.new("GeometryNodeGroup")
			group_004.name = "Group.004"
			group_004.node_tree = backbone_positions
			#Socket_3
			group_004.inputs[0].default_value = 0

			#node Vector Math.001
			vector_math_001 = backbone_vectors.nodes.new("ShaderNodeVectorMath")
			vector_math_001.name = "Vector Math.001"
			vector_math_001.operation = 'SUBTRACT'

			#node Vector Math.002
			vector_math_002 = backbone_vectors.nodes.new("ShaderNodeVectorMath")
			vector_math_002.name = "Vector Math.002"
			vector_math_002.operation = 'CROSS_PRODUCT'

			#node Vector Math.005
			vector_math_005 = backbone_vectors.nodes.new("ShaderNodeVectorMath")
			vector_math_005.name = "Vector Math.005"
			vector_math_005.operation = 'SUBTRACT'

			#node Vector Math
			vector_math = backbone_vectors.nodes.new("ShaderNodeVectorMath")
			vector_math.name = "Vector Math"
			vector_math.operation = 'NORMALIZE'

			#node Vector Math.004
			vector_math_004 = backbone_vectors.nodes.new("ShaderNodeVectorMath")
			vector_math_004.name = "Vector Math.004"
			vector_math_004.operation = 'NORMALIZE'

			#node Vector Math.006
			vector_math_006 = backbone_vectors.nodes.new("ShaderNodeVectorMath")
			vector_math_006.name = "Vector Math.006"
			vector_math_006.operation = 'NORMALIZE'

			#node Mix
			mix = backbone_vectors.nodes.new("ShaderNodeMix")
			mix.name = "Mix"
			mix.blend_type = 'MIX'
			mix.clamp_factor = True
			mix.clamp_result = False
			mix.data_type = 'VECTOR'
			mix.factor_mode = 'UNIFORM'
			#Factor_Float
			mix.inputs[0].default_value = 0.44999998807907104




			#Set locations
			group_output_24.location = (580.0, 60.0)
			group_input_24.location = (-480.0, -60.0)
			group_004.location = (-300.0, -20.0)
			vector_math_001.location = (-120.0, -100.0)
			vector_math_002.location = (200.0, -100.0)
			vector_math_005.location = (40.0, 120.0)
			vector_math.location = (40.0, -100.0)
			vector_math_004.location = (200.0, 120.0)
			vector_math_006.location = (360.0, -100.0)
			mix.location = (-120.0, 120.0)

			#Set dimensions
			group_output_24.width, group_output_24.height = 140.0, 100.0
			group_input_24.width, group_input_24.height = 140.0, 100.0
			group_004.width, group_004.height = 140.0, 100.0
			vector_math_001.width, vector_math_001.height = 140.0, 100.0
			vector_math_002.width, vector_math_002.height = 140.0, 100.0
			vector_math_005.width, vector_math_005.height = 140.0, 100.0
			vector_math.width, vector_math.height = 140.0, 100.0
			vector_math_004.width, vector_math_004.height = 140.0, 100.0
			vector_math_006.width, vector_math_006.height = 140.0, 100.0
			mix.width, mix.height = 140.0, 100.0

			#initialize backbone_vectors links
			#vector_math_001.Vector -> vector_math.Vector
			backbone_vectors.links.new(vector_math_001.outputs[0], vector_math.inputs[0])
			#vector_math.Vector -> group_output_24.Tangent
			backbone_vectors.links.new(vector_math.outputs[0], group_output_24.inputs[1])
			#vector_math_002.Vector -> vector_math_006.Vector
			backbone_vectors.links.new(vector_math_002.outputs[0], vector_math_006.inputs[0])
			#group_004.N -> vector_math_001.Vector
			backbone_vectors.links.new(group_004.outputs[3], vector_math_001.inputs[1])
			#vector_math_005.Vector -> vector_math_004.Vector
			backbone_vectors.links.new(vector_math_005.outputs[0], vector_math_004.inputs[0])
			#group_004.C -> vector_math_001.Vector
			backbone_vectors.links.new(group_004.outputs[1], vector_math_001.inputs[0])
			#group_004.N -> mix.B
			backbone_vectors.links.new(group_004.outputs[3], mix.inputs[5])
			#group_004.C -> mix.A
			backbone_vectors.links.new(group_004.outputs[1], mix.inputs[4])
			#group_004.CA -> vector_math_005.Vector
			backbone_vectors.links.new(group_004.outputs[2], vector_math_005.inputs[1])
			#vector_math_004.Vector -> vector_math_002.Vector
			backbone_vectors.links.new(vector_math_004.outputs[0], vector_math_002.inputs[1])
			#vector_math.Vector -> vector_math_002.Vector
			backbone_vectors.links.new(vector_math.outputs[0], vector_math_002.inputs[0])
			#vector_math_004.Vector -> group_output_24.Normal
			backbone_vectors.links.new(vector_math_004.outputs[0], group_output_24.inputs[0])
			#mix.Result -> vector_math_005.Vector
			backbone_vectors.links.new(mix.outputs[1], vector_math_005.inputs[0])
			#vector_math_006.Vector -> group_output_24.Bitangent
			backbone_vectors.links.new(vector_math_006.outputs[0], group_output_24.inputs[2])
			return backbone_vectors

		backbone_vectors = backbone_vectors_node_group()

		#initialize _mn_world_scale node group
		def _mn_world_scale_node_group():
			_mn_world_scale = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".MN_world_scale")

			_mn_world_scale.color_tag = 'NONE'
			_mn_world_scale.description = ""


			#_mn_world_scale interface
			#Socket world_scale
			world_scale_socket = _mn_world_scale.interface.new_socket(name = "world_scale", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
			world_scale_socket.subtype = 'NONE'
			world_scale_socket.default_value = 0.009999999776482582
			world_scale_socket.min_value = -3.4028234663852886e+38
			world_scale_socket.max_value = 3.4028234663852886e+38
			world_scale_socket.attribute_domain = 'POINT'


			#initialize _mn_world_scale nodes
			#node Group Input
			group_input_25 = _mn_world_scale.nodes.new("NodeGroupInput")
			group_input_25.name = "Group Input"

			#node Value
			value = _mn_world_scale.nodes.new("ShaderNodeValue")
			value.label = "world_scale"
			value.name = "Value"

			value.outputs[0].default_value = 0.009999999776482582
			#node Group Output
			group_output_25 = _mn_world_scale.nodes.new("NodeGroupOutput")
			group_output_25.name = "Group Output"
			group_output_25.is_active_output = True




			#Set locations
			group_input_25.location = (-200.0, 0.0)
			value.location = (0.0, 0.0)
			group_output_25.location = (190.0, 0.0)

			#Set dimensions
			group_input_25.width, group_input_25.height = 140.0, 100.0
			value.width, value.height = 140.0, 100.0
			group_output_25.width, group_output_25.height = 140.0, 100.0

			#initialize _mn_world_scale links
			#value.Value -> group_output_25.world_scale
			_mn_world_scale.links.new(value.outputs[0], group_output_25.inputs[0])
			return _mn_world_scale

		_mn_world_scale = _mn_world_scale_node_group()

		#initialize mn_units node group
		def mn_units_node_group():
			mn_units = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "MN Units")

			mn_units.color_tag = 'CONVERTER'
			mn_units.description = ""


			#mn_units interface
			#Socket Angstrom
			angstrom_socket = mn_units.interface.new_socket(name = "Angstrom", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
			angstrom_socket.subtype = 'NONE'
			angstrom_socket.default_value = 0.0
			angstrom_socket.min_value = -3.4028234663852886e+38
			angstrom_socket.max_value = 3.4028234663852886e+38
			angstrom_socket.attribute_domain = 'POINT'

			#Socket Nanometre
			nanometre_socket = mn_units.interface.new_socket(name = "Nanometre", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
			nanometre_socket.subtype = 'NONE'
			nanometre_socket.default_value = 0.0
			nanometre_socket.min_value = -3.4028234663852886e+38
			nanometre_socket.max_value = 3.4028234663852886e+38
			nanometre_socket.attribute_domain = 'POINT'

			#Socket Value
			value_socket_3 = mn_units.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat')
			value_socket_3.subtype = 'NONE'
			value_socket_3.default_value = 3.0
			value_socket_3.min_value = -10000.0
			value_socket_3.max_value = 10000.0
			value_socket_3.attribute_domain = 'POINT'
			value_socket_3.description = "A value which will be scaled appropriately for the world"


			#initialize mn_units nodes
			#node Group Output
			group_output_26 = mn_units.nodes.new("NodeGroupOutput")
			group_output_26.name = "Group Output"
			group_output_26.is_active_output = True

			#node Group Input
			group_input_26 = mn_units.nodes.new("NodeGroupInput")
			group_input_26.name = "Group Input"

			#node Math
			math_6 = mn_units.nodes.new("ShaderNodeMath")
			math_6.name = "Math"
			math_6.operation = 'MULTIPLY'
			math_6.use_clamp = False

			#node Math.001
			math_001 = mn_units.nodes.new("ShaderNodeMath")
			math_001.name = "Math.001"
			math_001.operation = 'MULTIPLY'
			math_001.use_clamp = False
			#Value_001
			math_001.inputs[1].default_value = 10.0

			#node Group
			group_9 = mn_units.nodes.new("GeometryNodeGroup")
			group_9.name = "Group"
			group_9.node_tree = _mn_world_scale




			#Set locations
			group_output_26.location = (190.0, 0.0)
			group_input_26.location = (-240.0, 0.0)
			math_6.location = (-60.0, 0.0)
			math_001.location = (-60.0, -160.0)
			group_9.location = (-304.00421142578125, -104.114013671875)

			#Set dimensions
			group_output_26.width, group_output_26.height = 140.0, 100.0
			group_input_26.width, group_input_26.height = 140.0, 100.0
			math_6.width, math_6.height = 140.0, 100.0
			math_001.width, math_001.height = 140.0, 100.0
			group_9.width, group_9.height = 197.58424377441406, 100.0

			#initialize mn_units links
			#math_6.Value -> group_output_26.Angstrom
			mn_units.links.new(math_6.outputs[0], group_output_26.inputs[0])
			#group_input_26.Value -> math_6.Value
			mn_units.links.new(group_input_26.outputs[0], math_6.inputs[0])
			#group_9.world_scale -> math_6.Value
			mn_units.links.new(group_9.outputs[0], math_6.inputs[1])
			#math_6.Value -> math_001.Value
			mn_units.links.new(math_6.outputs[0], math_001.inputs[0])
			#math_001.Value -> group_output_26.Nanometre
			mn_units.links.new(math_001.outputs[0], group_output_26.inputs[1])
			return mn_units

		mn_units = mn_units_node_group()

		#initialize atom_id node group
		def atom_id_node_group():
			atom_id = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Atom ID")

			atom_id.color_tag = 'INPUT'
			atom_id.description = ""


			#atom_id interface
			#Socket atom_id
			atom_id_socket = atom_id.interface.new_socket(name = "atom_id", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			atom_id_socket.subtype = 'NONE'
			atom_id_socket.default_value = 0
			atom_id_socket.min_value = -2147483648
			atom_id_socket.max_value = 2147483647
			atom_id_socket.attribute_domain = 'POINT'


			#initialize atom_id nodes
			#node Group Output
			group_output_27 = atom_id.nodes.new("NodeGroupOutput")
			group_output_27.name = "Group Output"
			group_output_27.is_active_output = True

			#node Group Input
			group_input_27 = atom_id.nodes.new("NodeGroupInput")
			group_input_27.name = "Group Input"

			#node Named Attribute.018
			named_attribute_018 = atom_id.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_018.name = "Named Attribute.018"
			named_attribute_018.data_type = 'INT'
			#Name
			named_attribute_018.inputs[0].default_value = "atom_id"




			#Set locations
			group_output_27.location = (190.0, 0.0)
			group_input_27.location = (-200.0, 0.0)
			named_attribute_018.location = (0.0, 0.0)

			#Set dimensions
			group_output_27.width, group_output_27.height = 140.0, 100.0
			group_input_27.width, group_input_27.height = 140.0, 100.0
			named_attribute_018.width, named_attribute_018.height = 140.0, 100.0

			#initialize atom_id links
			#named_attribute_018.Attribute -> group_output_27.atom_id
			atom_id.links.new(named_attribute_018.outputs[0], group_output_27.inputs[0])
			return atom_id

		atom_id = atom_id_node_group()

		#initialize chain_id node group
		def chain_id_node_group():
			chain_id = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Chain ID")

			chain_id.color_tag = 'INPUT'
			chain_id.description = ""


			#chain_id interface
			#Socket chain_id
			chain_id_socket = chain_id.interface.new_socket(name = "chain_id", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			chain_id_socket.subtype = 'NONE'
			chain_id_socket.default_value = 0
			chain_id_socket.min_value = -2147483648
			chain_id_socket.max_value = 2147483647
			chain_id_socket.attribute_domain = 'POINT'


			#initialize chain_id nodes
			#node Group Output
			group_output_28 = chain_id.nodes.new("NodeGroupOutput")
			group_output_28.name = "Group Output"
			group_output_28.is_active_output = True

			#node Group Input
			group_input_28 = chain_id.nodes.new("NodeGroupInput")
			group_input_28.name = "Group Input"

			#node Named Attribute.018
			named_attribute_018_1 = chain_id.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_018_1.name = "Named Attribute.018"
			named_attribute_018_1.data_type = 'INT'
			#Name
			named_attribute_018_1.inputs[0].default_value = "chain_id"




			#Set locations
			group_output_28.location = (190.0, 0.0)
			group_input_28.location = (-200.0, 0.0)
			named_attribute_018_1.location = (0.0, 0.0)

			#Set dimensions
			group_output_28.width, group_output_28.height = 140.0, 100.0
			group_input_28.width, group_input_28.height = 140.0, 100.0
			named_attribute_018_1.width, named_attribute_018_1.height = 140.0, 100.0

			#initialize chain_id links
			#named_attribute_018_1.Attribute -> group_output_28.chain_id
			chain_id.links.new(named_attribute_018_1.outputs[0], group_output_28.inputs[0])
			return chain_id

		chain_id = chain_id_node_group()

		#initialize integer_run node group
		def integer_run_node_group():
			integer_run = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Integer Run")

			integer_run.color_tag = 'CONVERTER'
			integer_run.description = "A unique value for each grouping of a value. Accumulating along the field, the output Group Mask increments by 1 whenever the value or Group ID changes"


			#integer_run interface
			#Socket Is Different
			is_different_socket = integer_run.interface.new_socket(name = "Is Different", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			is_different_socket.attribute_domain = 'POINT'
			is_different_socket.description = "True whenever the value is different to the value that came before it"

			#Socket Group Mask
			group_mask_socket = integer_run.interface.new_socket(name = "Group Mask", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			group_mask_socket.subtype = 'NONE'
			group_mask_socket.default_value = 0
			group_mask_socket.min_value = -2147483648
			group_mask_socket.max_value = 2147483647
			group_mask_socket.attribute_domain = 'POINT'
			group_mask_socket.description = "Group mask increments whenever the Value or the Group ID changes"

			#Socket Value
			value_socket_4 = integer_run.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketInt')
			value_socket_4.subtype = 'NONE'
			value_socket_4.default_value = 0
			value_socket_4.min_value = -2147483648
			value_socket_4.max_value = 2147483647
			value_socket_4.attribute_domain = 'POINT'
			value_socket_4.hide_value = True

			#Socket Group ID
			group_id_socket_5 = integer_run.interface.new_socket(name = "Group ID", in_out='INPUT', socket_type = 'NodeSocketInt')
			group_id_socket_5.subtype = 'NONE'
			group_id_socket_5.default_value = 0
			group_id_socket_5.min_value = -2147483648
			group_id_socket_5.max_value = 2147483647
			group_id_socket_5.attribute_domain = 'POINT'
			group_id_socket_5.description = "Does not restart counting for each Group ID, but does increment by 1 when the Group ID changes"


			#initialize integer_run nodes
			#node Group Output
			group_output_29 = integer_run.nodes.new("NodeGroupOutput")
			group_output_29.name = "Group Output"
			group_output_29.is_active_output = True

			#node Group Input
			group_input_29 = integer_run.nodes.new("NodeGroupInput")
			group_input_29.name = "Group Input"

			#node Group.005
			group_005_1 = integer_run.nodes.new("GeometryNodeGroup")
			group_005_1.name = "Group.005"
			group_005_1.node_tree = offset_integer
			#Socket_1
			group_005_1.inputs[0].default_value = 0
			#Socket_2
			group_005_1.inputs[2].default_value = -1

			#node Compare
			compare_2 = integer_run.nodes.new("FunctionNodeCompare")
			compare_2.name = "Compare"
			compare_2.data_type = 'INT'
			compare_2.mode = 'ELEMENT'
			compare_2.operation = 'NOT_EQUAL'

			#node Accumulate Field
			accumulate_field_1 = integer_run.nodes.new("GeometryNodeAccumulateField")
			accumulate_field_1.name = "Accumulate Field"
			accumulate_field_1.data_type = 'INT'
			accumulate_field_1.domain = 'POINT'
			#Group Index
			accumulate_field_1.inputs[1].default_value = 0

			#node Group.006
			group_006_1 = integer_run.nodes.new("GeometryNodeGroup")
			group_006_1.name = "Group.006"
			group_006_1.node_tree = offset_integer
			#Socket_1
			group_006_1.inputs[0].default_value = 0
			#Socket_2
			group_006_1.inputs[2].default_value = -1

			#node Compare.001
			compare_001_2 = integer_run.nodes.new("FunctionNodeCompare")
			compare_001_2.name = "Compare.001"
			compare_001_2.data_type = 'INT'
			compare_001_2.mode = 'ELEMENT'
			compare_001_2.operation = 'NOT_EQUAL'

			#node Boolean Math
			boolean_math_6 = integer_run.nodes.new("FunctionNodeBooleanMath")
			boolean_math_6.name = "Boolean Math"
			boolean_math_6.operation = 'OR'




			#Set locations
			group_output_29.location = (700.0, 0.0)
			group_input_29.location = (-300.0, -120.0)
			group_005_1.location = (-80.0, 0.0)
			compare_2.location = (80.0, 0.0)
			accumulate_field_1.location = (460.0, -60.0)
			group_006_1.location = (-100.0, -280.0)
			compare_001_2.location = (80.0, -160.0)
			boolean_math_6.location = (240.0, 0.0)

			#Set dimensions
			group_output_29.width, group_output_29.height = 140.0, 100.0
			group_input_29.width, group_input_29.height = 140.0, 100.0
			group_005_1.width, group_005_1.height = 140.0, 100.0
			compare_2.width, compare_2.height = 140.0, 100.0
			accumulate_field_1.width, accumulate_field_1.height = 140.0, 100.0
			group_006_1.width, group_006_1.height = 140.0, 100.0
			compare_001_2.width, compare_001_2.height = 140.0, 100.0
			boolean_math_6.width, boolean_math_6.height = 140.0, 100.0

			#initialize integer_run links
			#group_005_1.Value -> compare_2.A
			integer_run.links.new(group_005_1.outputs[0], compare_2.inputs[2])
			#group_input_29.Value -> group_005_1.Value
			integer_run.links.new(group_input_29.outputs[0], group_005_1.inputs[1])
			#group_input_29.Value -> compare_2.B
			integer_run.links.new(group_input_29.outputs[0], compare_2.inputs[3])
			#boolean_math_6.Boolean -> group_output_29.Is Different
			integer_run.links.new(boolean_math_6.outputs[0], group_output_29.inputs[0])
			#boolean_math_6.Boolean -> accumulate_field_1.Value
			integer_run.links.new(boolean_math_6.outputs[0], accumulate_field_1.inputs[0])
			#accumulate_field_1.Leading -> group_output_29.Group Mask
			integer_run.links.new(accumulate_field_1.outputs[0], group_output_29.inputs[1])
			#group_input_29.Group ID -> group_006_1.Value
			integer_run.links.new(group_input_29.outputs[1], group_006_1.inputs[1])
			#group_006_1.Value -> compare_001_2.B
			integer_run.links.new(group_006_1.outputs[0], compare_001_2.inputs[3])
			#group_input_29.Group ID -> compare_001_2.A
			integer_run.links.new(group_input_29.outputs[1], compare_001_2.inputs[2])
			#compare_2.Result -> boolean_math_6.Boolean
			integer_run.links.new(compare_2.outputs[0], boolean_math_6.inputs[0])
			#compare_001_2.Result -> boolean_math_6.Boolean
			integer_run.links.new(compare_001_2.outputs[0], boolean_math_6.inputs[1])
			return integer_run

		integer_run = integer_run_node_group()

		#initialize atoms_to_curves node group
		def atoms_to_curves_node_group():
			atoms_to_curves = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Atoms to Curves")

			atoms_to_curves.color_tag = 'NONE'
			atoms_to_curves.description = ""


			#atoms_to_curves interface
			#Socket Curves
			curves_socket = atoms_to_curves.interface.new_socket(name = "Curves", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			curves_socket.attribute_domain = 'POINT'

			#Socket Atoms
			atoms_socket_2 = atoms_to_curves.interface.new_socket(name = "Atoms", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			atoms_socket_2.attribute_domain = 'POINT'

			#Socket Selection
			selection_socket_5 = atoms_to_curves.interface.new_socket(name = "Selection", in_out='INPUT', socket_type = 'NodeSocketBool')
			selection_socket_5.attribute_domain = 'POINT'
			selection_socket_5.hide_value = True
			selection_socket_5.description = "Points to maintain and use for splines, non-selected points are removed"

			#Socket Sort Points
			sort_points_socket = atoms_to_curves.interface.new_socket(name = "Sort Points", in_out='INPUT', socket_type = 'NodeSocketBool')
			sort_points_socket.attribute_domain = 'POINT'
			sort_points_socket.description = "Sort points first by atom_id and chain_id before splitting to curves"

			#Socket Distance Cutoff (A)
			distance_cutoff__a__socket = atoms_to_curves.interface.new_socket(name = "Distance Cutoff (A)", in_out='INPUT', socket_type = 'NodeSocketFloat')
			distance_cutoff__a__socket.subtype = 'NONE'
			distance_cutoff__a__socket.default_value = 6.0
			distance_cutoff__a__socket.min_value = -10000.0
			distance_cutoff__a__socket.max_value = 10000.0
			distance_cutoff__a__socket.attribute_domain = 'POINT'


			#initialize atoms_to_curves nodes
			#node Group Output
			group_output_30 = atoms_to_curves.nodes.new("NodeGroupOutput")
			group_output_30.name = "Group Output"
			group_output_30.is_active_output = True

			#node Group Input
			group_input_30 = atoms_to_curves.nodes.new("NodeGroupInput")
			group_input_30.name = "Group Input"
			group_input_30.outputs[3].hide = True

			#node Mesh to Points.001
			mesh_to_points_001 = atoms_to_curves.nodes.new("GeometryNodeMeshToPoints")
			mesh_to_points_001.name = "Mesh to Points.001"
			mesh_to_points_001.mode = 'VERTICES'
			#Position
			mesh_to_points_001.inputs[2].default_value = (0.0, 0.0, 0.0)
			#Radius
			mesh_to_points_001.inputs[3].default_value = 0.05000000074505806

			#node Points to Curves.001
			points_to_curves_001 = atoms_to_curves.nodes.new("GeometryNodePointsToCurves")
			points_to_curves_001.name = "Points to Curves.001"
			#Weight
			points_to_curves_001.inputs[2].default_value = 0.0

			#node Math
			math_7 = atoms_to_curves.nodes.new("ShaderNodeMath")
			math_7.name = "Math"
			math_7.operation = 'ADD'
			math_7.use_clamp = False

			#node Edge Vertices.001
			edge_vertices_001 = atoms_to_curves.nodes.new("GeometryNodeInputMeshEdgeVertices")
			edge_vertices_001.name = "Edge Vertices.001"

			#node Vector Math.001
			vector_math_001_1 = atoms_to_curves.nodes.new("ShaderNodeVectorMath")
			vector_math_001_1.name = "Vector Math.001"
			vector_math_001_1.operation = 'DISTANCE'

			#node Compare.002
			compare_002_3 = atoms_to_curves.nodes.new("FunctionNodeCompare")
			compare_002_3.name = "Compare.002"
			compare_002_3.data_type = 'FLOAT'
			compare_002_3.mode = 'ELEMENT'
			compare_002_3.operation = 'GREATER_THAN'

			#node Group.010
			group_010 = atoms_to_curves.nodes.new("GeometryNodeGroup")
			group_010.name = "Group.010"
			group_010.node_tree = mn_units

			#node Accumulate Field.001
			accumulate_field_001_2 = atoms_to_curves.nodes.new("GeometryNodeAccumulateField")
			accumulate_field_001_2.name = "Accumulate Field.001"
			accumulate_field_001_2.data_type = 'INT'
			accumulate_field_001_2.domain = 'POINT'
			#Group Index
			accumulate_field_001_2.inputs[1].default_value = 0

			#node Frame.003
			frame_003 = atoms_to_curves.nodes.new("NodeFrame")
			frame_003.label = "Unique Group ID between chain and for large gaps in chains"
			frame_003.name = "Frame.003"
			frame_003.label_size = 20
			frame_003.shrink = True

			#node Float to Integer
			float_to_integer = atoms_to_curves.nodes.new("FunctionNodeFloatToInt")
			float_to_integer.name = "Float to Integer"
			float_to_integer.rounding_mode = 'FLOOR'

			#node Sort Elements
			sort_elements = atoms_to_curves.nodes.new("GeometryNodeSortElements")
			sort_elements.name = "Sort Elements"
			sort_elements.domain = 'POINT'
			#Selection
			sort_elements.inputs[1].default_value = True

			#node Group.006
			group_006_2 = atoms_to_curves.nodes.new("GeometryNodeGroup")
			group_006_2.name = "Group.006"
			group_006_2.node_tree = atom_id

			#node Switch
			switch_4 = atoms_to_curves.nodes.new("GeometryNodeSwitch")
			switch_4.name = "Switch"
			switch_4.input_type = 'GEOMETRY'

			#node Group.007
			group_007_1 = atoms_to_curves.nodes.new("GeometryNodeGroup")
			group_007_1.name = "Group.007"
			group_007_1.node_tree = chain_id

			#node Sort Elements.001
			sort_elements_001 = atoms_to_curves.nodes.new("GeometryNodeSortElements")
			sort_elements_001.name = "Sort Elements.001"
			sort_elements_001.domain = 'POINT'
			#Selection
			sort_elements_001.inputs[1].default_value = True
			#Group ID
			sort_elements_001.inputs[2].default_value = 0

			#node Group Input.001
			group_input_001_1 = atoms_to_curves.nodes.new("NodeGroupInput")
			group_input_001_1.name = "Group Input.001"
			group_input_001_1.outputs[0].hide = True
			group_input_001_1.outputs[1].hide = True
			group_input_001_1.outputs[2].hide = True
			group_input_001_1.outputs[4].hide = True

			#node Group
			group_10 = atoms_to_curves.nodes.new("GeometryNodeGroup")
			group_10.name = "Group"
			group_10.node_tree = integer_run
			#Socket_2
			group_10.inputs[1].default_value = 0



			#Set parents
			math_7.parent = frame_003
			edge_vertices_001.parent = frame_003
			vector_math_001_1.parent = frame_003
			compare_002_3.parent = frame_003
			group_010.parent = frame_003
			accumulate_field_001_2.parent = frame_003
			float_to_integer.parent = frame_003
			group_input_001_1.parent = frame_003
			group_10.parent = frame_003

			#Set locations
			group_output_30.location = (780.0, 480.0)
			group_input_30.location = (-520.0, 460.0)
			mesh_to_points_001.location = (-319.9999694824219, 460.0)
			points_to_curves_001.location = (580.0, 480.0)
			math_7.location = (-3340.199951171875, 30.0)
			edge_vertices_001.location = (-4000.199951171875, -130.0)
			vector_math_001_1.location = (-3840.199951171875, -130.0)
			compare_002_3.location = (-3680.199951171875, -130.0)
			group_010.location = (-3840.199951171875, -270.0)
			accumulate_field_001_2.location = (-3520.199951171875, -130.0)
			frame_003.location = (3560.199951171875, 10.0)
			float_to_integer.location = (-3180.199951171875, 30.0)
			sort_elements.location = (40.0, 360.0)
			group_006_2.location = (40.0, 180.0)
			switch_4.location = (220.0, 480.0)
			group_007_1.location = (-140.0, 180.0)
			sort_elements_001.location = (-139.99998474121094, 359.21661376953125)
			group_input_001_1.location = (-4020.199951171875, -330.0)
			group_10.location = (-3520.199951171875, 30.0)

			#Set dimensions
			group_output_30.width, group_output_30.height = 140.0, 100.0
			group_input_30.width, group_input_30.height = 140.0, 100.0
			mesh_to_points_001.width, mesh_to_points_001.height = 140.0, 100.0
			points_to_curves_001.width, points_to_curves_001.height = 140.0, 100.0
			math_7.width, math_7.height = 140.0, 100.0
			edge_vertices_001.width, edge_vertices_001.height = 140.0, 100.0
			vector_math_001_1.width, vector_math_001_1.height = 140.0, 100.0
			compare_002_3.width, compare_002_3.height = 140.0, 100.0
			group_010.width, group_010.height = 140.0, 100.0
			accumulate_field_001_2.width, accumulate_field_001_2.height = 140.0, 100.0
			frame_003.width, frame_003.height = 1040.0, 488.3999938964844
			float_to_integer.width, float_to_integer.height = 140.0, 100.0
			sort_elements.width, sort_elements.height = 140.0, 100.0
			group_006_2.width, group_006_2.height = 140.0, 100.0
			switch_4.width, switch_4.height = 140.0, 100.0
			group_007_1.width, group_007_1.height = 140.0, 100.0
			sort_elements_001.width, sort_elements_001.height = 140.0, 100.0
			group_input_001_1.width, group_input_001_1.height = 140.0, 100.0
			group_10.width, group_10.height = 140.0, 100.0

			#initialize atoms_to_curves links
			#accumulate_field_001_2.Trailing -> math_7.Value
			atoms_to_curves.links.new(accumulate_field_001_2.outputs[1], math_7.inputs[1])
			#edge_vertices_001.Position 1 -> vector_math_001_1.Vector
			atoms_to_curves.links.new(edge_vertices_001.outputs[2], vector_math_001_1.inputs[0])
			#math_7.Value -> float_to_integer.Float
			atoms_to_curves.links.new(math_7.outputs[0], float_to_integer.inputs[0])
			#compare_002_3.Result -> accumulate_field_001_2.Value
			atoms_to_curves.links.new(compare_002_3.outputs[0], accumulate_field_001_2.inputs[0])
			#edge_vertices_001.Position 2 -> vector_math_001_1.Vector
			atoms_to_curves.links.new(edge_vertices_001.outputs[3], vector_math_001_1.inputs[1])
			#group_010.Angstrom -> compare_002_3.B
			atoms_to_curves.links.new(group_010.outputs[0], compare_002_3.inputs[1])
			#float_to_integer.Integer -> points_to_curves_001.Curve Group ID
			atoms_to_curves.links.new(float_to_integer.outputs[0], points_to_curves_001.inputs[1])
			#vector_math_001_1.Value -> compare_002_3.A
			atoms_to_curves.links.new(vector_math_001_1.outputs[1], compare_002_3.inputs[0])
			#group_input_30.Atoms -> mesh_to_points_001.Mesh
			atoms_to_curves.links.new(group_input_30.outputs[0], mesh_to_points_001.inputs[0])
			#group_input_30.Selection -> mesh_to_points_001.Selection
			atoms_to_curves.links.new(group_input_30.outputs[1], mesh_to_points_001.inputs[1])
			#points_to_curves_001.Curves -> group_output_30.Curves
			atoms_to_curves.links.new(points_to_curves_001.outputs[0], group_output_30.inputs[0])
			#mesh_to_points_001.Points -> switch_4.False
			atoms_to_curves.links.new(mesh_to_points_001.outputs[0], switch_4.inputs[1])
			#sort_elements_001.Geometry -> sort_elements.Geometry
			atoms_to_curves.links.new(sort_elements_001.outputs[0], sort_elements.inputs[0])
			#sort_elements.Geometry -> switch_4.True
			atoms_to_curves.links.new(sort_elements.outputs[0], switch_4.inputs[2])
			#switch_4.Output -> points_to_curves_001.Points
			atoms_to_curves.links.new(switch_4.outputs[0], points_to_curves_001.inputs[0])
			#group_006_2.atom_id -> sort_elements.Sort Weight
			atoms_to_curves.links.new(group_006_2.outputs[0], sort_elements.inputs[3])
			#group_007_1.chain_id -> sort_elements.Group ID
			atoms_to_curves.links.new(group_007_1.outputs[0], sort_elements.inputs[2])
			#group_input_30.Sort Points -> switch_4.Switch
			atoms_to_curves.links.new(group_input_30.outputs[2], switch_4.inputs[0])
			#group_input_001_1.Distance Cutoff (A) -> group_010.Value
			atoms_to_curves.links.new(group_input_001_1.outputs[3], group_010.inputs[0])
			#group_10.Group Mask -> math_7.Value
			atoms_to_curves.links.new(group_10.outputs[1], math_7.inputs[0])
			#group_007_1.chain_id -> group_10.Value
			atoms_to_curves.links.new(group_007_1.outputs[0], group_10.inputs[0])
			#mesh_to_points_001.Points -> sort_elements_001.Geometry
			atoms_to_curves.links.new(mesh_to_points_001.outputs[0], sort_elements_001.inputs[0])
			#group_007_1.chain_id -> sort_elements_001.Sort Weight
			atoms_to_curves.links.new(group_007_1.outputs[0], sort_elements_001.inputs[3])
			return atoms_to_curves

		atoms_to_curves = atoms_to_curves_node_group()

		#initialize attribute_run node group
		def attribute_run_node_group():
			attribute_run = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Attribute Run")

			attribute_run.color_tag = 'CONVERTER'
			attribute_run.description = "Group mask increments whenever the attribute or the Group ID changes"


			#attribute_run interface
			#Socket Is Different
			is_different_socket_1 = attribute_run.interface.new_socket(name = "Is Different", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			is_different_socket_1.attribute_domain = 'POINT'

			#Socket Group Mask
			group_mask_socket_1 = attribute_run.interface.new_socket(name = "Group Mask", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			group_mask_socket_1.subtype = 'NONE'
			group_mask_socket_1.default_value = 0
			group_mask_socket_1.min_value = -2147483648
			group_mask_socket_1.max_value = 2147483647
			group_mask_socket_1.attribute_domain = 'POINT'

			#Socket Name
			name_socket_2 = attribute_run.interface.new_socket(name = "Name", in_out='INPUT', socket_type = 'NodeSocketString')
			name_socket_2.attribute_domain = 'POINT'

			#Socket Group ID
			group_id_socket_6 = attribute_run.interface.new_socket(name = "Group ID", in_out='INPUT', socket_type = 'NodeSocketInt')
			group_id_socket_6.subtype = 'NONE'
			group_id_socket_6.default_value = 0
			group_id_socket_6.min_value = -2147483648
			group_id_socket_6.max_value = 2147483647
			group_id_socket_6.attribute_domain = 'POINT'


			#initialize attribute_run nodes
			#node Group Output
			group_output_31 = attribute_run.nodes.new("NodeGroupOutput")
			group_output_31.name = "Group Output"
			group_output_31.is_active_output = True

			#node Group Input
			group_input_31 = attribute_run.nodes.new("NodeGroupInput")
			group_input_31.name = "Group Input"

			#node Group.117
			group_117 = attribute_run.nodes.new("GeometryNodeGroup")
			group_117.name = "Group.117"
			group_117.node_tree = integer_run

			#node Named Attribute
			named_attribute_3 = attribute_run.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_3.name = "Named Attribute"
			named_attribute_3.data_type = 'INT'




			#Set locations
			group_output_31.location = (85.79051208496094, 14.253557205200195)
			group_input_31.location = (-420.0, -60.0)
			group_117.location = (-100.0, 20.0)
			named_attribute_3.location = (-260.0, 20.0)

			#Set dimensions
			group_output_31.width, group_output_31.height = 140.0, 100.0
			group_input_31.width, group_input_31.height = 140.0, 100.0
			group_117.width, group_117.height = 140.0, 100.0
			named_attribute_3.width, named_attribute_3.height = 140.0, 100.0

			#initialize attribute_run links
			#group_117.Is Different -> group_output_31.Is Different
			attribute_run.links.new(group_117.outputs[0], group_output_31.inputs[0])
			#group_117.Group Mask -> group_output_31.Group Mask
			attribute_run.links.new(group_117.outputs[1], group_output_31.inputs[1])
			#group_input_31.Name -> named_attribute_3.Name
			attribute_run.links.new(group_input_31.outputs[0], named_attribute_3.inputs[0])
			#named_attribute_3.Attribute -> group_117.Value
			attribute_run.links.new(named_attribute_3.outputs[0], group_117.inputs[0])
			#group_input_31.Group ID -> group_117.Group ID
			attribute_run.links.new(group_input_31.outputs[1], group_117.inputs[1])
			return attribute_run

		attribute_run = attribute_run_node_group()

		#initialize _setup__tmp_attributes node group
		def _setup__tmp_attributes_node_group():
			_setup__tmp_attributes = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".Setup .tmp attributes")

			_setup__tmp_attributes.color_tag = 'NONE'
			_setup__tmp_attributes.description = ""


			#_setup__tmp_attributes interface
			#Socket Geometry
			geometry_socket_2 = _setup__tmp_attributes.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			geometry_socket_2.attribute_domain = 'POINT'

			#Socket Geometry
			geometry_socket_3 = _setup__tmp_attributes.interface.new_socket(name = "Geometry", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			geometry_socket_3.attribute_domain = 'POINT'


			#initialize _setup__tmp_attributes nodes
			#node Group Output
			group_output_32 = _setup__tmp_attributes.nodes.new("NodeGroupOutput")
			group_output_32.name = "Group Output"
			group_output_32.is_active_output = True

			#node Group Input
			group_input_32 = _setup__tmp_attributes.nodes.new("NodeGroupInput")
			group_input_32.name = "Group Input"

			#node Store Named Attribute.020
			store_named_attribute_020 = _setup__tmp_attributes.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_020.name = "Store Named Attribute.020"
			store_named_attribute_020.data_type = 'INT'
			store_named_attribute_020.domain = 'POINT'
			#Selection
			store_named_attribute_020.inputs[1].default_value = True
			#Name
			store_named_attribute_020.inputs[2].default_value = "tmp_ss_ID"

			#node Group.004
			group_004_1 = _setup__tmp_attributes.nodes.new("GeometryNodeGroup")
			group_004_1.name = "Group.004"
			group_004_1.node_tree = attribute_run
			#Socket_4
			group_004_1.inputs[0].default_value = "sec_struct"

			#node Curve of Point
			curve_of_point = _setup__tmp_attributes.nodes.new("GeometryNodeCurveOfPoint")
			curve_of_point.name = "Curve of Point"
			#Point Index
			curve_of_point.inputs[0].default_value = 0

			#node Store Named Attribute.021
			store_named_attribute_021 = _setup__tmp_attributes.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_021.name = "Store Named Attribute.021"
			store_named_attribute_021.data_type = 'INT'
			store_named_attribute_021.domain = 'POINT'
			#Selection
			store_named_attribute_021.inputs[1].default_value = True
			#Name
			store_named_attribute_021.inputs[2].default_value = "tmp_ss_size"

			#node Group.002
			group_002_4 = _setup__tmp_attributes.nodes.new("GeometryNodeGroup")
			group_002_4.name = "Group.002"
			group_002_4.node_tree = group_info

			#node Named Attribute
			named_attribute_4 = _setup__tmp_attributes.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_4.name = "Named Attribute"
			named_attribute_4.data_type = 'INT'
			#Name
			named_attribute_4.inputs[0].default_value = "tmp_ss_ID"

			#node Capture Attribute
			capture_attribute_1 = _setup__tmp_attributes.nodes.new("GeometryNodeCaptureAttribute")
			capture_attribute_1.name = "Capture Attribute"
			capture_attribute_1.active_index = 2
			capture_attribute_1.capture_items.clear()
			capture_attribute_1.capture_items.new('FLOAT', "Is First")
			capture_attribute_1.capture_items["Is First"].data_type = 'BOOLEAN'
			capture_attribute_1.capture_items.new('FLOAT', "Is Last")
			capture_attribute_1.capture_items["Is Last"].data_type = 'BOOLEAN'
			capture_attribute_1.capture_items.new('FLOAT', "Size")
			capture_attribute_1.capture_items["Size"].data_type = 'INT'
			capture_attribute_1.domain = 'POINT'

			#node Store Named Attribute.022
			store_named_attribute_022 = _setup__tmp_attributes.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_022.name = "Store Named Attribute.022"
			store_named_attribute_022.data_type = 'BOOLEAN'
			store_named_attribute_022.domain = 'POINT'
			#Selection
			store_named_attribute_022.inputs[1].default_value = True
			#Name
			store_named_attribute_022.inputs[2].default_value = "tmp_ss_first"

			#node Store Named Attribute.023
			store_named_attribute_023 = _setup__tmp_attributes.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_023.name = "Store Named Attribute.023"
			store_named_attribute_023.data_type = 'BOOLEAN'
			store_named_attribute_023.domain = 'POINT'
			#Selection
			store_named_attribute_023.inputs[1].default_value = True
			#Name
			store_named_attribute_023.inputs[2].default_value = "tmp_ss_last"

			#node Curve of Point.001
			curve_of_point_001 = _setup__tmp_attributes.nodes.new("GeometryNodeCurveOfPoint")
			curve_of_point_001.name = "Curve of Point.001"
			#Point Index
			curve_of_point_001.inputs[0].default_value = 0

			#node Store Named Attribute.024
			store_named_attribute_024 = _setup__tmp_attributes.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_024.name = "Store Named Attribute.024"
			store_named_attribute_024.data_type = 'INT'
			store_named_attribute_024.domain = 'POINT'
			#Selection
			store_named_attribute_024.inputs[1].default_value = True
			#Name
			store_named_attribute_024.inputs[2].default_value = "tmp_idx_curve"




			#Set locations
			group_output_32.location = (620.0, 180.0)
			group_input_32.location = (-569.5999145507812, 180.0)
			store_named_attribute_020.location = (-379.6000061035156, 180.0)
			group_004_1.location = (-380.00006103515625, -40.0)
			curve_of_point.location = (-380.00006103515625, -200.0)
			store_named_attribute_021.location = (-40.0, 180.0)
			group_002_4.location = (-220.0, 0.0)
			named_attribute_4.location = (-220.0, -220.0)
			capture_attribute_1.location = (-220.0, 180.0)
			store_named_attribute_022.location = (120.0, 180.0)
			store_named_attribute_023.location = (280.0, 180.0)
			curve_of_point_001.location = (280.0, -20.0)
			store_named_attribute_024.location = (440.0, 180.0)

			#Set dimensions
			group_output_32.width, group_output_32.height = 140.0, 100.0
			group_input_32.width, group_input_32.height = 140.0, 100.0
			store_named_attribute_020.width, store_named_attribute_020.height = 140.0, 100.0
			group_004_1.width, group_004_1.height = 140.0, 100.0
			curve_of_point.width, curve_of_point.height = 140.0, 100.0
			store_named_attribute_021.width, store_named_attribute_021.height = 140.0, 100.0
			group_002_4.width, group_002_4.height = 140.0, 100.0
			named_attribute_4.width, named_attribute_4.height = 140.0, 100.0
			capture_attribute_1.width, capture_attribute_1.height = 140.0, 100.0
			store_named_attribute_022.width, store_named_attribute_022.height = 140.0, 100.0
			store_named_attribute_023.width, store_named_attribute_023.height = 140.0, 100.0
			curve_of_point_001.width, curve_of_point_001.height = 140.0, 100.0
			store_named_attribute_024.width, store_named_attribute_024.height = 140.0, 100.0

			#initialize _setup__tmp_attributes links
			#capture_attribute_1.Geometry -> store_named_attribute_021.Geometry
			_setup__tmp_attributes.links.new(capture_attribute_1.outputs[0], store_named_attribute_021.inputs[0])
			#named_attribute_4.Attribute -> group_002_4.Group ID
			_setup__tmp_attributes.links.new(named_attribute_4.outputs[0], group_002_4.inputs[0])
			#group_004_1.Group Mask -> store_named_attribute_020.Value
			_setup__tmp_attributes.links.new(group_004_1.outputs[1], store_named_attribute_020.inputs[3])
			#curve_of_point.Curve Index -> group_004_1.Group ID
			_setup__tmp_attributes.links.new(curve_of_point.outputs[0], group_004_1.inputs[1])
			#group_input_32.Geometry -> store_named_attribute_020.Geometry
			_setup__tmp_attributes.links.new(group_input_32.outputs[0], store_named_attribute_020.inputs[0])
			#store_named_attribute_024.Geometry -> group_output_32.Geometry
			_setup__tmp_attributes.links.new(store_named_attribute_024.outputs[0], group_output_32.inputs[0])
			#store_named_attribute_020.Geometry -> capture_attribute_1.Geometry
			_setup__tmp_attributes.links.new(store_named_attribute_020.outputs[0], capture_attribute_1.inputs[0])
			#group_002_4.Is First -> capture_attribute_1.Is First
			_setup__tmp_attributes.links.new(group_002_4.outputs[0], capture_attribute_1.inputs[1])
			#group_002_4.Is Last -> capture_attribute_1.Is Last
			_setup__tmp_attributes.links.new(group_002_4.outputs[2], capture_attribute_1.inputs[2])
			#group_002_4.Size -> capture_attribute_1.Size
			_setup__tmp_attributes.links.new(group_002_4.outputs[5], capture_attribute_1.inputs[3])
			#capture_attribute_1.Size -> store_named_attribute_021.Value
			_setup__tmp_attributes.links.new(capture_attribute_1.outputs[3], store_named_attribute_021.inputs[3])
			#store_named_attribute_021.Geometry -> store_named_attribute_022.Geometry
			_setup__tmp_attributes.links.new(store_named_attribute_021.outputs[0], store_named_attribute_022.inputs[0])
			#store_named_attribute_022.Geometry -> store_named_attribute_023.Geometry
			_setup__tmp_attributes.links.new(store_named_attribute_022.outputs[0], store_named_attribute_023.inputs[0])
			#capture_attribute_1.Is First -> store_named_attribute_022.Value
			_setup__tmp_attributes.links.new(capture_attribute_1.outputs[1], store_named_attribute_022.inputs[3])
			#capture_attribute_1.Is Last -> store_named_attribute_023.Value
			_setup__tmp_attributes.links.new(capture_attribute_1.outputs[2], store_named_attribute_023.inputs[3])
			#store_named_attribute_023.Geometry -> store_named_attribute_024.Geometry
			_setup__tmp_attributes.links.new(store_named_attribute_023.outputs[0], store_named_attribute_024.inputs[0])
			#curve_of_point_001.Curve Index -> store_named_attribute_024.Value
			_setup__tmp_attributes.links.new(curve_of_point_001.outputs[0], store_named_attribute_024.inputs[3])
			return _setup__tmp_attributes

		_setup__tmp_attributes = _setup__tmp_attributes_node_group()

		#initialize _atoms_to_ca_splines node group
		def _atoms_to_ca_splines_node_group():
			_atoms_to_ca_splines = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".Atoms to CA Splines")

			_atoms_to_ca_splines.color_tag = 'NONE'
			_atoms_to_ca_splines.description = ""

			_atoms_to_ca_splines.is_modifier = True

			#_atoms_to_ca_splines interface
			#Socket CA Splines
			ca_splines_socket = _atoms_to_ca_splines.interface.new_socket(name = "CA Splines", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			ca_splines_socket.attribute_domain = 'POINT'

			#Socket Atoms
			atoms_socket_3 = _atoms_to_ca_splines.interface.new_socket(name = "Atoms", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			atoms_socket_3.attribute_domain = 'POINT'
			atoms_socket_3.description = "Atomic geometry that contains vertices and edges"

			#Socket Selection
			selection_socket_6 = _atoms_to_ca_splines.interface.new_socket(name = "Selection", in_out='INPUT', socket_type = 'NodeSocketBool')
			selection_socket_6.attribute_domain = 'POINT'
			selection_socket_6.hide_value = True
			selection_socket_6.description = "Selection of atoms to apply this node to"

			#Socket BS Smoothing
			bs_smoothing_socket = _atoms_to_ca_splines.interface.new_socket(name = "BS Smoothing", in_out='INPUT', socket_type = 'NodeSocketFloat')
			bs_smoothing_socket.subtype = 'FACTOR'
			bs_smoothing_socket.default_value = 1.0
			bs_smoothing_socket.min_value = 0.0
			bs_smoothing_socket.max_value = 1.0
			bs_smoothing_socket.attribute_domain = 'POINT'


			#initialize _atoms_to_ca_splines nodes
			#node Frame.002
			frame_002 = _atoms_to_ca_splines.nodes.new("NodeFrame")
			frame_002.label = "Turn backboen points to curves"
			frame_002.name = "Frame.002"
			frame_002.label_size = 20
			frame_002.shrink = True

			#node Group Input.001
			group_input_001_2 = _atoms_to_ca_splines.nodes.new("NodeGroupInput")
			group_input_001_2.name = "Group Input.001"
			group_input_001_2.outputs[0].hide = True
			group_input_001_2.outputs[1].hide = True
			group_input_001_2.outputs[3].hide = True

			#node Group Output
			group_output_33 = _atoms_to_ca_splines.nodes.new("NodeGroupOutput")
			group_output_33.name = "Group Output"
			group_output_33.is_active_output = True

			#node Group
			group_11 = _atoms_to_ca_splines.nodes.new("GeometryNodeGroup")
			group_11.name = "Group"
			group_11.node_tree = _bs_smooth
			#Input_3
			group_11.inputs[2].default_value = 3

			#node Group Input
			group_input_33 = _atoms_to_ca_splines.nodes.new("NodeGroupInput")
			group_input_33.name = "Group Input"

			#node Store Named Attribute.019
			store_named_attribute_019 = _atoms_to_ca_splines.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_019.name = "Store Named Attribute.019"
			store_named_attribute_019.data_type = 'INT'
			store_named_attribute_019.domain = 'POINT'
			#Selection
			store_named_attribute_019.inputs[1].default_value = True
			#Name
			store_named_attribute_019.inputs[2].default_value = "tmp_idx"

			#node Index.002
			index_002 = _atoms_to_ca_splines.nodes.new("GeometryNodeInputIndex")
			index_002.name = "Index.002"

			#node Group.001
			group_001_7 = _atoms_to_ca_splines.nodes.new("GeometryNodeGroup")
			group_001_7.name = "Group.001"
			group_001_7.node_tree = is_alpha_carbon
			#Socket_3
			group_001_7.inputs[1].default_value = False

			#node Group.006
			group_006_3 = _atoms_to_ca_splines.nodes.new("GeometryNodeGroup")
			group_006_3.name = "Group.006"
			group_006_3.node_tree = _mn_topo_assign_backbone

			#node Group.003
			group_003_1 = _atoms_to_ca_splines.nodes.new("GeometryNodeGroup")
			group_003_1.name = "Group.003"
			group_003_1.node_tree = backbone_vectors

			#node Group.011
			group_011 = _atoms_to_ca_splines.nodes.new("GeometryNodeGroup")
			group_011.name = "Group.011"
			group_011.node_tree = atoms_to_curves
			#Socket_3
			group_011.inputs[2].default_value = False
			#Socket_4
			group_011.inputs[3].default_value = 0.3000001907348633

			#node Set Curve Normal
			set_curve_normal = _atoms_to_ca_splines.nodes.new("GeometryNodeSetCurveNormal")
			set_curve_normal.name = "Set Curve Normal"
			set_curve_normal.mode = 'FREE'
			#Selection
			set_curve_normal.inputs[1].default_value = True

			#node Set Spline Type
			set_spline_type = _atoms_to_ca_splines.nodes.new("GeometryNodeCurveSplineType")
			set_spline_type.name = "Set Spline Type"
			set_spline_type.spline_type = 'BEZIER'
			#Selection
			set_spline_type.inputs[1].default_value = True

			#node Set Handle Type
			set_handle_type = _atoms_to_ca_splines.nodes.new("GeometryNodeCurveSetHandles")
			set_handle_type.name = "Set Handle Type"
			set_handle_type.handle_type = 'AUTO'
			set_handle_type.mode = {'LEFT', 'RIGHT'}
			#Selection
			set_handle_type.inputs[1].default_value = True

			#node Group.005
			group_005_2 = _atoms_to_ca_splines.nodes.new("GeometryNodeGroup")
			group_005_2.name = "Group.005"
			group_005_2.node_tree = _setup__tmp_attributes



			#Set parents
			group_001_7.parent = frame_002
			group_006_3.parent = frame_002
			group_011.parent = frame_002

			#Set locations
			frame_002.location = (1910.0, 100.0)
			group_input_001_2.location = (-1120.0, 740.0)
			group_output_33.location = (-520.0, 900.0)
			group_11.location = (-1120.0, 900.0)
			group_input_33.location = (-2320.0, 800.0)
			store_named_attribute_019.location = (-1640.0, 900.0)
			index_002.location = (-1640.0, 700.0)
			group_001_7.location = (-4010.000244140625, 640.0)
			group_006_3.location = (-4020.0, 800.0)
			group_003_1.location = (-1280.0, 740.0)
			group_011.location = (-3744.800048828125, 800.0)
			set_curve_normal.location = (-1280.0, 900.0)
			set_spline_type.location = (-840.0, 900.0)
			set_handle_type.location = (-680.0, 900.0)
			group_005_2.location = (-1460.0, 900.0)

			#Set dimensions
			frame_002.width, frame_002.height = 475.199951171875, 348.4000244140625
			group_input_001_2.width, group_input_001_2.height = 140.0, 100.0
			group_output_33.width, group_output_33.height = 140.0, 100.0
			group_11.width, group_11.height = 245.719482421875, 100.0
			group_input_33.width, group_input_33.height = 140.0, 100.0
			store_named_attribute_019.width, store_named_attribute_019.height = 140.0, 100.0
			index_002.width, index_002.height = 140.0, 100.0
			group_001_7.width, group_001_7.height = 140.0, 100.0
			group_006_3.width, group_006_3.height = 206.7611083984375, 100.0
			group_003_1.width, group_003_1.height = 142.91567993164062, 100.0
			group_011.width, group_011.height = 140.0, 100.0
			set_curve_normal.width, set_curve_normal.height = 140.0, 100.0
			set_spline_type.width, set_spline_type.height = 140.0, 100.0
			set_handle_type.width, set_handle_type.height = 140.0, 100.0
			group_005_2.width, group_005_2.height = 140.0, 100.0

			#initialize _atoms_to_ca_splines links
			#set_curve_normal.Curve -> group_11.Geometry
			_atoms_to_ca_splines.links.new(set_curve_normal.outputs[0], group_11.inputs[0])
			#group_input_001_2.BS Smoothing -> group_11.Factor
			_atoms_to_ca_splines.links.new(group_input_001_2.outputs[2], group_11.inputs[1])
			#index_002.Index -> store_named_attribute_019.Value
			_atoms_to_ca_splines.links.new(index_002.outputs[0], store_named_attribute_019.inputs[3])
			#group_input_33.Atoms -> group_006_3.Atoms
			_atoms_to_ca_splines.links.new(group_input_33.outputs[0], group_006_3.inputs[0])
			#group_011.Curves -> store_named_attribute_019.Geometry
			_atoms_to_ca_splines.links.new(group_011.outputs[0], store_named_attribute_019.inputs[0])
			#group_input_33.Selection -> group_001_7.And
			_atoms_to_ca_splines.links.new(group_input_33.outputs[1], group_001_7.inputs[0])
			#group_001_7.Selection -> group_011.Selection
			_atoms_to_ca_splines.links.new(group_001_7.outputs[0], group_011.inputs[1])
			#group_006_3.Atoms -> group_011.Atoms
			_atoms_to_ca_splines.links.new(group_006_3.outputs[0], group_011.inputs[0])
			#set_handle_type.Curve -> group_output_33.CA Splines
			_atoms_to_ca_splines.links.new(set_handle_type.outputs[0], group_output_33.inputs[0])
			#group_005_2.Geometry -> set_curve_normal.Curve
			_atoms_to_ca_splines.links.new(group_005_2.outputs[0], set_curve_normal.inputs[0])
			#group_003_1.Normal -> set_curve_normal.Normal
			_atoms_to_ca_splines.links.new(group_003_1.outputs[0], set_curve_normal.inputs[2])
			#group_11.Geometry -> set_spline_type.Curve
			_atoms_to_ca_splines.links.new(group_11.outputs[0], set_spline_type.inputs[0])
			#set_spline_type.Curve -> set_handle_type.Curve
			_atoms_to_ca_splines.links.new(set_spline_type.outputs[0], set_handle_type.inputs[0])
			#store_named_attribute_019.Geometry -> group_005_2.Geometry
			_atoms_to_ca_splines.links.new(store_named_attribute_019.outputs[0], group_005_2.inputs[0])
			return _atoms_to_ca_splines

		_atoms_to_ca_splines = _atoms_to_ca_splines_node_group()

		#initialize _curve_profile_backup node group
		def _curve_profile_backup_node_group():
			_curve_profile_backup = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".curve_profile_backup")

			_curve_profile_backup.color_tag = 'GEOMETRY'
			_curve_profile_backup.description = ""

			_curve_profile_backup.is_modifier = True

			#_curve_profile_backup interface
			#Socket Output
			output_socket_1 = _curve_profile_backup.interface.new_socket(name = "Output", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			output_socket_1.attribute_domain = 'POINT'

			#Socket Input
			input_socket = _curve_profile_backup.interface.new_socket(name = "Input", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			input_socket.attribute_domain = 'POINT'

			#Socket Resolution
			resolution_socket = _curve_profile_backup.interface.new_socket(name = "Resolution", in_out='INPUT', socket_type = 'NodeSocketInt')
			resolution_socket.subtype = 'NONE'
			resolution_socket.default_value = 12
			resolution_socket.min_value = 3
			resolution_socket.max_value = 512
			resolution_socket.attribute_domain = 'POINT'

			#Socket Radius (A)
			radius__a__socket = _curve_profile_backup.interface.new_socket(name = "Radius (A)", in_out='INPUT', socket_type = 'NodeSocketFloat')
			radius__a__socket.subtype = 'NONE'
			radius__a__socket.default_value = 0.009999999776482582
			radius__a__socket.min_value = 0.0
			radius__a__socket.max_value = 3.4028234663852886e+38
			radius__a__socket.attribute_domain = 'POINT'

			#Socket Rotation
			rotation_socket = _curve_profile_backup.interface.new_socket(name = "Rotation", in_out='INPUT', socket_type = 'NodeSocketFloat')
			rotation_socket.subtype = 'NONE'
			rotation_socket.default_value = 0.0
			rotation_socket.min_value = -10000.0
			rotation_socket.max_value = 10000.0
			rotation_socket.attribute_domain = 'POINT'


			#initialize _curve_profile_backup nodes
			#node Group Output
			group_output_34 = _curve_profile_backup.nodes.new("NodeGroupOutput")
			group_output_34.name = "Group Output"
			group_output_34.is_active_output = True

			#node Compare
			compare_3 = _curve_profile_backup.nodes.new("FunctionNodeCompare")
			compare_3.name = "Compare"
			compare_3.hide = True
			compare_3.data_type = 'INT'
			compare_3.mode = 'ELEMENT'
			compare_3.operation = 'GREATER_THAN'
			#B_INT
			compare_3.inputs[3].default_value = 0

			#node Switch
			switch_5 = _curve_profile_backup.nodes.new("GeometryNodeSwitch")
			switch_5.name = "Switch"
			switch_5.input_type = 'GEOMETRY'

			#node Domain Size
			domain_size = _curve_profile_backup.nodes.new("GeometryNodeAttributeDomainSize")
			domain_size.name = "Domain Size"
			domain_size.component = 'CURVE'

			#node Curve Circle
			curve_circle = _curve_profile_backup.nodes.new("GeometryNodeCurvePrimitiveCircle")
			curve_circle.name = "Curve Circle"
			curve_circle.mode = 'RADIUS'

			#node Transform Geometry.001
			transform_geometry_001 = _curve_profile_backup.nodes.new("GeometryNodeTransform")
			transform_geometry_001.name = "Transform Geometry.001"
			transform_geometry_001.mode = 'COMPONENTS'
			#Translation
			transform_geometry_001.inputs[1].default_value = (0.0, 0.0, 0.0)
			#Scale
			transform_geometry_001.inputs[3].default_value = (1.0, 1.0, 1.0)

			#node Group Input
			group_input_34 = _curve_profile_backup.nodes.new("NodeGroupInput")
			group_input_34.name = "Group Input"

			#node Group
			group_12 = _curve_profile_backup.nodes.new("GeometryNodeGroup")
			group_12.name = "Group"
			group_12.hide = True
			group_12.node_tree = mn_units

			#node Axis Angle to Rotation
			axis_angle_to_rotation = _curve_profile_backup.nodes.new("FunctionNodeAxisAngleToRotation")
			axis_angle_to_rotation.name = "Axis Angle to Rotation"
			#Axis
			axis_angle_to_rotation.inputs[0].default_value = (0.0, 0.0, 1.0)

			#node Math
			math_8 = _curve_profile_backup.nodes.new("ShaderNodeMath")
			math_8.name = "Math"
			math_8.operation = 'ADD'
			math_8.use_clamp = False

			#node Math.001
			math_001_1 = _curve_profile_backup.nodes.new("ShaderNodeMath")
			math_001_1.name = "Math.001"
			math_001_1.operation = 'RADIANS'
			math_001_1.use_clamp = False
			#Value
			math_001_1.inputs[0].default_value = 45.0




			#Set locations
			group_output_34.location = (380.0, 0.0)
			compare_3.location = (-400.0, 80.0)
			switch_5.location = (180.0, 120.0)
			domain_size.location = (-400.0, 40.0)
			curve_circle.location = (20.0, -60.0)
			transform_geometry_001.location = (180.0, -60.0)
			group_input_34.location = (-392.2209777832031, -102.58642578125)
			group_12.location = (-160.0, -180.0)
			axis_angle_to_rotation.location = (20.0, -220.0)
			math_8.location = (-160.0, -220.0)
			math_001_1.location = (-340.0, -340.0)

			#Set dimensions
			group_output_34.width, group_output_34.height = 140.0, 100.0
			compare_3.width, compare_3.height = 137.39459228515625, 100.0
			switch_5.width, switch_5.height = 140.0, 100.0
			domain_size.width, domain_size.height = 140.0, 100.0
			curve_circle.width, curve_circle.height = 140.0, 100.0
			transform_geometry_001.width, transform_geometry_001.height = 140.0, 100.0
			group_input_34.width, group_input_34.height = 140.0, 100.0
			group_12.width, group_12.height = 140.0, 100.0
			axis_angle_to_rotation.width, axis_angle_to_rotation.height = 140.0, 100.0
			math_8.width, math_8.height = 140.0, 100.0
			math_001_1.width, math_001_1.height = 140.0, 100.0

			#initialize _curve_profile_backup links
			#domain_size.Point Count -> compare_3.A
			_curve_profile_backup.links.new(domain_size.outputs[0], compare_3.inputs[2])
			#group_input_34.Input -> domain_size.Geometry
			_curve_profile_backup.links.new(group_input_34.outputs[0], domain_size.inputs[0])
			#curve_circle.Curve -> transform_geometry_001.Geometry
			_curve_profile_backup.links.new(curve_circle.outputs[0], transform_geometry_001.inputs[0])
			#compare_3.Result -> switch_5.Switch
			_curve_profile_backup.links.new(compare_3.outputs[0], switch_5.inputs[0])
			#group_input_34.Input -> switch_5.True
			_curve_profile_backup.links.new(group_input_34.outputs[0], switch_5.inputs[2])
			#transform_geometry_001.Geometry -> switch_5.False
			_curve_profile_backup.links.new(transform_geometry_001.outputs[0], switch_5.inputs[1])
			#switch_5.Output -> group_output_34.Output
			_curve_profile_backup.links.new(switch_5.outputs[0], group_output_34.inputs[0])
			#group_input_34.Resolution -> curve_circle.Resolution
			_curve_profile_backup.links.new(group_input_34.outputs[1], curve_circle.inputs[0])
			#group_input_34.Radius (A) -> group_12.Value
			_curve_profile_backup.links.new(group_input_34.outputs[2], group_12.inputs[0])
			#group_12.Angstrom -> curve_circle.Radius
			_curve_profile_backup.links.new(group_12.outputs[0], curve_circle.inputs[4])
			#axis_angle_to_rotation.Rotation -> transform_geometry_001.Rotation
			_curve_profile_backup.links.new(axis_angle_to_rotation.outputs[0], transform_geometry_001.inputs[2])
			#group_input_34.Rotation -> math_8.Value
			_curve_profile_backup.links.new(group_input_34.outputs[3], math_8.inputs[0])
			#math_8.Value -> axis_angle_to_rotation.Angle
			_curve_profile_backup.links.new(math_8.outputs[0], axis_angle_to_rotation.inputs[1])
			#math_001_1.Value -> math_8.Value
			_curve_profile_backup.links.new(math_001_1.outputs[0], math_8.inputs[1])
			return _curve_profile_backup

		_curve_profile_backup = _curve_profile_backup_node_group()

		#initialize sample_position node group
		def sample_position_node_group():
			sample_position = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Sample Position")

			sample_position.color_tag = 'GEOMETRY'
			sample_position.description = ""


			#sample_position interface
			#Socket Position
			position_socket_3 = sample_position.interface.new_socket(name = "Position", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			position_socket_3.subtype = 'NONE'
			position_socket_3.default_value = (0.0, 0.0, 0.0)
			position_socket_3.min_value = -3.4028234663852886e+38
			position_socket_3.max_value = 3.4028234663852886e+38
			position_socket_3.attribute_domain = 'POINT'

			#Socket Geometry
			geometry_socket_4 = sample_position.interface.new_socket(name = "Geometry", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			geometry_socket_4.attribute_domain = 'POINT'

			#Socket Index
			index_socket_7 = sample_position.interface.new_socket(name = "Index", in_out='INPUT', socket_type = 'NodeSocketInt')
			index_socket_7.subtype = 'NONE'
			index_socket_7.default_value = 0
			index_socket_7.min_value = -2147483648
			index_socket_7.max_value = 2147483647
			index_socket_7.attribute_domain = 'POINT'


			#initialize sample_position nodes
			#node Group Output
			group_output_35 = sample_position.nodes.new("NodeGroupOutput")
			group_output_35.name = "Group Output"
			group_output_35.is_active_output = True

			#node Group Input
			group_input_35 = sample_position.nodes.new("NodeGroupInput")
			group_input_35.name = "Group Input"

			#node Sample Index.001
			sample_index_001 = sample_position.nodes.new("GeometryNodeSampleIndex")
			sample_index_001.name = "Sample Index.001"
			sample_index_001.clamp = False
			sample_index_001.data_type = 'FLOAT_VECTOR'
			sample_index_001.domain = 'POINT'

			#node Position
			position = sample_position.nodes.new("GeometryNodeInputPosition")
			position.name = "Position"




			#Set locations
			group_output_35.location = (270.0, 0.0)
			group_input_35.location = (-280.0, 0.0)
			sample_index_001.location = (80.0, 110.0)
			position.location = (-280.0, -100.0)

			#Set dimensions
			group_output_35.width, group_output_35.height = 140.0, 100.0
			group_input_35.width, group_input_35.height = 140.0, 100.0
			sample_index_001.width, sample_index_001.height = 140.0, 100.0
			position.width, position.height = 140.0, 100.0

			#initialize sample_position links
			#group_input_35.Geometry -> sample_index_001.Geometry
			sample_position.links.new(group_input_35.outputs[0], sample_index_001.inputs[0])
			#sample_index_001.Value -> group_output_35.Position
			sample_position.links.new(sample_index_001.outputs[0], group_output_35.inputs[0])
			#group_input_35.Index -> sample_index_001.Index
			sample_position.links.new(group_input_35.outputs[1], sample_index_001.inputs[2])
			#position.Position -> sample_index_001.Value
			sample_position.links.new(position.outputs[0], sample_index_001.inputs[1])
			return sample_position

		sample_position = sample_position_node_group()

		#initialize curve_rotation node group
		def curve_rotation_node_group():
			curve_rotation = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Curve Rotation")

			curve_rotation.color_tag = 'INPUT'
			curve_rotation.description = ""


			#curve_rotation interface
			#Socket Rotation
			rotation_socket_1 = curve_rotation.interface.new_socket(name = "Rotation", in_out='OUTPUT', socket_type = 'NodeSocketRotation')
			rotation_socket_1.attribute_domain = 'POINT'

			#Socket Normal
			normal_socket_1 = curve_rotation.interface.new_socket(name = "Normal", in_out='INPUT', socket_type = 'NodeSocketVector')
			normal_socket_1.subtype = 'NONE'
			normal_socket_1.default_value = (0.0, 0.0, 1.0)
			normal_socket_1.min_value = -3.4028234663852886e+38
			normal_socket_1.max_value = 3.4028234663852886e+38
			normal_socket_1.attribute_domain = 'POINT'


			#initialize curve_rotation nodes
			#node Group Output
			group_output_36 = curve_rotation.nodes.new("NodeGroupOutput")
			group_output_36.name = "Group Output"
			group_output_36.is_active_output = True

			#node Group Input
			group_input_36 = curve_rotation.nodes.new("NodeGroupInput")
			group_input_36.name = "Group Input"

			#node Axes to Rotation
			axes_to_rotation = curve_rotation.nodes.new("FunctionNodeAxesToRotation")
			axes_to_rotation.name = "Axes to Rotation"
			axes_to_rotation.primary_axis = 'Z'
			axes_to_rotation.secondary_axis = 'X'

			#node Curve Tangent.001
			curve_tangent_001 = curve_rotation.nodes.new("GeometryNodeInputTangent")
			curve_tangent_001.name = "Curve Tangent.001"




			#Set locations
			group_output_36.location = (60.0, 0.0)
			group_input_36.location = (-280.0, -60.0)
			axes_to_rotation.location = (-100.0, 0.0)
			curve_tangent_001.location = (-280.0, 0.0)

			#Set dimensions
			group_output_36.width, group_output_36.height = 140.0, 100.0
			group_input_36.width, group_input_36.height = 140.0, 100.0
			axes_to_rotation.width, axes_to_rotation.height = 140.0, 100.0
			curve_tangent_001.width, curve_tangent_001.height = 140.0, 100.0

			#initialize curve_rotation links
			#axes_to_rotation.Rotation -> group_output_36.Rotation
			curve_rotation.links.new(axes_to_rotation.outputs[0], group_output_36.inputs[0])
			#group_input_36.Normal -> axes_to_rotation.Secondary Axis
			curve_rotation.links.new(group_input_36.outputs[0], axes_to_rotation.inputs[1])
			#curve_tangent_001.Tangent -> axes_to_rotation.Primary Axis
			curve_rotation.links.new(curve_tangent_001.outputs[0], axes_to_rotation.inputs[0])
			return curve_rotation

		curve_rotation = curve_rotation_node_group()

		#initialize _profile_type_picker node group
		def _profile_type_picker_node_group():
			_profile_type_picker = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".Profile Type Picker")

			_profile_type_picker.color_tag = 'NONE'
			_profile_type_picker.description = ""


			#_profile_type_picker interface
			#Socket Output
			output_socket_2 = _profile_type_picker.interface.new_socket(name = "Output", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			output_socket_2.subtype = 'NONE'
			output_socket_2.default_value = 0
			output_socket_2.min_value = -2147483648
			output_socket_2.max_value = 2147483647
			output_socket_2.attribute_domain = 'POINT'

			#Socket Menu
			menu_socket_1 = _profile_type_picker.interface.new_socket(name = "Menu", in_out='INPUT', socket_type = 'NodeSocketMenu')
			menu_socket_1.attribute_domain = 'POINT'


			#initialize _profile_type_picker nodes
			#node Group Output
			group_output_37 = _profile_type_picker.nodes.new("NodeGroupOutput")
			group_output_37.name = "Group Output"
			group_output_37.is_active_output = True

			#node Group Input
			group_input_37 = _profile_type_picker.nodes.new("NodeGroupInput")
			group_input_37.name = "Group Input"

			#node Menu Switch.002
			menu_switch_002 = _profile_type_picker.nodes.new("GeometryNodeMenuSwitch")
			menu_switch_002.name = "Menu Switch.002"
			menu_switch_002.active_index = 0
			menu_switch_002.data_type = 'INT'
			menu_switch_002.enum_items.clear()
			menu_switch_002.enum_items.new("Default Profile")
			menu_switch_002.enum_items[0].description = ""
			menu_switch_002.enum_items.new("Custom Profile")
			menu_switch_002.enum_items[1].description = ""
			#Item_1
			menu_switch_002.inputs[1].default_value = 0
			#Item_0
			menu_switch_002.inputs[2].default_value = 1




			#Set locations
			group_output_37.location = (190.0, 0.0)
			group_input_37.location = (-200.0, 0.0)
			menu_switch_002.location = (0.0, 0.0)

			#Set dimensions
			group_output_37.width, group_output_37.height = 140.0, 100.0
			group_input_37.width, group_input_37.height = 140.0, 100.0
			menu_switch_002.width, menu_switch_002.height = 140.0, 100.0

			#initialize _profile_type_picker links
			#group_input_37.Menu -> menu_switch_002.Menu
			_profile_type_picker.links.new(group_input_37.outputs[0], menu_switch_002.inputs[0])
			#menu_switch_002.Output -> group_output_37.Output
			_profile_type_picker.links.new(menu_switch_002.outputs[0], group_output_37.inputs[0])
			return _profile_type_picker

		_profile_type_picker = _profile_type_picker_node_group()

		#initialize curve_custom_profile node group
		def curve_custom_profile_node_group():
			curve_custom_profile = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Curve Custom Profile")

			curve_custom_profile.color_tag = 'GEOMETRY'
			curve_custom_profile.description = ""

			curve_custom_profile.is_modifier = True

			#curve_custom_profile interface
			#Socket Geometry
			geometry_socket_5 = curve_custom_profile.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			geometry_socket_5.attribute_domain = 'POINT'

			#Socket Curve
			curve_socket = curve_custom_profile.interface.new_socket(name = "Curve", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			curve_socket.attribute_domain = 'POINT'

			#Socket Subdivisions
			subdivisions_socket = curve_custom_profile.interface.new_socket(name = "Subdivisions", in_out='INPUT', socket_type = 'NodeSocketInt')
			subdivisions_socket.subtype = 'NONE'
			subdivisions_socket.default_value = 6
			subdivisions_socket.min_value = 1
			subdivisions_socket.max_value = 2147483647
			subdivisions_socket.attribute_domain = 'POINT'

			#Socket Profile Type
			profile_type_socket = curve_custom_profile.interface.new_socket(name = "Profile Type", in_out='INPUT', socket_type = 'NodeSocketMenu')
			profile_type_socket.attribute_domain = 'POINT'

			#Panel Profile
			profile_panel = curve_custom_profile.interface.new_panel("Profile", default_closed=True)
			#Socket Profile Rotation
			profile_rotation_socket = curve_custom_profile.interface.new_socket(name = "Profile Rotation", in_out='INPUT', socket_type = 'NodeSocketRotation', parent = profile_panel)
			profile_rotation_socket.attribute_domain = 'POINT'

			#Socket Profile Scale
			profile_scale_socket = curve_custom_profile.interface.new_socket(name = "Profile Scale", in_out='INPUT', socket_type = 'NodeSocketVector', parent = profile_panel)
			profile_scale_socket.subtype = 'XYZ'
			profile_scale_socket.default_value = (1.0, 1.0, 1.0)
			profile_scale_socket.min_value = -3.4028234663852886e+38
			profile_scale_socket.max_value = 3.4028234663852886e+38
			profile_scale_socket.attribute_domain = 'POINT'

			#Socket Profile Curve
			profile_curve_socket = curve_custom_profile.interface.new_socket(name = "Profile Curve", in_out='INPUT', socket_type = 'NodeSocketGeometry', parent = profile_panel)
			profile_curve_socket.attribute_domain = 'POINT'

			#Socket Profile Resolution
			profile_resolution_socket = curve_custom_profile.interface.new_socket(name = "Profile Resolution", in_out='INPUT', socket_type = 'NodeSocketInt', parent = profile_panel)
			profile_resolution_socket.subtype = 'NONE'
			profile_resolution_socket.default_value = 4
			profile_resolution_socket.min_value = 3
			profile_resolution_socket.max_value = 512
			profile_resolution_socket.attribute_domain = 'POINT'

			#Socket Profile Radius
			profile_radius_socket = curve_custom_profile.interface.new_socket(name = "Profile Radius", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = profile_panel)
			profile_radius_socket.subtype = 'DISTANCE'
			profile_radius_socket.default_value = 1.0
			profile_radius_socket.min_value = 0.0
			profile_radius_socket.max_value = 3.4028234663852886e+38
			profile_radius_socket.attribute_domain = 'POINT'

			#Socket Profile Rotation
			profile_rotation_socket_1 = curve_custom_profile.interface.new_socket(name = "Profile Rotation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = profile_panel)
			profile_rotation_socket_1.subtype = 'NONE'
			profile_rotation_socket_1.default_value = 0.7853981852531433
			profile_rotation_socket_1.min_value = -10000.0
			profile_rotation_socket_1.max_value = 10000.0
			profile_rotation_socket_1.attribute_domain = 'POINT'



			#initialize curve_custom_profile nodes
			#node Instance on Points.001
			instance_on_points_001 = curve_custom_profile.nodes.new("GeometryNodeInstanceOnPoints")
			instance_on_points_001.name = "Instance on Points.001"
			#Selection
			instance_on_points_001.inputs[1].default_value = True
			#Pick Instance
			instance_on_points_001.inputs[3].default_value = False
			#Instance Index
			instance_on_points_001.inputs[4].default_value = 0

			#node Realize Instances
			realize_instances = curve_custom_profile.nodes.new("GeometryNodeRealizeInstances")
			realize_instances.name = "Realize Instances"
			#Selection
			realize_instances.inputs[1].default_value = True
			#Realize All
			realize_instances.inputs[2].default_value = True
			#Depth
			realize_instances.inputs[3].default_value = 0

			#node Curve to Mesh
			curve_to_mesh = curve_custom_profile.nodes.new("GeometryNodeCurveToMesh")
			curve_to_mesh.name = "Curve to Mesh"
			#Fill Caps
			curve_to_mesh.inputs[2].default_value = True

			#node Set Position.002
			set_position_002 = curve_custom_profile.nodes.new("GeometryNodeSetPosition")
			set_position_002.name = "Set Position.002"
			#Selection
			set_position_002.inputs[1].default_value = True
			#Offset
			set_position_002.inputs[3].default_value = (0.0, 0.0, 0.0)

			#node Group Output
			group_output_38 = curve_custom_profile.nodes.new("NodeGroupOutput")
			group_output_38.name = "Group Output"
			group_output_38.is_active_output = True

			#node Group.001
			group_001_8 = curve_custom_profile.nodes.new("GeometryNodeGroup")
			group_001_8.name = "Group.001"
			group_001_8.node_tree = _curve_profile_backup

			#node Set Spline Resolution
			set_spline_resolution = curve_custom_profile.nodes.new("GeometryNodeSetSplineResolution")
			set_spline_resolution.name = "Set Spline Resolution"
			#Selection
			set_spline_resolution.inputs[1].default_value = True

			#node Resample Curve
			resample_curve = curve_custom_profile.nodes.new("GeometryNodeResampleCurve")
			resample_curve.name = "Resample Curve"
			resample_curve.mode = 'EVALUATED'
			#Selection
			resample_curve.inputs[1].default_value = True

			#node Group Input
			group_input_38 = curve_custom_profile.nodes.new("NodeGroupInput")
			group_input_38.name = "Group Input"

			#node Capture Attribute
			capture_attribute_2 = curve_custom_profile.nodes.new("GeometryNodeCaptureAttribute")
			capture_attribute_2.name = "Capture Attribute"
			capture_attribute_2.active_index = 3
			capture_attribute_2.capture_items.clear()
			capture_attribute_2.capture_items.new('FLOAT', "Resolution")
			capture_attribute_2.capture_items["Resolution"].data_type = 'INT'
			capture_attribute_2.capture_items.new('FLOAT', "Rotation")
			capture_attribute_2.capture_items["Rotation"].data_type = 'QUATERNION'
			capture_attribute_2.capture_items.new('FLOAT', "Scale")
			capture_attribute_2.capture_items["Scale"].data_type = 'FLOAT_VECTOR'
			capture_attribute_2.capture_items.new('FLOAT', "Index")
			capture_attribute_2.capture_items["Index"].data_type = 'INT'
			capture_attribute_2.domain = 'POINT'

			#node Group
			group_13 = curve_custom_profile.nodes.new("GeometryNodeGroup")
			group_13.name = "Group"
			group_13.node_tree = sample_position
			#Socket_3
			group_13.inputs[1].default_value = 0

			#node Reroute
			reroute_5 = curve_custom_profile.nodes.new("NodeReroute")
			reroute_5.name = "Reroute"
			#node Capture Attribute.001
			capture_attribute_001 = curve_custom_profile.nodes.new("GeometryNodeCaptureAttribute")
			capture_attribute_001.name = "Capture Attribute.001"
			capture_attribute_001.active_index = 0
			capture_attribute_001.capture_items.clear()
			capture_attribute_001.capture_items.new('FLOAT', "Index")
			capture_attribute_001.capture_items["Index"].data_type = 'INT'
			capture_attribute_001.domain = 'POINT'

			#node Index
			index_2 = curve_custom_profile.nodes.new("GeometryNodeInputIndex")
			index_2.name = "Index"

			#node Group Input.001
			group_input_001_3 = curve_custom_profile.nodes.new("NodeGroupInput")
			group_input_001_3.name = "Group Input.001"
			group_input_001_3.outputs[0].hide = True
			group_input_001_3.outputs[1].hide = True
			group_input_001_3.outputs[3].hide = True
			group_input_001_3.outputs[4].hide = True
			group_input_001_3.outputs[5].hide = True
			group_input_001_3.outputs[6].hide = True
			group_input_001_3.outputs[7].hide = True
			group_input_001_3.outputs[8].hide = True
			group_input_001_3.outputs[9].hide = True

			#node Index Switch
			index_switch_1 = curve_custom_profile.nodes.new("GeometryNodeIndexSwitch")
			index_switch_1.name = "Index Switch"
			index_switch_1.data_type = 'GEOMETRY'
			index_switch_1.index_switch_items.clear()
			index_switch_1.index_switch_items.new()
			index_switch_1.index_switch_items.new()

			#node Index Switch.001
			index_switch_001 = curve_custom_profile.nodes.new("GeometryNodeIndexSwitch")
			index_switch_001.name = "Index Switch.001"
			index_switch_001.data_type = 'ROTATION'
			index_switch_001.index_switch_items.clear()
			index_switch_001.index_switch_items.new()
			index_switch_001.index_switch_items.new()

			#node Group.002
			group_002_5 = curve_custom_profile.nodes.new("GeometryNodeGroup")
			group_002_5.name = "Group.002"
			group_002_5.node_tree = curve_rotation
			#Socket_1
			group_002_5.inputs[0].default_value = (0.0, 0.0, 1.0)

			#node Group.003
			group_003_2 = curve_custom_profile.nodes.new("GeometryNodeGroup")
			group_003_2.name = "Group.003"
			group_003_2.node_tree = _profile_type_picker

			#node Group.004
			group_004_2 = curve_custom_profile.nodes.new("GeometryNodeGroup")
			group_004_2.name = "Group.004"
			group_004_2.node_tree = _profile_type_picker




			#Set locations
			instance_on_points_001.location = (-1420.0, 20.0)
			realize_instances.location = (-1260.0, 20.0)
			curve_to_mesh.location = (-1420.0, -340.0)
			set_position_002.location = (-1100.0, -140.0)
			group_output_38.location = (-820.0, -260.0)
			group_001_8.location = (-2200.0, -320.0)
			set_spline_resolution.location = (-1800.0, 20.0)
			resample_curve.location = (-1640.0, 20.0)
			group_input_38.location = (-2580.0, -120.0)
			capture_attribute_2.location = (-1980.0, -20.0)
			group_13.location = (-1260.0, -140.0)
			reroute_5.location = (-1677.626220703125, -261.3639831542969)
			capture_attribute_001.location = (-1980.0, -320.0)
			index_2.location = (-2180.0, -240.0)
			group_input_001_3.location = (-1420.0, -480.0)
			index_switch_1.location = (-1100.0, -360.0)
			index_switch_001.location = (-2180.0, -20.0)
			group_002_5.location = (-2580.0, 120.0)
			group_003_2.location = (-2580.0, 0.0)
			group_004_2.location = (-1261.976318359375, -448.526123046875)

			#Set dimensions
			instance_on_points_001.width, instance_on_points_001.height = 140.0, 100.0
			realize_instances.width, realize_instances.height = 140.0, 100.0
			curve_to_mesh.width, curve_to_mesh.height = 140.0, 100.0
			set_position_002.width, set_position_002.height = 140.0, 100.0
			group_output_38.width, group_output_38.height = 140.0, 100.0
			group_001_8.width, group_001_8.height = 176.47764587402344, 100.0
			set_spline_resolution.width, set_spline_resolution.height = 140.0, 100.0
			resample_curve.width, resample_curve.height = 140.0, 100.0
			group_input_38.width, group_input_38.height = 140.0, 100.0
			capture_attribute_2.width, capture_attribute_2.height = 140.0, 100.0
			group_13.width, group_13.height = 140.0, 100.0
			reroute_5.width, reroute_5.height = 16.0, 100.0
			capture_attribute_001.width, capture_attribute_001.height = 149.49960327148438, 100.0
			index_2.width, index_2.height = 140.0, 100.0
			group_input_001_3.width, group_input_001_3.height = 140.0, 100.0
			index_switch_1.width, index_switch_1.height = 140.0, 100.0
			index_switch_001.width, index_switch_001.height = 140.0, 100.0
			group_002_5.width, group_002_5.height = 140.0, 100.0
			group_003_2.width, group_003_2.height = 140.0, 100.0
			group_004_2.width, group_004_2.height = 140.0, 100.0

			#initialize curve_custom_profile links
			#group_13.Position -> set_position_002.Position
			curve_custom_profile.links.new(group_13.outputs[0], set_position_002.inputs[2])
			#resample_curve.Curve -> curve_to_mesh.Curve
			curve_custom_profile.links.new(resample_curve.outputs[0], curve_to_mesh.inputs[0])
			#curve_to_mesh.Mesh -> set_position_002.Geometry
			curve_custom_profile.links.new(curve_to_mesh.outputs[0], set_position_002.inputs[0])
			#instance_on_points_001.Instances -> realize_instances.Geometry
			curve_custom_profile.links.new(instance_on_points_001.outputs[0], realize_instances.inputs[0])
			#reroute_5.Output -> instance_on_points_001.Instance
			curve_custom_profile.links.new(reroute_5.outputs[0], instance_on_points_001.inputs[2])
			#reroute_5.Output -> curve_to_mesh.Profile Curve
			curve_custom_profile.links.new(reroute_5.outputs[0], curve_to_mesh.inputs[1])
			#capture_attribute_2.Scale -> instance_on_points_001.Scale
			curve_custom_profile.links.new(capture_attribute_2.outputs[3], instance_on_points_001.inputs[6])
			#capture_attribute_2.Geometry -> set_spline_resolution.Geometry
			curve_custom_profile.links.new(capture_attribute_2.outputs[0], set_spline_resolution.inputs[0])
			#resample_curve.Curve -> instance_on_points_001.Points
			curve_custom_profile.links.new(resample_curve.outputs[0], instance_on_points_001.inputs[0])
			#set_spline_resolution.Geometry -> resample_curve.Curve
			curve_custom_profile.links.new(set_spline_resolution.outputs[0], resample_curve.inputs[0])
			#group_input_38.Curve -> capture_attribute_2.Geometry
			curve_custom_profile.links.new(group_input_38.outputs[0], capture_attribute_2.inputs[0])
			#capture_attribute_2.Rotation -> instance_on_points_001.Rotation
			curve_custom_profile.links.new(capture_attribute_2.outputs[2], instance_on_points_001.inputs[5])
			#realize_instances.Geometry -> group_13.Geometry
			curve_custom_profile.links.new(realize_instances.outputs[0], group_13.inputs[0])
			#group_input_38.Profile Scale -> capture_attribute_2.Scale
			curve_custom_profile.links.new(group_input_38.outputs[4], capture_attribute_2.inputs[3])
			#group_input_38.Subdivisions -> capture_attribute_2.Resolution
			curve_custom_profile.links.new(group_input_38.outputs[1], capture_attribute_2.inputs[1])
			#capture_attribute_2.Resolution -> set_spline_resolution.Resolution
			curve_custom_profile.links.new(capture_attribute_2.outputs[1], set_spline_resolution.inputs[2])
			#group_input_38.Profile Curve -> group_001_8.Input
			curve_custom_profile.links.new(group_input_38.outputs[5], group_001_8.inputs[0])
			#group_input_38.Profile Resolution -> group_001_8.Resolution
			curve_custom_profile.links.new(group_input_38.outputs[6], group_001_8.inputs[1])
			#group_input_38.Profile Radius -> group_001_8.Radius (A)
			curve_custom_profile.links.new(group_input_38.outputs[7], group_001_8.inputs[2])
			#group_input_38.Profile Rotation -> group_001_8.Rotation
			curve_custom_profile.links.new(group_input_38.outputs[8], group_001_8.inputs[3])
			#capture_attribute_001.Geometry -> reroute_5.Input
			curve_custom_profile.links.new(capture_attribute_001.outputs[0], reroute_5.inputs[0])
			#group_001_8.Output -> capture_attribute_001.Geometry
			curve_custom_profile.links.new(group_001_8.outputs[0], capture_attribute_001.inputs[0])
			#index_2.Index -> capture_attribute_001.Index
			curve_custom_profile.links.new(index_2.outputs[0], capture_attribute_001.inputs[1])
			#index_2.Index -> capture_attribute_2.Index
			curve_custom_profile.links.new(index_2.outputs[0], capture_attribute_2.inputs[4])
			#set_position_002.Geometry -> index_switch_1.1
			curve_custom_profile.links.new(set_position_002.outputs[0], index_switch_1.inputs[2])
			#index_switch_1.Output -> group_output_38.Geometry
			curve_custom_profile.links.new(index_switch_1.outputs[0], group_output_38.inputs[0])
			#group_input_38.Profile Rotation -> index_switch_001.1
			curve_custom_profile.links.new(group_input_38.outputs[3], index_switch_001.inputs[2])
			#group_002_5.Rotation -> index_switch_001.0
			curve_custom_profile.links.new(group_002_5.outputs[0], index_switch_001.inputs[1])
			#group_input_38.Profile Type -> group_003_2.Menu
			curve_custom_profile.links.new(group_input_38.outputs[2], group_003_2.inputs[0])
			#group_004_2.Output -> index_switch_1.Index
			curve_custom_profile.links.new(group_004_2.outputs[0], index_switch_1.inputs[0])
			#group_input_001_3.Profile Type -> group_004_2.Menu
			curve_custom_profile.links.new(group_input_001_3.outputs[2], group_004_2.inputs[0])
			#group_003_2.Output -> index_switch_001.Index
			curve_custom_profile.links.new(group_003_2.outputs[0], index_switch_001.inputs[0])
			#index_switch_001.Output -> capture_attribute_2.Rotation
			curve_custom_profile.links.new(index_switch_001.outputs[0], capture_attribute_2.inputs[2])
			#curve_to_mesh.Mesh -> index_switch_1.0
			curve_custom_profile.links.new(curve_to_mesh.outputs[0], index_switch_1.inputs[1])
			return curve_custom_profile

		curve_custom_profile = curve_custom_profile_node_group()

		#initialize offset_point_along_curve node group
		def offset_point_along_curve_node_group():
			offset_point_along_curve = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Offset Point Along Curve")

			offset_point_along_curve.color_tag = 'INPUT'
			offset_point_along_curve.description = ""


			#offset_point_along_curve interface
			#Socket Factor
			factor_socket_1 = offset_point_along_curve.interface.new_socket(name = "Factor", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
			factor_socket_1.subtype = 'NONE'
			factor_socket_1.default_value = 0.0
			factor_socket_1.min_value = -3.4028234663852886e+38
			factor_socket_1.max_value = 3.4028234663852886e+38
			factor_socket_1.attribute_domain = 'POINT'

			#Socket Length
			length_socket = offset_point_along_curve.interface.new_socket(name = "Length", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
			length_socket.subtype = 'NONE'
			length_socket.default_value = 0.0
			length_socket.min_value = -3.4028234663852886e+38
			length_socket.max_value = 3.4028234663852886e+38
			length_socket.attribute_domain = 'POINT'

			#Socket Index A
			index_a_socket = offset_point_along_curve.interface.new_socket(name = "Index A", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			index_a_socket.subtype = 'NONE'
			index_a_socket.default_value = 0
			index_a_socket.min_value = -2147483648
			index_a_socket.max_value = 2147483647
			index_a_socket.attribute_domain = 'POINT'

			#Socket Index B
			index_b_socket = offset_point_along_curve.interface.new_socket(name = "Index B", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			index_b_socket.subtype = 'NONE'
			index_b_socket.default_value = 0
			index_b_socket.min_value = -2147483648
			index_b_socket.max_value = 2147483647
			index_b_socket.attribute_domain = 'POINT'

			#Socket Point Index
			point_index_socket = offset_point_along_curve.interface.new_socket(name = "Point Index", in_out='INPUT', socket_type = 'NodeSocketInt')
			point_index_socket.subtype = 'NONE'
			point_index_socket.default_value = 0
			point_index_socket.min_value = -2147483648
			point_index_socket.max_value = 2147483647
			point_index_socket.attribute_domain = 'POINT'
			point_index_socket.hide_value = True

			#Socket Value
			value_socket_5 = offset_point_along_curve.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat')
			value_socket_5.subtype = 'NONE'
			value_socket_5.default_value = 0.5
			value_socket_5.min_value = -10000.0
			value_socket_5.max_value = 10000.0
			value_socket_5.attribute_domain = 'POINT'


			#initialize offset_point_along_curve nodes
			#node Group Output
			group_output_39 = offset_point_along_curve.nodes.new("NodeGroupOutput")
			group_output_39.name = "Group Output"
			group_output_39.is_active_output = True

			#node Group Input
			group_input_39 = offset_point_along_curve.nodes.new("NodeGroupInput")
			group_input_39.name = "Group Input"

			#node Offset Point in Curve
			offset_point_in_curve = offset_point_along_curve.nodes.new("GeometryNodeOffsetPointInCurve")
			offset_point_in_curve.name = "Offset Point in Curve"

			#node Offset Point in Curve.001
			offset_point_in_curve_001 = offset_point_along_curve.nodes.new("GeometryNodeOffsetPointInCurve")
			offset_point_in_curve_001.name = "Offset Point in Curve.001"

			#node Math
			math_9 = offset_point_along_curve.nodes.new("ShaderNodeMath")
			math_9.name = "Math"
			math_9.operation = 'ADD'
			math_9.use_clamp = False
			#Value_001
			math_9.inputs[1].default_value = 1.0

			#node Evaluate at Index
			evaluate_at_index_3 = offset_point_along_curve.nodes.new("GeometryNodeFieldAtIndex")
			evaluate_at_index_3.name = "Evaluate at Index"
			evaluate_at_index_3.data_type = 'FLOAT'
			evaluate_at_index_3.domain = 'POINT'

			#node Spline Parameter
			spline_parameter = offset_point_along_curve.nodes.new("GeometryNodeSplineParameter")
			spline_parameter.name = "Spline Parameter"

			#node Evaluate at Index.001
			evaluate_at_index_001_1 = offset_point_along_curve.nodes.new("GeometryNodeFieldAtIndex")
			evaluate_at_index_001_1.name = "Evaluate at Index.001"
			evaluate_at_index_001_1.data_type = 'FLOAT'
			evaluate_at_index_001_1.domain = 'POINT'

			#node Math.001
			math_001_2 = offset_point_along_curve.nodes.new("ShaderNodeMath")
			math_001_2.name = "Math.001"
			math_001_2.operation = 'FRACT'
			math_001_2.use_clamp = False

			#node Mix
			mix_1 = offset_point_along_curve.nodes.new("ShaderNodeMix")
			mix_1.name = "Mix"
			mix_1.blend_type = 'MIX'
			mix_1.clamp_factor = True
			mix_1.clamp_result = False
			mix_1.data_type = 'FLOAT'
			mix_1.factor_mode = 'UNIFORM'

			#node Math.002
			math_002 = offset_point_along_curve.nodes.new("ShaderNodeMath")
			math_002.name = "Math.002"
			math_002.operation = 'FLOOR'
			math_002.use_clamp = False

			#node Reroute
			reroute_6 = offset_point_along_curve.nodes.new("NodeReroute")
			reroute_6.name = "Reroute"
			#node Evaluate at Index.002
			evaluate_at_index_002 = offset_point_along_curve.nodes.new("GeometryNodeFieldAtIndex")
			evaluate_at_index_002.name = "Evaluate at Index.002"
			evaluate_at_index_002.data_type = 'FLOAT'
			evaluate_at_index_002.domain = 'POINT'

			#node Evaluate at Index.003
			evaluate_at_index_003 = offset_point_along_curve.nodes.new("GeometryNodeFieldAtIndex")
			evaluate_at_index_003.name = "Evaluate at Index.003"
			evaluate_at_index_003.data_type = 'FLOAT'
			evaluate_at_index_003.domain = 'POINT'

			#node Math.003
			math_003 = offset_point_along_curve.nodes.new("ShaderNodeMath")
			math_003.name = "Math.003"
			math_003.operation = 'FRACT'
			math_003.use_clamp = False

			#node Mix.001
			mix_001 = offset_point_along_curve.nodes.new("ShaderNodeMix")
			mix_001.name = "Mix.001"
			mix_001.blend_type = 'MIX'
			mix_001.clamp_factor = True
			mix_001.clamp_result = False
			mix_001.data_type = 'FLOAT'
			mix_001.factor_mode = 'UNIFORM'

			#node Compare
			compare_4 = offset_point_along_curve.nodes.new("FunctionNodeCompare")
			compare_4.name = "Compare"
			compare_4.data_type = 'FLOAT'
			compare_4.mode = 'ELEMENT'
			compare_4.operation = 'EQUAL'
			#B
			compare_4.inputs[1].default_value = 0.0
			#Epsilon
			compare_4.inputs[12].default_value = 0.0010000000474974513

			#node Switch
			switch_6 = offset_point_along_curve.nodes.new("GeometryNodeSwitch")
			switch_6.name = "Switch"
			switch_6.input_type = 'FLOAT'

			#node Switch.001
			switch_001_2 = offset_point_along_curve.nodes.new("GeometryNodeSwitch")
			switch_001_2.name = "Switch.001"
			switch_001_2.input_type = 'FLOAT'

			#node Reroute.002
			reroute_002_3 = offset_point_along_curve.nodes.new("NodeReroute")
			reroute_002_3.name = "Reroute.002"
			#node Reroute.001
			reroute_001_5 = offset_point_along_curve.nodes.new("NodeReroute")
			reroute_001_5.name = "Reroute.001"
			#node Reroute.003
			reroute_003_2 = offset_point_along_curve.nodes.new("NodeReroute")
			reroute_003_2.name = "Reroute.003"
			#node Reroute.004
			reroute_004 = offset_point_along_curve.nodes.new("NodeReroute")
			reroute_004.name = "Reroute.004"



			#Set locations
			group_output_39.location = (583.2135620117188, 167.43295288085938)
			group_input_39.location = (-700.0, 260.0)
			offset_point_in_curve.location = (-300.0, 60.0)
			offset_point_in_curve_001.location = (-300.0, -80.0)
			math_9.location = (-480.0, -80.0)
			evaluate_at_index_3.location = (40.0, 180.0)
			spline_parameter.location = (-300.0, 180.0)
			evaluate_at_index_001_1.location = (40.0, 0.0)
			math_001_2.location = (40.0, 320.0)
			mix_1.location = (220.0, 200.0)
			math_002.location = (-480.0, 60.0)
			reroute_6.location = (-20.0, 80.0)
			evaluate_at_index_002.location = (40.0, -300.0)
			evaluate_at_index_003.location = (40.0, -480.0)
			math_003.location = (40.0, -160.0)
			mix_001.location = (220.0, -280.0)
			compare_4.location = (-300.0, 400.0)
			switch_6.location = (408.91497802734375, 315.45098876953125)
			switch_001_2.location = (403.20001220703125, 149.92684936523438)
			reroute_002_3.location = (340.0, 360.0)
			reroute_001_5.location = (-60.0, 0.0)
			reroute_003_2.location = (-40.0, 20.0)
			reroute_004.location = (-80.0, -160.0)

			#Set dimensions
			group_output_39.width, group_output_39.height = 140.0, 100.0
			group_input_39.width, group_input_39.height = 140.0, 100.0
			offset_point_in_curve.width, offset_point_in_curve.height = 140.0, 100.0
			offset_point_in_curve_001.width, offset_point_in_curve_001.height = 140.0, 100.0
			math_9.width, math_9.height = 140.0, 100.0
			evaluate_at_index_3.width, evaluate_at_index_3.height = 140.0, 100.0
			spline_parameter.width, spline_parameter.height = 140.0, 100.0
			evaluate_at_index_001_1.width, evaluate_at_index_001_1.height = 140.0, 100.0
			math_001_2.width, math_001_2.height = 140.0, 100.0
			mix_1.width, mix_1.height = 140.0, 100.0
			math_002.width, math_002.height = 140.0, 100.0
			reroute_6.width, reroute_6.height = 16.0, 100.0
			evaluate_at_index_002.width, evaluate_at_index_002.height = 140.0, 100.0
			evaluate_at_index_003.width, evaluate_at_index_003.height = 140.0, 100.0
			math_003.width, math_003.height = 140.0, 100.0
			mix_001.width, mix_001.height = 140.0, 100.0
			compare_4.width, compare_4.height = 140.0, 100.0
			switch_6.width, switch_6.height = 140.0, 100.0
			switch_001_2.width, switch_001_2.height = 140.0, 100.0
			reroute_002_3.width, reroute_002_3.height = 16.0, 100.0
			reroute_001_5.width, reroute_001_5.height = 16.0, 100.0
			reroute_003_2.width, reroute_003_2.height = 16.0, 100.0
			reroute_004.width, reroute_004.height = 16.0, 100.0

			#initialize offset_point_along_curve links
			#math_9.Value -> offset_point_in_curve_001.Offset
			offset_point_along_curve.links.new(math_9.outputs[0], offset_point_in_curve_001.inputs[1])
			#reroute_6.Output -> evaluate_at_index_3.Value
			offset_point_along_curve.links.new(reroute_6.outputs[0], evaluate_at_index_3.inputs[1])
			#reroute_003_2.Output -> evaluate_at_index_3.Index
			offset_point_along_curve.links.new(reroute_003_2.outputs[0], evaluate_at_index_3.inputs[0])
			#reroute_6.Output -> evaluate_at_index_001_1.Value
			offset_point_along_curve.links.new(reroute_6.outputs[0], evaluate_at_index_001_1.inputs[1])
			#reroute_004.Output -> evaluate_at_index_001_1.Index
			offset_point_along_curve.links.new(reroute_004.outputs[0], evaluate_at_index_001_1.inputs[0])
			#group_input_39.Value -> math_001_2.Value
			offset_point_along_curve.links.new(group_input_39.outputs[1], math_001_2.inputs[0])
			#evaluate_at_index_3.Value -> mix_1.A
			offset_point_along_curve.links.new(evaluate_at_index_3.outputs[0], mix_1.inputs[2])
			#math_001_2.Value -> mix_1.Factor
			offset_point_along_curve.links.new(math_001_2.outputs[0], mix_1.inputs[0])
			#evaluate_at_index_001_1.Value -> mix_1.B
			offset_point_along_curve.links.new(evaluate_at_index_001_1.outputs[0], mix_1.inputs[3])
			#group_input_39.Value -> math_002.Value
			offset_point_along_curve.links.new(group_input_39.outputs[1], math_002.inputs[0])
			#math_002.Value -> offset_point_in_curve.Offset
			offset_point_along_curve.links.new(math_002.outputs[0], offset_point_in_curve.inputs[1])
			#math_002.Value -> math_9.Value
			offset_point_along_curve.links.new(math_002.outputs[0], math_9.inputs[0])
			#spline_parameter.Factor -> reroute_6.Input
			offset_point_along_curve.links.new(spline_parameter.outputs[0], reroute_6.inputs[0])
			#reroute_001_5.Output -> evaluate_at_index_002.Value
			offset_point_along_curve.links.new(reroute_001_5.outputs[0], evaluate_at_index_002.inputs[1])
			#reroute_003_2.Output -> evaluate_at_index_002.Index
			offset_point_along_curve.links.new(reroute_003_2.outputs[0], evaluate_at_index_002.inputs[0])
			#reroute_001_5.Output -> evaluate_at_index_003.Value
			offset_point_along_curve.links.new(reroute_001_5.outputs[0], evaluate_at_index_003.inputs[1])
			#reroute_004.Output -> evaluate_at_index_003.Index
			offset_point_along_curve.links.new(reroute_004.outputs[0], evaluate_at_index_003.inputs[0])
			#group_input_39.Value -> math_003.Value
			offset_point_along_curve.links.new(group_input_39.outputs[1], math_003.inputs[0])
			#evaluate_at_index_002.Value -> mix_001.A
			offset_point_along_curve.links.new(evaluate_at_index_002.outputs[0], mix_001.inputs[2])
			#math_003.Value -> mix_001.Factor
			offset_point_along_curve.links.new(math_003.outputs[0], mix_001.inputs[0])
			#evaluate_at_index_003.Value -> mix_001.B
			offset_point_along_curve.links.new(evaluate_at_index_003.outputs[0], mix_001.inputs[3])
			#switch_001_2.Output -> group_output_39.Length
			offset_point_along_curve.links.new(switch_001_2.outputs[0], group_output_39.inputs[1])
			#group_input_39.Value -> compare_4.A
			offset_point_along_curve.links.new(group_input_39.outputs[1], compare_4.inputs[0])
			#reroute_002_3.Output -> switch_6.Switch
			offset_point_along_curve.links.new(reroute_002_3.outputs[0], switch_6.inputs[0])
			#mix_1.Result -> switch_6.False
			offset_point_along_curve.links.new(mix_1.outputs[0], switch_6.inputs[1])
			#spline_parameter.Factor -> switch_6.True
			offset_point_along_curve.links.new(spline_parameter.outputs[0], switch_6.inputs[2])
			#switch_6.Output -> group_output_39.Factor
			offset_point_along_curve.links.new(switch_6.outputs[0], group_output_39.inputs[0])
			#mix_001.Result -> switch_001_2.False
			offset_point_along_curve.links.new(mix_001.outputs[0], switch_001_2.inputs[1])
			#reroute_002_3.Output -> switch_001_2.Switch
			offset_point_along_curve.links.new(reroute_002_3.outputs[0], switch_001_2.inputs[0])
			#compare_4.Result -> reroute_002_3.Input
			offset_point_along_curve.links.new(compare_4.outputs[0], reroute_002_3.inputs[0])
			#reroute_001_5.Output -> switch_001_2.True
			offset_point_along_curve.links.new(reroute_001_5.outputs[0], switch_001_2.inputs[2])
			#reroute_003_2.Output -> group_output_39.Index A
			offset_point_along_curve.links.new(reroute_003_2.outputs[0], group_output_39.inputs[2])
			#reroute_004.Output -> group_output_39.Index B
			offset_point_along_curve.links.new(reroute_004.outputs[0], group_output_39.inputs[3])
			#spline_parameter.Length -> reroute_001_5.Input
			offset_point_along_curve.links.new(spline_parameter.outputs[1], reroute_001_5.inputs[0])
			#offset_point_in_curve.Point Index -> reroute_003_2.Input
			offset_point_along_curve.links.new(offset_point_in_curve.outputs[1], reroute_003_2.inputs[0])
			#offset_point_in_curve_001.Point Index -> reroute_004.Input
			offset_point_along_curve.links.new(offset_point_in_curve_001.outputs[1], reroute_004.inputs[0])
			#group_input_39.Point Index -> offset_point_in_curve.Point Index
			offset_point_along_curve.links.new(group_input_39.outputs[0], offset_point_in_curve.inputs[0])
			#group_input_39.Point Index -> offset_point_in_curve_001.Point Index
			offset_point_along_curve.links.new(group_input_39.outputs[0], offset_point_in_curve_001.inputs[0])
			return offset_point_along_curve

		offset_point_along_curve = offset_point_along_curve_node_group()

		#initialize curve_split_splines node group
		def curve_split_splines_node_group():
			curve_split_splines = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Curve Split Splines")

			curve_split_splines.color_tag = 'GEOMETRY'
			curve_split_splines.description = "Spline the given curves into new separate splines based on their Curve Group ID, additionally dropping any non-selected points"


			#curve_split_splines interface
			#Socket Curve
			curve_socket_1 = curve_split_splines.interface.new_socket(name = "Curve", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			curve_socket_1.attribute_domain = 'POINT'

			#Socket Index
			index_socket_8 = curve_split_splines.interface.new_socket(name = "Index", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			index_socket_8.subtype = 'NONE'
			index_socket_8.default_value = 0
			index_socket_8.min_value = -2147483648
			index_socket_8.max_value = 2147483647
			index_socket_8.attribute_domain = 'POINT'

			#Socket Rotation
			rotation_socket_2 = curve_split_splines.interface.new_socket(name = "Rotation", in_out='OUTPUT', socket_type = 'NodeSocketRotation')
			rotation_socket_2.attribute_domain = 'POINT'

			#Socket Curve
			curve_socket_2 = curve_split_splines.interface.new_socket(name = "Curve", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			curve_socket_2.attribute_domain = 'POINT'

			#Socket Selection
			selection_socket_7 = curve_split_splines.interface.new_socket(name = "Selection", in_out='INPUT', socket_type = 'NodeSocketBool')
			selection_socket_7.attribute_domain = 'POINT'
			selection_socket_7.hide_value = True

			#Socket Curve Normal
			curve_normal_socket = curve_split_splines.interface.new_socket(name = "Curve Normal", in_out='INPUT', socket_type = 'NodeSocketMenu')
			curve_normal_socket.attribute_domain = 'POINT'

			#Socket Curve Group ID
			curve_group_id_socket = curve_split_splines.interface.new_socket(name = "Curve Group ID", in_out='INPUT', socket_type = 'NodeSocketInt')
			curve_group_id_socket.subtype = 'NONE'
			curve_group_id_socket.default_value = 0
			curve_group_id_socket.min_value = -2147483648
			curve_group_id_socket.max_value = 2147483647
			curve_group_id_socket.attribute_domain = 'POINT'

			#Socket Distance Split
			distance_split_socket = curve_split_splines.interface.new_socket(name = "Distance Split", in_out='INPUT', socket_type = 'NodeSocketMenu')
			distance_split_socket.attribute_domain = 'POINT'

			#Socket Distance Cutoff
			distance_cutoff_socket = curve_split_splines.interface.new_socket(name = "Distance Cutoff", in_out='INPUT', socket_type = 'NodeSocketFloat')
			distance_cutoff_socket.subtype = 'NONE'
			distance_cutoff_socket.default_value = 0.0
			distance_cutoff_socket.min_value = -10000.0
			distance_cutoff_socket.max_value = 10000.0
			distance_cutoff_socket.attribute_domain = 'POINT'

			#Socket Rotation
			rotation_socket_3 = curve_split_splines.interface.new_socket(name = "Rotation", in_out='INPUT', socket_type = 'NodeSocketRotation')
			rotation_socket_3.attribute_domain = 'POINT'
			rotation_socket_3.hide_value = True

			#Panel Offset
			offset_panel = curve_split_splines.interface.new_panel("Offset")
			#Socket Offset Rotation
			offset_rotation_socket = curve_split_splines.interface.new_socket(name = "Offset Rotation", in_out='OUTPUT', socket_type = 'NodeSocketRotation', parent = offset_panel)
			offset_rotation_socket.attribute_domain = 'POINT'

			#Socket Offset Position
			offset_position_socket = curve_split_splines.interface.new_socket(name = "Offset Position", in_out='OUTPUT', socket_type = 'NodeSocketVector', parent = offset_panel)
			offset_position_socket.subtype = 'NONE'
			offset_position_socket.default_value = (0.0, 0.0, 0.0)
			offset_position_socket.min_value = -3.4028234663852886e+38
			offset_position_socket.max_value = 3.4028234663852886e+38
			offset_position_socket.attribute_domain = 'POINT'

			#Socket Offset Tangent
			offset_tangent_socket = curve_split_splines.interface.new_socket(name = "Offset Tangent", in_out='OUTPUT', socket_type = 'NodeSocketVector', parent = offset_panel)
			offset_tangent_socket.subtype = 'NONE'
			offset_tangent_socket.default_value = (0.0, 0.0, 0.0)
			offset_tangent_socket.min_value = -3.4028234663852886e+38
			offset_tangent_socket.max_value = 3.4028234663852886e+38
			offset_tangent_socket.attribute_domain = 'POINT'

			#Socket Offset Normal
			offset_normal_socket = curve_split_splines.interface.new_socket(name = "Offset Normal", in_out='OUTPUT', socket_type = 'NodeSocketVector', parent = offset_panel)
			offset_normal_socket.subtype = 'NONE'
			offset_normal_socket.default_value = (0.0, 0.0, 0.0)
			offset_normal_socket.min_value = -3.4028234663852886e+38
			offset_normal_socket.max_value = 3.4028234663852886e+38
			offset_normal_socket.attribute_domain = 'POINT'

			#Socket Offset Amount
			offset_amount_socket = curve_split_splines.interface.new_socket(name = "Offset Amount", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = offset_panel)
			offset_amount_socket.subtype = 'NONE'
			offset_amount_socket.default_value = 0.0
			offset_amount_socket.min_value = -10000.0
			offset_amount_socket.max_value = 10000.0
			offset_amount_socket.attribute_domain = 'POINT'

			#Socket Offset Spline Type
			offset_spline_type_socket = curve_split_splines.interface.new_socket(name = "Offset Spline Type", in_out='INPUT', socket_type = 'NodeSocketMenu', parent = offset_panel)
			offset_spline_type_socket.attribute_domain = 'POINT'

			#Socket Offset Resolution
			offset_resolution_socket = curve_split_splines.interface.new_socket(name = "Offset Resolution", in_out='INPUT', socket_type = 'NodeSocketInt', parent = offset_panel)
			offset_resolution_socket.subtype = 'NONE'
			offset_resolution_socket.default_value = 12
			offset_resolution_socket.min_value = 1
			offset_resolution_socket.max_value = 2147483647
			offset_resolution_socket.attribute_domain = 'POINT'



			#initialize curve_split_splines nodes
			#node Group Output
			group_output_40 = curve_split_splines.nodes.new("NodeGroupOutput")
			group_output_40.name = "Group Output"
			group_output_40.is_active_output = True

			#node Group Input
			group_input_40 = curve_split_splines.nodes.new("NodeGroupInput")
			group_input_40.name = "Group Input"
			group_input_40.outputs[2].hide = True
			group_input_40.outputs[4].hide = True
			group_input_40.outputs[7].hide = True
			group_input_40.outputs[8].hide = True
			group_input_40.outputs[9].hide = True
			group_input_40.outputs[10].hide = True

			#node Curve to Points
			curve_to_points = curve_split_splines.nodes.new("GeometryNodeCurveToPoints")
			curve_to_points.name = "Curve to Points"
			curve_to_points.mode = 'EVALUATED'
			curve_to_points.inputs[1].hide = True
			curve_to_points.inputs[2].hide = True
			curve_to_points.outputs[1].hide = True
			curve_to_points.outputs[3].hide = True

			#node Points to Curves
			points_to_curves = curve_split_splines.nodes.new("GeometryNodePointsToCurves")
			points_to_curves.name = "Points to Curves"
			#Weight
			points_to_curves.inputs[2].default_value = 0.0

			#node Menu Switch
			menu_switch_1 = curve_split_splines.nodes.new("GeometryNodeMenuSwitch")
			menu_switch_1.name = "Menu Switch"
			menu_switch_1.active_index = 1
			menu_switch_1.data_type = 'GEOMETRY'
			menu_switch_1.enum_items.clear()
			menu_switch_1.enum_items.new("Minimum Twist")
			menu_switch_1.enum_items[0].description = ""
			menu_switch_1.enum_items.new("Free")
			menu_switch_1.enum_items[1].description = ""

			#node Set Curve Normal
			set_curve_normal_1 = curve_split_splines.nodes.new("GeometryNodeSetCurveNormal")
			set_curve_normal_1.name = "Set Curve Normal"
			set_curve_normal_1.mode = 'FREE'
			#Selection
			set_curve_normal_1.inputs[1].default_value = True

			#node Separate Geometry
			separate_geometry_1 = curve_split_splines.nodes.new("GeometryNodeSeparateGeometry")
			separate_geometry_1.name = "Separate Geometry"
			separate_geometry_1.domain = 'POINT'

			#node Group Input.001
			group_input_001_4 = curve_split_splines.nodes.new("NodeGroupInput")
			group_input_001_4.name = "Group Input.001"
			group_input_001_4.outputs[0].hide = True
			group_input_001_4.outputs[1].hide = True
			group_input_001_4.outputs[3].hide = True
			group_input_001_4.outputs[4].hide = True
			group_input_001_4.outputs[5].hide = True
			group_input_001_4.outputs[6].hide = True
			group_input_001_4.outputs[7].hide = True
			group_input_001_4.outputs[8].hide = True
			group_input_001_4.outputs[9].hide = True
			group_input_001_4.outputs[10].hide = True

			#node Menu Switch.001
			menu_switch_001 = curve_split_splines.nodes.new("GeometryNodeMenuSwitch")
			menu_switch_001.name = "Menu Switch.001"
			menu_switch_001.active_index = 1
			menu_switch_001.data_type = 'INT'
			menu_switch_001.enum_items.clear()
			menu_switch_001.enum_items.new("Ignore Distance")
			menu_switch_001.enum_items[0].description = ""
			menu_switch_001.enum_items.new("Split Distance")
			menu_switch_001.enum_items[1].description = ""

			#node Group
			group_14 = curve_split_splines.nodes.new("GeometryNodeGroup")
			group_14.name = "Group"
			group_14.node_tree = offset_vector
			#Socket_2
			group_14.inputs[0].default_value = 0
			#Socket_0
			group_14.inputs[1].default_value = (0.0, 0.0, 0.0)
			#Socket_3
			group_14.inputs[2].default_value = -1

			#node Vector Math
			vector_math_1 = curve_split_splines.nodes.new("ShaderNodeVectorMath")
			vector_math_1.name = "Vector Math"
			vector_math_1.operation = 'DISTANCE'

			#node Position
			position_1 = curve_split_splines.nodes.new("GeometryNodeInputPosition")
			position_1.name = "Position"

			#node Compare
			compare_5 = curve_split_splines.nodes.new("FunctionNodeCompare")
			compare_5.name = "Compare"
			compare_5.data_type = 'FLOAT'
			compare_5.mode = 'ELEMENT'
			compare_5.operation = 'GREATER_THAN'

			#node Accumulate Field
			accumulate_field_2 = curve_split_splines.nodes.new("GeometryNodeAccumulateField")
			accumulate_field_2.name = "Accumulate Field"
			accumulate_field_2.data_type = 'INT'
			accumulate_field_2.domain = 'POINT'
			#Group Index
			accumulate_field_2.inputs[1].default_value = 0

			#node Math
			math_10 = curve_split_splines.nodes.new("ShaderNodeMath")
			math_10.name = "Math"
			math_10.operation = 'ADD'
			math_10.use_clamp = False

			#node Index
			index_3 = curve_split_splines.nodes.new("GeometryNodeInputIndex")
			index_3.name = "Index"

			#node Reroute
			reroute_7 = curve_split_splines.nodes.new("NodeReroute")
			reroute_7.name = "Reroute"
			#node Sample Curve
			sample_curve = curve_split_splines.nodes.new("GeometryNodeSampleCurve")
			sample_curve.name = "Sample Curve"
			sample_curve.data_type = 'QUATERNION'
			sample_curve.mode = 'FACTOR'
			sample_curve.use_all_curves = False

			#node Curve of Point
			curve_of_point_1 = curve_split_splines.nodes.new("GeometryNodeCurveOfPoint")
			curve_of_point_1.name = "Curve of Point"
			curve_of_point_1.inputs[0].hide = True
			curve_of_point_1.outputs[1].hide = True
			#Point Index
			curve_of_point_1.inputs[0].default_value = 0

			#node Set Position
			set_position_1 = curve_split_splines.nodes.new("GeometryNodeSetPosition")
			set_position_1.name = "Set Position"
			#Selection
			set_position_1.inputs[1].default_value = True
			#Offset
			set_position_1.inputs[3].default_value = (0.0, 0.0, 0.0)

			#node Group.002
			group_002_6 = curve_split_splines.nodes.new("GeometryNodeGroup")
			group_002_6.name = "Group.002"
			group_002_6.node_tree = offset_point_along_curve
			#Socket_6
			group_002_6.inputs[0].default_value = 0

			#node Capture Attribute.002
			capture_attribute_002 = curve_split_splines.nodes.new("GeometryNodeCaptureAttribute")
			capture_attribute_002.name = "Capture Attribute.002"
			capture_attribute_002.active_index = 9
			capture_attribute_002.capture_items.clear()
			capture_attribute_002.capture_items.new('FLOAT', "Factor")
			capture_attribute_002.capture_items["Factor"].data_type = 'FLOAT'
			capture_attribute_002.capture_items.new('FLOAT', "Curve Index")
			capture_attribute_002.capture_items["Curve Index"].data_type = 'INT'
			capture_attribute_002.capture_items.new('FLOAT', "Selection")
			capture_attribute_002.capture_items["Selection"].data_type = 'BOOLEAN'
			capture_attribute_002.capture_items.new('FLOAT', "Curve Group ID")
			capture_attribute_002.capture_items["Curve Group ID"].data_type = 'INT'
			capture_attribute_002.capture_items.new('FLOAT', "Distance Cutoff")
			capture_attribute_002.capture_items["Distance Cutoff"].data_type = 'FLOAT'
			capture_attribute_002.capture_items.new('FLOAT', "Rotation")
			capture_attribute_002.capture_items["Rotation"].data_type = 'QUATERNION'
			capture_attribute_002.capture_items.new('FLOAT', "Index")
			capture_attribute_002.capture_items["Index"].data_type = 'INT'
			capture_attribute_002.capture_items.new('FLOAT', "Normal")
			capture_attribute_002.capture_items["Normal"].data_type = 'FLOAT_VECTOR'
			capture_attribute_002.capture_items.new('FLOAT', "Position")
			capture_attribute_002.capture_items["Position"].data_type = 'FLOAT_VECTOR'
			capture_attribute_002.capture_items.new('FLOAT', "Trailing")
			capture_attribute_002.capture_items["Trailing"].data_type = 'INT'
			capture_attribute_002.domain = 'POINT'

			#node Normal
			normal = curve_split_splines.nodes.new("GeometryNodeInputNormal")
			normal.name = "Normal"

			#node Position.001
			position_001_1 = curve_split_splines.nodes.new("GeometryNodeInputPosition")
			position_001_1.name = "Position.001"

			#node Group Input.002
			group_input_002 = curve_split_splines.nodes.new("NodeGroupInput")
			group_input_002.name = "Group Input.002"
			group_input_002.outputs[0].hide = True
			group_input_002.outputs[1].hide = True
			group_input_002.outputs[2].hide = True
			group_input_002.outputs[3].hide = True
			group_input_002.outputs[4].hide = True
			group_input_002.outputs[5].hide = True
			group_input_002.outputs[6].hide = True
			group_input_002.outputs[8].hide = True
			group_input_002.outputs[9].hide = True
			group_input_002.outputs[10].hide = True

			#node Set Spline Resolution
			set_spline_resolution_1 = curve_split_splines.nodes.new("GeometryNodeSetSplineResolution")
			set_spline_resolution_1.name = "Set Spline Resolution"
			#Selection
			set_spline_resolution_1.inputs[1].default_value = True

			#node Menu Switch.002
			menu_switch_002_1 = curve_split_splines.nodes.new("GeometryNodeMenuSwitch")
			menu_switch_002_1.name = "Menu Switch.002"
			menu_switch_002_1.active_index = 1
			menu_switch_002_1.data_type = 'GEOMETRY'
			menu_switch_002_1.enum_items.clear()
			menu_switch_002_1.enum_items.new("Poly")
			menu_switch_002_1.enum_items[0].description = ""
			menu_switch_002_1.enum_items.new("Bezier")
			menu_switch_002_1.enum_items[1].description = ""

			#node Reroute.005
			reroute_005 = curve_split_splines.nodes.new("NodeReroute")
			reroute_005.name = "Reroute.005"
			#node Group Input.003
			group_input_003 = curve_split_splines.nodes.new("NodeGroupInput")
			group_input_003.name = "Group Input.003"
			group_input_003.outputs[0].hide = True
			group_input_003.outputs[1].hide = True
			group_input_003.outputs[2].hide = True
			group_input_003.outputs[3].hide = True
			group_input_003.outputs[4].hide = True
			group_input_003.outputs[5].hide = True
			group_input_003.outputs[6].hide = True
			group_input_003.outputs[7].hide = True
			group_input_003.outputs[9].hide = True
			group_input_003.outputs[10].hide = True

			#node Group Input.004
			group_input_004 = curve_split_splines.nodes.new("NodeGroupInput")
			group_input_004.name = "Group Input.004"
			group_input_004.outputs[0].hide = True
			group_input_004.outputs[1].hide = True
			group_input_004.outputs[2].hide = True
			group_input_004.outputs[3].hide = True
			group_input_004.outputs[4].hide = True
			group_input_004.outputs[5].hide = True
			group_input_004.outputs[6].hide = True
			group_input_004.outputs[7].hide = True
			group_input_004.outputs[8].hide = True
			group_input_004.outputs[10].hide = True

			#node Group Input.005
			group_input_005 = curve_split_splines.nodes.new("NodeGroupInput")
			group_input_005.name = "Group Input.005"
			group_input_005.outputs[0].hide = True
			group_input_005.outputs[1].hide = True
			group_input_005.outputs[2].hide = True
			group_input_005.outputs[3].hide = True
			group_input_005.outputs[5].hide = True
			group_input_005.outputs[6].hide = True
			group_input_005.outputs[7].hide = True
			group_input_005.outputs[8].hide = True
			group_input_005.outputs[9].hide = True
			group_input_005.outputs[10].hide = True

			#node Reroute.001
			reroute_001_6 = curve_split_splines.nodes.new("NodeReroute")
			reroute_001_6.name = "Reroute.001"
			#node Reroute.003
			reroute_003_3 = curve_split_splines.nodes.new("NodeReroute")
			reroute_003_3.name = "Reroute.003"
			#node Reroute.004
			reroute_004_1 = curve_split_splines.nodes.new("NodeReroute")
			reroute_004_1.name = "Reroute.004"
			#node Reroute.006
			reroute_006 = curve_split_splines.nodes.new("NodeReroute")
			reroute_006.name = "Reroute.006"
			#node Reroute.007
			reroute_007 = curve_split_splines.nodes.new("NodeReroute")
			reroute_007.name = "Reroute.007"
			#node Reroute.008
			reroute_008 = curve_split_splines.nodes.new("NodeReroute")
			reroute_008.name = "Reroute.008"
			#node Reroute.009
			reroute_009 = curve_split_splines.nodes.new("NodeReroute")
			reroute_009.name = "Reroute.009"
			#node Reroute.010
			reroute_010 = curve_split_splines.nodes.new("NodeReroute")
			reroute_010.name = "Reroute.010"
			#node Reroute.011
			reroute_011 = curve_split_splines.nodes.new("NodeReroute")
			reroute_011.name = "Reroute.011"
			#node Reroute.002
			reroute_002_4 = curve_split_splines.nodes.new("NodeReroute")
			reroute_002_4.name = "Reroute.002"
			#node Frame
			frame_1 = curve_split_splines.nodes.new("NodeFrame")
			frame_1.label = "Potentially sample a new interpolated point along the curve"
			frame_1.name = "Frame"
			frame_1.label_size = 20
			frame_1.shrink = True

			#node Accumulate Field.001
			accumulate_field_001_3 = curve_split_splines.nodes.new("GeometryNodeAccumulateField")
			accumulate_field_001_3.name = "Accumulate Field.001"
			accumulate_field_001_3.data_type = 'INT'
			accumulate_field_001_3.domain = 'POINT'
			#Group Index
			accumulate_field_001_3.inputs[1].default_value = 0

			#node Boolean Math
			boolean_math_7 = curve_split_splines.nodes.new("FunctionNodeBooleanMath")
			boolean_math_7.name = "Boolean Math"
			boolean_math_7.operation = 'NOT'

			#node Reroute.012
			reroute_012 = curve_split_splines.nodes.new("NodeReroute")
			reroute_012.name = "Reroute.012"
			#node Set Spline Resolution.001
			set_spline_resolution_001 = curve_split_splines.nodes.new("GeometryNodeSetSplineResolution")
			set_spline_resolution_001.name = "Set Spline Resolution.001"
			#Selection
			set_spline_resolution_001.inputs[1].default_value = True
			#Resolution
			set_spline_resolution_001.inputs[2].default_value = 1

			#node Set Handle Positions
			set_handle_positions = curve_split_splines.nodes.new("GeometryNodeSetCurveHandlePositions")
			set_handle_positions.name = "Set Handle Positions"
			set_handle_positions.mode = 'LEFT'
			#Selection
			set_handle_positions.inputs[1].default_value = True
			#Offset
			set_handle_positions.inputs[3].default_value = (0.0, 0.0, 0.0)

			#node Set Spline Type
			set_spline_type_1 = curve_split_splines.nodes.new("GeometryNodeCurveSplineType")
			set_spline_type_1.name = "Set Spline Type"
			set_spline_type_1.spline_type = 'BEZIER'
			#Selection
			set_spline_type_1.inputs[1].default_value = True

			#node Set Handle Type
			set_handle_type_1 = curve_split_splines.nodes.new("GeometryNodeCurveSetHandles")
			set_handle_type_1.name = "Set Handle Type"
			set_handle_type_1.handle_type = 'AUTO'
			set_handle_type_1.mode = {'LEFT', 'RIGHT'}
			#Selection
			set_handle_type_1.inputs[1].default_value = True

			#node Set Handle Positions.001
			set_handle_positions_001 = curve_split_splines.nodes.new("GeometryNodeSetCurveHandlePositions")
			set_handle_positions_001.name = "Set Handle Positions.001"
			set_handle_positions_001.mode = 'RIGHT'
			#Selection
			set_handle_positions_001.inputs[1].default_value = True
			#Offset
			set_handle_positions_001.inputs[3].default_value = (0.0, 0.0, 0.0)

			#node Capture Attribute
			capture_attribute_3 = curve_split_splines.nodes.new("GeometryNodeCaptureAttribute")
			capture_attribute_3.name = "Capture Attribute"
			capture_attribute_3.active_index = 1
			capture_attribute_3.capture_items.clear()
			capture_attribute_3.capture_items.new('FLOAT', "Left")
			capture_attribute_3.capture_items["Left"].data_type = 'FLOAT_VECTOR'
			capture_attribute_3.capture_items.new('FLOAT', "Right")
			capture_attribute_3.capture_items["Right"].data_type = 'FLOAT_VECTOR'
			capture_attribute_3.domain = 'POINT'

			#node Curve Handle Positions
			curve_handle_positions = curve_split_splines.nodes.new("GeometryNodeInputCurveHandlePositions")
			curve_handle_positions.name = "Curve Handle Positions"
			#Relative
			curve_handle_positions.inputs[0].default_value = False

			#node Set Spline Type.001
			set_spline_type_001 = curve_split_splines.nodes.new("GeometryNodeCurveSplineType")
			set_spline_type_001.name = "Set Spline Type.001"
			set_spline_type_001.spline_type = 'BEZIER'
			#Selection
			set_spline_type_001.inputs[1].default_value = True

			#node Set Handle Type.001
			set_handle_type_001 = curve_split_splines.nodes.new("GeometryNodeCurveSetHandles")
			set_handle_type_001.name = "Set Handle Type.001"
			set_handle_type_001.handle_type = 'AUTO'
			set_handle_type_001.mode = {'LEFT', 'RIGHT'}
			#Selection
			set_handle_type_001.inputs[1].default_value = True



			#Set parents
			sample_curve.parent = frame_1
			set_spline_resolution_1.parent = frame_1
			menu_switch_002_1.parent = frame_1
			reroute_005.parent = frame_1
			group_input_003.parent = frame_1
			group_input_004.parent = frame_1

			#Set locations
			group_output_40.location = (-180.0, 140.0)
			group_input_40.location = (-3089.593505859375, -21.9822998046875)
			curve_to_points.location = (-1820.0, 40.0)
			points_to_curves.location = (-1260.0, 0.0)
			menu_switch_1.location = (-1080.0, 20.0)
			set_curve_normal_1.location = (-1080.0, -160.0)
			separate_geometry_1.location = (-1620.0, 0.0)
			group_input_001_4.location = (-1260.0, 80.0)
			menu_switch_001.location = (-1260.0, -140.0)
			group_14.location = (-2140.0, -340.0)
			vector_math_1.location = (-1980.0, -340.0)
			position_1.location = (-2140.0, -500.0)
			compare_5.location = (-1820.0, -340.0)
			accumulate_field_2.location = (-1660.0, -340.0)
			math_10.location = (-1500.0, -340.0)
			index_3.location = (-3087.200439453125, -180.0)
			reroute_7.location = (-1700.0, -160.0)
			sample_curve.location = (-1300.0, 460.0)
			curve_of_point_1.location = (-3087.200439453125, 40.0)
			set_position_1.location = (-1460.0, 0.0)
			group_002_6.location = (-3087.200439453125, 220.0)
			capture_attribute_002.location = (-2767.200439453125, 40.0)
			normal.location = (-3087.200439453125, -240.0)
			position_001_1.location = (-3087.200439453125, -300.0)
			group_input_002.location = (-3247.200439453125, 220.0)
			set_spline_resolution_1.location = (-1500.0, 660.0)
			menu_switch_002_1.location = (-1500.0, 520.0)
			reroute_005.location = (-1576.0, 600.0)
			group_input_003.location = (-1660.0, 480.0)
			group_input_004.location = (-1660.0, 540.0)
			group_input_005.location = (-1640.0, -200.0)
			reroute_001_6.location = (-2260.0, -180.0)
			reroute_003_3.location = (-2260.0, -160.0)
			reroute_004_1.location = (-2260.0, -200.0)
			reroute_006.location = (-2260.0, -100.0)
			reroute_007.location = (-2260.0, -120.0)
			reroute_008.location = (-2260.0, -80.0)
			reroute_009.location = (-2260.0, -60.0)
			reroute_010.location = (-2260.0, -140.0)
			reroute_011.location = (-2260.0, -220.0)
			reroute_002_4.location = (-1520.0, -300.0)
			frame_1.location = (-650.0, -60.0)
			accumulate_field_001_3.location = (-2927.200439453125, -360.0)
			boolean_math_7.location = (-3087.200439453125, -360.0)
			reroute_012.location = (-2260.0, -240.0)
			set_spline_resolution_001.location = (-2180.0, 40.0)
			set_handle_positions.location = (-600.0, 20.0)
			set_spline_type_1.location = (-920.0, 20.0)
			set_handle_type_1.location = (-760.0, 20.0)
			set_handle_positions_001.location = (-440.0, 20.0)
			capture_attribute_3.location = (-2000.0, 40.0)
			curve_handle_positions.location = (-2180.0, -100.0)
			set_spline_type_001.location = (-2500.0, 40.0)
			set_handle_type_001.location = (-2340.0, 40.0)

			#Set dimensions
			group_output_40.width, group_output_40.height = 140.0, 100.0
			group_input_40.width, group_input_40.height = 140.0, 100.0
			curve_to_points.width, curve_to_points.height = 140.0, 100.0
			points_to_curves.width, points_to_curves.height = 140.0, 100.0
			menu_switch_1.width, menu_switch_1.height = 140.0, 100.0
			set_curve_normal_1.width, set_curve_normal_1.height = 140.0, 100.0
			separate_geometry_1.width, separate_geometry_1.height = 140.0, 100.0
			group_input_001_4.width, group_input_001_4.height = 140.0, 100.0
			menu_switch_001.width, menu_switch_001.height = 140.0, 100.0
			group_14.width, group_14.height = 140.0, 100.0
			vector_math_1.width, vector_math_1.height = 140.0, 100.0
			position_1.width, position_1.height = 140.0, 100.0
			compare_5.width, compare_5.height = 140.0, 100.0
			accumulate_field_2.width, accumulate_field_2.height = 140.0, 100.0
			math_10.width, math_10.height = 140.0, 100.0
			index_3.width, index_3.height = 140.0, 100.0
			reroute_7.width, reroute_7.height = 16.0, 100.0
			sample_curve.width, sample_curve.height = 140.0, 100.0
			curve_of_point_1.width, curve_of_point_1.height = 140.0, 100.0
			set_position_1.width, set_position_1.height = 140.0, 100.0
			group_002_6.width, group_002_6.height = 140.0, 100.0
			capture_attribute_002.width, capture_attribute_002.height = 140.0, 100.0
			normal.width, normal.height = 140.0, 100.0
			position_001_1.width, position_001_1.height = 140.0, 100.0
			group_input_002.width, group_input_002.height = 140.0, 100.0
			set_spline_resolution_1.width, set_spline_resolution_1.height = 140.0, 100.0
			menu_switch_002_1.width, menu_switch_002_1.height = 140.0, 100.0
			reroute_005.width, reroute_005.height = 16.0, 100.0
			group_input_003.width, group_input_003.height = 140.0, 100.0
			group_input_004.width, group_input_004.height = 140.0, 100.0
			group_input_005.width, group_input_005.height = 140.0, 100.0
			reroute_001_6.width, reroute_001_6.height = 16.0, 100.0
			reroute_003_3.width, reroute_003_3.height = 16.0, 100.0
			reroute_004_1.width, reroute_004_1.height = 16.0, 100.0
			reroute_006.width, reroute_006.height = 16.0, 100.0
			reroute_007.width, reroute_007.height = 16.0, 100.0
			reroute_008.width, reroute_008.height = 16.0, 100.0
			reroute_009.width, reroute_009.height = 16.0, 100.0
			reroute_010.width, reroute_010.height = 16.0, 100.0
			reroute_011.width, reroute_011.height = 16.0, 100.0
			reroute_002_4.width, reroute_002_4.height = 16.0, 100.0
			frame_1.width, frame_1.height = 559.9998779296875, 553.2000122070312
			accumulate_field_001_3.width, accumulate_field_001_3.height = 140.0, 100.0
			boolean_math_7.width, boolean_math_7.height = 140.0, 100.0
			reroute_012.width, reroute_012.height = 16.0, 100.0
			set_spline_resolution_001.width, set_spline_resolution_001.height = 140.0, 100.0
			set_handle_positions.width, set_handle_positions.height = 140.0, 100.0
			set_spline_type_1.width, set_spline_type_1.height = 140.0, 100.0
			set_handle_type_1.width, set_handle_type_1.height = 140.0, 100.0
			set_handle_positions_001.width, set_handle_positions_001.height = 140.0, 100.0
			capture_attribute_3.width, capture_attribute_3.height = 140.0, 100.0
			curve_handle_positions.width, curve_handle_positions.height = 150.0, 100.0
			set_spline_type_001.width, set_spline_type_001.height = 140.0, 100.0
			set_handle_type_001.width, set_handle_type_001.height = 140.0, 100.0

			#initialize curve_split_splines links
			#capture_attribute_3.Geometry -> curve_to_points.Curve
			curve_split_splines.links.new(capture_attribute_3.outputs[0], curve_to_points.inputs[0])
			#points_to_curves.Curves -> menu_switch_1.Minimum Twist
			curve_split_splines.links.new(points_to_curves.outputs[0], menu_switch_1.inputs[1])
			#points_to_curves.Curves -> set_curve_normal_1.Curve
			curve_split_splines.links.new(points_to_curves.outputs[0], set_curve_normal_1.inputs[0])
			#set_curve_normal_1.Curve -> menu_switch_1.Free
			curve_split_splines.links.new(set_curve_normal_1.outputs[0], menu_switch_1.inputs[2])
			#group_input_001_4.Curve Normal -> menu_switch_1.Menu
			curve_split_splines.links.new(group_input_001_4.outputs[2], menu_switch_1.inputs[0])
			#group_14.Value -> vector_math_1.Vector
			curve_split_splines.links.new(group_14.outputs[0], vector_math_1.inputs[0])
			#position_1.Position -> vector_math_1.Vector
			curve_split_splines.links.new(position_1.outputs[0], vector_math_1.inputs[1])
			#reroute_002_4.Output -> math_10.Value
			curve_split_splines.links.new(reroute_002_4.outputs[0], math_10.inputs[0])
			#accumulate_field_2.Leading -> math_10.Value
			curve_split_splines.links.new(accumulate_field_2.outputs[0], math_10.inputs[1])
			#compare_5.Result -> accumulate_field_2.Value
			curve_split_splines.links.new(compare_5.outputs[0], accumulate_field_2.inputs[0])
			#reroute_002_4.Output -> menu_switch_001.Ignore Distance
			curve_split_splines.links.new(reroute_002_4.outputs[0], menu_switch_001.inputs[1])
			#math_10.Value -> menu_switch_001.Split Distance
			curve_split_splines.links.new(math_10.outputs[0], menu_switch_001.inputs[2])
			#vector_math_1.Value -> compare_5.A
			curve_split_splines.links.new(vector_math_1.outputs[1], compare_5.inputs[0])
			#reroute_001_6.Output -> group_output_40.Index
			curve_split_splines.links.new(reroute_001_6.outputs[0], group_output_40.inputs[1])
			#reroute_004_1.Output -> set_curve_normal_1.Normal
			curve_split_splines.links.new(reroute_004_1.outputs[0], set_curve_normal_1.inputs[2])
			#curve_to_points.Points -> separate_geometry_1.Geometry
			curve_split_splines.links.new(curve_to_points.outputs[0], separate_geometry_1.inputs[0])
			#set_position_1.Geometry -> points_to_curves.Points
			curve_split_splines.links.new(set_position_1.outputs[0], points_to_curves.inputs[0])
			#reroute_006.Output -> reroute_7.Input
			curve_split_splines.links.new(reroute_006.outputs[0], reroute_7.inputs[0])
			#separate_geometry_1.Selection -> set_position_1.Geometry
			curve_split_splines.links.new(separate_geometry_1.outputs[0], set_position_1.inputs[0])
			#reroute_011.Output -> set_position_1.Position
			curve_split_splines.links.new(reroute_011.outputs[0], set_position_1.inputs[2])
			#reroute_003_3.Output -> group_output_40.Rotation
			curve_split_splines.links.new(reroute_003_3.outputs[0], group_output_40.inputs[2])
			#group_input_40.Curve -> capture_attribute_002.Geometry
			curve_split_splines.links.new(group_input_40.outputs[0], capture_attribute_002.inputs[0])
			#group_input_40.Rotation -> capture_attribute_002.Rotation
			curve_split_splines.links.new(group_input_40.outputs[6], capture_attribute_002.inputs[6])
			#reroute_003_3.Output -> sample_curve.Value
			curve_split_splines.links.new(reroute_003_3.outputs[0], sample_curve.inputs[1])
			#group_input_40.Distance Cutoff -> capture_attribute_002.Distance Cutoff
			curve_split_splines.links.new(group_input_40.outputs[5], capture_attribute_002.inputs[5])
			#reroute_010.Output -> compare_5.B
			curve_split_splines.links.new(reroute_010.outputs[0], compare_5.inputs[1])
			#sample_curve.Value -> group_output_40.Offset Rotation
			curve_split_splines.links.new(sample_curve.outputs[0], group_output_40.inputs[3])
			#sample_curve.Position -> group_output_40.Offset Position
			curve_split_splines.links.new(sample_curve.outputs[1], group_output_40.inputs[4])
			#sample_curve.Tangent -> group_output_40.Offset Tangent
			curve_split_splines.links.new(sample_curve.outputs[2], group_output_40.inputs[5])
			#sample_curve.Normal -> group_output_40.Offset Normal
			curve_split_splines.links.new(sample_curve.outputs[3], group_output_40.inputs[6])
			#group_input_002.Offset Amount -> group_002_6.Value
			curve_split_splines.links.new(group_input_002.outputs[7], group_002_6.inputs[1])
			#reroute_005.Output -> set_spline_resolution_1.Geometry
			curve_split_splines.links.new(reroute_005.outputs[0], set_spline_resolution_1.inputs[0])
			#capture_attribute_002.Geometry -> reroute_005.Input
			curve_split_splines.links.new(capture_attribute_002.outputs[0], reroute_005.inputs[0])
			#set_spline_resolution_1.Geometry -> menu_switch_002_1.Bezier
			curve_split_splines.links.new(set_spline_resolution_1.outputs[0], menu_switch_002_1.inputs[2])
			#reroute_005.Output -> menu_switch_002_1.Poly
			curve_split_splines.links.new(reroute_005.outputs[0], menu_switch_002_1.inputs[1])
			#menu_switch_002_1.Output -> sample_curve.Curves
			curve_split_splines.links.new(menu_switch_002_1.outputs[0], sample_curve.inputs[0])
			#group_input_003.Offset Spline Type -> menu_switch_002_1.Menu
			curve_split_splines.links.new(group_input_003.outputs[8], menu_switch_002_1.inputs[0])
			#group_input_004.Offset Resolution -> set_spline_resolution_1.Resolution
			curve_split_splines.links.new(group_input_004.outputs[9], set_spline_resolution_1.inputs[2])
			#group_002_6.Factor -> capture_attribute_002.Factor
			curve_split_splines.links.new(group_002_6.outputs[0], capture_attribute_002.inputs[1])
			#reroute_009.Output -> sample_curve.Factor
			curve_split_splines.links.new(reroute_009.outputs[0], sample_curve.inputs[2])
			#curve_of_point_1.Curve Index -> capture_attribute_002.Curve Index
			curve_split_splines.links.new(curve_of_point_1.outputs[0], capture_attribute_002.inputs[2])
			#reroute_008.Output -> sample_curve.Curve Index
			curve_split_splines.links.new(reroute_008.outputs[0], sample_curve.inputs[4])
			#group_input_40.Selection -> capture_attribute_002.Selection
			curve_split_splines.links.new(group_input_40.outputs[1], capture_attribute_002.inputs[3])
			#group_input_40.Curve Group ID -> capture_attribute_002.Curve Group ID
			curve_split_splines.links.new(group_input_40.outputs[3], capture_attribute_002.inputs[4])
			#group_input_005.Distance Split -> menu_switch_001.Menu
			curve_split_splines.links.new(group_input_005.outputs[4], menu_switch_001.inputs[0])
			#index_3.Index -> capture_attribute_002.Index
			curve_split_splines.links.new(index_3.outputs[0], capture_attribute_002.inputs[7])
			#normal.Normal -> capture_attribute_002.Normal
			curve_split_splines.links.new(normal.outputs[0], capture_attribute_002.inputs[8])
			#position_001_1.Position -> capture_attribute_002.Position
			curve_split_splines.links.new(position_001_1.outputs[0], capture_attribute_002.inputs[9])
			#capture_attribute_002.Index -> reroute_001_6.Input
			curve_split_splines.links.new(capture_attribute_002.outputs[7], reroute_001_6.inputs[0])
			#capture_attribute_002.Rotation -> reroute_003_3.Input
			curve_split_splines.links.new(capture_attribute_002.outputs[6], reroute_003_3.inputs[0])
			#capture_attribute_002.Normal -> reroute_004_1.Input
			curve_split_splines.links.new(capture_attribute_002.outputs[8], reroute_004_1.inputs[0])
			#capture_attribute_002.Selection -> reroute_006.Input
			curve_split_splines.links.new(capture_attribute_002.outputs[3], reroute_006.inputs[0])
			#capture_attribute_002.Curve Group ID -> reroute_007.Input
			curve_split_splines.links.new(capture_attribute_002.outputs[4], reroute_007.inputs[0])
			#capture_attribute_002.Curve Index -> reroute_008.Input
			curve_split_splines.links.new(capture_attribute_002.outputs[2], reroute_008.inputs[0])
			#capture_attribute_002.Factor -> reroute_009.Input
			curve_split_splines.links.new(capture_attribute_002.outputs[1], reroute_009.inputs[0])
			#capture_attribute_002.Distance Cutoff -> reroute_010.Input
			curve_split_splines.links.new(capture_attribute_002.outputs[5], reroute_010.inputs[0])
			#capture_attribute_002.Position -> reroute_011.Input
			curve_split_splines.links.new(capture_attribute_002.outputs[9], reroute_011.inputs[0])
			#set_handle_positions_001.Curve -> group_output_40.Curve
			curve_split_splines.links.new(set_handle_positions_001.outputs[0], group_output_40.inputs[0])
			#group_input_40.Selection -> boolean_math_7.Boolean
			curve_split_splines.links.new(group_input_40.outputs[1], boolean_math_7.inputs[0])
			#boolean_math_7.Boolean -> accumulate_field_001_3.Value
			curve_split_splines.links.new(boolean_math_7.outputs[0], accumulate_field_001_3.inputs[0])
			#menu_switch_001.Output -> points_to_curves.Curve Group ID
			curve_split_splines.links.new(menu_switch_001.outputs[0], points_to_curves.inputs[1])
			#reroute_012.Output -> reroute_002_4.Input
			curve_split_splines.links.new(reroute_012.outputs[0], reroute_002_4.inputs[0])
			#accumulate_field_001_3.Trailing -> capture_attribute_002.Trailing
			curve_split_splines.links.new(accumulate_field_001_3.outputs[1], capture_attribute_002.inputs[10])
			#capture_attribute_002.Trailing -> reroute_012.Input
			curve_split_splines.links.new(capture_attribute_002.outputs[10], reroute_012.inputs[0])
			#reroute_7.Output -> separate_geometry_1.Selection
			curve_split_splines.links.new(reroute_7.outputs[0], separate_geometry_1.inputs[1])
			#set_handle_type_001.Curve -> set_spline_resolution_001.Geometry
			curve_split_splines.links.new(set_handle_type_001.outputs[0], set_spline_resolution_001.inputs[0])
			#menu_switch_1.Output -> set_spline_type_1.Curve
			curve_split_splines.links.new(menu_switch_1.outputs[0], set_spline_type_1.inputs[0])
			#set_spline_type_1.Curve -> set_handle_type_1.Curve
			curve_split_splines.links.new(set_spline_type_1.outputs[0], set_handle_type_1.inputs[0])
			#set_handle_type_1.Curve -> set_handle_positions.Curve
			curve_split_splines.links.new(set_handle_type_1.outputs[0], set_handle_positions.inputs[0])
			#set_handle_positions.Curve -> set_handle_positions_001.Curve
			curve_split_splines.links.new(set_handle_positions.outputs[0], set_handle_positions_001.inputs[0])
			#set_spline_resolution_001.Geometry -> capture_attribute_3.Geometry
			curve_split_splines.links.new(set_spline_resolution_001.outputs[0], capture_attribute_3.inputs[0])
			#curve_handle_positions.Left -> capture_attribute_3.Left
			curve_split_splines.links.new(curve_handle_positions.outputs[0], capture_attribute_3.inputs[1])
			#curve_handle_positions.Right -> capture_attribute_3.Right
			curve_split_splines.links.new(curve_handle_positions.outputs[1], capture_attribute_3.inputs[2])
			#capture_attribute_3.Left -> set_handle_positions.Position
			curve_split_splines.links.new(capture_attribute_3.outputs[1], set_handle_positions.inputs[2])
			#capture_attribute_3.Right -> set_handle_positions_001.Position
			curve_split_splines.links.new(capture_attribute_3.outputs[2], set_handle_positions_001.inputs[2])
			#capture_attribute_002.Geometry -> set_spline_type_001.Curve
			curve_split_splines.links.new(capture_attribute_002.outputs[0], set_spline_type_001.inputs[0])
			#set_spline_type_001.Curve -> set_handle_type_001.Curve
			curve_split_splines.links.new(set_spline_type_001.outputs[0], set_handle_type_001.inputs[0])
			return curve_split_splines

		curve_split_splines = curve_split_splines_node_group()

		#initialize set_color node group
		def set_color_node_group():
			set_color = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Set Color")

			set_color.color_tag = 'GEOMETRY'
			set_color.description = ""

			set_color.is_modifier = True

			#set_color interface
			#Socket Atoms
			atoms_socket_4 = set_color.interface.new_socket(name = "Atoms", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			atoms_socket_4.attribute_domain = 'POINT'
			atoms_socket_4.description = "Atomic geometry with an updated `Color` attribute"

			#Socket Atoms
			atoms_socket_5 = set_color.interface.new_socket(name = "Atoms", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			atoms_socket_5.attribute_domain = 'POINT'
			atoms_socket_5.description = "Atomic geometry that contains vertices and edges"

			#Socket Selection
			selection_socket_8 = set_color.interface.new_socket(name = "Selection", in_out='INPUT', socket_type = 'NodeSocketBool')
			selection_socket_8.attribute_domain = 'POINT'
			selection_socket_8.hide_value = True
			selection_socket_8.description = "Selection of atoms to apply this node to"

			#Socket Color
			color_socket = set_color.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor')
			color_socket.attribute_domain = 'POINT'
			color_socket.description = "Color to apply to the selected atoms"


			#initialize set_color nodes
			#node Group Input
			group_input_41 = set_color.nodes.new("NodeGroupInput")
			group_input_41.name = "Group Input"

			#node Store Named Attribute
			store_named_attribute = set_color.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute.name = "Store Named Attribute"
			store_named_attribute.data_type = 'FLOAT_COLOR'
			store_named_attribute.domain = 'POINT'
			#Name
			store_named_attribute.inputs[2].default_value = "Color"

			#node Group Output
			group_output_41 = set_color.nodes.new("NodeGroupOutput")
			group_output_41.name = "Group Output"
			group_output_41.is_active_output = True




			#Set locations
			group_input_41.location = (-460.0, -80.0)
			store_named_attribute.location = (-260.0, -20.0)
			group_output_41.location = (-100.0, -20.0)

			#Set dimensions
			group_input_41.width, group_input_41.height = 140.0, 100.0
			store_named_attribute.width, store_named_attribute.height = 140.0, 100.0
			group_output_41.width, group_output_41.height = 140.0, 100.0

			#initialize set_color links
			#store_named_attribute.Geometry -> group_output_41.Atoms
			set_color.links.new(store_named_attribute.outputs[0], group_output_41.inputs[0])
			#group_input_41.Atoms -> store_named_attribute.Geometry
			set_color.links.new(group_input_41.outputs[0], store_named_attribute.inputs[0])
			#group_input_41.Selection -> store_named_attribute.Selection
			set_color.links.new(group_input_41.outputs[1], store_named_attribute.inputs[1])
			#group_input_41.Color -> store_named_attribute.Value
			set_color.links.new(group_input_41.outputs[2], store_named_attribute.inputs[3])
			return set_color

		set_color = set_color_node_group()

		#initialize offset_color node group
		def offset_color_node_group():
			offset_color = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Offset Color")

			offset_color.color_tag = 'CONVERTER'
			offset_color.description = ""


			#offset_color interface
			#Socket Color
			color_socket_1 = offset_color.interface.new_socket(name = "Color", in_out='OUTPUT', socket_type = 'NodeSocketColor')
			color_socket_1.attribute_domain = 'POINT'

			#Socket Index
			index_socket_9 = offset_color.interface.new_socket(name = "Index", in_out='INPUT', socket_type = 'NodeSocketInt')
			index_socket_9.subtype = 'NONE'
			index_socket_9.default_value = 0
			index_socket_9.min_value = -2147483648
			index_socket_9.max_value = 2147483647
			index_socket_9.attribute_domain = 'POINT'

			#Socket Offset
			offset_socket_5 = offset_color.interface.new_socket(name = "Offset", in_out='INPUT', socket_type = 'NodeSocketInt')
			offset_socket_5.subtype = 'NONE'
			offset_socket_5.default_value = 0
			offset_socket_5.min_value = -2147483648
			offset_socket_5.max_value = 2147483647
			offset_socket_5.attribute_domain = 'POINT'


			#initialize offset_color nodes
			#node Group Input
			group_input_42 = offset_color.nodes.new("NodeGroupInput")
			group_input_42.name = "Group Input"

			#node Math.012
			math_012 = offset_color.nodes.new("ShaderNodeMath")
			math_012.name = "Math.012"
			math_012.operation = 'ADD'
			math_012.use_clamp = False

			#node Evaluate at Index.004
			evaluate_at_index_004 = offset_color.nodes.new("GeometryNodeFieldAtIndex")
			evaluate_at_index_004.name = "Evaluate at Index.004"
			evaluate_at_index_004.data_type = 'FLOAT_COLOR'
			evaluate_at_index_004.domain = 'POINT'

			#node Group Output
			group_output_42 = offset_color.nodes.new("NodeGroupOutput")
			group_output_42.name = "Group Output"
			group_output_42.is_active_output = True

			#node Named Attribute
			named_attribute_5 = offset_color.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_5.name = "Named Attribute"
			named_attribute_5.data_type = 'FLOAT_COLOR'
			#Name
			named_attribute_5.inputs[0].default_value = "Color"




			#Set locations
			group_input_42.location = (-220.0, -20.0)
			math_012.location = (-40.0, 0.0)
			evaluate_at_index_004.location = (140.0, 0.0)
			group_output_42.location = (340.0, 0.0)
			named_attribute_5.location = (-40.0, -160.0)

			#Set dimensions
			group_input_42.width, group_input_42.height = 140.0, 100.0
			math_012.width, math_012.height = 140.0, 100.0
			evaluate_at_index_004.width, evaluate_at_index_004.height = 140.0, 100.0
			group_output_42.width, group_output_42.height = 140.0, 100.0
			named_attribute_5.width, named_attribute_5.height = 140.0, 100.0

			#initialize offset_color links
			#math_012.Value -> evaluate_at_index_004.Index
			offset_color.links.new(math_012.outputs[0], evaluate_at_index_004.inputs[0])
			#group_input_42.Offset -> math_012.Value
			offset_color.links.new(group_input_42.outputs[1], math_012.inputs[1])
			#evaluate_at_index_004.Value -> group_output_42.Color
			offset_color.links.new(evaluate_at_index_004.outputs[0], group_output_42.inputs[0])
			#named_attribute_5.Attribute -> evaluate_at_index_004.Value
			offset_color.links.new(named_attribute_5.outputs[0], evaluate_at_index_004.inputs[1])
			#group_input_42.Index -> math_012.Value
			offset_color.links.new(group_input_42.outputs[0], math_012.inputs[0])
			return offset_color

		offset_color = offset_color_node_group()

		#initialize curve_endpoint_values node group
		def curve_endpoint_values_node_group():
			curve_endpoint_values = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Curve Endpoint Values")

			curve_endpoint_values.color_tag = 'INPUT'
			curve_endpoint_values.description = ""


			#curve_endpoint_values interface
			#Socket Value
			value_socket_6 = curve_endpoint_values.interface.new_socket(name = "Value", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			value_socket_6.subtype = 'NONE'
			value_socket_6.default_value = 0
			value_socket_6.min_value = -2147483648
			value_socket_6.max_value = 2147483647
			value_socket_6.attribute_domain = 'POINT'

			#Socket Start Size
			start_size_socket = curve_endpoint_values.interface.new_socket(name = "Start Size", in_out='INPUT', socket_type = 'NodeSocketInt')
			start_size_socket.subtype = 'NONE'
			start_size_socket.default_value = 1
			start_size_socket.min_value = 0
			start_size_socket.max_value = 2147483647
			start_size_socket.attribute_domain = 'POINT'

			#Socket Start Value
			start_value_socket = curve_endpoint_values.interface.new_socket(name = "Start Value", in_out='INPUT', socket_type = 'NodeSocketInt')
			start_value_socket.subtype = 'NONE'
			start_value_socket.default_value = 1
			start_value_socket.min_value = -2147483647
			start_value_socket.max_value = 2147483647
			start_value_socket.attribute_domain = 'POINT'

			#Socket Other Value
			other_value_socket = curve_endpoint_values.interface.new_socket(name = "Other Value", in_out='INPUT', socket_type = 'NodeSocketInt')
			other_value_socket.subtype = 'NONE'
			other_value_socket.default_value = 0
			other_value_socket.min_value = -2147483647
			other_value_socket.max_value = 2147483647
			other_value_socket.attribute_domain = 'POINT'

			#Socket End Size
			end_size_socket = curve_endpoint_values.interface.new_socket(name = "End Size", in_out='INPUT', socket_type = 'NodeSocketInt')
			end_size_socket.subtype = 'NONE'
			end_size_socket.default_value = 1
			end_size_socket.min_value = 0
			end_size_socket.max_value = 2147483647
			end_size_socket.attribute_domain = 'POINT'

			#Socket End Value
			end_value_socket = curve_endpoint_values.interface.new_socket(name = "End Value", in_out='INPUT', socket_type = 'NodeSocketInt')
			end_value_socket.subtype = 'NONE'
			end_value_socket.default_value = -1
			end_value_socket.min_value = -2147483648
			end_value_socket.max_value = 2147483647
			end_value_socket.attribute_domain = 'POINT'


			#initialize curve_endpoint_values nodes
			#node Group Output
			group_output_43 = curve_endpoint_values.nodes.new("NodeGroupOutput")
			group_output_43.name = "Group Output"
			group_output_43.is_active_output = True

			#node Group Input
			group_input_43 = curve_endpoint_values.nodes.new("NodeGroupInput")
			group_input_43.name = "Group Input"

			#node Endpoint Selection
			endpoint_selection = curve_endpoint_values.nodes.new("GeometryNodeCurveEndpointSelection")
			endpoint_selection.name = "Endpoint Selection"
			#End Size
			endpoint_selection.inputs[1].default_value = 0

			#node Switch
			switch_7 = curve_endpoint_values.nodes.new("GeometryNodeSwitch")
			switch_7.name = "Switch"
			switch_7.input_type = 'INT'

			#node Switch.001
			switch_001_3 = curve_endpoint_values.nodes.new("GeometryNodeSwitch")
			switch_001_3.name = "Switch.001"
			switch_001_3.input_type = 'INT'

			#node Endpoint Selection.001
			endpoint_selection_001 = curve_endpoint_values.nodes.new("GeometryNodeCurveEndpointSelection")
			endpoint_selection_001.name = "Endpoint Selection.001"
			#Start Size
			endpoint_selection_001.inputs[0].default_value = 0




			#Set locations
			group_output_43.location = (360.49853515625, 0.0)
			group_input_43.location = (-788.796142578125, -16.119346618652344)
			endpoint_selection.location = (-240.0, 60.0)
			switch_7.location = (0.0, 40.0)
			switch_001_3.location = (0.0, -120.0)
			endpoint_selection_001.location = (-206.1257781982422, -162.97543334960938)

			#Set dimensions
			group_output_43.width, group_output_43.height = 140.0, 100.0
			group_input_43.width, group_input_43.height = 140.0, 100.0
			endpoint_selection.width, endpoint_selection.height = 140.0, 100.0
			switch_7.width, switch_7.height = 140.0, 100.0
			switch_001_3.width, switch_001_3.height = 140.0, 100.0
			endpoint_selection_001.width, endpoint_selection_001.height = 140.0, 100.0

			#initialize curve_endpoint_values links
			#endpoint_selection.Selection -> switch_7.Switch
			curve_endpoint_values.links.new(endpoint_selection.outputs[0], switch_7.inputs[0])
			#group_input_43.Other Value -> switch_7.False
			curve_endpoint_values.links.new(group_input_43.outputs[2], switch_7.inputs[1])
			#group_input_43.Start Value -> switch_7.True
			curve_endpoint_values.links.new(group_input_43.outputs[1], switch_7.inputs[2])
			#endpoint_selection_001.Selection -> switch_001_3.Switch
			curve_endpoint_values.links.new(endpoint_selection_001.outputs[0], switch_001_3.inputs[0])
			#switch_7.Output -> switch_001_3.False
			curve_endpoint_values.links.new(switch_7.outputs[0], switch_001_3.inputs[1])
			#switch_001_3.Output -> group_output_43.Value
			curve_endpoint_values.links.new(switch_001_3.outputs[0], group_output_43.inputs[0])
			#group_input_43.End Value -> switch_001_3.True
			curve_endpoint_values.links.new(group_input_43.outputs[4], switch_001_3.inputs[2])
			#group_input_43.Start Size -> endpoint_selection.Start Size
			curve_endpoint_values.links.new(group_input_43.outputs[0], endpoint_selection.inputs[0])
			#group_input_43.End Size -> endpoint_selection_001.End Size
			curve_endpoint_values.links.new(group_input_43.outputs[3], endpoint_selection_001.inputs[1])
			return curve_endpoint_values

		curve_endpoint_values = curve_endpoint_values_node_group()

		#initialize unit_convert node group
		def unit_convert_node_group():
			unit_convert = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Unit Convert")

			unit_convert.color_tag = 'CONVERTER'
			unit_convert.description = ""


			#unit_convert interface
			#Socket World
			world_socket = unit_convert.interface.new_socket(name = "World", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
			world_socket.subtype = 'NONE'
			world_socket.default_value = 0.0
			world_socket.min_value = -3.4028234663852886e+38
			world_socket.max_value = 3.4028234663852886e+38
			world_socket.attribute_domain = 'POINT'
			world_socket.description = "The value that has been scaled appropriately for the world space"

			#Socket Distance Type
			distance_type_socket = unit_convert.interface.new_socket(name = "Distance Type", in_out='INPUT', socket_type = 'NodeSocketMenu')
			distance_type_socket.attribute_domain = 'POINT'
			distance_type_socket.description = "What unit to scale the value to"

			#Socket From
			from_socket = unit_convert.interface.new_socket(name = "From", in_out='INPUT', socket_type = 'NodeSocketFloat')
			from_socket.subtype = 'NONE'
			from_socket.default_value = 3.0
			from_socket.min_value = -10000.0
			from_socket.max_value = 10000.0
			from_socket.attribute_domain = 'POINT'
			from_socket.description = "A value which will be scaled appropriately for the world"


			#initialize unit_convert nodes
			#node Group Output
			group_output_44 = unit_convert.nodes.new("NodeGroupOutput")
			group_output_44.name = "Group Output"
			group_output_44.is_active_output = True

			#node Group Input
			group_input_44 = unit_convert.nodes.new("NodeGroupInput")
			group_input_44.name = "Group Input"

			#node Math
			math_11 = unit_convert.nodes.new("ShaderNodeMath")
			math_11.name = "Math"
			math_11.operation = 'MULTIPLY'
			math_11.use_clamp = False

			#node Math.001
			math_001_3 = unit_convert.nodes.new("ShaderNodeMath")
			math_001_3.name = "Math.001"
			math_001_3.operation = 'MULTIPLY'
			math_001_3.use_clamp = False
			#Value_001
			math_001_3.inputs[1].default_value = 10.0

			#node Group
			group_15 = unit_convert.nodes.new("GeometryNodeGroup")
			group_15.name = "Group"
			group_15.node_tree = _mn_world_scale

			#node Menu Switch
			menu_switch_2 = unit_convert.nodes.new("GeometryNodeMenuSwitch")
			menu_switch_2.name = "Menu Switch"
			menu_switch_2.active_index = 2
			menu_switch_2.data_type = 'FLOAT'
			menu_switch_2.enum_items.clear()
			menu_switch_2.enum_items.new("Angstrom")
			menu_switch_2.enum_items[0].description = ""
			menu_switch_2.enum_items.new("Nanometre")
			menu_switch_2.enum_items[1].description = ""
			menu_switch_2.enum_items.new("Micrometre")
			menu_switch_2.enum_items[2].description = ""

			#node Math.002
			math_002_1 = unit_convert.nodes.new("ShaderNodeMath")
			math_002_1.name = "Math.002"
			math_002_1.operation = 'MULTIPLY'
			math_002_1.use_clamp = False
			#Value_001
			math_002_1.inputs[1].default_value = 1000.0




			#Set locations
			group_output_44.location = (280.0, 0.0)
			group_input_44.location = (-240.0, 0.0)
			math_11.location = (-60.0, 0.0)
			math_001_3.location = (-60.0, -160.0)
			group_15.location = (-300.0, -100.0)
			menu_switch_2.location = (120.0, 0.0)
			math_002_1.location = (-60.0, -320.0)

			#Set dimensions
			group_output_44.width, group_output_44.height = 140.0, 100.0
			group_input_44.width, group_input_44.height = 140.0, 100.0
			math_11.width, math_11.height = 140.0, 100.0
			math_001_3.width, math_001_3.height = 140.0, 100.0
			group_15.width, group_15.height = 197.58424377441406, 100.0
			menu_switch_2.width, menu_switch_2.height = 140.0, 100.0
			math_002_1.width, math_002_1.height = 140.0, 100.0

			#initialize unit_convert links
			#group_input_44.From -> math_11.Value
			unit_convert.links.new(group_input_44.outputs[1], math_11.inputs[0])
			#group_15.world_scale -> math_11.Value
			unit_convert.links.new(group_15.outputs[0], math_11.inputs[1])
			#math_11.Value -> math_001_3.Value
			unit_convert.links.new(math_11.outputs[0], math_001_3.inputs[0])
			#math_11.Value -> menu_switch_2.Angstrom
			unit_convert.links.new(math_11.outputs[0], menu_switch_2.inputs[1])
			#math_001_3.Value -> menu_switch_2.Nanometre
			unit_convert.links.new(math_001_3.outputs[0], menu_switch_2.inputs[2])
			#menu_switch_2.Output -> group_output_44.World
			unit_convert.links.new(menu_switch_2.outputs[0], group_output_44.inputs[0])
			#group_input_44.Distance Type -> menu_switch_2.Menu
			unit_convert.links.new(group_input_44.outputs[0], menu_switch_2.inputs[0])
			#math_001_3.Value -> math_002_1.Value
			unit_convert.links.new(math_001_3.outputs[0], math_002_1.inputs[0])
			#math_002_1.Value -> menu_switch_2.Micrometre
			unit_convert.links.new(math_002_1.outputs[0], menu_switch_2.inputs[3])
			return unit_convert

		unit_convert = unit_convert_node_group()

		#initialize angstrom_to_world node group
		def angstrom_to_world_node_group():
			angstrom_to_world = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Angstrom to World")

			angstrom_to_world.color_tag = 'CONVERTER'
			angstrom_to_world.description = ""


			#angstrom_to_world interface
			#Socket World
			world_socket_1 = angstrom_to_world.interface.new_socket(name = "World", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
			world_socket_1.subtype = 'NONE'
			world_socket_1.default_value = 0.0
			world_socket_1.min_value = -3.4028234663852886e+38
			world_socket_1.max_value = 3.4028234663852886e+38
			world_socket_1.attribute_domain = 'POINT'

			#Socket Angstrom
			angstrom_socket_1 = angstrom_to_world.interface.new_socket(name = "Angstrom", in_out='INPUT', socket_type = 'NodeSocketFloat')
			angstrom_socket_1.subtype = 'NONE'
			angstrom_socket_1.default_value = 3.0
			angstrom_socket_1.min_value = -10000.0
			angstrom_socket_1.max_value = 10000.0
			angstrom_socket_1.attribute_domain = 'POINT'


			#initialize angstrom_to_world nodes
			#node Group Output
			group_output_45 = angstrom_to_world.nodes.new("NodeGroupOutput")
			group_output_45.name = "Group Output"
			group_output_45.is_active_output = True

			#node Group Input
			group_input_45 = angstrom_to_world.nodes.new("NodeGroupInput")
			group_input_45.name = "Group Input"

			#node Group.136
			group_136 = angstrom_to_world.nodes.new("GeometryNodeGroup")
			group_136.name = "Group.136"
			group_136.node_tree = unit_convert
			#Socket_1
			group_136.inputs[0].default_value = 'Angstrom'




			#Set locations
			group_output_45.location = (196.83529663085938, 0.0)
			group_input_45.location = (-200.0, 0.0)
			group_136.location = (0.0, 0.0)

			#Set dimensions
			group_output_45.width, group_output_45.height = 140.0, 100.0
			group_input_45.width, group_input_45.height = 140.0, 100.0
			group_136.width, group_136.height = 146.83529663085938, 100.0

			#initialize angstrom_to_world links
			#group_136.World -> group_output_45.World
			angstrom_to_world.links.new(group_136.outputs[0], group_output_45.inputs[0])
			#group_input_45.Angstrom -> group_136.From
			angstrom_to_world.links.new(group_input_45.outputs[0], group_136.inputs[1])
			return angstrom_to_world

		angstrom_to_world = angstrom_to_world_node_group()

		#initialize vector_in_angstroms node group
		def vector_in_angstroms_node_group():
			vector_in_angstroms = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Vector in Angstroms")

			vector_in_angstroms.color_tag = 'CONVERTER'
			vector_in_angstroms.description = ""


			#vector_in_angstroms interface
			#Socket Vector
			vector_socket_2 = vector_in_angstroms.interface.new_socket(name = "Vector", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			vector_socket_2.subtype = 'NONE'
			vector_socket_2.default_value = (0.0, 0.0, 0.0)
			vector_socket_2.min_value = -3.4028234663852886e+38
			vector_socket_2.max_value = 3.4028234663852886e+38
			vector_socket_2.attribute_domain = 'POINT'
			vector_socket_2.description = "Vector that has been scaled by the number of input angstroms, optionally normalizing the vector first"

			#Socket Vector
			vector_socket_3 = vector_in_angstroms.interface.new_socket(name = "Vector", in_out='INPUT', socket_type = 'NodeSocketVector')
			vector_socket_3.subtype = 'NONE'
			vector_socket_3.default_value = (0.0, 0.0, 0.0)
			vector_socket_3.min_value = -10000.0
			vector_socket_3.max_value = 10000.0
			vector_socket_3.attribute_domain = 'POINT'

			#Socket Normalize
			normalize_socket = vector_in_angstroms.interface.new_socket(name = "Normalize", in_out='INPUT', socket_type = 'NodeSocketBool')
			normalize_socket.attribute_domain = 'POINT'
			normalize_socket.description = "Normalize the vector before first scaling to angstroms"

			#Socket Angstrom
			angstrom_socket_2 = vector_in_angstroms.interface.new_socket(name = "Angstrom", in_out='INPUT', socket_type = 'NodeSocketFloat')
			angstrom_socket_2.subtype = 'NONE'
			angstrom_socket_2.default_value = 2.5
			angstrom_socket_2.min_value = -10000.0
			angstrom_socket_2.max_value = 10000.0
			angstrom_socket_2.attribute_domain = 'POINT'


			#initialize vector_in_angstroms nodes
			#node Group Output
			group_output_46 = vector_in_angstroms.nodes.new("NodeGroupOutput")
			group_output_46.name = "Group Output"
			group_output_46.is_active_output = True

			#node Group Input
			group_input_46 = vector_in_angstroms.nodes.new("NodeGroupInput")
			group_input_46.name = "Group Input"

			#node Vector Math
			vector_math_2 = vector_in_angstroms.nodes.new("ShaderNodeVectorMath")
			vector_math_2.name = "Vector Math"
			vector_math_2.operation = 'SCALE'

			#node Group.004
			group_004_3 = vector_in_angstroms.nodes.new("GeometryNodeGroup")
			group_004_3.name = "Group.004"
			group_004_3.node_tree = angstrom_to_world

			#node Vector Math.001
			vector_math_001_2 = vector_in_angstroms.nodes.new("ShaderNodeVectorMath")
			vector_math_001_2.name = "Vector Math.001"
			vector_math_001_2.operation = 'NORMALIZE'

			#node Switch
			switch_8 = vector_in_angstroms.nodes.new("GeometryNodeSwitch")
			switch_8.name = "Switch"
			switch_8.input_type = 'VECTOR'




			#Set locations
			group_output_46.location = (395.25921630859375, 0.0)
			group_input_46.location = (-367.75994873046875, 45.195247650146484)
			vector_math_2.location = (205.25921630859375, 70.0)
			group_004_3.location = (205.25921630859375, -70.0)
			vector_math_001_2.location = (-180.0, -20.0)
			switch_8.location = (20.0, 80.0)

			#Set dimensions
			group_output_46.width, group_output_46.height = 140.0, 100.0
			group_input_46.width, group_input_46.height = 140.0, 100.0
			vector_math_2.width, vector_math_2.height = 140.0, 100.0
			group_004_3.width, group_004_3.height = 140.0, 100.0
			vector_math_001_2.width, vector_math_001_2.height = 140.0, 100.0
			switch_8.width, switch_8.height = 140.0, 100.0

			#initialize vector_in_angstroms links
			#group_004_3.World -> vector_math_2.Scale
			vector_in_angstroms.links.new(group_004_3.outputs[0], vector_math_2.inputs[3])
			#vector_math_2.Vector -> group_output_46.Vector
			vector_in_angstroms.links.new(vector_math_2.outputs[0], group_output_46.inputs[0])
			#group_input_46.Angstrom -> group_004_3.Angstrom
			vector_in_angstroms.links.new(group_input_46.outputs[2], group_004_3.inputs[0])
			#group_input_46.Vector -> vector_math_001_2.Vector
			vector_in_angstroms.links.new(group_input_46.outputs[0], vector_math_001_2.inputs[0])
			#vector_math_001_2.Vector -> switch_8.True
			vector_in_angstroms.links.new(vector_math_001_2.outputs[0], switch_8.inputs[2])
			#group_input_46.Vector -> switch_8.False
			vector_in_angstroms.links.new(group_input_46.outputs[0], switch_8.inputs[1])
			#switch_8.Output -> vector_math_2.Vector
			vector_in_angstroms.links.new(switch_8.outputs[0], vector_math_2.inputs[0])
			#group_input_46.Normalize -> switch_8.Switch
			vector_in_angstroms.links.new(group_input_46.outputs[1], switch_8.inputs[0])
			return vector_in_angstroms

		vector_in_angstroms = vector_in_angstroms_node_group()

		#initialize tmp_ss_attributes node group
		def tmp_ss_attributes_node_group():
			tmp_ss_attributes = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "tmp_ss_attributes")

			tmp_ss_attributes.color_tag = 'INPUT'
			tmp_ss_attributes.description = ""


			#tmp_ss_attributes interface
			#Socket tmp_ss_is_first
			tmp_ss_is_first_socket = tmp_ss_attributes.interface.new_socket(name = "tmp_ss_is_first", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			tmp_ss_is_first_socket.attribute_domain = 'POINT'

			#Socket tmp_ss_is_last
			tmp_ss_is_last_socket = tmp_ss_attributes.interface.new_socket(name = "tmp_ss_is_last", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			tmp_ss_is_last_socket.attribute_domain = 'POINT'

			#Socket tmp_ss_size
			tmp_ss_size_socket = tmp_ss_attributes.interface.new_socket(name = "tmp_ss_size", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			tmp_ss_size_socket.subtype = 'NONE'
			tmp_ss_size_socket.default_value = 0
			tmp_ss_size_socket.min_value = -2147483648
			tmp_ss_size_socket.max_value = 2147483647
			tmp_ss_size_socket.attribute_domain = 'POINT'

			#Socket tmp_idx
			tmp_idx_socket = tmp_ss_attributes.interface.new_socket(name = "tmp_idx", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			tmp_idx_socket.subtype = 'NONE'
			tmp_idx_socket.default_value = 0
			tmp_idx_socket.min_value = -2147483648
			tmp_idx_socket.max_value = 2147483647
			tmp_idx_socket.attribute_domain = 'POINT'

			#Socket tmp_idx_curve
			tmp_idx_curve_socket = tmp_ss_attributes.interface.new_socket(name = "tmp_idx_curve", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			tmp_idx_curve_socket.subtype = 'NONE'
			tmp_idx_curve_socket.default_value = 0
			tmp_idx_curve_socket.min_value = -2147483648
			tmp_idx_curve_socket.max_value = 2147483647
			tmp_idx_curve_socket.attribute_domain = 'POINT'

			#Socket tmp_curve_normal
			tmp_curve_normal_socket = tmp_ss_attributes.interface.new_socket(name = "tmp_curve_normal", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			tmp_curve_normal_socket.subtype = 'NONE'
			tmp_curve_normal_socket.default_value = (0.0, 0.0, 0.0)
			tmp_curve_normal_socket.min_value = -3.4028234663852886e+38
			tmp_curve_normal_socket.max_value = 3.4028234663852886e+38
			tmp_curve_normal_socket.attribute_domain = 'POINT'

			#Socket tmp_curve_tangent
			tmp_curve_tangent_socket = tmp_ss_attributes.interface.new_socket(name = "tmp_curve_tangent", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			tmp_curve_tangent_socket.subtype = 'NONE'
			tmp_curve_tangent_socket.default_value = (0.0, 0.0, 0.0)
			tmp_curve_tangent_socket.min_value = -3.4028234663852886e+38
			tmp_curve_tangent_socket.max_value = 3.4028234663852886e+38
			tmp_curve_tangent_socket.attribute_domain = 'POINT'


			#initialize tmp_ss_attributes nodes
			#node Group Output
			group_output_47 = tmp_ss_attributes.nodes.new("NodeGroupOutput")
			group_output_47.name = "Group Output"
			group_output_47.is_active_output = True

			#node Group Input
			group_input_47 = tmp_ss_attributes.nodes.new("NodeGroupInput")
			group_input_47.name = "Group Input"

			#node Named Attribute.001
			named_attribute_001_2 = tmp_ss_attributes.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_001_2.name = "Named Attribute.001"
			named_attribute_001_2.data_type = 'BOOLEAN'
			#Name
			named_attribute_001_2.inputs[0].default_value = "tmp_ss_is_first"

			#node Named Attribute.002
			named_attribute_002_2 = tmp_ss_attributes.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_002_2.name = "Named Attribute.002"
			named_attribute_002_2.data_type = 'BOOLEAN'
			#Name
			named_attribute_002_2.inputs[0].default_value = "tmp_ss_is_last"

			#node Named Attribute.003
			named_attribute_003 = tmp_ss_attributes.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_003.name = "Named Attribute.003"
			named_attribute_003.data_type = 'INT'
			#Name
			named_attribute_003.inputs[0].default_value = "tmp_ss_size"

			#node Named Attribute.004
			named_attribute_004 = tmp_ss_attributes.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_004.name = "Named Attribute.004"
			named_attribute_004.data_type = 'INT'
			#Name
			named_attribute_004.inputs[0].default_value = "tmp_idx"

			#node Named Attribute.005
			named_attribute_005 = tmp_ss_attributes.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_005.name = "Named Attribute.005"
			named_attribute_005.data_type = 'INT'
			#Name
			named_attribute_005.inputs[0].default_value = "tmp_idx_curve"

			#node Named Attribute.006
			named_attribute_006 = tmp_ss_attributes.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_006.name = "Named Attribute.006"
			named_attribute_006.data_type = 'FLOAT_VECTOR'
			#Name
			named_attribute_006.inputs[0].default_value = "tmp_curve_normal"

			#node Named Attribute.007
			named_attribute_007 = tmp_ss_attributes.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_007.name = "Named Attribute.007"
			named_attribute_007.data_type = 'FLOAT_VECTOR'
			#Name
			named_attribute_007.inputs[0].default_value = "tmp_curve_tangent"




			#Set locations
			group_output_47.location = (603.9637451171875, 53.98777389526367)
			group_input_47.location = (-49.340919494628906, 57.35612869262695)
			named_attribute_001_2.location = (160.0, 120.0)
			named_attribute_002_2.location = (160.0, -20.0)
			named_attribute_003.location = (160.0, -160.0)
			named_attribute_004.location = (160.0, -300.0)
			named_attribute_005.location = (160.0, -440.0)
			named_attribute_006.location = (160.0, -580.0)
			named_attribute_007.location = (160.0, -720.0)

			#Set dimensions
			group_output_47.width, group_output_47.height = 140.0, 100.0
			group_input_47.width, group_input_47.height = 140.0, 100.0
			named_attribute_001_2.width, named_attribute_001_2.height = 174.255126953125, 100.0
			named_attribute_002_2.width, named_attribute_002_2.height = 174.2551727294922, 100.0
			named_attribute_003.width, named_attribute_003.height = 174.2551727294922, 100.0
			named_attribute_004.width, named_attribute_004.height = 174.2551727294922, 100.0
			named_attribute_005.width, named_attribute_005.height = 174.2551727294922, 100.0
			named_attribute_006.width, named_attribute_006.height = 174.2551727294922, 100.0
			named_attribute_007.width, named_attribute_007.height = 174.2551727294922, 100.0

			#initialize tmp_ss_attributes links
			#named_attribute_001_2.Attribute -> group_output_47.tmp_ss_is_first
			tmp_ss_attributes.links.new(named_attribute_001_2.outputs[0], group_output_47.inputs[0])
			#named_attribute_002_2.Attribute -> group_output_47.tmp_ss_is_last
			tmp_ss_attributes.links.new(named_attribute_002_2.outputs[0], group_output_47.inputs[1])
			#named_attribute_003.Attribute -> group_output_47.tmp_ss_size
			tmp_ss_attributes.links.new(named_attribute_003.outputs[0], group_output_47.inputs[2])
			#named_attribute_004.Attribute -> group_output_47.tmp_idx
			tmp_ss_attributes.links.new(named_attribute_004.outputs[0], group_output_47.inputs[3])
			#named_attribute_005.Attribute -> group_output_47.tmp_idx_curve
			tmp_ss_attributes.links.new(named_attribute_005.outputs[0], group_output_47.inputs[4])
			#named_attribute_006.Attribute -> group_output_47.tmp_curve_normal
			tmp_ss_attributes.links.new(named_attribute_006.outputs[0], group_output_47.inputs[5])
			#named_attribute_007.Attribute -> group_output_47.tmp_curve_tangent
			tmp_ss_attributes.links.new(named_attribute_007.outputs[0], group_output_47.inputs[6])
			return tmp_ss_attributes

		tmp_ss_attributes = tmp_ss_attributes_node_group()

		#initialize _sample_from_ca_curve node group
		def _sample_from_ca_curve_node_group():
			_sample_from_ca_curve = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".Sample from CA curve")

			_sample_from_ca_curve.color_tag = 'GEOMETRY'
			_sample_from_ca_curve.description = ""


			#_sample_from_ca_curve interface
			#Socket Position
			position_socket_4 = _sample_from_ca_curve.interface.new_socket(name = "Position", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			position_socket_4.subtype = 'NONE'
			position_socket_4.default_value = (0.0, 0.0, 0.0)
			position_socket_4.min_value = -3.4028234663852886e+38
			position_socket_4.max_value = 3.4028234663852886e+38
			position_socket_4.attribute_domain = 'POINT'

			#Socket Tangent
			tangent_socket_1 = _sample_from_ca_curve.interface.new_socket(name = "Tangent", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			tangent_socket_1.subtype = 'NONE'
			tangent_socket_1.default_value = (0.0, 0.0, 0.0)
			tangent_socket_1.min_value = -3.4028234663852886e+38
			tangent_socket_1.max_value = 3.4028234663852886e+38
			tangent_socket_1.attribute_domain = 'POINT'

			#Socket Normal
			normal_socket_2 = _sample_from_ca_curve.interface.new_socket(name = "Normal", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			normal_socket_2.subtype = 'NONE'
			normal_socket_2.default_value = (0.0, 0.0, 0.0)
			normal_socket_2.min_value = -3.4028234663852886e+38
			normal_socket_2.max_value = 3.4028234663852886e+38
			normal_socket_2.attribute_domain = 'POINT'

			#Socket CA Curve
			ca_curve_socket = _sample_from_ca_curve.interface.new_socket(name = "CA Curve", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			ca_curve_socket.attribute_domain = 'POINT'

			#Socket Offset
			offset_socket_6 = _sample_from_ca_curve.interface.new_socket(name = "Offset", in_out='INPUT', socket_type = 'NodeSocketFloat')
			offset_socket_6.subtype = 'NONE'
			offset_socket_6.default_value = 0.0
			offset_socket_6.min_value = -10000.0
			offset_socket_6.max_value = 10000.0
			offset_socket_6.attribute_domain = 'POINT'


			#initialize _sample_from_ca_curve nodes
			#node Group Output
			group_output_48 = _sample_from_ca_curve.nodes.new("NodeGroupOutput")
			group_output_48.name = "Group Output"
			group_output_48.is_active_output = True

			#node Group Input
			group_input_48 = _sample_from_ca_curve.nodes.new("NodeGroupInput")
			group_input_48.name = "Group Input"

			#node Sample Curve
			sample_curve_1 = _sample_from_ca_curve.nodes.new("GeometryNodeSampleCurve")
			sample_curve_1.name = "Sample Curve"
			sample_curve_1.data_type = 'FLOAT'
			sample_curve_1.mode = 'FACTOR'
			sample_curve_1.use_all_curves = False
			#Value
			sample_curve_1.inputs[1].default_value = 0.0

			#node Group.001
			group_001_9 = _sample_from_ca_curve.nodes.new("GeometryNodeGroup")
			group_001_9.name = "Group.001"
			group_001_9.node_tree = offset_point_along_curve

			#node Group.002
			group_002_7 = _sample_from_ca_curve.nodes.new("GeometryNodeGroup")
			group_002_7.name = "Group.002"
			group_002_7.node_tree = tmp_ss_attributes
			group_002_7.outputs[0].hide = True
			group_002_7.outputs[1].hide = True
			group_002_7.outputs[2].hide = True

			#node Capture Attribute.002
			capture_attribute_002_1 = _sample_from_ca_curve.nodes.new("GeometryNodeCaptureAttribute")
			capture_attribute_002_1.name = "Capture Attribute.002"
			capture_attribute_002_1.active_index = 1
			capture_attribute_002_1.capture_items.clear()
			capture_attribute_002_1.capture_items.new('FLOAT', "Position")
			capture_attribute_002_1.capture_items["Position"].data_type = 'FLOAT_VECTOR'
			capture_attribute_002_1.capture_items.new('FLOAT', "Tangent")
			capture_attribute_002_1.capture_items["Tangent"].data_type = 'FLOAT_VECTOR'
			capture_attribute_002_1.capture_items.new('FLOAT', "Normal")
			capture_attribute_002_1.capture_items["Normal"].data_type = 'FLOAT_VECTOR'
			capture_attribute_002_1.domain = 'POINT'

			#node Reroute.003
			reroute_003_4 = _sample_from_ca_curve.nodes.new("NodeReroute")
			reroute_003_4.name = "Reroute.003"
			#node Sample Index
			sample_index = _sample_from_ca_curve.nodes.new("GeometryNodeSampleIndex")
			sample_index.name = "Sample Index"
			sample_index.clamp = False
			sample_index.data_type = 'FLOAT_VECTOR'
			sample_index.domain = 'POINT'

			#node Sample Index.001
			sample_index_001_1 = _sample_from_ca_curve.nodes.new("GeometryNodeSampleIndex")
			sample_index_001_1.name = "Sample Index.001"
			sample_index_001_1.clamp = False
			sample_index_001_1.data_type = 'FLOAT_VECTOR'
			sample_index_001_1.domain = 'POINT'

			#node Reroute.004
			reroute_004_2 = _sample_from_ca_curve.nodes.new("NodeReroute")
			reroute_004_2.name = "Reroute.004"
			#node Sample Index.002
			sample_index_002 = _sample_from_ca_curve.nodes.new("GeometryNodeSampleIndex")
			sample_index_002.name = "Sample Index.002"
			sample_index_002.clamp = False
			sample_index_002.data_type = 'FLOAT_VECTOR'
			sample_index_002.domain = 'POINT'




			#Set locations
			group_output_48.location = (650.0, 0.0)
			group_input_48.location = (-660.0, 0.0)
			sample_curve_1.location = (-80.0, 40.0)
			group_001_9.location = (-295.7841796875, -88.2349853515625)
			group_002_7.location = (-480.2359313964844, -36.91614532470703)
			capture_attribute_002_1.location = (100.0, 83.329345703125)
			reroute_003_4.location = (-200.0, 23.329345703125)
			sample_index.location = (458.0, 119.329345703125)
			sample_index_001_1.location = (460.0, -280.0)
			reroute_004_2.location = (153.90460205078125, -119.3294677734375)
			sample_index_002.location = (460.0, -80.0)

			#Set dimensions
			group_output_48.width, group_output_48.height = 140.0, 100.0
			group_input_48.width, group_input_48.height = 140.0, 100.0
			sample_curve_1.width, sample_curve_1.height = 140.0, 100.0
			group_001_9.width, group_001_9.height = 140.0, 100.0
			group_002_7.width, group_002_7.height = 140.0, 100.0
			capture_attribute_002_1.width, capture_attribute_002_1.height = 140.0, 100.0
			reroute_003_4.width, reroute_003_4.height = 16.0, 100.0
			sample_index.width, sample_index.height = 140.0, 100.0
			sample_index_001_1.width, sample_index_001_1.height = 140.0, 100.0
			reroute_004_2.width, reroute_004_2.height = 16.0, 100.0
			sample_index_002.width, sample_index_002.height = 140.0, 100.0

			#initialize _sample_from_ca_curve links
			#group_001_9.Factor -> sample_curve_1.Factor
			_sample_from_ca_curve.links.new(group_001_9.outputs[0], sample_curve_1.inputs[2])
			#reroute_004_2.Output -> sample_index_001_1.Index
			_sample_from_ca_curve.links.new(reroute_004_2.outputs[0], sample_index_001_1.inputs[2])
			#reroute_004_2.Output -> sample_index.Index
			_sample_from_ca_curve.links.new(reroute_004_2.outputs[0], sample_index.inputs[2])
			#reroute_003_4.Output -> sample_curve_1.Curves
			_sample_from_ca_curve.links.new(reroute_003_4.outputs[0], sample_curve_1.inputs[0])
			#sample_curve_1.Position -> capture_attribute_002_1.Position
			_sample_from_ca_curve.links.new(sample_curve_1.outputs[1], capture_attribute_002_1.inputs[1])
			#capture_attribute_002_1.Geometry -> sample_index_001_1.Geometry
			_sample_from_ca_curve.links.new(capture_attribute_002_1.outputs[0], sample_index_001_1.inputs[0])
			#capture_attribute_002_1.Geometry -> sample_index.Geometry
			_sample_from_ca_curve.links.new(capture_attribute_002_1.outputs[0], sample_index.inputs[0])
			#reroute_003_4.Output -> capture_attribute_002_1.Geometry
			_sample_from_ca_curve.links.new(reroute_003_4.outputs[0], capture_attribute_002_1.inputs[0])
			#capture_attribute_002_1.Normal -> sample_index_001_1.Value
			_sample_from_ca_curve.links.new(capture_attribute_002_1.outputs[3], sample_index_001_1.inputs[1])
			#sample_curve_1.Normal -> capture_attribute_002_1.Normal
			_sample_from_ca_curve.links.new(sample_curve_1.outputs[3], capture_attribute_002_1.inputs[3])
			#group_002_7.tmp_idx -> reroute_004_2.Input
			_sample_from_ca_curve.links.new(group_002_7.outputs[3], reroute_004_2.inputs[0])
			#group_002_7.tmp_idx -> group_001_9.Point Index
			_sample_from_ca_curve.links.new(group_002_7.outputs[3], group_001_9.inputs[0])
			#group_002_7.tmp_idx_curve -> sample_curve_1.Curve Index
			_sample_from_ca_curve.links.new(group_002_7.outputs[4], sample_curve_1.inputs[4])
			#capture_attribute_002_1.Position -> sample_index.Value
			_sample_from_ca_curve.links.new(capture_attribute_002_1.outputs[1], sample_index.inputs[1])
			#group_input_48.CA Curve -> reroute_003_4.Input
			_sample_from_ca_curve.links.new(group_input_48.outputs[0], reroute_003_4.inputs[0])
			#sample_index.Value -> group_output_48.Position
			_sample_from_ca_curve.links.new(sample_index.outputs[0], group_output_48.inputs[0])
			#sample_index_001_1.Value -> group_output_48.Normal
			_sample_from_ca_curve.links.new(sample_index_001_1.outputs[0], group_output_48.inputs[2])
			#group_input_48.Offset -> group_001_9.Value
			_sample_from_ca_curve.links.new(group_input_48.outputs[1], group_001_9.inputs[1])
			#reroute_004_2.Output -> sample_index_002.Index
			_sample_from_ca_curve.links.new(reroute_004_2.outputs[0], sample_index_002.inputs[2])
			#capture_attribute_002_1.Geometry -> sample_index_002.Geometry
			_sample_from_ca_curve.links.new(capture_attribute_002_1.outputs[0], sample_index_002.inputs[0])
			#sample_curve_1.Tangent -> capture_attribute_002_1.Tangent
			_sample_from_ca_curve.links.new(sample_curve_1.outputs[2], capture_attribute_002_1.inputs[2])
			#sample_index_002.Value -> group_output_48.Tangent
			_sample_from_ca_curve.links.new(sample_index_002.outputs[0], group_output_48.inputs[1])
			#capture_attribute_002_1.Tangent -> sample_index_002.Value
			_sample_from_ca_curve.links.new(capture_attribute_002_1.outputs[2], sample_index_002.inputs[1])
			return _sample_from_ca_curve

		_sample_from_ca_curve = _sample_from_ca_curve_node_group()

		#initialize _fix_loop_alignment_into_ah node group
		def _fix_loop_alignment_into_ah_node_group():
			_fix_loop_alignment_into_ah = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".Fix Loop Alignment into AH")

			_fix_loop_alignment_into_ah.color_tag = 'NONE'
			_fix_loop_alignment_into_ah.description = ""


			#_fix_loop_alignment_into_ah interface
			#Socket Geometry
			geometry_socket_6 = _fix_loop_alignment_into_ah.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			geometry_socket_6.attribute_domain = 'POINT'

			#Socket Curve
			curve_socket_3 = _fix_loop_alignment_into_ah.interface.new_socket(name = "Curve", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			curve_socket_3.attribute_domain = 'POINT'

			#Socket Tangent
			tangent_socket_2 = _fix_loop_alignment_into_ah.interface.new_socket(name = "Tangent", in_out='INPUT', socket_type = 'NodeSocketVector')
			tangent_socket_2.subtype = 'NONE'
			tangent_socket_2.default_value = (0.0, 0.0, 0.0)
			tangent_socket_2.min_value = -3.4028234663852886e+38
			tangent_socket_2.max_value = 3.4028234663852886e+38
			tangent_socket_2.attribute_domain = 'POINT'
			tangent_socket_2.hide_value = True


			#initialize _fix_loop_alignment_into_ah nodes
			#node Group Output
			group_output_49 = _fix_loop_alignment_into_ah.nodes.new("NodeGroupOutput")
			group_output_49.name = "Group Output"
			group_output_49.is_active_output = True

			#node Group Input
			group_input_49 = _fix_loop_alignment_into_ah.nodes.new("NodeGroupInput")
			group_input_49.name = "Group Input"
			group_input_49.outputs[1].hide = True
			group_input_49.outputs[2].hide = True

			#node Subdivide Curve
			subdivide_curve = _fix_loop_alignment_into_ah.nodes.new("GeometryNodeSubdivideCurve")
			subdivide_curve.name = "Subdivide Curve"

			#node Switch.004
			switch_004 = _fix_loop_alignment_into_ah.nodes.new("GeometryNodeSwitch")
			switch_004.name = "Switch.004"
			switch_004.input_type = 'INT'
			#False
			switch_004.inputs[1].default_value = 0
			#True
			switch_004.inputs[2].default_value = 1

			#node Endpoint Selection.002
			endpoint_selection_002 = _fix_loop_alignment_into_ah.nodes.new("GeometryNodeCurveEndpointSelection")
			endpoint_selection_002.name = "Endpoint Selection.002"
			#Start Size
			endpoint_selection_002.inputs[0].default_value = 1
			#End Size
			endpoint_selection_002.inputs[1].default_value = 0

			#node Endpoint Selection.003
			endpoint_selection_003 = _fix_loop_alignment_into_ah.nodes.new("GeometryNodeCurveEndpointSelection")
			endpoint_selection_003.name = "Endpoint Selection.003"
			#Start Size
			endpoint_selection_003.inputs[0].default_value = 0
			#End Size
			endpoint_selection_003.inputs[1].default_value = 2

			#node Endpoint Selection.004
			endpoint_selection_004 = _fix_loop_alignment_into_ah.nodes.new("GeometryNodeCurveEndpointSelection")
			endpoint_selection_004.name = "Endpoint Selection.004"
			#Start Size
			endpoint_selection_004.inputs[0].default_value = 0
			#End Size
			endpoint_selection_004.inputs[1].default_value = 1

			#node Boolean Math.004
			boolean_math_004 = _fix_loop_alignment_into_ah.nodes.new("FunctionNodeBooleanMath")
			boolean_math_004.name = "Boolean Math.004"
			boolean_math_004.operation = 'NIMPLY'

			#node Boolean Math.008
			boolean_math_008 = _fix_loop_alignment_into_ah.nodes.new("FunctionNodeBooleanMath")
			boolean_math_008.name = "Boolean Math.008"
			boolean_math_008.operation = 'OR'

			#node Set Position
			set_position_2 = _fix_loop_alignment_into_ah.nodes.new("GeometryNodeSetPosition")
			set_position_2.name = "Set Position"

			#node Group.002
			group_002_8 = _fix_loop_alignment_into_ah.nodes.new("GeometryNodeGroup")
			group_002_8.name = "Group.002"
			group_002_8.node_tree = offset_vector
			#Socket_2
			group_002_8.inputs[0].default_value = 0

			#node Endpoint Selection.005
			endpoint_selection_005 = _fix_loop_alignment_into_ah.nodes.new("GeometryNodeCurveEndpointSelection")
			endpoint_selection_005.name = "Endpoint Selection.005"
			#Start Size
			endpoint_selection_005.inputs[0].default_value = 2
			#End Size
			endpoint_selection_005.inputs[1].default_value = 0

			#node Endpoint Selection.006
			endpoint_selection_006 = _fix_loop_alignment_into_ah.nodes.new("GeometryNodeCurveEndpointSelection")
			endpoint_selection_006.name = "Endpoint Selection.006"
			#Start Size
			endpoint_selection_006.inputs[0].default_value = 0
			#End Size
			endpoint_selection_006.inputs[1].default_value = 2

			#node Endpoint Selection.007
			endpoint_selection_007 = _fix_loop_alignment_into_ah.nodes.new("GeometryNodeCurveEndpointSelection")
			endpoint_selection_007.name = "Endpoint Selection.007"
			#Start Size
			endpoint_selection_007.inputs[0].default_value = 0
			#End Size
			endpoint_selection_007.inputs[1].default_value = 1

			#node Boolean Math.009
			boolean_math_009 = _fix_loop_alignment_into_ah.nodes.new("FunctionNodeBooleanMath")
			boolean_math_009.name = "Boolean Math.009"
			boolean_math_009.operation = 'NIMPLY'

			#node Boolean Math.010
			boolean_math_010 = _fix_loop_alignment_into_ah.nodes.new("FunctionNodeBooleanMath")
			boolean_math_010.name = "Boolean Math.010"
			boolean_math_010.operation = 'OR'

			#node Boolean Math.011
			boolean_math_011 = _fix_loop_alignment_into_ah.nodes.new("FunctionNodeBooleanMath")
			boolean_math_011.name = "Boolean Math.011"
			boolean_math_011.operation = 'NIMPLY'

			#node Endpoint Selection.008
			endpoint_selection_008 = _fix_loop_alignment_into_ah.nodes.new("GeometryNodeCurveEndpointSelection")
			endpoint_selection_008.name = "Endpoint Selection.008"
			#Start Size
			endpoint_selection_008.inputs[0].default_value = 1
			#End Size
			endpoint_selection_008.inputs[1].default_value = 0

			#node Group.008
			group_008 = _fix_loop_alignment_into_ah.nodes.new("GeometryNodeGroup")
			group_008.name = "Group.008"
			group_008.node_tree = vector_in_angstroms
			#Socket_4
			group_008.inputs[1].default_value = False

			#node Group.014
			group_014 = _fix_loop_alignment_into_ah.nodes.new("GeometryNodeGroup")
			group_014.name = "Group.014"
			group_014.node_tree = offset_vector
			#Socket_2
			group_014.inputs[0].default_value = 0

			#node Position
			position_2 = _fix_loop_alignment_into_ah.nodes.new("GeometryNodeInputPosition")
			position_2.name = "Position"

			#node Group.018
			group_018 = _fix_loop_alignment_into_ah.nodes.new("GeometryNodeGroup")
			group_018.name = "Group.018"
			group_018.node_tree = curve_endpoint_values
			#Socket_5
			group_018.inputs[0].default_value = 2
			#Socket_1
			group_018.inputs[1].default_value = -1
			#Socket_2
			group_018.inputs[2].default_value = 0
			#Socket_6
			group_018.inputs[3].default_value = 2
			#Socket_3
			group_018.inputs[4].default_value = 1

			#node Math
			math_12 = _fix_loop_alignment_into_ah.nodes.new("ShaderNodeMath")
			math_12.name = "Math"
			math_12.operation = 'MULTIPLY'
			math_12.use_clamp = False
			#Value_001
			math_12.inputs[1].default_value = -0.5

			#node Group Input.001
			group_input_001_5 = _fix_loop_alignment_into_ah.nodes.new("NodeGroupInput")
			group_input_001_5.name = "Group Input.001"
			group_input_001_5.outputs[0].hide = True
			group_input_001_5.outputs[2].hide = True

			#node Frame
			frame_2 = _fix_loop_alignment_into_ah.nodes.new("NodeFrame")
			frame_2.label = "Subdivide the first and last segments going into AH"
			frame_2.name = "Frame"
			frame_2.label_size = 20
			frame_2.shrink = True

			#node Capture Attribute
			capture_attribute_4 = _fix_loop_alignment_into_ah.nodes.new("GeometryNodeCaptureAttribute")
			capture_attribute_4.name = "Capture Attribute"
			capture_attribute_4.active_index = 0
			capture_attribute_4.capture_items.clear()
			capture_attribute_4.capture_items.new('FLOAT', "Value")
			capture_attribute_4.capture_items["Value"].data_type = 'INT'
			capture_attribute_4.domain = 'POINT'

			#node Reroute
			reroute_8 = _fix_loop_alignment_into_ah.nodes.new("NodeReroute")
			reroute_8.name = "Reroute"
			#node Frame.001
			frame_001 = _fix_loop_alignment_into_ah.nodes.new("NodeFrame")
			frame_001.label = "Selection for second point and second last point"
			frame_001.name = "Frame.001"
			frame_001.label_size = 20
			frame_001.shrink = True

			#node Set Position.001
			set_position_001 = _fix_loop_alignment_into_ah.nodes.new("GeometryNodeSetPosition")
			set_position_001.name = "Set Position.001"
			#Position
			set_position_001.inputs[2].default_value = (0.0, 0.0, 0.0)

			#node Endpoint Selection
			endpoint_selection_1 = _fix_loop_alignment_into_ah.nodes.new("GeometryNodeCurveEndpointSelection")
			endpoint_selection_1.name = "Endpoint Selection"
			#Start Size
			endpoint_selection_1.inputs[0].default_value = 1
			#End Size
			endpoint_selection_1.inputs[1].default_value = 1

			#node Group.009
			group_009 = _fix_loop_alignment_into_ah.nodes.new("GeometryNodeGroup")
			group_009.name = "Group.009"
			group_009.node_tree = vector_in_angstroms
			#Socket_4
			group_009.inputs[1].default_value = False

			#node Math.001
			math_001_4 = _fix_loop_alignment_into_ah.nodes.new("ShaderNodeMath")
			math_001_4.name = "Math.001"
			math_001_4.operation = 'MULTIPLY'
			math_001_4.use_clamp = False
			#Value_001
			math_001_4.inputs[1].default_value = 0.30000001192092896

			#node Group Input.002
			group_input_002_1 = _fix_loop_alignment_into_ah.nodes.new("NodeGroupInput")
			group_input_002_1.name = "Group Input.002"
			group_input_002_1.outputs[0].hide = True
			group_input_002_1.outputs[2].hide = True

			#node Frame.002
			frame_002_1 = _fix_loop_alignment_into_ah.nodes.new("NodeFrame")
			frame_002_1.label = "Move loop ends slightly inside of SS"
			frame_002_1.name = "Frame.002"
			frame_002_1.label_size = 20
			frame_002_1.shrink = True

			#node Capture Attribute.001
			capture_attribute_001_1 = _fix_loop_alignment_into_ah.nodes.new("GeometryNodeCaptureAttribute")
			capture_attribute_001_1.name = "Capture Attribute.001"
			capture_attribute_001_1.active_index = 0
			capture_attribute_001_1.capture_items.clear()
			capture_attribute_001_1.capture_items.new('FLOAT', "Selection")
			capture_attribute_001_1.capture_items["Selection"].data_type = 'BOOLEAN'
			capture_attribute_001_1.domain = 'POINT'

			#node Group.003
			group_003_3 = _fix_loop_alignment_into_ah.nodes.new("GeometryNodeGroup")
			group_003_3.name = "Group.003"
			group_003_3.node_tree = is_helix
			#Socket_1
			group_003_3.inputs[0].default_value = True
			#Socket_3
			group_003_3.inputs[1].default_value = False

			#node Boolean Math
			boolean_math_8 = _fix_loop_alignment_into_ah.nodes.new("FunctionNodeBooleanMath")
			boolean_math_8.name = "Boolean Math"
			boolean_math_8.operation = 'AND'

			#node Boolean Math.001
			boolean_math_001_5 = _fix_loop_alignment_into_ah.nodes.new("FunctionNodeBooleanMath")
			boolean_math_001_5.name = "Boolean Math.001"
			boolean_math_001_5.operation = 'AND'

			#node Group
			group_16 = _fix_loop_alignment_into_ah.nodes.new("GeometryNodeGroup")
			group_16.name = "Group"
			group_16.node_tree = expand_boolean
			#Socket_2
			group_16.inputs[1].default_value = 1



			#Set parents
			subdivide_curve.parent = frame_2
			switch_004.parent = frame_2
			endpoint_selection_002.parent = frame_2
			endpoint_selection_003.parent = frame_2
			endpoint_selection_004.parent = frame_2
			boolean_math_004.parent = frame_2
			boolean_math_008.parent = frame_2
			endpoint_selection_005.parent = frame_001
			endpoint_selection_006.parent = frame_001
			endpoint_selection_007.parent = frame_001
			boolean_math_009.parent = frame_001
			boolean_math_010.parent = frame_001
			boolean_math_011.parent = frame_001
			endpoint_selection_008.parent = frame_001
			set_position_001.parent = frame_002_1
			endpoint_selection_1.parent = frame_002_1
			group_009.parent = frame_002_1
			math_001_4.parent = frame_002_1
			group_input_002_1.parent = frame_002_1
			boolean_math_8.parent = frame_2
			boolean_math_001_5.parent = frame_001
			group_16.parent = frame_2

			#Set locations
			group_output_49.location = (1520.0, -100.0)
			group_input_49.location = (-1360.0, 280.0)
			subdivide_curve.location = (-380.0, -200.0)
			switch_004.location = (-380.0, -320.0)
			endpoint_selection_002.location = (-990.0, -540.0)
			endpoint_selection_003.location = (-1150.0, -400.0)
			endpoint_selection_004.location = (-1150.0, -520.0)
			boolean_math_004.location = (-990.0, -400.0)
			boolean_math_008.location = (-830.0, -400.0)
			set_position_2.location = (520.0, -120.0)
			group_002_8.location = (180.0, -340.0)
			endpoint_selection_005.location = (-219.6986083984375, 190.0)
			endpoint_selection_006.location = (-219.6986083984375, 430.0)
			endpoint_selection_007.location = (-219.6986083984375, 310.0)
			boolean_math_009.location = (-59.6986083984375, 430.0)
			boolean_math_010.location = (100.3013916015625, 330.0)
			boolean_math_011.location = (-59.6986083984375, 190.0)
			endpoint_selection_008.location = (-219.6986083984375, 70.0)
			group_008.location = (340.0, -340.0)
			group_014.location = (340.0, -180.0)
			position_2.location = (180.0, -180.0)
			group_018.location = (-354.9727478027344, -202.68789672851562)
			math_12.location = (180.0, -500.0)
			group_input_001_5.location = (20.0, -340.0)
			frame_2.location = (-190.0, 60.0)
			capture_attribute_4.location = (-166.6365509033203, -106.50935363769531)
			reroute_8.location = (100.0, -560.0)
			frame_001.location = (-70.0, 50.0)
			set_position_001.location = (960.0, -120.0)
			endpoint_selection_1.location = (740.0, -220.0)
			group_009.location = (960.0, -280.0)
			math_001_4.location = (960.0, -440.0)
			group_input_002_1.location = (740.0, -340.0)
			frame_002_1.location = (190.0, 20.0)
			capture_attribute_001_1.location = (-1160.0, 280.0)
			group_003_3.location = (-1356.5357666015625, 202.73043823242188)
			boolean_math_8.location = (-610.0, -340.0)
			boolean_math_001_5.location = (270.0, 330.0)
			group_16.location = (-830.0, -260.0)

			#Set dimensions
			group_output_49.width, group_output_49.height = 140.0, 100.0
			group_input_49.width, group_input_49.height = 140.0, 100.0
			subdivide_curve.width, subdivide_curve.height = 140.0, 100.0
			switch_004.width, switch_004.height = 140.0, 100.0
			endpoint_selection_002.width, endpoint_selection_002.height = 140.0, 100.0
			endpoint_selection_003.width, endpoint_selection_003.height = 140.0, 100.0
			endpoint_selection_004.width, endpoint_selection_004.height = 140.0, 100.0
			boolean_math_004.width, boolean_math_004.height = 140.0, 100.0
			boolean_math_008.width, boolean_math_008.height = 140.0, 100.0
			set_position_2.width, set_position_2.height = 140.0, 100.0
			group_002_8.width, group_002_8.height = 140.0, 100.0
			endpoint_selection_005.width, endpoint_selection_005.height = 140.0, 100.0
			endpoint_selection_006.width, endpoint_selection_006.height = 140.0, 100.0
			endpoint_selection_007.width, endpoint_selection_007.height = 140.0, 100.0
			boolean_math_009.width, boolean_math_009.height = 140.0, 100.0
			boolean_math_010.width, boolean_math_010.height = 140.0, 100.0
			boolean_math_011.width, boolean_math_011.height = 140.0, 100.0
			endpoint_selection_008.width, endpoint_selection_008.height = 140.0, 100.0
			group_008.width, group_008.height = 140.0, 100.0
			group_014.width, group_014.height = 140.0, 100.0
			position_2.width, position_2.height = 140.0, 100.0
			group_018.width, group_018.height = 140.0, 100.0
			math_12.width, math_12.height = 140.0, 100.0
			group_input_001_5.width, group_input_001_5.height = 140.0, 100.0
			frame_2.width, frame_2.height = 969.5999755859375, 506.0
			capture_attribute_4.width, capture_attribute_4.height = 140.0, 100.0
			reroute_8.width, reroute_8.height = 16.0, 100.0
			frame_001.width, frame_001.height = 689.5999755859375, 526.7999877929688
			set_position_001.width, set_position_001.height = 140.0, 100.0
			endpoint_selection_1.width, endpoint_selection_1.height = 140.0, 100.0
			group_009.width, group_009.height = 140.0, 100.0
			math_001_4.width, math_001_4.height = 140.0, 100.0
			group_input_002_1.width, group_input_002_1.height = 140.0, 100.0
			frame_002_1.width, frame_002_1.height = 420.0, 537.2000122070312
			capture_attribute_001_1.width, capture_attribute_001_1.height = 140.0, 100.0
			group_003_3.width, group_003_3.height = 140.0, 100.0
			boolean_math_8.width, boolean_math_8.height = 140.0, 100.0
			boolean_math_001_5.width, boolean_math_001_5.height = 140.0, 100.0
			group_16.width, group_16.height = 140.0, 100.0

			#initialize _fix_loop_alignment_into_ah links
			#endpoint_selection_005.Selection -> boolean_math_011.Boolean
			_fix_loop_alignment_into_ah.links.new(endpoint_selection_005.outputs[0], boolean_math_011.inputs[0])
			#group_008.Vector -> set_position_2.Offset
			_fix_loop_alignment_into_ah.links.new(group_008.outputs[0], set_position_2.inputs[3])
			#endpoint_selection_003.Selection -> boolean_math_004.Boolean
			_fix_loop_alignment_into_ah.links.new(endpoint_selection_003.outputs[0], boolean_math_004.inputs[0])
			#reroute_8.Output -> group_002_8.Offset
			_fix_loop_alignment_into_ah.links.new(reroute_8.outputs[0], group_002_8.inputs[2])
			#boolean_math_009.Boolean -> boolean_math_010.Boolean
			_fix_loop_alignment_into_ah.links.new(boolean_math_009.outputs[0], boolean_math_010.inputs[0])
			#endpoint_selection_007.Selection -> boolean_math_009.Boolean
			_fix_loop_alignment_into_ah.links.new(endpoint_selection_007.outputs[0], boolean_math_009.inputs[1])
			#math_12.Value -> group_008.Angstrom
			_fix_loop_alignment_into_ah.links.new(math_12.outputs[0], group_008.inputs[2])
			#switch_004.Output -> subdivide_curve.Cuts
			_fix_loop_alignment_into_ah.links.new(switch_004.outputs[0], subdivide_curve.inputs[1])
			#boolean_math_011.Boolean -> boolean_math_010.Boolean
			_fix_loop_alignment_into_ah.links.new(boolean_math_011.outputs[0], boolean_math_010.inputs[1])
			#capture_attribute_4.Value -> group_014.Offset
			_fix_loop_alignment_into_ah.links.new(capture_attribute_4.outputs[1], group_014.inputs[2])
			#endpoint_selection_002.Selection -> boolean_math_008.Boolean
			_fix_loop_alignment_into_ah.links.new(endpoint_selection_002.outputs[0], boolean_math_008.inputs[1])
			#position_2.Position -> group_014.Vector
			_fix_loop_alignment_into_ah.links.new(position_2.outputs[0], group_014.inputs[1])
			#endpoint_selection_004.Selection -> boolean_math_004.Boolean
			_fix_loop_alignment_into_ah.links.new(endpoint_selection_004.outputs[0], boolean_math_004.inputs[1])
			#endpoint_selection_006.Selection -> boolean_math_009.Boolean
			_fix_loop_alignment_into_ah.links.new(endpoint_selection_006.outputs[0], boolean_math_009.inputs[0])
			#reroute_8.Output -> math_12.Value
			_fix_loop_alignment_into_ah.links.new(reroute_8.outputs[0], math_12.inputs[0])
			#group_014.Value -> set_position_2.Position
			_fix_loop_alignment_into_ah.links.new(group_014.outputs[0], set_position_2.inputs[2])
			#boolean_math_004.Boolean -> boolean_math_008.Boolean
			_fix_loop_alignment_into_ah.links.new(boolean_math_004.outputs[0], boolean_math_008.inputs[0])
			#endpoint_selection_008.Selection -> boolean_math_011.Boolean
			_fix_loop_alignment_into_ah.links.new(endpoint_selection_008.outputs[0], boolean_math_011.inputs[1])
			#capture_attribute_4.Geometry -> set_position_2.Geometry
			_fix_loop_alignment_into_ah.links.new(capture_attribute_4.outputs[0], set_position_2.inputs[0])
			#capture_attribute_001_1.Geometry -> subdivide_curve.Curve
			_fix_loop_alignment_into_ah.links.new(capture_attribute_001_1.outputs[0], subdivide_curve.inputs[0])
			#set_position_001.Geometry -> group_output_49.Geometry
			_fix_loop_alignment_into_ah.links.new(set_position_001.outputs[0], group_output_49.inputs[0])
			#group_input_001_5.Tangent -> group_002_8.Vector
			_fix_loop_alignment_into_ah.links.new(group_input_001_5.outputs[1], group_002_8.inputs[1])
			#subdivide_curve.Curve -> capture_attribute_4.Geometry
			_fix_loop_alignment_into_ah.links.new(subdivide_curve.outputs[0], capture_attribute_4.inputs[0])
			#group_018.Value -> capture_attribute_4.Value
			_fix_loop_alignment_into_ah.links.new(group_018.outputs[0], capture_attribute_4.inputs[1])
			#group_002_8.Value -> group_008.Vector
			_fix_loop_alignment_into_ah.links.new(group_002_8.outputs[0], group_008.inputs[0])
			#capture_attribute_4.Value -> reroute_8.Input
			_fix_loop_alignment_into_ah.links.new(capture_attribute_4.outputs[1], reroute_8.inputs[0])
			#set_position_2.Geometry -> set_position_001.Geometry
			_fix_loop_alignment_into_ah.links.new(set_position_2.outputs[0], set_position_001.inputs[0])
			#endpoint_selection_1.Selection -> set_position_001.Selection
			_fix_loop_alignment_into_ah.links.new(endpoint_selection_1.outputs[0], set_position_001.inputs[1])
			#reroute_8.Output -> math_001_4.Value
			_fix_loop_alignment_into_ah.links.new(reroute_8.outputs[0], math_001_4.inputs[0])
			#math_001_4.Value -> group_009.Angstrom
			_fix_loop_alignment_into_ah.links.new(math_001_4.outputs[0], group_009.inputs[2])
			#group_009.Vector -> set_position_001.Offset
			_fix_loop_alignment_into_ah.links.new(group_009.outputs[0], set_position_001.inputs[3])
			#group_input_002_1.Tangent -> group_009.Vector
			_fix_loop_alignment_into_ah.links.new(group_input_002_1.outputs[1], group_009.inputs[0])
			#group_input_49.Curve -> capture_attribute_001_1.Geometry
			_fix_loop_alignment_into_ah.links.new(group_input_49.outputs[0], capture_attribute_001_1.inputs[0])
			#group_003_3.Selection -> capture_attribute_001_1.Selection
			_fix_loop_alignment_into_ah.links.new(group_003_3.outputs[0], capture_attribute_001_1.inputs[1])
			#boolean_math_008.Boolean -> boolean_math_8.Boolean
			_fix_loop_alignment_into_ah.links.new(boolean_math_008.outputs[0], boolean_math_8.inputs[1])
			#group_16.Boolean -> boolean_math_8.Boolean
			_fix_loop_alignment_into_ah.links.new(group_16.outputs[0], boolean_math_8.inputs[0])
			#boolean_math_8.Boolean -> switch_004.Switch
			_fix_loop_alignment_into_ah.links.new(boolean_math_8.outputs[0], switch_004.inputs[0])
			#boolean_math_010.Boolean -> boolean_math_001_5.Boolean
			_fix_loop_alignment_into_ah.links.new(boolean_math_010.outputs[0], boolean_math_001_5.inputs[0])
			#capture_attribute_001_1.Selection -> boolean_math_001_5.Boolean
			_fix_loop_alignment_into_ah.links.new(capture_attribute_001_1.outputs[1], boolean_math_001_5.inputs[1])
			#boolean_math_001_5.Boolean -> set_position_2.Selection
			_fix_loop_alignment_into_ah.links.new(boolean_math_001_5.outputs[0], set_position_2.inputs[1])
			#capture_attribute_001_1.Selection -> group_16.Boolean
			_fix_loop_alignment_into_ah.links.new(capture_attribute_001_1.outputs[1], group_16.inputs[0])
			return _fix_loop_alignment_into_ah

		_fix_loop_alignment_into_ah = _fix_loop_alignment_into_ah_node_group()

		#initialize _ca_to_loops node group
		def _ca_to_loops_node_group():
			_ca_to_loops = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".CA to loops")

			_ca_to_loops.color_tag = 'NONE'
			_ca_to_loops.description = ""


			#_ca_to_loops interface
			#Socket Geometry
			geometry_socket_7 = _ca_to_loops.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			geometry_socket_7.attribute_domain = 'POINT'

			#Socket Geometry
			geometry_socket_8 = _ca_to_loops.interface.new_socket(name = "Geometry", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			geometry_socket_8.attribute_domain = 'POINT'

			#Socket Subdivisions
			subdivisions_socket_1 = _ca_to_loops.interface.new_socket(name = "Subdivisions", in_out='INPUT', socket_type = 'NodeSocketInt')
			subdivisions_socket_1.subtype = 'NONE'
			subdivisions_socket_1.default_value = 12
			subdivisions_socket_1.min_value = 1
			subdivisions_socket_1.max_value = 2147483647
			subdivisions_socket_1.attribute_domain = 'POINT'

			#Socket Thickness
			thickness_socket = _ca_to_loops.interface.new_socket(name = "Thickness", in_out='INPUT', socket_type = 'NodeSocketFloat')
			thickness_socket.subtype = 'NONE'
			thickness_socket.default_value = 0.0
			thickness_socket.min_value = -10000.0
			thickness_socket.max_value = 10000.0
			thickness_socket.attribute_domain = 'POINT'

			#Socket Width
			width_socket = _ca_to_loops.interface.new_socket(name = "Width", in_out='INPUT', socket_type = 'NodeSocketFloat')
			width_socket.subtype = 'NONE'
			width_socket.default_value = 0.0
			width_socket.min_value = -10000.0
			width_socket.max_value = 10000.0
			width_socket.attribute_domain = 'POINT'

			#Socket As Cylinders
			as_cylinders_socket = _ca_to_loops.interface.new_socket(name = "As Cylinders", in_out='INPUT', socket_type = 'NodeSocketBool')
			as_cylinders_socket.attribute_domain = 'POINT'


			#initialize _ca_to_loops nodes
			#node Group Output
			group_output_50 = _ca_to_loops.nodes.new("NodeGroupOutput")
			group_output_50.name = "Group Output"
			group_output_50.is_active_output = True

			#node Group Input
			group_input_50 = _ca_to_loops.nodes.new("NodeGroupInput")
			group_input_50.name = "Group Input"

			#node Frame.001
			frame_001_1 = _ca_to_loops.nodes.new("NodeFrame")
			frame_001_1.label = "catch direct change from one to another (needs improving)"
			frame_001_1.name = "Frame.001"
			frame_001_1.label_size = 20
			frame_001_1.shrink = True

			#node Group.037
			group_037 = _ca_to_loops.nodes.new("GeometryNodeGroup")
			group_037.name = "Group.037"
			group_037.node_tree = curve_custom_profile
			#Socket_8
			group_037.inputs[2].default_value = 'Custom Profile'
			#Input_12
			group_037.inputs[6].default_value = 6
			#Input_13
			group_037.inputs[7].default_value = 1.0
			#Input_14
			group_037.inputs[8].default_value = 0.0

			#node Capture Attribute
			capture_attribute_5 = _ca_to_loops.nodes.new("GeometryNodeCaptureAttribute")
			capture_attribute_5.name = "Capture Attribute"
			capture_attribute_5.active_index = 0
			capture_attribute_5.capture_items.clear()
			capture_attribute_5.capture_items.new('FLOAT', "Rotation")
			capture_attribute_5.capture_items["Rotation"].data_type = 'QUATERNION'
			capture_attribute_5.domain = 'POINT'

			#node Group.039
			group_039 = _ca_to_loops.nodes.new("GeometryNodeGroup")
			group_039.name = "Group.039"
			group_039.node_tree = curve_rotation
			#Socket_1
			group_039.inputs[0].default_value = (0.0, 0.0, 1.0)

			#node Rotate Rotation.004
			rotate_rotation_004 = _ca_to_loops.nodes.new("FunctionNodeRotateRotation")
			rotate_rotation_004.name = "Rotate Rotation.004"
			rotate_rotation_004.rotation_space = 'LOCAL'
			#Rotate By
			rotate_rotation_004.inputs[1].default_value = (0.0, 0.0, 0.0)

			#node Set Curve Normal
			set_curve_normal_2 = _ca_to_loops.nodes.new("GeometryNodeSetCurveNormal")
			set_curve_normal_2.name = "Set Curve Normal"
			set_curve_normal_2.mode = 'MINIMUM_TWIST'
			#Selection
			set_curve_normal_2.inputs[1].default_value = True

			#node Group
			group_17 = _ca_to_loops.nodes.new("GeometryNodeGroup")
			group_17.name = "Group"
			group_17.node_tree = is_loop
			#Socket_1
			group_17.inputs[0].default_value = True
			#Socket_3
			group_17.inputs[1].default_value = False

			#node Group.003
			group_003_4 = _ca_to_loops.nodes.new("GeometryNodeGroup")
			group_003_4.name = "Group.003"
			group_003_4.node_tree = curve_split_splines
			#Socket_4
			group_003_4.inputs[2].default_value = 'Free'
			#Socket_2
			group_003_4.inputs[3].default_value = 0
			#Socket_7
			group_003_4.inputs[4].default_value = 'Split Distance'
			#Socket_6
			group_003_4.inputs[5].default_value = 0.05000000074505806
			#Socket_17
			group_003_4.inputs[8].default_value = 'Bezier'
			#Socket_18
			group_003_4.inputs[9].default_value = 12

			#node Group.005
			group_005_3 = _ca_to_loops.nodes.new("GeometryNodeGroup")
			group_005_3.name = "Group.005"
			group_005_3.node_tree = set_color

			#node Group.006
			group_006_4 = _ca_to_loops.nodes.new("GeometryNodeGroup")
			group_006_4.name = "Group.006"
			group_006_4.node_tree = offset_color
			#Socket_0
			group_006_4.inputs[0].default_value = 0

			#node Group.007
			group_007_2 = _ca_to_loops.nodes.new("GeometryNodeGroup")
			group_007_2.name = "Group.007"
			group_007_2.node_tree = curve_endpoint_values
			#Socket_5
			group_007_2.inputs[0].default_value = 1
			#Socket_1
			group_007_2.inputs[1].default_value = 1
			#Socket_2
			group_007_2.inputs[2].default_value = 0
			#Socket_6
			group_007_2.inputs[3].default_value = 1
			#Socket_3
			group_007_2.inputs[4].default_value = -1

			#node Store Named Attribute
			store_named_attribute_1 = _ca_to_loops.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_1.name = "Store Named Attribute"
			store_named_attribute_1.data_type = 'INT'
			store_named_attribute_1.domain = 'POINT'
			#Selection
			store_named_attribute_1.inputs[1].default_value = True
			#Name
			store_named_attribute_1.inputs[2].default_value = "sec_struct"
			#Value
			store_named_attribute_1.inputs[3].default_value = 3

			#node Capture Attribute.004
			capture_attribute_004 = _ca_to_loops.nodes.new("GeometryNodeCaptureAttribute")
			capture_attribute_004.name = "Capture Attribute.004"
			capture_attribute_004.active_index = 1
			capture_attribute_004.capture_items.clear()
			capture_attribute_004.capture_items.new('FLOAT', "Boolean")
			capture_attribute_004.capture_items["Boolean"].data_type = 'BOOLEAN'
			capture_attribute_004.capture_items.new('FLOAT', "Subdivisions")
			capture_attribute_004.capture_items["Subdivisions"].data_type = 'INT'
			capture_attribute_004.capture_items.new('FLOAT', "Thickness")
			capture_attribute_004.capture_items["Thickness"].data_type = 'FLOAT'
			capture_attribute_004.capture_items.new('FLOAT', "Width")
			capture_attribute_004.capture_items["Width"].data_type = 'FLOAT'
			capture_attribute_004.domain = 'POINT'

			#node Group.019
			group_019 = _ca_to_loops.nodes.new("GeometryNodeGroup")
			group_019.name = "Group.019"
			group_019.node_tree = expand_boolean
			#Socket_2
			group_019.inputs[1].default_value = 1

			#node Reroute.002
			reroute_002_5 = _ca_to_loops.nodes.new("NodeReroute")
			reroute_002_5.name = "Reroute.002"
			#node Reroute.010
			reroute_010_1 = _ca_to_loops.nodes.new("NodeReroute")
			reroute_010_1.name = "Reroute.010"
			#node Boolean Math.003
			boolean_math_003_1 = _ca_to_loops.nodes.new("FunctionNodeBooleanMath")
			boolean_math_003_1.name = "Boolean Math.003"
			boolean_math_003_1.operation = 'OR'

			#node Group.021
			group_021_1 = _ca_to_loops.nodes.new("GeometryNodeGroup")
			group_021_1.name = "Group.021"
			group_021_1.node_tree = is_sheet
			#Socket_1
			group_021_1.inputs[0].default_value = True
			#Socket_3
			group_021_1.inputs[1].default_value = False

			#node Group.022
			group_022 = _ca_to_loops.nodes.new("GeometryNodeGroup")
			group_022.name = "Group.022"
			group_022.node_tree = offset_boolean
			#Socket_1
			group_022.inputs[0].default_value = 0
			#Socket_3
			group_022.inputs[2].default_value = 1

			#node Group.023
			group_023 = _ca_to_loops.nodes.new("GeometryNodeGroup")
			group_023.name = "Group.023"
			group_023.node_tree = is_helix
			#Socket_1
			group_023.inputs[0].default_value = True
			#Socket_3
			group_023.inputs[1].default_value = False

			#node Boolean Math.005
			boolean_math_005 = _ca_to_loops.nodes.new("FunctionNodeBooleanMath")
			boolean_math_005.name = "Boolean Math.005"
			boolean_math_005.operation = 'AND'

			#node Group.024
			group_024 = _ca_to_loops.nodes.new("GeometryNodeGroup")
			group_024.name = "Group.024"
			group_024.node_tree = is_sheet
			#Socket_1
			group_024.inputs[0].default_value = True
			#Socket_3
			group_024.inputs[1].default_value = False

			#node Group.025
			group_025 = _ca_to_loops.nodes.new("GeometryNodeGroup")
			group_025.name = "Group.025"
			group_025.node_tree = offset_boolean
			#Socket_1
			group_025.inputs[0].default_value = 0
			#Socket_3
			group_025.inputs[2].default_value = -1

			#node Group.030
			group_030 = _ca_to_loops.nodes.new("GeometryNodeGroup")
			group_030.name = "Group.030"
			group_030.node_tree = is_helix
			#Socket_1
			group_030.inputs[0].default_value = True
			#Socket_3
			group_030.inputs[1].default_value = False

			#node Boolean Math.006
			boolean_math_006 = _ca_to_loops.nodes.new("FunctionNodeBooleanMath")
			boolean_math_006.name = "Boolean Math.006"
			boolean_math_006.operation = 'AND'

			#node Boolean Math.007
			boolean_math_007 = _ca_to_loops.nodes.new("FunctionNodeBooleanMath")
			boolean_math_007.name = "Boolean Math.007"
			boolean_math_007.operation = 'OR'

			#node Combine XYZ
			combine_xyz = _ca_to_loops.nodes.new("ShaderNodeCombineXYZ")
			combine_xyz.name = "Combine XYZ"
			#Z
			combine_xyz.inputs[2].default_value = 0.0

			#node Reroute
			reroute_9 = _ca_to_loops.nodes.new("NodeReroute")
			reroute_9.name = "Reroute"
			#node Reroute.001
			reroute_001_7 = _ca_to_loops.nodes.new("NodeReroute")
			reroute_001_7.name = "Reroute.001"
			#node Endpoint Selection
			endpoint_selection_2 = _ca_to_loops.nodes.new("GeometryNodeCurveEndpointSelection")
			endpoint_selection_2.name = "Endpoint Selection"
			#Start Size
			endpoint_selection_2.inputs[0].default_value = 1
			#End Size
			endpoint_selection_2.inputs[1].default_value = 1

			#node Switch
			switch_9 = _ca_to_loops.nodes.new("GeometryNodeSwitch")
			switch_9.name = "Switch"
			switch_9.input_type = 'FLOAT'
			#False
			switch_9.inputs[1].default_value = 0.0
			#True
			switch_9.inputs[2].default_value = 0.03999999910593033

			#node Switch.001
			switch_001_4 = _ca_to_loops.nodes.new("GeometryNodeSwitch")
			switch_001_4.name = "Switch.001"
			switch_001_4.input_type = 'FLOAT'
			#True
			switch_001_4.inputs[2].default_value = -0.08999999612569809

			#node Set Position.001
			set_position_001_1 = _ca_to_loops.nodes.new("GeometryNodeSetPosition")
			set_position_001_1.name = "Set Position.001"

			#node Normal
			normal_1 = _ca_to_loops.nodes.new("GeometryNodeInputNormal")
			normal_1.name = "Normal"

			#node Group.009
			group_009_1 = _ca_to_loops.nodes.new("GeometryNodeGroup")
			group_009_1.name = "Group.009"
			group_009_1.node_tree = vector_in_angstroms
			#Socket_4
			group_009_1.inputs[1].default_value = False
			#Socket_3
			group_009_1.inputs[2].default_value = 2.0

			#node Group.010
			group_010_1 = _ca_to_loops.nodes.new("GeometryNodeGroup")
			group_010_1.name = "Group.010"
			group_010_1.node_tree = is_helix
			#Socket_3
			group_010_1.inputs[1].default_value = False

			#node Frame.002
			frame_002_2 = _ca_to_loops.nodes.new("NodeFrame")
			frame_002_2.label = "Expand selection by 1 so the ribbon stops where the SS starts"
			frame_002_2.name = "Frame.002"
			frame_002_2.label_size = 20
			frame_002_2.shrink = True

			#node Group.011
			group_011_1 = _ca_to_loops.nodes.new("GeometryNodeGroup")
			group_011_1.name = "Group.011"
			group_011_1.node_tree = tmp_ss_attributes

			#node Group Input.002
			group_input_002_2 = _ca_to_loops.nodes.new("NodeGroupInput")
			group_input_002_2.name = "Group Input.002"
			group_input_002_2.outputs[1].hide = True
			group_input_002_2.outputs[2].hide = True
			group_input_002_2.outputs[3].hide = True
			group_input_002_2.outputs[4].hide = True
			group_input_002_2.outputs[5].hide = True

			#node Set Curve Normal.001
			set_curve_normal_001 = _ca_to_loops.nodes.new("GeometryNodeSetCurveNormal")
			set_curve_normal_001.name = "Set Curve Normal.001"
			set_curve_normal_001.mode = 'FREE'

			#node Set Handle Type
			set_handle_type_2 = _ca_to_loops.nodes.new("GeometryNodeCurveSetHandles")
			set_handle_type_2.name = "Set Handle Type"
			set_handle_type_2.handle_type = 'AUTO'
			set_handle_type_2.mode = {'LEFT', 'RIGHT'}
			#Selection
			set_handle_type_2.inputs[1].default_value = True

			#node Group.012
			group_012 = _ca_to_loops.nodes.new("GeometryNodeGroup")
			group_012.name = "Group.012"
			group_012.node_tree = _sample_from_ca_curve
			#Socket_3
			group_012.inputs[1].default_value = -0.10000000149011612

			#node Group.013
			group_013 = _ca_to_loops.nodes.new("GeometryNodeGroup")
			group_013.name = "Group.013"
			group_013.node_tree = _sample_from_ca_curve
			#Socket_3
			group_013.inputs[1].default_value = 0.10000000149011612

			#node Switch.002
			switch_002_2 = _ca_to_loops.nodes.new("GeometryNodeSwitch")
			switch_002_2.name = "Switch.002"
			switch_002_2.input_type = 'VECTOR'

			#node Endpoint Selection.001
			endpoint_selection_001_1 = _ca_to_loops.nodes.new("GeometryNodeCurveEndpointSelection")
			endpoint_selection_001_1.name = "Endpoint Selection.001"
			#Start Size
			endpoint_selection_001_1.inputs[0].default_value = 1
			#End Size
			endpoint_selection_001_1.inputs[1].default_value = 0

			#node Switch.003
			switch_003 = _ca_to_loops.nodes.new("GeometryNodeSwitch")
			switch_003.name = "Switch.003"
			switch_003.input_type = 'VECTOR'

			#node Group Input.003
			group_input_003_1 = _ca_to_loops.nodes.new("NodeGroupInput")
			group_input_003_1.name = "Group Input.003"
			group_input_003_1.outputs[0].hide = True
			group_input_003_1.outputs[1].hide = True
			group_input_003_1.outputs[2].hide = True
			group_input_003_1.outputs[3].hide = True
			group_input_003_1.outputs[5].hide = True

			#node Reroute.003
			reroute_003_5 = _ca_to_loops.nodes.new("NodeReroute")
			reroute_003_5.name = "Reroute.003"
			#node Boolean Math.002
			boolean_math_002_2 = _ca_to_loops.nodes.new("FunctionNodeBooleanMath")
			boolean_math_002_2.name = "Boolean Math.002"
			boolean_math_002_2.operation = 'AND'

			#node Capture Attribute.001
			capture_attribute_001_2 = _ca_to_loops.nodes.new("GeometryNodeCaptureAttribute")
			capture_attribute_001_2.name = "Capture Attribute.001"
			capture_attribute_001_2.active_index = 1
			capture_attribute_001_2.capture_items.clear()
			capture_attribute_001_2.capture_items.new('FLOAT', "Position")
			capture_attribute_001_2.capture_items["Position"].data_type = 'FLOAT_VECTOR'
			capture_attribute_001_2.capture_items.new('FLOAT', "Tangent")
			capture_attribute_001_2.capture_items["Tangent"].data_type = 'FLOAT_VECTOR'
			capture_attribute_001_2.domain = 'POINT'

			#node Switch.006
			switch_006 = _ca_to_loops.nodes.new("GeometryNodeSwitch")
			switch_006.name = "Switch.006"
			switch_006.input_type = 'VECTOR'

			#node Group.016
			group_016_1 = _ca_to_loops.nodes.new("GeometryNodeGroup")
			group_016_1.name = "Group.016"
			group_016_1.node_tree = _sample_from_ca_curve
			#Socket_3
			group_016_1.inputs[1].default_value = -0.20000000298023224

			#node Group.017
			group_017_1 = _ca_to_loops.nodes.new("GeometryNodeGroup")
			group_017_1.name = "Group.017"
			group_017_1.node_tree = _sample_from_ca_curve
			#Socket_3
			group_017_1.inputs[1].default_value = 0.20000000298023224

			#node Group.015
			group_015 = _ca_to_loops.nodes.new("GeometryNodeGroup")
			group_015.name = "Group.015"
			group_015.node_tree = _fix_loop_alignment_into_ah

			#node Group.008
			group_008_1 = _ca_to_loops.nodes.new("GeometryNodeGroup")
			group_008_1.name = "Group.008"
			group_008_1.node_tree = is_helix
			#Socket_1
			group_008_1.inputs[0].default_value = True
			#Socket_3
			group_008_1.inputs[1].default_value = False

			#node Group.014
			group_014_1 = _ca_to_loops.nodes.new("GeometryNodeGroup")
			group_014_1.name = "Group.014"
			group_014_1.node_tree = is_sheet
			#Socket_1
			group_014_1.inputs[0].default_value = True
			#Socket_3
			group_014_1.inputs[1].default_value = False

			#node Group.026
			group_026 = _ca_to_loops.nodes.new("GeometryNodeGroup")
			group_026.name = "Group.026"
			group_026.node_tree = expand_boolean
			#Socket_2
			group_026.inputs[1].default_value = 1

			#node Boolean Math.004
			boolean_math_004_1 = _ca_to_loops.nodes.new("FunctionNodeBooleanMath")
			boolean_math_004_1.name = "Boolean Math.004"
			boolean_math_004_1.operation = 'AND'

			#node Group.027
			group_027 = _ca_to_loops.nodes.new("GeometryNodeGroup")
			group_027.name = "Group.027"
			group_027.node_tree = expand_boolean
			#Socket_2
			group_027.inputs[1].default_value = 1

			#node Boolean Math.008
			boolean_math_008_1 = _ca_to_loops.nodes.new("FunctionNodeBooleanMath")
			boolean_math_008_1.name = "Boolean Math.008"
			boolean_math_008_1.operation = 'AND'

			#node Boolean Math.009
			boolean_math_009_1 = _ca_to_loops.nodes.new("FunctionNodeBooleanMath")
			boolean_math_009_1.name = "Boolean Math.009"
			boolean_math_009_1.operation = 'OR'

			#node Frame
			frame_3 = _ca_to_loops.nodes.new("NodeFrame")
			frame_3.label = "Find where it transitions direction from one SS to another"
			frame_3.name = "Frame"
			frame_3.label_size = 20
			frame_3.shrink = True

			#node Spline Length
			spline_length = _ca_to_loops.nodes.new("GeometryNodeSplineLength")
			spline_length.name = "Spline Length"

			#node Compare
			compare_6 = _ca_to_loops.nodes.new("FunctionNodeCompare")
			compare_6.name = "Compare"
			compare_6.data_type = 'INT'
			compare_6.mode = 'ELEMENT'
			compare_6.operation = 'GREATER_THAN'
			#B_INT
			compare_6.inputs[3].default_value = 2

			#node Frame.003
			frame_003_1 = _ca_to_loops.nodes.new("NodeFrame")
			frame_003_1.label = "Don't resample when directly from one SS to another"
			frame_003_1.name = "Frame.003"
			frame_003_1.label_size = 20
			frame_003_1.shrink = True



			#Set parents
			group_019.parent = frame_002_2
			boolean_math_003_1.parent = frame_002_2
			group_021_1.parent = frame_001_1
			group_022.parent = frame_001_1
			group_023.parent = frame_001_1
			boolean_math_005.parent = frame_001_1
			group_024.parent = frame_001_1
			group_025.parent = frame_001_1
			group_030.parent = frame_001_1
			boolean_math_006.parent = frame_001_1
			boolean_math_007.parent = frame_001_1
			group_008_1.parent = frame_3
			group_014_1.parent = frame_3
			group_026.parent = frame_3
			boolean_math_004_1.parent = frame_3
			group_027.parent = frame_3
			boolean_math_008_1.parent = frame_3
			boolean_math_009_1.parent = frame_3
			spline_length.parent = frame_003_1
			compare_6.parent = frame_003_1

			#Set locations
			group_output_50.location = (1980.0, 600.0)
			group_input_50.location = (-1262.4000244140625, 440.0)
			frame_001_1.location = (3959.0, 329.0)
			group_037.location = (1560.0, 600.0)
			capture_attribute_5.location = (-605.5999145507812, 397.86602783203125)
			group_039.location = (-982.4000244140625, 180.0)
			rotate_rotation_004.location = (-822.4000244140625, 180.0)
			set_curve_normal_2.location = (1360.0, 580.0)
			group_17.location = (-2140.0, 360.0)
			group_003_4.location = (-425.5998840332031, 417.86602783203125)
			group_005_3.location = (720.0, 600.0)
			group_006_4.location = (720.0, 440.0)
			group_007_2.location = (560.0, 440.0)
			store_named_attribute_1.location = (1820.0, 600.0)
			capture_attribute_004.location = (-965.5999755859375, 397.86602783203125)
			group_019.location = (-1940.0, 340.0)
			reroute_002_5.location = (1280.0, -20.0)
			reroute_010_1.location = (-320.0, -120.0)
			boolean_math_003_1.location = (-1760.0, 340.0)
			group_021_1.location = (-5229.0322265625, -489.14385986328125)
			group_022.location = (-5069.0322265625, -489.14385986328125)
			group_023.location = (-5229.0322265625, -329.14385986328125)
			boolean_math_005.location = (-5069.0322265625, -329.14385986328125)
			group_024.location = (-5229.0322265625, -809.1438598632812)
			group_025.location = (-5069.0322265625, -809.1438598632812)
			group_030.location = (-5229.0322265625, -649.1438598632812)
			boolean_math_006.location = (-5069.0322265625, -649.1438598632812)
			boolean_math_007.location = (-4909.0322265625, -329.14385986328125)
			combine_xyz.location = (1340.0, 420.0)
			reroute_9.location = (-560.0, 200.0)
			reroute_001_7.location = (-560.0, 180.0)
			endpoint_selection_2.location = (-642.4000244140625, 720.0)
			switch_9.location = (-602.4000244140625, -100.0)
			switch_001_4.location = (-442.3999328613281, -100.0)
			set_position_001_1.location = (277.6000061035156, 600.0)
			normal_1.location = (-82.4000015258789, 440.0)
			group_009_1.location = (77.5999984741211, 440.0)
			group_010_1.location = (-322.3999938964844, 720.0)
			frame_002_2.location = (87.5999984741211, 0.0)
			group_011_1.location = (-782.4000244140625, -240.0)
			group_input_002_2.location = (-982.4000244140625, 1260.0)
			set_curve_normal_001.location = (97.5999984741211, 600.0)
			set_handle_type_2.location = (1180.0, 580.0)
			group_012.location = (-802.4000244140625, 1260.0)
			group_013.location = (-802.4000244140625, 1420.0)
			switch_002_2.location = (-437.5854797363281, 1300.735107421875)
			endpoint_selection_001_1.location = (-802.4000244140625, 1540.0)
			switch_003.location = (-437.5854797363281, 980.7351684570312)
			group_input_003_1.location = (-642.4000244140625, 600.0)
			reroute_003_5.location = (-2.4000015258789062, 600.0)
			boolean_math_002_2.location = (-482.3999938964844, 720.0)
			capture_attribute_001_2.location = (-82.4000015258789, 600.0)
			switch_006.location = (-440.0758361816406, 1138.243408203125)
			group_016_1.location = (-802.4000244140625, 880.0)
			group_017_1.location = (-802.4000244140625, 1080.0)
			group_015.location = (900.0, 600.0)
			group_008_1.location = (-2360.0, 120.0)
			group_014_1.location = (-2360.0, -40.0)
			group_026.location = (-2180.0, 120.0)
			boolean_math_004_1.location = (-2020.0, 120.0)
			group_027.location = (-2180.0, -40.0)
			boolean_math_008_1.location = (-2020.0, -20.0)
			boolean_math_009_1.location = (-1860.0, 120.0)
			frame_3.location = (10.0, 0.0)
			spline_length.location = (360.0, 800.0)
			compare_6.location = (520.0, 800.0)
			frame_003_1.location = (10.0, 20.0)

			#Set dimensions
			group_output_50.width, group_output_50.height = 140.0, 100.0
			group_input_50.width, group_input_50.height = 140.0, 100.0
			frame_001_1.width, frame_001_1.height = 520.0, 690.0
			group_037.width, group_037.height = 244.548095703125, 100.0
			capture_attribute_5.width, capture_attribute_5.height = 140.0, 100.0
			group_039.width, group_039.height = 140.0, 100.0
			rotate_rotation_004.width, rotate_rotation_004.height = 140.0, 100.0
			set_curve_normal_2.width, set_curve_normal_2.height = 140.0, 100.0
			group_17.width, group_17.height = 140.0, 100.0
			group_003_4.width, group_003_4.height = 140.0, 100.0
			group_005_3.width, group_005_3.height = 140.0, 100.0
			group_006_4.width, group_006_4.height = 140.0, 100.0
			group_007_2.width, group_007_2.height = 140.0, 100.0
			store_named_attribute_1.width, store_named_attribute_1.height = 140.0, 100.0
			capture_attribute_004.width, capture_attribute_004.height = 140.0, 100.0
			group_019.width, group_019.height = 140.0, 100.0
			reroute_002_5.width, reroute_002_5.height = 16.0, 100.0
			reroute_010_1.width, reroute_010_1.height = 16.0, 100.0
			boolean_math_003_1.width, boolean_math_003_1.height = 140.0, 100.0
			group_021_1.width, group_021_1.height = 140.0, 100.0
			group_022.width, group_022.height = 140.0, 100.0
			group_023.width, group_023.height = 140.0, 100.0
			boolean_math_005.width, boolean_math_005.height = 140.0, 100.0
			group_024.width, group_024.height = 140.0, 100.0
			group_025.width, group_025.height = 140.0, 100.0
			group_030.width, group_030.height = 140.0, 100.0
			boolean_math_006.width, boolean_math_006.height = 140.0, 100.0
			boolean_math_007.width, boolean_math_007.height = 140.0, 100.0
			combine_xyz.width, combine_xyz.height = 140.0, 100.0
			reroute_9.width, reroute_9.height = 16.0, 100.0
			reroute_001_7.width, reroute_001_7.height = 16.0, 100.0
			endpoint_selection_2.width, endpoint_selection_2.height = 140.0, 100.0
			switch_9.width, switch_9.height = 140.0, 100.0
			switch_001_4.width, switch_001_4.height = 140.0, 100.0
			set_position_001_1.width, set_position_001_1.height = 140.0, 100.0
			normal_1.width, normal_1.height = 140.0, 100.0
			group_009_1.width, group_009_1.height = 140.0, 100.0
			group_010_1.width, group_010_1.height = 140.0, 100.0
			frame_002_2.width, frame_002_2.height = 380.0, 191.60000610351562
			group_011_1.width, group_011_1.height = 140.0, 100.0
			group_input_002_2.width, group_input_002_2.height = 140.0, 100.0
			set_curve_normal_001.width, set_curve_normal_001.height = 140.0, 100.0
			set_handle_type_2.width, set_handle_type_2.height = 140.0, 100.0
			group_012.width, group_012.height = 140.0, 100.0
			group_013.width, group_013.height = 140.0, 100.0
			switch_002_2.width, switch_002_2.height = 140.0, 100.0
			endpoint_selection_001_1.width, endpoint_selection_001_1.height = 140.0, 100.0
			switch_003.width, switch_003.height = 140.0, 100.0
			group_input_003_1.width, group_input_003_1.height = 140.0, 100.0
			reroute_003_5.width, reroute_003_5.height = 16.0, 100.0
			boolean_math_002_2.width, boolean_math_002_2.height = 140.0, 100.0
			capture_attribute_001_2.width, capture_attribute_001_2.height = 140.0, 100.0
			switch_006.width, switch_006.height = 140.0, 100.0
			group_016_1.width, group_016_1.height = 140.0, 100.0
			group_017_1.width, group_017_1.height = 140.0, 100.0
			group_015.width, group_015.height = 262.720458984375, 100.0
			group_008_1.width, group_008_1.height = 140.0, 100.0
			group_014_1.width, group_014_1.height = 140.0, 100.0
			group_026.width, group_026.height = 140.0, 100.0
			boolean_math_004_1.width, boolean_math_004_1.height = 140.0, 100.0
			group_027.width, group_027.height = 140.0, 100.0
			boolean_math_008_1.width, boolean_math_008_1.height = 140.0, 100.0
			boolean_math_009_1.width, boolean_math_009_1.height = 140.0, 100.0
			frame_3.width, frame_3.height = 699.9998779296875, 370.0
			spline_length.width, spline_length.height = 140.0, 100.0
			compare_6.width, compare_6.height = 140.0, 100.0
			frame_003_1.width, frame_003_1.height = 360.0000305175781, 218.79998779296875

			#initialize _ca_to_loops links
			#capture_attribute_004.Geometry -> capture_attribute_5.Geometry
			_ca_to_loops.links.new(capture_attribute_004.outputs[0], capture_attribute_5.inputs[0])
			#reroute_002_5.Output -> group_037.Profile Rotation
			_ca_to_loops.links.new(reroute_002_5.outputs[0], group_037.inputs[3])
			#group_037.Geometry -> store_named_attribute_1.Geometry
			_ca_to_loops.links.new(group_037.outputs[0], store_named_attribute_1.inputs[0])
			#group_021_1.Selection -> group_022.Boolean
			_ca_to_loops.links.new(group_021_1.outputs[0], group_022.inputs[1])
			#group_007_2.Value -> group_006_4.Offset
			_ca_to_loops.links.new(group_007_2.outputs[0], group_006_4.inputs[1])
			#group_019.Boolean -> boolean_math_003_1.Boolean
			_ca_to_loops.links.new(group_019.outputs[0], boolean_math_003_1.inputs[0])
			#set_curve_normal_2.Curve -> group_037.Curve
			_ca_to_loops.links.new(set_curve_normal_2.outputs[0], group_037.inputs[0])
			#boolean_math_003_1.Boolean -> capture_attribute_004.Boolean
			_ca_to_loops.links.new(boolean_math_003_1.outputs[0], capture_attribute_004.inputs[1])
			#group_023.Selection -> boolean_math_005.Boolean
			_ca_to_loops.links.new(group_023.outputs[0], boolean_math_005.inputs[0])
			#capture_attribute_5.Rotation -> group_003_4.Rotation
			_ca_to_loops.links.new(capture_attribute_5.outputs[1], group_003_4.inputs[6])
			#boolean_math_006.Boolean -> boolean_math_007.Boolean
			_ca_to_loops.links.new(boolean_math_006.outputs[0], boolean_math_007.inputs[1])
			#group_024.Selection -> boolean_math_006.Boolean
			_ca_to_loops.links.new(group_024.outputs[0], boolean_math_006.inputs[0])
			#capture_attribute_5.Geometry -> group_003_4.Curve
			_ca_to_loops.links.new(capture_attribute_5.outputs[0], group_003_4.inputs[0])
			#capture_attribute_004.Boolean -> group_003_4.Selection
			_ca_to_loops.links.new(capture_attribute_004.outputs[1], group_003_4.inputs[1])
			#group_17.Selection -> group_019.Boolean
			_ca_to_loops.links.new(group_17.outputs[0], group_019.inputs[0])
			#reroute_010_1.Output -> reroute_002_5.Input
			_ca_to_loops.links.new(reroute_010_1.outputs[0], reroute_002_5.inputs[0])
			#rotate_rotation_004.Rotation -> reroute_010_1.Input
			_ca_to_loops.links.new(rotate_rotation_004.outputs[0], reroute_010_1.inputs[0])
			#group_030.Selection -> group_025.Boolean
			_ca_to_loops.links.new(group_030.outputs[0], group_025.inputs[1])
			#boolean_math_005.Boolean -> boolean_math_007.Boolean
			_ca_to_loops.links.new(boolean_math_005.outputs[0], boolean_math_007.inputs[0])
			#rotate_rotation_004.Rotation -> capture_attribute_5.Rotation
			_ca_to_loops.links.new(rotate_rotation_004.outputs[0], capture_attribute_5.inputs[1])
			#group_025.Boolean -> boolean_math_006.Boolean
			_ca_to_loops.links.new(group_025.outputs[0], boolean_math_006.inputs[1])
			#group_039.Rotation -> rotate_rotation_004.Rotation
			_ca_to_loops.links.new(group_039.outputs[0], rotate_rotation_004.inputs[0])
			#group_022.Boolean -> boolean_math_005.Boolean
			_ca_to_loops.links.new(group_022.outputs[0], boolean_math_005.inputs[1])
			#group_input_50.Geometry -> capture_attribute_004.Geometry
			_ca_to_loops.links.new(group_input_50.outputs[0], capture_attribute_004.inputs[0])
			#store_named_attribute_1.Geometry -> group_output_50.Geometry
			_ca_to_loops.links.new(store_named_attribute_1.outputs[0], group_output_50.inputs[0])
			#combine_xyz.Vector -> group_037.Profile Scale
			_ca_to_loops.links.new(combine_xyz.outputs[0], group_037.inputs[4])
			#group_input_50.Thickness -> capture_attribute_004.Thickness
			_ca_to_loops.links.new(group_input_50.outputs[2], capture_attribute_004.inputs[3])
			#group_input_50.Width -> capture_attribute_004.Width
			_ca_to_loops.links.new(group_input_50.outputs[3], capture_attribute_004.inputs[4])
			#reroute_9.Output -> combine_xyz.X
			_ca_to_loops.links.new(reroute_9.outputs[0], combine_xyz.inputs[0])
			#reroute_001_7.Output -> combine_xyz.Y
			_ca_to_loops.links.new(reroute_001_7.outputs[0], combine_xyz.inputs[1])
			#capture_attribute_004.Thickness -> reroute_9.Input
			_ca_to_loops.links.new(capture_attribute_004.outputs[3], reroute_9.inputs[0])
			#capture_attribute_004.Width -> reroute_001_7.Input
			_ca_to_loops.links.new(capture_attribute_004.outputs[4], reroute_001_7.inputs[0])
			#group_input_50.Subdivisions -> capture_attribute_004.Subdivisions
			_ca_to_loops.links.new(group_input_50.outputs[1], capture_attribute_004.inputs[2])
			#capture_attribute_004.Subdivisions -> group_037.Subdivisions
			_ca_to_loops.links.new(capture_attribute_004.outputs[2], group_037.inputs[1])
			#switch_9.Output -> switch_001_4.False
			_ca_to_loops.links.new(switch_9.outputs[0], switch_001_4.inputs[1])
			#switch_001_4.Output -> group_003_4.Offset Amount
			_ca_to_loops.links.new(switch_001_4.outputs[0], group_003_4.inputs[7])
			#set_curve_normal_001.Curve -> set_position_001_1.Geometry
			_ca_to_loops.links.new(set_curve_normal_001.outputs[0], set_position_001_1.inputs[0])
			#set_handle_type_2.Curve -> set_curve_normal_2.Curve
			_ca_to_loops.links.new(set_handle_type_2.outputs[0], set_curve_normal_2.inputs[0])
			#group_011_1.tmp_ss_is_first -> switch_9.Switch
			_ca_to_loops.links.new(group_011_1.outputs[0], switch_9.inputs[0])
			#group_011_1.tmp_ss_is_last -> switch_001_4.Switch
			_ca_to_loops.links.new(group_011_1.outputs[1], switch_001_4.inputs[0])
			#capture_attribute_001_2.Geometry -> set_curve_normal_001.Curve
			_ca_to_loops.links.new(capture_attribute_001_2.outputs[0], set_curve_normal_001.inputs[0])
			#group_015.Geometry -> set_handle_type_2.Curve
			_ca_to_loops.links.new(group_015.outputs[0], set_handle_type_2.inputs[0])
			#group_input_002_2.Geometry -> group_012.CA Curve
			_ca_to_loops.links.new(group_input_002_2.outputs[0], group_012.inputs[0])
			#group_input_002_2.Geometry -> group_013.CA Curve
			_ca_to_loops.links.new(group_input_002_2.outputs[0], group_013.inputs[0])
			#endpoint_selection_001_1.Selection -> switch_002_2.Switch
			_ca_to_loops.links.new(endpoint_selection_001_1.outputs[0], switch_002_2.inputs[0])
			#group_013.Position -> switch_002_2.False
			_ca_to_loops.links.new(group_013.outputs[0], switch_002_2.inputs[1])
			#group_012.Position -> switch_002_2.True
			_ca_to_loops.links.new(group_012.outputs[0], switch_002_2.inputs[2])
			#endpoint_selection_001_1.Selection -> switch_003.Switch
			_ca_to_loops.links.new(endpoint_selection_001_1.outputs[0], switch_003.inputs[0])
			#group_012.Normal -> switch_003.True
			_ca_to_loops.links.new(group_012.outputs[2], switch_003.inputs[2])
			#group_013.Normal -> switch_003.False
			_ca_to_loops.links.new(group_013.outputs[2], switch_003.inputs[1])
			#switch_002_2.Output -> set_position_001_1.Position
			_ca_to_loops.links.new(switch_002_2.outputs[0], set_position_001_1.inputs[2])
			#switch_003.Output -> set_curve_normal_001.Normal
			_ca_to_loops.links.new(switch_003.outputs[0], set_curve_normal_001.inputs[2])
			#reroute_003_5.Output -> set_curve_normal_001.Selection
			_ca_to_loops.links.new(reroute_003_5.outputs[0], set_curve_normal_001.inputs[1])
			#reroute_003_5.Output -> set_position_001_1.Selection
			_ca_to_loops.links.new(reroute_003_5.outputs[0], set_position_001_1.inputs[1])
			#normal_1.Normal -> group_009_1.Vector
			_ca_to_loops.links.new(normal_1.outputs[0], group_009_1.inputs[0])
			#group_009_1.Vector -> set_position_001_1.Offset
			_ca_to_loops.links.new(group_009_1.outputs[0], set_position_001_1.inputs[3])
			#group_010_1.Selection -> reroute_003_5.Input
			_ca_to_loops.links.new(group_010_1.outputs[0], reroute_003_5.inputs[0])
			#endpoint_selection_2.Selection -> boolean_math_002_2.Boolean
			_ca_to_loops.links.new(endpoint_selection_2.outputs[0], boolean_math_002_2.inputs[0])
			#group_input_003_1.As Cylinders -> boolean_math_002_2.Boolean
			_ca_to_loops.links.new(group_input_003_1.outputs[4], boolean_math_002_2.inputs[1])
			#boolean_math_002_2.Boolean -> group_010_1.And
			_ca_to_loops.links.new(boolean_math_002_2.outputs[0], group_010_1.inputs[0])
			#group_003_4.Curve -> capture_attribute_001_2.Geometry
			_ca_to_loops.links.new(group_003_4.outputs[0], capture_attribute_001_2.inputs[0])
			#switch_002_2.Output -> capture_attribute_001_2.Position
			_ca_to_loops.links.new(switch_002_2.outputs[0], capture_attribute_001_2.inputs[1])
			#endpoint_selection_001_1.Selection -> switch_006.Switch
			_ca_to_loops.links.new(endpoint_selection_001_1.outputs[0], switch_006.inputs[0])
			#group_input_002_2.Geometry -> group_016_1.CA Curve
			_ca_to_loops.links.new(group_input_002_2.outputs[0], group_016_1.inputs[0])
			#group_016_1.Tangent -> switch_006.True
			_ca_to_loops.links.new(group_016_1.outputs[1], switch_006.inputs[2])
			#group_input_002_2.Geometry -> group_017_1.CA Curve
			_ca_to_loops.links.new(group_input_002_2.outputs[0], group_017_1.inputs[0])
			#group_017_1.Tangent -> switch_006.False
			_ca_to_loops.links.new(group_017_1.outputs[1], switch_006.inputs[1])
			#switch_006.Output -> capture_attribute_001_2.Tangent
			_ca_to_loops.links.new(switch_006.outputs[0], capture_attribute_001_2.inputs[2])
			#capture_attribute_001_2.Tangent -> group_015.Tangent
			_ca_to_loops.links.new(capture_attribute_001_2.outputs[2], group_015.inputs[1])
			#group_005_3.Atoms -> group_015.Curve
			_ca_to_loops.links.new(group_005_3.outputs[0], group_015.inputs[0])
			#set_position_001_1.Geometry -> group_005_3.Atoms
			_ca_to_loops.links.new(set_position_001_1.outputs[0], group_005_3.inputs[0])
			#group_006_4.Color -> group_005_3.Color
			_ca_to_loops.links.new(group_006_4.outputs[0], group_005_3.inputs[2])
			#group_026.Boolean -> boolean_math_004_1.Boolean
			_ca_to_loops.links.new(group_026.outputs[0], boolean_math_004_1.inputs[0])
			#group_014_1.Selection -> boolean_math_004_1.Boolean
			_ca_to_loops.links.new(group_014_1.outputs[0], boolean_math_004_1.inputs[1])
			#group_014_1.Selection -> group_027.Boolean
			_ca_to_loops.links.new(group_014_1.outputs[0], group_027.inputs[0])
			#group_008_1.Selection -> group_026.Boolean
			_ca_to_loops.links.new(group_008_1.outputs[0], group_026.inputs[0])
			#group_008_1.Selection -> boolean_math_008_1.Boolean
			_ca_to_loops.links.new(group_008_1.outputs[0], boolean_math_008_1.inputs[0])
			#group_027.Boolean -> boolean_math_008_1.Boolean
			_ca_to_loops.links.new(group_027.outputs[0], boolean_math_008_1.inputs[1])
			#boolean_math_004_1.Boolean -> boolean_math_009_1.Boolean
			_ca_to_loops.links.new(boolean_math_004_1.outputs[0], boolean_math_009_1.inputs[0])
			#boolean_math_008_1.Boolean -> boolean_math_009_1.Boolean
			_ca_to_loops.links.new(boolean_math_008_1.outputs[0], boolean_math_009_1.inputs[1])
			#boolean_math_009_1.Boolean -> boolean_math_003_1.Boolean
			_ca_to_loops.links.new(boolean_math_009_1.outputs[0], boolean_math_003_1.inputs[1])
			#spline_length.Point Count -> compare_6.A
			_ca_to_loops.links.new(spline_length.outputs[1], compare_6.inputs[2])
			#compare_6.Result -> group_005_3.Selection
			_ca_to_loops.links.new(compare_6.outputs[0], group_005_3.inputs[1])
			return _ca_to_loops

		_ca_to_loops = _ca_to_loops_node_group()

		#initialize curve_offset_dot node group
		def curve_offset_dot_node_group():
			curve_offset_dot = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Curve Offset Dot")

			curve_offset_dot.color_tag = 'INPUT'
			curve_offset_dot.description = ""


			#curve_offset_dot interface
			#Socket Output
			output_socket_3 = curve_offset_dot.interface.new_socket(name = "Output", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			output_socket_3.attribute_domain = 'POINT'

			#Socket Leading
			leading_socket = curve_offset_dot.interface.new_socket(name = "Leading", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			leading_socket.subtype = 'NONE'
			leading_socket.default_value = 0
			leading_socket.min_value = -2147483648
			leading_socket.max_value = 2147483647
			leading_socket.attribute_domain = 'POINT'

			#Socket Rotation
			rotation_socket_4 = curve_offset_dot.interface.new_socket(name = "Rotation", in_out='OUTPUT', socket_type = 'NodeSocketRotation')
			rotation_socket_4.attribute_domain = 'POINT'

			#Socket Normal
			normal_socket_3 = curve_offset_dot.interface.new_socket(name = "Normal", in_out='INPUT', socket_type = 'NodeSocketVector')
			normal_socket_3.subtype = 'NONE'
			normal_socket_3.default_value = (0.0, 0.0, 0.0)
			normal_socket_3.min_value = -3.4028234663852886e+38
			normal_socket_3.max_value = 3.4028234663852886e+38
			normal_socket_3.attribute_domain = 'POINT'

			#Socket Menu
			menu_socket_2 = curve_offset_dot.interface.new_socket(name = "Menu", in_out='INPUT', socket_type = 'NodeSocketMenu')
			menu_socket_2.attribute_domain = 'POINT'

			#Socket B
			b_socket = curve_offset_dot.interface.new_socket(name = "B", in_out='INPUT', socket_type = 'NodeSocketFloat')
			b_socket.subtype = 'NONE'
			b_socket.default_value = -0.8999999761581421
			b_socket.min_value = -10000.0
			b_socket.max_value = 10000.0
			b_socket.attribute_domain = 'POINT'

			#Socket Offset
			offset_socket_7 = curve_offset_dot.interface.new_socket(name = "Offset", in_out='INPUT', socket_type = 'NodeSocketInt')
			offset_socket_7.subtype = 'NONE'
			offset_socket_7.default_value = -1
			offset_socket_7.min_value = -2147483647
			offset_socket_7.max_value = 2147483647
			offset_socket_7.attribute_domain = 'POINT'

			#Panel Rotation
			rotation_panel = curve_offset_dot.interface.new_panel("Rotation", default_closed=True)
			#Socket Rotation Axis
			rotation_axis_socket = curve_offset_dot.interface.new_socket(name = "Rotation Axis", in_out='INPUT', socket_type = 'NodeSocketVector', parent = rotation_panel)
			rotation_axis_socket.subtype = 'NONE'
			rotation_axis_socket.default_value = (0.0, 0.0, 1.0)
			rotation_axis_socket.min_value = -3.4028234663852886e+38
			rotation_axis_socket.max_value = 3.4028234663852886e+38
			rotation_axis_socket.attribute_domain = 'POINT'

			#Socket Rotation Amount
			rotation_amount_socket = curve_offset_dot.interface.new_socket(name = "Rotation Amount", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = rotation_panel)
			rotation_amount_socket.subtype = 'NONE'
			rotation_amount_socket.default_value = 3.1415927410125732
			rotation_amount_socket.min_value = -10000.0
			rotation_amount_socket.max_value = 10000.0
			rotation_amount_socket.attribute_domain = 'POINT'



			#initialize curve_offset_dot nodes
			#node Group Output
			group_output_51 = curve_offset_dot.nodes.new("NodeGroupOutput")
			group_output_51.name = "Group Output"
			group_output_51.is_active_output = True

			#node Group Input
			group_input_51 = curve_offset_dot.nodes.new("NodeGroupInput")
			group_input_51.name = "Group Input"

			#node Accumulate Field.001
			accumulate_field_001_4 = curve_offset_dot.nodes.new("GeometryNodeAccumulateField")
			accumulate_field_001_4.name = "Accumulate Field.001"
			accumulate_field_001_4.data_type = 'INT'
			accumulate_field_001_4.domain = 'POINT'

			#node Math
			math_13 = curve_offset_dot.nodes.new("ShaderNodeMath")
			math_13.name = "Math"
			math_13.operation = 'MULTIPLY'
			math_13.use_clamp = False

			#node Axis Angle to Rotation
			axis_angle_to_rotation_1 = curve_offset_dot.nodes.new("FunctionNodeAxisAngleToRotation")
			axis_angle_to_rotation_1.name = "Axis Angle to Rotation"

			#node Group.002
			group_002_9 = curve_offset_dot.nodes.new("GeometryNodeGroup")
			group_002_9.name = "Group.002"
			group_002_9.node_tree = offset_vector
			#Socket_2
			group_002_9.inputs[0].default_value = 0

			#node Vector Math.002
			vector_math_002_1 = curve_offset_dot.nodes.new("ShaderNodeVectorMath")
			vector_math_002_1.name = "Vector Math.002"
			vector_math_002_1.operation = 'DOT_PRODUCT'

			#node Compare.001
			compare_001_3 = curve_offset_dot.nodes.new("FunctionNodeCompare")
			compare_001_3.name = "Compare.001"
			compare_001_3.data_type = 'FLOAT'
			compare_001_3.mode = 'ELEMENT'
			compare_001_3.operation = 'LESS_THAN'

			#node Curve of Point.001
			curve_of_point_001_1 = curve_offset_dot.nodes.new("GeometryNodeCurveOfPoint")
			curve_of_point_001_1.name = "Curve of Point.001"
			#Point Index
			curve_of_point_001_1.inputs[0].default_value = 0

			#node Reroute.003
			reroute_003_6 = curve_offset_dot.nodes.new("NodeReroute")
			reroute_003_6.name = "Reroute.003"
			#node Compare.002
			compare_002_4 = curve_offset_dot.nodes.new("FunctionNodeCompare")
			compare_002_4.name = "Compare.002"
			compare_002_4.data_type = 'FLOAT'
			compare_002_4.mode = 'ELEMENT'
			compare_002_4.operation = 'GREATER_THAN'

			#node Menu Switch
			menu_switch_3 = curve_offset_dot.nodes.new("GeometryNodeMenuSwitch")
			menu_switch_3.name = "Menu Switch"
			menu_switch_3.active_index = 1
			menu_switch_3.data_type = 'BOOLEAN'
			menu_switch_3.enum_items.clear()
			menu_switch_3.enum_items.new("Less Than")
			menu_switch_3.enum_items[0].description = ""
			menu_switch_3.enum_items.new("Greater Than")
			menu_switch_3.enum_items[1].description = ""




			#Set locations
			group_output_51.location = (600.0, 100.0)
			group_input_51.location = (-800.0, 40.0)
			accumulate_field_001_4.location = (100.0, 80.0)
			math_13.location = (280.0, 0.0)
			axis_angle_to_rotation_1.location = (440.0, 0.0)
			group_002_9.location = (-560.0, -20.0)
			vector_math_002_1.location = (-400.0, 120.0)
			compare_001_3.location = (-220.0, 100.0)
			curve_of_point_001_1.location = (-60.0, -80.0)
			reroute_003_6.location = (-600.0, 40.0)
			compare_002_4.location = (-220.0, -60.0)
			menu_switch_3.location = (-60.0, 100.0)

			#Set dimensions
			group_output_51.width, group_output_51.height = 140.0, 100.0
			group_input_51.width, group_input_51.height = 140.0, 100.0
			accumulate_field_001_4.width, accumulate_field_001_4.height = 140.0, 100.0
			math_13.width, math_13.height = 140.0, 100.0
			axis_angle_to_rotation_1.width, axis_angle_to_rotation_1.height = 140.0, 100.0
			group_002_9.width, group_002_9.height = 140.0, 100.0
			vector_math_002_1.width, vector_math_002_1.height = 140.0, 100.0
			compare_001_3.width, compare_001_3.height = 140.0, 100.0
			curve_of_point_001_1.width, curve_of_point_001_1.height = 140.0, 100.0
			reroute_003_6.width, reroute_003_6.height = 16.0, 100.0
			compare_002_4.width, compare_002_4.height = 140.0, 100.0
			menu_switch_3.width, menu_switch_3.height = 140.0, 100.0

			#initialize curve_offset_dot links
			#curve_of_point_001_1.Curve Index -> accumulate_field_001_4.Group ID
			curve_offset_dot.links.new(curve_of_point_001_1.outputs[0], accumulate_field_001_4.inputs[1])
			#math_13.Value -> axis_angle_to_rotation_1.Angle
			curve_offset_dot.links.new(math_13.outputs[0], axis_angle_to_rotation_1.inputs[1])
			#vector_math_002_1.Value -> compare_001_3.A
			curve_offset_dot.links.new(vector_math_002_1.outputs[1], compare_001_3.inputs[0])
			#accumulate_field_001_4.Trailing -> math_13.Value
			curve_offset_dot.links.new(accumulate_field_001_4.outputs[1], math_13.inputs[0])
			#group_002_9.Value -> vector_math_002_1.Vector
			curve_offset_dot.links.new(group_002_9.outputs[0], vector_math_002_1.inputs[1])
			#reroute_003_6.Output -> vector_math_002_1.Vector
			curve_offset_dot.links.new(reroute_003_6.outputs[0], vector_math_002_1.inputs[0])
			#reroute_003_6.Output -> group_002_9.Vector
			curve_offset_dot.links.new(reroute_003_6.outputs[0], group_002_9.inputs[1])
			#group_input_51.Normal -> reroute_003_6.Input
			curve_offset_dot.links.new(group_input_51.outputs[0], reroute_003_6.inputs[0])
			#axis_angle_to_rotation_1.Rotation -> group_output_51.Rotation
			curve_offset_dot.links.new(axis_angle_to_rotation_1.outputs[0], group_output_51.inputs[2])
			#accumulate_field_001_4.Trailing -> group_output_51.Leading
			curve_offset_dot.links.new(accumulate_field_001_4.outputs[1], group_output_51.inputs[1])
			#group_input_51.B -> compare_001_3.B
			curve_offset_dot.links.new(group_input_51.outputs[2], compare_001_3.inputs[1])
			#vector_math_002_1.Value -> compare_002_4.A
			curve_offset_dot.links.new(vector_math_002_1.outputs[1], compare_002_4.inputs[0])
			#group_input_51.B -> compare_002_4.B
			curve_offset_dot.links.new(group_input_51.outputs[2], compare_002_4.inputs[1])
			#compare_001_3.Result -> menu_switch_3.Less Than
			curve_offset_dot.links.new(compare_001_3.outputs[0], menu_switch_3.inputs[1])
			#compare_002_4.Result -> menu_switch_3.Greater Than
			curve_offset_dot.links.new(compare_002_4.outputs[0], menu_switch_3.inputs[2])
			#menu_switch_3.Output -> accumulate_field_001_4.Value
			curve_offset_dot.links.new(menu_switch_3.outputs[0], accumulate_field_001_4.inputs[0])
			#group_input_51.Menu -> menu_switch_3.Menu
			curve_offset_dot.links.new(group_input_51.outputs[1], menu_switch_3.inputs[0])
			#menu_switch_3.Output -> group_output_51.Output
			curve_offset_dot.links.new(menu_switch_3.outputs[0], group_output_51.inputs[0])
			#group_input_51.Offset -> group_002_9.Offset
			curve_offset_dot.links.new(group_input_51.outputs[3], group_002_9.inputs[2])
			#group_input_51.Rotation Amount -> math_13.Value
			curve_offset_dot.links.new(group_input_51.outputs[5], math_13.inputs[1])
			#group_input_51.Rotation Axis -> axis_angle_to_rotation_1.Axis
			curve_offset_dot.links.new(group_input_51.outputs[4], axis_angle_to_rotation_1.inputs[0])
			return curve_offset_dot

		curve_offset_dot = curve_offset_dot_node_group()

		#initialize _tweak_arrow_heads node group
		def _tweak_arrow_heads_node_group():
			_tweak_arrow_heads = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".Tweak Arrow Heads")

			_tweak_arrow_heads.color_tag = 'NONE'
			_tweak_arrow_heads.description = ""


			#_tweak_arrow_heads interface
			#Socket Output
			output_socket_4 = _tweak_arrow_heads.interface.new_socket(name = "Output", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			output_socket_4.attribute_domain = 'POINT'

			#Socket Geometry
			geometry_socket_9 = _tweak_arrow_heads.interface.new_socket(name = "Geometry", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			geometry_socket_9.attribute_domain = 'POINT'

			#Socket Rounded
			rounded_socket = _tweak_arrow_heads.interface.new_socket(name = "Rounded", in_out='INPUT', socket_type = 'NodeSocketBool')
			rounded_socket.attribute_domain = 'POINT'

			#Socket Input
			input_socket_1 = _tweak_arrow_heads.interface.new_socket(name = "Input", in_out='INPUT', socket_type = 'NodeSocketFloat')
			input_socket_1.subtype = 'NONE'
			input_socket_1.default_value = 0.0
			input_socket_1.min_value = -3.4028234663852886e+38
			input_socket_1.max_value = 3.4028234663852886e+38
			input_socket_1.attribute_domain = 'POINT'


			#initialize _tweak_arrow_heads nodes
			#node Group Output
			group_output_52 = _tweak_arrow_heads.nodes.new("NodeGroupOutput")
			group_output_52.name = "Group Output"
			group_output_52.is_active_output = True

			#node Group Input
			group_input_52 = _tweak_arrow_heads.nodes.new("NodeGroupInput")
			group_input_52.name = "Group Input"

			#node Extrude Mesh
			extrude_mesh = _tweak_arrow_heads.nodes.new("GeometryNodeExtrudeMesh")
			extrude_mesh.name = "Extrude Mesh"
			extrude_mesh.mode = 'FACES'
			#Individual
			extrude_mesh.inputs[4].default_value = False

			#node Normal
			normal_2 = _tweak_arrow_heads.nodes.new("GeometryNodeInputNormal")
			normal_2.name = "Normal"

			#node Map Range
			map_range = _tweak_arrow_heads.nodes.new("ShaderNodeMapRange")
			map_range.name = "Map Range"
			map_range.clamp = True
			map_range.data_type = 'FLOAT'
			map_range.interpolation_type = 'LINEAR'
			#From Min
			map_range.inputs[1].default_value = 0.0
			#From Max
			map_range.inputs[2].default_value = 1.0
			#To Min
			map_range.inputs[3].default_value = 0.0

			#node Vector Math
			vector_math_3 = _tweak_arrow_heads.nodes.new("ShaderNodeVectorMath")
			vector_math_3.name = "Vector Math"
			vector_math_3.operation = 'DOT_PRODUCT'

			#node Math.001
			math_001_5 = _tweak_arrow_heads.nodes.new("ShaderNodeMath")
			math_001_5.name = "Math.001"
			math_001_5.operation = 'ABSOLUTE'
			math_001_5.use_clamp = False

			#node Group.001
			group_001_10 = _tweak_arrow_heads.nodes.new("GeometryNodeGroup")
			group_001_10.name = "Group.001"
			group_001_10.node_tree = mn_units
			#Input_1
			group_001_10.inputs[0].default_value = 0.8900001645088196

			#node Compare.001
			compare_001_4 = _tweak_arrow_heads.nodes.new("FunctionNodeCompare")
			compare_001_4.name = "Compare.001"
			compare_001_4.data_type = 'FLOAT'
			compare_001_4.mode = 'ELEMENT'
			compare_001_4.operation = 'EQUAL'
			#B
			compare_001_4.inputs[1].default_value = 0.0
			#Epsilon
			compare_001_4.inputs[12].default_value = 0.5

			#node Boolean Math.001
			boolean_math_001_6 = _tweak_arrow_heads.nodes.new("FunctionNodeBooleanMath")
			boolean_math_001_6.name = "Boolean Math.001"
			boolean_math_001_6.operation = 'AND'

			#node Capture Attribute.002
			capture_attribute_002_2 = _tweak_arrow_heads.nodes.new("GeometryNodeCaptureAttribute")
			capture_attribute_002_2.name = "Capture Attribute.002"
			capture_attribute_002_2.active_index = 1
			capture_attribute_002_2.capture_items.clear()
			capture_attribute_002_2.capture_items.new('FLOAT', "Boolean")
			capture_attribute_002_2.capture_items["Boolean"].data_type = 'BOOLEAN'
			capture_attribute_002_2.capture_items.new('FLOAT', "Normal")
			capture_attribute_002_2.capture_items["Normal"].data_type = 'FLOAT_VECTOR'
			capture_attribute_002_2.domain = 'FACE'

			#node Evaluate on Domain
			evaluate_on_domain = _tweak_arrow_heads.nodes.new("GeometryNodeFieldOnDomain")
			evaluate_on_domain.name = "Evaluate on Domain"
			evaluate_on_domain.data_type = 'FLOAT'
			evaluate_on_domain.domain = 'FACE'

			#node Compare
			compare_7 = _tweak_arrow_heads.nodes.new("FunctionNodeCompare")
			compare_7.name = "Compare"
			compare_7.data_type = 'FLOAT'
			compare_7.mode = 'ELEMENT'
			compare_7.operation = 'GREATER_THAN'
			#B
			compare_7.inputs[1].default_value = 0.4399999976158142

			#node Compare.002
			compare_002_5 = _tweak_arrow_heads.nodes.new("FunctionNodeCompare")
			compare_002_5.name = "Compare.002"
			compare_002_5.data_type = 'FLOAT'
			compare_002_5.mode = 'ELEMENT'
			compare_002_5.operation = 'LESS_THAN'
			#B
			compare_002_5.inputs[1].default_value = 1.0

			#node Set Position
			set_position_3 = _tweak_arrow_heads.nodes.new("GeometryNodeSetPosition")
			set_position_3.name = "Set Position"
			#Position
			set_position_3.inputs[2].default_value = (0.0, 0.0, 0.0)

			#node Group
			group_18 = _tweak_arrow_heads.nodes.new("GeometryNodeGroup")
			group_18.name = "Group"
			group_18.node_tree = vector_in_angstroms
			#Socket_4
			group_18.inputs[1].default_value = False

			#node Map Range.002
			map_range_002 = _tweak_arrow_heads.nodes.new("ShaderNodeMapRange")
			map_range_002.name = "Map Range.002"
			map_range_002.clamp = True
			map_range_002.data_type = 'FLOAT'
			map_range_002.interpolation_type = 'LINEAR'
			#From Min
			map_range_002.inputs[1].default_value = 0.0
			#From Max
			map_range_002.inputs[2].default_value = 1.0
			#To Min
			map_range_002.inputs[3].default_value = 0.0
			#To Max
			map_range_002.inputs[4].default_value = -0.20000001788139343

			#node Switch
			switch_10 = _tweak_arrow_heads.nodes.new("GeometryNodeSwitch")
			switch_10.name = "Switch"
			switch_10.input_type = 'GEOMETRY'

			#node Set Position.001
			set_position_001_2 = _tweak_arrow_heads.nodes.new("GeometryNodeSetPosition")
			set_position_001_2.name = "Set Position.001"
			#Position
			set_position_001_2.inputs[2].default_value = (0.0, 0.0, 0.0)

			#node Group.004
			group_004_4 = _tweak_arrow_heads.nodes.new("GeometryNodeGroup")
			group_004_4.name = "Group.004"
			group_004_4.node_tree = vector_in_angstroms
			#Socket_4
			group_004_4.inputs[1].default_value = False

			#node Map Range.003
			map_range_003 = _tweak_arrow_heads.nodes.new("ShaderNodeMapRange")
			map_range_003.name = "Map Range.003"
			map_range_003.clamp = True
			map_range_003.data_type = 'FLOAT'
			map_range_003.interpolation_type = 'LINEAR'
			#From Min
			map_range_003.inputs[1].default_value = 0.0
			#From Max
			map_range_003.inputs[2].default_value = 3.7699999809265137
			#To Min
			map_range_003.inputs[3].default_value = 0.0
			#To Max
			map_range_003.inputs[4].default_value = -0.14000000059604645

			#node Switch.004
			switch_004_1 = _tweak_arrow_heads.nodes.new("GeometryNodeSwitch")
			switch_004_1.name = "Switch.004"
			switch_004_1.input_type = 'FLOAT'
			#True
			switch_004_1.inputs[2].default_value = 0.0

			#node Reroute.001
			reroute_001_8 = _tweak_arrow_heads.nodes.new("NodeReroute")
			reroute_001_8.name = "Reroute.001"
			#node Compare.003
			compare_003_2 = _tweak_arrow_heads.nodes.new("FunctionNodeCompare")
			compare_003_2.name = "Compare.003"
			compare_003_2.data_type = 'FLOAT'
			compare_003_2.mode = 'ELEMENT'
			compare_003_2.operation = 'GREATER_THAN'
			#B
			compare_003_2.inputs[1].default_value = 0.8999999761581421

			#node Normal.002
			normal_002 = _tweak_arrow_heads.nodes.new("GeometryNodeInputNormal")
			normal_002.name = "Normal.002"

			#node Group.002
			group_002_10 = _tweak_arrow_heads.nodes.new("GeometryNodeGroup")
			group_002_10.name = "Group.002"
			group_002_10.node_tree = tmp_ss_attributes
			group_002_10.outputs[0].hide = True
			group_002_10.outputs[1].hide = True
			group_002_10.outputs[2].hide = True
			group_002_10.outputs[3].hide = True
			group_002_10.outputs[4].hide = True

			#node Group.003
			group_003_5 = _tweak_arrow_heads.nodes.new("GeometryNodeGroup")
			group_003_5.name = "Group.003"
			group_003_5.node_tree = tmp_ss_attributes
			group_003_5.outputs[0].hide = True
			group_003_5.outputs[1].hide = True
			group_003_5.outputs[2].hide = True
			group_003_5.outputs[3].hide = True
			group_003_5.outputs[4].hide = True
			group_003_5.outputs[5].hide = True

			#node Reroute
			reroute_10 = _tweak_arrow_heads.nodes.new("NodeReroute")
			reroute_10.name = "Reroute"
			#node Group Input.001
			group_input_001_6 = _tweak_arrow_heads.nodes.new("NodeGroupInput")
			group_input_001_6.name = "Group Input.001"
			group_input_001_6.outputs[0].hide = True
			group_input_001_6.outputs[2].hide = True
			group_input_001_6.outputs[3].hide = True

			#node Reroute.003
			reroute_003_7 = _tweak_arrow_heads.nodes.new("NodeReroute")
			reroute_003_7.name = "Reroute.003"
			#node Reroute.004
			reroute_004_3 = _tweak_arrow_heads.nodes.new("NodeReroute")
			reroute_004_3.name = "Reroute.004"
			#node Reroute.005
			reroute_005_1 = _tweak_arrow_heads.nodes.new("NodeReroute")
			reroute_005_1.name = "Reroute.005"
			#node Reroute.006
			reroute_006_1 = _tweak_arrow_heads.nodes.new("NodeReroute")
			reroute_006_1.name = "Reroute.006"
			#node Reroute.002
			reroute_002_6 = _tweak_arrow_heads.nodes.new("NodeReroute")
			reroute_002_6.name = "Reroute.002"



			#Set locations
			group_output_52.location = (412.5384826660156, 321.8724060058594)
			group_input_52.location = (-1607.4615478515625, 201.87240600585938)
			extrude_mesh.location = (-510.6846618652344, 224.22409057617188)
			normal_2.location = (-1767.4615478515625, -458.1275939941406)
			map_range.location = (-674.5552978515625, -16.81798553466797)
			vector_math_3.location = (-1587.4615478515625, -478.1275939941406)
			math_001_5.location = (-1427.4615478515625, -478.1275939941406)
			group_001_10.location = (-679.3472900390625, -277.635986328125)
			compare_001_4.location = (-1267.4615478515625, -478.1275939941406)
			boolean_math_001_6.location = (-1087.4615478515625, -158.12759399414062)
			capture_attribute_002_2.location = (-757.3184814453125, 222.22958374023438)
			evaluate_on_domain.location = (-1267.4615478515625, -318.1275939941406)
			compare_7.location = (-1107.4615478515625, -318.1275939941406)
			compare_002_5.location = (-1267.4615478515625, -158.12759399414062)
			set_position_3.location = (243.4894561767578, 151.32467651367188)
			group_18.location = (243.4894561767578, -8.675328254699707)
			map_range_002.location = (243.4894561767578, -168.6753387451172)
			switch_10.location = (244.42422485351562, 324.3465270996094)
			set_position_001_2.location = (82.4095687866211, 163.94786071777344)
			group_004_4.location = (-120.7271499633789, 111.24515533447266)
			map_range_003.location = (-361.1294860839844, -162.6943359375)
			switch_004_1.location = (-92.9600601196289, -71.98685455322266)
			reroute_001_8.location = (-467.4615173339844, -98.12759399414062)
			compare_003_2.location = (-367.8775329589844, 14.738061904907227)
			normal_002.location = (-747.4615478515625, 61.872406005859375)
			group_002_10.location = (-1767.4615478515625, -538.1275634765625)
			group_003_5.location = (72.5384750366211, 1.8724075555801392)
			reroute_10.location = (52.538475036621094, 201.87240600585938)
			group_input_001_6.location = (92.5384750366211, 321.8724060058594)
			reroute_003_7.location = (-747.4615478515625, -478.1275939941406)
			reroute_004_3.location = (92.5384750366211, -458.1275939941406)
			reroute_005_1.location = (-1327.4615478515625, -118.1275863647461)
			reroute_006_1.location = (-827.4615478515625, -118.1275863647461)
			reroute_002_6.location = (32.538475036621094, 141.87240600585938)

			#Set dimensions
			group_output_52.width, group_output_52.height = 140.0, 100.0
			group_input_52.width, group_input_52.height = 140.0, 100.0
			extrude_mesh.width, extrude_mesh.height = 140.0, 100.0
			normal_2.width, normal_2.height = 140.0, 100.0
			map_range.width, map_range.height = 140.0, 100.0
			vector_math_3.width, vector_math_3.height = 140.0, 100.0
			math_001_5.width, math_001_5.height = 140.0, 100.0
			group_001_10.width, group_001_10.height = 140.0, 100.0
			compare_001_4.width, compare_001_4.height = 140.0, 100.0
			boolean_math_001_6.width, boolean_math_001_6.height = 140.0, 100.0
			capture_attribute_002_2.width, capture_attribute_002_2.height = 140.0, 100.0
			evaluate_on_domain.width, evaluate_on_domain.height = 140.0, 100.0
			compare_7.width, compare_7.height = 140.0, 100.0
			compare_002_5.width, compare_002_5.height = 140.0, 100.0
			set_position_3.width, set_position_3.height = 140.0, 100.0
			group_18.width, group_18.height = 140.0, 100.0
			map_range_002.width, map_range_002.height = 140.0, 100.0
			switch_10.width, switch_10.height = 140.0, 100.0
			set_position_001_2.width, set_position_001_2.height = 140.0, 100.0
			group_004_4.width, group_004_4.height = 140.0, 100.0
			map_range_003.width, map_range_003.height = 140.0, 100.0
			switch_004_1.width, switch_004_1.height = 140.0, 100.0
			reroute_001_8.width, reroute_001_8.height = 16.0, 100.0
			compare_003_2.width, compare_003_2.height = 140.0, 100.0
			normal_002.width, normal_002.height = 140.0, 100.0
			group_002_10.width, group_002_10.height = 140.0, 100.0
			group_003_5.width, group_003_5.height = 140.0, 100.0
			reroute_10.width, reroute_10.height = 16.0, 100.0
			group_input_001_6.width, group_input_001_6.height = 140.0, 100.0
			reroute_003_7.width, reroute_003_7.height = 16.0, 100.0
			reroute_004_3.width, reroute_004_3.height = 16.0, 100.0
			reroute_005_1.width, reroute_005_1.height = 16.0, 100.0
			reroute_006_1.width, reroute_006_1.height = 16.0, 100.0
			reroute_002_6.width, reroute_002_6.height = 16.0, 100.0

			#initialize _tweak_arrow_heads links
			#compare_001_4.Result -> evaluate_on_domain.Value
			_tweak_arrow_heads.links.new(compare_001_4.outputs[0], evaluate_on_domain.inputs[0])
			#capture_attribute_002_2.Geometry -> extrude_mesh.Mesh
			_tweak_arrow_heads.links.new(capture_attribute_002_2.outputs[0], extrude_mesh.inputs[0])
			#set_position_3.Geometry -> switch_10.False
			_tweak_arrow_heads.links.new(set_position_3.outputs[0], switch_10.inputs[1])
			#capture_attribute_002_2.Boolean -> extrude_mesh.Selection
			_tweak_arrow_heads.links.new(capture_attribute_002_2.outputs[1], extrude_mesh.inputs[1])
			#reroute_10.Output -> switch_10.True
			_tweak_arrow_heads.links.new(reroute_10.outputs[0], switch_10.inputs[2])
			#reroute_006_1.Output -> reroute_001_8.Input
			_tweak_arrow_heads.links.new(reroute_006_1.outputs[0], reroute_001_8.inputs[0])
			#boolean_math_001_6.Boolean -> capture_attribute_002_2.Boolean
			_tweak_arrow_heads.links.new(boolean_math_001_6.outputs[0], capture_attribute_002_2.inputs[1])
			#map_range_002.Result -> group_18.Angstrom
			_tweak_arrow_heads.links.new(map_range_002.outputs[0], group_18.inputs[2])
			#compare_003_2.Result -> switch_004_1.Switch
			_tweak_arrow_heads.links.new(compare_003_2.outputs[0], switch_004_1.inputs[0])
			#reroute_004_3.Output -> map_range_002.Value
			_tweak_arrow_heads.links.new(reroute_004_3.outputs[0], map_range_002.inputs[0])
			#group_001_10.Angstrom -> map_range.To Max
			_tweak_arrow_heads.links.new(group_001_10.outputs[0], map_range.inputs[4])
			#reroute_002_6.Output -> set_position_3.Selection
			_tweak_arrow_heads.links.new(reroute_002_6.outputs[0], set_position_3.inputs[1])
			#reroute_001_8.Output -> map_range_003.Value
			_tweak_arrow_heads.links.new(reroute_001_8.outputs[0], map_range_003.inputs[0])
			#group_18.Vector -> set_position_3.Offset
			_tweak_arrow_heads.links.new(group_18.outputs[0], set_position_3.inputs[3])
			#group_004_4.Vector -> set_position_001_2.Offset
			_tweak_arrow_heads.links.new(group_004_4.outputs[0], set_position_001_2.inputs[3])
			#capture_attribute_002_2.Normal -> group_004_4.Vector
			_tweak_arrow_heads.links.new(capture_attribute_002_2.outputs[2], group_004_4.inputs[0])
			#math_001_5.Value -> compare_001_4.A
			_tweak_arrow_heads.links.new(math_001_5.outputs[0], compare_001_4.inputs[0])
			#set_position_001_2.Geometry -> set_position_3.Geometry
			_tweak_arrow_heads.links.new(set_position_001_2.outputs[0], set_position_3.inputs[0])
			#reroute_002_6.Output -> set_position_001_2.Selection
			_tweak_arrow_heads.links.new(reroute_002_6.outputs[0], set_position_001_2.inputs[1])
			#capture_attribute_002_2.Normal -> extrude_mesh.Offset
			_tweak_arrow_heads.links.new(capture_attribute_002_2.outputs[2], extrude_mesh.inputs[2])
			#reroute_10.Output -> set_position_001_2.Geometry
			_tweak_arrow_heads.links.new(reroute_10.outputs[0], set_position_001_2.inputs[0])
			#switch_004_1.Output -> group_004_4.Angstrom
			_tweak_arrow_heads.links.new(switch_004_1.outputs[0], group_004_4.inputs[2])
			#normal_002.Normal -> capture_attribute_002_2.Normal
			_tweak_arrow_heads.links.new(normal_002.outputs[0], capture_attribute_002_2.inputs[2])
			#compare_002_5.Result -> boolean_math_001_6.Boolean
			_tweak_arrow_heads.links.new(compare_002_5.outputs[0], boolean_math_001_6.inputs[0])
			#map_range_003.Result -> switch_004_1.False
			_tweak_arrow_heads.links.new(map_range_003.outputs[0], switch_004_1.inputs[1])
			#reroute_005_1.Output -> compare_002_5.A
			_tweak_arrow_heads.links.new(reroute_005_1.outputs[0], compare_002_5.inputs[0])
			#vector_math_3.Value -> math_001_5.Value
			_tweak_arrow_heads.links.new(vector_math_3.outputs[1], math_001_5.inputs[0])
			#reroute_006_1.Output -> map_range.Value
			_tweak_arrow_heads.links.new(reroute_006_1.outputs[0], map_range.inputs[0])
			#reroute_001_8.Output -> compare_003_2.A
			_tweak_arrow_heads.links.new(reroute_001_8.outputs[0], compare_003_2.inputs[0])
			#evaluate_on_domain.Value -> compare_7.A
			_tweak_arrow_heads.links.new(evaluate_on_domain.outputs[0], compare_7.inputs[0])
			#map_range.Result -> extrude_mesh.Offset Scale
			_tweak_arrow_heads.links.new(map_range.outputs[0], extrude_mesh.inputs[3])
			#group_input_52.Geometry -> capture_attribute_002_2.Geometry
			_tweak_arrow_heads.links.new(group_input_52.outputs[0], capture_attribute_002_2.inputs[0])
			#switch_10.Output -> group_output_52.Output
			_tweak_arrow_heads.links.new(switch_10.outputs[0], group_output_52.inputs[0])
			#compare_7.Result -> boolean_math_001_6.Boolean
			_tweak_arrow_heads.links.new(compare_7.outputs[0], boolean_math_001_6.inputs[1])
			#group_002_10.tmp_curve_normal -> vector_math_3.Vector
			_tweak_arrow_heads.links.new(group_002_10.outputs[5], vector_math_3.inputs[1])
			#normal_2.Normal -> vector_math_3.Vector
			_tweak_arrow_heads.links.new(normal_2.outputs[0], vector_math_3.inputs[0])
			#group_003_5.tmp_curve_tangent -> group_18.Vector
			_tweak_arrow_heads.links.new(group_003_5.outputs[6], group_18.inputs[0])
			#extrude_mesh.Mesh -> reroute_10.Input
			_tweak_arrow_heads.links.new(extrude_mesh.outputs[0], reroute_10.inputs[0])
			#group_input_001_6.Rounded -> switch_10.Switch
			_tweak_arrow_heads.links.new(group_input_001_6.outputs[1], switch_10.inputs[0])
			#reroute_006_1.Output -> reroute_003_7.Input
			_tweak_arrow_heads.links.new(reroute_006_1.outputs[0], reroute_003_7.inputs[0])
			#reroute_003_7.Output -> reroute_004_3.Input
			_tweak_arrow_heads.links.new(reroute_003_7.outputs[0], reroute_004_3.inputs[0])
			#group_input_52.Input -> reroute_005_1.Input
			_tweak_arrow_heads.links.new(group_input_52.outputs[2], reroute_005_1.inputs[0])
			#reroute_005_1.Output -> reroute_006_1.Input
			_tweak_arrow_heads.links.new(reroute_005_1.outputs[0], reroute_006_1.inputs[0])
			#extrude_mesh.Top -> reroute_002_6.Input
			_tweak_arrow_heads.links.new(extrude_mesh.outputs[1], reroute_002_6.inputs[0])
			return _tweak_arrow_heads

		_tweak_arrow_heads = _tweak_arrow_heads_node_group()

		#initialize _ca_to_sheet node group
		def _ca_to_sheet_node_group():
			_ca_to_sheet = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".CA to sheet")

			_ca_to_sheet.color_tag = 'NONE'
			_ca_to_sheet.description = ""


			#_ca_to_sheet interface
			#Socket Geometry
			geometry_socket_10 = _ca_to_sheet.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			geometry_socket_10.attribute_domain = 'POINT'

			#Socket Curve
			curve_socket_4 = _ca_to_sheet.interface.new_socket(name = "Curve", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			curve_socket_4.attribute_domain = 'POINT'

			#Socket Profile Resolution
			profile_resolution_socket_1 = _ca_to_sheet.interface.new_socket(name = "Profile Resolution", in_out='INPUT', socket_type = 'NodeSocketInt')
			profile_resolution_socket_1.subtype = 'NONE'
			profile_resolution_socket_1.default_value = 4
			profile_resolution_socket_1.min_value = 3
			profile_resolution_socket_1.max_value = 512
			profile_resolution_socket_1.attribute_domain = 'POINT'

			#Socket Thickness
			thickness_socket_1 = _ca_to_sheet.interface.new_socket(name = "Thickness", in_out='INPUT', socket_type = 'NodeSocketFloat')
			thickness_socket_1.subtype = 'NONE'
			thickness_socket_1.default_value = 2.3399999141693115
			thickness_socket_1.min_value = -10000.0
			thickness_socket_1.max_value = 10000.0
			thickness_socket_1.attribute_domain = 'POINT'

			#Socket Width
			width_socket_1 = _ca_to_sheet.interface.new_socket(name = "Width", in_out='INPUT', socket_type = 'NodeSocketFloat')
			width_socket_1.subtype = 'NONE'
			width_socket_1.default_value = 0.5600000023841858
			width_socket_1.min_value = -10000.0
			width_socket_1.max_value = 10000.0
			width_socket_1.attribute_domain = 'POINT'

			#Socket Subdivisions
			subdivisions_socket_2 = _ca_to_sheet.interface.new_socket(name = "Subdivisions", in_out='INPUT', socket_type = 'NodeSocketInt')
			subdivisions_socket_2.subtype = 'NONE'
			subdivisions_socket_2.default_value = 6
			subdivisions_socket_2.min_value = 1
			subdivisions_socket_2.max_value = 2147483647
			subdivisions_socket_2.attribute_domain = 'POINT'

			#Socket Rounded
			rounded_socket_1 = _ca_to_sheet.interface.new_socket(name = "Rounded", in_out='INPUT', socket_type = 'NodeSocketBool')
			rounded_socket_1.attribute_domain = 'POINT'

			#Socket Arrows
			arrows_socket = _ca_to_sheet.interface.new_socket(name = "Arrows", in_out='INPUT', socket_type = 'NodeSocketBool')
			arrows_socket.attribute_domain = 'POINT'


			#initialize _ca_to_sheet nodes
			#node Group Output
			group_output_53 = _ca_to_sheet.nodes.new("NodeGroupOutput")
			group_output_53.name = "Group Output"
			group_output_53.is_active_output = True

			#node Group Input
			group_input_53 = _ca_to_sheet.nodes.new("NodeGroupInput")
			group_input_53.name = "Group Input"

			#node Combine XYZ.003
			combine_xyz_003 = _ca_to_sheet.nodes.new("ShaderNodeCombineXYZ")
			combine_xyz_003.name = "Combine XYZ.003"
			#Z
			combine_xyz_003.inputs[2].default_value = 0.0

			#node Group.032
			group_032 = _ca_to_sheet.nodes.new("GeometryNodeGroup")
			group_032.name = "Group.032"
			group_032.node_tree = curve_custom_profile
			#Socket_8
			group_032.inputs[2].default_value = 'Custom Profile'
			#Input_13
			group_032.inputs[7].default_value = 1.0
			#Input_14
			group_032.inputs[8].default_value = 0.0

			#node Group.035
			group_035 = _ca_to_sheet.nodes.new("GeometryNodeGroup")
			group_035.name = "Group.035"
			group_035.node_tree = curve_split_splines
			#Socket_4
			group_035.inputs[2].default_value = 'Free'
			#Socket_2
			group_035.inputs[3].default_value = 0
			#Socket_7
			group_035.inputs[4].default_value = 'Split Distance'
			#Socket_6
			group_035.inputs[5].default_value = 0.05000000074505806
			#Socket_9
			group_035.inputs[6].default_value = (0.0, 0.0, 0.0)
			#Socket_16
			group_035.inputs[7].default_value = 0.0
			#Socket_17
			group_035.inputs[8].default_value = 'Poly'
			#Socket_18
			group_035.inputs[9].default_value = 12

			#node Group.042
			group_042 = _ca_to_sheet.nodes.new("GeometryNodeGroup")
			group_042.name = "Group.042"
			group_042.node_tree = is_sheet
			#Socket_1
			group_042.inputs[0].default_value = True
			#Socket_3
			group_042.inputs[1].default_value = False

			#node Math.008
			math_008 = _ca_to_sheet.nodes.new("ShaderNodeMath")
			math_008.name = "Math.008"
			math_008.operation = 'MULTIPLY'
			math_008.use_clamp = False
			#Value_001
			math_008.inputs[1].default_value = 3.141590118408203

			#node Index.001
			index_001 = _ca_to_sheet.nodes.new("GeometryNodeInputIndex")
			index_001.name = "Index.001"

			#node Math.011
			math_011 = _ca_to_sheet.nodes.new("ShaderNodeMath")
			math_011.name = "Math.011"
			math_011.operation = 'WRAP'
			math_011.use_clamp = False
			#Value_001
			math_011.inputs[1].default_value = 2.0
			#Value_002
			math_011.inputs[2].default_value = 0.0

			#node Set Spline Type.002
			set_spline_type_002 = _ca_to_sheet.nodes.new("GeometryNodeCurveSplineType")
			set_spline_type_002.name = "Set Spline Type.002"
			set_spline_type_002.spline_type = 'BEZIER'
			#Selection
			set_spline_type_002.inputs[1].default_value = True

			#node Set Handle Type.001
			set_handle_type_001_1 = _ca_to_sheet.nodes.new("GeometryNodeCurveSetHandles")
			set_handle_type_001_1.name = "Set Handle Type.001"
			set_handle_type_001_1.handle_type = 'AUTO'
			set_handle_type_001_1.mode = {'LEFT', 'RIGHT'}
			#Selection
			set_handle_type_001_1.inputs[1].default_value = True

			#node Set Curve Normal.003
			set_curve_normal_003 = _ca_to_sheet.nodes.new("GeometryNodeSetCurveNormal")
			set_curve_normal_003.name = "Set Curve Normal.003"
			set_curve_normal_003.mode = 'FREE'
			#Selection
			set_curve_normal_003.inputs[1].default_value = True

			#node Rotate Vector
			rotate_vector = _ca_to_sheet.nodes.new("FunctionNodeRotateVector")
			rotate_vector.name = "Rotate Vector"

			#node Normal.005
			normal_005 = _ca_to_sheet.nodes.new("GeometryNodeInputNormal")
			normal_005.name = "Normal.005"

			#node Axis Angle to Rotation.001
			axis_angle_to_rotation_001 = _ca_to_sheet.nodes.new("FunctionNodeAxisAngleToRotation")
			axis_angle_to_rotation_001.name = "Axis Angle to Rotation.001"

			#node Curve Tangent
			curve_tangent = _ca_to_sheet.nodes.new("GeometryNodeInputTangent")
			curve_tangent.name = "Curve Tangent"

			#node Math.002
			math_002_2 = _ca_to_sheet.nodes.new("ShaderNodeMath")
			math_002_2.name = "Math.002"
			math_002_2.operation = 'ADD'
			math_002_2.use_clamp = False

			#node Math.007
			math_007 = _ca_to_sheet.nodes.new("ShaderNodeMath")
			math_007.name = "Math.007"
			math_007.operation = 'ADD'
			math_007.use_clamp = False

			#node Blur Attribute.002
			blur_attribute_002 = _ca_to_sheet.nodes.new("GeometryNodeBlurAttribute")
			blur_attribute_002.name = "Blur Attribute.002"
			blur_attribute_002.data_type = 'FLOAT_VECTOR'
			#Iterations
			blur_attribute_002.inputs[1].default_value = 1
			#Weight
			blur_attribute_002.inputs[2].default_value = 1.0

			#node Math.009
			math_009 = _ca_to_sheet.nodes.new("ShaderNodeMath")
			math_009.name = "Math.009"
			math_009.operation = 'RADIANS'
			math_009.use_clamp = False
			#Value
			math_009.inputs[0].default_value = 30.0

			#node Group.002
			group_002_11 = _ca_to_sheet.nodes.new("GeometryNodeGroup")
			group_002_11.name = "Group.002"
			group_002_11.node_tree = curve_offset_dot
			#Socket_1
			group_002_11.inputs[0].default_value = (0.0, 0.0, 0.0)
			#Socket_4
			group_002_11.inputs[1].default_value = 'Greater Than'
			#Socket_3
			group_002_11.inputs[2].default_value = -0.30000001192092896
			#Socket_6
			group_002_11.inputs[3].default_value = 1
			#Socket_8
			group_002_11.inputs[4].default_value = (0.0, 0.0, 1.0)
			#Socket_7
			group_002_11.inputs[5].default_value = 3.1415927410125732

			#node Set Position.002
			set_position_002_1 = _ca_to_sheet.nodes.new("GeometryNodeSetPosition")
			set_position_002_1.name = "Set Position.002"
			#Selection
			set_position_002_1.inputs[1].default_value = True
			#Position
			set_position_002_1.inputs[2].default_value = (0.0, 0.0, 0.0)

			#node Curve Tangent.001
			curve_tangent_001_1 = _ca_to_sheet.nodes.new("GeometryNodeInputTangent")
			curve_tangent_001_1.name = "Curve Tangent.001"

			#node Vector Math.002
			vector_math_002_2 = _ca_to_sheet.nodes.new("ShaderNodeVectorMath")
			vector_math_002_2.name = "Vector Math.002"
			vector_math_002_2.operation = 'SCALE'

			#node Math
			math_14 = _ca_to_sheet.nodes.new("ShaderNodeMath")
			math_14.name = "Math"
			math_14.operation = 'MULTIPLY'
			math_14.use_clamp = False

			#node Group.013
			group_013_1 = _ca_to_sheet.nodes.new("GeometryNodeGroup")
			group_013_1.name = "Group.013"
			group_013_1.node_tree = curve_endpoint_values
			#Socket_5
			group_013_1.inputs[0].default_value = 1
			#Socket_1
			group_013_1.inputs[1].default_value = -1
			#Socket_2
			group_013_1.inputs[2].default_value = 0
			#Socket_6
			group_013_1.inputs[3].default_value = 1
			#Socket_3
			group_013_1.inputs[4].default_value = 1

			#node Group.020
			group_020 = _ca_to_sheet.nodes.new("GeometryNodeGroup")
			group_020.name = "Group.020"
			group_020.node_tree = mn_units
			#Input_1
			group_020.inputs[0].default_value = 0.20000000298023224

			#node Frame
			frame_4 = _ca_to_sheet.nodes.new("NodeFrame")
			frame_4.label = "alternating flipping of normal to smoothen out sheets"
			frame_4.name = "Frame"
			frame_4.label_size = 20
			frame_4.shrink = True

			#node Group Input.001
			group_input_001_7 = _ca_to_sheet.nodes.new("NodeGroupInput")
			group_input_001_7.name = "Group Input.001"
			group_input_001_7.outputs[0].hide = True
			group_input_001_7.outputs[2].hide = True
			group_input_001_7.outputs[3].hide = True
			group_input_001_7.outputs[4].hide = True
			group_input_001_7.outputs[5].hide = True
			group_input_001_7.outputs[6].hide = True
			group_input_001_7.outputs[7].hide = True

			#node Capture Attribute
			capture_attribute_6 = _ca_to_sheet.nodes.new("GeometryNodeCaptureAttribute")
			capture_attribute_6.name = "Capture Attribute"
			capture_attribute_6.active_index = 1
			capture_attribute_6.capture_items.clear()
			capture_attribute_6.capture_items.new('FLOAT', "Resolution")
			capture_attribute_6.capture_items["Resolution"].data_type = 'INT'
			capture_attribute_6.capture_items.new('FLOAT', "Thickness")
			capture_attribute_6.capture_items["Thickness"].data_type = 'FLOAT'
			capture_attribute_6.capture_items.new('FLOAT', "Width")
			capture_attribute_6.capture_items["Width"].data_type = 'FLOAT'
			capture_attribute_6.domain = 'POINT'

			#node Capture Attribute.001
			capture_attribute_001_3 = _ca_to_sheet.nodes.new("GeometryNodeCaptureAttribute")
			capture_attribute_001_3.name = "Capture Attribute.001"
			capture_attribute_001_3.active_index = 0
			capture_attribute_001_3.capture_items.clear()
			capture_attribute_001_3.capture_items.new('FLOAT', "Arrow Mask")
			capture_attribute_001_3.capture_items["Arrow Mask"].data_type = 'FLOAT'
			capture_attribute_001_3.domain = 'POINT'

			#node Spline Parameter
			spline_parameter_1 = _ca_to_sheet.nodes.new("GeometryNodeSplineParameter")
			spline_parameter_1.name = "Spline Parameter"
			spline_parameter_1.outputs[0].hide = True
			spline_parameter_1.outputs[1].hide = True

			#node Normal.001
			normal_001 = _ca_to_sheet.nodes.new("GeometryNodeInputNormal")
			normal_001.name = "Normal.001"

			#node Curve Tangent.002
			curve_tangent_002 = _ca_to_sheet.nodes.new("GeometryNodeInputTangent")
			curve_tangent_002.name = "Curve Tangent.002"

			#node Spline Length
			spline_length_1 = _ca_to_sheet.nodes.new("GeometryNodeSplineLength")
			spline_length_1.name = "Spline Length"

			#node Math.003
			math_003_1 = _ca_to_sheet.nodes.new("ShaderNodeMath")
			math_003_1.name = "Math.003"
			math_003_1.hide = True
			math_003_1.operation = 'SUBTRACT'
			math_003_1.use_clamp = False
			#Value_001
			math_003_1.inputs[1].default_value = 1.0

			#node Math.004
			math_004 = _ca_to_sheet.nodes.new("ShaderNodeMath")
			math_004.name = "Math.004"
			math_004.operation = 'SUBTRACT'
			math_004.use_clamp = False

			#node Math.006
			math_006 = _ca_to_sheet.nodes.new("ShaderNodeMath")
			math_006.name = "Math.006"
			math_006.operation = 'ADD'
			math_006.use_clamp = False

			#node Map Range.001
			map_range_001 = _ca_to_sheet.nodes.new("ShaderNodeMapRange")
			map_range_001.name = "Map Range.001"
			map_range_001.clamp = True
			map_range_001.data_type = 'FLOAT'
			map_range_001.interpolation_type = 'LINEAR'
			#From Min
			map_range_001.inputs[1].default_value = 0.0
			#From Max
			map_range_001.inputs[2].default_value = 1.0
			#To Max
			map_range_001.inputs[4].default_value = -0.1600000262260437

			#node Math.005
			math_005 = _ca_to_sheet.nodes.new("ShaderNodeMath")
			math_005.name = "Math.005"
			math_005.operation = 'MULTIPLY'
			math_005.use_clamp = False
			#Value_001
			math_005.inputs[1].default_value = -1.0

			#node Math.012
			math_012_1 = _ca_to_sheet.nodes.new("ShaderNodeMath")
			math_012_1.name = "Math.012"
			math_012_1.operation = 'MAXIMUM'
			math_012_1.use_clamp = False
			#Value_001
			math_012_1.inputs[1].default_value = 1.0

			#node Group Input.002
			group_input_002_3 = _ca_to_sheet.nodes.new("NodeGroupInput")
			group_input_002_3.name = "Group Input.002"

			#node Switch.001
			switch_001_5 = _ca_to_sheet.nodes.new("GeometryNodeSwitch")
			switch_001_5.name = "Switch.001"
			switch_001_5.input_type = 'GEOMETRY'

			#node Group Input.003
			group_input_003_2 = _ca_to_sheet.nodes.new("NodeGroupInput")
			group_input_003_2.name = "Group Input.003"
			group_input_003_2.outputs[0].hide = True
			group_input_003_2.outputs[1].hide = True
			group_input_003_2.outputs[2].hide = True
			group_input_003_2.outputs[3].hide = True
			group_input_003_2.outputs[4].hide = True
			group_input_003_2.outputs[7].hide = True

			#node Switch.002
			switch_002_3 = _ca_to_sheet.nodes.new("GeometryNodeSwitch")
			switch_002_3.name = "Switch.002"
			switch_002_3.input_type = 'FLOAT'
			#False
			switch_002_3.inputs[1].default_value = 1.0

			#node Group.003
			group_003_6 = _ca_to_sheet.nodes.new("GeometryNodeGroup")
			group_003_6.name = "Group.003"
			group_003_6.node_tree = _tweak_arrow_heads

			#node Frame.001
			frame_001_2 = _ca_to_sheet.nodes.new("NodeFrame")
			frame_001_2.label = "Adjustment for arrowheads"
			frame_001_2.name = "Frame.001"
			frame_001_2.label_size = 20
			frame_001_2.shrink = True

			#node Group.045
			group_045 = _ca_to_sheet.nodes.new("GeometryNodeGroup")
			group_045.name = "Group.045"
			group_045.node_tree = curve_rotation
			#Socket_1
			group_045.inputs[0].default_value = (0.0, 0.0, 1.0)

			#node Store Named Attribute
			store_named_attribute_2 = _ca_to_sheet.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_2.name = "Store Named Attribute"
			store_named_attribute_2.data_type = 'FLOAT_VECTOR'
			store_named_attribute_2.domain = 'POINT'
			#Selection
			store_named_attribute_2.inputs[1].default_value = True
			#Name
			store_named_attribute_2.inputs[2].default_value = "tmp_curve_normal"

			#node Store Named Attribute.001
			store_named_attribute_001 = _ca_to_sheet.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_001.name = "Store Named Attribute.001"
			store_named_attribute_001.data_type = 'FLOAT_VECTOR'
			store_named_attribute_001.domain = 'POINT'
			#Selection
			store_named_attribute_001.inputs[1].default_value = True
			#Name
			store_named_attribute_001.inputs[2].default_value = "tmp_curve_tangent"

			#node Reroute.001
			reroute_001_9 = _ca_to_sheet.nodes.new("NodeReroute")
			reroute_001_9.name = "Reroute.001"
			#node Reroute.002
			reroute_002_7 = _ca_to_sheet.nodes.new("NodeReroute")
			reroute_002_7.name = "Reroute.002"
			#node Boolean Math
			boolean_math_9 = _ca_to_sheet.nodes.new("FunctionNodeBooleanMath")
			boolean_math_9.name = "Boolean Math"
			boolean_math_9.operation = 'NIMPLY'

			#node Group Input.004
			group_input_004_1 = _ca_to_sheet.nodes.new("NodeGroupInput")
			group_input_004_1.name = "Group Input.004"
			group_input_004_1.outputs[0].hide = True
			group_input_004_1.outputs[1].hide = True
			group_input_004_1.outputs[2].hide = True
			group_input_004_1.outputs[3].hide = True
			group_input_004_1.outputs[4].hide = True
			group_input_004_1.outputs[6].hide = True
			group_input_004_1.outputs[7].hide = True

			#node Switch
			switch_11 = _ca_to_sheet.nodes.new("GeometryNodeSwitch")
			switch_11.name = "Switch"
			switch_11.input_type = 'FLOAT'

			#node Reroute
			reroute_11 = _ca_to_sheet.nodes.new("NodeReroute")
			reroute_11.name = "Reroute"


			#Set parents
			math_008.parent = frame_4
			index_001.parent = frame_4
			math_011.parent = frame_4
			rotate_vector.parent = frame_4
			normal_005.parent = frame_4
			axis_angle_to_rotation_001.parent = frame_4
			curve_tangent.parent = frame_4
			math_002_2.parent = frame_4
			math_007.parent = frame_4
			blur_attribute_002.parent = frame_4
			math_009.parent = frame_4
			group_002_11.parent = frame_4
			map_range_001.parent = frame_001_2
			math_005.parent = frame_001_2
			group_input_003_2.parent = frame_001_2
			switch_002_3.parent = frame_001_2
			reroute_001_9.parent = frame_001_2

			#Set locations
			group_output_53.location = (2720.0, 340.0)
			group_input_53.location = (-775.7479858398438, 160.0)
			combine_xyz_003.location = (1840.0, 160.0)
			group_032.location = (2040.0, 280.0)
			group_035.location = (69.29638671875, 240.0491943359375)
			group_042.location = (-120.0, 260.0)
			math_008.location = (-700.0, -80.0)
			index_001.location = (-1200.0, -80.0)
			math_011.location = (-860.0, -80.0)
			set_spline_type_002.location = (529.2964477539062, 240.0491943359375)
			set_handle_type_001_1.location = (689.2964477539062, 240.0491943359375)
			set_curve_normal_003.location = (-515.748046875, 200.0)
			rotate_vector.location = (-380.0, 100.0)
			normal_005.location = (-540.0, 100.0)
			axis_angle_to_rotation_001.location = (-540.0, 40.0)
			curve_tangent.location = (-700.0, 40.0)
			math_002_2.location = (-1020.0, -80.0)
			math_007.location = (-540.0, -80.0)
			blur_attribute_002.location = (-220.0, 100.0)
			math_009.location = (-700.0, -260.0)
			group_002_11.location = (-1200.0, -160.0)
			set_position_002_1.location = (349.2964172363281, 232.809814453125)
			curve_tangent_001_1.location = (220.0, -80.0)
			vector_math_002_2.location = (380.0, -40.0)
			math_14.location = (220.0, -140.0)
			group_013_1.location = (60.0, -140.0)
			group_020.location = (220.0, -300.0)
			frame_4.location = (-550.0, -260.0)
			group_input_001_7.location = (1840.0, 20.0)
			capture_attribute_6.location = (-335.748046875, 160.0)
			capture_attribute_001_3.location = (1040.0, 260.0)
			spline_parameter_1.location = (220.0, 340.0)
			normal_001.location = (1340.0, 100.0)
			curve_tangent_002.location = (1520.0, 100.0)
			spline_length_1.location = (220.0, 420.0)
			math_003_1.location = (380.0, 420.0)
			math_004.location = (700.0, 420.0)
			math_006.location = (1680.0, -140.0)
			map_range_001.location = (1505.0, -242.0)
			math_005.location = (1325.0, -242.0)
			math_012_1.location = (540.0, 420.0)
			group_input_002_3.location = (2156.098388671875, 602.7443237304688)
			switch_001_5.location = (2500.0, 340.0)
			group_input_003_2.location = (1285.0, -82.0)
			switch_002_3.location = (1505.0, -82.0)
			group_003_6.location = (2442.931640625, 180.0)
			frame_001_2.location = (-195.0, -208.0)
			group_045.location = (1840.0, 240.0)
			store_named_attribute_2.location = (1340.0, 300.0)
			store_named_attribute_001.location = (1520.0, 300.0)
			reroute_001_9.location = (1465.0, -28.0)
			reroute_002_7.location = (880.0, -80.0)
			boolean_math_9.location = (2383.22998046875, 483.77313232421875)
			group_input_004_1.location = (1520.0, 20.0)
			switch_11.location = (1680.0, 20.0)
			reroute_11.location = (1420.0, -80.0)

			#Set dimensions
			group_output_53.width, group_output_53.height = 140.0, 100.0
			group_input_53.width, group_input_53.height = 140.0, 100.0
			combine_xyz_003.width, combine_xyz_003.height = 140.0, 100.0
			group_032.width, group_032.height = 244.548095703125, 100.0
			group_035.width, group_035.height = 140.0, 100.0
			group_042.width, group_042.height = 140.0, 100.0
			math_008.width, math_008.height = 140.0, 100.0
			index_001.width, index_001.height = 140.0, 100.0
			math_011.width, math_011.height = 140.0, 100.0
			set_spline_type_002.width, set_spline_type_002.height = 140.0, 100.0
			set_handle_type_001_1.width, set_handle_type_001_1.height = 140.0, 100.0
			set_curve_normal_003.width, set_curve_normal_003.height = 140.0, 100.0
			rotate_vector.width, rotate_vector.height = 140.0, 100.0
			normal_005.width, normal_005.height = 140.0, 100.0
			axis_angle_to_rotation_001.width, axis_angle_to_rotation_001.height = 140.0, 100.0
			curve_tangent.width, curve_tangent.height = 140.0, 100.0
			math_002_2.width, math_002_2.height = 140.0, 100.0
			math_007.width, math_007.height = 140.0, 100.0
			blur_attribute_002.width, blur_attribute_002.height = 140.0, 100.0
			math_009.width, math_009.height = 140.0, 100.0
			group_002_11.width, group_002_11.height = 140.0, 100.0
			set_position_002_1.width, set_position_002_1.height = 140.0, 100.0
			curve_tangent_001_1.width, curve_tangent_001_1.height = 140.0, 100.0
			vector_math_002_2.width, vector_math_002_2.height = 140.0, 100.0
			math_14.width, math_14.height = 140.0, 100.0
			group_013_1.width, group_013_1.height = 140.0, 100.0
			group_020.width, group_020.height = 140.0, 100.0
			frame_4.width, frame_4.height = 1180.0, 555.5999755859375
			group_input_001_7.width, group_input_001_7.height = 140.0, 100.0
			capture_attribute_6.width, capture_attribute_6.height = 140.0, 100.0
			capture_attribute_001_3.width, capture_attribute_001_3.height = 140.0, 100.0
			spline_parameter_1.width, spline_parameter_1.height = 140.0, 100.0
			normal_001.width, normal_001.height = 140.0, 100.0
			curve_tangent_002.width, curve_tangent_002.height = 140.0, 100.0
			spline_length_1.width, spline_length_1.height = 140.0, 100.0
			math_003_1.width, math_003_1.height = 140.0, 100.0
			math_004.width, math_004.height = 140.0, 100.0
			math_006.width, math_006.height = 140.0, 100.0
			map_range_001.width, map_range_001.height = 140.0, 100.0
			math_005.width, math_005.height = 140.0, 100.0
			math_012_1.width, math_012_1.height = 140.0, 100.0
			group_input_002_3.width, group_input_002_3.height = 140.0, 100.0
			switch_001_5.width, switch_001_5.height = 140.0, 100.0
			group_input_003_2.width, group_input_003_2.height = 140.0, 100.0
			switch_002_3.width, switch_002_3.height = 140.0, 100.0
			group_003_6.width, group_003_6.height = 197.068359375, 100.0
			frame_001_2.width, frame_001_2.height = 420.0, 529.199951171875
			group_045.width, group_045.height = 140.0, 100.0
			store_named_attribute_2.width, store_named_attribute_2.height = 140.0, 100.0
			store_named_attribute_001.width, store_named_attribute_001.height = 140.0, 100.0
			reroute_001_9.width, reroute_001_9.height = 16.0, 100.0
			reroute_002_7.width, reroute_002_7.height = 16.0, 100.0
			boolean_math_9.width, boolean_math_9.height = 140.0, 100.0
			group_input_004_1.width, group_input_004_1.height = 140.0, 100.0
			switch_11.width, switch_11.height = 140.0, 100.0
			reroute_11.width, reroute_11.height = 16.0, 100.0

			#initialize _ca_to_sheet links
			#set_spline_type_002.Curve -> set_handle_type_001_1.Curve
			_ca_to_sheet.links.new(set_spline_type_002.outputs[0], set_handle_type_001_1.inputs[0])
			#blur_attribute_002.Value -> set_curve_normal_003.Normal
			_ca_to_sheet.links.new(blur_attribute_002.outputs[0], set_curve_normal_003.inputs[2])
			#vector_math_002_2.Vector -> set_position_002_1.Offset
			_ca_to_sheet.links.new(vector_math_002_2.outputs[0], set_position_002_1.inputs[3])
			#group_020.Angstrom -> math_14.Value
			_ca_to_sheet.links.new(group_020.outputs[0], math_14.inputs[1])
			#rotate_vector.Vector -> blur_attribute_002.Value
			_ca_to_sheet.links.new(rotate_vector.outputs[0], blur_attribute_002.inputs[0])
			#group_013_1.Value -> math_14.Value
			_ca_to_sheet.links.new(group_013_1.outputs[0], math_14.inputs[0])
			#math_007.Value -> axis_angle_to_rotation_001.Angle
			_ca_to_sheet.links.new(math_007.outputs[0], axis_angle_to_rotation_001.inputs[1])
			#math_14.Value -> vector_math_002_2.Scale
			_ca_to_sheet.links.new(math_14.outputs[0], vector_math_002_2.inputs[3])
			#capture_attribute_6.Geometry -> group_035.Curve
			_ca_to_sheet.links.new(capture_attribute_6.outputs[0], group_035.inputs[0])
			#store_named_attribute_001.Geometry -> group_032.Curve
			_ca_to_sheet.links.new(store_named_attribute_001.outputs[0], group_032.inputs[0])
			#curve_tangent_001_1.Tangent -> vector_math_002_2.Vector
			_ca_to_sheet.links.new(curve_tangent_001_1.outputs[0], vector_math_002_2.inputs[0])
			#math_002_2.Value -> math_011.Value
			_ca_to_sheet.links.new(math_002_2.outputs[0], math_011.inputs[0])
			#group_035.Curve -> set_position_002_1.Geometry
			_ca_to_sheet.links.new(group_035.outputs[0], set_position_002_1.inputs[0])
			#group_042.Selection -> group_035.Selection
			_ca_to_sheet.links.new(group_042.outputs[0], group_035.inputs[1])
			#group_002_11.Leading -> math_002_2.Value
			_ca_to_sheet.links.new(group_002_11.outputs[1], math_002_2.inputs[1])
			#curve_tangent.Tangent -> axis_angle_to_rotation_001.Axis
			_ca_to_sheet.links.new(curve_tangent.outputs[0], axis_angle_to_rotation_001.inputs[0])
			#axis_angle_to_rotation_001.Rotation -> rotate_vector.Rotation
			_ca_to_sheet.links.new(axis_angle_to_rotation_001.outputs[0], rotate_vector.inputs[1])
			#math_011.Value -> math_008.Value
			_ca_to_sheet.links.new(math_011.outputs[0], math_008.inputs[0])
			#set_position_002_1.Geometry -> set_spline_type_002.Curve
			_ca_to_sheet.links.new(set_position_002_1.outputs[0], set_spline_type_002.inputs[0])
			#combine_xyz_003.Vector -> group_032.Profile Scale
			_ca_to_sheet.links.new(combine_xyz_003.outputs[0], group_032.inputs[4])
			#normal_005.Normal -> rotate_vector.Vector
			_ca_to_sheet.links.new(normal_005.outputs[0], rotate_vector.inputs[0])
			#index_001.Index -> math_002_2.Value
			_ca_to_sheet.links.new(index_001.outputs[0], math_002_2.inputs[0])
			#math_008.Value -> math_007.Value
			_ca_to_sheet.links.new(math_008.outputs[0], math_007.inputs[0])
			#math_009.Value -> math_007.Value
			_ca_to_sheet.links.new(math_009.outputs[0], math_007.inputs[1])
			#group_input_53.Curve -> set_curve_normal_003.Curve
			_ca_to_sheet.links.new(group_input_53.outputs[0], set_curve_normal_003.inputs[0])
			#group_input_001_7.Profile Resolution -> group_032.Profile Resolution
			_ca_to_sheet.links.new(group_input_001_7.outputs[1], group_032.inputs[6])
			#set_curve_normal_003.Curve -> capture_attribute_6.Geometry
			_ca_to_sheet.links.new(set_curve_normal_003.outputs[0], capture_attribute_6.inputs[0])
			#group_input_53.Subdivisions -> capture_attribute_6.Resolution
			_ca_to_sheet.links.new(group_input_53.outputs[4], capture_attribute_6.inputs[1])
			#capture_attribute_6.Resolution -> group_032.Subdivisions
			_ca_to_sheet.links.new(capture_attribute_6.outputs[1], group_032.inputs[1])
			#group_input_53.Thickness -> capture_attribute_6.Thickness
			_ca_to_sheet.links.new(group_input_53.outputs[2], capture_attribute_6.inputs[2])
			#group_input_53.Width -> capture_attribute_6.Width
			_ca_to_sheet.links.new(group_input_53.outputs[3], capture_attribute_6.inputs[3])
			#capture_attribute_6.Thickness -> combine_xyz_003.X
			_ca_to_sheet.links.new(capture_attribute_6.outputs[2], combine_xyz_003.inputs[0])
			#set_handle_type_001_1.Curve -> capture_attribute_001_3.Geometry
			_ca_to_sheet.links.new(set_handle_type_001_1.outputs[0], capture_attribute_001_3.inputs[0])
			#spline_length_1.Point Count -> math_003_1.Value
			_ca_to_sheet.links.new(spline_length_1.outputs[1], math_003_1.inputs[0])
			#spline_parameter_1.Index -> math_004.Value
			_ca_to_sheet.links.new(spline_parameter_1.outputs[2], math_004.inputs[1])
			#math_004.Value -> capture_attribute_001_3.Arrow Mask
			_ca_to_sheet.links.new(math_004.outputs[0], capture_attribute_001_3.inputs[1])
			#reroute_11.Output -> math_006.Value
			_ca_to_sheet.links.new(reroute_11.outputs[0], math_006.inputs[0])
			#reroute_001_9.Output -> map_range_001.Value
			_ca_to_sheet.links.new(reroute_001_9.outputs[0], map_range_001.inputs[0])
			#reroute_002_7.Output -> math_005.Value
			_ca_to_sheet.links.new(reroute_002_7.outputs[0], math_005.inputs[0])
			#math_005.Value -> map_range_001.To Min
			_ca_to_sheet.links.new(math_005.outputs[0], map_range_001.inputs[3])
			#math_003_1.Value -> math_012_1.Value
			_ca_to_sheet.links.new(math_003_1.outputs[0], math_012_1.inputs[0])
			#math_012_1.Value -> math_004.Value
			_ca_to_sheet.links.new(math_012_1.outputs[0], math_004.inputs[0])
			#group_003_6.Output -> switch_001_5.True
			_ca_to_sheet.links.new(group_003_6.outputs[0], switch_001_5.inputs[2])
			#switch_001_5.Output -> group_output_53.Geometry
			_ca_to_sheet.links.new(switch_001_5.outputs[0], group_output_53.inputs[0])
			#map_range_001.Result -> switch_002_3.True
			_ca_to_sheet.links.new(map_range_001.outputs[0], switch_002_3.inputs[2])
			#switch_002_3.Output -> math_006.Value
			_ca_to_sheet.links.new(switch_002_3.outputs[0], math_006.inputs[1])
			#group_032.Geometry -> switch_001_5.False
			_ca_to_sheet.links.new(group_032.outputs[0], switch_001_5.inputs[1])
			#reroute_001_9.Output -> group_003_6.Input
			_ca_to_sheet.links.new(reroute_001_9.outputs[0], group_003_6.inputs[2])
			#group_032.Geometry -> group_003_6.Geometry
			_ca_to_sheet.links.new(group_032.outputs[0], group_003_6.inputs[0])
			#group_input_002_3.Rounded -> group_003_6.Rounded
			_ca_to_sheet.links.new(group_input_002_3.outputs[5], group_003_6.inputs[1])
			#group_045.Rotation -> group_032.Profile Rotation
			_ca_to_sheet.links.new(group_045.outputs[0], group_032.inputs[3])
			#capture_attribute_001_3.Geometry -> store_named_attribute_2.Geometry
			_ca_to_sheet.links.new(capture_attribute_001_3.outputs[0], store_named_attribute_2.inputs[0])
			#normal_001.Normal -> store_named_attribute_2.Value
			_ca_to_sheet.links.new(normal_001.outputs[0], store_named_attribute_2.inputs[3])
			#store_named_attribute_2.Geometry -> store_named_attribute_001.Geometry
			_ca_to_sheet.links.new(store_named_attribute_2.outputs[0], store_named_attribute_001.inputs[0])
			#curve_tangent_002.Tangent -> store_named_attribute_001.Value
			_ca_to_sheet.links.new(curve_tangent_002.outputs[0], store_named_attribute_001.inputs[3])
			#capture_attribute_001_3.Arrow Mask -> reroute_001_9.Input
			_ca_to_sheet.links.new(capture_attribute_001_3.outputs[1], reroute_001_9.inputs[0])
			#capture_attribute_6.Width -> reroute_002_7.Input
			_ca_to_sheet.links.new(capture_attribute_6.outputs[3], reroute_002_7.inputs[0])
			#group_input_002_3.Arrows -> boolean_math_9.Boolean
			_ca_to_sheet.links.new(group_input_002_3.outputs[6], boolean_math_9.inputs[0])
			#group_input_002_3.Rounded -> boolean_math_9.Boolean
			_ca_to_sheet.links.new(group_input_002_3.outputs[5], boolean_math_9.inputs[1])
			#boolean_math_9.Boolean -> switch_001_5.Switch
			_ca_to_sheet.links.new(boolean_math_9.outputs[0], switch_001_5.inputs[0])
			#group_input_003_2.Arrows -> switch_002_3.Switch
			_ca_to_sheet.links.new(group_input_003_2.outputs[6], switch_002_3.inputs[0])
			#group_input_004_1.Rounded -> switch_11.Switch
			_ca_to_sheet.links.new(group_input_004_1.outputs[5], switch_11.inputs[0])
			#math_006.Value -> switch_11.False
			_ca_to_sheet.links.new(math_006.outputs[0], switch_11.inputs[1])
			#switch_11.Output -> combine_xyz_003.Y
			_ca_to_sheet.links.new(switch_11.outputs[0], combine_xyz_003.inputs[1])
			#reroute_11.Output -> switch_11.True
			_ca_to_sheet.links.new(reroute_11.outputs[0], switch_11.inputs[2])
			#reroute_002_7.Output -> reroute_11.Input
			_ca_to_sheet.links.new(reroute_002_7.outputs[0], reroute_11.inputs[0])
			return _ca_to_sheet

		_ca_to_sheet = _ca_to_sheet_node_group()

		#initialize boolean_shrink node group
		def boolean_shrink_node_group():
			boolean_shrink = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Boolean Shrink")

			boolean_shrink.color_tag = 'CONVERTER'
			boolean_shrink.description = ""


			#boolean_shrink interface
			#Socket Boolean
			boolean_socket_7 = boolean_shrink.interface.new_socket(name = "Boolean", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			boolean_socket_7.attribute_domain = 'POINT'

			#Socket Boolean
			boolean_socket_8 = boolean_shrink.interface.new_socket(name = "Boolean", in_out='INPUT', socket_type = 'NodeSocketBool')
			boolean_socket_8.attribute_domain = 'POINT'
			boolean_socket_8.hide_value = True

			#Socket Shrink
			shrink_socket = boolean_shrink.interface.new_socket(name = "Shrink", in_out='INPUT', socket_type = 'NodeSocketInt')
			shrink_socket.subtype = 'NONE'
			shrink_socket.default_value = 0
			shrink_socket.min_value = -2147483647
			shrink_socket.max_value = 2147483647
			shrink_socket.attribute_domain = 'POINT'


			#initialize boolean_shrink nodes
			#node Group Output
			group_output_54 = boolean_shrink.nodes.new("NodeGroupOutput")
			group_output_54.name = "Group Output"
			group_output_54.is_active_output = True

			#node Group Input
			group_input_54 = boolean_shrink.nodes.new("NodeGroupInput")
			group_input_54.name = "Group Input"

			#node Group.016
			group_016_2 = boolean_shrink.nodes.new("GeometryNodeGroup")
			group_016_2.name = "Group.016"
			group_016_2.node_tree = offset_boolean
			#Socket_1
			group_016_2.inputs[0].default_value = 0

			#node Group.017
			group_017_2 = boolean_shrink.nodes.new("GeometryNodeGroup")
			group_017_2.name = "Group.017"
			group_017_2.node_tree = offset_boolean
			#Socket_1
			group_017_2.inputs[0].default_value = 0

			#node Boolean Math
			boolean_math_10 = boolean_shrink.nodes.new("FunctionNodeBooleanMath")
			boolean_math_10.name = "Boolean Math"
			boolean_math_10.operation = 'AND'

			#node Math
			math_15 = boolean_shrink.nodes.new("ShaderNodeMath")
			math_15.name = "Math"
			math_15.operation = 'MULTIPLY'
			math_15.use_clamp = False
			#Value_001
			math_15.inputs[1].default_value = -1.0

			#node Boolean Math.001
			boolean_math_001_7 = boolean_shrink.nodes.new("FunctionNodeBooleanMath")
			boolean_math_001_7.name = "Boolean Math.001"
			boolean_math_001_7.operation = 'AND'

			#node Reroute
			reroute_12 = boolean_shrink.nodes.new("NodeReroute")
			reroute_12.name = "Reroute"
			#node Reroute.001
			reroute_001_10 = boolean_shrink.nodes.new("NodeReroute")
			reroute_001_10.name = "Reroute.001"



			#Set locations
			group_output_54.location = (340.0, 80.0)
			group_input_54.location = (-640.0, 60.0)
			group_016_2.location = (-173.58670043945312, -14.669303894042969)
			group_017_2.location = (-180.0, -200.0)
			boolean_math_10.location = (-13.586694717407227, -14.669303894042969)
			math_15.location = (-360.0, -200.0)
			boolean_math_001_7.location = (159.99998474121094, 89.90420532226562)
			reroute_12.location = (-420.0, -140.0)
			reroute_001_10.location = (-300.0, 20.0)

			#Set dimensions
			group_output_54.width, group_output_54.height = 140.0, 100.0
			group_input_54.width, group_input_54.height = 140.0, 100.0
			group_016_2.width, group_016_2.height = 140.0, 100.0
			group_017_2.width, group_017_2.height = 140.0, 100.0
			boolean_math_10.width, boolean_math_10.height = 140.0, 100.0
			math_15.width, math_15.height = 140.0, 100.0
			boolean_math_001_7.width, boolean_math_001_7.height = 140.0, 100.0
			reroute_12.width, reroute_12.height = 16.0, 100.0
			reroute_001_10.width, reroute_001_10.height = 16.0, 100.0

			#initialize boolean_shrink links
			#group_016_2.Boolean -> boolean_math_10.Boolean
			boolean_shrink.links.new(group_016_2.outputs[0], boolean_math_10.inputs[0])
			#boolean_math_001_7.Boolean -> group_output_54.Boolean
			boolean_shrink.links.new(boolean_math_001_7.outputs[0], group_output_54.inputs[0])
			#group_017_2.Boolean -> boolean_math_10.Boolean
			boolean_shrink.links.new(group_017_2.outputs[0], boolean_math_10.inputs[1])
			#reroute_001_10.Output -> group_016_2.Boolean
			boolean_shrink.links.new(reroute_001_10.outputs[0], group_016_2.inputs[1])
			#reroute_001_10.Output -> group_017_2.Boolean
			boolean_shrink.links.new(reroute_001_10.outputs[0], group_017_2.inputs[1])
			#reroute_12.Output -> group_016_2.Offset
			boolean_shrink.links.new(reroute_12.outputs[0], group_016_2.inputs[2])
			#reroute_12.Output -> math_15.Value
			boolean_shrink.links.new(reroute_12.outputs[0], math_15.inputs[0])
			#math_15.Value -> group_017_2.Offset
			boolean_shrink.links.new(math_15.outputs[0], group_017_2.inputs[2])
			#boolean_math_10.Boolean -> boolean_math_001_7.Boolean
			boolean_shrink.links.new(boolean_math_10.outputs[0], boolean_math_001_7.inputs[1])
			#reroute_001_10.Output -> boolean_math_001_7.Boolean
			boolean_shrink.links.new(reroute_001_10.outputs[0], boolean_math_001_7.inputs[0])
			#group_input_54.Shrink -> reroute_12.Input
			boolean_shrink.links.new(group_input_54.outputs[1], reroute_12.inputs[0])
			#group_input_54.Boolean -> reroute_001_10.Input
			boolean_shrink.links.new(group_input_54.outputs[0], reroute_001_10.inputs[0])
			return boolean_shrink

		boolean_shrink = boolean_shrink_node_group()

		#initialize offset_rotation node group
		def offset_rotation_node_group():
			offset_rotation = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Offset Rotation")

			offset_rotation.color_tag = 'CONVERTER'
			offset_rotation.description = ""


			#offset_rotation interface
			#Socket Rotation
			rotation_socket_5 = offset_rotation.interface.new_socket(name = "Rotation", in_out='OUTPUT', socket_type = 'NodeSocketRotation')
			rotation_socket_5.attribute_domain = 'POINT'

			#Socket Index
			index_socket_10 = offset_rotation.interface.new_socket(name = "Index", in_out='INPUT', socket_type = 'NodeSocketInt')
			index_socket_10.subtype = 'NONE'
			index_socket_10.default_value = 0
			index_socket_10.min_value = 0
			index_socket_10.max_value = 2147483647
			index_socket_10.attribute_domain = 'POINT'

			#Socket Rotation
			rotation_socket_6 = offset_rotation.interface.new_socket(name = "Rotation", in_out='INPUT', socket_type = 'NodeSocketRotation')
			rotation_socket_6.attribute_domain = 'POINT'
			rotation_socket_6.hide_value = True

			#Socket Offset
			offset_socket_8 = offset_rotation.interface.new_socket(name = "Offset", in_out='INPUT', socket_type = 'NodeSocketInt')
			offset_socket_8.subtype = 'NONE'
			offset_socket_8.default_value = 0
			offset_socket_8.min_value = -2147483648
			offset_socket_8.max_value = 2147483647
			offset_socket_8.attribute_domain = 'POINT'


			#initialize offset_rotation nodes
			#node Group Output
			group_output_55 = offset_rotation.nodes.new("NodeGroupOutput")
			group_output_55.name = "Group Output"
			group_output_55.is_active_output = True

			#node Group Input
			group_input_55 = offset_rotation.nodes.new("NodeGroupInput")
			group_input_55.name = "Group Input"

			#node Evaluate at Index
			evaluate_at_index_4 = offset_rotation.nodes.new("GeometryNodeFieldAtIndex")
			evaluate_at_index_4.name = "Evaluate at Index"
			evaluate_at_index_4.data_type = 'QUATERNION'
			evaluate_at_index_4.domain = 'POINT'

			#node Math
			math_16 = offset_rotation.nodes.new("ShaderNodeMath")
			math_16.name = "Math"
			math_16.operation = 'ADD'
			math_16.use_clamp = False




			#Set locations
			group_output_55.location = (100.0, 0.0)
			group_input_55.location = (-400.0, 0.0)
			evaluate_at_index_4.location = (-60.0, 0.0)
			math_16.location = (-220.0, 0.0)

			#Set dimensions
			group_output_55.width, group_output_55.height = 140.0, 100.0
			group_input_55.width, group_input_55.height = 140.0, 100.0
			evaluate_at_index_4.width, evaluate_at_index_4.height = 140.0, 100.0
			math_16.width, math_16.height = 140.0, 100.0

			#initialize offset_rotation links
			#evaluate_at_index_4.Value -> group_output_55.Rotation
			offset_rotation.links.new(evaluate_at_index_4.outputs[0], group_output_55.inputs[0])
			#group_input_55.Index -> math_16.Value
			offset_rotation.links.new(group_input_55.outputs[0], math_16.inputs[0])
			#group_input_55.Offset -> math_16.Value
			offset_rotation.links.new(group_input_55.outputs[2], math_16.inputs[1])
			#math_16.Value -> evaluate_at_index_4.Index
			offset_rotation.links.new(math_16.outputs[0], evaluate_at_index_4.inputs[0])
			#group_input_55.Rotation -> evaluate_at_index_4.Value
			offset_rotation.links.new(group_input_55.outputs[1], evaluate_at_index_4.inputs[1])
			return offset_rotation

		offset_rotation = offset_rotation_node_group()

		#initialize _ca_to_helix node group
		def _ca_to_helix_node_group():
			_ca_to_helix = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".CA to helix")

			_ca_to_helix.color_tag = 'NONE'
			_ca_to_helix.description = ""


			#_ca_to_helix interface
			#Socket Geometry
			geometry_socket_11 = _ca_to_helix.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			geometry_socket_11.attribute_domain = 'POINT'

			#Socket Curve
			curve_socket_5 = _ca_to_helix.interface.new_socket(name = "Curve", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			curve_socket_5.attribute_domain = 'POINT'

			#Socket Boolean
			boolean_socket_9 = _ca_to_helix.interface.new_socket(name = "Boolean", in_out='INPUT', socket_type = 'NodeSocketBool')
			boolean_socket_9.attribute_domain = 'POINT'

			#Socket Thickness
			thickness_socket_2 = _ca_to_helix.interface.new_socket(name = "Thickness", in_out='INPUT', socket_type = 'NodeSocketFloat')
			thickness_socket_2.subtype = 'NONE'
			thickness_socket_2.default_value = 2.3399999141693115
			thickness_socket_2.min_value = -10000.0
			thickness_socket_2.max_value = 10000.0
			thickness_socket_2.attribute_domain = 'POINT'

			#Socket Width
			width_socket_2 = _ca_to_helix.interface.new_socket(name = "Width", in_out='INPUT', socket_type = 'NodeSocketFloat')
			width_socket_2.subtype = 'NONE'
			width_socket_2.default_value = 0.5600000023841858
			width_socket_2.min_value = -10000.0
			width_socket_2.max_value = 10000.0
			width_socket_2.attribute_domain = 'POINT'

			#Socket Profile Resolution
			profile_resolution_socket_2 = _ca_to_helix.interface.new_socket(name = "Profile Resolution", in_out='INPUT', socket_type = 'NodeSocketInt')
			profile_resolution_socket_2.subtype = 'NONE'
			profile_resolution_socket_2.default_value = 4
			profile_resolution_socket_2.min_value = 3
			profile_resolution_socket_2.max_value = 512
			profile_resolution_socket_2.attribute_domain = 'POINT'

			#Socket Subdivisions
			subdivisions_socket_3 = _ca_to_helix.interface.new_socket(name = "Subdivisions", in_out='INPUT', socket_type = 'NodeSocketInt')
			subdivisions_socket_3.subtype = 'NONE'
			subdivisions_socket_3.default_value = 6
			subdivisions_socket_3.min_value = 1
			subdivisions_socket_3.max_value = 2147483647
			subdivisions_socket_3.attribute_domain = 'POINT'


			#initialize _ca_to_helix nodes
			#node Group Output
			group_output_56 = _ca_to_helix.nodes.new("NodeGroupOutput")
			group_output_56.name = "Group Output"
			group_output_56.is_active_output = True

			#node Group Input
			group_input_56 = _ca_to_helix.nodes.new("NodeGroupInput")
			group_input_56.name = "Group Input"

			#node Frame.005
			frame_005 = _ca_to_helix.nodes.new("NodeFrame")
			frame_005.label = "Creating Alpha-helix Geometry"
			frame_005.name = "Frame.005"
			frame_005.label_size = 20
			frame_005.shrink = True

			#node Boolean Math.001
			boolean_math_001_8 = _ca_to_helix.nodes.new("FunctionNodeBooleanMath")
			boolean_math_001_8.name = "Boolean Math.001"
			boolean_math_001_8.operation = 'NOT'

			#node Group.014
			group_014_2 = _ca_to_helix.nodes.new("GeometryNodeGroup")
			group_014_2.name = "Group.014"
			group_014_2.node_tree = curve_offset_dot
			#Socket_1
			group_014_2.inputs[0].default_value = (0.0, 0.0, 0.0)
			#Socket_4
			group_014_2.inputs[1].default_value = 'Less Than'
			#Socket_3
			group_014_2.inputs[2].default_value = -0.699999988079071
			#Socket_6
			group_014_2.inputs[3].default_value = 1
			#Socket_8
			group_014_2.inputs[4].default_value = (0.0, 0.0, 1.0)
			#Socket_7
			group_014_2.inputs[5].default_value = 3.1415927410125732

			#node Combine XYZ.002
			combine_xyz_002 = _ca_to_helix.nodes.new("ShaderNodeCombineXYZ")
			combine_xyz_002.name = "Combine XYZ.002"
			#Z
			combine_xyz_002.inputs[2].default_value = 0.0

			#node Curve Tangent.003
			curve_tangent_003 = _ca_to_helix.nodes.new("GeometryNodeInputTangent")
			curve_tangent_003.name = "Curve Tangent.003"

			#node Group.016
			group_016_3 = _ca_to_helix.nodes.new("GeometryNodeGroup")
			group_016_3.name = "Group.016"
			group_016_3.node_tree = curve_custom_profile
			#Socket_8
			group_016_3.inputs[2].default_value = 'Custom Profile'
			#Input_13
			group_016_3.inputs[7].default_value = 1.0
			#Input_14
			group_016_3.inputs[8].default_value = 0.0

			#node Group.027
			group_027_1 = _ca_to_helix.nodes.new("GeometryNodeGroup")
			group_027_1.name = "Group.027"
			group_027_1.node_tree = curve_split_splines
			#Socket_4
			group_027_1.inputs[2].default_value = 'Free'
			#Socket_2
			group_027_1.inputs[3].default_value = 0
			#Socket_7
			group_027_1.inputs[4].default_value = 'Split Distance'
			#Socket_6
			group_027_1.inputs[5].default_value = 0.05000000074505806
			#Socket_16
			group_027_1.inputs[7].default_value = 0.14999999105930328
			#Socket_17
			group_027_1.inputs[8].default_value = 'Bezier'
			#Socket_18
			group_027_1.inputs[9].default_value = 12

			#node Group.034
			group_034 = _ca_to_helix.nodes.new("GeometryNodeGroup")
			group_034.name = "Group.034"
			group_034.node_tree = is_helix
			#Socket_3
			group_034.inputs[1].default_value = False

			#node Group.029
			group_029 = _ca_to_helix.nodes.new("GeometryNodeGroup")
			group_029.name = "Group.029"
			group_029.node_tree = curve_rotation
			#Socket_1
			group_029.inputs[0].default_value = (0.0, 0.0, 1.0)

			#node Rotate Rotation.001
			rotate_rotation_001 = _ca_to_helix.nodes.new("FunctionNodeRotateRotation")
			rotate_rotation_001.name = "Rotate Rotation.001"
			rotate_rotation_001.rotation_space = 'LOCAL'
			#Rotate By
			rotate_rotation_001.inputs[1].default_value = (0.3490658402442932, 0.0, 0.0)

			#node Set Spline Type.001
			set_spline_type_001_1 = _ca_to_helix.nodes.new("GeometryNodeCurveSplineType")
			set_spline_type_001_1.name = "Set Spline Type.001"
			set_spline_type_001_1.spline_type = 'BEZIER'
			#Selection
			set_spline_type_001_1.inputs[1].default_value = True

			#node Set Handle Type
			set_handle_type_3 = _ca_to_helix.nodes.new("GeometryNodeCurveSetHandles")
			set_handle_type_3.name = "Set Handle Type"
			set_handle_type_3.handle_type = 'AUTO'
			set_handle_type_3.mode = {'LEFT', 'RIGHT'}
			#Selection
			set_handle_type_3.inputs[1].default_value = True

			#node Frame.011
			frame_011 = _ca_to_helix.nodes.new("NodeFrame")
			frame_011.label = "Creating Helix Cylinders"
			frame_011.name = "Frame.011"
			frame_011.label_size = 20
			frame_011.shrink = True

			#node Group.018
			group_018_1 = _ca_to_helix.nodes.new("GeometryNodeGroup")
			group_018_1.name = "Group.018"
			group_018_1.node_tree = curve_custom_profile
			#Input_15
			group_018_1.inputs[1].default_value = 6
			#Socket_8
			group_018_1.inputs[2].default_value = 'Custom Profile'
			#Socket_6
			group_018_1.inputs[3].default_value = (0.0, 0.0, 0.0)
			#Input_2
			group_018_1.inputs[4].default_value = (2.6500000953674316, 2.6500000953674316, 2.6500000953674316)
			#Input_12
			group_018_1.inputs[6].default_value = 8
			#Input_13
			group_018_1.inputs[7].default_value = 1.0
			#Input_14
			group_018_1.inputs[8].default_value = 0.0

			#node Group.028
			group_028 = _ca_to_helix.nodes.new("GeometryNodeGroup")
			group_028.name = "Group.028"
			group_028.node_tree = curve_split_splines
			#Socket_4
			group_028.inputs[2].default_value = 'Free'
			#Socket_2
			group_028.inputs[3].default_value = 0
			#Socket_7
			group_028.inputs[4].default_value = 'Split Distance'
			#Socket_6
			group_028.inputs[5].default_value = 0.05999999865889549
			#Socket_9
			group_028.inputs[6].default_value = (0.0, 0.0, 0.0)
			#Socket_16
			group_028.inputs[7].default_value = 0.0
			#Socket_17
			group_028.inputs[8].default_value = 'Bezier'
			#Socket_18
			group_028.inputs[9].default_value = 12

			#node Group.036
			group_036 = _ca_to_helix.nodes.new("GeometryNodeGroup")
			group_036.name = "Group.036"
			group_036.node_tree = is_helix
			#Socket_3
			group_036.inputs[1].default_value = False

			#node Set Position
			set_position_4 = _ca_to_helix.nodes.new("GeometryNodeSetPosition")
			set_position_4.name = "Set Position"
			#Selection
			set_position_4.inputs[1].default_value = True
			#Position
			set_position_4.inputs[2].default_value = (0.0, 0.0, 0.0)

			#node Normal
			normal_3 = _ca_to_helix.nodes.new("GeometryNodeInputNormal")
			normal_3.name = "Normal"

			#node Endpoint Selection
			endpoint_selection_3 = _ca_to_helix.nodes.new("GeometryNodeCurveEndpointSelection")
			endpoint_selection_3.name = "Endpoint Selection"
			#Start Size
			endpoint_selection_3.inputs[0].default_value = 1
			#End Size
			endpoint_selection_3.inputs[1].default_value = 1

			#node Boolean Math
			boolean_math_11 = _ca_to_helix.nodes.new("FunctionNodeBooleanMath")
			boolean_math_11.name = "Boolean Math"
			boolean_math_11.operation = 'NOT'

			#node Set Position.001
			set_position_001_3 = _ca_to_helix.nodes.new("GeometryNodeSetPosition")
			set_position_001_3.name = "Set Position.001"
			set_position_001_3.inputs[3].hide = True
			#Offset
			set_position_001_3.inputs[3].default_value = (0.0, 0.0, 0.0)

			#node Blur Attribute.001
			blur_attribute_001 = _ca_to_helix.nodes.new("GeometryNodeBlurAttribute")
			blur_attribute_001.name = "Blur Attribute.001"
			blur_attribute_001.data_type = 'FLOAT_VECTOR'
			#Iterations
			blur_attribute_001.inputs[1].default_value = 2

			#node Position.001
			position_001_2 = _ca_to_helix.nodes.new("GeometryNodeInputPosition")
			position_001_2.name = "Position.001"

			#node Set Curve Normal.001
			set_curve_normal_001_1 = _ca_to_helix.nodes.new("GeometryNodeSetCurveNormal")
			set_curve_normal_001_1.name = "Set Curve Normal.001"
			set_curve_normal_001_1.mode = 'MINIMUM_TWIST'
			#Selection
			set_curve_normal_001_1.inputs[1].default_value = True

			#node Curve to Mesh
			curve_to_mesh_1 = _ca_to_helix.nodes.new("GeometryNodeCurveToMesh")
			curve_to_mesh_1.name = "Curve to Mesh"
			#Fill Caps
			curve_to_mesh_1.inputs[2].default_value = True

			#node Curve Circle
			curve_circle_1 = _ca_to_helix.nodes.new("GeometryNodeCurvePrimitiveCircle")
			curve_circle_1.name = "Curve Circle"
			curve_circle_1.mode = 'RADIUS'
			#Resolution
			curve_circle_1.inputs[0].default_value = 12
			#Radius
			curve_circle_1.inputs[4].default_value = 0.3100000023841858

			#node Set Spline Resolution
			set_spline_resolution_2 = _ca_to_helix.nodes.new("GeometryNodeSetSplineResolution")
			set_spline_resolution_2.name = "Set Spline Resolution"
			#Selection
			set_spline_resolution_2.inputs[1].default_value = True

			#node Resample Curve
			resample_curve_1 = _ca_to_helix.nodes.new("GeometryNodeResampleCurve")
			resample_curve_1.name = "Resample Curve"
			resample_curve_1.mode = 'LENGTH'
			#Selection
			resample_curve_1.inputs[1].default_value = True

			#node Group.010
			group_010_2 = _ca_to_helix.nodes.new("GeometryNodeGroup")
			group_010_2.name = "Group.010"
			group_010_2.node_tree = mn_units
			#Input_1
			group_010_2.inputs[0].default_value = 2.0

			#node Set Curve Radius
			set_curve_radius = _ca_to_helix.nodes.new("GeometryNodeSetCurveRadius")
			set_curve_radius.name = "Set Curve Radius"
			#Selection
			set_curve_radius.inputs[1].default_value = True
			#Radius
			set_curve_radius.inputs[2].default_value = 0.08500000089406967

			#node Group.011
			group_011_2 = _ca_to_helix.nodes.new("GeometryNodeGroup")
			group_011_2.name = "Group.011"
			group_011_2.node_tree = expand_boolean
			#Socket_1
			group_011_2.inputs[0].default_value = False
			#Socket_2
			group_011_2.inputs[1].default_value = 0

			#node Group.012
			group_012_1 = _ca_to_helix.nodes.new("GeometryNodeGroup")
			group_012_1.name = "Group.012"
			group_012_1.node_tree = boolean_shrink
			#Socket_2
			group_012_1.inputs[1].default_value = 1

			#node Rotate Rotation.002
			rotate_rotation_002 = _ca_to_helix.nodes.new("FunctionNodeRotateRotation")
			rotate_rotation_002.name = "Rotate Rotation.002"
			rotate_rotation_002.rotation_space = 'LOCAL'

			#node Group.050
			group_050 = _ca_to_helix.nodes.new("GeometryNodeGroup")
			group_050.name = "Group.050"
			group_050.node_tree = offset_rotation
			#Socket_1
			group_050.inputs[0].default_value = 0

			#node Group.051
			group_051 = _ca_to_helix.nodes.new("GeometryNodeGroup")
			group_051.name = "Group.051"
			group_051.node_tree = curve_endpoint_values
			#Socket_5
			group_051.inputs[0].default_value = 1
			#Socket_1
			group_051.inputs[1].default_value = 1
			#Socket_2
			group_051.inputs[2].default_value = 0
			#Socket_6
			group_051.inputs[3].default_value = 1
			#Socket_3
			group_051.inputs[4].default_value = -1

			#node Align Rotation to Vector
			align_rotation_to_vector = _ca_to_helix.nodes.new("FunctionNodeAlignRotationToVector")
			align_rotation_to_vector.name = "Align Rotation to Vector"
			align_rotation_to_vector.axis = 'Z'
			align_rotation_to_vector.pivot_axis = 'Y'
			#Factor
			align_rotation_to_vector.inputs[1].default_value = 1.0

			#node Join Geometry
			join_geometry = _ca_to_helix.nodes.new("GeometryNodeJoinGeometry")
			join_geometry.name = "Join Geometry"

			#node Group Input.001
			group_input_001_8 = _ca_to_helix.nodes.new("NodeGroupInput")
			group_input_001_8.name = "Group Input.001"
			group_input_001_8.outputs[0].hide = True
			group_input_001_8.outputs[1].hide = True
			group_input_001_8.outputs[2].hide = True
			group_input_001_8.outputs[3].hide = True
			group_input_001_8.outputs[5].hide = True
			group_input_001_8.outputs[6].hide = True

			#node Reroute
			reroute_13 = _ca_to_helix.nodes.new("NodeReroute")
			reroute_13.name = "Reroute"
			#node Set Spline Type
			set_spline_type_2 = _ca_to_helix.nodes.new("GeometryNodeCurveSplineType")
			set_spline_type_2.name = "Set Spline Type"
			set_spline_type_2.spline_type = 'POLY'
			#Selection
			set_spline_type_2.inputs[1].default_value = True

			#node Set Spline Type.002
			set_spline_type_002_1 = _ca_to_helix.nodes.new("GeometryNodeCurveSplineType")
			set_spline_type_002_1.name = "Set Spline Type.002"
			set_spline_type_002_1.spline_type = 'BEZIER'
			#Selection
			set_spline_type_002_1.inputs[1].default_value = True

			#node Set Handle Type.001
			set_handle_type_001_2 = _ca_to_helix.nodes.new("GeometryNodeCurveSetHandles")
			set_handle_type_001_2.name = "Set Handle Type.001"
			set_handle_type_001_2.handle_type = 'AUTO'
			set_handle_type_001_2.mode = {'LEFT', 'RIGHT'}
			#Selection
			set_handle_type_001_2.inputs[1].default_value = True

			#node Group Input.002
			group_input_002_4 = _ca_to_helix.nodes.new("NodeGroupInput")
			group_input_002_4.name = "Group Input.002"
			group_input_002_4.outputs[0].hide = True
			group_input_002_4.outputs[1].hide = True
			group_input_002_4.outputs[2].hide = True
			group_input_002_4.outputs[3].hide = True
			group_input_002_4.outputs[4].hide = True
			group_input_002_4.outputs[6].hide = True

			#node Math
			math_17 = _ca_to_helix.nodes.new("ShaderNodeMath")
			math_17.name = "Math"
			math_17.operation = 'DIVIDE'
			math_17.use_clamp = False
			#Value_001
			math_17.inputs[1].default_value = 4.0

			#node Group
			group_19 = _ca_to_helix.nodes.new("GeometryNodeGroup")
			group_19.name = "Group"
			group_19.node_tree = vector_in_angstroms
			#Socket_4
			group_19.inputs[1].default_value = True
			#Socket_3
			group_19.inputs[2].default_value = 2.4000000953674316

			#node Group.001
			group_001_11 = _ca_to_helix.nodes.new("GeometryNodeGroup")
			group_001_11.name = "Group.001"
			group_001_11.node_tree = tmp_ss_attributes

			#node Compare
			compare_8 = _ca_to_helix.nodes.new("FunctionNodeCompare")
			compare_8.name = "Compare"
			compare_8.data_type = 'INT'
			compare_8.mode = 'ELEMENT'
			compare_8.operation = 'GREATER_THAN'
			#B_INT
			compare_8.inputs[3].default_value = 6

			#node Switch
			switch_12 = _ca_to_helix.nodes.new("GeometryNodeSwitch")
			switch_12.name = "Switch"
			switch_12.input_type = 'BOOLEAN'



			#Set parents
			boolean_math_001_8.parent = frame_005
			group_014_2.parent = frame_005
			combine_xyz_002.parent = frame_005
			curve_tangent_003.parent = frame_005
			group_016_3.parent = frame_005
			group_027_1.parent = frame_005
			group_034.parent = frame_005
			group_029.parent = frame_005
			rotate_rotation_001.parent = frame_005
			set_spline_type_001_1.parent = frame_005
			set_handle_type_3.parent = frame_005
			group_018_1.parent = frame_011
			group_028.parent = frame_011
			group_036.parent = frame_011
			set_position_4.parent = frame_011
			normal_3.parent = frame_011
			endpoint_selection_3.parent = frame_011
			boolean_math_11.parent = frame_011
			set_position_001_3.parent = frame_011
			blur_attribute_001.parent = frame_011
			position_001_2.parent = frame_011
			set_curve_normal_001_1.parent = frame_011
			curve_to_mesh_1.parent = frame_011
			curve_circle_1.parent = frame_011
			set_spline_resolution_2.parent = frame_011
			resample_curve_1.parent = frame_011
			group_010_2.parent = frame_011
			set_curve_radius.parent = frame_011
			group_011_2.parent = frame_011
			group_012_1.parent = frame_011
			rotate_rotation_002.parent = frame_005
			group_050.parent = frame_005
			group_051.parent = frame_005
			align_rotation_to_vector.parent = frame_005
			group_input_001_8.parent = frame_005
			set_spline_type_2.parent = frame_011
			set_spline_type_002_1.parent = frame_011
			set_handle_type_001_2.parent = frame_011
			group_input_002_4.parent = frame_011
			math_17.parent = frame_011
			group_19.parent = frame_011
			group_001_11.parent = frame_011
			compare_8.parent = frame_011
			switch_12.parent = frame_011

			#Set locations
			group_output_56.location = (1842.0908203125, 23.19063949584961)
			group_input_56.location = (-1560.2000732421875, 0.0)
			frame_005.location = (2445.0, -2080.0)
			boolean_math_001_8.location = (-2785.0, 1700.0)
			group_014_2.location = (-3145.0, 1220.0)
			combine_xyz_002.location = (-1985.0, 1680.0)
			curve_tangent_003.location = (-2805.0, 1260.0)
			group_016_3.location = (-1675.0, 1820.0)
			group_027_1.location = (-2445.0, 1840.0)
			group_034.location = (-2625.0, 1700.0)
			group_029.location = (-3305.0, 1420.0)
			rotate_rotation_001.location = (-3145.0, 1420.0)
			set_spline_type_001_1.location = (-2159.46923828125, 1839.013916015625)
			set_handle_type_3.location = (-1979.46923828125, 1839.013916015625)
			frame_011.location = (3093.897216796875, -1186.8548583984375)
			group_018_1.location = (-1937.62841796875, 1558.099853515625)
			group_028.location = (-3976.3818359375, 1851.57080078125)
			group_036.location = (-4468.47265625, 1783.848388671875)
			set_position_4.location = (-3593.897216796875, 1826.8548583984375)
			normal_3.location = (-3753.897216796875, 1666.8548583984375)
			endpoint_selection_3.location = (-3433.897216796875, 1706.8548583984375)
			boolean_math_11.location = (-3273.897216796875, 1706.8548583984375)
			set_position_001_3.location = (-3073.897216796875, 1866.8548583984375)
			blur_attribute_001.location = (-3073.897216796875, 1686.8548583984375)
			position_001_2.location = (-3273.897216796875, 1586.8548583984375)
			set_curve_normal_001_1.location = (-2803.100341796875, 1862.029296875)
			curve_to_mesh_1.location = (-1933.897216796875, 1866.8548583984375)
			curve_circle_1.location = (-1933.897216796875, 1726.8548583984375)
			set_spline_resolution_2.location = (-2093.897216796875, 1866.8548583984375)
			resample_curve_1.location = (-2579.897216796875, 1866.8548583984375)
			group_010_2.location = (-2579.897216796875, 1706.8548583984375)
			set_curve_radius.location = (-4503.3876953125, 1945.980224609375)
			group_011_2.location = (-4032.4833984375, 1432.8636474609375)
			group_012_1.location = (-4268.7890625, 1626.6763916015625)
			rotate_rotation_002.location = (-2965.0, 1420.0)
			group_050.location = (-2805.0, 1420.0)
			group_051.location = (-2965.0, 1280.0)
			align_rotation_to_vector.location = (-2645.0, 1420.0)
			join_geometry.location = (1662.4000244140625, 147.8900146484375)
			group_input_001_8.location = (-1985.0, 1540.0)
			reroute_13.location = (1564.7734375, 214.01461791992188)
			set_spline_type_2.location = (-3277.73291015625, 1861.396240234375)
			set_spline_type_002_1.location = (-2419.897216796875, 1866.8548583984375)
			set_handle_type_001_2.location = (-2253.897216796875, 1866.8548583984375)
			group_input_002_4.location = (-2253.897216796875, 1706.8548583984375)
			math_17.location = (-2093.897216796875, 1706.8548583984375)
			group_19.location = (-3593.897216796875, 1666.8548583984375)
			group_001_11.location = (-4393.8974609375, 1526.8548583984375)
			compare_8.location = (-4195.23193359375, 1542.93701171875)
			switch_12.location = (-4264.5966796875, 1751.932861328125)

			#Set dimensions
			group_output_56.width, group_output_56.height = 140.0, 100.0
			group_input_56.width, group_input_56.height = 140.0, 100.0
			frame_005.width, frame_005.height = 1934.947998046875, 890.0
			boolean_math_001_8.width, boolean_math_001_8.height = 140.0, 100.0
			group_014_2.width, group_014_2.height = 142.4111785888672, 100.0
			combine_xyz_002.width, combine_xyz_002.height = 140.0, 100.0
			curve_tangent_003.width, curve_tangent_003.height = 140.0, 100.0
			group_016_3.width, group_016_3.height = 244.548095703125, 100.0
			group_027_1.width, group_027_1.height = 140.0, 100.0
			group_034.width, group_034.height = 140.0, 100.0
			group_029.width, group_029.height = 140.0, 100.0
			rotate_rotation_001.width, rotate_rotation_001.height = 140.0, 100.0
			set_spline_type_001_1.width, set_spline_type_001_1.height = 140.0, 100.0
			set_handle_type_3.width, set_handle_type_3.height = 140.0, 100.0
			frame_011.width, frame_011.height = 2870.14794921875, 882.0001220703125
			group_018_1.width, group_018_1.height = 244.548095703125, 100.0
			group_028.width, group_028.height = 140.0, 100.0
			group_036.width, group_036.height = 140.0, 100.0
			set_position_4.width, set_position_4.height = 140.0, 100.0
			normal_3.width, normal_3.height = 140.0, 100.0
			endpoint_selection_3.width, endpoint_selection_3.height = 140.0, 100.0
			boolean_math_11.width, boolean_math_11.height = 140.0, 100.0
			set_position_001_3.width, set_position_001_3.height = 140.0, 100.0
			blur_attribute_001.width, blur_attribute_001.height = 140.0, 100.0
			position_001_2.width, position_001_2.height = 140.0, 100.0
			set_curve_normal_001_1.width, set_curve_normal_001_1.height = 140.0, 100.0
			curve_to_mesh_1.width, curve_to_mesh_1.height = 140.0, 100.0
			curve_circle_1.width, curve_circle_1.height = 140.0, 100.0
			set_spline_resolution_2.width, set_spline_resolution_2.height = 140.0, 100.0
			resample_curve_1.width, resample_curve_1.height = 140.0, 100.0
			group_010_2.width, group_010_2.height = 140.0, 100.0
			set_curve_radius.width, set_curve_radius.height = 140.0, 100.0
			group_011_2.width, group_011_2.height = 140.0, 100.0
			group_012_1.width, group_012_1.height = 140.0, 100.0
			rotate_rotation_002.width, rotate_rotation_002.height = 140.0, 100.0
			group_050.width, group_050.height = 140.0, 100.0
			group_051.width, group_051.height = 140.0, 100.0
			align_rotation_to_vector.width, align_rotation_to_vector.height = 140.0, 100.0
			join_geometry.width, join_geometry.height = 140.0, 100.0
			group_input_001_8.width, group_input_001_8.height = 140.0, 100.0
			reroute_13.width, reroute_13.height = 16.0, 100.0
			set_spline_type_2.width, set_spline_type_2.height = 140.0, 100.0
			set_spline_type_002_1.width, set_spline_type_002_1.height = 140.0, 100.0
			set_handle_type_001_2.width, set_handle_type_001_2.height = 140.0, 100.0
			group_input_002_4.width, group_input_002_4.height = 140.0, 100.0
			math_17.width, math_17.height = 140.0, 100.0
			group_19.width, group_19.height = 140.0, 100.0
			group_001_11.width, group_001_11.height = 140.0, 100.0
			compare_8.width, compare_8.height = 140.0, 100.0
			switch_12.width, switch_12.height = 140.0, 100.0

			#initialize _ca_to_helix links
			#group_051.Value -> group_050.Offset
			_ca_to_helix.links.new(group_051.outputs[0], group_050.inputs[2])
			#rotate_rotation_002.Rotation -> group_050.Rotation
			_ca_to_helix.links.new(rotate_rotation_002.outputs[0], group_050.inputs[1])
			#rotate_rotation_001.Rotation -> rotate_rotation_002.Rotation
			_ca_to_helix.links.new(rotate_rotation_001.outputs[0], rotate_rotation_002.inputs[0])
			#set_curve_radius.Curve -> group_028.Curve
			_ca_to_helix.links.new(set_curve_radius.outputs[0], group_028.inputs[0])
			#group_036.Selection -> group_012_1.Boolean
			_ca_to_helix.links.new(group_036.outputs[0], group_012_1.inputs[0])
			#group_010_2.Angstrom -> resample_curve_1.Length
			_ca_to_helix.links.new(group_010_2.outputs[0], resample_curve_1.inputs[3])
			#set_spline_type_001_1.Curve -> set_handle_type_3.Curve
			_ca_to_helix.links.new(set_spline_type_001_1.outputs[0], set_handle_type_3.inputs[0])
			#set_curve_normal_001_1.Curve -> resample_curve_1.Curve
			_ca_to_helix.links.new(set_curve_normal_001_1.outputs[0], resample_curve_1.inputs[0])
			#group_027_1.Curve -> set_spline_type_001_1.Curve
			_ca_to_helix.links.new(group_027_1.outputs[0], set_spline_type_001_1.inputs[0])
			#set_handle_type_001_2.Curve -> set_spline_resolution_2.Geometry
			_ca_to_helix.links.new(set_handle_type_001_2.outputs[0], set_spline_resolution_2.inputs[0])
			#set_spline_resolution_2.Geometry -> curve_to_mesh_1.Curve
			_ca_to_helix.links.new(set_spline_resolution_2.outputs[0], curve_to_mesh_1.inputs[0])
			#blur_attribute_001.Value -> set_position_001_3.Position
			_ca_to_helix.links.new(blur_attribute_001.outputs[0], set_position_001_3.inputs[2])
			#curve_circle_1.Curve -> curve_to_mesh_1.Profile Curve
			_ca_to_helix.links.new(curve_circle_1.outputs[0], curve_to_mesh_1.inputs[1])
			#align_rotation_to_vector.Rotation -> group_016_3.Profile Rotation
			_ca_to_helix.links.new(align_rotation_to_vector.outputs[0], group_016_3.inputs[3])
			#group_029.Rotation -> rotate_rotation_001.Rotation
			_ca_to_helix.links.new(group_029.outputs[0], rotate_rotation_001.inputs[0])
			#combine_xyz_002.Vector -> group_016_3.Profile Scale
			_ca_to_helix.links.new(combine_xyz_002.outputs[0], group_016_3.inputs[4])
			#position_001_2.Position -> blur_attribute_001.Value
			_ca_to_helix.links.new(position_001_2.outputs[0], blur_attribute_001.inputs[0])
			#set_position_001_3.Geometry -> set_curve_normal_001_1.Curve
			_ca_to_helix.links.new(set_position_001_3.outputs[0], set_curve_normal_001_1.inputs[0])
			#set_spline_type_2.Curve -> set_position_001_3.Geometry
			_ca_to_helix.links.new(set_spline_type_2.outputs[0], set_position_001_3.inputs[0])
			#boolean_math_001_8.Boolean -> group_034.And
			_ca_to_helix.links.new(boolean_math_001_8.outputs[0], group_034.inputs[0])
			#set_handle_type_3.Curve -> group_016_3.Curve
			_ca_to_helix.links.new(set_handle_type_3.outputs[0], group_016_3.inputs[0])
			#endpoint_selection_3.Selection -> boolean_math_11.Boolean
			_ca_to_helix.links.new(endpoint_selection_3.outputs[0], boolean_math_11.inputs[0])
			#group_014_2.Rotation -> rotate_rotation_002.Rotate By
			_ca_to_helix.links.new(group_014_2.outputs[2], rotate_rotation_002.inputs[1])
			#curve_tangent_003.Tangent -> align_rotation_to_vector.Vector
			_ca_to_helix.links.new(curve_tangent_003.outputs[0], align_rotation_to_vector.inputs[2])
			#group_028.Curve -> set_position_4.Geometry
			_ca_to_helix.links.new(group_028.outputs[0], set_position_4.inputs[0])
			#group_050.Rotation -> align_rotation_to_vector.Rotation
			_ca_to_helix.links.new(group_050.outputs[0], align_rotation_to_vector.inputs[0])
			#group_input_56.Curve -> group_027_1.Curve
			_ca_to_helix.links.new(group_input_56.outputs[0], group_027_1.inputs[0])
			#group_input_56.Curve -> set_curve_radius.Curve
			_ca_to_helix.links.new(group_input_56.outputs[0], set_curve_radius.inputs[0])
			#group_input_56.Thickness -> combine_xyz_002.X
			_ca_to_helix.links.new(group_input_56.outputs[2], combine_xyz_002.inputs[0])
			#group_input_56.Subdivisions -> group_016_3.Subdivisions
			_ca_to_helix.links.new(group_input_56.outputs[5], group_016_3.inputs[1])
			#group_input_56.Boolean -> boolean_math_001_8.Boolean
			_ca_to_helix.links.new(group_input_56.outputs[1], boolean_math_001_8.inputs[0])
			#group_input_56.Width -> combine_xyz_002.Y
			_ca_to_helix.links.new(group_input_56.outputs[3], combine_xyz_002.inputs[1])
			#group_input_56.Boolean -> group_036.And
			_ca_to_helix.links.new(group_input_56.outputs[1], group_036.inputs[0])
			#reroute_13.Output -> join_geometry.Geometry
			_ca_to_helix.links.new(reroute_13.outputs[0], join_geometry.inputs[0])
			#join_geometry.Geometry -> group_output_56.Geometry
			_ca_to_helix.links.new(join_geometry.outputs[0], group_output_56.inputs[0])
			#group_034.Selection -> group_027_1.Selection
			_ca_to_helix.links.new(group_034.outputs[0], group_027_1.inputs[1])
			#group_input_001_8.Profile Resolution -> group_016_3.Profile Resolution
			_ca_to_helix.links.new(group_input_001_8.outputs[4], group_016_3.inputs[6])
			#align_rotation_to_vector.Rotation -> group_027_1.Rotation
			_ca_to_helix.links.new(align_rotation_to_vector.outputs[0], group_027_1.inputs[6])
			#curve_to_mesh_1.Mesh -> reroute_13.Input
			_ca_to_helix.links.new(curve_to_mesh_1.outputs[0], reroute_13.inputs[0])
			#set_position_4.Geometry -> set_spline_type_2.Curve
			_ca_to_helix.links.new(set_position_4.outputs[0], set_spline_type_2.inputs[0])
			#boolean_math_11.Boolean -> set_position_001_3.Selection
			_ca_to_helix.links.new(boolean_math_11.outputs[0], set_position_001_3.inputs[1])
			#boolean_math_11.Boolean -> blur_attribute_001.Weight
			_ca_to_helix.links.new(boolean_math_11.outputs[0], blur_attribute_001.inputs[2])
			#resample_curve_1.Curve -> set_spline_type_002_1.Curve
			_ca_to_helix.links.new(resample_curve_1.outputs[0], set_spline_type_002_1.inputs[0])
			#set_spline_type_002_1.Curve -> set_handle_type_001_2.Curve
			_ca_to_helix.links.new(set_spline_type_002_1.outputs[0], set_handle_type_001_2.inputs[0])
			#group_input_002_4.Subdivisions -> math_17.Value
			_ca_to_helix.links.new(group_input_002_4.outputs[5], math_17.inputs[0])
			#math_17.Value -> set_spline_resolution_2.Resolution
			_ca_to_helix.links.new(math_17.outputs[0], set_spline_resolution_2.inputs[2])
			#normal_3.Normal -> group_19.Vector
			_ca_to_helix.links.new(normal_3.outputs[0], group_19.inputs[0])
			#group_19.Vector -> set_position_4.Offset
			_ca_to_helix.links.new(group_19.outputs[0], set_position_4.inputs[3])
			#group_001_11.tmp_ss_size -> compare_8.A
			_ca_to_helix.links.new(group_001_11.outputs[2], compare_8.inputs[2])
			#group_012_1.Boolean -> switch_12.True
			_ca_to_helix.links.new(group_012_1.outputs[0], switch_12.inputs[2])
			#compare_8.Result -> switch_12.Switch
			_ca_to_helix.links.new(compare_8.outputs[0], switch_12.inputs[0])
			#group_036.Selection -> switch_12.False
			_ca_to_helix.links.new(group_036.outputs[0], switch_12.inputs[1])
			#group_036.Selection -> group_028.Selection
			_ca_to_helix.links.new(group_036.outputs[0], group_028.inputs[1])
			#group_016_3.Geometry -> join_geometry.Geometry
			_ca_to_helix.links.new(group_016_3.outputs[0], join_geometry.inputs[0])
			return _ca_to_helix

		_ca_to_helix = _ca_to_helix_node_group()

		#initialize _cleanup node group
		def _cleanup_node_group():
			_cleanup = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".Cleanup")

			_cleanup.color_tag = 'NONE'
			_cleanup.description = ""


			#_cleanup interface
			#Socket Geometry
			geometry_socket_12 = _cleanup.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			geometry_socket_12.attribute_domain = 'POINT'

			#Socket Geometry
			geometry_socket_13 = _cleanup.interface.new_socket(name = "Geometry", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			geometry_socket_13.attribute_domain = 'POINT'

			#Socket Blurred Color
			blurred_color_socket = _cleanup.interface.new_socket(name = "Blurred Color", in_out='INPUT', socket_type = 'NodeSocketBool')
			blurred_color_socket.attribute_domain = 'POINT'

			#Socket Color Source
			color_source_socket = _cleanup.interface.new_socket(name = "Color Source", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			color_source_socket.attribute_domain = 'POINT'

			#Socket Material
			material_socket = _cleanup.interface.new_socket(name = "Material", in_out='INPUT', socket_type = 'NodeSocketMaterial')
			material_socket.attribute_domain = 'POINT'

			#Socket Shade Smooth
			shade_smooth_socket = _cleanup.interface.new_socket(name = "Shade Smooth", in_out='INPUT', socket_type = 'NodeSocketBool')
			shade_smooth_socket.attribute_domain = 'POINT'


			#initialize _cleanup nodes
			#node Group Output
			group_output_57 = _cleanup.nodes.new("NodeGroupOutput")
			group_output_57.name = "Group Output"
			group_output_57.is_active_output = True

			#node Group Input
			group_input_57 = _cleanup.nodes.new("NodeGroupInput")
			group_input_57.name = "Group Input"

			#node Named Attribute
			named_attribute_6 = _cleanup.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_6.name = "Named Attribute"
			named_attribute_6.data_type = 'INT'
			#Name
			named_attribute_6.inputs[0].default_value = "tmp_idx"

			#node Named Attribute.001
			named_attribute_001_3 = _cleanup.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_001_3.name = "Named Attribute.001"
			named_attribute_001_3.data_type = 'FLOAT_COLOR'
			#Name
			named_attribute_001_3.inputs[0].default_value = "Color"

			#node Store Named Attribute.001
			store_named_attribute_001_1 = _cleanup.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_001_1.name = "Store Named Attribute.001"
			store_named_attribute_001_1.data_type = 'FLOAT_COLOR'
			store_named_attribute_001_1.domain = 'FACE'
			#Selection
			store_named_attribute_001_1.inputs[1].default_value = True
			#Name
			store_named_attribute_001_1.inputs[2].default_value = "Color"

			#node Set Material
			set_material = _cleanup.nodes.new("GeometryNodeSetMaterial")
			set_material.name = "Set Material"
			#Selection
			set_material.inputs[1].default_value = True

			#node Remove Named Attribute.001
			remove_named_attribute_001 = _cleanup.nodes.new("GeometryNodeRemoveAttribute")
			remove_named_attribute_001.name = "Remove Named Attribute.001"
			remove_named_attribute_001.pattern_mode = 'WILDCARD'
			#Name
			remove_named_attribute_001.inputs[1].default_value = "backbone_*"

			#node Sample Index
			sample_index_1 = _cleanup.nodes.new("GeometryNodeSampleIndex")
			sample_index_1.name = "Sample Index"
			sample_index_1.clamp = False
			sample_index_1.data_type = 'FLOAT_COLOR'
			sample_index_1.domain = 'POINT'

			#node Switch.001
			switch_001_6 = _cleanup.nodes.new("GeometryNodeSwitch")
			switch_001_6.name = "Switch.001"
			switch_001_6.input_type = 'GEOMETRY'

			#node Remove Named Attribute
			remove_named_attribute = _cleanup.nodes.new("GeometryNodeRemoveAttribute")
			remove_named_attribute.name = "Remove Named Attribute"
			remove_named_attribute.pattern_mode = 'WILDCARD'
			#Name
			remove_named_attribute.inputs[1].default_value = "tmp_*"

			#node Reroute.001
			reroute_001_11 = _cleanup.nodes.new("NodeReroute")
			reroute_001_11.name = "Reroute.001"
			#node Reroute.003
			reroute_003_8 = _cleanup.nodes.new("NodeReroute")
			reroute_003_8.name = "Reroute.003"
			#node Group Input.001
			group_input_001_9 = _cleanup.nodes.new("NodeGroupInput")
			group_input_001_9.name = "Group Input.001"

			#node Group Input.002
			group_input_002_5 = _cleanup.nodes.new("NodeGroupInput")
			group_input_002_5.name = "Group Input.002"
			group_input_002_5.outputs[0].hide = True
			group_input_002_5.outputs[2].hide = True
			group_input_002_5.outputs[3].hide = True
			group_input_002_5.outputs[4].hide = True
			group_input_002_5.outputs[5].hide = True

			#node Set Shade Smooth
			set_shade_smooth = _cleanup.nodes.new("GeometryNodeSetShadeSmooth")
			set_shade_smooth.name = "Set Shade Smooth"
			set_shade_smooth.domain = 'FACE'
			#Selection
			set_shade_smooth.inputs[1].default_value = True

			#node Viewer
			viewer = _cleanup.nodes.new("GeometryNodeViewer")
			viewer.name = "Viewer"
			viewer.data_type = 'INT'
			viewer.domain = 'AUTO'




			#Set locations
			group_output_57.location = (720.0, 0.0)
			group_input_57.location = (-720.0, 60.0)
			named_attribute_6.location = (-560.0, -360.0)
			named_attribute_001_3.location = (-560.0, -220.0)
			store_named_attribute_001_1.location = (-340.0, 120.0)
			set_material.location = (360.0, 60.0)
			remove_named_attribute_001.location = (200.0, 60.0)
			sample_index_1.location = (-340.0, -120.0)
			switch_001_6.location = (-140.00001525878906, 40.0)
			remove_named_attribute.location = (39.99998092651367, 60.0)
			reroute_001_11.location = (-400.0, -80.0)
			reroute_003_8.location = (-460.0, 20.0)
			group_input_001_9.location = (200.0, -80.0)
			group_input_002_5.location = (-140.00001525878906, 100.0)
			set_shade_smooth.location = (540.0, 60.0)
			viewer.location = (-336.69696044921875, -326.4769592285156)

			#Set dimensions
			group_output_57.width, group_output_57.height = 140.0, 100.0
			group_input_57.width, group_input_57.height = 140.0, 100.0
			named_attribute_6.width, named_attribute_6.height = 140.0, 100.0
			named_attribute_001_3.width, named_attribute_001_3.height = 140.0, 100.0
			store_named_attribute_001_1.width, store_named_attribute_001_1.height = 140.0, 100.0
			set_material.width, set_material.height = 140.0, 100.0
			remove_named_attribute_001.width, remove_named_attribute_001.height = 134.0596923828125, 100.0
			sample_index_1.width, sample_index_1.height = 140.0, 100.0
			switch_001_6.width, switch_001_6.height = 140.0, 100.0
			remove_named_attribute.width, remove_named_attribute.height = 134.0596923828125, 100.0
			reroute_001_11.width, reroute_001_11.height = 16.0, 100.0
			reroute_003_8.width, reroute_003_8.height = 16.0, 100.0
			group_input_001_9.width, group_input_001_9.height = 140.0, 100.0
			group_input_002_5.width, group_input_002_5.height = 140.0, 100.0
			set_shade_smooth.width, set_shade_smooth.height = 140.0, 100.0
			viewer.width, viewer.height = 140.0, 100.0

			#initialize _cleanup links
			#named_attribute_001_3.Attribute -> sample_index_1.Value
			_cleanup.links.new(named_attribute_001_3.outputs[0], sample_index_1.inputs[1])
			#sample_index_1.Value -> store_named_attribute_001_1.Value
			_cleanup.links.new(sample_index_1.outputs[0], store_named_attribute_001_1.inputs[3])
			#store_named_attribute_001_1.Geometry -> switch_001_6.False
			_cleanup.links.new(store_named_attribute_001_1.outputs[0], switch_001_6.inputs[1])
			#remove_named_attribute.Geometry -> remove_named_attribute_001.Geometry
			_cleanup.links.new(remove_named_attribute.outputs[0], remove_named_attribute_001.inputs[0])
			#group_input_57.Color Source -> sample_index_1.Geometry
			_cleanup.links.new(group_input_57.outputs[2], sample_index_1.inputs[0])
			#remove_named_attribute_001.Geometry -> set_material.Geometry
			_cleanup.links.new(remove_named_attribute_001.outputs[0], set_material.inputs[0])
			#switch_001_6.Output -> remove_named_attribute.Geometry
			_cleanup.links.new(switch_001_6.outputs[0], remove_named_attribute.inputs[0])
			#reroute_003_8.Output -> store_named_attribute_001_1.Geometry
			_cleanup.links.new(reroute_003_8.outputs[0], store_named_attribute_001_1.inputs[0])
			#reroute_001_11.Output -> switch_001_6.True
			_cleanup.links.new(reroute_001_11.outputs[0], switch_001_6.inputs[2])
			#set_shade_smooth.Geometry -> group_output_57.Geometry
			_cleanup.links.new(set_shade_smooth.outputs[0], group_output_57.inputs[0])
			#group_input_57.Geometry -> reroute_003_8.Input
			_cleanup.links.new(group_input_57.outputs[0], reroute_003_8.inputs[0])
			#group_input_001_9.Material -> set_material.Material
			_cleanup.links.new(group_input_001_9.outputs[3], set_material.inputs[2])
			#group_input_002_5.Blurred Color -> switch_001_6.Switch
			_cleanup.links.new(group_input_002_5.outputs[1], switch_001_6.inputs[0])
			#reroute_003_8.Output -> reroute_001_11.Input
			_cleanup.links.new(reroute_003_8.outputs[0], reroute_001_11.inputs[0])
			#set_material.Geometry -> set_shade_smooth.Geometry
			_cleanup.links.new(set_material.outputs[0], set_shade_smooth.inputs[0])
			#group_input_001_9.Shade Smooth -> set_shade_smooth.Shade Smooth
			_cleanup.links.new(group_input_001_9.outputs[4], set_shade_smooth.inputs[2])
			#named_attribute_6.Attribute -> sample_index_1.Index
			_cleanup.links.new(named_attribute_6.outputs[0], sample_index_1.inputs[2])
			#group_input_57.Geometry -> viewer.Geometry
			_cleanup.links.new(group_input_57.outputs[0], viewer.inputs[0])
			#named_attribute_6.Attribute -> viewer.Value
			_cleanup.links.new(named_attribute_6.outputs[0], viewer.inputs[1])
			return _cleanup

		_cleanup = _cleanup_node_group()

		#initialize _mn_utils_style_cartoon node group
		def _mn_utils_style_cartoon_node_group():
			_mn_utils_style_cartoon = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".MN_utils_style_cartoon")

			_mn_utils_style_cartoon.color_tag = 'GEOMETRY'
			_mn_utils_style_cartoon.description = ""

			_mn_utils_style_cartoon.is_modifier = True

			#_mn_utils_style_cartoon interface
			#Socket Cartoon Mesh
			cartoon_mesh_socket = _mn_utils_style_cartoon.interface.new_socket(name = "Cartoon Mesh", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			cartoon_mesh_socket.attribute_domain = 'POINT'

			#Socket CA Splines
			ca_splines_socket_1 = _mn_utils_style_cartoon.interface.new_socket(name = "CA Splines", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			ca_splines_socket_1.attribute_domain = 'POINT'

			#Socket Atoms
			atoms_socket_6 = _mn_utils_style_cartoon.interface.new_socket(name = "Atoms", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			atoms_socket_6.attribute_domain = 'POINT'
			atoms_socket_6.description = "Atomic geometry that contains vertices and edges"

			#Socket Selection
			selection_socket_9 = _mn_utils_style_cartoon.interface.new_socket(name = "Selection", in_out='INPUT', socket_type = 'NodeSocketBool')
			selection_socket_9.attribute_domain = 'POINT'
			selection_socket_9.hide_value = True
			selection_socket_9.description = "Selection of atoms to apply this node to"

			#Socket Shade Smooth
			shade_smooth_socket_1 = _mn_utils_style_cartoon.interface.new_socket(name = "Shade Smooth", in_out='INPUT', socket_type = 'NodeSocketBool')
			shade_smooth_socket_1.attribute_domain = 'POINT'
			shade_smooth_socket_1.description = "Apply smooth shading to the created geometry"

			#Socket Interpolate Color
			interpolate_color_socket = _mn_utils_style_cartoon.interface.new_socket(name = "Interpolate Color", in_out='INPUT', socket_type = 'NodeSocketBool')
			interpolate_color_socket.attribute_domain = 'POINT'
			interpolate_color_socket.description = "Interpolate between distinct color selections"

			#Socket Material
			material_socket_1 = _mn_utils_style_cartoon.interface.new_socket(name = "Material", in_out='INPUT', socket_type = 'NodeSocketMaterial')
			material_socket_1.attribute_domain = 'POINT'
			material_socket_1.description = "Material to apply to the resulting geometry"

			#Panel Profile
			profile_panel_1 = _mn_utils_style_cartoon.interface.new_panel("Profile")
			#Socket Profile Curve
			profile_curve_socket_1 = _mn_utils_style_cartoon.interface.new_socket(name = "Profile Curve", in_out='INPUT', socket_type = 'NodeSocketGeometry', parent = profile_panel_1)
			profile_curve_socket_1.attribute_domain = 'POINT'
			profile_curve_socket_1.description = "A custom curve-cirlce making SS ribbons."

			#Socket Profile Resolution
			profile_resolution_socket_3 = _mn_utils_style_cartoon.interface.new_socket(name = "Profile Resolution", in_out='INPUT', socket_type = 'NodeSocketInt', parent = profile_panel_1)
			profile_resolution_socket_3.subtype = 'NONE'
			profile_resolution_socket_3.default_value = 4
			profile_resolution_socket_3.min_value = 4
			profile_resolution_socket_3.max_value = 100
			profile_resolution_socket_3.attribute_domain = 'POINT'


			#Panel Cylinder
			cylinder_panel = _mn_utils_style_cartoon.interface.new_panel("Cylinder")
			#Socket As Cylinders
			as_cylinders_socket_1 = _mn_utils_style_cartoon.interface.new_socket(name = "As Cylinders", in_out='INPUT', socket_type = 'NodeSocketBool', parent = cylinder_panel)
			as_cylinders_socket_1.attribute_domain = 'POINT'

			#Socket Cylinder Curved
			cylinder_curved_socket = _mn_utils_style_cartoon.interface.new_socket(name = "Cylinder Curved", in_out='INPUT', socket_type = 'NodeSocketBool', parent = cylinder_panel)
			cylinder_curved_socket.attribute_domain = 'POINT'

			#Socket Cylinder Radius
			cylinder_radius_socket = _mn_utils_style_cartoon.interface.new_socket(name = "Cylinder Radius", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = cylinder_panel)
			cylinder_radius_socket.subtype = 'NONE'
			cylinder_radius_socket.default_value = 2.0
			cylinder_radius_socket.min_value = 0.0
			cylinder_radius_socket.max_value = 10000.0
			cylinder_radius_socket.attribute_domain = 'POINT'

			#Socket Cylinder Resolution
			cylinder_resolution_socket = _mn_utils_style_cartoon.interface.new_socket(name = "Cylinder Resolution", in_out='INPUT', socket_type = 'NodeSocketInt', parent = cylinder_panel)
			cylinder_resolution_socket.subtype = 'NONE'
			cylinder_resolution_socket.default_value = 12
			cylinder_resolution_socket.min_value = 3
			cylinder_resolution_socket.max_value = 512
			cylinder_resolution_socket.attribute_domain = 'POINT'

			#Socket Cylinder Subdivisions
			cylinder_subdivisions_socket = _mn_utils_style_cartoon.interface.new_socket(name = "Cylinder Subdivisions", in_out='INPUT', socket_type = 'NodeSocketInt', parent = cylinder_panel)
			cylinder_subdivisions_socket.subtype = 'NONE'
			cylinder_subdivisions_socket.default_value = 5
			cylinder_subdivisions_socket.min_value = 1
			cylinder_subdivisions_socket.max_value = 2147483647
			cylinder_subdivisions_socket.attribute_domain = 'POINT'


			#Panel Helix
			helix_panel = _mn_utils_style_cartoon.interface.new_panel("Helix")
			#Socket Helix Thickness
			helix_thickness_socket = _mn_utils_style_cartoon.interface.new_socket(name = "Helix Thickness", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = helix_panel)
			helix_thickness_socket.subtype = 'NONE'
			helix_thickness_socket.default_value = 0.5
			helix_thickness_socket.min_value = 0.0
			helix_thickness_socket.max_value = 10000.0
			helix_thickness_socket.attribute_domain = 'POINT'

			#Socket Helix Width
			helix_width_socket = _mn_utils_style_cartoon.interface.new_socket(name = "Helix Width", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = helix_panel)
			helix_width_socket.subtype = 'NONE'
			helix_width_socket.default_value = 2.0
			helix_width_socket.min_value = -3.4028234663852886e+38
			helix_width_socket.max_value = 3.4028234663852886e+38
			helix_width_socket.attribute_domain = 'POINT'

			#Socket Helix Subdivisions
			helix_subdivisions_socket = _mn_utils_style_cartoon.interface.new_socket(name = "Helix Subdivisions", in_out='INPUT', socket_type = 'NodeSocketInt', parent = helix_panel)
			helix_subdivisions_socket.subtype = 'NONE'
			helix_subdivisions_socket.default_value = 5
			helix_subdivisions_socket.min_value = 1
			helix_subdivisions_socket.max_value = 20
			helix_subdivisions_socket.attribute_domain = 'POINT'

			#Socket Helix smoothing
			helix_smoothing_socket = _mn_utils_style_cartoon.interface.new_socket(name = "Helix smoothing", in_out='INPUT', socket_type = 'NodeSocketBool', parent = helix_panel)
			helix_smoothing_socket.attribute_domain = 'POINT'
			helix_smoothing_socket.description = "Smoothen out AH to be more cylindrical."


			#Panel Arrows
			arrows_panel = _mn_utils_style_cartoon.interface.new_panel("Arrows")
			#Socket As Arrows
			as_arrows_socket = _mn_utils_style_cartoon.interface.new_socket(name = "As Arrows", in_out='INPUT', socket_type = 'NodeSocketBool', parent = arrows_panel)
			as_arrows_socket.attribute_domain = 'POINT'
			as_arrows_socket.description = "Render beta-strands with directional arrows."

			#Socket Arrows Sharp
			arrows_sharp_socket = _mn_utils_style_cartoon.interface.new_socket(name = "Arrows Sharp", in_out='INPUT', socket_type = 'NodeSocketBool', parent = arrows_panel)
			arrows_sharp_socket.attribute_domain = 'POINT'

			#Socket Arrows Point
			arrows_point_socket = _mn_utils_style_cartoon.interface.new_socket(name = "Arrows Point", in_out='INPUT', socket_type = 'NodeSocketBool', parent = arrows_panel)
			arrows_point_socket.attribute_domain = 'POINT'

			#Socket Arrow Thickness Scale
			arrow_thickness_scale_socket = _mn_utils_style_cartoon.interface.new_socket(name = "Arrow Thickness Scale", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = arrows_panel)
			arrow_thickness_scale_socket.subtype = 'NONE'
			arrow_thickness_scale_socket.default_value = 1.0
			arrow_thickness_scale_socket.min_value = 0.0
			arrow_thickness_scale_socket.max_value = 10000.0
			arrow_thickness_scale_socket.attribute_domain = 'POINT'

			#Socket Arrow Width Scale
			arrow_width_scale_socket = _mn_utils_style_cartoon.interface.new_socket(name = "Arrow Width Scale", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = arrows_panel)
			arrow_width_scale_socket.subtype = 'NONE'
			arrow_width_scale_socket.default_value = 1.0
			arrow_width_scale_socket.min_value = -10000.0
			arrow_width_scale_socket.max_value = 10000.0
			arrow_width_scale_socket.attribute_domain = 'POINT'


			#Panel Sheet
			sheet_panel = _mn_utils_style_cartoon.interface.new_panel("Sheet")
			#Socket Sheet Rotate
			sheet_rotate_socket = _mn_utils_style_cartoon.interface.new_socket(name = "Sheet Rotate", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = sheet_panel)
			sheet_rotate_socket.subtype = 'NONE'
			sheet_rotate_socket.default_value = 0.0
			sheet_rotate_socket.min_value = -3.4028234663852886e+38
			sheet_rotate_socket.max_value = 3.4028234663852886e+38
			sheet_rotate_socket.attribute_domain = 'POINT'

			#Socket Sheet Thickness
			sheet_thickness_socket = _mn_utils_style_cartoon.interface.new_socket(name = "Sheet Thickness", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = sheet_panel)
			sheet_thickness_socket.subtype = 'NONE'
			sheet_thickness_socket.default_value = 0.5
			sheet_thickness_socket.min_value = 0.0
			sheet_thickness_socket.max_value = 3.4028234663852886e+38
			sheet_thickness_socket.attribute_domain = 'POINT'

			#Socket Sheet Width
			sheet_width_socket = _mn_utils_style_cartoon.interface.new_socket(name = "Sheet Width", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = sheet_panel)
			sheet_width_socket.subtype = 'NONE'
			sheet_width_socket.default_value = 2.0
			sheet_width_socket.min_value = 0.0
			sheet_width_socket.max_value = 10000.0
			sheet_width_socket.attribute_domain = 'POINT'

			#Socket Sheet Smoothing
			sheet_smoothing_socket = _mn_utils_style_cartoon.interface.new_socket(name = "Sheet Smoothing", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = sheet_panel)
			sheet_smoothing_socket.subtype = 'NONE'
			sheet_smoothing_socket.default_value = 1.0
			sheet_smoothing_socket.min_value = 0.0
			sheet_smoothing_socket.max_value = 1.0
			sheet_smoothing_socket.attribute_domain = 'POINT'

			#Socket Sheet Subdivision
			sheet_subdivision_socket = _mn_utils_style_cartoon.interface.new_socket(name = "Sheet Subdivision", in_out='INPUT', socket_type = 'NodeSocketInt', parent = sheet_panel)
			sheet_subdivision_socket.subtype = 'NONE'
			sheet_subdivision_socket.default_value = 3
			sheet_subdivision_socket.min_value = 1
			sheet_subdivision_socket.max_value = 20
			sheet_subdivision_socket.attribute_domain = 'POINT'


			#Panel Loop
			loop_panel = _mn_utils_style_cartoon.interface.new_panel("Loop")
			#Socket Loop Radius
			loop_radius_socket = _mn_utils_style_cartoon.interface.new_socket(name = "Loop Radius", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = loop_panel)
			loop_radius_socket.subtype = 'NONE'
			loop_radius_socket.default_value = 0.30000001192092896
			loop_radius_socket.min_value = 0.0
			loop_radius_socket.max_value = 3.0
			loop_radius_socket.attribute_domain = 'POINT'

			#Socket Loop Subdivisions
			loop_subdivisions_socket = _mn_utils_style_cartoon.interface.new_socket(name = "Loop Subdivisions", in_out='INPUT', socket_type = 'NodeSocketInt', parent = loop_panel)
			loop_subdivisions_socket.subtype = 'NONE'
			loop_subdivisions_socket.default_value = 6
			loop_subdivisions_socket.min_value = 1
			loop_subdivisions_socket.max_value = 2147483647
			loop_subdivisions_socket.attribute_domain = 'POINT'

			#Socket Loop Resolution
			loop_resolution_socket = _mn_utils_style_cartoon.interface.new_socket(name = "Loop Resolution", in_out='INPUT', socket_type = 'NodeSocketInt', parent = loop_panel)
			loop_resolution_socket.subtype = 'NONE'
			loop_resolution_socket.default_value = 8
			loop_resolution_socket.min_value = 3
			loop_resolution_socket.max_value = 512
			loop_resolution_socket.attribute_domain = 'POINT'



			#initialize _mn_utils_style_cartoon nodes
			#node Join Geometry.001
			join_geometry_001 = _mn_utils_style_cartoon.nodes.new("GeometryNodeJoinGeometry")
			join_geometry_001.name = "Join Geometry.001"

			#node Store Named Attribute.002
			store_named_attribute_002_1 = _mn_utils_style_cartoon.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_002_1.name = "Store Named Attribute.002"
			store_named_attribute_002_1.data_type = 'BOOLEAN'
			store_named_attribute_002_1.domain = 'EDGE'
			#Selection
			store_named_attribute_002_1.inputs[1].default_value = True
			#Name
			store_named_attribute_002_1.inputs[2].default_value = "sharp_edge"

			#node Group Input.004
			group_input_004_2 = _mn_utils_style_cartoon.nodes.new("NodeGroupInput")
			group_input_004_2.name = "Group Input.004"
			group_input_004_2.outputs[0].hide = True
			group_input_004_2.outputs[1].hide = True
			group_input_004_2.outputs[2].hide = True
			group_input_004_2.outputs[3].hide = True
			group_input_004_2.outputs[4].hide = True
			group_input_004_2.outputs[5].hide = True
			group_input_004_2.outputs[8].hide = True
			group_input_004_2.outputs[9].hide = True
			group_input_004_2.outputs[10].hide = True
			group_input_004_2.outputs[11].hide = True
			group_input_004_2.outputs[15].hide = True
			group_input_004_2.outputs[18].hide = True
			group_input_004_2.outputs[19].hide = True
			group_input_004_2.outputs[20].hide = True
			group_input_004_2.outputs[21].hide = True
			group_input_004_2.outputs[22].hide = True
			group_input_004_2.outputs[23].hide = True
			group_input_004_2.outputs[24].hide = True
			group_input_004_2.outputs[25].hide = True
			group_input_004_2.outputs[28].hide = True
			group_input_004_2.outputs[29].hide = True

			#node Group Input.007
			group_input_007 = _mn_utils_style_cartoon.nodes.new("NodeGroupInput")
			group_input_007.name = "Group Input.007"
			group_input_007.outputs[0].hide = True
			group_input_007.outputs[1].hide = True
			group_input_007.outputs[3].hide = True
			group_input_007.outputs[4].hide = True
			group_input_007.outputs[5].hide = True
			group_input_007.outputs[6].hide = True
			group_input_007.outputs[7].hide = True
			group_input_007.outputs[8].hide = True
			group_input_007.outputs[9].hide = True
			group_input_007.outputs[10].hide = True
			group_input_007.outputs[11].hide = True
			group_input_007.outputs[12].hide = True
			group_input_007.outputs[13].hide = True
			group_input_007.outputs[14].hide = True
			group_input_007.outputs[15].hide = True
			group_input_007.outputs[16].hide = True
			group_input_007.outputs[19].hide = True
			group_input_007.outputs[20].hide = True
			group_input_007.outputs[21].hide = True
			group_input_007.outputs[22].hide = True
			group_input_007.outputs[23].hide = True
			group_input_007.outputs[24].hide = True
			group_input_007.outputs[25].hide = True
			group_input_007.outputs[26].hide = True
			group_input_007.outputs[27].hide = True
			group_input_007.outputs[28].hide = True
			group_input_007.outputs[29].hide = True

			#node Boolean Math.004
			boolean_math_004_2 = _mn_utils_style_cartoon.nodes.new("FunctionNodeBooleanMath")
			boolean_math_004_2.name = "Boolean Math.004"
			boolean_math_004_2.operation = 'NOT'
			boolean_math_004_2.inputs[1].hide = True

			#node Edge Angle.001
			edge_angle_001 = _mn_utils_style_cartoon.nodes.new("GeometryNodeInputMeshEdgeAngle")
			edge_angle_001.name = "Edge Angle.001"

			#node Compare.006
			compare_006_1 = _mn_utils_style_cartoon.nodes.new("FunctionNodeCompare")
			compare_006_1.name = "Compare.006"
			compare_006_1.data_type = 'FLOAT'
			compare_006_1.mode = 'ELEMENT'
			compare_006_1.operation = 'GREATER_THAN'
			#B
			compare_006_1.inputs[1].default_value = 1.0471975803375244

			#node Boolean Math.002
			boolean_math_002_3 = _mn_utils_style_cartoon.nodes.new("FunctionNodeBooleanMath")
			boolean_math_002_3.name = "Boolean Math.002"
			boolean_math_002_3.operation = 'OR'

			#node Group Output
			group_output_58 = _mn_utils_style_cartoon.nodes.new("NodeGroupOutput")
			group_output_58.name = "Group Output"
			group_output_58.is_active_output = True

			#node Group.001
			group_001_12 = _mn_utils_style_cartoon.nodes.new("GeometryNodeGroup")
			group_001_12.name = "Group.001"
			group_001_12.node_tree = _atoms_to_ca_splines

			#node Group Input
			group_input_58 = _mn_utils_style_cartoon.nodes.new("NodeGroupInput")
			group_input_58.name = "Group Input"
			group_input_58.outputs[2].hide = True
			group_input_58.outputs[3].hide = True
			group_input_58.outputs[4].hide = True
			group_input_58.outputs[5].hide = True
			group_input_58.outputs[6].hide = True
			group_input_58.outputs[7].hide = True
			group_input_58.outputs[8].hide = True
			group_input_58.outputs[9].hide = True
			group_input_58.outputs[10].hide = True
			group_input_58.outputs[11].hide = True
			group_input_58.outputs[12].hide = True
			group_input_58.outputs[13].hide = True
			group_input_58.outputs[14].hide = True
			group_input_58.outputs[15].hide = True
			group_input_58.outputs[16].hide = True
			group_input_58.outputs[17].hide = True
			group_input_58.outputs[18].hide = True
			group_input_58.outputs[19].hide = True
			group_input_58.outputs[20].hide = True
			group_input_58.outputs[21].hide = True
			group_input_58.outputs[22].hide = True
			group_input_58.outputs[23].hide = True
			group_input_58.outputs[25].hide = True
			group_input_58.outputs[26].hide = True
			group_input_58.outputs[27].hide = True
			group_input_58.outputs[28].hide = True
			group_input_58.outputs[29].hide = True

			#node Group Input.001
			group_input_001_10 = _mn_utils_style_cartoon.nodes.new("NodeGroupInput")
			group_input_001_10.name = "Group Input.001"
			group_input_001_10.outputs[0].hide = True
			group_input_001_10.outputs[1].hide = True
			group_input_001_10.outputs[5].hide = True
			group_input_001_10.outputs[6].hide = True
			group_input_001_10.outputs[7].hide = True
			group_input_001_10.outputs[8].hide = True
			group_input_001_10.outputs[9].hide = True
			group_input_001_10.outputs[10].hide = True
			group_input_001_10.outputs[11].hide = True
			group_input_001_10.outputs[12].hide = True
			group_input_001_10.outputs[13].hide = True
			group_input_001_10.outputs[14].hide = True
			group_input_001_10.outputs[15].hide = True
			group_input_001_10.outputs[16].hide = True
			group_input_001_10.outputs[17].hide = True
			group_input_001_10.outputs[18].hide = True
			group_input_001_10.outputs[19].hide = True
			group_input_001_10.outputs[20].hide = True
			group_input_001_10.outputs[21].hide = True
			group_input_001_10.outputs[22].hide = True
			group_input_001_10.outputs[23].hide = True
			group_input_001_10.outputs[24].hide = True
			group_input_001_10.outputs[25].hide = True
			group_input_001_10.outputs[26].hide = True
			group_input_001_10.outputs[27].hide = True
			group_input_001_10.outputs[28].hide = True
			group_input_001_10.outputs[29].hide = True

			#node Group.031
			group_031 = _mn_utils_style_cartoon.nodes.new("GeometryNodeGroup")
			group_031.name = "Group.031"
			group_031.node_tree = _ca_to_loops

			#node Group
			group_20 = _mn_utils_style_cartoon.nodes.new("GeometryNodeGroup")
			group_20.name = "Group"
			group_20.node_tree = _ca_to_sheet

			#node Group.002
			group_002_12 = _mn_utils_style_cartoon.nodes.new("GeometryNodeGroup")
			group_002_12.name = "Group.002"
			group_002_12.node_tree = _ca_to_helix

			#node Reroute.001
			reroute_001_12 = _mn_utils_style_cartoon.nodes.new("NodeReroute")
			reroute_001_12.name = "Reroute.001"
			#node Group.003
			group_003_7 = _mn_utils_style_cartoon.nodes.new("GeometryNodeGroup")
			group_003_7.name = "Group.003"
			group_003_7.node_tree = _cleanup

			#node Reroute
			reroute_14 = _mn_utils_style_cartoon.nodes.new("NodeReroute")
			reroute_14.name = "Reroute"
			#node Reroute.002
			reroute_002_8 = _mn_utils_style_cartoon.nodes.new("NodeReroute")
			reroute_002_8.name = "Reroute.002"
			#node Viewer
			viewer_1 = _mn_utils_style_cartoon.nodes.new("GeometryNodeViewer")
			viewer_1.name = "Viewer"
			viewer_1.data_type = 'FLOAT'
			viewer_1.domain = 'AUTO'
			#Value
			viewer_1.inputs[1].default_value = 0.0




			#Set locations
			join_geometry_001.location = (-3160.0, 1620.0)
			store_named_attribute_002_1.location = (-2800.0, 1600.0)
			group_input_004_2.location = (-3692.57763671875, 1411.1031494140625)
			group_input_007.location = (-3080.0, 1380.0)
			boolean_math_004_2.location = (-2920.0, 1380.0)
			edge_angle_001.location = (-2920.0, 1240.0)
			compare_006_1.location = (-2760.0, 1240.0)
			boolean_math_002_3.location = (-2760.0, 1380.0)
			group_output_58.location = (-2300.0, 1840.0)
			group_001_12.location = (-3820.0, 1720.0)
			group_input_58.location = (-4040.0, 1700.0)
			group_input_001_10.location = (-2740.0, 1820.0)
			group_031.location = (-3360.0, 1140.0)
			group_20.location = (-3360.0, 1400.0)
			group_002_12.location = (-3360.0, 1640.0)
			reroute_001_12.location = (-3460.0, 1680.0)
			group_003_7.location = (-2500.0, 1840.0)
			reroute_14.location = (-2820.0, 1660.0)
			reroute_002_8.location = (-2340.0, 1660.0)
			viewer_1.location = (-2111.49365234375, 1882.300048828125)

			#Set dimensions
			join_geometry_001.width, join_geometry_001.height = 140.0, 100.0
			store_named_attribute_002_1.width, store_named_attribute_002_1.height = 176.01080322265625, 100.0
			group_input_004_2.width, group_input_004_2.height = 140.0, 100.0
			group_input_007.width, group_input_007.height = 140.0, 100.0
			boolean_math_004_2.width, boolean_math_004_2.height = 140.0, 100.0
			edge_angle_001.width, edge_angle_001.height = 140.0, 100.0
			compare_006_1.width, compare_006_1.height = 140.0, 100.0
			boolean_math_002_3.width, boolean_math_002_3.height = 140.0, 100.0
			group_output_58.width, group_output_58.height = 140.0, 100.0
			group_001_12.width, group_001_12.height = 276.27490234375, 100.0
			group_input_58.width, group_input_58.height = 140.0, 100.0
			group_input_001_10.width, group_input_001_10.height = 140.0, 100.0
			group_031.width, group_031.height = 140.0, 100.0
			group_20.width, group_20.height = 140.0, 100.0
			group_002_12.width, group_002_12.height = 140.0, 100.0
			reroute_001_12.width, reroute_001_12.height = 16.0, 100.0
			group_003_7.width, group_003_7.height = 140.0, 100.0
			reroute_14.width, reroute_14.height = 16.0, 100.0
			reroute_002_8.width, reroute_002_8.height = 16.0, 100.0
			viewer_1.width, viewer_1.height = 140.0, 100.0

			#initialize _mn_utils_style_cartoon links
			#group_003_7.Geometry -> group_output_58.Cartoon Mesh
			_mn_utils_style_cartoon.links.new(group_003_7.outputs[0], group_output_58.inputs[0])
			#group_input_58.Atoms -> group_001_12.Atoms
			_mn_utils_style_cartoon.links.new(group_input_58.outputs[0], group_001_12.inputs[0])
			#group_input_58.Selection -> group_001_12.Selection
			_mn_utils_style_cartoon.links.new(group_input_58.outputs[1], group_001_12.inputs[1])
			#group_input_58.Sheet Smoothing -> group_001_12.BS Smoothing
			_mn_utils_style_cartoon.links.new(group_input_58.outputs[24], group_001_12.inputs[2])
			#edge_angle_001.Signed Angle -> compare_006_1.A
			_mn_utils_style_cartoon.links.new(edge_angle_001.outputs[1], compare_006_1.inputs[0])
			#join_geometry_001.Geometry -> store_named_attribute_002_1.Geometry
			_mn_utils_style_cartoon.links.new(join_geometry_001.outputs[0], store_named_attribute_002_1.inputs[0])
			#group_input_007.Shade Smooth -> boolean_math_004_2.Boolean
			_mn_utils_style_cartoon.links.new(group_input_007.outputs[2], boolean_math_004_2.inputs[0])
			#boolean_math_004_2.Boolean -> boolean_math_002_3.Boolean
			_mn_utils_style_cartoon.links.new(boolean_math_004_2.outputs[0], boolean_math_002_3.inputs[0])
			#boolean_math_002_3.Boolean -> store_named_attribute_002_1.Value
			_mn_utils_style_cartoon.links.new(boolean_math_002_3.outputs[0], store_named_attribute_002_1.inputs[3])
			#compare_006_1.Result -> boolean_math_002_3.Boolean
			_mn_utils_style_cartoon.links.new(compare_006_1.outputs[0], boolean_math_002_3.inputs[1])
			#reroute_001_12.Output -> group_031.Geometry
			_mn_utils_style_cartoon.links.new(reroute_001_12.outputs[0], group_031.inputs[0])
			#reroute_001_12.Output -> group_20.Curve
			_mn_utils_style_cartoon.links.new(reroute_001_12.outputs[0], group_20.inputs[0])
			#reroute_001_12.Output -> group_002_12.Curve
			_mn_utils_style_cartoon.links.new(reroute_001_12.outputs[0], group_002_12.inputs[0])
			#group_input_004_2.Helix Thickness -> group_002_12.Thickness
			_mn_utils_style_cartoon.links.new(group_input_004_2.outputs[12], group_002_12.inputs[2])
			#group_input_004_2.Helix Subdivisions -> group_002_12.Subdivisions
			_mn_utils_style_cartoon.links.new(group_input_004_2.outputs[14], group_002_12.inputs[5])
			#group_input_004_2.Profile Resolution -> group_002_12.Profile Resolution
			_mn_utils_style_cartoon.links.new(group_input_004_2.outputs[6], group_002_12.inputs[4])
			#group_input_004_2.Helix Width -> group_002_12.Width
			_mn_utils_style_cartoon.links.new(group_input_004_2.outputs[13], group_002_12.inputs[3])
			#group_input_004_2.As Cylinders -> group_002_12.Boolean
			_mn_utils_style_cartoon.links.new(group_input_004_2.outputs[7], group_002_12.inputs[1])
			#group_input_004_2.Profile Resolution -> group_20.Profile Resolution
			_mn_utils_style_cartoon.links.new(group_input_004_2.outputs[6], group_20.inputs[1])
			#group_input_004_2.Helix Thickness -> group_20.Thickness
			_mn_utils_style_cartoon.links.new(group_input_004_2.outputs[12], group_20.inputs[2])
			#group_input_004_2.Helix Width -> group_20.Width
			_mn_utils_style_cartoon.links.new(group_input_004_2.outputs[13], group_20.inputs[3])
			#group_input_004_2.Helix Subdivisions -> group_20.Subdivisions
			_mn_utils_style_cartoon.links.new(group_input_004_2.outputs[14], group_20.inputs[4])
			#group_031.Geometry -> join_geometry_001.Geometry
			_mn_utils_style_cartoon.links.new(group_031.outputs[0], join_geometry_001.inputs[0])
			#group_001_12.CA Splines -> reroute_001_12.Input
			_mn_utils_style_cartoon.links.new(group_001_12.outputs[0], reroute_001_12.inputs[0])
			#group_input_004_2.Loop Subdivisions -> group_031.Subdivisions
			_mn_utils_style_cartoon.links.new(group_input_004_2.outputs[27], group_031.inputs[1])
			#group_input_004_2.Loop Radius -> group_031.Thickness
			_mn_utils_style_cartoon.links.new(group_input_004_2.outputs[26], group_031.inputs[2])
			#group_input_004_2.Loop Radius -> group_031.Width
			_mn_utils_style_cartoon.links.new(group_input_004_2.outputs[26], group_031.inputs[3])
			#group_input_004_2.As Cylinders -> group_031.As Cylinders
			_mn_utils_style_cartoon.links.new(group_input_004_2.outputs[7], group_031.inputs[4])
			#group_input_004_2.Arrows Sharp -> group_20.Rounded
			_mn_utils_style_cartoon.links.new(group_input_004_2.outputs[17], group_20.inputs[5])
			#group_input_004_2.As Arrows -> group_20.Arrows
			_mn_utils_style_cartoon.links.new(group_input_004_2.outputs[16], group_20.inputs[6])
			#store_named_attribute_002_1.Geometry -> group_003_7.Geometry
			_mn_utils_style_cartoon.links.new(store_named_attribute_002_1.outputs[0], group_003_7.inputs[0])
			#group_input_001_10.Interpolate Color -> group_003_7.Blurred Color
			_mn_utils_style_cartoon.links.new(group_input_001_10.outputs[3], group_003_7.inputs[1])
			#reroute_14.Output -> group_003_7.Color Source
			_mn_utils_style_cartoon.links.new(reroute_14.outputs[0], group_003_7.inputs[2])
			#group_input_001_10.Material -> group_003_7.Material
			_mn_utils_style_cartoon.links.new(group_input_001_10.outputs[4], group_003_7.inputs[3])
			#reroute_002_8.Output -> group_output_58.CA Splines
			_mn_utils_style_cartoon.links.new(reroute_002_8.outputs[0], group_output_58.inputs[1])
			#reroute_001_12.Output -> reroute_14.Input
			_mn_utils_style_cartoon.links.new(reroute_001_12.outputs[0], reroute_14.inputs[0])
			#reroute_14.Output -> reroute_002_8.Input
			_mn_utils_style_cartoon.links.new(reroute_14.outputs[0], reroute_002_8.inputs[0])
			#group_input_001_10.Shade Smooth -> group_003_7.Shade Smooth
			_mn_utils_style_cartoon.links.new(group_input_001_10.outputs[2], group_003_7.inputs[4])
			#group_003_7.Geometry -> viewer_1.Geometry
			_mn_utils_style_cartoon.links.new(group_003_7.outputs[0], viewer_1.inputs[0])
			#group_20.Geometry -> join_geometry_001.Geometry
			_mn_utils_style_cartoon.links.new(group_20.outputs[0], join_geometry_001.inputs[0])
			#group_002_12.Geometry -> join_geometry_001.Geometry
			_mn_utils_style_cartoon.links.new(group_002_12.outputs[0], join_geometry_001.inputs[0])
			return _mn_utils_style_cartoon

		_mn_utils_style_cartoon = _mn_utils_style_cartoon_node_group()

		#initialize is_peptide node group
		def is_peptide_node_group():
			is_peptide = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Is Peptide")

			is_peptide.color_tag = 'INPUT'
			is_peptide.description = ""


			#is_peptide interface
			#Socket Selection
			selection_socket_10 = is_peptide.interface.new_socket(name = "Selection", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			selection_socket_10.attribute_domain = 'POINT'
			selection_socket_10.description = "True if atoms are part of a peptide"

			#Socket Inverted
			inverted_socket_6 = is_peptide.interface.new_socket(name = "Inverted", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			inverted_socket_6.attribute_domain = 'POINT'

			#Socket And
			and_socket_7 = is_peptide.interface.new_socket(name = "And", in_out='INPUT', socket_type = 'NodeSocketBool')
			and_socket_7.attribute_domain = 'POINT'
			and_socket_7.hide_value = True

			#Socket Or
			or_socket_6 = is_peptide.interface.new_socket(name = "Or", in_out='INPUT', socket_type = 'NodeSocketBool')
			or_socket_6.attribute_domain = 'POINT'
			or_socket_6.hide_value = True


			#initialize is_peptide nodes
			#node Group Input
			group_input_59 = is_peptide.nodes.new("NodeGroupInput")
			group_input_59.name = "Group Input"

			#node Group
			group_21 = is_peptide.nodes.new("GeometryNodeGroup")
			group_21.name = "Group"
			group_21.node_tree = _mn_select_peptide

			#node Group Output
			group_output_59 = is_peptide.nodes.new("NodeGroupOutput")
			group_output_59.name = "Group Output"
			group_output_59.is_active_output = True

			#node Group.001
			group_001_13 = is_peptide.nodes.new("GeometryNodeGroup")
			group_001_13.name = "Group.001"
			group_001_13.node_tree = fallback_boolean
			#Socket_2
			group_001_13.inputs[0].default_value = "is_peptide"

			#node Group.002
			group_002_13 = is_peptide.nodes.new("GeometryNodeGroup")
			group_002_13.name = "Group.002"
			group_002_13.node_tree = boolean_andor




			#Set locations
			group_input_59.location = (-200.0, 0.0)
			group_21.location = (-500.0, -120.0)
			group_output_59.location = (180.0, 0.0)
			group_001_13.location = (-200.0, -120.0)
			group_002_13.location = (0.0, 0.0)

			#Set dimensions
			group_input_59.width, group_input_59.height = 140.0, 100.0
			group_21.width, group_21.height = 247.90924072265625, 100.0
			group_output_59.width, group_output_59.height = 140.0, 100.0
			group_001_13.width, group_001_13.height = 140.0, 100.0
			group_002_13.width, group_002_13.height = 140.0, 100.0

			#initialize is_peptide links
			#group_21.Is Peptide -> group_001_13.Fallback
			is_peptide.links.new(group_21.outputs[2], group_001_13.inputs[1])
			#group_input_59.And -> group_002_13.And
			is_peptide.links.new(group_input_59.outputs[0], group_002_13.inputs[0])
			#group_input_59.Or -> group_002_13.Or
			is_peptide.links.new(group_input_59.outputs[1], group_002_13.inputs[1])
			#group_001_13.Boolean -> group_002_13.Boolean
			is_peptide.links.new(group_001_13.outputs[0], group_002_13.inputs[2])
			#group_002_13.Boolean -> group_output_59.Selection
			is_peptide.links.new(group_002_13.outputs[0], group_output_59.inputs[0])
			#group_002_13.Inverted -> group_output_59.Inverted
			is_peptide.links.new(group_002_13.outputs[1], group_output_59.inputs[1])
			return is_peptide

		is_peptide = is_peptide_node_group()

		#initialize boolean_run_mask node group
		def boolean_run_mask_node_group():
			boolean_run_mask = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Boolean Run Mask")

			boolean_run_mask.color_tag = 'CONVERTER'
			boolean_run_mask.description = ""


			#boolean_run_mask interface
			#Socket Boolean
			boolean_socket_10 = boolean_run_mask.interface.new_socket(name = "Boolean", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			boolean_socket_10.attribute_domain = 'POINT'

			#Socket Boolean
			boolean_socket_11 = boolean_run_mask.interface.new_socket(name = "Boolean", in_out='INPUT', socket_type = 'NodeSocketBool')
			boolean_socket_11.attribute_domain = 'POINT'

			#Socket Lag Start
			lag_start_socket = boolean_run_mask.interface.new_socket(name = "Lag Start", in_out='INPUT', socket_type = 'NodeSocketInt')
			lag_start_socket.subtype = 'NONE'
			lag_start_socket.default_value = 0
			lag_start_socket.min_value = 0
			lag_start_socket.max_value = 2147483647
			lag_start_socket.attribute_domain = 'POINT'
			lag_start_socket.description = "The first N values in a run are made to be false"

			#Socket Min Length
			min_length_socket = boolean_run_mask.interface.new_socket(name = "Min Length", in_out='INPUT', socket_type = 'NodeSocketInt')
			min_length_socket.subtype = 'NONE'
			min_length_socket.default_value = 0
			min_length_socket.min_value = 0
			min_length_socket.max_value = 2147483647
			min_length_socket.attribute_domain = 'POINT'
			min_length_socket.description = "Run is only valid if it contains at least N values"

			#Socket Trim End
			trim_end_socket = boolean_run_mask.interface.new_socket(name = "Trim End", in_out='INPUT', socket_type = 'NodeSocketInt')
			trim_end_socket.subtype = 'NONE'
			trim_end_socket.default_value = 0
			trim_end_socket.min_value = -2147483648
			trim_end_socket.max_value = 2147483647
			trim_end_socket.attribute_domain = 'POINT'


			#initialize boolean_run_mask nodes
			#node Group Output
			group_output_60 = boolean_run_mask.nodes.new("NodeGroupOutput")
			group_output_60.name = "Group Output"
			group_output_60.is_active_output = True

			#node Group Input
			group_input_60 = boolean_run_mask.nodes.new("NodeGroupInput")
			group_input_60.name = "Group Input"
			group_input_60.outputs[3].hide = True

			#node Accumulate Field
			accumulate_field_3 = boolean_run_mask.nodes.new("GeometryNodeAccumulateField")
			accumulate_field_3.name = "Accumulate Field"
			accumulate_field_3.data_type = 'INT'
			accumulate_field_3.domain = 'POINT'
			#Group Index
			accumulate_field_3.inputs[1].default_value = 0

			#node Boolean Math.001
			boolean_math_001_9 = boolean_run_mask.nodes.new("FunctionNodeBooleanMath")
			boolean_math_001_9.name = "Boolean Math.001"
			boolean_math_001_9.operation = 'NOT'

			#node Accumulate Field.001
			accumulate_field_001_5 = boolean_run_mask.nodes.new("GeometryNodeAccumulateField")
			accumulate_field_001_5.name = "Accumulate Field.001"
			accumulate_field_001_5.data_type = 'INT'
			accumulate_field_001_5.domain = 'POINT'
			#Value
			accumulate_field_001_5.inputs[0].default_value = 1

			#node Compare
			compare_9 = boolean_run_mask.nodes.new("FunctionNodeCompare")
			compare_9.name = "Compare"
			compare_9.data_type = 'INT'
			compare_9.mode = 'ELEMENT'
			compare_9.operation = 'GREATER_THAN'

			#node Boolean Math.002
			boolean_math_002_4 = boolean_run_mask.nodes.new("FunctionNodeBooleanMath")
			boolean_math_002_4.name = "Boolean Math.002"
			boolean_math_002_4.operation = 'AND'

			#node Reroute
			reroute_15 = boolean_run_mask.nodes.new("NodeReroute")
			reroute_15.name = "Reroute"
			#node Boolean Math.003
			boolean_math_003_2 = boolean_run_mask.nodes.new("FunctionNodeBooleanMath")
			boolean_math_003_2.name = "Boolean Math.003"
			boolean_math_003_2.operation = 'AND'

			#node Compare.001
			compare_001_5 = boolean_run_mask.nodes.new("FunctionNodeCompare")
			compare_001_5.name = "Compare.001"
			compare_001_5.data_type = 'INT'
			compare_001_5.mode = 'ELEMENT'
			compare_001_5.operation = 'GREATER_THAN'

			#node Boolean Math.004
			boolean_math_004_3 = boolean_run_mask.nodes.new("FunctionNodeBooleanMath")
			boolean_math_004_3.name = "Boolean Math.004"
			boolean_math_004_3.operation = 'AND'

			#node Compare.002
			compare_002_6 = boolean_run_mask.nodes.new("FunctionNodeCompare")
			compare_002_6.name = "Compare.002"
			compare_002_6.data_type = 'INT'
			compare_002_6.mode = 'ELEMENT'
			compare_002_6.operation = 'GREATER_THAN'

			#node Math
			math_18 = boolean_run_mask.nodes.new("ShaderNodeMath")
			math_18.name = "Math"
			math_18.operation = 'SUBTRACT'
			math_18.use_clamp = False

			#node Group Input.001
			group_input_001_11 = boolean_run_mask.nodes.new("NodeGroupInput")
			group_input_001_11.name = "Group Input.001"
			group_input_001_11.outputs[0].hide = True
			group_input_001_11.outputs[1].hide = True
			group_input_001_11.outputs[2].hide = True
			group_input_001_11.outputs[4].hide = True




			#Set locations
			group_output_60.location = (860.0001220703125, 60.0)
			group_input_60.location = (-460.0031433105469, 0.0)
			accumulate_field_3.location = (-100.0, -300.0)
			boolean_math_001_9.location = (-260.0, -300.0)
			accumulate_field_001_5.location = (60.0, -300.0)
			compare_9.location = (260.0031433105469, -80.0)
			boolean_math_002_4.location = (260.0, 60.0)
			reroute_15.location = (-260.0031433105469, -29.36541748046875)
			boolean_math_003_2.location = (420.0, 60.0)
			compare_001_5.location = (420.0, -80.0)
			boolean_math_004_3.location = (580.0, 60.0)
			compare_002_6.location = (580.0, -80.0)
			math_18.location = (420.0, -240.0)
			group_input_001_11.location = (580.0, -240.0)

			#Set dimensions
			group_output_60.width, group_output_60.height = 140.0, 100.0
			group_input_60.width, group_input_60.height = 140.0, 100.0
			accumulate_field_3.width, accumulate_field_3.height = 140.0, 100.0
			boolean_math_001_9.width, boolean_math_001_9.height = 140.0, 100.0
			accumulate_field_001_5.width, accumulate_field_001_5.height = 140.0, 100.0
			compare_9.width, compare_9.height = 140.0, 100.0
			boolean_math_002_4.width, boolean_math_002_4.height = 140.0, 100.0
			reroute_15.width, reroute_15.height = 16.0, 100.0
			boolean_math_003_2.width, boolean_math_003_2.height = 140.0, 100.0
			compare_001_5.width, compare_001_5.height = 140.0, 100.0
			boolean_math_004_3.width, boolean_math_004_3.height = 140.0, 100.0
			compare_002_6.width, compare_002_6.height = 140.0, 100.0
			math_18.width, math_18.height = 140.0, 100.0
			group_input_001_11.width, group_input_001_11.height = 140.0, 100.0

			#initialize boolean_run_mask links
			#boolean_math_001_9.Boolean -> accumulate_field_3.Value
			boolean_run_mask.links.new(boolean_math_001_9.outputs[0], accumulate_field_3.inputs[0])
			#reroute_15.Output -> boolean_math_001_9.Boolean
			boolean_run_mask.links.new(reroute_15.outputs[0], boolean_math_001_9.inputs[0])
			#compare_9.Result -> boolean_math_002_4.Boolean
			boolean_run_mask.links.new(compare_9.outputs[0], boolean_math_002_4.inputs[1])
			#group_input_60.Boolean -> reroute_15.Input
			boolean_run_mask.links.new(group_input_60.outputs[0], reroute_15.inputs[0])
			#boolean_math_004_3.Boolean -> group_output_60.Boolean
			boolean_run_mask.links.new(boolean_math_004_3.outputs[0], group_output_60.inputs[0])
			#group_input_60.Lag Start -> compare_9.B
			boolean_run_mask.links.new(group_input_60.outputs[1], compare_9.inputs[3])
			#boolean_math_002_4.Boolean -> boolean_math_003_2.Boolean
			boolean_run_mask.links.new(boolean_math_002_4.outputs[0], boolean_math_003_2.inputs[0])
			#accumulate_field_001_5.Total -> compare_001_5.A
			boolean_run_mask.links.new(accumulate_field_001_5.outputs[2], compare_001_5.inputs[2])
			#group_input_60.Min Length -> compare_001_5.B
			boolean_run_mask.links.new(group_input_60.outputs[2], compare_001_5.inputs[3])
			#compare_001_5.Result -> boolean_math_003_2.Boolean
			boolean_run_mask.links.new(compare_001_5.outputs[0], boolean_math_003_2.inputs[1])
			#reroute_15.Output -> boolean_math_002_4.Boolean
			boolean_run_mask.links.new(reroute_15.outputs[0], boolean_math_002_4.inputs[0])
			#accumulate_field_3.Trailing -> accumulate_field_001_5.Group ID
			boolean_run_mask.links.new(accumulate_field_3.outputs[1], accumulate_field_001_5.inputs[1])
			#boolean_math_003_2.Boolean -> boolean_math_004_3.Boolean
			boolean_run_mask.links.new(boolean_math_003_2.outputs[0], boolean_math_004_3.inputs[0])
			#accumulate_field_001_5.Total -> math_18.Value
			boolean_run_mask.links.new(accumulate_field_001_5.outputs[2], math_18.inputs[0])
			#accumulate_field_001_5.Leading -> math_18.Value
			boolean_run_mask.links.new(accumulate_field_001_5.outputs[0], math_18.inputs[1])
			#math_18.Value -> compare_002_6.A
			boolean_run_mask.links.new(math_18.outputs[0], compare_002_6.inputs[2])
			#group_input_001_11.Trim End -> compare_002_6.B
			boolean_run_mask.links.new(group_input_001_11.outputs[3], compare_002_6.inputs[3])
			#compare_002_6.Result -> boolean_math_004_3.Boolean
			boolean_run_mask.links.new(compare_002_6.outputs[0], boolean_math_004_3.inputs[1])
			#accumulate_field_001_5.Leading -> compare_9.A
			boolean_run_mask.links.new(accumulate_field_001_5.outputs[0], compare_9.inputs[2])
			return boolean_run_mask

		boolean_run_mask = boolean_run_mask_node_group()

		#initialize world_to_angstrom node group
		def world_to_angstrom_node_group():
			world_to_angstrom = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "World to Angstrom")

			world_to_angstrom.color_tag = 'NONE'
			world_to_angstrom.description = ""


			#world_to_angstrom interface
			#Socket Angstrom
			angstrom_socket_3 = world_to_angstrom.interface.new_socket(name = "Angstrom", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
			angstrom_socket_3.subtype = 'NONE'
			angstrom_socket_3.default_value = 0.0
			angstrom_socket_3.min_value = -3.4028234663852886e+38
			angstrom_socket_3.max_value = 3.4028234663852886e+38
			angstrom_socket_3.attribute_domain = 'POINT'

			#Socket World
			world_socket_2 = world_to_angstrom.interface.new_socket(name = "World", in_out='INPUT', socket_type = 'NodeSocketFloat')
			world_socket_2.subtype = 'NONE'
			world_socket_2.default_value = 0.5
			world_socket_2.min_value = -10000.0
			world_socket_2.max_value = 10000.0
			world_socket_2.attribute_domain = 'POINT'


			#initialize world_to_angstrom nodes
			#node Group Output
			group_output_61 = world_to_angstrom.nodes.new("NodeGroupOutput")
			group_output_61.name = "Group Output"
			group_output_61.is_active_output = True

			#node Group Input
			group_input_61 = world_to_angstrom.nodes.new("NodeGroupInput")
			group_input_61.name = "Group Input"

			#node Group
			group_22 = world_to_angstrom.nodes.new("GeometryNodeGroup")
			group_22.name = "Group"
			group_22.node_tree = _mn_world_scale

			#node Math
			math_19 = world_to_angstrom.nodes.new("ShaderNodeMath")
			math_19.name = "Math"
			math_19.operation = 'DIVIDE'
			math_19.use_clamp = False




			#Set locations
			group_output_61.location = (190.0, 0.0)
			group_input_61.location = (-200.0, 0.0)
			group_22.location = (0.0, -80.0)
			math_19.location = (0.0, 80.0)

			#Set dimensions
			group_output_61.width, group_output_61.height = 140.0, 100.0
			group_input_61.width, group_input_61.height = 140.0, 100.0
			group_22.width, group_22.height = 140.0, 100.0
			math_19.width, math_19.height = 140.0, 100.0

			#initialize world_to_angstrom links
			#group_22.world_scale -> math_19.Value
			world_to_angstrom.links.new(group_22.outputs[0], math_19.inputs[1])
			#group_input_61.World -> math_19.Value
			world_to_angstrom.links.new(group_input_61.outputs[0], math_19.inputs[0])
			#math_19.Value -> group_output_61.Angstrom
			world_to_angstrom.links.new(math_19.outputs[0], group_output_61.inputs[0])
			return world_to_angstrom

		world_to_angstrom = world_to_angstrom_node_group()

		#initialize nodegroup_001 node group
		def nodegroup_001_node_group():
			nodegroup_001 = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "NodeGroup.001")

			nodegroup_001.color_tag = 'NONE'
			nodegroup_001.description = ""


			#nodegroup_001 interface
			#Socket Value
			value_socket_7 = nodegroup_001.interface.new_socket(name = "Value", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
			value_socket_7.subtype = 'NONE'
			value_socket_7.default_value = 0.0
			value_socket_7.min_value = -3.4028234663852886e+38
			value_socket_7.max_value = 3.4028234663852886e+38
			value_socket_7.attribute_domain = 'POINT'

			#Socket Vector
			vector_socket_4 = nodegroup_001.interface.new_socket(name = "Vector", in_out='INPUT', socket_type = 'NodeSocketVector')
			vector_socket_4.subtype = 'NONE'
			vector_socket_4.default_value = (0.0, 0.0, 0.0)
			vector_socket_4.min_value = -10000.0
			vector_socket_4.max_value = 10000.0
			vector_socket_4.attribute_domain = 'POINT'

			#Socket Vector
			vector_socket_5 = nodegroup_001.interface.new_socket(name = "Vector", in_out='INPUT', socket_type = 'NodeSocketVector')
			vector_socket_5.subtype = 'NONE'
			vector_socket_5.default_value = (0.0, 0.0, 0.0)
			vector_socket_5.min_value = -10000.0
			vector_socket_5.max_value = 10000.0
			vector_socket_5.attribute_domain = 'POINT'


			#initialize nodegroup_001 nodes
			#node Group Output
			group_output_62 = nodegroup_001.nodes.new("NodeGroupOutput")
			group_output_62.name = "Group Output"
			group_output_62.is_active_output = True

			#node Group Input
			group_input_62 = nodegroup_001.nodes.new("NodeGroupInput")
			group_input_62.name = "Group Input"

			#node Vector Math.002
			vector_math_002_3 = nodegroup_001.nodes.new("ShaderNodeVectorMath")
			vector_math_002_3.name = "Vector Math.002"
			vector_math_002_3.operation = 'DISTANCE'

			#node Math.002
			math_002_3 = nodegroup_001.nodes.new("ShaderNodeMath")
			math_002_3.name = "Math.002"
			math_002_3.operation = 'DIVIDE'
			math_002_3.use_clamp = False
			#Value
			math_002_3.inputs[0].default_value = 1.0

			#node Group.001
			group_001_14 = nodegroup_001.nodes.new("GeometryNodeGroup")
			group_001_14.name = "Group.001"
			group_001_14.node_tree = world_to_angstrom




			#Set locations
			group_output_62.location = (670.8533325195312, -4.1087493896484375)
			group_input_62.location = (-280.0, 0.0)
			vector_math_002_3.location = (-80.0, 0.0)
			math_002_3.location = (260.0, 0.0)
			group_001_14.location = (80.0, 0.0)

			#Set dimensions
			group_output_62.width, group_output_62.height = 140.0, 100.0
			group_input_62.width, group_input_62.height = 140.0, 100.0
			vector_math_002_3.width, vector_math_002_3.height = 140.0, 100.0
			math_002_3.width, math_002_3.height = 140.0, 100.0
			group_001_14.width, group_001_14.height = 152.50686645507812, 100.0

			#initialize nodegroup_001 links
			#group_001_14.Angstrom -> math_002_3.Value
			nodegroup_001.links.new(group_001_14.outputs[0], math_002_3.inputs[1])
			#group_input_62.Vector -> vector_math_002_3.Vector
			nodegroup_001.links.new(group_input_62.outputs[1], vector_math_002_3.inputs[1])
			#group_input_62.Vector -> vector_math_002_3.Vector
			nodegroup_001.links.new(group_input_62.outputs[0], vector_math_002_3.inputs[0])
			#math_002_3.Value -> group_output_62.Value
			nodegroup_001.links.new(math_002_3.outputs[0], group_output_62.inputs[0])
			#vector_math_002_3.Value -> group_001_14.World
			nodegroup_001.links.new(vector_math_002_3.outputs[1], group_001_14.inputs[0])
			return nodegroup_001

		nodegroup_001 = nodegroup_001_node_group()

		#initialize hbond_energy node group
		def hbond_energy_node_group():
			hbond_energy = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "HBond Energy")

			hbond_energy.color_tag = 'NONE'
			hbond_energy.description = ""


			#hbond_energy interface
			#Socket Is Bonded
			is_bonded_socket = hbond_energy.interface.new_socket(name = "Is Bonded", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			is_bonded_socket.attribute_domain = 'POINT'

			#Socket Bond Energy
			bond_energy_socket = hbond_energy.interface.new_socket(name = "Bond Energy", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
			bond_energy_socket.subtype = 'NONE'
			bond_energy_socket.default_value = 0.0
			bond_energy_socket.min_value = -3.4028234663852886e+38
			bond_energy_socket.max_value = 3.4028234663852886e+38
			bond_energy_socket.attribute_domain = 'POINT'

			#Socket Bond Vector
			bond_vector_socket = hbond_energy.interface.new_socket(name = "Bond Vector", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			bond_vector_socket.subtype = 'NONE'
			bond_vector_socket.default_value = (0.0, 0.0, 0.0)
			bond_vector_socket.min_value = -3.4028234663852886e+38
			bond_vector_socket.max_value = 3.4028234663852886e+38
			bond_vector_socket.attribute_domain = 'POINT'

			#Socket O
			o_socket_1 = hbond_energy.interface.new_socket(name = "O", in_out='INPUT', socket_type = 'NodeSocketVector')
			o_socket_1.subtype = 'NONE'
			o_socket_1.default_value = (0.0, 0.0, 0.0)
			o_socket_1.min_value = -3.4028234663852886e+38
			o_socket_1.max_value = 3.4028234663852886e+38
			o_socket_1.attribute_domain = 'POINT'

			#Socket C
			c_socket_1 = hbond_energy.interface.new_socket(name = "C", in_out='INPUT', socket_type = 'NodeSocketVector')
			c_socket_1.subtype = 'NONE'
			c_socket_1.default_value = (0.0, 0.0, 0.0)
			c_socket_1.min_value = -3.4028234663852886e+38
			c_socket_1.max_value = 3.4028234663852886e+38
			c_socket_1.attribute_domain = 'POINT'

			#Socket N
			n_socket_1 = hbond_energy.interface.new_socket(name = "N", in_out='INPUT', socket_type = 'NodeSocketVector')
			n_socket_1.subtype = 'NONE'
			n_socket_1.default_value = (0.0, 0.0, 0.0)
			n_socket_1.min_value = -3.4028234663852886e+38
			n_socket_1.max_value = 3.4028234663852886e+38
			n_socket_1.attribute_domain = 'POINT'

			#Socket H
			h_socket = hbond_energy.interface.new_socket(name = "H", in_out='INPUT', socket_type = 'NodeSocketVector')
			h_socket.subtype = 'NONE'
			h_socket.default_value = (0.0, 0.0, 0.0)
			h_socket.min_value = -3.4028234663852886e+38
			h_socket.max_value = 3.4028234663852886e+38
			h_socket.attribute_domain = 'POINT'


			#initialize hbond_energy nodes
			#node Group Output
			group_output_63 = hbond_energy.nodes.new("NodeGroupOutput")
			group_output_63.name = "Group Output"
			group_output_63.is_active_output = True

			#node Group Input
			group_input_63 = hbond_energy.nodes.new("NodeGroupInput")
			group_input_63.name = "Group Input"

			#node Group.003
			group_003_8 = hbond_energy.nodes.new("GeometryNodeGroup")
			group_003_8.label = "1/r(ON)"
			group_003_8.name = "Group.003"
			group_003_8.node_tree = nodegroup_001

			#node Group.008
			group_008_2 = hbond_energy.nodes.new("GeometryNodeGroup")
			group_008_2.label = "1/r(CH)"
			group_008_2.name = "Group.008"
			group_008_2.node_tree = nodegroup_001

			#node Group.009
			group_009_2 = hbond_energy.nodes.new("GeometryNodeGroup")
			group_009_2.label = "1/r(OH)"
			group_009_2.name = "Group.009"
			group_009_2.node_tree = nodegroup_001

			#node Group.010
			group_010_3 = hbond_energy.nodes.new("GeometryNodeGroup")
			group_010_3.label = "1/r(CN)"
			group_010_3.name = "Group.010"
			group_010_3.node_tree = nodegroup_001

			#node Math.002
			math_002_4 = hbond_energy.nodes.new("ShaderNodeMath")
			math_002_4.name = "Math.002"
			math_002_4.hide = True
			math_002_4.operation = 'ADD'
			math_002_4.use_clamp = False

			#node Math.003
			math_003_2 = hbond_energy.nodes.new("ShaderNodeMath")
			math_003_2.name = "Math.003"
			math_003_2.hide = True
			math_003_2.operation = 'SUBTRACT'
			math_003_2.use_clamp = False

			#node Math.004
			math_004_1 = hbond_energy.nodes.new("ShaderNodeMath")
			math_004_1.name = "Math.004"
			math_004_1.hide = True
			math_004_1.operation = 'SUBTRACT'
			math_004_1.use_clamp = False

			#node Math.005
			math_005_1 = hbond_energy.nodes.new("ShaderNodeMath")
			math_005_1.label = "* q1q2"
			math_005_1.name = "Math.005"
			math_005_1.operation = 'MULTIPLY'
			math_005_1.use_clamp = False
			#Value_001
			math_005_1.inputs[1].default_value = 0.08399999886751175

			#node Math.006
			math_006_1 = hbond_energy.nodes.new("ShaderNodeMath")
			math_006_1.label = "*f"
			math_006_1.name = "Math.006"
			math_006_1.operation = 'MULTIPLY'
			math_006_1.use_clamp = False
			#Value_001
			math_006_1.inputs[1].default_value = 332.0

			#node Vector Math
			vector_math_4 = hbond_energy.nodes.new("ShaderNodeVectorMath")
			vector_math_4.name = "Vector Math"
			vector_math_4.operation = 'SUBTRACT'

			#node Math.007
			math_007_1 = hbond_energy.nodes.new("ShaderNodeMath")
			math_007_1.label = "*e"
			math_007_1.name = "Math.007"
			math_007_1.mute = True
			math_007_1.operation = 'MULTIPLY'
			math_007_1.use_clamp = False
			#Value_001
			math_007_1.inputs[1].default_value = -1.0

			#node Compare
			compare_10 = hbond_energy.nodes.new("FunctionNodeCompare")
			compare_10.label = "Cutoff kcal/mol"
			compare_10.name = "Compare"
			compare_10.data_type = 'FLOAT'
			compare_10.mode = 'ELEMENT'
			compare_10.operation = 'LESS_THAN'
			#B
			compare_10.inputs[1].default_value = -0.5

			#node Group Input.001
			group_input_001_12 = hbond_energy.nodes.new("NodeGroupInput")
			group_input_001_12.name = "Group Input.001"




			#Set locations
			group_output_63.location = (900.0, 40.0)
			group_input_63.location = (-644.257568359375, 10.571624755859375)
			group_003_8.location = (-355.197021484375, 210.6334228515625)
			group_008_2.location = (-360.0, 69.3665771484375)
			group_009_2.location = (-360.0, -70.6334228515625)
			group_010_3.location = (-360.0, -210.6334228515625)
			math_002_4.location = (-180.0, 60.0)
			math_003_2.location = (-180.0, -80.0)
			math_004_1.location = (-180.0, -220.0)
			math_005_1.location = (320.0, 100.0)
			math_006_1.location = (480.0, 100.0)
			vector_math_4.location = (480.0, -60.0)
			math_007_1.location = (160.0, 100.0)
			compare_10.location = (720.0, 220.0)
			group_input_001_12.location = (320.0, -60.0)

			#Set dimensions
			group_output_63.width, group_output_63.height = 140.0, 100.0
			group_input_63.width, group_input_63.height = 140.0, 100.0
			group_003_8.width, group_003_8.height = 140.0, 100.0
			group_008_2.width, group_008_2.height = 140.0, 100.0
			group_009_2.width, group_009_2.height = 140.0, 100.0
			group_010_3.width, group_010_3.height = 140.0, 100.0
			math_002_4.width, math_002_4.height = 140.0, 100.0
			math_003_2.width, math_003_2.height = 140.0, 100.0
			math_004_1.width, math_004_1.height = 140.0, 100.0
			math_005_1.width, math_005_1.height = 140.0, 100.0
			math_006_1.width, math_006_1.height = 140.0, 100.0
			vector_math_4.width, vector_math_4.height = 140.0, 100.0
			math_007_1.width, math_007_1.height = 140.0, 100.0
			compare_10.width, compare_10.height = 140.0, 100.0
			group_input_001_12.width, group_input_001_12.height = 140.0, 100.0

			#initialize hbond_energy links
			#math_002_4.Value -> math_003_2.Value
			hbond_energy.links.new(math_002_4.outputs[0], math_003_2.inputs[0])
			#group_009_2.Value -> math_003_2.Value
			hbond_energy.links.new(group_009_2.outputs[0], math_003_2.inputs[1])
			#math_007_1.Value -> math_005_1.Value
			hbond_energy.links.new(math_007_1.outputs[0], math_005_1.inputs[0])
			#group_008_2.Value -> math_002_4.Value
			hbond_energy.links.new(group_008_2.outputs[0], math_002_4.inputs[1])
			#math_003_2.Value -> math_004_1.Value
			hbond_energy.links.new(math_003_2.outputs[0], math_004_1.inputs[0])
			#group_010_3.Value -> math_004_1.Value
			hbond_energy.links.new(group_010_3.outputs[0], math_004_1.inputs[1])
			#group_003_8.Value -> math_002_4.Value
			hbond_energy.links.new(group_003_8.outputs[0], math_002_4.inputs[0])
			#math_005_1.Value -> math_006_1.Value
			hbond_energy.links.new(math_005_1.outputs[0], math_006_1.inputs[0])
			#math_006_1.Value -> group_output_63.Bond Energy
			hbond_energy.links.new(math_006_1.outputs[0], group_output_63.inputs[1])
			#math_004_1.Value -> math_007_1.Value
			hbond_energy.links.new(math_004_1.outputs[0], math_007_1.inputs[0])
			#vector_math_4.Vector -> group_output_63.Bond Vector
			hbond_energy.links.new(vector_math_4.outputs[0], group_output_63.inputs[2])
			#math_006_1.Value -> compare_10.A
			hbond_energy.links.new(math_006_1.outputs[0], compare_10.inputs[0])
			#compare_10.Result -> group_output_63.Is Bonded
			hbond_energy.links.new(compare_10.outputs[0], group_output_63.inputs[0])
			#group_input_63.O -> group_003_8.Vector
			hbond_energy.links.new(group_input_63.outputs[0], group_003_8.inputs[0])
			#group_input_63.N -> group_003_8.Vector
			hbond_energy.links.new(group_input_63.outputs[2], group_003_8.inputs[1])
			#group_input_63.C -> group_008_2.Vector
			hbond_energy.links.new(group_input_63.outputs[1], group_008_2.inputs[0])
			#group_input_63.H -> group_008_2.Vector
			hbond_energy.links.new(group_input_63.outputs[3], group_008_2.inputs[1])
			#group_input_63.O -> group_009_2.Vector
			hbond_energy.links.new(group_input_63.outputs[0], group_009_2.inputs[0])
			#group_input_63.H -> group_009_2.Vector
			hbond_energy.links.new(group_input_63.outputs[3], group_009_2.inputs[1])
			#group_input_63.C -> group_010_3.Vector
			hbond_energy.links.new(group_input_63.outputs[1], group_010_3.inputs[0])
			#group_input_63.N -> group_010_3.Vector
			hbond_energy.links.new(group_input_63.outputs[2], group_010_3.inputs[1])
			#group_input_001_12.H -> vector_math_4.Vector
			hbond_energy.links.new(group_input_001_12.outputs[3], vector_math_4.inputs[1])
			#group_input_001_12.O -> vector_math_4.Vector
			hbond_energy.links.new(group_input_001_12.outputs[0], vector_math_4.inputs[0])
			return hbond_energy

		hbond_energy = hbond_energy_node_group()

		#initialize backbone_nh node group
		def backbone_nh_node_group():
			backbone_nh = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Backbone NH")

			backbone_nh.color_tag = 'NONE'
			backbone_nh.description = ""


			#backbone_nh interface
			#Socket H
			h_socket_1 = backbone_nh.interface.new_socket(name = "H", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			h_socket_1.subtype = 'NONE'
			h_socket_1.default_value = (0.0, 0.0, 0.0)
			h_socket_1.min_value = -3.4028234663852886e+38
			h_socket_1.max_value = 3.4028234663852886e+38
			h_socket_1.attribute_domain = 'POINT'

			#Socket Value
			value_socket_8 = backbone_nh.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat')
			value_socket_8.subtype = 'NONE'
			value_socket_8.default_value = 1.0
			value_socket_8.min_value = -10000.0
			value_socket_8.max_value = 10000.0
			value_socket_8.attribute_domain = 'POINT'


			#initialize backbone_nh nodes
			#node Group Output
			group_output_64 = backbone_nh.nodes.new("NodeGroupOutput")
			group_output_64.name = "Group Output"
			group_output_64.is_active_output = True

			#node Group Input
			group_input_64 = backbone_nh.nodes.new("NodeGroupInput")
			group_input_64.name = "Group Input"

			#node Named Attribute
			named_attribute_7 = backbone_nh.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_7.name = "Named Attribute"
			named_attribute_7.data_type = 'FLOAT_VECTOR'
			#Name
			named_attribute_7.inputs[0].default_value = "backbone_N"

			#node Named Attribute.001
			named_attribute_001_4 = backbone_nh.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_001_4.name = "Named Attribute.001"
			named_attribute_001_4.data_type = 'FLOAT_VECTOR'
			#Name
			named_attribute_001_4.inputs[0].default_value = "backbone_CA"

			#node Named Attribute.002
			named_attribute_002_3 = backbone_nh.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_002_3.name = "Named Attribute.002"
			named_attribute_002_3.data_type = 'FLOAT_VECTOR'
			#Name
			named_attribute_002_3.inputs[0].default_value = "backbone_C"

			#node Group.002
			group_002_14 = backbone_nh.nodes.new("GeometryNodeGroup")
			group_002_14.name = "Group.002"
			group_002_14.node_tree = offset_vector
			#Socket_2
			group_002_14.inputs[0].default_value = 0
			#Socket_3
			group_002_14.inputs[2].default_value = -1

			#node Vector Math
			vector_math_5 = backbone_nh.nodes.new("ShaderNodeVectorMath")
			vector_math_5.name = "Vector Math"
			vector_math_5.operation = 'SUBTRACT'

			#node Vector Math.001
			vector_math_001_3 = backbone_nh.nodes.new("ShaderNodeVectorMath")
			vector_math_001_3.name = "Vector Math.001"
			vector_math_001_3.operation = 'SUBTRACT'

			#node Vector Math.002
			vector_math_002_4 = backbone_nh.nodes.new("ShaderNodeVectorMath")
			vector_math_002_4.name = "Vector Math.002"
			vector_math_002_4.operation = 'NORMALIZE'

			#node Vector Math.003
			vector_math_003 = backbone_nh.nodes.new("ShaderNodeVectorMath")
			vector_math_003.name = "Vector Math.003"
			vector_math_003.operation = 'NORMALIZE'

			#node Vector Math.005
			vector_math_005_1 = backbone_nh.nodes.new("ShaderNodeVectorMath")
			vector_math_005_1.name = "Vector Math.005"
			vector_math_005_1.operation = 'ADD'

			#node Vector Math.006
			vector_math_006_1 = backbone_nh.nodes.new("ShaderNodeVectorMath")
			vector_math_006_1.name = "Vector Math.006"
			vector_math_006_1.operation = 'ADD'

			#node Vector Math.004
			vector_math_004_1 = backbone_nh.nodes.new("ShaderNodeVectorMath")
			vector_math_004_1.name = "Vector Math.004"
			vector_math_004_1.operation = 'SCALE'

			#node Group.003
			group_003_9 = backbone_nh.nodes.new("GeometryNodeGroup")
			group_003_9.name = "Group.003"
			group_003_9.node_tree = mn_units

			#node Vector Math.007
			vector_math_007 = backbone_nh.nodes.new("ShaderNodeVectorMath")
			vector_math_007.name = "Vector Math.007"
			vector_math_007.operation = 'NORMALIZE'




			#Set locations
			group_output_64.location = (620.0, 0.0)
			group_input_64.location = (-630.0, 0.0)
			named_attribute_7.location = (-430.0, 140.0)
			named_attribute_001_4.location = (-430.0, 0.0)
			named_attribute_002_3.location = (-430.0, -140.0)
			group_002_14.location = (-210.0, -120.0)
			vector_math_5.location = (-50.0, 0.0)
			vector_math_001_3.location = (-50.0, 140.0)
			vector_math_002_4.location = (110.0, 140.0)
			vector_math_003.location = (110.0, 0.0)
			vector_math_005_1.location = (270.0, 140.0)
			vector_math_006_1.location = (430.0, 140.0)
			vector_math_004_1.location = (260.0, -120.0)
			group_003_9.location = (100.0, -120.0)
			vector_math_007.location = (260.0, 0.0)

			#Set dimensions
			group_output_64.width, group_output_64.height = 140.0, 100.0
			group_input_64.width, group_input_64.height = 140.0, 100.0
			named_attribute_7.width, named_attribute_7.height = 189.579833984375, 100.0
			named_attribute_001_4.width, named_attribute_001_4.height = 189.579833984375, 100.0
			named_attribute_002_3.width, named_attribute_002_3.height = 189.579833984375, 100.0
			group_002_14.width, group_002_14.height = 140.0, 100.0
			vector_math_5.width, vector_math_5.height = 140.0, 100.0
			vector_math_001_3.width, vector_math_001_3.height = 140.0, 100.0
			vector_math_002_4.width, vector_math_002_4.height = 140.0, 100.0
			vector_math_003.width, vector_math_003.height = 140.0, 100.0
			vector_math_005_1.width, vector_math_005_1.height = 140.0, 100.0
			vector_math_006_1.width, vector_math_006_1.height = 140.0, 100.0
			vector_math_004_1.width, vector_math_004_1.height = 140.0, 100.0
			group_003_9.width, group_003_9.height = 140.0, 100.0
			vector_math_007.width, vector_math_007.height = 140.0, 100.0

			#initialize backbone_nh links
			#vector_math_004_1.Vector -> vector_math_006_1.Vector
			backbone_nh.links.new(vector_math_004_1.outputs[0], vector_math_006_1.inputs[1])
			#named_attribute_001_4.Attribute -> vector_math_001_3.Vector
			backbone_nh.links.new(named_attribute_001_4.outputs[0], vector_math_001_3.inputs[1])
			#named_attribute_002_3.Attribute -> group_002_14.Vector
			backbone_nh.links.new(named_attribute_002_3.outputs[0], group_002_14.inputs[1])
			#named_attribute_7.Attribute -> vector_math_5.Vector
			backbone_nh.links.new(named_attribute_7.outputs[0], vector_math_5.inputs[0])
			#vector_math_5.Vector -> vector_math_003.Vector
			backbone_nh.links.new(vector_math_5.outputs[0], vector_math_003.inputs[0])
			#group_003_9.Angstrom -> vector_math_004_1.Scale
			backbone_nh.links.new(group_003_9.outputs[0], vector_math_004_1.inputs[3])
			#vector_math_003.Vector -> vector_math_005_1.Vector
			backbone_nh.links.new(vector_math_003.outputs[0], vector_math_005_1.inputs[1])
			#group_002_14.Value -> vector_math_5.Vector
			backbone_nh.links.new(group_002_14.outputs[0], vector_math_5.inputs[1])
			#vector_math_002_4.Vector -> vector_math_005_1.Vector
			backbone_nh.links.new(vector_math_002_4.outputs[0], vector_math_005_1.inputs[0])
			#named_attribute_7.Attribute -> vector_math_001_3.Vector
			backbone_nh.links.new(named_attribute_7.outputs[0], vector_math_001_3.inputs[0])
			#vector_math_001_3.Vector -> vector_math_002_4.Vector
			backbone_nh.links.new(vector_math_001_3.outputs[0], vector_math_002_4.inputs[0])
			#named_attribute_7.Attribute -> vector_math_006_1.Vector
			backbone_nh.links.new(named_attribute_7.outputs[0], vector_math_006_1.inputs[0])
			#vector_math_006_1.Vector -> group_output_64.H
			backbone_nh.links.new(vector_math_006_1.outputs[0], group_output_64.inputs[0])
			#group_input_64.Value -> group_003_9.Value
			backbone_nh.links.new(group_input_64.outputs[0], group_003_9.inputs[0])
			#vector_math_005_1.Vector -> vector_math_007.Vector
			backbone_nh.links.new(vector_math_005_1.outputs[0], vector_math_007.inputs[0])
			#vector_math_007.Vector -> vector_math_004_1.Vector
			backbone_nh.links.new(vector_math_007.outputs[0], vector_math_004_1.inputs[0])
			return backbone_nh

		backbone_nh = backbone_nh_node_group()

		#initialize mn_topo_backbone node group
		def mn_topo_backbone_node_group():
			mn_topo_backbone = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "MN_topo_backbone")

			mn_topo_backbone.color_tag = 'NONE'
			mn_topo_backbone.description = ""


			#mn_topo_backbone interface
			#Socket O
			o_socket_2 = mn_topo_backbone.interface.new_socket(name = "O", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			o_socket_2.subtype = 'NONE'
			o_socket_2.default_value = (0.0, 0.0, 0.0)
			o_socket_2.min_value = -3.4028234663852886e+38
			o_socket_2.max_value = 3.4028234663852886e+38
			o_socket_2.attribute_domain = 'POINT'

			#Socket C
			c_socket_2 = mn_topo_backbone.interface.new_socket(name = "C", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			c_socket_2.subtype = 'NONE'
			c_socket_2.default_value = (0.0, 0.0, 0.0)
			c_socket_2.min_value = -3.4028234663852886e+38
			c_socket_2.max_value = 3.4028234663852886e+38
			c_socket_2.attribute_domain = 'POINT'

			#Socket CA
			ca_socket_1 = mn_topo_backbone.interface.new_socket(name = "CA", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			ca_socket_1.subtype = 'NONE'
			ca_socket_1.default_value = (0.0, 0.0, 0.0)
			ca_socket_1.min_value = -3.4028234663852886e+38
			ca_socket_1.max_value = 3.4028234663852886e+38
			ca_socket_1.attribute_domain = 'POINT'

			#Socket N
			n_socket_2 = mn_topo_backbone.interface.new_socket(name = "N", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			n_socket_2.subtype = 'NONE'
			n_socket_2.default_value = (0.0, 0.0, 0.0)
			n_socket_2.min_value = -3.4028234663852886e+38
			n_socket_2.max_value = 3.4028234663852886e+38
			n_socket_2.attribute_domain = 'POINT'

			#Socket NH
			nh_socket = mn_topo_backbone.interface.new_socket(name = "NH", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			nh_socket.subtype = 'NONE'
			nh_socket.default_value = (0.0, 0.0, 0.0)
			nh_socket.min_value = -3.4028234663852886e+38
			nh_socket.max_value = 3.4028234663852886e+38
			nh_socket.attribute_domain = 'POINT'

			#Socket Offset
			offset_socket_9 = mn_topo_backbone.interface.new_socket(name = "Offset", in_out='INPUT', socket_type = 'NodeSocketInt')
			offset_socket_9.subtype = 'NONE'
			offset_socket_9.default_value = 0
			offset_socket_9.min_value = -2147483648
			offset_socket_9.max_value = 2147483647
			offset_socket_9.attribute_domain = 'POINT'


			#initialize mn_topo_backbone nodes
			#node Group Output
			group_output_65 = mn_topo_backbone.nodes.new("NodeGroupOutput")
			group_output_65.name = "Group Output"
			group_output_65.is_active_output = True

			#node Group Input
			group_input_65 = mn_topo_backbone.nodes.new("NodeGroupInput")
			group_input_65.name = "Group Input"

			#node Named Attribute.001
			named_attribute_001_5 = mn_topo_backbone.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_001_5.name = "Named Attribute.001"
			named_attribute_001_5.data_type = 'FLOAT_VECTOR'
			#Name
			named_attribute_001_5.inputs[0].default_value = "backbone_O"

			#node Named Attribute.002
			named_attribute_002_4 = mn_topo_backbone.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_002_4.name = "Named Attribute.002"
			named_attribute_002_4.data_type = 'FLOAT_VECTOR'
			#Name
			named_attribute_002_4.inputs[0].default_value = "backbone_C"

			#node Evaluate at Index
			evaluate_at_index_5 = mn_topo_backbone.nodes.new("GeometryNodeFieldAtIndex")
			evaluate_at_index_5.name = "Evaluate at Index"
			evaluate_at_index_5.data_type = 'FLOAT_VECTOR'
			evaluate_at_index_5.domain = 'POINT'

			#node Math
			math_20 = mn_topo_backbone.nodes.new("ShaderNodeMath")
			math_20.name = "Math"
			math_20.operation = 'ADD'
			math_20.use_clamp = False

			#node Index
			index_4 = mn_topo_backbone.nodes.new("GeometryNodeInputIndex")
			index_4.name = "Index"

			#node Evaluate at Index.001
			evaluate_at_index_001_2 = mn_topo_backbone.nodes.new("GeometryNodeFieldAtIndex")
			evaluate_at_index_001_2.name = "Evaluate at Index.001"
			evaluate_at_index_001_2.data_type = 'FLOAT_VECTOR'
			evaluate_at_index_001_2.domain = 'POINT'

			#node Named Attribute.003
			named_attribute_003_1 = mn_topo_backbone.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_003_1.name = "Named Attribute.003"
			named_attribute_003_1.data_type = 'FLOAT_VECTOR'
			#Name
			named_attribute_003_1.inputs[0].default_value = "backbone_CA"

			#node Evaluate at Index.002
			evaluate_at_index_002_1 = mn_topo_backbone.nodes.new("GeometryNodeFieldAtIndex")
			evaluate_at_index_002_1.name = "Evaluate at Index.002"
			evaluate_at_index_002_1.data_type = 'FLOAT_VECTOR'
			evaluate_at_index_002_1.domain = 'POINT'

			#node Evaluate at Index.003
			evaluate_at_index_003_1 = mn_topo_backbone.nodes.new("GeometryNodeFieldAtIndex")
			evaluate_at_index_003_1.name = "Evaluate at Index.003"
			evaluate_at_index_003_1.data_type = 'FLOAT_VECTOR'
			evaluate_at_index_003_1.domain = 'POINT'

			#node Named Attribute.004
			named_attribute_004_1 = mn_topo_backbone.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_004_1.name = "Named Attribute.004"
			named_attribute_004_1.data_type = 'FLOAT_VECTOR'
			#Name
			named_attribute_004_1.inputs[0].default_value = "backbone_N"

			#node Reroute
			reroute_16 = mn_topo_backbone.nodes.new("NodeReroute")
			reroute_16.name = "Reroute"
			#node Group
			group_23 = mn_topo_backbone.nodes.new("GeometryNodeGroup")
			group_23.name = "Group"
			group_23.node_tree = backbone_nh
			#Socket_1
			group_23.inputs[0].default_value = 1.0099999904632568

			#node Evaluate at Index.004
			evaluate_at_index_004_1 = mn_topo_backbone.nodes.new("GeometryNodeFieldAtIndex")
			evaluate_at_index_004_1.name = "Evaluate at Index.004"
			evaluate_at_index_004_1.data_type = 'FLOAT_VECTOR'
			evaluate_at_index_004_1.domain = 'POINT'

			#node Named Attribute.005
			named_attribute_005_1 = mn_topo_backbone.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_005_1.name = "Named Attribute.005"
			named_attribute_005_1.data_type = 'FLOAT_VECTOR'
			#Name
			named_attribute_005_1.inputs[0].default_value = "backbone_NH"

			#node Switch
			switch_13 = mn_topo_backbone.nodes.new("GeometryNodeSwitch")
			switch_13.name = "Switch"
			switch_13.input_type = 'VECTOR'

			#node Boolean Math
			boolean_math_12 = mn_topo_backbone.nodes.new("FunctionNodeBooleanMath")
			boolean_math_12.name = "Boolean Math"
			boolean_math_12.operation = 'NOT'




			#Set locations
			group_output_65.location = (320.0, -220.0)
			group_input_65.location = (-520.0, -260.0)
			named_attribute_001_5.location = (-300.0, 40.0)
			named_attribute_002_4.location = (-300.0, -100.0)
			evaluate_at_index_5.location = (80.0, -14.04681396484375)
			math_20.location = (-260.0, -260.0)
			index_4.location = (-520.0, -360.0)
			evaluate_at_index_001_2.location = (80.0, -170.47593688964844)
			named_attribute_003_1.location = (-300.0, -460.0)
			evaluate_at_index_002_1.location = (80.0, -326.90509033203125)
			evaluate_at_index_003_1.location = (80.0, -480.0)
			named_attribute_004_1.location = (-300.0, -600.0)
			reroute_16.location = (20.0, -340.0)
			group_23.location = (-640.0, -920.0)
			evaluate_at_index_004_1.location = (77.81956481933594, -655.5125732421875)
			named_attribute_005_1.location = (-640.0, -780.0)
			switch_13.location = (-240.0, -780.0)
			boolean_math_12.location = (-420.0, -780.0)

			#Set dimensions
			group_output_65.width, group_output_65.height = 140.0, 100.0
			group_input_65.width, group_input_65.height = 140.0, 100.0
			named_attribute_001_5.width, named_attribute_001_5.height = 186.42977905273438, 100.0
			named_attribute_002_4.width, named_attribute_002_4.height = 186.42977905273438, 100.0
			evaluate_at_index_5.width, evaluate_at_index_5.height = 140.0, 100.0
			math_20.width, math_20.height = 140.0, 100.0
			index_4.width, index_4.height = 140.0, 100.0
			evaluate_at_index_001_2.width, evaluate_at_index_001_2.height = 140.0, 100.0
			named_attribute_003_1.width, named_attribute_003_1.height = 186.42977905273438, 100.0
			evaluate_at_index_002_1.width, evaluate_at_index_002_1.height = 140.0, 100.0
			evaluate_at_index_003_1.width, evaluate_at_index_003_1.height = 140.0, 100.0
			named_attribute_004_1.width, named_attribute_004_1.height = 186.42977905273438, 100.0
			reroute_16.width, reroute_16.height = 16.0, 100.0
			group_23.width, group_23.height = 186.0294189453125, 100.0
			evaluate_at_index_004_1.width, evaluate_at_index_004_1.height = 140.0, 100.0
			named_attribute_005_1.width, named_attribute_005_1.height = 186.42977905273438, 100.0
			switch_13.width, switch_13.height = 140.0, 100.0
			boolean_math_12.width, boolean_math_12.height = 140.0, 100.0

			#initialize mn_topo_backbone links
			#named_attribute_001_5.Attribute -> evaluate_at_index_5.Value
			mn_topo_backbone.links.new(named_attribute_001_5.outputs[0], evaluate_at_index_5.inputs[1])
			#reroute_16.Output -> evaluate_at_index_5.Index
			mn_topo_backbone.links.new(reroute_16.outputs[0], evaluate_at_index_5.inputs[0])
			#group_input_65.Offset -> math_20.Value
			mn_topo_backbone.links.new(group_input_65.outputs[0], math_20.inputs[0])
			#reroute_16.Output -> evaluate_at_index_001_2.Index
			mn_topo_backbone.links.new(reroute_16.outputs[0], evaluate_at_index_001_2.inputs[0])
			#named_attribute_002_4.Attribute -> evaluate_at_index_001_2.Value
			mn_topo_backbone.links.new(named_attribute_002_4.outputs[0], evaluate_at_index_001_2.inputs[1])
			#reroute_16.Output -> evaluate_at_index_002_1.Index
			mn_topo_backbone.links.new(reroute_16.outputs[0], evaluate_at_index_002_1.inputs[0])
			#named_attribute_003_1.Attribute -> evaluate_at_index_002_1.Value
			mn_topo_backbone.links.new(named_attribute_003_1.outputs[0], evaluate_at_index_002_1.inputs[1])
			#reroute_16.Output -> evaluate_at_index_003_1.Index
			mn_topo_backbone.links.new(reroute_16.outputs[0], evaluate_at_index_003_1.inputs[0])
			#named_attribute_004_1.Attribute -> evaluate_at_index_003_1.Value
			mn_topo_backbone.links.new(named_attribute_004_1.outputs[0], evaluate_at_index_003_1.inputs[1])
			#index_4.Index -> math_20.Value
			mn_topo_backbone.links.new(index_4.outputs[0], math_20.inputs[1])
			#math_20.Value -> reroute_16.Input
			mn_topo_backbone.links.new(math_20.outputs[0], reroute_16.inputs[0])
			#evaluate_at_index_003_1.Value -> group_output_65.N
			mn_topo_backbone.links.new(evaluate_at_index_003_1.outputs[0], group_output_65.inputs[3])
			#evaluate_at_index_002_1.Value -> group_output_65.CA
			mn_topo_backbone.links.new(evaluate_at_index_002_1.outputs[0], group_output_65.inputs[2])
			#evaluate_at_index_001_2.Value -> group_output_65.C
			mn_topo_backbone.links.new(evaluate_at_index_001_2.outputs[0], group_output_65.inputs[1])
			#evaluate_at_index_5.Value -> group_output_65.O
			mn_topo_backbone.links.new(evaluate_at_index_5.outputs[0], group_output_65.inputs[0])
			#reroute_16.Output -> evaluate_at_index_004_1.Index
			mn_topo_backbone.links.new(reroute_16.outputs[0], evaluate_at_index_004_1.inputs[0])
			#evaluate_at_index_004_1.Value -> group_output_65.NH
			mn_topo_backbone.links.new(evaluate_at_index_004_1.outputs[0], group_output_65.inputs[4])
			#group_23.H -> switch_13.True
			mn_topo_backbone.links.new(group_23.outputs[0], switch_13.inputs[2])
			#switch_13.Output -> evaluate_at_index_004_1.Value
			mn_topo_backbone.links.new(switch_13.outputs[0], evaluate_at_index_004_1.inputs[1])
			#named_attribute_005_1.Exists -> boolean_math_12.Boolean
			mn_topo_backbone.links.new(named_attribute_005_1.outputs[1], boolean_math_12.inputs[0])
			#boolean_math_12.Boolean -> switch_13.Switch
			mn_topo_backbone.links.new(boolean_math_12.outputs[0], switch_13.inputs[0])
			#named_attribute_005_1.Attribute -> switch_13.False
			mn_topo_backbone.links.new(named_attribute_005_1.outputs[0], switch_13.inputs[1])
			return mn_topo_backbone

		mn_topo_backbone = mn_topo_backbone_node_group()

		#initialize hbond_backbone_check node group
		def hbond_backbone_check_node_group():
			hbond_backbone_check = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "HBond Backbone Check")

			hbond_backbone_check.color_tag = 'NONE'
			hbond_backbone_check.description = ""


			#hbond_backbone_check interface
			#Socket Is Bonded
			is_bonded_socket_1 = hbond_backbone_check.interface.new_socket(name = "Is Bonded", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			is_bonded_socket_1.attribute_domain = 'POINT'

			#Socket Bond Energy
			bond_energy_socket_1 = hbond_backbone_check.interface.new_socket(name = "Bond Energy", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
			bond_energy_socket_1.subtype = 'NONE'
			bond_energy_socket_1.default_value = 0.0
			bond_energy_socket_1.min_value = -3.4028234663852886e+38
			bond_energy_socket_1.max_value = 3.4028234663852886e+38
			bond_energy_socket_1.attribute_domain = 'POINT'

			#Socket H->O
			h__o_socket = hbond_backbone_check.interface.new_socket(name = "H->O", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			h__o_socket.subtype = 'NONE'
			h__o_socket.default_value = (0.0, 0.0, 0.0)
			h__o_socket.min_value = -3.4028234663852886e+38
			h__o_socket.max_value = 3.4028234663852886e+38
			h__o_socket.attribute_domain = 'POINT'

			#Panel CO
			co_panel = hbond_backbone_check.interface.new_panel("CO")
			#Socket CO Index
			co_index_socket = hbond_backbone_check.interface.new_socket(name = "CO Index", in_out='INPUT', socket_type = 'NodeSocketInt', parent = co_panel)
			co_index_socket.subtype = 'NONE'
			co_index_socket.default_value = 0
			co_index_socket.min_value = 0
			co_index_socket.max_value = 2147483647
			co_index_socket.attribute_domain = 'POINT'

			#Socket CO Offset
			co_offset_socket = hbond_backbone_check.interface.new_socket(name = "CO Offset", in_out='INPUT', socket_type = 'NodeSocketInt', parent = co_panel)
			co_offset_socket.subtype = 'NONE'
			co_offset_socket.default_value = 0
			co_offset_socket.min_value = -2147483648
			co_offset_socket.max_value = 2147483647
			co_offset_socket.attribute_domain = 'POINT'


			#Panel NH
			nh_panel = hbond_backbone_check.interface.new_panel("NH")
			#Socket NH Index
			nh_index_socket = hbond_backbone_check.interface.new_socket(name = "NH Index", in_out='INPUT', socket_type = 'NodeSocketInt', parent = nh_panel)
			nh_index_socket.subtype = 'NONE'
			nh_index_socket.default_value = 0
			nh_index_socket.min_value = 0
			nh_index_socket.max_value = 2147483647
			nh_index_socket.attribute_domain = 'POINT'

			#Socket NH Offset
			nh_offset_socket = hbond_backbone_check.interface.new_socket(name = "NH Offset", in_out='INPUT', socket_type = 'NodeSocketInt', parent = nh_panel)
			nh_offset_socket.subtype = 'NONE'
			nh_offset_socket.default_value = 0
			nh_offset_socket.min_value = -2147483648
			nh_offset_socket.max_value = 2147483647
			nh_offset_socket.attribute_domain = 'POINT'



			#initialize hbond_backbone_check nodes
			#node Group Output
			group_output_66 = hbond_backbone_check.nodes.new("NodeGroupOutput")
			group_output_66.name = "Group Output"
			group_output_66.is_active_output = True

			#node Group Input
			group_input_66 = hbond_backbone_check.nodes.new("NodeGroupInput")
			group_input_66.name = "Group Input"

			#node Group.008
			group_008_3 = hbond_backbone_check.nodes.new("GeometryNodeGroup")
			group_008_3.name = "Group.008"
			group_008_3.node_tree = hbond_energy

			#node Group.009
			group_009_3 = hbond_backbone_check.nodes.new("GeometryNodeGroup")
			group_009_3.name = "Group.009"
			group_009_3.node_tree = mn_topo_backbone
			#Socket_3
			group_009_3.inputs[0].default_value = 0

			#node Evaluate at Index
			evaluate_at_index_6 = hbond_backbone_check.nodes.new("GeometryNodeFieldAtIndex")
			evaluate_at_index_6.name = "Evaluate at Index"
			evaluate_at_index_6.data_type = 'FLOAT_VECTOR'
			evaluate_at_index_6.domain = 'POINT'

			#node Evaluate at Index.001
			evaluate_at_index_001_3 = hbond_backbone_check.nodes.new("GeometryNodeFieldAtIndex")
			evaluate_at_index_001_3.name = "Evaluate at Index.001"
			evaluate_at_index_001_3.data_type = 'FLOAT_VECTOR'
			evaluate_at_index_001_3.domain = 'POINT'

			#node Evaluate at Index.002
			evaluate_at_index_002_2 = hbond_backbone_check.nodes.new("GeometryNodeFieldAtIndex")
			evaluate_at_index_002_2.name = "Evaluate at Index.002"
			evaluate_at_index_002_2.data_type = 'FLOAT_VECTOR'
			evaluate_at_index_002_2.domain = 'POINT'

			#node Evaluate at Index.003
			evaluate_at_index_003_2 = hbond_backbone_check.nodes.new("GeometryNodeFieldAtIndex")
			evaluate_at_index_003_2.name = "Evaluate at Index.003"
			evaluate_at_index_003_2.data_type = 'FLOAT_VECTOR'
			evaluate_at_index_003_2.domain = 'POINT'

			#node Math
			math_21 = hbond_backbone_check.nodes.new("ShaderNodeMath")
			math_21.name = "Math"
			math_21.operation = 'ADD'
			math_21.use_clamp = False

			#node Math.001
			math_001_6 = hbond_backbone_check.nodes.new("ShaderNodeMath")
			math_001_6.name = "Math.001"
			math_001_6.operation = 'ADD'
			math_001_6.use_clamp = False

			#node Math.002
			math_002_5 = hbond_backbone_check.nodes.new("ShaderNodeMath")
			math_002_5.name = "Math.002"
			math_002_5.operation = 'SUBTRACT'
			math_002_5.use_clamp = False

			#node Math.003
			math_003_3 = hbond_backbone_check.nodes.new("ShaderNodeMath")
			math_003_3.name = "Math.003"
			math_003_3.operation = 'ABSOLUTE'
			math_003_3.use_clamp = False

			#node Compare
			compare_11 = hbond_backbone_check.nodes.new("FunctionNodeCompare")
			compare_11.name = "Compare"
			compare_11.data_type = 'FLOAT'
			compare_11.mode = 'ELEMENT'
			compare_11.operation = 'GREATER_THAN'

			#node Integer
			integer_1 = hbond_backbone_check.nodes.new("FunctionNodeInputInt")
			integer_1.name = "Integer"
			integer_1.integer = 2

			#node Frame
			frame_5 = hbond_backbone_check.nodes.new("NodeFrame")
			frame_5.label = "Check not bonded to +/- residues"
			frame_5.name = "Frame"
			frame_5.label_size = 20
			frame_5.shrink = True

			#node Switch
			switch_14 = hbond_backbone_check.nodes.new("GeometryNodeSwitch")
			switch_14.name = "Switch"
			switch_14.input_type = 'BOOLEAN'
			#False
			switch_14.inputs[1].default_value = False

			#node Compare.001
			compare_001_6 = hbond_backbone_check.nodes.new("FunctionNodeCompare")
			compare_001_6.name = "Compare.001"
			compare_001_6.data_type = 'FLOAT'
			compare_001_6.mode = 'ELEMENT'
			compare_001_6.operation = 'LESS_THAN'

			#node Vector Math
			vector_math_6 = hbond_backbone_check.nodes.new("ShaderNodeVectorMath")
			vector_math_6.name = "Vector Math"
			vector_math_6.operation = 'LENGTH'

			#node Group
			group_24 = hbond_backbone_check.nodes.new("GeometryNodeGroup")
			group_24.name = "Group"
			group_24.node_tree = mn_units
			#Input_1
			group_24.inputs[0].default_value = 3.0



			#Set parents
			math_002_5.parent = frame_5
			math_003_3.parent = frame_5
			compare_11.parent = frame_5
			integer_1.parent = frame_5

			#Set locations
			group_output_66.location = (820.0, 240.0)
			group_input_66.location = (-680.0, 140.0)
			group_008_3.location = (224.2731170654297, 240.0)
			group_009_3.location = (-480.0, 460.0)
			evaluate_at_index_6.location = (-20.0, 40.0)
			evaluate_at_index_001_3.location = (-20.0, -120.0)
			evaluate_at_index_002_2.location = (-20.0, 400.0)
			evaluate_at_index_003_2.location = (-20.0, 240.0)
			math_21.location = (-480.0, 240.0)
			math_001_6.location = (-480.0, 80.0)
			math_002_5.location = (70.0, 640.0)
			math_003_3.location = (240.0, 640.0)
			compare_11.location = (420.0, 640.0)
			integer_1.location = (240.0, 500.0)
			frame_5.location = (-70.0, 40.0)
			switch_14.location = (620.0, 340.0)
			compare_001_6.location = (520.0, 140.0)
			vector_math_6.location = (260.0, 20.0)
			group_24.location = (520.0, -20.0)

			#Set dimensions
			group_output_66.width, group_output_66.height = 140.0, 100.0
			group_input_66.width, group_input_66.height = 140.0, 100.0
			group_008_3.width, group_008_3.height = 184.92144775390625, 100.0
			group_009_3.width, group_009_3.height = 140.0, 100.0
			evaluate_at_index_6.width, evaluate_at_index_6.height = 140.0, 100.0
			evaluate_at_index_001_3.width, evaluate_at_index_001_3.height = 140.0, 100.0
			evaluate_at_index_002_2.width, evaluate_at_index_002_2.height = 140.0, 100.0
			evaluate_at_index_003_2.width, evaluate_at_index_003_2.height = 140.0, 100.0
			math_21.width, math_21.height = 140.0, 100.0
			math_001_6.width, math_001_6.height = 140.0, 100.0
			math_002_5.width, math_002_5.height = 140.0, 100.0
			math_003_3.width, math_003_3.height = 140.0, 100.0
			compare_11.width, compare_11.height = 140.0, 100.0
			integer_1.width, integer_1.height = 140.0, 100.0
			frame_5.width, frame_5.height = 550.0, 284.0
			switch_14.width, switch_14.height = 140.0, 100.0
			compare_001_6.width, compare_001_6.height = 140.0, 100.0
			vector_math_6.width, vector_math_6.height = 140.0, 100.0
			group_24.width, group_24.height = 140.0, 100.0

			#initialize hbond_backbone_check links
			#evaluate_at_index_001_3.Value -> group_008_3.H
			hbond_backbone_check.links.new(evaluate_at_index_001_3.outputs[0], group_008_3.inputs[3])
			#evaluate_at_index_6.Value -> group_008_3.N
			hbond_backbone_check.links.new(evaluate_at_index_6.outputs[0], group_008_3.inputs[2])
			#evaluate_at_index_002_2.Value -> group_008_3.O
			hbond_backbone_check.links.new(evaluate_at_index_002_2.outputs[0], group_008_3.inputs[0])
			#math_001_6.Value -> evaluate_at_index_001_3.Index
			hbond_backbone_check.links.new(math_001_6.outputs[0], evaluate_at_index_001_3.inputs[0])
			#math_001_6.Value -> evaluate_at_index_6.Index
			hbond_backbone_check.links.new(math_001_6.outputs[0], evaluate_at_index_6.inputs[0])
			#evaluate_at_index_003_2.Value -> group_008_3.C
			hbond_backbone_check.links.new(evaluate_at_index_003_2.outputs[0], group_008_3.inputs[1])
			#group_008_3.Bond Energy -> group_output_66.Bond Energy
			hbond_backbone_check.links.new(group_008_3.outputs[1], group_output_66.inputs[1])
			#group_008_3.Bond Vector -> group_output_66.H->O
			hbond_backbone_check.links.new(group_008_3.outputs[2], group_output_66.inputs[2])
			#math_21.Value -> evaluate_at_index_002_2.Index
			hbond_backbone_check.links.new(math_21.outputs[0], evaluate_at_index_002_2.inputs[0])
			#math_21.Value -> evaluate_at_index_003_2.Index
			hbond_backbone_check.links.new(math_21.outputs[0], evaluate_at_index_003_2.inputs[0])
			#group_input_66.CO Index -> math_21.Value
			hbond_backbone_check.links.new(group_input_66.outputs[0], math_21.inputs[0])
			#group_input_66.CO Offset -> math_21.Value
			hbond_backbone_check.links.new(group_input_66.outputs[1], math_21.inputs[1])
			#group_input_66.NH Index -> math_001_6.Value
			hbond_backbone_check.links.new(group_input_66.outputs[2], math_001_6.inputs[0])
			#group_input_66.NH Offset -> math_001_6.Value
			hbond_backbone_check.links.new(group_input_66.outputs[3], math_001_6.inputs[1])
			#math_21.Value -> math_002_5.Value
			hbond_backbone_check.links.new(math_21.outputs[0], math_002_5.inputs[0])
			#math_001_6.Value -> math_002_5.Value
			hbond_backbone_check.links.new(math_001_6.outputs[0], math_002_5.inputs[1])
			#math_002_5.Value -> math_003_3.Value
			hbond_backbone_check.links.new(math_002_5.outputs[0], math_003_3.inputs[0])
			#math_003_3.Value -> compare_11.A
			hbond_backbone_check.links.new(math_003_3.outputs[0], compare_11.inputs[0])
			#integer_1.Integer -> compare_11.B
			hbond_backbone_check.links.new(integer_1.outputs[0], compare_11.inputs[1])
			#compare_11.Result -> switch_14.Switch
			hbond_backbone_check.links.new(compare_11.outputs[0], switch_14.inputs[0])
			#group_008_3.Bond Vector -> vector_math_6.Vector
			hbond_backbone_check.links.new(group_008_3.outputs[2], vector_math_6.inputs[0])
			#vector_math_6.Value -> compare_001_6.A
			hbond_backbone_check.links.new(vector_math_6.outputs[1], compare_001_6.inputs[0])
			#group_24.Angstrom -> compare_001_6.B
			hbond_backbone_check.links.new(group_24.outputs[0], compare_001_6.inputs[1])
			#switch_14.Output -> group_output_66.Is Bonded
			hbond_backbone_check.links.new(switch_14.outputs[0], group_output_66.inputs[0])
			#group_008_3.Is Bonded -> switch_14.True
			hbond_backbone_check.links.new(group_008_3.outputs[0], switch_14.inputs[2])
			#group_009_3.O -> evaluate_at_index_002_2.Value
			hbond_backbone_check.links.new(group_009_3.outputs[0], evaluate_at_index_002_2.inputs[1])
			#group_009_3.C -> evaluate_at_index_003_2.Value
			hbond_backbone_check.links.new(group_009_3.outputs[1], evaluate_at_index_003_2.inputs[1])
			#group_009_3.N -> evaluate_at_index_6.Value
			hbond_backbone_check.links.new(group_009_3.outputs[3], evaluate_at_index_6.inputs[1])
			#group_009_3.NH -> evaluate_at_index_001_3.Value
			hbond_backbone_check.links.new(group_009_3.outputs[4], evaluate_at_index_001_3.inputs[1])
			return hbond_backbone_check

		hbond_backbone_check = hbond_backbone_check_node_group()

		#initialize boolean_run_fill node group
		def boolean_run_fill_node_group():
			boolean_run_fill = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Boolean Run Fill")

			boolean_run_fill.color_tag = 'CONVERTER'
			boolean_run_fill.description = ""


			#boolean_run_fill interface
			#Socket Boolean
			boolean_socket_12 = boolean_run_fill.interface.new_socket(name = "Boolean", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			boolean_socket_12.attribute_domain = 'POINT'

			#Socket Boolean
			boolean_socket_13 = boolean_run_fill.interface.new_socket(name = "Boolean", in_out='INPUT', socket_type = 'NodeSocketBool')
			boolean_socket_13.attribute_domain = 'POINT'
			boolean_socket_13.description = "Boolean array to fill runs of False"

			#Socket Fill Size
			fill_size_socket = boolean_run_fill.interface.new_socket(name = "Fill Size", in_out='INPUT', socket_type = 'NodeSocketInt')
			fill_size_socket.subtype = 'NONE'
			fill_size_socket.default_value = 3
			fill_size_socket.min_value = -2147483648
			fill_size_socket.max_value = 2147483647
			fill_size_socket.attribute_domain = 'POINT'
			fill_size_socket.description = "Set a run of False to True if length equal or less than Fill Size"


			#initialize boolean_run_fill nodes
			#node Group Output
			group_output_67 = boolean_run_fill.nodes.new("NodeGroupOutput")
			group_output_67.name = "Group Output"
			group_output_67.is_active_output = True

			#node Group Input
			group_input_67 = boolean_run_fill.nodes.new("NodeGroupInput")
			group_input_67.name = "Group Input"

			#node Accumulate Field
			accumulate_field_4 = boolean_run_fill.nodes.new("GeometryNodeAccumulateField")
			accumulate_field_4.name = "Accumulate Field"
			accumulate_field_4.data_type = 'INT'
			accumulate_field_4.domain = 'POINT'
			#Group Index
			accumulate_field_4.inputs[1].default_value = 0

			#node Accumulate Field.001
			accumulate_field_001_6 = boolean_run_fill.nodes.new("GeometryNodeAccumulateField")
			accumulate_field_001_6.name = "Accumulate Field.001"
			accumulate_field_001_6.data_type = 'INT'
			accumulate_field_001_6.domain = 'POINT'
			#Value
			accumulate_field_001_6.inputs[0].default_value = 1

			#node Compare
			compare_12 = boolean_run_fill.nodes.new("FunctionNodeCompare")
			compare_12.name = "Compare"
			compare_12.data_type = 'INT'
			compare_12.mode = 'ELEMENT'
			compare_12.operation = 'LESS_EQUAL'

			#node Compare.001
			compare_001_7 = boolean_run_fill.nodes.new("FunctionNodeCompare")
			compare_001_7.name = "Compare.001"
			compare_001_7.data_type = 'INT'
			compare_001_7.mode = 'ELEMENT'
			compare_001_7.operation = 'LESS_EQUAL'

			#node Boolean Math.010
			boolean_math_010_1 = boolean_run_fill.nodes.new("FunctionNodeBooleanMath")
			boolean_math_010_1.name = "Boolean Math.010"
			boolean_math_010_1.operation = 'AND'

			#node Boolean Math
			boolean_math_13 = boolean_run_fill.nodes.new("FunctionNodeBooleanMath")
			boolean_math_13.name = "Boolean Math"
			boolean_math_13.operation = 'OR'

			#node Reroute
			reroute_17 = boolean_run_fill.nodes.new("NodeReroute")
			reroute_17.name = "Reroute"
			#node Reroute.001
			reroute_001_13 = boolean_run_fill.nodes.new("NodeReroute")
			reroute_001_13.name = "Reroute.001"
			#node Reroute.003
			reroute_003_9 = boolean_run_fill.nodes.new("NodeReroute")
			reroute_003_9.name = "Reroute.003"
			#node Reroute.002
			reroute_002_9 = boolean_run_fill.nodes.new("NodeReroute")
			reroute_002_9.name = "Reroute.002"



			#Set locations
			group_output_67.location = (430.0, 0.0)
			group_input_67.location = (-480.0, -20.0)
			accumulate_field_4.location = (-220.0, -120.0)
			accumulate_field_001_6.location = (-60.0, -120.0)
			compare_12.location = (100.0, -120.0)
			compare_001_7.location = (100.0, -280.0)
			boolean_math_010_1.location = (260.0, -120.0)
			boolean_math_13.location = (260.0, 20.0)
			reroute_17.location = (60.0, -380.0)
			reroute_001_13.location = (-280.0, -380.0)
			reroute_003_9.location = (-300.0, -80.0)
			reroute_002_9.location = (-240.0, -60.0)

			#Set dimensions
			group_output_67.width, group_output_67.height = 140.0, 100.0
			group_input_67.width, group_input_67.height = 140.0, 100.0
			accumulate_field_4.width, accumulate_field_4.height = 140.0, 100.0
			accumulate_field_001_6.width, accumulate_field_001_6.height = 140.0, 100.0
			compare_12.width, compare_12.height = 140.0, 100.0
			compare_001_7.width, compare_001_7.height = 140.0, 100.0
			boolean_math_010_1.width, boolean_math_010_1.height = 140.0, 100.0
			boolean_math_13.width, boolean_math_13.height = 140.0, 100.0
			reroute_17.width, reroute_17.height = 16.0, 100.0
			reroute_001_13.width, reroute_001_13.height = 16.0, 100.0
			reroute_003_9.width, reroute_003_9.height = 16.0, 100.0
			reroute_002_9.width, reroute_002_9.height = 16.0, 100.0

			#initialize boolean_run_fill links
			#accumulate_field_001_6.Trailing -> compare_12.A
			boolean_run_fill.links.new(accumulate_field_001_6.outputs[1], compare_12.inputs[2])
			#accumulate_field_4.Leading -> accumulate_field_001_6.Group ID
			boolean_run_fill.links.new(accumulate_field_4.outputs[0], accumulate_field_001_6.inputs[1])
			#compare_001_7.Result -> boolean_math_010_1.Boolean
			boolean_run_fill.links.new(compare_001_7.outputs[0], boolean_math_010_1.inputs[1])
			#compare_12.Result -> boolean_math_010_1.Boolean
			boolean_run_fill.links.new(compare_12.outputs[0], boolean_math_010_1.inputs[0])
			#accumulate_field_001_6.Total -> compare_001_7.A
			boolean_run_fill.links.new(accumulate_field_001_6.outputs[2], compare_001_7.inputs[2])
			#reroute_17.Output -> compare_12.B
			boolean_run_fill.links.new(reroute_17.outputs[0], compare_12.inputs[3])
			#reroute_17.Output -> compare_001_7.B
			boolean_run_fill.links.new(reroute_17.outputs[0], compare_001_7.inputs[3])
			#reroute_002_9.Output -> accumulate_field_4.Value
			boolean_run_fill.links.new(reroute_002_9.outputs[0], accumulate_field_4.inputs[0])
			#reroute_002_9.Output -> boolean_math_13.Boolean
			boolean_run_fill.links.new(reroute_002_9.outputs[0], boolean_math_13.inputs[0])
			#boolean_math_010_1.Boolean -> boolean_math_13.Boolean
			boolean_run_fill.links.new(boolean_math_010_1.outputs[0], boolean_math_13.inputs[1])
			#boolean_math_13.Boolean -> group_output_67.Boolean
			boolean_run_fill.links.new(boolean_math_13.outputs[0], group_output_67.inputs[0])
			#reroute_001_13.Output -> reroute_17.Input
			boolean_run_fill.links.new(reroute_001_13.outputs[0], reroute_17.inputs[0])
			#reroute_003_9.Output -> reroute_001_13.Input
			boolean_run_fill.links.new(reroute_003_9.outputs[0], reroute_001_13.inputs[0])
			#group_input_67.Fill Size -> reroute_003_9.Input
			boolean_run_fill.links.new(group_input_67.outputs[1], reroute_003_9.inputs[0])
			#group_input_67.Boolean -> reroute_002_9.Input
			boolean_run_fill.links.new(group_input_67.outputs[0], reroute_002_9.inputs[0])
			return boolean_run_fill

		boolean_run_fill = boolean_run_fill_node_group()

		#initialize vector_angle node group
		def vector_angle_node_group():
			vector_angle = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Vector Angle")

			vector_angle.color_tag = 'VECTOR'
			vector_angle.description = ""


			#vector_angle interface
			#Socket Angle
			angle_socket = vector_angle.interface.new_socket(name = "Angle", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
			angle_socket.subtype = 'ANGLE'
			angle_socket.default_value = 0.0
			angle_socket.min_value = -3.4028234663852886e+38
			angle_socket.max_value = 3.4028234663852886e+38
			angle_socket.attribute_domain = 'POINT'
			angle_socket.description = "Angle between the two given vectors in radians"

			#Socket A
			a_socket = vector_angle.interface.new_socket(name = "A", in_out='INPUT', socket_type = 'NodeSocketVector')
			a_socket.subtype = 'NONE'
			a_socket.default_value = (0.0, 0.0, 0.0)
			a_socket.min_value = -10000.0
			a_socket.max_value = 10000.0
			a_socket.attribute_domain = 'POINT'

			#Socket B
			b_socket_1 = vector_angle.interface.new_socket(name = "B", in_out='INPUT', socket_type = 'NodeSocketVector')
			b_socket_1.subtype = 'NONE'
			b_socket_1.default_value = (0.0, 0.0, 0.0)
			b_socket_1.min_value = -10000.0
			b_socket_1.max_value = 10000.0
			b_socket_1.attribute_domain = 'POINT'


			#initialize vector_angle nodes
			#node Group Input
			group_input_68 = vector_angle.nodes.new("NodeGroupInput")
			group_input_68.name = "Group Input"

			#node Vector Math.002
			vector_math_002_5 = vector_angle.nodes.new("ShaderNodeVectorMath")
			vector_math_002_5.name = "Vector Math.002"
			vector_math_002_5.operation = 'NORMALIZE'

			#node Vector Math.001
			vector_math_001_4 = vector_angle.nodes.new("ShaderNodeVectorMath")
			vector_math_001_4.name = "Vector Math.001"
			vector_math_001_4.operation = 'NORMALIZE'

			#node Vector Math
			vector_math_7 = vector_angle.nodes.new("ShaderNodeVectorMath")
			vector_math_7.name = "Vector Math"
			vector_math_7.operation = 'DOT_PRODUCT'

			#node Math
			math_22 = vector_angle.nodes.new("ShaderNodeMath")
			math_22.name = "Math"
			math_22.operation = 'ARCCOSINE'
			math_22.use_clamp = False

			#node Group Output
			group_output_68 = vector_angle.nodes.new("NodeGroupOutput")
			group_output_68.name = "Group Output"
			group_output_68.is_active_output = True




			#Set locations
			group_input_68.location = (-360.0, 0.0)
			vector_math_002_5.location = (-160.0, -60.0)
			vector_math_001_4.location = (-160.0, 60.0)
			vector_math_7.location = (0.0, 60.0)
			math_22.location = (160.0, 60.0)
			group_output_68.location = (340.0, 60.0)

			#Set dimensions
			group_input_68.width, group_input_68.height = 140.0, 100.0
			vector_math_002_5.width, vector_math_002_5.height = 140.0, 100.0
			vector_math_001_4.width, vector_math_001_4.height = 140.0, 100.0
			vector_math_7.width, vector_math_7.height = 140.0, 100.0
			math_22.width, math_22.height = 140.0, 100.0
			group_output_68.width, group_output_68.height = 140.0, 100.0

			#initialize vector_angle links
			#vector_math_7.Value -> math_22.Value
			vector_angle.links.new(vector_math_7.outputs[1], math_22.inputs[0])
			#vector_math_002_5.Vector -> vector_math_7.Vector
			vector_angle.links.new(vector_math_002_5.outputs[0], vector_math_7.inputs[1])
			#vector_math_001_4.Vector -> vector_math_7.Vector
			vector_angle.links.new(vector_math_001_4.outputs[0], vector_math_7.inputs[0])
			#math_22.Value -> group_output_68.Angle
			vector_angle.links.new(math_22.outputs[0], group_output_68.inputs[0])
			#group_input_68.A -> vector_math_001_4.Vector
			vector_angle.links.new(group_input_68.outputs[0], vector_math_001_4.inputs[0])
			#group_input_68.B -> vector_math_002_5.Vector
			vector_angle.links.new(group_input_68.outputs[1], vector_math_002_5.inputs[0])
			return vector_angle

		vector_angle = vector_angle_node_group()

		#initialize dihedral_angle node group
		def dihedral_angle_node_group():
			dihedral_angle = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Dihedral Angle")

			dihedral_angle.color_tag = 'VECTOR'
			dihedral_angle.description = ""


			#dihedral_angle interface
			#Socket Angle
			angle_socket_1 = dihedral_angle.interface.new_socket(name = "Angle", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
			angle_socket_1.subtype = 'ANGLE'
			angle_socket_1.default_value = 0.0
			angle_socket_1.min_value = -3.4028234663852886e+38
			angle_socket_1.max_value = 3.4028234663852886e+38
			angle_socket_1.attribute_domain = 'POINT'
			angle_socket_1.description = "The angle between the vectors AB and CD, when made perpendicular to BC."

			#Socket BA⟂(BC)
			ba__bc__socket = dihedral_angle.interface.new_socket(name = "BA⟂(BC)", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			ba__bc__socket.subtype = 'NONE'
			ba__bc__socket.default_value = (0.0, 0.0, 0.0)
			ba__bc__socket.min_value = -3.4028234663852886e+38
			ba__bc__socket.max_value = 3.4028234663852886e+38
			ba__bc__socket.attribute_domain = 'POINT'
			ba__bc__socket.description = "The vector BA when made perpendicular to  the axis BC"

			#Socket CD⟂(BC)
			cd__bc__socket = dihedral_angle.interface.new_socket(name = "CD⟂(BC)", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			cd__bc__socket.subtype = 'NONE'
			cd__bc__socket.default_value = (0.0, 0.0, 0.0)
			cd__bc__socket.min_value = -3.4028234663852886e+38
			cd__bc__socket.max_value = 3.4028234663852886e+38
			cd__bc__socket.attribute_domain = 'POINT'
			cd__bc__socket.description = "The Vector CD when makde perpendicular to the axis BC"

			#Socket BC
			bc_socket = dihedral_angle.interface.new_socket(name = "BC", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			bc_socket.subtype = 'NONE'
			bc_socket.default_value = (0.0, 0.0, 0.0)
			bc_socket.min_value = -3.4028234663852886e+38
			bc_socket.max_value = 3.4028234663852886e+38
			bc_socket.attribute_domain = 'POINT'
			bc_socket.description = "The axis vector BC"

			#Socket A
			a_socket_1 = dihedral_angle.interface.new_socket(name = "A", in_out='INPUT', socket_type = 'NodeSocketVector')
			a_socket_1.subtype = 'NONE'
			a_socket_1.default_value = (0.0, 0.0, 0.0)
			a_socket_1.min_value = -3.4028234663852886e+38
			a_socket_1.max_value = 3.4028234663852886e+38
			a_socket_1.attribute_domain = 'POINT'
			a_socket_1.description = "First vector for the calculation, which draws a line to B"

			#Socket B
			b_socket_2 = dihedral_angle.interface.new_socket(name = "B", in_out='INPUT', socket_type = 'NodeSocketVector')
			b_socket_2.subtype = 'NONE'
			b_socket_2.default_value = (0.0, 0.0, 0.0)
			b_socket_2.min_value = -3.4028234663852886e+38
			b_socket_2.max_value = 3.4028234663852886e+38
			b_socket_2.attribute_domain = 'POINT'
			b_socket_2.description = "Second vector for the calculation, which receives a line from A and draws a line to C"

			#Socket C
			c_socket_3 = dihedral_angle.interface.new_socket(name = "C", in_out='INPUT', socket_type = 'NodeSocketVector')
			c_socket_3.subtype = 'NONE'
			c_socket_3.default_value = (0.0, 0.0, 0.0)
			c_socket_3.min_value = -3.4028234663852886e+38
			c_socket_3.max_value = 3.4028234663852886e+38
			c_socket_3.attribute_domain = 'POINT'
			c_socket_3.description = "Third vector for the calculation, which receives a line from B and draws a line to D"

			#Socket D
			d_socket = dihedral_angle.interface.new_socket(name = "D", in_out='INPUT', socket_type = 'NodeSocketVector')
			d_socket.subtype = 'NONE'
			d_socket.default_value = (0.0, 0.0, 0.0)
			d_socket.min_value = -3.4028234663852886e+38
			d_socket.max_value = 3.4028234663852886e+38
			d_socket.attribute_domain = 'POINT'
			d_socket.description = "Last vector for the calculation, which is the end point of the line from D"


			#initialize dihedral_angle nodes
			#node Vector Math.003
			vector_math_003_1 = dihedral_angle.nodes.new("ShaderNodeVectorMath")
			vector_math_003_1.name = "Vector Math.003"
			vector_math_003_1.operation = 'SUBTRACT'

			#node Vector Math.004
			vector_math_004_2 = dihedral_angle.nodes.new("ShaderNodeVectorMath")
			vector_math_004_2.name = "Vector Math.004"
			vector_math_004_2.operation = 'SUBTRACT'

			#node Vector Math.006
			vector_math_006_2 = dihedral_angle.nodes.new("ShaderNodeVectorMath")
			vector_math_006_2.name = "Vector Math.006"
			vector_math_006_2.operation = 'SUBTRACT'

			#node Vector Math.007
			vector_math_007_1 = dihedral_angle.nodes.new("ShaderNodeVectorMath")
			vector_math_007_1.name = "Vector Math.007"
			vector_math_007_1.operation = 'PROJECT'

			#node Vector Math.009
			vector_math_009 = dihedral_angle.nodes.new("ShaderNodeVectorMath")
			vector_math_009.name = "Vector Math.009"
			vector_math_009.operation = 'PROJECT'

			#node Vector Math.008
			vector_math_008 = dihedral_angle.nodes.new("ShaderNodeVectorMath")
			vector_math_008.name = "Vector Math.008"
			vector_math_008.operation = 'SUBTRACT'

			#node Vector Math.010
			vector_math_010 = dihedral_angle.nodes.new("ShaderNodeVectorMath")
			vector_math_010.name = "Vector Math.010"
			vector_math_010.operation = 'SUBTRACT'

			#node MN_utils_vector_angle.002
			mn_utils_vector_angle_002 = dihedral_angle.nodes.new("GeometryNodeGroup")
			mn_utils_vector_angle_002.label = "Vector Angle"
			mn_utils_vector_angle_002.name = "MN_utils_vector_angle.002"
			mn_utils_vector_angle_002.node_tree = vector_angle

			#node Group Output
			group_output_69 = dihedral_angle.nodes.new("NodeGroupOutput")
			group_output_69.name = "Group Output"
			group_output_69.is_active_output = True

			#node Reroute.002
			reroute_002_10 = dihedral_angle.nodes.new("NodeReroute")
			reroute_002_10.name = "Reroute.002"
			#node Reroute.001
			reroute_001_14 = dihedral_angle.nodes.new("NodeReroute")
			reroute_001_14.name = "Reroute.001"
			#node Vector Math
			vector_math_8 = dihedral_angle.nodes.new("ShaderNodeVectorMath")
			vector_math_8.name = "Vector Math"
			vector_math_8.operation = 'CROSS_PRODUCT'

			#node Vector Math.001
			vector_math_001_5 = dihedral_angle.nodes.new("ShaderNodeVectorMath")
			vector_math_001_5.name = "Vector Math.001"
			vector_math_001_5.operation = 'DOT_PRODUCT'

			#node Math.001
			math_001_7 = dihedral_angle.nodes.new("ShaderNodeMath")
			math_001_7.name = "Math.001"
			math_001_7.operation = 'SIGN'
			math_001_7.use_clamp = False

			#node Reroute
			reroute_18 = dihedral_angle.nodes.new("NodeReroute")
			reroute_18.name = "Reroute"
			#node Math
			math_23 = dihedral_angle.nodes.new("ShaderNodeMath")
			math_23.name = "Math"
			math_23.operation = 'MULTIPLY'
			math_23.use_clamp = False

			#node Group Input.003
			group_input_003_3 = dihedral_angle.nodes.new("NodeGroupInput")
			group_input_003_3.name = "Group Input.003"
			group_input_003_3.outputs[0].hide = True
			group_input_003_3.outputs[1].hide = True
			group_input_003_3.outputs[2].hide = True
			group_input_003_3.outputs[4].hide = True

			#node Group Input.001
			group_input_001_13 = dihedral_angle.nodes.new("NodeGroupInput")
			group_input_001_13.name = "Group Input.001"
			group_input_001_13.outputs[1].hide = True
			group_input_001_13.outputs[2].hide = True
			group_input_001_13.outputs[3].hide = True
			group_input_001_13.outputs[4].hide = True

			#node Group Input
			group_input_69 = dihedral_angle.nodes.new("NodeGroupInput")
			group_input_69.name = "Group Input"
			group_input_69.outputs[0].hide = True
			group_input_69.outputs[2].hide = True
			group_input_69.outputs[3].hide = True
			group_input_69.outputs[4].hide = True

			#node Group Input.002
			group_input_002_6 = dihedral_angle.nodes.new("NodeGroupInput")
			group_input_002_6.name = "Group Input.002"
			group_input_002_6.outputs[0].hide = True
			group_input_002_6.outputs[1].hide = True
			group_input_002_6.outputs[3].hide = True
			group_input_002_6.outputs[4].hide = True




			#Set locations
			vector_math_003_1.location = (-142.68453979492188, 25.911895751953125)
			vector_math_004_2.location = (-140.0, 440.0)
			vector_math_006_2.location = (-140.0, 180.0)
			vector_math_007_1.location = (80.0, 320.0)
			vector_math_009.location = (80.0, -80.0)
			vector_math_008.location = (80.0, 460.0)
			vector_math_010.location = (80.0, 60.0)
			mn_utils_vector_angle_002.location = (420.0, 420.0)
			group_output_69.location = (920.0, 320.0)
			reroute_002_10.location = (300.0, 260.0)
			reroute_001_14.location = (300.0, 240.0)
			vector_math_8.location = (420.0, 180.0)
			vector_math_001_5.location = (420.0, 40.0)
			math_001_7.location = (580.0, 40.0)
			reroute_18.location = (300.0, 220.0)
			math_23.location = (640.0, 420.0)
			group_input_003_3.location = (-440.0, 0.0)
			group_input_001_13.location = (-440.0, 420.0)
			group_input_69.location = (-440.0, 280.0)
			group_input_002_6.location = (-440.0, 140.0)

			#Set dimensions
			vector_math_003_1.width, vector_math_003_1.height = 140.0, 100.0
			vector_math_004_2.width, vector_math_004_2.height = 140.0, 100.0
			vector_math_006_2.width, vector_math_006_2.height = 140.0, 100.0
			vector_math_007_1.width, vector_math_007_1.height = 140.0, 100.0
			vector_math_009.width, vector_math_009.height = 140.0, 100.0
			vector_math_008.width, vector_math_008.height = 140.0, 100.0
			vector_math_010.width, vector_math_010.height = 140.0, 100.0
			mn_utils_vector_angle_002.width, mn_utils_vector_angle_002.height = 200.0, 100.0
			group_output_69.width, group_output_69.height = 140.0, 100.0
			reroute_002_10.width, reroute_002_10.height = 16.0, 100.0
			reroute_001_14.width, reroute_001_14.height = 16.0, 100.0
			vector_math_8.width, vector_math_8.height = 140.0, 100.0
			vector_math_001_5.width, vector_math_001_5.height = 140.0, 100.0
			math_001_7.width, math_001_7.height = 140.0, 100.0
			reroute_18.width, reroute_18.height = 16.0, 100.0
			math_23.width, math_23.height = 140.0, 100.0
			group_input_003_3.width, group_input_003_3.height = 140.0, 100.0
			group_input_001_13.width, group_input_001_13.height = 140.0, 100.0
			group_input_69.width, group_input_69.height = 140.0, 100.0
			group_input_002_6.width, group_input_002_6.height = 140.0, 100.0

			#initialize dihedral_angle links
			#vector_math_007_1.Vector -> vector_math_008.Vector
			dihedral_angle.links.new(vector_math_007_1.outputs[0], vector_math_008.inputs[1])
			#vector_math_009.Vector -> vector_math_010.Vector
			dihedral_angle.links.new(vector_math_009.outputs[0], vector_math_010.inputs[1])
			#vector_math_004_2.Vector -> vector_math_007_1.Vector
			dihedral_angle.links.new(vector_math_004_2.outputs[0], vector_math_007_1.inputs[0])
			#vector_math_006_2.Vector -> vector_math_007_1.Vector
			dihedral_angle.links.new(vector_math_006_2.outputs[0], vector_math_007_1.inputs[1])
			#reroute_002_10.Output -> mn_utils_vector_angle_002.A
			dihedral_angle.links.new(reroute_002_10.outputs[0], mn_utils_vector_angle_002.inputs[0])
			#vector_math_004_2.Vector -> vector_math_008.Vector
			dihedral_angle.links.new(vector_math_004_2.outputs[0], vector_math_008.inputs[0])
			#vector_math_003_1.Vector -> vector_math_010.Vector
			dihedral_angle.links.new(vector_math_003_1.outputs[0], vector_math_010.inputs[0])
			#vector_math_003_1.Vector -> vector_math_009.Vector
			dihedral_angle.links.new(vector_math_003_1.outputs[0], vector_math_009.inputs[0])
			#vector_math_006_2.Vector -> vector_math_009.Vector
			dihedral_angle.links.new(vector_math_006_2.outputs[0], vector_math_009.inputs[1])
			#vector_math_006_2.Vector -> reroute_18.Input
			dihedral_angle.links.new(vector_math_006_2.outputs[0], reroute_18.inputs[0])
			#reroute_001_14.Output -> mn_utils_vector_angle_002.B
			dihedral_angle.links.new(reroute_001_14.outputs[0], mn_utils_vector_angle_002.inputs[1])
			#vector_math_8.Vector -> vector_math_001_5.Vector
			dihedral_angle.links.new(vector_math_8.outputs[0], vector_math_001_5.inputs[0])
			#reroute_18.Output -> vector_math_001_5.Vector
			dihedral_angle.links.new(reroute_18.outputs[0], vector_math_001_5.inputs[1])
			#mn_utils_vector_angle_002.Angle -> math_23.Value
			dihedral_angle.links.new(mn_utils_vector_angle_002.outputs[0], math_23.inputs[0])
			#reroute_001_14.Output -> vector_math_8.Vector
			dihedral_angle.links.new(reroute_001_14.outputs[0], vector_math_8.inputs[1])
			#group_input_002_6.C -> vector_math_003_1.Vector
			dihedral_angle.links.new(group_input_002_6.outputs[2], vector_math_003_1.inputs[1])
			#group_input_69.B -> vector_math_004_2.Vector
			dihedral_angle.links.new(group_input_69.outputs[1], vector_math_004_2.inputs[1])
			#group_input_69.B -> vector_math_006_2.Vector
			dihedral_angle.links.new(group_input_69.outputs[1], vector_math_006_2.inputs[1])
			#group_input_002_6.C -> vector_math_006_2.Vector
			dihedral_angle.links.new(group_input_002_6.outputs[2], vector_math_006_2.inputs[0])
			#math_23.Value -> group_output_69.Angle
			dihedral_angle.links.new(math_23.outputs[0], group_output_69.inputs[0])
			#reroute_002_10.Output -> group_output_69.BA⟂(BC)
			dihedral_angle.links.new(reroute_002_10.outputs[0], group_output_69.inputs[1])
			#reroute_18.Output -> group_output_69.BC
			dihedral_angle.links.new(reroute_18.outputs[0], group_output_69.inputs[3])
			#reroute_001_14.Output -> group_output_69.CD⟂(BC)
			dihedral_angle.links.new(reroute_001_14.outputs[0], group_output_69.inputs[2])
			#reroute_002_10.Output -> vector_math_8.Vector
			dihedral_angle.links.new(reroute_002_10.outputs[0], vector_math_8.inputs[0])
			#vector_math_001_5.Value -> math_001_7.Value
			dihedral_angle.links.new(vector_math_001_5.outputs[1], math_001_7.inputs[0])
			#math_001_7.Value -> math_23.Value
			dihedral_angle.links.new(math_001_7.outputs[0], math_23.inputs[1])
			#vector_math_010.Vector -> reroute_001_14.Input
			dihedral_angle.links.new(vector_math_010.outputs[0], reroute_001_14.inputs[0])
			#vector_math_008.Vector -> reroute_002_10.Input
			dihedral_angle.links.new(vector_math_008.outputs[0], reroute_002_10.inputs[0])
			#group_input_001_13.A -> vector_math_004_2.Vector
			dihedral_angle.links.new(group_input_001_13.outputs[0], vector_math_004_2.inputs[0])
			#group_input_003_3.D -> vector_math_003_1.Vector
			dihedral_angle.links.new(group_input_003_3.outputs[3], vector_math_003_1.inputs[0])
			return dihedral_angle

		dihedral_angle = dihedral_angle_node_group()

		#initialize _mn_topo_phi_psi node group
		def _mn_topo_phi_psi_node_group():
			_mn_topo_phi_psi = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".MN_topo_phi_psi")

			_mn_topo_phi_psi.color_tag = 'NONE'
			_mn_topo_phi_psi.description = ""


			#_mn_topo_phi_psi interface
			#Socket Angle
			angle_socket_2 = _mn_topo_phi_psi.interface.new_socket(name = "Angle", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
			angle_socket_2.subtype = 'ANGLE'
			angle_socket_2.default_value = 0.0
			angle_socket_2.min_value = -3.4028234663852886e+38
			angle_socket_2.max_value = 3.4028234663852886e+38
			angle_socket_2.attribute_domain = 'POINT'

			#Socket BA⟂(BC)
			ba__bc__socket_1 = _mn_topo_phi_psi.interface.new_socket(name = "BA⟂(BC)", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			ba__bc__socket_1.subtype = 'NONE'
			ba__bc__socket_1.default_value = (0.0, 0.0, 0.0)
			ba__bc__socket_1.min_value = -3.4028234663852886e+38
			ba__bc__socket_1.max_value = 3.4028234663852886e+38
			ba__bc__socket_1.attribute_domain = 'POINT'

			#Socket CD⟂(BC)
			cd__bc__socket_1 = _mn_topo_phi_psi.interface.new_socket(name = "CD⟂(BC)", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			cd__bc__socket_1.subtype = 'NONE'
			cd__bc__socket_1.default_value = (0.0, 0.0, 0.0)
			cd__bc__socket_1.min_value = -3.4028234663852886e+38
			cd__bc__socket_1.max_value = 3.4028234663852886e+38
			cd__bc__socket_1.attribute_domain = 'POINT'

			#Socket BC
			bc_socket_1 = _mn_topo_phi_psi.interface.new_socket(name = "BC", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			bc_socket_1.subtype = 'NONE'
			bc_socket_1.default_value = (0.0, 0.0, 0.0)
			bc_socket_1.min_value = -3.4028234663852886e+38
			bc_socket_1.max_value = 3.4028234663852886e+38
			bc_socket_1.attribute_domain = 'POINT'

			#Socket A
			a_socket_2 = _mn_topo_phi_psi.interface.new_socket(name = "A", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			a_socket_2.subtype = 'NONE'
			a_socket_2.default_value = (0.0, 0.0, 0.0)
			a_socket_2.min_value = -3.4028234663852886e+38
			a_socket_2.max_value = 3.4028234663852886e+38
			a_socket_2.attribute_domain = 'POINT'

			#Socket B
			b_socket_3 = _mn_topo_phi_psi.interface.new_socket(name = "B", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			b_socket_3.subtype = 'NONE'
			b_socket_3.default_value = (0.0, 0.0, 0.0)
			b_socket_3.min_value = -3.4028234663852886e+38
			b_socket_3.max_value = 3.4028234663852886e+38
			b_socket_3.attribute_domain = 'POINT'

			#Socket C
			c_socket_4 = _mn_topo_phi_psi.interface.new_socket(name = "C", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			c_socket_4.subtype = 'NONE'
			c_socket_4.default_value = (0.0, 0.0, 0.0)
			c_socket_4.min_value = -3.4028234663852886e+38
			c_socket_4.max_value = 3.4028234663852886e+38
			c_socket_4.attribute_domain = 'POINT'

			#Socket D
			d_socket_1 = _mn_topo_phi_psi.interface.new_socket(name = "D", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			d_socket_1.subtype = 'NONE'
			d_socket_1.default_value = (0.0, 0.0, 0.0)
			d_socket_1.min_value = -3.4028234663852886e+38
			d_socket_1.max_value = 3.4028234663852886e+38
			d_socket_1.attribute_domain = 'POINT'

			#Socket Menu
			menu_socket_3 = _mn_topo_phi_psi.interface.new_socket(name = "Menu", in_out='INPUT', socket_type = 'NodeSocketMenu')
			menu_socket_3.attribute_domain = 'POINT'


			#initialize _mn_topo_phi_psi nodes
			#node Group Output
			group_output_70 = _mn_topo_phi_psi.nodes.new("NodeGroupOutput")
			group_output_70.name = "Group Output"
			group_output_70.is_active_output = True

			#node Group Input
			group_input_70 = _mn_topo_phi_psi.nodes.new("NodeGroupInput")
			group_input_70.name = "Group Input"

			#node Group.005
			group_005_4 = _mn_topo_phi_psi.nodes.new("GeometryNodeGroup")
			group_005_4.name = "Group.005"
			group_005_4.node_tree = mn_topo_backbone
			#Socket_3
			group_005_4.inputs[0].default_value = 1

			#node Group.007
			group_007_3 = _mn_topo_phi_psi.nodes.new("GeometryNodeGroup")
			group_007_3.name = "Group.007"
			group_007_3.node_tree = mn_topo_backbone
			#Socket_3
			group_007_3.inputs[0].default_value = -1

			#node Group.008
			group_008_4 = _mn_topo_phi_psi.nodes.new("GeometryNodeGroup")
			group_008_4.name = "Group.008"
			group_008_4.node_tree = mn_topo_backbone
			#Socket_3
			group_008_4.inputs[0].default_value = 0

			#node Group.009
			group_009_4 = _mn_topo_phi_psi.nodes.new("GeometryNodeGroup")
			group_009_4.name = "Group.009"
			group_009_4.node_tree = dihedral_angle

			#node Menu Switch
			menu_switch_4 = _mn_topo_phi_psi.nodes.new("GeometryNodeMenuSwitch")
			menu_switch_4.name = "Menu Switch"
			menu_switch_4.active_index = 1
			menu_switch_4.data_type = 'INT'
			menu_switch_4.enum_items.clear()
			menu_switch_4.enum_items.new("Phi")
			menu_switch_4.enum_items[0].description = ""
			menu_switch_4.enum_items.new("Psi")
			menu_switch_4.enum_items[1].description = ""
			#Item_0
			menu_switch_4.inputs[1].default_value = 0
			#Item_1
			menu_switch_4.inputs[2].default_value = 1

			#node Index Switch
			index_switch_2 = _mn_topo_phi_psi.nodes.new("GeometryNodeIndexSwitch")
			index_switch_2.name = "Index Switch"
			index_switch_2.data_type = 'VECTOR'
			index_switch_2.index_switch_items.clear()
			index_switch_2.index_switch_items.new()
			index_switch_2.index_switch_items.new()

			#node Index Switch.001
			index_switch_001_1 = _mn_topo_phi_psi.nodes.new("GeometryNodeIndexSwitch")
			index_switch_001_1.name = "Index Switch.001"
			index_switch_001_1.data_type = 'VECTOR'
			index_switch_001_1.index_switch_items.clear()
			index_switch_001_1.index_switch_items.new()
			index_switch_001_1.index_switch_items.new()

			#node Index Switch.002
			index_switch_002 = _mn_topo_phi_psi.nodes.new("GeometryNodeIndexSwitch")
			index_switch_002.name = "Index Switch.002"
			index_switch_002.data_type = 'VECTOR'
			index_switch_002.index_switch_items.clear()
			index_switch_002.index_switch_items.new()
			index_switch_002.index_switch_items.new()




			#Set locations
			group_output_70.location = (698.508544921875, 198.78929138183594)
			group_input_70.location = (-520.0, 280.0)
			group_005_4.location = (-380.0, -320.0)
			group_007_3.location = (-380.0, -120.0)
			group_008_4.location = (-380.0, 80.0)
			group_009_4.location = (272.33380126953125, 98.96731567382812)
			menu_switch_4.location = (-340.0, 260.0)
			index_switch_2.location = (-20.0, 140.0)
			index_switch_001_1.location = (-20.0, -100.0)
			index_switch_002.location = (-20.0, -280.0)

			#Set dimensions
			group_output_70.width, group_output_70.height = 140.0, 100.0
			group_input_70.width, group_input_70.height = 140.0, 100.0
			group_005_4.width, group_005_4.height = 171.90289306640625, 100.0
			group_007_3.width, group_007_3.height = 171.90289306640625, 100.0
			group_008_4.width, group_008_4.height = 171.90289306640625, 100.0
			group_009_4.width, group_009_4.height = 299.8184509277344, 100.0
			menu_switch_4.width, menu_switch_4.height = 140.0, 100.0
			index_switch_2.width, index_switch_2.height = 140.0, 100.0
			index_switch_001_1.width, index_switch_001_1.height = 140.0, 100.0
			index_switch_002.width, index_switch_002.height = 140.0, 100.0

			#initialize _mn_topo_phi_psi links
			#group_008_4.CA -> group_009_4.B
			_mn_topo_phi_psi.links.new(group_008_4.outputs[2], group_009_4.inputs[1])
			#index_switch_002.Output -> group_009_4.D
			_mn_topo_phi_psi.links.new(index_switch_002.outputs[0], group_009_4.inputs[3])
			#index_switch_2.Output -> group_009_4.A
			_mn_topo_phi_psi.links.new(index_switch_2.outputs[0], group_009_4.inputs[0])
			#index_switch_001_1.Output -> group_009_4.C
			_mn_topo_phi_psi.links.new(index_switch_001_1.outputs[0], group_009_4.inputs[2])
			#group_009_4.Angle -> group_output_70.Angle
			_mn_topo_phi_psi.links.new(group_009_4.outputs[0], group_output_70.inputs[0])
			#group_009_4.BA⟂(BC) -> group_output_70.BA⟂(BC)
			_mn_topo_phi_psi.links.new(group_009_4.outputs[1], group_output_70.inputs[1])
			#group_009_4.BC -> group_output_70.BC
			_mn_topo_phi_psi.links.new(group_009_4.outputs[3], group_output_70.inputs[3])
			#index_switch_2.Output -> group_output_70.A
			_mn_topo_phi_psi.links.new(index_switch_2.outputs[0], group_output_70.inputs[4])
			#group_008_4.CA -> group_output_70.B
			_mn_topo_phi_psi.links.new(group_008_4.outputs[2], group_output_70.inputs[5])
			#index_switch_001_1.Output -> group_output_70.C
			_mn_topo_phi_psi.links.new(index_switch_001_1.outputs[0], group_output_70.inputs[6])
			#index_switch_002.Output -> group_output_70.D
			_mn_topo_phi_psi.links.new(index_switch_002.outputs[0], group_output_70.inputs[7])
			#group_009_4.CD⟂(BC) -> group_output_70.CD⟂(BC)
			_mn_topo_phi_psi.links.new(group_009_4.outputs[2], group_output_70.inputs[2])
			#menu_switch_4.Output -> index_switch_2.Index
			_mn_topo_phi_psi.links.new(menu_switch_4.outputs[0], index_switch_2.inputs[0])
			#group_input_70.Menu -> menu_switch_4.Menu
			_mn_topo_phi_psi.links.new(group_input_70.outputs[0], menu_switch_4.inputs[0])
			#group_008_4.C -> index_switch_2.0
			_mn_topo_phi_psi.links.new(group_008_4.outputs[1], index_switch_2.inputs[1])
			#menu_switch_4.Output -> index_switch_001_1.Index
			_mn_topo_phi_psi.links.new(menu_switch_4.outputs[0], index_switch_001_1.inputs[0])
			#group_008_4.N -> index_switch_001_1.0
			_mn_topo_phi_psi.links.new(group_008_4.outputs[3], index_switch_001_1.inputs[1])
			#group_008_4.C -> index_switch_001_1.1
			_mn_topo_phi_psi.links.new(group_008_4.outputs[1], index_switch_001_1.inputs[2])
			#menu_switch_4.Output -> index_switch_002.Index
			_mn_topo_phi_psi.links.new(menu_switch_4.outputs[0], index_switch_002.inputs[0])
			#group_007_3.C -> index_switch_002.0
			_mn_topo_phi_psi.links.new(group_007_3.outputs[1], index_switch_002.inputs[1])
			#group_005_4.N -> index_switch_002.1
			_mn_topo_phi_psi.links.new(group_005_4.outputs[3], index_switch_002.inputs[2])
			#group_008_4.N -> index_switch_2.1
			_mn_topo_phi_psi.links.new(group_008_4.outputs[3], index_switch_2.inputs[2])
			return _mn_topo_phi_psi

		_mn_topo_phi_psi = _mn_topo_phi_psi_node_group()

		#initialize between_float node group
		def between_float_node_group():
			between_float = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Between Float")

			between_float.color_tag = 'CONVERTER'
			between_float.description = ""


			#between_float interface
			#Socket Boolean
			boolean_socket_14 = between_float.interface.new_socket(name = "Boolean", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			boolean_socket_14.attribute_domain = 'POINT'

			#Socket Value
			value_socket_9 = between_float.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat')
			value_socket_9.subtype = 'NONE'
			value_socket_9.default_value = 0.0
			value_socket_9.min_value = -3.4028234663852886e+38
			value_socket_9.max_value = 3.4028234663852886e+38
			value_socket_9.attribute_domain = 'POINT'

			#Socket Lower
			lower_socket = between_float.interface.new_socket(name = "Lower", in_out='INPUT', socket_type = 'NodeSocketFloat')
			lower_socket.subtype = 'NONE'
			lower_socket.default_value = 0.0
			lower_socket.min_value = -3.4028234663852886e+38
			lower_socket.max_value = 3.4028234663852886e+38
			lower_socket.attribute_domain = 'POINT'

			#Socket Upper
			upper_socket = between_float.interface.new_socket(name = "Upper", in_out='INPUT', socket_type = 'NodeSocketFloat')
			upper_socket.subtype = 'NONE'
			upper_socket.default_value = 0.0
			upper_socket.min_value = -3.4028234663852886e+38
			upper_socket.max_value = 3.4028234663852886e+38
			upper_socket.attribute_domain = 'POINT'


			#initialize between_float nodes
			#node Group Output
			group_output_71 = between_float.nodes.new("NodeGroupOutput")
			group_output_71.name = "Group Output"
			group_output_71.is_active_output = True

			#node Group Input
			group_input_71 = between_float.nodes.new("NodeGroupInput")
			group_input_71.name = "Group Input"

			#node Compare
			compare_13 = between_float.nodes.new("FunctionNodeCompare")
			compare_13.name = "Compare"
			compare_13.data_type = 'FLOAT'
			compare_13.mode = 'ELEMENT'
			compare_13.operation = 'LESS_EQUAL'

			#node Compare.001
			compare_001_8 = between_float.nodes.new("FunctionNodeCompare")
			compare_001_8.name = "Compare.001"
			compare_001_8.data_type = 'FLOAT'
			compare_001_8.mode = 'ELEMENT'
			compare_001_8.operation = 'GREATER_EQUAL'

			#node Boolean Math
			boolean_math_14 = between_float.nodes.new("FunctionNodeBooleanMath")
			boolean_math_14.name = "Boolean Math"
			boolean_math_14.operation = 'AND'




			#Set locations
			group_output_71.location = (270.0, 0.0)
			group_input_71.location = (-280.0, 0.0)
			compare_13.location = (-80.0, -80.0)
			compare_001_8.location = (-80.0, 80.0)
			boolean_math_14.location = (80.0, 80.0)

			#Set dimensions
			group_output_71.width, group_output_71.height = 140.0, 100.0
			group_input_71.width, group_input_71.height = 140.0, 100.0
			compare_13.width, compare_13.height = 140.0, 100.0
			compare_001_8.width, compare_001_8.height = 140.0, 100.0
			boolean_math_14.width, boolean_math_14.height = 140.0, 100.0

			#initialize between_float links
			#compare_13.Result -> boolean_math_14.Boolean
			between_float.links.new(compare_13.outputs[0], boolean_math_14.inputs[1])
			#compare_001_8.Result -> boolean_math_14.Boolean
			between_float.links.new(compare_001_8.outputs[0], boolean_math_14.inputs[0])
			#group_input_71.Value -> compare_13.A
			between_float.links.new(group_input_71.outputs[0], compare_13.inputs[2])
			#group_input_71.Value -> compare_001_8.A
			between_float.links.new(group_input_71.outputs[0], compare_001_8.inputs[2])
			#boolean_math_14.Boolean -> group_output_71.Boolean
			between_float.links.new(boolean_math_14.outputs[0], group_output_71.inputs[0])
			#group_input_71.Lower -> compare_001_8.B
			between_float.links.new(group_input_71.outputs[1], compare_001_8.inputs[3])
			#group_input_71.Upper -> compare_13.B
			between_float.links.new(group_input_71.outputs[2], compare_13.inputs[3])
			#group_input_71.Value -> compare_001_8.A
			between_float.links.new(group_input_71.outputs[0], compare_001_8.inputs[0])
			#group_input_71.Value -> compare_13.A
			between_float.links.new(group_input_71.outputs[0], compare_13.inputs[0])
			#group_input_71.Lower -> compare_001_8.B
			between_float.links.new(group_input_71.outputs[1], compare_001_8.inputs[1])
			#group_input_71.Upper -> compare_13.B
			between_float.links.new(group_input_71.outputs[2], compare_13.inputs[1])
			return between_float

		between_float = between_float_node_group()

		#initialize helix_detect node group
		def helix_detect_node_group():
			helix_detect = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Helix Detect")

			helix_detect.color_tag = 'NONE'
			helix_detect.description = ""


			#helix_detect interface
			#Socket Boolean
			boolean_socket_15 = helix_detect.interface.new_socket(name = "Boolean", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			boolean_socket_15.attribute_domain = 'POINT'

			#Socket Helix Size
			helix_size_socket = helix_detect.interface.new_socket(name = "Helix Size", in_out='INPUT', socket_type = 'NodeSocketInt')
			helix_size_socket.subtype = 'NONE'
			helix_size_socket.default_value = 3
			helix_size_socket.min_value = -2147483648
			helix_size_socket.max_value = 2147483647
			helix_size_socket.attribute_domain = 'POINT'


			#initialize helix_detect nodes
			#node Group Output
			group_output_72 = helix_detect.nodes.new("NodeGroupOutput")
			group_output_72.name = "Group Output"
			group_output_72.is_active_output = True

			#node Group Input
			group_input_72 = helix_detect.nodes.new("NodeGroupInput")
			group_input_72.name = "Group Input"

			#node Group.003
			group_003_10 = helix_detect.nodes.new("GeometryNodeGroup")
			group_003_10.name = "Group.003"
			group_003_10.node_tree = hbond_backbone_check
			#Socket_3
			group_003_10.inputs[0].default_value = 0
			#Socket_5
			group_003_10.inputs[1].default_value = 0
			#Socket_0
			group_003_10.inputs[2].default_value = 0

			#node Group.017
			group_017_3 = helix_detect.nodes.new("GeometryNodeGroup")
			group_017_3.name = "Group.017"
			group_017_3.node_tree = boolean_run_fill

			#node Math
			math_24 = helix_detect.nodes.new("ShaderNodeMath")
			math_24.name = "Math"
			math_24.operation = 'MULTIPLY'
			math_24.use_clamp = False
			#Value_001
			math_24.inputs[1].default_value = -1.0

			#node Reroute
			reroute_19 = helix_detect.nodes.new("NodeReroute")
			reroute_19.name = "Reroute"
			#node Group
			group_25 = helix_detect.nodes.new("GeometryNodeGroup")
			group_25.name = "Group"
			group_25.node_tree = offset_boolean
			#Socket_1
			group_25.inputs[0].default_value = 0
			#Socket_3
			group_25.inputs[2].default_value = -1

			#node Boolean Math
			boolean_math_15 = helix_detect.nodes.new("FunctionNodeBooleanMath")
			boolean_math_15.name = "Boolean Math"
			boolean_math_15.operation = 'AND'

			#node Boolean Math.001
			boolean_math_001_10 = helix_detect.nodes.new("FunctionNodeBooleanMath")
			boolean_math_001_10.name = "Boolean Math.001"
			boolean_math_001_10.operation = 'OR'

			#node Group.001
			group_001_15 = helix_detect.nodes.new("GeometryNodeGroup")
			group_001_15.name = "Group.001"
			group_001_15.node_tree = offset_boolean
			#Socket_1
			group_001_15.inputs[0].default_value = 0

			#node Frame
			frame_6 = helix_detect.nodes.new("NodeFrame")
			frame_6.label = "Look to see if bonded with i - n residue, being end of helix"
			frame_6.name = "Frame"
			frame_6.label_size = 20
			frame_6.shrink = True

			#node Frame.001
			frame_001_3 = helix_detect.nodes.new("NodeFrame")
			frame_001_3.label = "i and i-1 are both Hbonded n residues ahead (i..i+n are helix)"
			frame_001_3.name = "Frame.001"
			frame_001_3.label_size = 20
			frame_001_3.shrink = True

			#node Frame.002
			frame_002_3 = helix_detect.nodes.new("NodeFrame")
			frame_002_3.label = "Assign to in-between residues"
			frame_002_3.name = "Frame.002"
			frame_002_3.label_size = 20
			frame_002_3.shrink = True

			#node Group.002
			group_002_15 = helix_detect.nodes.new("GeometryNodeGroup")
			group_002_15.name = "Group.002"
			group_002_15.node_tree = _mn_topo_phi_psi
			#Socket_11
			group_002_15.inputs[0].default_value = 'Phi'

			#node Boolean Math.003
			boolean_math_003_3 = helix_detect.nodes.new("FunctionNodeBooleanMath")
			boolean_math_003_3.name = "Boolean Math.003"
			boolean_math_003_3.operation = 'AND'

			#node Group.004
			group_004_5 = helix_detect.nodes.new("GeometryNodeGroup")
			group_004_5.name = "Group.004"
			group_004_5.node_tree = _mn_topo_phi_psi
			#Socket_11
			group_004_5.inputs[0].default_value = 'Psi'

			#node Group.005
			group_005_5 = helix_detect.nodes.new("GeometryNodeGroup")
			group_005_5.name = "Group.005"
			group_005_5.node_tree = between_float
			#Socket_2
			group_005_5.inputs[1].default_value = -120.0
			#Socket_3
			group_005_5.inputs[2].default_value = 45.0

			#node Math.002
			math_002_6 = helix_detect.nodes.new("ShaderNodeMath")
			math_002_6.name = "Math.002"
			math_002_6.operation = 'DEGREES'
			math_002_6.use_clamp = False

			#node Group.006
			group_006_5 = helix_detect.nodes.new("GeometryNodeGroup")
			group_006_5.name = "Group.006"
			group_006_5.node_tree = between_float
			#Socket_2
			group_006_5.inputs[1].default_value = -180.0
			#Socket_3
			group_006_5.inputs[2].default_value = 10.0

			#node Math.003
			math_003_4 = helix_detect.nodes.new("ShaderNodeMath")
			math_003_4.name = "Math.003"
			math_003_4.operation = 'DEGREES'
			math_003_4.use_clamp = False

			#node Boolean Math.002
			boolean_math_002_5 = helix_detect.nodes.new("FunctionNodeBooleanMath")
			boolean_math_002_5.name = "Boolean Math.002"
			boolean_math_002_5.operation = 'AND'

			#node Frame.003
			frame_003_2 = helix_detect.nodes.new("NodeFrame")
			frame_003_2.label = "extra dihedral check, to discard turns in helix-turn-helix"
			frame_003_2.name = "Frame.003"
			frame_003_2.label_size = 20
			frame_003_2.shrink = True



			#Set parents
			group_003_10.parent = frame_001_3
			group_017_3.parent = frame_002_3
			group_25.parent = frame_001_3
			boolean_math_15.parent = frame_001_3
			group_001_15.parent = frame_6
			group_002_15.parent = frame_003_2
			group_004_5.parent = frame_003_2
			group_005_5.parent = frame_003_2
			math_002_6.parent = frame_003_2
			group_006_5.parent = frame_003_2
			math_003_4.parent = frame_003_2
			boolean_math_002_5.parent = frame_003_2

			#Set locations
			group_output_72.location = (680.0, 180.0)
			group_input_72.location = (-800.0, -260.0)
			group_003_10.location = (-500.0, 100.0)
			group_017_3.location = (320.0, -20.0)
			math_24.location = (-300.0, -180.0)
			reroute_19.location = (-540.0, -200.0)
			group_25.location = (-500.0, 240.0)
			boolean_math_15.location = (-340.0, 240.0)
			boolean_math_001_10.location = (-40.0, 240.0)
			group_001_15.location = (-40.0, 20.0)
			frame_6.location = (-10.0, -20.0)
			frame_001_3.location = (10.0, 40.0)
			frame_002_3.location = (-30.0, 200.0)
			group_002_15.location = (254.93621826171875, -98.54428100585938)
			boolean_math_003_3.location = (500.0, 180.0)
			group_004_5.location = (254.93621826171875, -378.5442810058594)
			group_005_5.location = (574.9362182617188, -98.54428100585938)
			math_002_6.location = (414.93621826171875, -98.54428100585938)
			group_006_5.location = (574.9362182617188, -378.5442810058594)
			math_003_4.location = (414.93621826171875, -378.5442810058594)
			boolean_math_002_5.location = (774.9362182617188, -98.54428100585938)
			frame_003_2.location = (35.0, 99.0)

			#Set dimensions
			group_output_72.width, group_output_72.height = 140.0, 100.0
			group_input_72.width, group_input_72.height = 140.0, 100.0
			group_003_10.width, group_003_10.height = 140.0, 100.0
			group_017_3.width, group_017_3.height = 144.84217834472656, 100.0
			math_24.width, math_24.height = 140.0, 100.0
			reroute_19.width, reroute_19.height = 16.0, 100.0
			group_25.width, group_25.height = 140.0, 100.0
			boolean_math_15.width, boolean_math_15.height = 140.0, 100.0
			boolean_math_001_10.width, boolean_math_001_10.height = 140.0, 100.0
			group_001_15.width, group_001_15.height = 140.0, 100.0
			frame_6.width, frame_6.height = 200.0, 187.0
			frame_001_3.width, frame_001_3.height = 360.0, 474.0
			frame_002_3.width, frame_002_3.height = 204.8421630859375, 165.0
			group_002_15.width, group_002_15.height = 140.0, 100.0
			boolean_math_003_3.width, boolean_math_003_3.height = 140.0, 100.0
			group_004_5.width, group_004_5.height = 140.0, 100.0
			group_005_5.width, group_005_5.height = 176.237548828125, 100.0
			math_002_6.width, math_002_6.height = 140.0, 100.0
			group_006_5.width, group_006_5.height = 176.237548828125, 100.0
			math_003_4.width, math_003_4.height = 140.0, 100.0
			boolean_math_002_5.width, boolean_math_002_5.height = 140.0, 100.0
			frame_003_2.width, frame_003_2.height = 720.0, 602.0

			#initialize helix_detect links
			#group_input_72.Helix Size -> math_24.Value
			helix_detect.links.new(group_input_72.outputs[0], math_24.inputs[0])
			#group_input_72.Helix Size -> reroute_19.Input
			helix_detect.links.new(group_input_72.outputs[0], reroute_19.inputs[0])
			#reroute_19.Output -> group_003_10.NH Offset
			helix_detect.links.new(reroute_19.outputs[0], group_003_10.inputs[3])
			#group_003_10.Is Bonded -> group_25.Boolean
			helix_detect.links.new(group_003_10.outputs[0], group_25.inputs[1])
			#group_25.Boolean -> boolean_math_15.Boolean
			helix_detect.links.new(group_25.outputs[0], boolean_math_15.inputs[0])
			#group_003_10.Is Bonded -> boolean_math_15.Boolean
			helix_detect.links.new(group_003_10.outputs[0], boolean_math_15.inputs[1])
			#boolean_math_001_10.Boolean -> group_017_3.Boolean
			helix_detect.links.new(boolean_math_001_10.outputs[0], group_017_3.inputs[0])
			#boolean_math_15.Boolean -> boolean_math_001_10.Boolean
			helix_detect.links.new(boolean_math_15.outputs[0], boolean_math_001_10.inputs[0])
			#boolean_math_15.Boolean -> group_001_15.Boolean
			helix_detect.links.new(boolean_math_15.outputs[0], group_001_15.inputs[1])
			#group_001_15.Boolean -> boolean_math_001_10.Boolean
			helix_detect.links.new(group_001_15.outputs[0], boolean_math_001_10.inputs[1])
			#math_24.Value -> group_001_15.Offset
			helix_detect.links.new(math_24.outputs[0], group_001_15.inputs[2])
			#reroute_19.Output -> group_017_3.Fill Size
			helix_detect.links.new(reroute_19.outputs[0], group_017_3.inputs[1])
			#group_017_3.Boolean -> boolean_math_003_3.Boolean
			helix_detect.links.new(group_017_3.outputs[0], boolean_math_003_3.inputs[0])
			#boolean_math_003_3.Boolean -> group_output_72.Boolean
			helix_detect.links.new(boolean_math_003_3.outputs[0], group_output_72.inputs[0])
			#boolean_math_002_5.Boolean -> boolean_math_003_3.Boolean
			helix_detect.links.new(boolean_math_002_5.outputs[0], boolean_math_003_3.inputs[1])
			#group_002_15.Angle -> math_002_6.Value
			helix_detect.links.new(group_002_15.outputs[0], math_002_6.inputs[0])
			#math_002_6.Value -> group_005_5.Value
			helix_detect.links.new(math_002_6.outputs[0], group_005_5.inputs[0])
			#math_003_4.Value -> group_006_5.Value
			helix_detect.links.new(math_003_4.outputs[0], group_006_5.inputs[0])
			#group_004_5.Angle -> math_003_4.Value
			helix_detect.links.new(group_004_5.outputs[0], math_003_4.inputs[0])
			#group_005_5.Boolean -> boolean_math_002_5.Boolean
			helix_detect.links.new(group_005_5.outputs[0], boolean_math_002_5.inputs[0])
			#group_006_5.Boolean -> boolean_math_002_5.Boolean
			helix_detect.links.new(group_006_5.outputs[0], boolean_math_002_5.inputs[1])
			return helix_detect

		helix_detect = helix_detect_node_group()

		#initialize _mn_topo_calc_helix node group
		def _mn_topo_calc_helix_node_group():
			_mn_topo_calc_helix = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".MN_topo_calc_helix")

			_mn_topo_calc_helix.color_tag = 'NONE'
			_mn_topo_calc_helix.description = ""


			#_mn_topo_calc_helix interface
			#Socket Is Helix
			is_helix_socket_1 = _mn_topo_calc_helix.interface.new_socket(name = "Is Helix", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			is_helix_socket_1.attribute_domain = 'POINT'

			#Socket Bonded Index
			bonded_index_socket = _mn_topo_calc_helix.interface.new_socket(name = "Bonded Index", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			bonded_index_socket.subtype = 'NONE'
			bonded_index_socket.default_value = 0
			bonded_index_socket.min_value = -2147483648
			bonded_index_socket.max_value = 2147483647
			bonded_index_socket.attribute_domain = 'POINT'


			#initialize _mn_topo_calc_helix nodes
			#node Group Output
			group_output_73 = _mn_topo_calc_helix.nodes.new("NodeGroupOutput")
			group_output_73.name = "Group Output"
			group_output_73.is_active_output = True

			#node Group.001
			group_001_16 = _mn_topo_calc_helix.nodes.new("GeometryNodeGroup")
			group_001_16.name = "Group.001"
			group_001_16.node_tree = boolean_run_mask
			#Socket_2
			group_001_16.inputs[1].default_value = 0
			#Socket_3
			group_001_16.inputs[2].default_value = 5
			#Socket_6
			group_001_16.inputs[3].default_value = 0

			#node Boolean Math.004
			boolean_math_004_4 = _mn_topo_calc_helix.nodes.new("FunctionNodeBooleanMath")
			boolean_math_004_4.name = "Boolean Math.004"
			boolean_math_004_4.operation = 'OR'

			#node Boolean Math.005
			boolean_math_005_1 = _mn_topo_calc_helix.nodes.new("FunctionNodeBooleanMath")
			boolean_math_005_1.name = "Boolean Math.005"
			boolean_math_005_1.operation = 'OR'

			#node Group
			group_26 = _mn_topo_calc_helix.nodes.new("GeometryNodeGroup")
			group_26.name = "Group"
			group_26.node_tree = helix_detect
			#Socket_1
			group_26.inputs[0].default_value = 3

			#node Group.002
			group_002_16 = _mn_topo_calc_helix.nodes.new("GeometryNodeGroup")
			group_002_16.name = "Group.002"
			group_002_16.node_tree = helix_detect
			#Socket_1
			group_002_16.inputs[0].default_value = 4

			#node Group.003
			group_003_11 = _mn_topo_calc_helix.nodes.new("GeometryNodeGroup")
			group_003_11.name = "Group.003"
			group_003_11.node_tree = helix_detect
			#Socket_1
			group_003_11.inputs[0].default_value = 5

			#node Group.004
			group_004_6 = _mn_topo_calc_helix.nodes.new("GeometryNodeGroup")
			group_004_6.name = "Group.004"
			group_004_6.node_tree = offset_integer
			#Socket_1
			group_004_6.inputs[0].default_value = 0
			#Socket_2
			group_004_6.inputs[2].default_value = 3

			#node Index
			index_5 = _mn_topo_calc_helix.nodes.new("GeometryNodeInputIndex")
			index_5.name = "Index"

			#node Switch
			switch_15 = _mn_topo_calc_helix.nodes.new("GeometryNodeSwitch")
			switch_15.name = "Switch"
			switch_15.input_type = 'INT'
			#False
			switch_15.inputs[1].default_value = -1

			#node Switch.001
			switch_001_7 = _mn_topo_calc_helix.nodes.new("GeometryNodeSwitch")
			switch_001_7.name = "Switch.001"
			switch_001_7.input_type = 'INT'

			#node Group.005
			group_005_6 = _mn_topo_calc_helix.nodes.new("GeometryNodeGroup")
			group_005_6.name = "Group.005"
			group_005_6.node_tree = offset_integer
			#Socket_1
			group_005_6.inputs[0].default_value = 0
			#Socket_2
			group_005_6.inputs[2].default_value = 4

			#node Switch.002
			switch_002_4 = _mn_topo_calc_helix.nodes.new("GeometryNodeSwitch")
			switch_002_4.name = "Switch.002"
			switch_002_4.input_type = 'INT'

			#node Group.006
			group_006_6 = _mn_topo_calc_helix.nodes.new("GeometryNodeGroup")
			group_006_6.name = "Group.006"
			group_006_6.node_tree = offset_integer
			#Socket_1
			group_006_6.inputs[0].default_value = 0
			#Socket_2
			group_006_6.inputs[2].default_value = 5

			#node Frame
			frame_7 = _mn_topo_calc_helix.nodes.new("NodeFrame")
			frame_7.label = "If part of a helix, return the Index of the CA that is bonded"
			frame_7.name = "Frame"
			frame_7.label_size = 20
			frame_7.shrink = True



			#Set parents
			group_004_6.parent = frame_7
			index_5.parent = frame_7
			switch_15.parent = frame_7
			switch_001_7.parent = frame_7
			group_005_6.parent = frame_7
			switch_002_4.parent = frame_7
			group_006_6.parent = frame_7

			#Set locations
			group_output_73.location = (900.0, 620.0)
			group_001_16.location = (660.0, 620.0)
			boolean_math_004_4.location = (320.0, 620.0)
			boolean_math_005_1.location = (500.0, 620.0)
			group_26.location = (137.64556884765625, 620.0)
			group_002_16.location = (140.0, 500.0)
			group_003_11.location = (320.0, 480.0)
			group_004_6.location = (320.0, 840.0)
			index_5.location = (140.0, 820.0)
			switch_15.location = (320.0, 1000.0)
			switch_001_7.location = (480.0, 1000.0)
			group_005_6.location = (480.0, 840.0)
			switch_002_4.location = (640.0, 1000.0)
			group_006_6.location = (640.0, 840.0)
			frame_7.location = (0.0, 0.0)

			#Set dimensions
			group_output_73.width, group_output_73.height = 140.0, 100.0
			group_001_16.width, group_001_16.height = 208.096435546875, 100.0
			boolean_math_004_4.width, boolean_math_004_4.height = 140.0, 100.0
			boolean_math_005_1.width, boolean_math_005_1.height = 140.0, 100.0
			group_26.width, group_26.height = 142.35443115234375, 100.0
			group_002_16.width, group_002_16.height = 140.0, 100.0
			group_003_11.width, group_003_11.height = 140.0, 100.0
			group_004_6.width, group_004_6.height = 140.0, 100.0
			index_5.width, index_5.height = 140.0, 100.0
			switch_15.width, switch_15.height = 140.0, 100.0
			switch_001_7.width, switch_001_7.height = 140.0, 100.0
			group_005_6.width, group_005_6.height = 140.0, 100.0
			switch_002_4.width, switch_002_4.height = 140.0, 100.0
			group_006_6.width, group_006_6.height = 140.0, 100.0
			frame_7.width, frame_7.height = 700.0, 372.0

			#initialize _mn_topo_calc_helix links
			#boolean_math_004_4.Boolean -> boolean_math_005_1.Boolean
			_mn_topo_calc_helix.links.new(boolean_math_004_4.outputs[0], boolean_math_005_1.inputs[0])
			#group_001_16.Boolean -> group_output_73.Is Helix
			_mn_topo_calc_helix.links.new(group_001_16.outputs[0], group_output_73.inputs[0])
			#group_26.Boolean -> boolean_math_004_4.Boolean
			_mn_topo_calc_helix.links.new(group_26.outputs[0], boolean_math_004_4.inputs[0])
			#group_002_16.Boolean -> boolean_math_004_4.Boolean
			_mn_topo_calc_helix.links.new(group_002_16.outputs[0], boolean_math_004_4.inputs[1])
			#group_003_11.Boolean -> boolean_math_005_1.Boolean
			_mn_topo_calc_helix.links.new(group_003_11.outputs[0], boolean_math_005_1.inputs[1])
			#boolean_math_005_1.Boolean -> group_001_16.Boolean
			_mn_topo_calc_helix.links.new(boolean_math_005_1.outputs[0], group_001_16.inputs[0])
			#index_5.Index -> group_004_6.Value
			_mn_topo_calc_helix.links.new(index_5.outputs[0], group_004_6.inputs[1])
			#group_004_6.Value -> switch_15.True
			_mn_topo_calc_helix.links.new(group_004_6.outputs[0], switch_15.inputs[2])
			#group_26.Boolean -> switch_15.Switch
			_mn_topo_calc_helix.links.new(group_26.outputs[0], switch_15.inputs[0])
			#switch_15.Output -> switch_001_7.False
			_mn_topo_calc_helix.links.new(switch_15.outputs[0], switch_001_7.inputs[1])
			#group_002_16.Boolean -> switch_001_7.Switch
			_mn_topo_calc_helix.links.new(group_002_16.outputs[0], switch_001_7.inputs[0])
			#group_005_6.Value -> switch_001_7.True
			_mn_topo_calc_helix.links.new(group_005_6.outputs[0], switch_001_7.inputs[2])
			#switch_001_7.Output -> switch_002_4.False
			_mn_topo_calc_helix.links.new(switch_001_7.outputs[0], switch_002_4.inputs[1])
			#group_003_11.Boolean -> switch_002_4.Switch
			_mn_topo_calc_helix.links.new(group_003_11.outputs[0], switch_002_4.inputs[0])
			#index_5.Index -> group_005_6.Value
			_mn_topo_calc_helix.links.new(index_5.outputs[0], group_005_6.inputs[1])
			#index_5.Index -> group_006_6.Value
			_mn_topo_calc_helix.links.new(index_5.outputs[0], group_006_6.inputs[1])
			#group_006_6.Value -> switch_002_4.True
			_mn_topo_calc_helix.links.new(group_006_6.outputs[0], switch_002_4.inputs[2])
			#switch_002_4.Output -> group_output_73.Bonded Index
			_mn_topo_calc_helix.links.new(switch_002_4.outputs[0], group_output_73.inputs[1])
			return _mn_topo_calc_helix

		_mn_topo_calc_helix = _mn_topo_calc_helix_node_group()

		#initialize self_sample_proximity node group
		def self_sample_proximity_node_group():
			self_sample_proximity = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Self Sample Proximity")

			self_sample_proximity.color_tag = 'NONE'
			self_sample_proximity.description = ""


			#self_sample_proximity interface
			#Socket Closest Index
			closest_index_socket = self_sample_proximity.interface.new_socket(name = "Closest Index", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			closest_index_socket.subtype = 'NONE'
			closest_index_socket.default_value = 0
			closest_index_socket.min_value = -2147483648
			closest_index_socket.max_value = 2147483647
			closest_index_socket.attribute_domain = 'POINT'

			#Socket Input
			input_socket_2 = self_sample_proximity.interface.new_socket(name = "Input", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			input_socket_2.attribute_domain = 'POINT'

			#Socket Target Position
			target_position_socket = self_sample_proximity.interface.new_socket(name = "Target Position", in_out='INPUT', socket_type = 'NodeSocketVector')
			target_position_socket.subtype = 'NONE'
			target_position_socket.default_value = (0.0, 0.0, 0.0)
			target_position_socket.min_value = -3.4028234663852886e+38
			target_position_socket.max_value = 3.4028234663852886e+38
			target_position_socket.attribute_domain = 'POINT'

			#Socket Self Position
			self_position_socket = self_sample_proximity.interface.new_socket(name = "Self Position", in_out='INPUT', socket_type = 'NodeSocketVector')
			self_position_socket.subtype = 'NONE'
			self_position_socket.default_value = (0.0, 0.0, 0.0)
			self_position_socket.min_value = -3.4028234663852886e+38
			self_position_socket.max_value = 3.4028234663852886e+38
			self_position_socket.attribute_domain = 'POINT'


			#initialize self_sample_proximity nodes
			#node Group Output
			group_output_74 = self_sample_proximity.nodes.new("NodeGroupOutput")
			group_output_74.name = "Group Output"
			group_output_74.is_active_output = True

			#node Group Input
			group_input_73 = self_sample_proximity.nodes.new("NodeGroupInput")
			group_input_73.name = "Group Input"

			#node Set Position.002
			set_position_002_2 = self_sample_proximity.nodes.new("GeometryNodeSetPosition")
			set_position_002_2.name = "Set Position.002"
			#Selection
			set_position_002_2.inputs[1].default_value = True
			#Offset
			set_position_002_2.inputs[3].default_value = (0.0, 0.0, 0.0)

			#node Sample Nearest.001
			sample_nearest_001 = self_sample_proximity.nodes.new("GeometryNodeSampleNearest")
			sample_nearest_001.name = "Sample Nearest.001"
			sample_nearest_001.domain = 'POINT'




			#Set locations
			group_output_74.location = (4.068901062011719, 95.01506042480469)
			group_input_73.location = (-640.0, 20.0)
			set_position_002_2.location = (-380.0, -20.0)
			sample_nearest_001.location = (-220.0, -20.0)

			#Set dimensions
			group_output_74.width, group_output_74.height = 140.0, 100.0
			group_input_73.width, group_input_73.height = 140.0, 100.0
			set_position_002_2.width, set_position_002_2.height = 140.0, 100.0
			sample_nearest_001.width, sample_nearest_001.height = 140.0, 100.0

			#initialize self_sample_proximity links
			#group_input_73.Input -> set_position_002_2.Geometry
			self_sample_proximity.links.new(group_input_73.outputs[0], set_position_002_2.inputs[0])
			#set_position_002_2.Geometry -> sample_nearest_001.Geometry
			self_sample_proximity.links.new(set_position_002_2.outputs[0], sample_nearest_001.inputs[0])
			#group_input_73.Target Position -> set_position_002_2.Position
			self_sample_proximity.links.new(group_input_73.outputs[1], set_position_002_2.inputs[2])
			#group_input_73.Self Position -> sample_nearest_001.Sample Position
			self_sample_proximity.links.new(group_input_73.outputs[2], sample_nearest_001.inputs[1])
			#sample_nearest_001.Index -> group_output_74.Closest Index
			self_sample_proximity.links.new(sample_nearest_001.outputs[0], group_output_74.inputs[0])
			return self_sample_proximity

		self_sample_proximity = self_sample_proximity_node_group()

		#initialize hbond_backbone_check_backup node group
		def hbond_backbone_check_backup_node_group():
			hbond_backbone_check_backup = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "HBond Backbone Check_backup")

			hbond_backbone_check_backup.color_tag = 'NONE'
			hbond_backbone_check_backup.description = ""


			#hbond_backbone_check_backup interface
			#Socket Is Bonded
			is_bonded_socket_2 = hbond_backbone_check_backup.interface.new_socket(name = "Is Bonded", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			is_bonded_socket_2.attribute_domain = 'POINT'

			#Socket Bond Energy
			bond_energy_socket_2 = hbond_backbone_check_backup.interface.new_socket(name = "Bond Energy", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
			bond_energy_socket_2.subtype = 'NONE'
			bond_energy_socket_2.default_value = 0.0
			bond_energy_socket_2.min_value = -3.4028234663852886e+38
			bond_energy_socket_2.max_value = 3.4028234663852886e+38
			bond_energy_socket_2.attribute_domain = 'POINT'

			#Socket H->O
			h__o_socket_1 = hbond_backbone_check_backup.interface.new_socket(name = "H->O", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			h__o_socket_1.subtype = 'NONE'
			h__o_socket_1.default_value = (0.0, 0.0, 0.0)
			h__o_socket_1.min_value = -3.4028234663852886e+38
			h__o_socket_1.max_value = 3.4028234663852886e+38
			h__o_socket_1.attribute_domain = 'POINT'

			#Panel CO
			co_panel_1 = hbond_backbone_check_backup.interface.new_panel("CO")
			#Socket CO Index
			co_index_socket_1 = hbond_backbone_check_backup.interface.new_socket(name = "CO Index", in_out='INPUT', socket_type = 'NodeSocketInt', parent = co_panel_1)
			co_index_socket_1.subtype = 'NONE'
			co_index_socket_1.default_value = 0
			co_index_socket_1.min_value = 0
			co_index_socket_1.max_value = 2147483647
			co_index_socket_1.attribute_domain = 'POINT'

			#Socket CO Offset
			co_offset_socket_1 = hbond_backbone_check_backup.interface.new_socket(name = "CO Offset", in_out='INPUT', socket_type = 'NodeSocketInt', parent = co_panel_1)
			co_offset_socket_1.subtype = 'NONE'
			co_offset_socket_1.default_value = 0
			co_offset_socket_1.min_value = -2147483648
			co_offset_socket_1.max_value = 2147483647
			co_offset_socket_1.attribute_domain = 'POINT'


			#Panel NH
			nh_panel_1 = hbond_backbone_check_backup.interface.new_panel("NH")
			#Socket NH Index
			nh_index_socket_1 = hbond_backbone_check_backup.interface.new_socket(name = "NH Index", in_out='INPUT', socket_type = 'NodeSocketInt', parent = nh_panel_1)
			nh_index_socket_1.subtype = 'NONE'
			nh_index_socket_1.default_value = 0
			nh_index_socket_1.min_value = 0
			nh_index_socket_1.max_value = 2147483647
			nh_index_socket_1.attribute_domain = 'POINT'

			#Socket NH Offset
			nh_offset_socket_1 = hbond_backbone_check_backup.interface.new_socket(name = "NH Offset", in_out='INPUT', socket_type = 'NodeSocketInt', parent = nh_panel_1)
			nh_offset_socket_1.subtype = 'NONE'
			nh_offset_socket_1.default_value = 0
			nh_offset_socket_1.min_value = -2147483648
			nh_offset_socket_1.max_value = 2147483647
			nh_offset_socket_1.attribute_domain = 'POINT'



			#initialize hbond_backbone_check_backup nodes
			#node Group Output
			group_output_75 = hbond_backbone_check_backup.nodes.new("NodeGroupOutput")
			group_output_75.name = "Group Output"
			group_output_75.is_active_output = True

			#node Group Input
			group_input_74 = hbond_backbone_check_backup.nodes.new("NodeGroupInput")
			group_input_74.name = "Group Input"

			#node Group.008
			group_008_5 = hbond_backbone_check_backup.nodes.new("GeometryNodeGroup")
			group_008_5.name = "Group.008"
			group_008_5.node_tree = hbond_energy

			#node Group.009
			group_009_5 = hbond_backbone_check_backup.nodes.new("GeometryNodeGroup")
			group_009_5.name = "Group.009"
			group_009_5.node_tree = mn_topo_backbone
			#Socket_3
			group_009_5.inputs[0].default_value = 0

			#node Evaluate at Index
			evaluate_at_index_7 = hbond_backbone_check_backup.nodes.new("GeometryNodeFieldAtIndex")
			evaluate_at_index_7.name = "Evaluate at Index"
			evaluate_at_index_7.data_type = 'FLOAT_VECTOR'
			evaluate_at_index_7.domain = 'POINT'

			#node Evaluate at Index.001
			evaluate_at_index_001_4 = hbond_backbone_check_backup.nodes.new("GeometryNodeFieldAtIndex")
			evaluate_at_index_001_4.name = "Evaluate at Index.001"
			evaluate_at_index_001_4.data_type = 'FLOAT_VECTOR'
			evaluate_at_index_001_4.domain = 'POINT'

			#node Evaluate at Index.002
			evaluate_at_index_002_3 = hbond_backbone_check_backup.nodes.new("GeometryNodeFieldAtIndex")
			evaluate_at_index_002_3.name = "Evaluate at Index.002"
			evaluate_at_index_002_3.data_type = 'FLOAT_VECTOR'
			evaluate_at_index_002_3.domain = 'POINT'

			#node Evaluate at Index.003
			evaluate_at_index_003_3 = hbond_backbone_check_backup.nodes.new("GeometryNodeFieldAtIndex")
			evaluate_at_index_003_3.name = "Evaluate at Index.003"
			evaluate_at_index_003_3.data_type = 'FLOAT_VECTOR'
			evaluate_at_index_003_3.domain = 'POINT'

			#node Math
			math_25 = hbond_backbone_check_backup.nodes.new("ShaderNodeMath")
			math_25.name = "Math"
			math_25.operation = 'ADD'
			math_25.use_clamp = False

			#node Math.001
			math_001_8 = hbond_backbone_check_backup.nodes.new("ShaderNodeMath")
			math_001_8.name = "Math.001"
			math_001_8.operation = 'ADD'
			math_001_8.use_clamp = False

			#node Math.002
			math_002_7 = hbond_backbone_check_backup.nodes.new("ShaderNodeMath")
			math_002_7.name = "Math.002"
			math_002_7.operation = 'SUBTRACT'
			math_002_7.use_clamp = False

			#node Math.003
			math_003_5 = hbond_backbone_check_backup.nodes.new("ShaderNodeMath")
			math_003_5.name = "Math.003"
			math_003_5.operation = 'ABSOLUTE'
			math_003_5.use_clamp = False

			#node Compare
			compare_14 = hbond_backbone_check_backup.nodes.new("FunctionNodeCompare")
			compare_14.name = "Compare"
			compare_14.data_type = 'FLOAT'
			compare_14.mode = 'ELEMENT'
			compare_14.operation = 'GREATER_THAN'

			#node Integer
			integer_2 = hbond_backbone_check_backup.nodes.new("FunctionNodeInputInt")
			integer_2.name = "Integer"
			integer_2.integer = 1

			#node Frame
			frame_8 = hbond_backbone_check_backup.nodes.new("NodeFrame")
			frame_8.label = "Check not bonded to +/- residues"
			frame_8.name = "Frame"
			frame_8.label_size = 20
			frame_8.shrink = True

			#node Switch
			switch_16 = hbond_backbone_check_backup.nodes.new("GeometryNodeSwitch")
			switch_16.name = "Switch"
			switch_16.input_type = 'BOOLEAN'
			#False
			switch_16.inputs[1].default_value = False

			#node Compare.001
			compare_001_9 = hbond_backbone_check_backup.nodes.new("FunctionNodeCompare")
			compare_001_9.name = "Compare.001"
			compare_001_9.data_type = 'FLOAT'
			compare_001_9.mode = 'ELEMENT'
			compare_001_9.operation = 'LESS_THAN'

			#node Vector Math
			vector_math_9 = hbond_backbone_check_backup.nodes.new("ShaderNodeVectorMath")
			vector_math_9.name = "Vector Math"
			vector_math_9.operation = 'LENGTH'

			#node Group
			group_27 = hbond_backbone_check_backup.nodes.new("GeometryNodeGroup")
			group_27.name = "Group"
			group_27.node_tree = mn_units
			#Input_1
			group_27.inputs[0].default_value = 3.0



			#Set parents
			math_002_7.parent = frame_8
			math_003_5.parent = frame_8
			compare_14.parent = frame_8
			integer_2.parent = frame_8

			#Set locations
			group_output_75.location = (820.0, 240.0)
			group_input_74.location = (-680.0, 140.0)
			group_008_5.location = (224.2731170654297, 240.0)
			group_009_5.location = (-480.0, 460.0)
			evaluate_at_index_7.location = (-20.0, 40.0)
			evaluate_at_index_001_4.location = (-20.0, -120.0)
			evaluate_at_index_002_3.location = (-20.0, 400.0)
			evaluate_at_index_003_3.location = (-20.0, 240.0)
			math_25.location = (-480.0, 240.0)
			math_001_8.location = (-480.0, 80.0)
			math_002_7.location = (70.0, 640.0)
			math_003_5.location = (240.0, 640.0)
			compare_14.location = (420.0, 640.0)
			integer_2.location = (240.0, 500.0)
			frame_8.location = (-70.0, 40.0)
			switch_16.location = (620.0, 340.0)
			compare_001_9.location = (520.0, 140.0)
			vector_math_9.location = (260.0, 20.0)
			group_27.location = (520.0, -20.0)

			#Set dimensions
			group_output_75.width, group_output_75.height = 140.0, 100.0
			group_input_74.width, group_input_74.height = 140.0, 100.0
			group_008_5.width, group_008_5.height = 184.92144775390625, 100.0
			group_009_5.width, group_009_5.height = 140.0, 100.0
			evaluate_at_index_7.width, evaluate_at_index_7.height = 140.0, 100.0
			evaluate_at_index_001_4.width, evaluate_at_index_001_4.height = 140.0, 100.0
			evaluate_at_index_002_3.width, evaluate_at_index_002_3.height = 140.0, 100.0
			evaluate_at_index_003_3.width, evaluate_at_index_003_3.height = 140.0, 100.0
			math_25.width, math_25.height = 140.0, 100.0
			math_001_8.width, math_001_8.height = 140.0, 100.0
			math_002_7.width, math_002_7.height = 140.0, 100.0
			math_003_5.width, math_003_5.height = 140.0, 100.0
			compare_14.width, compare_14.height = 140.0, 100.0
			integer_2.width, integer_2.height = 140.0, 100.0
			frame_8.width, frame_8.height = 550.0, 285.0
			switch_16.width, switch_16.height = 140.0, 100.0
			compare_001_9.width, compare_001_9.height = 140.0, 100.0
			vector_math_9.width, vector_math_9.height = 140.0, 100.0
			group_27.width, group_27.height = 140.0, 100.0

			#initialize hbond_backbone_check_backup links
			#evaluate_at_index_001_4.Value -> group_008_5.H
			hbond_backbone_check_backup.links.new(evaluate_at_index_001_4.outputs[0], group_008_5.inputs[3])
			#evaluate_at_index_7.Value -> group_008_5.N
			hbond_backbone_check_backup.links.new(evaluate_at_index_7.outputs[0], group_008_5.inputs[2])
			#evaluate_at_index_002_3.Value -> group_008_5.O
			hbond_backbone_check_backup.links.new(evaluate_at_index_002_3.outputs[0], group_008_5.inputs[0])
			#math_001_8.Value -> evaluate_at_index_001_4.Index
			hbond_backbone_check_backup.links.new(math_001_8.outputs[0], evaluate_at_index_001_4.inputs[0])
			#math_001_8.Value -> evaluate_at_index_7.Index
			hbond_backbone_check_backup.links.new(math_001_8.outputs[0], evaluate_at_index_7.inputs[0])
			#evaluate_at_index_003_3.Value -> group_008_5.C
			hbond_backbone_check_backup.links.new(evaluate_at_index_003_3.outputs[0], group_008_5.inputs[1])
			#group_009_5.NH -> evaluate_at_index_001_4.Value
			hbond_backbone_check_backup.links.new(group_009_5.outputs[4], evaluate_at_index_001_4.inputs[1])
			#group_009_5.N -> evaluate_at_index_7.Value
			hbond_backbone_check_backup.links.new(group_009_5.outputs[3], evaluate_at_index_7.inputs[1])
			#group_008_5.Bond Energy -> group_output_75.Bond Energy
			hbond_backbone_check_backup.links.new(group_008_5.outputs[1], group_output_75.inputs[1])
			#group_008_5.Bond Vector -> group_output_75.H->O
			hbond_backbone_check_backup.links.new(group_008_5.outputs[2], group_output_75.inputs[2])
			#group_009_5.O -> evaluate_at_index_002_3.Value
			hbond_backbone_check_backup.links.new(group_009_5.outputs[0], evaluate_at_index_002_3.inputs[1])
			#group_009_5.C -> evaluate_at_index_003_3.Value
			hbond_backbone_check_backup.links.new(group_009_5.outputs[1], evaluate_at_index_003_3.inputs[1])
			#math_25.Value -> evaluate_at_index_002_3.Index
			hbond_backbone_check_backup.links.new(math_25.outputs[0], evaluate_at_index_002_3.inputs[0])
			#math_25.Value -> evaluate_at_index_003_3.Index
			hbond_backbone_check_backup.links.new(math_25.outputs[0], evaluate_at_index_003_3.inputs[0])
			#group_input_74.CO Index -> math_25.Value
			hbond_backbone_check_backup.links.new(group_input_74.outputs[0], math_25.inputs[0])
			#group_input_74.CO Offset -> math_25.Value
			hbond_backbone_check_backup.links.new(group_input_74.outputs[1], math_25.inputs[1])
			#group_input_74.NH Index -> math_001_8.Value
			hbond_backbone_check_backup.links.new(group_input_74.outputs[2], math_001_8.inputs[0])
			#group_input_74.NH Offset -> math_001_8.Value
			hbond_backbone_check_backup.links.new(group_input_74.outputs[3], math_001_8.inputs[1])
			#math_25.Value -> math_002_7.Value
			hbond_backbone_check_backup.links.new(math_25.outputs[0], math_002_7.inputs[0])
			#math_001_8.Value -> math_002_7.Value
			hbond_backbone_check_backup.links.new(math_001_8.outputs[0], math_002_7.inputs[1])
			#math_002_7.Value -> math_003_5.Value
			hbond_backbone_check_backup.links.new(math_002_7.outputs[0], math_003_5.inputs[0])
			#math_003_5.Value -> compare_14.A
			hbond_backbone_check_backup.links.new(math_003_5.outputs[0], compare_14.inputs[0])
			#integer_2.Integer -> compare_14.B
			hbond_backbone_check_backup.links.new(integer_2.outputs[0], compare_14.inputs[1])
			#compare_14.Result -> switch_16.Switch
			hbond_backbone_check_backup.links.new(compare_14.outputs[0], switch_16.inputs[0])
			#group_008_5.Bond Vector -> vector_math_9.Vector
			hbond_backbone_check_backup.links.new(group_008_5.outputs[2], vector_math_9.inputs[0])
			#vector_math_9.Value -> compare_001_9.A
			hbond_backbone_check_backup.links.new(vector_math_9.outputs[1], compare_001_9.inputs[0])
			#group_27.Angstrom -> compare_001_9.B
			hbond_backbone_check_backup.links.new(group_27.outputs[0], compare_001_9.inputs[1])
			#switch_16.Output -> group_output_75.Is Bonded
			hbond_backbone_check_backup.links.new(switch_16.outputs[0], group_output_75.inputs[0])
			#group_008_5.Is Bonded -> switch_16.True
			hbond_backbone_check_backup.links.new(group_008_5.outputs[0], switch_16.inputs[2])
			return hbond_backbone_check_backup

		hbond_backbone_check_backup = hbond_backbone_check_backup_node_group()

		#initialize _hbond_i__j__and_hbond_j__i_ node group
		def _hbond_i__j__and_hbond_j__i__node_group():
			_hbond_i__j__and_hbond_j__i_ = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".HBond(i, j) and HBond(j, i)")

			_hbond_i__j__and_hbond_j__i_.color_tag = 'NONE'
			_hbond_i__j__and_hbond_j__i_.description = ""


			#_hbond_i__j__and_hbond_j__i_ interface
			#Socket Boolean
			boolean_socket_16 = _hbond_i__j__and_hbond_j__i_.interface.new_socket(name = "Boolean", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			boolean_socket_16.attribute_domain = 'POINT'

			#Socket i
			i_socket = _hbond_i__j__and_hbond_j__i_.interface.new_socket(name = "i", in_out='INPUT', socket_type = 'NodeSocketInt')
			i_socket.subtype = 'NONE'
			i_socket.default_value = 0
			i_socket.min_value = 0
			i_socket.max_value = 2147483647
			i_socket.attribute_domain = 'POINT'
			i_socket.hide_value = True

			#Socket j
			j_socket = _hbond_i__j__and_hbond_j__i_.interface.new_socket(name = "j", in_out='INPUT', socket_type = 'NodeSocketInt')
			j_socket.subtype = 'NONE'
			j_socket.default_value = 0
			j_socket.min_value = 0
			j_socket.max_value = 2147483647
			j_socket.attribute_domain = 'POINT'
			j_socket.hide_value = True


			#initialize _hbond_i__j__and_hbond_j__i_ nodes
			#node Group Output
			group_output_76 = _hbond_i__j__and_hbond_j__i_.nodes.new("NodeGroupOutput")
			group_output_76.name = "Group Output"
			group_output_76.is_active_output = True

			#node Group Input
			group_input_75 = _hbond_i__j__and_hbond_j__i_.nodes.new("NodeGroupInput")
			group_input_75.name = "Group Input"

			#node Group.010
			group_010_4 = _hbond_i__j__and_hbond_j__i_.nodes.new("GeometryNodeGroup")
			group_010_4.name = "Group.010"
			group_010_4.node_tree = hbond_backbone_check
			#Socket_5
			group_010_4.inputs[1].default_value = 0
			#Socket_6
			group_010_4.inputs[3].default_value = 0

			#node Group.011
			group_011_3 = _hbond_i__j__and_hbond_j__i_.nodes.new("GeometryNodeGroup")
			group_011_3.name = "Group.011"
			group_011_3.node_tree = hbond_backbone_check
			#Socket_5
			group_011_3.inputs[1].default_value = 0
			#Socket_6
			group_011_3.inputs[3].default_value = 0

			#node Frame
			frame_9 = _hbond_i__j__and_hbond_j__i_.nodes.new("NodeFrame")
			frame_9.label = "Check Backbone O is bonded to an NH"
			frame_9.name = "Frame"
			frame_9.label_size = 20
			frame_9.shrink = True

			#node Frame.001
			frame_001_4 = _hbond_i__j__and_hbond_j__i_.nodes.new("NodeFrame")
			frame_001_4.label = "Check Backbone NH is bonded to an O"
			frame_001_4.name = "Frame.001"
			frame_001_4.label_size = 20
			frame_001_4.shrink = True

			#node Boolean Math.003
			boolean_math_003_4 = _hbond_i__j__and_hbond_j__i_.nodes.new("FunctionNodeBooleanMath")
			boolean_math_003_4.name = "Boolean Math.003"
			boolean_math_003_4.operation = 'AND'

			#node Group.012
			group_012_2 = _hbond_i__j__and_hbond_j__i_.nodes.new("GeometryNodeGroup")
			group_012_2.name = "Group.012"
			group_012_2.node_tree = hbond_backbone_check_backup
			#Socket_3
			group_012_2.inputs[0].default_value = 0
			#Socket_5
			group_012_2.inputs[1].default_value = 0
			#Socket_0
			group_012_2.inputs[2].default_value = 0
			#Socket_6
			group_012_2.inputs[3].default_value = 0



			#Set parents
			group_010_4.parent = frame_001_4
			group_011_3.parent = frame_9

			#Set locations
			group_output_76.location = (640.0, 180.0)
			group_input_75.location = (-235.75640869140625, 47.462432861328125)
			group_010_4.location = (-640.0, 40.0)
			group_011_3.location = (-640.0, -220.0)
			frame_9.location = (635.0, 20.0)
			frame_001_4.location = (630.0, 140.0)
			boolean_math_003_4.location = (435.0, 180.0)
			group_012_2.location = (-20.0, 520.0)

			#Set dimensions
			group_output_76.width, group_output_76.height = 140.0, 100.0
			group_input_75.width, group_input_75.height = 140.0, 100.0
			group_010_4.width, group_010_4.height = 267.0645751953125, 100.0
			group_011_3.width, group_011_3.height = 267.0645751953125, 100.0
			frame_9.width, frame_9.height = 327.0645751953125, 309.0
			frame_001_4.width, frame_001_4.height = 327.0645751953125, 309.0
			boolean_math_003_4.width, boolean_math_003_4.height = 140.0, 100.0
			group_012_2.width, group_012_2.height = 267.0645751953125, 100.0

			#initialize _hbond_i__j__and_hbond_j__i_ links
			#group_010_4.Is Bonded -> boolean_math_003_4.Boolean
			_hbond_i__j__and_hbond_j__i_.links.new(group_010_4.outputs[0], boolean_math_003_4.inputs[0])
			#group_011_3.Is Bonded -> boolean_math_003_4.Boolean
			_hbond_i__j__and_hbond_j__i_.links.new(group_011_3.outputs[0], boolean_math_003_4.inputs[1])
			#boolean_math_003_4.Boolean -> group_output_76.Boolean
			_hbond_i__j__and_hbond_j__i_.links.new(boolean_math_003_4.outputs[0], group_output_76.inputs[0])
			#group_input_75.j -> group_010_4.NH Index
			_hbond_i__j__and_hbond_j__i_.links.new(group_input_75.outputs[1], group_010_4.inputs[2])
			#group_input_75.j -> group_011_3.CO Index
			_hbond_i__j__and_hbond_j__i_.links.new(group_input_75.outputs[1], group_011_3.inputs[0])
			#group_input_75.i -> group_010_4.CO Index
			_hbond_i__j__and_hbond_j__i_.links.new(group_input_75.outputs[0], group_010_4.inputs[0])
			#group_input_75.i -> group_011_3.NH Index
			_hbond_i__j__and_hbond_j__i_.links.new(group_input_75.outputs[0], group_011_3.inputs[2])
			return _hbond_i__j__and_hbond_j__i_

		_hbond_i__j__and_hbond_j__i_ = _hbond_i__j__and_hbond_j__i__node_group()

		#initialize _hbond_i___1__j___1__and_hbond_j___1__i___1_ node group
		def _hbond_i___1__j___1__and_hbond_j___1__i___1__node_group():
			_hbond_i___1__j___1__and_hbond_j___1__i___1_ = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".HBond(i - 1, j + 1) and HBond(j - 1, i + 1)")

			_hbond_i___1__j___1__and_hbond_j___1__i___1_.color_tag = 'NONE'
			_hbond_i___1__j___1__and_hbond_j___1__i___1_.description = ""


			#_hbond_i___1__j___1__and_hbond_j___1__i___1_ interface
			#Socket Boolean
			boolean_socket_17 = _hbond_i___1__j___1__and_hbond_j___1__i___1_.interface.new_socket(name = "Boolean", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			boolean_socket_17.attribute_domain = 'POINT'

			#Socket i
			i_socket_1 = _hbond_i___1__j___1__and_hbond_j___1__i___1_.interface.new_socket(name = "i", in_out='INPUT', socket_type = 'NodeSocketInt')
			i_socket_1.subtype = 'NONE'
			i_socket_1.default_value = 0
			i_socket_1.min_value = 0
			i_socket_1.max_value = 2147483647
			i_socket_1.attribute_domain = 'POINT'
			i_socket_1.hide_value = True

			#Socket j
			j_socket_1 = _hbond_i___1__j___1__and_hbond_j___1__i___1_.interface.new_socket(name = "j", in_out='INPUT', socket_type = 'NodeSocketInt')
			j_socket_1.subtype = 'NONE'
			j_socket_1.default_value = 0
			j_socket_1.min_value = 0
			j_socket_1.max_value = 2147483647
			j_socket_1.attribute_domain = 'POINT'
			j_socket_1.hide_value = True


			#initialize _hbond_i___1__j___1__and_hbond_j___1__i___1_ nodes
			#node Group Output
			group_output_77 = _hbond_i___1__j___1__and_hbond_j___1__i___1_.nodes.new("NodeGroupOutput")
			group_output_77.name = "Group Output"
			group_output_77.is_active_output = True

			#node Group Input
			group_input_76 = _hbond_i___1__j___1__and_hbond_j___1__i___1_.nodes.new("NodeGroupInput")
			group_input_76.name = "Group Input"

			#node Group.010
			group_010_5 = _hbond_i___1__j___1__and_hbond_j___1__i___1_.nodes.new("GeometryNodeGroup")
			group_010_5.name = "Group.010"
			group_010_5.node_tree = hbond_backbone_check
			#Socket_5
			group_010_5.inputs[1].default_value = -1
			#Socket_6
			group_010_5.inputs[3].default_value = 1

			#node Group.011
			group_011_4 = _hbond_i___1__j___1__and_hbond_j___1__i___1_.nodes.new("GeometryNodeGroup")
			group_011_4.name = "Group.011"
			group_011_4.node_tree = hbond_backbone_check
			#Socket_5
			group_011_4.inputs[1].default_value = -1
			#Socket_6
			group_011_4.inputs[3].default_value = 1

			#node Frame
			frame_10 = _hbond_i___1__j___1__and_hbond_j___1__i___1_.nodes.new("NodeFrame")
			frame_10.label = "Check Backbone O is bonded to an NH"
			frame_10.name = "Frame"
			frame_10.label_size = 20
			frame_10.shrink = True

			#node Frame.001
			frame_001_5 = _hbond_i___1__j___1__and_hbond_j___1__i___1_.nodes.new("NodeFrame")
			frame_001_5.label = "Check Backbone NH is bonded to an O"
			frame_001_5.name = "Frame.001"
			frame_001_5.label_size = 20
			frame_001_5.shrink = True

			#node Boolean Math.003
			boolean_math_003_5 = _hbond_i___1__j___1__and_hbond_j___1__i___1_.nodes.new("FunctionNodeBooleanMath")
			boolean_math_003_5.name = "Boolean Math.003"
			boolean_math_003_5.operation = 'AND'



			#Set parents
			group_010_5.parent = frame_001_5
			group_011_4.parent = frame_10

			#Set locations
			group_output_77.location = (625.0, 0.0)
			group_input_76.location = (-394.84100341796875, -236.38262939453125)
			group_010_5.location = (-655.0, 40.0)
			group_011_4.location = (-640.0, -220.0)
			frame_10.location = (635.0, 20.0)
			frame_001_5.location = (655.0, 120.0)
			boolean_math_003_5.location = (435.0, 180.0)

			#Set dimensions
			group_output_77.width, group_output_77.height = 140.0, 100.0
			group_input_76.width, group_input_76.height = 140.0, 100.0
			group_010_5.width, group_010_5.height = 267.0645751953125, 100.0
			group_011_4.width, group_011_4.height = 267.0645751953125, 100.0
			frame_10.width, frame_10.height = 327.0645751953125, 309.0
			frame_001_5.width, frame_001_5.height = 327.0645751953125, 309.0
			boolean_math_003_5.width, boolean_math_003_5.height = 140.0, 100.0

			#initialize _hbond_i___1__j___1__and_hbond_j___1__i___1_ links
			#group_010_5.Is Bonded -> boolean_math_003_5.Boolean
			_hbond_i___1__j___1__and_hbond_j___1__i___1_.links.new(group_010_5.outputs[0], boolean_math_003_5.inputs[0])
			#group_011_4.Is Bonded -> boolean_math_003_5.Boolean
			_hbond_i___1__j___1__and_hbond_j___1__i___1_.links.new(group_011_4.outputs[0], boolean_math_003_5.inputs[1])
			#boolean_math_003_5.Boolean -> group_output_77.Boolean
			_hbond_i___1__j___1__and_hbond_j___1__i___1_.links.new(boolean_math_003_5.outputs[0], group_output_77.inputs[0])
			#group_input_76.j -> group_010_5.NH Index
			_hbond_i___1__j___1__and_hbond_j___1__i___1_.links.new(group_input_76.outputs[1], group_010_5.inputs[2])
			#group_input_76.j -> group_011_4.CO Index
			_hbond_i___1__j___1__and_hbond_j___1__i___1_.links.new(group_input_76.outputs[1], group_011_4.inputs[0])
			#group_input_76.i -> group_010_5.CO Index
			_hbond_i___1__j___1__and_hbond_j___1__i___1_.links.new(group_input_76.outputs[0], group_010_5.inputs[0])
			#group_input_76.i -> group_011_4.NH Index
			_hbond_i___1__j___1__and_hbond_j___1__i___1_.links.new(group_input_76.outputs[0], group_011_4.inputs[2])
			return _hbond_i___1__j___1__and_hbond_j___1__i___1_

		_hbond_i___1__j___1__and_hbond_j___1__i___1_ = _hbond_i___1__j___1__and_hbond_j___1__i___1__node_group()

		#initialize _hbond_i___1_j__and_hbond_j_i___1_ node group
		def _hbond_i___1_j__and_hbond_j_i___1__node_group():
			_hbond_i___1_j__and_hbond_j_i___1_ = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".Hbond(i - 1,j) and Hbond(j,i + 1)")

			_hbond_i___1_j__and_hbond_j_i___1_.color_tag = 'NONE'
			_hbond_i___1_j__and_hbond_j_i___1_.description = ""


			#_hbond_i___1_j__and_hbond_j_i___1_ interface
			#Socket Boolean
			boolean_socket_18 = _hbond_i___1_j__and_hbond_j_i___1_.interface.new_socket(name = "Boolean", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			boolean_socket_18.attribute_domain = 'POINT'

			#Socket i
			i_socket_2 = _hbond_i___1_j__and_hbond_j_i___1_.interface.new_socket(name = "i", in_out='INPUT', socket_type = 'NodeSocketInt')
			i_socket_2.subtype = 'NONE'
			i_socket_2.default_value = 0
			i_socket_2.min_value = 0
			i_socket_2.max_value = 2147483647
			i_socket_2.attribute_domain = 'POINT'
			i_socket_2.hide_value = True

			#Socket j
			j_socket_2 = _hbond_i___1_j__and_hbond_j_i___1_.interface.new_socket(name = "j", in_out='INPUT', socket_type = 'NodeSocketInt')
			j_socket_2.subtype = 'NONE'
			j_socket_2.default_value = 0
			j_socket_2.min_value = 0
			j_socket_2.max_value = 2147483647
			j_socket_2.attribute_domain = 'POINT'
			j_socket_2.hide_value = True


			#initialize _hbond_i___1_j__and_hbond_j_i___1_ nodes
			#node Group Output
			group_output_78 = _hbond_i___1_j__and_hbond_j_i___1_.nodes.new("NodeGroupOutput")
			group_output_78.name = "Group Output"
			group_output_78.is_active_output = True

			#node Group Input
			group_input_77 = _hbond_i___1_j__and_hbond_j_i___1_.nodes.new("NodeGroupInput")
			group_input_77.name = "Group Input"

			#node Group.010
			group_010_6 = _hbond_i___1_j__and_hbond_j_i___1_.nodes.new("GeometryNodeGroup")
			group_010_6.name = "Group.010"
			group_010_6.node_tree = hbond_backbone_check
			#Socket_5
			group_010_6.inputs[1].default_value = -1
			#Socket_6
			group_010_6.inputs[3].default_value = 0

			#node Group.011
			group_011_5 = _hbond_i___1_j__and_hbond_j_i___1_.nodes.new("GeometryNodeGroup")
			group_011_5.name = "Group.011"
			group_011_5.node_tree = hbond_backbone_check
			#Socket_5
			group_011_5.inputs[1].default_value = 0
			#Socket_6
			group_011_5.inputs[3].default_value = 1

			#node Frame
			frame_11 = _hbond_i___1_j__and_hbond_j_i___1_.nodes.new("NodeFrame")
			frame_11.label = "Check Backbone O is bonded to an NH"
			frame_11.name = "Frame"
			frame_11.label_size = 20
			frame_11.shrink = True

			#node Frame.001
			frame_001_6 = _hbond_i___1_j__and_hbond_j_i___1_.nodes.new("NodeFrame")
			frame_001_6.label = "Check Backbone NH is bonded to an O"
			frame_001_6.name = "Frame.001"
			frame_001_6.label_size = 20
			frame_001_6.shrink = True

			#node Boolean Math.003
			boolean_math_003_6 = _hbond_i___1_j__and_hbond_j_i___1_.nodes.new("FunctionNodeBooleanMath")
			boolean_math_003_6.name = "Boolean Math.003"
			boolean_math_003_6.operation = 'AND'



			#Set parents
			group_010_6.parent = frame_001_6
			group_011_5.parent = frame_11

			#Set locations
			group_output_78.location = (625.0, 0.0)
			group_input_77.location = (-373.2626953125, 13.94732666015625)
			group_010_6.location = (-640.0, 40.0)
			group_011_5.location = (-640.0, -220.0)
			frame_11.location = (635.0, 20.0)
			frame_001_6.location = (655.0, 120.0)
			boolean_math_003_6.location = (435.0, 180.0)

			#Set dimensions
			group_output_78.width, group_output_78.height = 140.0, 100.0
			group_input_77.width, group_input_77.height = 140.0, 100.0
			group_010_6.width, group_010_6.height = 267.0645751953125, 100.0
			group_011_5.width, group_011_5.height = 267.0645751953125, 100.0
			frame_11.width, frame_11.height = 327.0645751953125, 309.0
			frame_001_6.width, frame_001_6.height = 327.0645751953125, 309.0
			boolean_math_003_6.width, boolean_math_003_6.height = 140.0, 100.0

			#initialize _hbond_i___1_j__and_hbond_j_i___1_ links
			#group_010_6.Is Bonded -> boolean_math_003_6.Boolean
			_hbond_i___1_j__and_hbond_j_i___1_.links.new(group_010_6.outputs[0], boolean_math_003_6.inputs[0])
			#group_011_5.Is Bonded -> boolean_math_003_6.Boolean
			_hbond_i___1_j__and_hbond_j_i___1_.links.new(group_011_5.outputs[0], boolean_math_003_6.inputs[1])
			#boolean_math_003_6.Boolean -> group_output_78.Boolean
			_hbond_i___1_j__and_hbond_j_i___1_.links.new(boolean_math_003_6.outputs[0], group_output_78.inputs[0])
			#group_input_77.j -> group_010_6.NH Index
			_hbond_i___1_j__and_hbond_j_i___1_.links.new(group_input_77.outputs[1], group_010_6.inputs[2])
			#group_input_77.j -> group_011_5.CO Index
			_hbond_i___1_j__and_hbond_j_i___1_.links.new(group_input_77.outputs[1], group_011_5.inputs[0])
			#group_input_77.i -> group_010_6.CO Index
			_hbond_i___1_j__and_hbond_j_i___1_.links.new(group_input_77.outputs[0], group_010_6.inputs[0])
			#group_input_77.i -> group_011_5.NH Index
			_hbond_i___1_j__and_hbond_j_i___1_.links.new(group_input_77.outputs[0], group_011_5.inputs[2])
			return _hbond_i___1_j__and_hbond_j_i___1_

		_hbond_i___1_j__and_hbond_j_i___1_ = _hbond_i___1_j__and_hbond_j_i___1__node_group()

		#initialize _hbond_j___1_i_and_hbond_i_j___1_ node group
		def _hbond_j___1_i_and_hbond_i_j___1__node_group():
			_hbond_j___1_i_and_hbond_i_j___1_ = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".Hbond(j - 1,i)and Hbond(i,j + 1)")

			_hbond_j___1_i_and_hbond_i_j___1_.color_tag = 'NONE'
			_hbond_j___1_i_and_hbond_i_j___1_.description = ""


			#_hbond_j___1_i_and_hbond_i_j___1_ interface
			#Socket Boolean
			boolean_socket_19 = _hbond_j___1_i_and_hbond_i_j___1_.interface.new_socket(name = "Boolean", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			boolean_socket_19.attribute_domain = 'POINT'

			#Socket i
			i_socket_3 = _hbond_j___1_i_and_hbond_i_j___1_.interface.new_socket(name = "i", in_out='INPUT', socket_type = 'NodeSocketInt')
			i_socket_3.subtype = 'NONE'
			i_socket_3.default_value = 0
			i_socket_3.min_value = 0
			i_socket_3.max_value = 2147483647
			i_socket_3.attribute_domain = 'POINT'
			i_socket_3.hide_value = True

			#Socket j
			j_socket_3 = _hbond_j___1_i_and_hbond_i_j___1_.interface.new_socket(name = "j", in_out='INPUT', socket_type = 'NodeSocketInt')
			j_socket_3.subtype = 'NONE'
			j_socket_3.default_value = 0
			j_socket_3.min_value = 0
			j_socket_3.max_value = 2147483647
			j_socket_3.attribute_domain = 'POINT'
			j_socket_3.hide_value = True


			#initialize _hbond_j___1_i_and_hbond_i_j___1_ nodes
			#node Group Output
			group_output_79 = _hbond_j___1_i_and_hbond_i_j___1_.nodes.new("NodeGroupOutput")
			group_output_79.name = "Group Output"
			group_output_79.is_active_output = True

			#node Group Input
			group_input_78 = _hbond_j___1_i_and_hbond_i_j___1_.nodes.new("NodeGroupInput")
			group_input_78.name = "Group Input"

			#node Group.010
			group_010_7 = _hbond_j___1_i_and_hbond_i_j___1_.nodes.new("GeometryNodeGroup")
			group_010_7.name = "Group.010"
			group_010_7.node_tree = hbond_backbone_check
			#Socket_5
			group_010_7.inputs[1].default_value = -1
			#Socket_6
			group_010_7.inputs[3].default_value = 0

			#node Group.011
			group_011_6 = _hbond_j___1_i_and_hbond_i_j___1_.nodes.new("GeometryNodeGroup")
			group_011_6.name = "Group.011"
			group_011_6.node_tree = hbond_backbone_check
			#Socket_5
			group_011_6.inputs[1].default_value = 0
			#Socket_6
			group_011_6.inputs[3].default_value = 1

			#node Frame
			frame_12 = _hbond_j___1_i_and_hbond_i_j___1_.nodes.new("NodeFrame")
			frame_12.label = "Check Backbone O is bonded to an NH"
			frame_12.name = "Frame"
			frame_12.label_size = 20
			frame_12.shrink = True

			#node Frame.001
			frame_001_7 = _hbond_j___1_i_and_hbond_i_j___1_.nodes.new("NodeFrame")
			frame_001_7.label = "Check Backbone NH is bonded to an O"
			frame_001_7.name = "Frame.001"
			frame_001_7.label_size = 20
			frame_001_7.shrink = True

			#node Boolean Math.003
			boolean_math_003_7 = _hbond_j___1_i_and_hbond_i_j___1_.nodes.new("FunctionNodeBooleanMath")
			boolean_math_003_7.name = "Boolean Math.003"
			boolean_math_003_7.operation = 'AND'



			#Set parents
			group_010_7.parent = frame_001_7
			group_011_6.parent = frame_12

			#Set locations
			group_output_79.location = (625.0, 0.0)
			group_input_78.location = (-360.0, 120.0)
			group_010_7.location = (-640.0, 40.0)
			group_011_6.location = (-640.0, -220.0)
			frame_12.location = (635.0, 20.0)
			frame_001_7.location = (655.0, 120.0)
			boolean_math_003_7.location = (435.0, 180.0)

			#Set dimensions
			group_output_79.width, group_output_79.height = 140.0, 100.0
			group_input_78.width, group_input_78.height = 140.0, 100.0
			group_010_7.width, group_010_7.height = 267.0645751953125, 100.0
			group_011_6.width, group_011_6.height = 267.0645751953125, 100.0
			frame_12.width, frame_12.height = 327.0645751953125, 309.0
			frame_001_7.width, frame_001_7.height = 327.0645751953125, 309.0
			boolean_math_003_7.width, boolean_math_003_7.height = 140.0, 100.0

			#initialize _hbond_j___1_i_and_hbond_i_j___1_ links
			#group_010_7.Is Bonded -> boolean_math_003_7.Boolean
			_hbond_j___1_i_and_hbond_i_j___1_.links.new(group_010_7.outputs[0], boolean_math_003_7.inputs[0])
			#group_011_6.Is Bonded -> boolean_math_003_7.Boolean
			_hbond_j___1_i_and_hbond_i_j___1_.links.new(group_011_6.outputs[0], boolean_math_003_7.inputs[1])
			#boolean_math_003_7.Boolean -> group_output_79.Boolean
			_hbond_j___1_i_and_hbond_i_j___1_.links.new(boolean_math_003_7.outputs[0], group_output_79.inputs[0])
			#group_input_78.j -> group_011_6.NH Index
			_hbond_j___1_i_and_hbond_i_j___1_.links.new(group_input_78.outputs[1], group_011_6.inputs[2])
			#group_input_78.j -> group_010_7.CO Index
			_hbond_j___1_i_and_hbond_i_j___1_.links.new(group_input_78.outputs[1], group_010_7.inputs[0])
			#group_input_78.i -> group_010_7.NH Index
			_hbond_j___1_i_and_hbond_i_j___1_.links.new(group_input_78.outputs[0], group_010_7.inputs[2])
			#group_input_78.i -> group_011_6.CO Index
			_hbond_j___1_i_and_hbond_i_j___1_.links.new(group_input_78.outputs[0], group_011_6.inputs[0])
			return _hbond_j___1_i_and_hbond_i_j___1_

		_hbond_j___1_i_and_hbond_i_j___1_ = _hbond_j___1_i_and_hbond_i_j___1__node_group()

		#initialize _dssp_sheet_checks node group
		def _dssp_sheet_checks_node_group():
			_dssp_sheet_checks = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".DSSP Sheet Checks")

			_dssp_sheet_checks.color_tag = 'NONE'
			_dssp_sheet_checks.description = ""


			#_dssp_sheet_checks interface
			#Socket Boolean
			boolean_socket_20 = _dssp_sheet_checks.interface.new_socket(name = "Boolean", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			boolean_socket_20.attribute_domain = 'POINT'

			#Socket j
			j_socket_4 = _dssp_sheet_checks.interface.new_socket(name = "j", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			j_socket_4.subtype = 'NONE'
			j_socket_4.default_value = 0
			j_socket_4.min_value = -2147483648
			j_socket_4.max_value = 2147483647
			j_socket_4.attribute_domain = 'POINT'

			#Socket Index
			index_socket_11 = _dssp_sheet_checks.interface.new_socket(name = "Index", in_out='INPUT', socket_type = 'NodeSocketInt')
			index_socket_11.subtype = 'NONE'
			index_socket_11.default_value = 0
			index_socket_11.min_value = 0
			index_socket_11.max_value = 2147483647
			index_socket_11.attribute_domain = 'POINT'
			index_socket_11.hide_value = True

			#Socket j
			j_socket_5 = _dssp_sheet_checks.interface.new_socket(name = "j", in_out='INPUT', socket_type = 'NodeSocketInt')
			j_socket_5.subtype = 'NONE'
			j_socket_5.default_value = 0
			j_socket_5.min_value = -2147483648
			j_socket_5.max_value = 2147483647
			j_socket_5.attribute_domain = 'POINT'


			#initialize _dssp_sheet_checks nodes
			#node Group Output
			group_output_80 = _dssp_sheet_checks.nodes.new("NodeGroupOutput")
			group_output_80.name = "Group Output"
			group_output_80.is_active_output = True

			#node Group Input
			group_input_79 = _dssp_sheet_checks.nodes.new("NodeGroupInput")
			group_input_79.name = "Group Input"

			#node Group.001
			group_001_17 = _dssp_sheet_checks.nodes.new("GeometryNodeGroup")
			group_001_17.name = "Group.001"
			group_001_17.node_tree = _hbond_i__j__and_hbond_j__i_

			#node Group.002
			group_002_17 = _dssp_sheet_checks.nodes.new("GeometryNodeGroup")
			group_002_17.name = "Group.002"
			group_002_17.node_tree = _hbond_i___1__j___1__and_hbond_j___1__i___1_

			#node Boolean Math
			boolean_math_16 = _dssp_sheet_checks.nodes.new("FunctionNodeBooleanMath")
			boolean_math_16.name = "Boolean Math"
			boolean_math_16.operation = 'OR'

			#node Group.004
			group_004_7 = _dssp_sheet_checks.nodes.new("GeometryNodeGroup")
			group_004_7.name = "Group.004"
			group_004_7.node_tree = _hbond_i___1_j__and_hbond_j_i___1_

			#node Frame
			frame_13 = _dssp_sheet_checks.nodes.new("NodeFrame")
			frame_13.label = "Anti-parallel Bridge"
			frame_13.name = "Frame"
			frame_13.label_size = 20
			frame_13.shrink = True

			#node Frame.001
			frame_001_8 = _dssp_sheet_checks.nodes.new("NodeFrame")
			frame_001_8.label = "Paralell Bridge"
			frame_001_8.name = "Frame.001"
			frame_001_8.label_size = 20
			frame_001_8.shrink = True

			#node Boolean Math.001
			boolean_math_001_11 = _dssp_sheet_checks.nodes.new("FunctionNodeBooleanMath")
			boolean_math_001_11.name = "Boolean Math.001"
			boolean_math_001_11.operation = 'OR'

			#node Boolean Math.002
			boolean_math_002_6 = _dssp_sheet_checks.nodes.new("FunctionNodeBooleanMath")
			boolean_math_002_6.name = "Boolean Math.002"
			boolean_math_002_6.operation = 'OR'

			#node Group.005
			group_005_7 = _dssp_sheet_checks.nodes.new("GeometryNodeGroup")
			group_005_7.name = "Group.005"
			group_005_7.node_tree = _hbond_j___1_i_and_hbond_i_j___1_



			#Set parents
			group_001_17.parent = frame_13
			group_002_17.parent = frame_13
			boolean_math_16.parent = frame_13
			group_004_7.parent = frame_001_8
			boolean_math_001_11.parent = frame_001_8
			group_005_7.parent = frame_001_8

			#Set locations
			group_output_80.location = (570.0, 0.0)
			group_input_79.location = (-657.7005004882812, 1.8694610595703125)
			group_001_17.location = (-800.0, 160.0)
			group_002_17.location = (-800.0, 0.0)
			boolean_math_16.location = (-440.0, 160.0)
			group_004_7.location = (-800.0, -300.0)
			frame_13.location = (580.0, 180.0)
			frame_001_8.location = (580.0, 180.0)
			boolean_math_001_11.location = (-440.0, -300.0)
			boolean_math_002_6.location = (380.0, 140.0)
			group_005_7.location = (-800.0, -460.0)

			#Set dimensions
			group_output_80.width, group_output_80.height = 140.0, 100.0
			group_input_79.width, group_input_79.height = 140.0, 100.0
			group_001_17.width, group_001_17.height = 333.0748291015625, 100.0
			group_002_17.width, group_002_17.height = 333.0748291015625, 100.0
			boolean_math_16.width, boolean_math_16.height = 140.0, 100.0
			group_004_7.width, group_004_7.height = 333.0748291015625, 100.0
			frame_13.width, frame_13.height = 560.0, 350.0
			frame_001_8.width, frame_001_8.height = 560.0, 350.0
			boolean_math_001_11.width, boolean_math_001_11.height = 140.0, 100.0
			boolean_math_002_6.width, boolean_math_002_6.height = 140.0, 100.0
			group_005_7.width, group_005_7.height = 333.0748291015625, 100.0

			#initialize _dssp_sheet_checks links
			#group_001_17.Boolean -> boolean_math_16.Boolean
			_dssp_sheet_checks.links.new(group_001_17.outputs[0], boolean_math_16.inputs[0])
			#group_input_79.j -> group_002_17.j
			_dssp_sheet_checks.links.new(group_input_79.outputs[1], group_002_17.inputs[1])
			#boolean_math_001_11.Boolean -> boolean_math_002_6.Boolean
			_dssp_sheet_checks.links.new(boolean_math_001_11.outputs[0], boolean_math_002_6.inputs[1])
			#group_004_7.Boolean -> boolean_math_001_11.Boolean
			_dssp_sheet_checks.links.new(group_004_7.outputs[0], boolean_math_001_11.inputs[0])
			#group_input_79.j -> group_005_7.j
			_dssp_sheet_checks.links.new(group_input_79.outputs[1], group_005_7.inputs[1])
			#group_002_17.Boolean -> boolean_math_16.Boolean
			_dssp_sheet_checks.links.new(group_002_17.outputs[0], boolean_math_16.inputs[1])
			#group_input_79.j -> group_001_17.j
			_dssp_sheet_checks.links.new(group_input_79.outputs[1], group_001_17.inputs[1])
			#boolean_math_16.Boolean -> boolean_math_002_6.Boolean
			_dssp_sheet_checks.links.new(boolean_math_16.outputs[0], boolean_math_002_6.inputs[0])
			#group_005_7.Boolean -> boolean_math_001_11.Boolean
			_dssp_sheet_checks.links.new(group_005_7.outputs[0], boolean_math_001_11.inputs[1])
			#group_input_79.j -> group_004_7.j
			_dssp_sheet_checks.links.new(group_input_79.outputs[1], group_004_7.inputs[1])
			#boolean_math_002_6.Boolean -> group_output_80.Boolean
			_dssp_sheet_checks.links.new(boolean_math_002_6.outputs[0], group_output_80.inputs[0])
			#group_input_79.Index -> group_001_17.i
			_dssp_sheet_checks.links.new(group_input_79.outputs[0], group_001_17.inputs[0])
			#group_input_79.Index -> group_002_17.i
			_dssp_sheet_checks.links.new(group_input_79.outputs[0], group_002_17.inputs[0])
			#group_input_79.Index -> group_004_7.i
			_dssp_sheet_checks.links.new(group_input_79.outputs[0], group_004_7.inputs[0])
			#group_input_79.Index -> group_005_7.i
			_dssp_sheet_checks.links.new(group_input_79.outputs[0], group_005_7.inputs[0])
			#group_input_79.j -> group_output_80.j
			_dssp_sheet_checks.links.new(group_input_79.outputs[1], group_output_80.inputs[1])
			return _dssp_sheet_checks

		_dssp_sheet_checks = _dssp_sheet_checks_node_group()

		#initialize _mn_topo_calc_sheet node group
		def _mn_topo_calc_sheet_node_group():
			_mn_topo_calc_sheet = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".MN_topo_calc_sheet")

			_mn_topo_calc_sheet.color_tag = 'NONE'
			_mn_topo_calc_sheet.description = ""


			#_mn_topo_calc_sheet interface
			#Socket Geometry
			geometry_socket_14 = _mn_topo_calc_sheet.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			geometry_socket_14.attribute_domain = 'POINT'

			#Socket Attribute
			attribute_socket = _mn_topo_calc_sheet.interface.new_socket(name = "Attribute", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			attribute_socket.attribute_domain = 'POINT'

			#Socket Geometry
			geometry_socket_15 = _mn_topo_calc_sheet.interface.new_socket(name = "Geometry", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			geometry_socket_15.attribute_domain = 'POINT'


			#initialize _mn_topo_calc_sheet nodes
			#node Group Output
			group_output_81 = _mn_topo_calc_sheet.nodes.new("NodeGroupOutput")
			group_output_81.name = "Group Output"
			group_output_81.is_active_output = True

			#node Group Input
			group_input_80 = _mn_topo_calc_sheet.nodes.new("NodeGroupInput")
			group_input_80.name = "Group Input"

			#node Capture Attribute.002
			capture_attribute_002_3 = _mn_topo_calc_sheet.nodes.new("GeometryNodeCaptureAttribute")
			capture_attribute_002_3.name = "Capture Attribute.002"
			capture_attribute_002_3.active_index = 0
			capture_attribute_002_3.capture_items.clear()
			capture_attribute_002_3.capture_items.new('FLOAT', "Value")
			capture_attribute_002_3.capture_items["Value"].data_type = 'BOOLEAN'
			capture_attribute_002_3.domain = 'POINT'

			#node Group.003
			group_003_12 = _mn_topo_calc_sheet.nodes.new("GeometryNodeGroup")
			group_003_12.name = "Group.003"
			group_003_12.node_tree = boolean_run_mask
			#Socket_2
			group_003_12.inputs[1].default_value = 0
			#Socket_3
			group_003_12.inputs[2].default_value = 3
			#Socket_6
			group_003_12.inputs[3].default_value = 0

			#node Group
			group_28 = _mn_topo_calc_sheet.nodes.new("GeometryNodeGroup")
			group_28.name = "Group"
			group_28.mute = True
			group_28.node_tree = boolean_run_fill
			#Socket_2
			group_28.inputs[1].default_value = 1

			#node Group.006
			group_006_7 = _mn_topo_calc_sheet.nodes.new("GeometryNodeGroup")
			group_006_7.name = "Group.006"
			group_006_7.node_tree = self_sample_proximity

			#node Group.007
			group_007_4 = _mn_topo_calc_sheet.nodes.new("GeometryNodeGroup")
			group_007_4.name = "Group.007"
			group_007_4.node_tree = mn_topo_backbone
			#Socket_3
			group_007_4.inputs[0].default_value = 0

			#node Capture Attribute
			capture_attribute_7 = _mn_topo_calc_sheet.nodes.new("GeometryNodeCaptureAttribute")
			capture_attribute_7.name = "Capture Attribute"
			capture_attribute_7.active_index = 3
			capture_attribute_7.capture_items.clear()
			capture_attribute_7.capture_items.new('FLOAT', "Value")
			capture_attribute_7.capture_items["Value"].data_type = 'INT'
			capture_attribute_7.capture_items.new('FLOAT', "Closest Index")
			capture_attribute_7.capture_items["Closest Index"].data_type = 'INT'
			capture_attribute_7.capture_items.new('FLOAT', "Closest Index.001")
			capture_attribute_7.capture_items["Closest Index.001"].data_type = 'INT'
			capture_attribute_7.capture_items.new('FLOAT', "Closest Index.002")
			capture_attribute_7.capture_items["Closest Index.002"].data_type = 'INT'
			capture_attribute_7.domain = 'POINT'

			#node Group.008
			group_008_6 = _mn_topo_calc_sheet.nodes.new("GeometryNodeGroup")
			group_008_6.name = "Group.008"
			group_008_6.node_tree = _dssp_sheet_checks
			#Socket_3
			group_008_6.inputs[0].default_value = 0

			#node Group.009
			group_009_6 = _mn_topo_calc_sheet.nodes.new("GeometryNodeGroup")
			group_009_6.name = "Group.009"
			group_009_6.node_tree = _dssp_sheet_checks
			#Socket_3
			group_009_6.inputs[0].default_value = 0

			#node Boolean Math
			boolean_math_17 = _mn_topo_calc_sheet.nodes.new("FunctionNodeBooleanMath")
			boolean_math_17.name = "Boolean Math"
			boolean_math_17.operation = 'OR'

			#node Group.010
			group_010_8 = _mn_topo_calc_sheet.nodes.new("GeometryNodeGroup")
			group_010_8.name = "Group.010"
			group_010_8.node_tree = _dssp_sheet_checks
			#Socket_3
			group_010_8.inputs[0].default_value = 0

			#node Boolean Math.001
			boolean_math_001_12 = _mn_topo_calc_sheet.nodes.new("FunctionNodeBooleanMath")
			boolean_math_001_12.name = "Boolean Math.001"
			boolean_math_001_12.operation = 'OR'

			#node Group.011
			group_011_7 = _mn_topo_calc_sheet.nodes.new("GeometryNodeGroup")
			group_011_7.name = "Group.011"
			group_011_7.node_tree = self_sample_proximity

			#node Group.012
			group_012_3 = _mn_topo_calc_sheet.nodes.new("GeometryNodeGroup")
			group_012_3.name = "Group.012"
			group_012_3.node_tree = mn_topo_backbone
			#Socket_3
			group_012_3.inputs[0].default_value = 0

			#node Vector Math
			vector_math_10 = _mn_topo_calc_sheet.nodes.new("ShaderNodeVectorMath")
			vector_math_10.name = "Vector Math"
			vector_math_10.operation = 'SUBTRACT'

			#node Vector Math.001
			vector_math_001_6 = _mn_topo_calc_sheet.nodes.new("ShaderNodeVectorMath")
			vector_math_001_6.name = "Vector Math.001"
			vector_math_001_6.operation = 'ADD'

			#node Vector Math.002
			vector_math_002_6 = _mn_topo_calc_sheet.nodes.new("ShaderNodeVectorMath")
			vector_math_002_6.name = "Vector Math.002"
			vector_math_002_6.operation = 'SCALE'
			#Scale
			vector_math_002_6.inputs[3].default_value = 3.0

			#node Group.013
			group_013_2 = _mn_topo_calc_sheet.nodes.new("GeometryNodeGroup")
			group_013_2.name = "Group.013"
			group_013_2.node_tree = self_sample_proximity

			#node Group.014
			group_014_3 = _mn_topo_calc_sheet.nodes.new("GeometryNodeGroup")
			group_014_3.name = "Group.014"
			group_014_3.node_tree = self_sample_proximity

			#node Vector Math.003
			vector_math_003_2 = _mn_topo_calc_sheet.nodes.new("ShaderNodeVectorMath")
			vector_math_003_2.name = "Vector Math.003"
			vector_math_003_2.operation = 'SUBTRACT'

			#node Group.015
			group_015_1 = _mn_topo_calc_sheet.nodes.new("GeometryNodeGroup")
			group_015_1.name = "Group.015"
			group_015_1.node_tree = _dssp_sheet_checks
			#Socket_3
			group_015_1.inputs[0].default_value = 0

			#node Boolean Math.002
			boolean_math_002_7 = _mn_topo_calc_sheet.nodes.new("FunctionNodeBooleanMath")
			boolean_math_002_7.name = "Boolean Math.002"
			boolean_math_002_7.operation = 'OR'

			#node Group.016
			group_016_4 = _mn_topo_calc_sheet.nodes.new("GeometryNodeGroup")
			group_016_4.name = "Group.016"
			group_016_4.node_tree = _dssp_sheet_checks
			#Socket_3
			group_016_4.inputs[0].default_value = 0

			#node Boolean Math.003
			boolean_math_003_8 = _mn_topo_calc_sheet.nodes.new("FunctionNodeBooleanMath")
			boolean_math_003_8.name = "Boolean Math.003"
			boolean_math_003_8.operation = 'OR'

			#node Group.017
			group_017_4 = _mn_topo_calc_sheet.nodes.new("GeometryNodeGroup")
			group_017_4.name = "Group.017"
			group_017_4.node_tree = _dssp_sheet_checks
			#Socket_3
			group_017_4.inputs[0].default_value = 0

			#node Reroute
			reroute_20 = _mn_topo_calc_sheet.nodes.new("NodeReroute")
			reroute_20.name = "Reroute"
			#node Boolean Math.004
			boolean_math_004_5 = _mn_topo_calc_sheet.nodes.new("FunctionNodeBooleanMath")
			boolean_math_004_5.name = "Boolean Math.004"
			boolean_math_004_5.operation = 'OR'

			#node Store Named Attribute
			store_named_attribute_3 = _mn_topo_calc_sheet.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_3.name = "Store Named Attribute"
			store_named_attribute_3.data_type = 'INT'
			store_named_attribute_3.domain = 'POINT'
			#Name
			store_named_attribute_3.inputs[2].default_value = "tmp_bonded_idx"

			#node Store Named Attribute.001
			store_named_attribute_001_2 = _mn_topo_calc_sheet.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_001_2.name = "Store Named Attribute.001"
			store_named_attribute_001_2.data_type = 'INT'
			store_named_attribute_001_2.domain = 'POINT'
			#Name
			store_named_attribute_001_2.inputs[2].default_value = "tmp_bonded_idx"

			#node Store Named Attribute.002
			store_named_attribute_002_2 = _mn_topo_calc_sheet.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_002_2.name = "Store Named Attribute.002"
			store_named_attribute_002_2.data_type = 'INT'
			store_named_attribute_002_2.domain = 'POINT'
			#Selection
			store_named_attribute_002_2.inputs[1].default_value = True
			#Name
			store_named_attribute_002_2.inputs[2].default_value = "tmp_bonded_idx"
			#Value
			store_named_attribute_002_2.inputs[3].default_value = -1

			#node Store Named Attribute.003
			store_named_attribute_003_1 = _mn_topo_calc_sheet.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_003_1.name = "Store Named Attribute.003"
			store_named_attribute_003_1.data_type = 'INT'
			store_named_attribute_003_1.domain = 'POINT'
			#Name
			store_named_attribute_003_1.inputs[2].default_value = "tmp_bonded_idx"

			#node Store Named Attribute.004
			store_named_attribute_004_1 = _mn_topo_calc_sheet.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_004_1.name = "Store Named Attribute.004"
			store_named_attribute_004_1.data_type = 'INT'
			store_named_attribute_004_1.domain = 'POINT'
			#Name
			store_named_attribute_004_1.inputs[2].default_value = "tmp_bonded_idx"

			#node Store Named Attribute.005
			store_named_attribute_005_1 = _mn_topo_calc_sheet.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_005_1.name = "Store Named Attribute.005"
			store_named_attribute_005_1.data_type = 'INT'
			store_named_attribute_005_1.domain = 'POINT'
			#Name
			store_named_attribute_005_1.inputs[2].default_value = "tmp_bonded_idx"

			#node Store Named Attribute.006
			store_named_attribute_006 = _mn_topo_calc_sheet.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_006.name = "Store Named Attribute.006"
			store_named_attribute_006.data_type = 'INT'
			store_named_attribute_006.domain = 'POINT'
			#Name
			store_named_attribute_006.inputs[2].default_value = "tmp_bonded_idx"

			#node Group.001
			group_001_18 = _mn_topo_calc_sheet.nodes.new("GeometryNodeGroup")
			group_001_18.name = "Group.001"
			group_001_18.node_tree = offset_integer
			#Socket_1
			group_001_18.inputs[0].default_value = 0
			#Socket_2
			group_001_18.inputs[2].default_value = 1

			#node Math
			math_26 = _mn_topo_calc_sheet.nodes.new("ShaderNodeMath")
			math_26.name = "Math"
			math_26.operation = 'ADD'
			math_26.use_clamp = False
			#Value_001
			math_26.inputs[1].default_value = -1.0

			#node Group.002
			group_002_18 = _mn_topo_calc_sheet.nodes.new("GeometryNodeGroup")
			group_002_18.name = "Group.002"
			group_002_18.node_tree = offset_integer
			#Socket_1
			group_002_18.inputs[0].default_value = 0
			#Socket_2
			group_002_18.inputs[2].default_value = 1

			#node Math.001
			math_001_9 = _mn_topo_calc_sheet.nodes.new("ShaderNodeMath")
			math_001_9.name = "Math.001"
			math_001_9.operation = 'ADD'
			math_001_9.use_clamp = False
			#Value_001
			math_001_9.inputs[1].default_value = -1.0




			#Set locations
			group_output_81.location = (1360.0, 240.0)
			group_input_80.location = (-1780.0, 80.0)
			capture_attribute_002_3.location = (960.0, 240.0)
			group_003_12.location = (960.0, -80.0)
			group_28.location = (960.0, 60.0)
			group_006_7.location = (-1520.0, 20.0)
			group_007_4.location = (-2100.0, -60.0)
			capture_attribute_7.location = (-1240.0, 100.0)
			group_008_6.location = (-340.0, 20.0)
			group_009_6.location = (-340.0, -120.0)
			boolean_math_17.location = (40.0, 0.0)
			group_010_8.location = (-340.0, -260.0)
			boolean_math_001_12.location = (40.0, -140.0)
			group_011_7.location = (-1520.0, -320.0)
			group_012_3.location = (-2300.0, -280.0)
			vector_math_10.location = (-2060.0, -600.0)
			vector_math_001_6.location = (-1740.0, -600.0)
			vector_math_002_6.location = (-1900.0, -600.0)
			group_013_2.location = (-1520.0, -140.0)
			group_014_3.location = (-1520.0, -480.0)
			vector_math_003_2.location = (-1740.0, -740.0)
			group_015_1.location = (-340.0, -400.0)
			boolean_math_002_7.location = (40.0, -280.0)
			group_016_4.location = (-344.5273742675781, -540.385498046875)
			boolean_math_003_8.location = (40.0, -440.0)
			group_017_4.location = (-340.0, -680.0)
			reroute_20.location = (-740.0, -640.0)
			boolean_math_004_5.location = (40.0, -600.0)
			store_named_attribute_3.location = (-180.0, 240.0)
			store_named_attribute_001_2.location = (-20.0, 240.0)
			store_named_attribute_002_2.location = (-340.0, 240.0)
			store_named_attribute_003_1.location = (140.0, 240.0)
			store_named_attribute_004_1.location = (300.0, 240.0)
			store_named_attribute_005_1.location = (460.0, 240.0)
			store_named_attribute_006.location = (620.0, 240.0)
			group_001_18.location = (-680.0, -540.0)
			math_26.location = (-520.0, -540.0)
			group_002_18.location = (-680.0, -720.0)
			math_001_9.location = (-520.0, -720.0)

			#Set dimensions
			group_output_81.width, group_output_81.height = 140.0, 100.0
			group_input_80.width, group_input_80.height = 140.0, 100.0
			capture_attribute_002_3.width, capture_attribute_002_3.height = 140.0, 100.0
			group_003_12.width, group_003_12.height = 167.49020385742188, 100.0
			group_28.width, group_28.height = 140.0, 100.0
			group_006_7.width, group_006_7.height = 140.0, 100.0
			group_007_4.width, group_007_4.height = 140.0, 100.0
			capture_attribute_7.width, capture_attribute_7.height = 140.0, 100.0
			group_008_6.width, group_008_6.height = 140.0, 100.0
			group_009_6.width, group_009_6.height = 140.0, 100.0
			boolean_math_17.width, boolean_math_17.height = 140.0, 100.0
			group_010_8.width, group_010_8.height = 140.0, 100.0
			boolean_math_001_12.width, boolean_math_001_12.height = 140.0, 100.0
			group_011_7.width, group_011_7.height = 140.0, 100.0
			group_012_3.width, group_012_3.height = 140.0, 100.0
			vector_math_10.width, vector_math_10.height = 140.0, 100.0
			vector_math_001_6.width, vector_math_001_6.height = 140.0, 100.0
			vector_math_002_6.width, vector_math_002_6.height = 140.0, 100.0
			group_013_2.width, group_013_2.height = 140.0, 100.0
			group_014_3.width, group_014_3.height = 140.0, 100.0
			vector_math_003_2.width, vector_math_003_2.height = 140.0, 100.0
			group_015_1.width, group_015_1.height = 140.0, 100.0
			boolean_math_002_7.width, boolean_math_002_7.height = 140.0, 100.0
			group_016_4.width, group_016_4.height = 140.0, 100.0
			boolean_math_003_8.width, boolean_math_003_8.height = 140.0, 100.0
			group_017_4.width, group_017_4.height = 140.0, 100.0
			reroute_20.width, reroute_20.height = 16.0, 100.0
			boolean_math_004_5.width, boolean_math_004_5.height = 140.0, 100.0
			store_named_attribute_3.width, store_named_attribute_3.height = 140.0, 100.0
			store_named_attribute_001_2.width, store_named_attribute_001_2.height = 140.0, 100.0
			store_named_attribute_002_2.width, store_named_attribute_002_2.height = 140.0, 100.0
			store_named_attribute_003_1.width, store_named_attribute_003_1.height = 140.0, 100.0
			store_named_attribute_004_1.width, store_named_attribute_004_1.height = 140.0, 100.0
			store_named_attribute_005_1.width, store_named_attribute_005_1.height = 140.0, 100.0
			store_named_attribute_006.width, store_named_attribute_006.height = 140.0, 100.0
			group_001_18.width, group_001_18.height = 140.0, 100.0
			math_26.width, math_26.height = 140.0, 100.0
			group_002_18.width, group_002_18.height = 140.0, 100.0
			math_001_9.width, math_001_9.height = 140.0, 100.0

			#initialize _mn_topo_calc_sheet links
			#store_named_attribute_006.Geometry -> capture_attribute_002_3.Geometry
			_mn_topo_calc_sheet.links.new(store_named_attribute_006.outputs[0], capture_attribute_002_3.inputs[0])
			#capture_attribute_002_3.Geometry -> group_output_81.Geometry
			_mn_topo_calc_sheet.links.new(capture_attribute_002_3.outputs[0], group_output_81.inputs[0])
			#capture_attribute_002_3.Value -> group_output_81.Attribute
			_mn_topo_calc_sheet.links.new(capture_attribute_002_3.outputs[1], group_output_81.inputs[1])
			#group_28.Boolean -> capture_attribute_002_3.Value
			_mn_topo_calc_sheet.links.new(group_28.outputs[0], capture_attribute_002_3.inputs[1])
			#group_input_80.Geometry -> group_006_7.Input
			_mn_topo_calc_sheet.links.new(group_input_80.outputs[0], group_006_7.inputs[0])
			#group_007_4.NH -> group_006_7.Target Position
			_mn_topo_calc_sheet.links.new(group_007_4.outputs[4], group_006_7.inputs[1])
			#group_007_4.O -> group_006_7.Self Position
			_mn_topo_calc_sheet.links.new(group_007_4.outputs[0], group_006_7.inputs[2])
			#group_input_80.Geometry -> capture_attribute_7.Geometry
			_mn_topo_calc_sheet.links.new(group_input_80.outputs[0], capture_attribute_7.inputs[0])
			#group_006_7.Closest Index -> capture_attribute_7.Value
			_mn_topo_calc_sheet.links.new(group_006_7.outputs[0], capture_attribute_7.inputs[1])
			#capture_attribute_7.Value -> group_008_6.j
			_mn_topo_calc_sheet.links.new(capture_attribute_7.outputs[1], group_008_6.inputs[1])
			#group_008_6.Boolean -> boolean_math_17.Boolean
			_mn_topo_calc_sheet.links.new(group_008_6.outputs[0], boolean_math_17.inputs[0])
			#group_003_12.Boolean -> group_28.Boolean
			_mn_topo_calc_sheet.links.new(group_003_12.outputs[0], group_28.inputs[0])
			#boolean_math_17.Boolean -> boolean_math_001_12.Boolean
			_mn_topo_calc_sheet.links.new(boolean_math_17.outputs[0], boolean_math_001_12.inputs[0])
			#group_input_80.Geometry -> group_011_7.Input
			_mn_topo_calc_sheet.links.new(group_input_80.outputs[0], group_011_7.inputs[0])
			#capture_attribute_7.Closest Index -> group_009_6.j
			_mn_topo_calc_sheet.links.new(capture_attribute_7.outputs[2], group_009_6.inputs[1])
			#group_012_3.O -> vector_math_10.Vector
			_mn_topo_calc_sheet.links.new(group_012_3.outputs[0], vector_math_10.inputs[1])
			#group_012_3.CA -> vector_math_001_6.Vector
			_mn_topo_calc_sheet.links.new(group_012_3.outputs[2], vector_math_001_6.inputs[0])
			#vector_math_10.Vector -> vector_math_002_6.Vector
			_mn_topo_calc_sheet.links.new(vector_math_10.outputs[0], vector_math_002_6.inputs[0])
			#vector_math_002_6.Vector -> vector_math_001_6.Vector
			_mn_topo_calc_sheet.links.new(vector_math_002_6.outputs[0], vector_math_001_6.inputs[1])
			#group_012_3.CA -> group_011_7.Target Position
			_mn_topo_calc_sheet.links.new(group_012_3.outputs[2], group_011_7.inputs[1])
			#vector_math_001_6.Vector -> group_011_7.Self Position
			_mn_topo_calc_sheet.links.new(vector_math_001_6.outputs[0], group_011_7.inputs[2])
			#group_012_3.C -> vector_math_10.Vector
			_mn_topo_calc_sheet.links.new(group_012_3.outputs[1], vector_math_10.inputs[0])
			#group_input_80.Geometry -> group_013_2.Input
			_mn_topo_calc_sheet.links.new(group_input_80.outputs[0], group_013_2.inputs[0])
			#capture_attribute_7.Closest Index.001 -> group_010_8.j
			_mn_topo_calc_sheet.links.new(capture_attribute_7.outputs[3], group_010_8.inputs[1])
			#group_012_3.NH -> group_013_2.Self Position
			_mn_topo_calc_sheet.links.new(group_012_3.outputs[4], group_013_2.inputs[2])
			#group_012_3.O -> group_013_2.Target Position
			_mn_topo_calc_sheet.links.new(group_012_3.outputs[0], group_013_2.inputs[1])
			#group_010_8.Boolean -> boolean_math_001_12.Boolean
			_mn_topo_calc_sheet.links.new(group_010_8.outputs[0], boolean_math_001_12.inputs[1])
			#group_009_6.Boolean -> boolean_math_17.Boolean
			_mn_topo_calc_sheet.links.new(group_009_6.outputs[0], boolean_math_17.inputs[1])
			#group_input_80.Geometry -> group_014_3.Input
			_mn_topo_calc_sheet.links.new(group_input_80.outputs[0], group_014_3.inputs[0])
			#group_012_3.CA -> group_014_3.Target Position
			_mn_topo_calc_sheet.links.new(group_012_3.outputs[2], group_014_3.inputs[1])
			#group_012_3.CA -> vector_math_003_2.Vector
			_mn_topo_calc_sheet.links.new(group_012_3.outputs[2], vector_math_003_2.inputs[0])
			#vector_math_002_6.Vector -> vector_math_003_2.Vector
			_mn_topo_calc_sheet.links.new(vector_math_002_6.outputs[0], vector_math_003_2.inputs[1])
			#vector_math_003_2.Vector -> group_014_3.Self Position
			_mn_topo_calc_sheet.links.new(vector_math_003_2.outputs[0], group_014_3.inputs[2])
			#capture_attribute_7.Closest Index.002 -> group_015_1.j
			_mn_topo_calc_sheet.links.new(capture_attribute_7.outputs[4], group_015_1.inputs[1])
			#boolean_math_001_12.Boolean -> boolean_math_002_7.Boolean
			_mn_topo_calc_sheet.links.new(boolean_math_001_12.outputs[0], boolean_math_002_7.inputs[0])
			#group_015_1.Boolean -> boolean_math_002_7.Boolean
			_mn_topo_calc_sheet.links.new(group_015_1.outputs[0], boolean_math_002_7.inputs[1])
			#boolean_math_002_7.Boolean -> boolean_math_003_8.Boolean
			_mn_topo_calc_sheet.links.new(boolean_math_002_7.outputs[0], boolean_math_003_8.inputs[0])
			#group_016_4.Boolean -> boolean_math_003_8.Boolean
			_mn_topo_calc_sheet.links.new(group_016_4.outputs[0], boolean_math_003_8.inputs[1])
			#capture_attribute_7.Value -> reroute_20.Input
			_mn_topo_calc_sheet.links.new(capture_attribute_7.outputs[1], reroute_20.inputs[0])
			#boolean_math_003_8.Boolean -> boolean_math_004_5.Boolean
			_mn_topo_calc_sheet.links.new(boolean_math_003_8.outputs[0], boolean_math_004_5.inputs[0])
			#group_017_4.Boolean -> boolean_math_004_5.Boolean
			_mn_topo_calc_sheet.links.new(group_017_4.outputs[0], boolean_math_004_5.inputs[1])
			#boolean_math_004_5.Boolean -> group_003_12.Boolean
			_mn_topo_calc_sheet.links.new(boolean_math_004_5.outputs[0], group_003_12.inputs[0])
			#store_named_attribute_002_2.Geometry -> store_named_attribute_3.Geometry
			_mn_topo_calc_sheet.links.new(store_named_attribute_002_2.outputs[0], store_named_attribute_3.inputs[0])
			#group_008_6.j -> store_named_attribute_3.Value
			_mn_topo_calc_sheet.links.new(group_008_6.outputs[1], store_named_attribute_3.inputs[3])
			#group_008_6.Boolean -> store_named_attribute_3.Selection
			_mn_topo_calc_sheet.links.new(group_008_6.outputs[0], store_named_attribute_3.inputs[1])
			#store_named_attribute_3.Geometry -> store_named_attribute_001_2.Geometry
			_mn_topo_calc_sheet.links.new(store_named_attribute_3.outputs[0], store_named_attribute_001_2.inputs[0])
			#group_009_6.Boolean -> store_named_attribute_001_2.Selection
			_mn_topo_calc_sheet.links.new(group_009_6.outputs[0], store_named_attribute_001_2.inputs[1])
			#group_009_6.j -> store_named_attribute_001_2.Value
			_mn_topo_calc_sheet.links.new(group_009_6.outputs[1], store_named_attribute_001_2.inputs[3])
			#capture_attribute_7.Geometry -> store_named_attribute_002_2.Geometry
			_mn_topo_calc_sheet.links.new(capture_attribute_7.outputs[0], store_named_attribute_002_2.inputs[0])
			#store_named_attribute_001_2.Geometry -> store_named_attribute_003_1.Geometry
			_mn_topo_calc_sheet.links.new(store_named_attribute_001_2.outputs[0], store_named_attribute_003_1.inputs[0])
			#group_010_8.Boolean -> store_named_attribute_003_1.Selection
			_mn_topo_calc_sheet.links.new(group_010_8.outputs[0], store_named_attribute_003_1.inputs[1])
			#group_010_8.j -> store_named_attribute_003_1.Value
			_mn_topo_calc_sheet.links.new(group_010_8.outputs[1], store_named_attribute_003_1.inputs[3])
			#store_named_attribute_003_1.Geometry -> store_named_attribute_004_1.Geometry
			_mn_topo_calc_sheet.links.new(store_named_attribute_003_1.outputs[0], store_named_attribute_004_1.inputs[0])
			#group_015_1.Boolean -> store_named_attribute_004_1.Selection
			_mn_topo_calc_sheet.links.new(group_015_1.outputs[0], store_named_attribute_004_1.inputs[1])
			#group_015_1.j -> store_named_attribute_004_1.Value
			_mn_topo_calc_sheet.links.new(group_015_1.outputs[1], store_named_attribute_004_1.inputs[3])
			#store_named_attribute_004_1.Geometry -> store_named_attribute_005_1.Geometry
			_mn_topo_calc_sheet.links.new(store_named_attribute_004_1.outputs[0], store_named_attribute_005_1.inputs[0])
			#group_016_4.Boolean -> store_named_attribute_005_1.Selection
			_mn_topo_calc_sheet.links.new(group_016_4.outputs[0], store_named_attribute_005_1.inputs[1])
			#group_016_4.j -> store_named_attribute_005_1.Value
			_mn_topo_calc_sheet.links.new(group_016_4.outputs[1], store_named_attribute_005_1.inputs[3])
			#store_named_attribute_005_1.Geometry -> store_named_attribute_006.Geometry
			_mn_topo_calc_sheet.links.new(store_named_attribute_005_1.outputs[0], store_named_attribute_006.inputs[0])
			#group_017_4.Boolean -> store_named_attribute_006.Selection
			_mn_topo_calc_sheet.links.new(group_017_4.outputs[0], store_named_attribute_006.inputs[1])
			#group_017_4.j -> store_named_attribute_006.Value
			_mn_topo_calc_sheet.links.new(group_017_4.outputs[1], store_named_attribute_006.inputs[3])
			#group_001_18.Value -> math_26.Value
			_mn_topo_calc_sheet.links.new(group_001_18.outputs[0], math_26.inputs[0])
			#reroute_20.Output -> group_001_18.Value
			_mn_topo_calc_sheet.links.new(reroute_20.outputs[0], group_001_18.inputs[1])
			#math_26.Value -> group_016_4.j
			_mn_topo_calc_sheet.links.new(math_26.outputs[0], group_016_4.inputs[1])
			#group_002_18.Value -> math_001_9.Value
			_mn_topo_calc_sheet.links.new(group_002_18.outputs[0], math_001_9.inputs[0])
			#reroute_20.Output -> group_002_18.Value
			_mn_topo_calc_sheet.links.new(reroute_20.outputs[0], group_002_18.inputs[1])
			#math_001_9.Value -> group_017_4.j
			_mn_topo_calc_sheet.links.new(math_001_9.outputs[0], group_017_4.inputs[1])
			#group_013_2.Closest Index -> capture_attribute_7.Closest Index
			_mn_topo_calc_sheet.links.new(group_013_2.outputs[0], capture_attribute_7.inputs[2])
			#group_011_7.Closest Index -> capture_attribute_7.Closest Index.001
			_mn_topo_calc_sheet.links.new(group_011_7.outputs[0], capture_attribute_7.inputs[3])
			#group_014_3.Closest Index -> capture_attribute_7.Closest Index.002
			_mn_topo_calc_sheet.links.new(group_014_3.outputs[0], capture_attribute_7.inputs[4])
			return _mn_topo_calc_sheet

		_mn_topo_calc_sheet = _mn_topo_calc_sheet_node_group()

		#initialize topology_dssp node group
		def topology_dssp_node_group():
			topology_dssp = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Topology DSSP")

			topology_dssp.color_tag = 'GEOMETRY'
			topology_dssp.description = "Calculate the secondary structure attributes for the protein chains, based on the 1983 Kabsch algorithm"


			#topology_dssp interface
			#Socket Atoms
			atoms_socket_7 = topology_dssp.interface.new_socket(name = "Atoms", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			atoms_socket_7.attribute_domain = 'POINT'

			#Socket Atoms
			atoms_socket_8 = topology_dssp.interface.new_socket(name = "Atoms", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			atoms_socket_8.attribute_domain = 'POINT'

			#Socket Selection
			selection_socket_11 = topology_dssp.interface.new_socket(name = "Selection", in_out='INPUT', socket_type = 'NodeSocketBool')
			selection_socket_11.attribute_domain = 'POINT'
			selection_socket_11.hide_value = True


			#initialize topology_dssp nodes
			#node Group Output
			group_output_82 = topology_dssp.nodes.new("NodeGroupOutput")
			group_output_82.name = "Group Output"
			group_output_82.is_active_output = True

			#node Group Input
			group_input_81 = topology_dssp.nodes.new("NodeGroupInput")
			group_input_81.name = "Group Input"

			#node Group.002
			group_002_19 = topology_dssp.nodes.new("GeometryNodeGroup")
			group_002_19.name = "Group.002"
			group_002_19.node_tree = _mn_topo_calc_helix

			#node Store Named Attribute.003
			store_named_attribute_003_2 = topology_dssp.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_003_2.label = "store helix"
			store_named_attribute_003_2.name = "Store Named Attribute.003"
			store_named_attribute_003_2.data_type = 'INT'
			store_named_attribute_003_2.domain = 'POINT'
			#Name
			store_named_attribute_003_2.inputs[2].default_value = "sec_struct"

			#node Sample Index
			sample_index_2 = topology_dssp.nodes.new("GeometryNodeSampleIndex")
			sample_index_2.name = "Sample Index"
			sample_index_2.clamp = False
			sample_index_2.data_type = 'BOOLEAN'
			sample_index_2.domain = 'POINT'

			#node Group.005
			group_005_8 = topology_dssp.nodes.new("GeometryNodeGroup")
			group_005_8.name = "Group.005"
			group_005_8.node_tree = _mn_topo_calc_sheet

			#node Sample Index.001
			sample_index_001_2 = topology_dssp.nodes.new("GeometryNodeSampleIndex")
			sample_index_001_2.name = "Sample Index.001"
			sample_index_001_2.clamp = False
			sample_index_001_2.data_type = 'BOOLEAN'
			sample_index_001_2.domain = 'POINT'

			#node Sample Index.002
			sample_index_002_1 = topology_dssp.nodes.new("GeometryNodeSampleIndex")
			sample_index_002_1.name = "Sample Index.002"
			sample_index_002_1.hide = True
			sample_index_002_1.clamp = False
			sample_index_002_1.data_type = 'INT'
			sample_index_002_1.domain = 'POINT'

			#node Index
			index_6 = topology_dssp.nodes.new("GeometryNodeInputIndex")
			index_6.name = "Index"

			#node Switch
			switch_17 = topology_dssp.nodes.new("GeometryNodeSwitch")
			switch_17.name = "Switch"
			switch_17.input_type = 'INT'
			#False
			switch_17.inputs[1].default_value = 3
			#True
			switch_17.inputs[2].default_value = 2

			#node Switch.001
			switch_001_8 = topology_dssp.nodes.new("GeometryNodeSwitch")
			switch_001_8.name = "Switch.001"
			switch_001_8.input_type = 'INT'
			#True
			switch_001_8.inputs[2].default_value = 1

			#node Reroute.003
			reroute_003_10 = topology_dssp.nodes.new("NodeReroute")
			reroute_003_10.name = "Reroute.003"
			#node Sample Index.003
			sample_index_003 = topology_dssp.nodes.new("GeometryNodeSampleIndex")
			sample_index_003.name = "Sample Index.003"
			sample_index_003.clamp = False
			sample_index_003.data_type = 'INT'
			sample_index_003.domain = 'POINT'

			#node Index.002
			index_002_1 = topology_dssp.nodes.new("GeometryNodeInputIndex")
			index_002_1.name = "Index.002"

			#node MN_topo_compute_backbone.001
			mn_topo_compute_backbone_001 = topology_dssp.nodes.new("GeometryNodeGroup")
			mn_topo_compute_backbone_001.label = "Topology Compute Backbone"
			mn_topo_compute_backbone_001.name = "MN_topo_compute_backbone.001"
			mn_topo_compute_backbone_001.node_tree = _mn_topo_assign_backbone

			#node Frame
			frame_14 = topology_dssp.nodes.new("NodeFrame")
			frame_14.label = "Compute Helix"
			frame_14.name = "Frame"
			frame_14.label_size = 20
			frame_14.shrink = True

			#node Frame.001
			frame_001_9 = topology_dssp.nodes.new("NodeFrame")
			frame_001_9.label = "Compute Sheet"
			frame_001_9.name = "Frame.001"
			frame_001_9.label_size = 20
			frame_001_9.shrink = True



			#Set parents
			group_002_19.parent = frame_14
			sample_index_2.parent = frame_14
			group_005_8.parent = frame_001_9
			sample_index_001_2.parent = frame_001_9

			#Set locations
			group_output_82.location = (676.5311889648438, 311.6835632324219)
			group_input_81.location = (-1820.0, 380.0)
			group_002_19.location = (-1140.0, -80.0)
			store_named_attribute_003_2.location = (-520.0, 480.0)
			sample_index_2.location = (-740.0, -60.0)
			group_005_8.location = (-1140.0, -380.0)
			sample_index_001_2.location = (-740.0, -380.0)
			sample_index_002_1.location = (-720.0, 120.0)
			index_6.location = (-920.0, 120.0)
			switch_17.location = (-520.0, -120.0)
			switch_001_8.location = (-520.0, 40.0)
			reroute_003_10.location = (-1300.0, -120.0)
			sample_index_003.location = (-520.0, 280.0)
			index_002_1.location = (-940.0, -200.0)
			mn_topo_compute_backbone_001.location = (-1560.0, 300.0)
			frame_14.location = (-10.0, 80.0)
			frame_001_9.location = (-10.0, 80.0)

			#Set dimensions
			group_output_82.width, group_output_82.height = 140.0, 100.0
			group_input_81.width, group_input_81.height = 140.0, 100.0
			group_002_19.width, group_002_19.height = 238.041015625, 100.0
			store_named_attribute_003_2.width, store_named_attribute_003_2.height = 140.0, 100.0
			sample_index_2.width, sample_index_2.height = 140.0, 100.0
			group_005_8.width, group_005_8.height = 210.28070068359375, 100.0
			sample_index_001_2.width, sample_index_001_2.height = 140.0, 100.0
			sample_index_002_1.width, sample_index_002_1.height = 140.0, 100.0
			index_6.width, index_6.height = 140.0, 100.0
			switch_17.width, switch_17.height = 140.0, 100.0
			switch_001_8.width, switch_001_8.height = 140.0, 100.0
			reroute_003_10.width, reroute_003_10.height = 16.0, 100.0
			sample_index_003.width, sample_index_003.height = 140.0, 100.0
			index_002_1.width, index_002_1.height = 140.0, 100.0
			mn_topo_compute_backbone_001.width, mn_topo_compute_backbone_001.height = 207.010986328125, 100.0
			frame_14.width, frame_14.height = 600.0, 264.0
			frame_001_9.width, frame_001_9.height = 600.0, 264.0

			#initialize topology_dssp links
			#group_input_81.Atoms -> store_named_attribute_003_2.Geometry
			topology_dssp.links.new(group_input_81.outputs[0], store_named_attribute_003_2.inputs[0])
			#reroute_003_10.Output -> sample_index_2.Geometry
			topology_dssp.links.new(reroute_003_10.outputs[0], sample_index_2.inputs[0])
			#store_named_attribute_003_2.Geometry -> group_output_82.Atoms
			topology_dssp.links.new(store_named_attribute_003_2.outputs[0], group_output_82.inputs[0])
			#reroute_003_10.Output -> group_005_8.Geometry
			topology_dssp.links.new(reroute_003_10.outputs[0], group_005_8.inputs[0])
			#mn_topo_compute_backbone_001.Atoms -> sample_index_002_1.Geometry
			topology_dssp.links.new(mn_topo_compute_backbone_001.outputs[0], sample_index_002_1.inputs[0])
			#index_6.Index -> sample_index_002_1.Index
			topology_dssp.links.new(index_6.outputs[0], sample_index_002_1.inputs[2])
			#group_005_8.Geometry -> sample_index_001_2.Geometry
			topology_dssp.links.new(group_005_8.outputs[0], sample_index_001_2.inputs[0])
			#sample_index_001_2.Value -> switch_17.Switch
			topology_dssp.links.new(sample_index_001_2.outputs[0], switch_17.inputs[0])
			#switch_17.Output -> switch_001_8.False
			topology_dssp.links.new(switch_17.outputs[0], switch_001_8.inputs[1])
			#sample_index_2.Value -> switch_001_8.Switch
			topology_dssp.links.new(sample_index_2.outputs[0], switch_001_8.inputs[0])
			#mn_topo_compute_backbone_001.CA Atoms -> reroute_003_10.Input
			topology_dssp.links.new(mn_topo_compute_backbone_001.outputs[2], reroute_003_10.inputs[0])
			#group_002_19.Is Helix -> sample_index_2.Value
			topology_dssp.links.new(group_002_19.outputs[0], sample_index_2.inputs[1])
			#group_005_8.Attribute -> sample_index_001_2.Value
			topology_dssp.links.new(group_005_8.outputs[1], sample_index_001_2.inputs[1])
			#mn_topo_compute_backbone_001.Unique Group ID -> sample_index_002_1.Value
			topology_dssp.links.new(mn_topo_compute_backbone_001.outputs[1], sample_index_002_1.inputs[1])
			#sample_index_002_1.Value -> sample_index_003.Index
			topology_dssp.links.new(sample_index_002_1.outputs[0], sample_index_003.inputs[2])
			#mn_topo_compute_backbone_001.CA Atoms -> sample_index_003.Geometry
			topology_dssp.links.new(mn_topo_compute_backbone_001.outputs[2], sample_index_003.inputs[0])
			#switch_001_8.Output -> sample_index_003.Value
			topology_dssp.links.new(switch_001_8.outputs[0], sample_index_003.inputs[1])
			#sample_index_003.Value -> store_named_attribute_003_2.Value
			topology_dssp.links.new(sample_index_003.outputs[0], store_named_attribute_003_2.inputs[3])
			#index_002_1.Index -> sample_index_2.Index
			topology_dssp.links.new(index_002_1.outputs[0], sample_index_2.inputs[2])
			#group_input_81.Selection -> store_named_attribute_003_2.Selection
			topology_dssp.links.new(group_input_81.outputs[1], store_named_attribute_003_2.inputs[1])
			#group_input_81.Atoms -> mn_topo_compute_backbone_001.Atoms
			topology_dssp.links.new(group_input_81.outputs[0], mn_topo_compute_backbone_001.inputs[0])
			#index_002_1.Index -> sample_index_001_2.Index
			topology_dssp.links.new(index_002_1.outputs[0], sample_index_001_2.inputs[2])
			return topology_dssp

		topology_dssp = topology_dssp_node_group()

		#initialize _mn_constants_atom_name_nucleic node group
		def _mn_constants_atom_name_nucleic_node_group():
			_mn_constants_atom_name_nucleic = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".MN_constants_atom_name_nucleic")

			_mn_constants_atom_name_nucleic.color_tag = 'NONE'
			_mn_constants_atom_name_nucleic.description = ""


			#_mn_constants_atom_name_nucleic interface
			#Socket Backbone Lower
			backbone_lower_socket_1 = _mn_constants_atom_name_nucleic.interface.new_socket(name = "Backbone Lower", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			backbone_lower_socket_1.subtype = 'NONE'
			backbone_lower_socket_1.default_value = 0
			backbone_lower_socket_1.min_value = -2147483648
			backbone_lower_socket_1.max_value = 2147483647
			backbone_lower_socket_1.attribute_domain = 'POINT'

			#Socket Backbone Upper
			backbone_upper_socket_1 = _mn_constants_atom_name_nucleic.interface.new_socket(name = "Backbone Upper", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			backbone_upper_socket_1.subtype = 'NONE'
			backbone_upper_socket_1.default_value = 0
			backbone_upper_socket_1.min_value = -2147483648
			backbone_upper_socket_1.max_value = 2147483647
			backbone_upper_socket_1.attribute_domain = 'POINT'

			#Socket Side Chain Lower
			side_chain_lower_socket_1 = _mn_constants_atom_name_nucleic.interface.new_socket(name = "Side Chain Lower", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			side_chain_lower_socket_1.subtype = 'NONE'
			side_chain_lower_socket_1.default_value = 0
			side_chain_lower_socket_1.min_value = -2147483648
			side_chain_lower_socket_1.max_value = 2147483647
			side_chain_lower_socket_1.attribute_domain = 'POINT'

			#Socket Side Chain Upper
			side_chain_upper_socket_1 = _mn_constants_atom_name_nucleic.interface.new_socket(name = "Side Chain Upper", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			side_chain_upper_socket_1.subtype = 'NONE'
			side_chain_upper_socket_1.default_value = 0
			side_chain_upper_socket_1.min_value = -2147483648
			side_chain_upper_socket_1.max_value = 2147483647
			side_chain_upper_socket_1.attribute_domain = 'POINT'

			#Socket Side Chain Joint Carbon
			side_chain_joint_carbon_socket = _mn_constants_atom_name_nucleic.interface.new_socket(name = "Side Chain Joint Carbon", in_out='OUTPUT', socket_type = 'NodeSocketInt')
			side_chain_joint_carbon_socket.subtype = 'NONE'
			side_chain_joint_carbon_socket.default_value = 0
			side_chain_joint_carbon_socket.min_value = -2147483648
			side_chain_joint_carbon_socket.max_value = 2147483647
			side_chain_joint_carbon_socket.attribute_domain = 'POINT'


			#initialize _mn_constants_atom_name_nucleic nodes
			#node Group Output
			group_output_83 = _mn_constants_atom_name_nucleic.nodes.new("NodeGroupOutput")
			group_output_83.name = "Group Output"
			group_output_83.is_active_output = True

			#node Group Input
			group_input_82 = _mn_constants_atom_name_nucleic.nodes.new("NodeGroupInput")
			group_input_82.name = "Group Input"

			#node Integer
			integer_3 = _mn_constants_atom_name_nucleic.nodes.new("FunctionNodeInputInt")
			integer_3.name = "Integer"
			integer_3.integer = 61

			#node Integer.002
			integer_002_1 = _mn_constants_atom_name_nucleic.nodes.new("FunctionNodeInputInt")
			integer_002_1.name = "Integer.002"
			integer_002_1.integer = 50

			#node Integer.003
			integer_003_1 = _mn_constants_atom_name_nucleic.nodes.new("FunctionNodeInputInt")
			integer_003_1.name = "Integer.003"
			integer_003_1.integer = 61

			#node Integer.001
			integer_001_1 = _mn_constants_atom_name_nucleic.nodes.new("FunctionNodeInputInt")
			integer_001_1.name = "Integer.001"
			integer_001_1.integer = 77

			#node Integer.004
			integer_004_1 = _mn_constants_atom_name_nucleic.nodes.new("FunctionNodeInputInt")
			integer_004_1.name = "Integer.004"
			integer_004_1.integer = 54




			#Set locations
			group_output_83.location = (190.0, 0.0)
			group_input_82.location = (-200.0, 0.0)
			integer_3.location = (0.0, -100.0)
			integer_002_1.location = (0.0, 100.0)
			integer_003_1.location = (0.0, 0.0)
			integer_001_1.location = (0.0, -200.0)
			integer_004_1.location = (0.0, -300.0)

			#Set dimensions
			group_output_83.width, group_output_83.height = 140.0, 100.0
			group_input_82.width, group_input_82.height = 140.0, 100.0
			integer_3.width, integer_3.height = 140.0, 100.0
			integer_002_1.width, integer_002_1.height = 140.0, 100.0
			integer_003_1.width, integer_003_1.height = 140.0, 100.0
			integer_001_1.width, integer_001_1.height = 140.0, 100.0
			integer_004_1.width, integer_004_1.height = 140.0, 100.0

			#initialize _mn_constants_atom_name_nucleic links
			#integer_3.Integer -> group_output_83.Side Chain Lower
			_mn_constants_atom_name_nucleic.links.new(integer_3.outputs[0], group_output_83.inputs[2])
			#integer_001_1.Integer -> group_output_83.Side Chain Upper
			_mn_constants_atom_name_nucleic.links.new(integer_001_1.outputs[0], group_output_83.inputs[3])
			#integer_002_1.Integer -> group_output_83.Backbone Lower
			_mn_constants_atom_name_nucleic.links.new(integer_002_1.outputs[0], group_output_83.inputs[0])
			#integer_003_1.Integer -> group_output_83.Backbone Upper
			_mn_constants_atom_name_nucleic.links.new(integer_003_1.outputs[0], group_output_83.inputs[1])
			#integer_004_1.Integer -> group_output_83.Side Chain Joint Carbon
			_mn_constants_atom_name_nucleic.links.new(integer_004_1.outputs[0], group_output_83.inputs[4])
			return _mn_constants_atom_name_nucleic

		_mn_constants_atom_name_nucleic = _mn_constants_atom_name_nucleic_node_group()

		#initialize _mn_select_nucleic node group
		def _mn_select_nucleic_node_group():
			_mn_select_nucleic = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".MN_select_nucleic")

			_mn_select_nucleic.color_tag = 'NONE'
			_mn_select_nucleic.description = ""


			#_mn_select_nucleic interface
			#Socket Is Backbone
			is_backbone_socket_1 = _mn_select_nucleic.interface.new_socket(name = "Is Backbone", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			is_backbone_socket_1.attribute_domain = 'POINT'
			is_backbone_socket_1.description = "True for atoms that are part of the sugar-phosphate backbone for the nucleotides"

			#Socket Is Side Chain
			is_side_chain_socket_1 = _mn_select_nucleic.interface.new_socket(name = "Is Side Chain", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			is_side_chain_socket_1.attribute_domain = 'POINT'
			is_side_chain_socket_1.description = "True for atoms that are part of the bases for nucleotides."

			#Socket Is Nucleic
			is_nucleic_socket = _mn_select_nucleic.interface.new_socket(name = "Is Nucleic", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			is_nucleic_socket.attribute_domain = 'POINT'
			is_nucleic_socket.description = "True if the atoms are part of a nucleic acid"


			#initialize _mn_select_nucleic nodes
			#node Group Input
			group_input_83 = _mn_select_nucleic.nodes.new("NodeGroupInput")
			group_input_83.name = "Group Input"

			#node Compare
			compare_15 = _mn_select_nucleic.nodes.new("FunctionNodeCompare")
			compare_15.name = "Compare"
			compare_15.data_type = 'INT'
			compare_15.mode = 'ELEMENT'
			compare_15.operation = 'GREATER_EQUAL'

			#node Compare.001
			compare_001_10 = _mn_select_nucleic.nodes.new("FunctionNodeCompare")
			compare_001_10.name = "Compare.001"
			compare_001_10.data_type = 'INT'
			compare_001_10.mode = 'ELEMENT'
			compare_001_10.operation = 'LESS_EQUAL'

			#node Boolean Math.001
			boolean_math_001_13 = _mn_select_nucleic.nodes.new("FunctionNodeBooleanMath")
			boolean_math_001_13.name = "Boolean Math.001"
			boolean_math_001_13.operation = 'AND'

			#node Group Output
			group_output_84 = _mn_select_nucleic.nodes.new("NodeGroupOutput")
			group_output_84.name = "Group Output"
			group_output_84.is_active_output = True

			#node Compare.002
			compare_002_7 = _mn_select_nucleic.nodes.new("FunctionNodeCompare")
			compare_002_7.name = "Compare.002"
			compare_002_7.data_type = 'INT'
			compare_002_7.mode = 'ELEMENT'
			compare_002_7.operation = 'GREATER_EQUAL'

			#node Compare.003
			compare_003_3 = _mn_select_nucleic.nodes.new("FunctionNodeCompare")
			compare_003_3.name = "Compare.003"
			compare_003_3.data_type = 'INT'
			compare_003_3.mode = 'ELEMENT'
			compare_003_3.operation = 'LESS_EQUAL'

			#node Boolean Math.002
			boolean_math_002_8 = _mn_select_nucleic.nodes.new("FunctionNodeBooleanMath")
			boolean_math_002_8.name = "Boolean Math.002"
			boolean_math_002_8.operation = 'AND'

			#node Compare.004
			compare_004_1 = _mn_select_nucleic.nodes.new("FunctionNodeCompare")
			compare_004_1.name = "Compare.004"
			compare_004_1.data_type = 'INT'
			compare_004_1.mode = 'ELEMENT'
			compare_004_1.operation = 'GREATER_EQUAL'

			#node Compare.005
			compare_005_1 = _mn_select_nucleic.nodes.new("FunctionNodeCompare")
			compare_005_1.name = "Compare.005"
			compare_005_1.data_type = 'INT'
			compare_005_1.mode = 'ELEMENT'
			compare_005_1.operation = 'LESS_EQUAL'

			#node Boolean Math.003
			boolean_math_003_9 = _mn_select_nucleic.nodes.new("FunctionNodeBooleanMath")
			boolean_math_003_9.name = "Boolean Math.003"
			boolean_math_003_9.operation = 'AND'

			#node Named Attribute
			named_attribute_8 = _mn_select_nucleic.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_8.name = "Named Attribute"
			named_attribute_8.data_type = 'INT'
			#Name
			named_attribute_8.inputs[0].default_value = "atom_name"

			#node Group
			group_29 = _mn_select_nucleic.nodes.new("GeometryNodeGroup")
			group_29.name = "Group"
			group_29.node_tree = _mn_constants_atom_name_nucleic




			#Set locations
			group_input_83.location = (-460.0, 0.0)
			compare_15.location = (80.0, 80.0)
			compare_001_10.location = (80.0, -80.0)
			boolean_math_001_13.location = (260.0, 80.0)
			group_output_84.location = (580.0, 60.0)
			compare_002_7.location = (80.0, -260.0)
			compare_003_3.location = (80.0, -420.0)
			boolean_math_002_8.location = (260.0, -260.0)
			compare_004_1.location = (80.0, -580.0)
			compare_005_1.location = (80.0, -740.0)
			boolean_math_003_9.location = (260.0, -580.0)
			named_attribute_8.location = (-260.0, -280.0)
			group_29.location = (-480.0, -100.0)

			#Set dimensions
			group_input_83.width, group_input_83.height = 140.0, 100.0
			compare_15.width, compare_15.height = 140.0, 100.0
			compare_001_10.width, compare_001_10.height = 140.0, 100.0
			boolean_math_001_13.width, boolean_math_001_13.height = 140.0, 100.0
			group_output_84.width, group_output_84.height = 140.0, 100.0
			compare_002_7.width, compare_002_7.height = 140.0, 100.0
			compare_003_3.width, compare_003_3.height = 140.0, 100.0
			boolean_math_002_8.width, boolean_math_002_8.height = 140.0, 100.0
			compare_004_1.width, compare_004_1.height = 140.0, 100.0
			compare_005_1.width, compare_005_1.height = 140.0, 100.0
			boolean_math_003_9.width, boolean_math_003_9.height = 140.0, 100.0
			named_attribute_8.width, named_attribute_8.height = 140.0, 100.0
			group_29.width, group_29.height = 365.8858337402344, 100.0

			#initialize _mn_select_nucleic links
			#compare_001_10.Result -> boolean_math_001_13.Boolean
			_mn_select_nucleic.links.new(compare_001_10.outputs[0], boolean_math_001_13.inputs[1])
			#named_attribute_8.Attribute -> compare_15.A
			_mn_select_nucleic.links.new(named_attribute_8.outputs[0], compare_15.inputs[2])
			#compare_15.Result -> boolean_math_001_13.Boolean
			_mn_select_nucleic.links.new(compare_15.outputs[0], boolean_math_001_13.inputs[0])
			#named_attribute_8.Attribute -> compare_001_10.A
			_mn_select_nucleic.links.new(named_attribute_8.outputs[0], compare_001_10.inputs[2])
			#boolean_math_001_13.Boolean -> group_output_84.Is Backbone
			_mn_select_nucleic.links.new(boolean_math_001_13.outputs[0], group_output_84.inputs[0])
			#group_29.Backbone Lower -> compare_15.B
			_mn_select_nucleic.links.new(group_29.outputs[0], compare_15.inputs[3])
			#group_29.Backbone Upper -> compare_001_10.B
			_mn_select_nucleic.links.new(group_29.outputs[1], compare_001_10.inputs[3])
			#compare_003_3.Result -> boolean_math_002_8.Boolean
			_mn_select_nucleic.links.new(compare_003_3.outputs[0], boolean_math_002_8.inputs[1])
			#compare_002_7.Result -> boolean_math_002_8.Boolean
			_mn_select_nucleic.links.new(compare_002_7.outputs[0], boolean_math_002_8.inputs[0])
			#group_29.Side Chain Lower -> compare_002_7.B
			_mn_select_nucleic.links.new(group_29.outputs[2], compare_002_7.inputs[3])
			#group_29.Side Chain Upper -> compare_003_3.B
			_mn_select_nucleic.links.new(group_29.outputs[3], compare_003_3.inputs[3])
			#boolean_math_002_8.Boolean -> group_output_84.Is Side Chain
			_mn_select_nucleic.links.new(boolean_math_002_8.outputs[0], group_output_84.inputs[1])
			#named_attribute_8.Attribute -> compare_002_7.A
			_mn_select_nucleic.links.new(named_attribute_8.outputs[0], compare_002_7.inputs[2])
			#named_attribute_8.Attribute -> compare_003_3.A
			_mn_select_nucleic.links.new(named_attribute_8.outputs[0], compare_003_3.inputs[2])
			#compare_005_1.Result -> boolean_math_003_9.Boolean
			_mn_select_nucleic.links.new(compare_005_1.outputs[0], boolean_math_003_9.inputs[1])
			#compare_004_1.Result -> boolean_math_003_9.Boolean
			_mn_select_nucleic.links.new(compare_004_1.outputs[0], boolean_math_003_9.inputs[0])
			#group_29.Backbone Lower -> compare_004_1.B
			_mn_select_nucleic.links.new(group_29.outputs[0], compare_004_1.inputs[3])
			#named_attribute_8.Attribute -> compare_004_1.A
			_mn_select_nucleic.links.new(named_attribute_8.outputs[0], compare_004_1.inputs[2])
			#group_29.Side Chain Upper -> compare_005_1.B
			_mn_select_nucleic.links.new(group_29.outputs[3], compare_005_1.inputs[3])
			#named_attribute_8.Attribute -> compare_005_1.A
			_mn_select_nucleic.links.new(named_attribute_8.outputs[0], compare_005_1.inputs[2])
			#boolean_math_003_9.Boolean -> group_output_84.Is Nucleic
			_mn_select_nucleic.links.new(boolean_math_003_9.outputs[0], group_output_84.inputs[2])
			return _mn_select_nucleic

		_mn_select_nucleic = _mn_select_nucleic_node_group()

		#initialize is_nucleic node group
		def is_nucleic_node_group():
			is_nucleic = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Is Nucleic")

			is_nucleic.color_tag = 'INPUT'
			is_nucleic.description = ""


			#is_nucleic interface
			#Socket Selection
			selection_socket_12 = is_nucleic.interface.new_socket(name = "Selection", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			selection_socket_12.attribute_domain = 'POINT'
			selection_socket_12.description = "True if atoms are part of a nucleic acid"

			#Socket Inverted
			inverted_socket_7 = is_nucleic.interface.new_socket(name = "Inverted", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			inverted_socket_7.attribute_domain = 'POINT'

			#Socket And
			and_socket_8 = is_nucleic.interface.new_socket(name = "And", in_out='INPUT', socket_type = 'NodeSocketBool')
			and_socket_8.attribute_domain = 'POINT'
			and_socket_8.hide_value = True

			#Socket Or
			or_socket_7 = is_nucleic.interface.new_socket(name = "Or", in_out='INPUT', socket_type = 'NodeSocketBool')
			or_socket_7.attribute_domain = 'POINT'
			or_socket_7.hide_value = True


			#initialize is_nucleic nodes
			#node Group Input
			group_input_84 = is_nucleic.nodes.new("NodeGroupInput")
			group_input_84.name = "Group Input"

			#node Group Output
			group_output_85 = is_nucleic.nodes.new("NodeGroupOutput")
			group_output_85.name = "Group Output"
			group_output_85.is_active_output = True

			#node Group
			group_30 = is_nucleic.nodes.new("GeometryNodeGroup")
			group_30.name = "Group"
			group_30.node_tree = _mn_select_nucleic

			#node Group.001
			group_001_19 = is_nucleic.nodes.new("GeometryNodeGroup")
			group_001_19.name = "Group.001"
			group_001_19.node_tree = fallback_boolean
			#Socket_2
			group_001_19.inputs[0].default_value = "is_nucleic"

			#node Group.002
			group_002_20 = is_nucleic.nodes.new("GeometryNodeGroup")
			group_002_20.name = "Group.002"
			group_002_20.node_tree = boolean_andor




			#Set locations
			group_input_84.location = (-260.0, -20.0)
			group_output_85.location = (160.0, -20.0)
			group_30.location = (-620.0, -160.0)
			group_001_19.location = (-340.0, -160.0)
			group_002_20.location = (-40.0, -20.0)

			#Set dimensions
			group_input_84.width, group_input_84.height = 140.0, 100.0
			group_output_85.width, group_output_85.height = 140.0, 100.0
			group_30.width, group_30.height = 247.90924072265625, 100.0
			group_001_19.width, group_001_19.height = 232.0133056640625, 100.0
			group_002_20.width, group_002_20.height = 140.0, 100.0

			#initialize is_nucleic links
			#group_30.Is Nucleic -> group_001_19.Fallback
			is_nucleic.links.new(group_30.outputs[2], group_001_19.inputs[1])
			#group_input_84.And -> group_002_20.And
			is_nucleic.links.new(group_input_84.outputs[0], group_002_20.inputs[0])
			#group_001_19.Boolean -> group_002_20.Boolean
			is_nucleic.links.new(group_001_19.outputs[0], group_002_20.inputs[2])
			#group_input_84.Or -> group_002_20.Or
			is_nucleic.links.new(group_input_84.outputs[1], group_002_20.inputs[1])
			#group_002_20.Boolean -> group_output_85.Selection
			is_nucleic.links.new(group_002_20.outputs[0], group_output_85.inputs[0])
			#group_002_20.Inverted -> group_output_85.Inverted
			is_nucleic.links.new(group_002_20.outputs[1], group_output_85.inputs[1])
			return is_nucleic

		is_nucleic = is_nucleic_node_group()

		#initialize separate_polymers node group
		def separate_polymers_node_group():
			separate_polymers = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Separate Polymers")

			separate_polymers.color_tag = 'GEOMETRY'
			separate_polymers.description = ""

			separate_polymers.is_modifier = True

			#separate_polymers interface
			#Socket Peptide
			peptide_socket = separate_polymers.interface.new_socket(name = "Peptide", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			peptide_socket.attribute_domain = 'POINT'

			#Socket Nucleic
			nucleic_socket = separate_polymers.interface.new_socket(name = "Nucleic", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			nucleic_socket.attribute_domain = 'POINT'

			#Socket Other
			other_socket = separate_polymers.interface.new_socket(name = "Other", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			other_socket.attribute_domain = 'POINT'

			#Socket Atoms
			atoms_socket_9 = separate_polymers.interface.new_socket(name = "Atoms", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			atoms_socket_9.attribute_domain = 'POINT'
			atoms_socket_9.description = "Atomic geometry that contains vertices and edges"


			#initialize separate_polymers nodes
			#node Group Input
			group_input_85 = separate_polymers.nodes.new("NodeGroupInput")
			group_input_85.name = "Group Input"

			#node Group Output
			group_output_86 = separate_polymers.nodes.new("NodeGroupOutput")
			group_output_86.name = "Group Output"
			group_output_86.is_active_output = True

			#node Separate Geometry
			separate_geometry_2 = separate_polymers.nodes.new("GeometryNodeSeparateGeometry")
			separate_geometry_2.name = "Separate Geometry"
			separate_geometry_2.domain = 'POINT'

			#node Separate Geometry.001
			separate_geometry_001 = separate_polymers.nodes.new("GeometryNodeSeparateGeometry")
			separate_geometry_001.name = "Separate Geometry.001"
			separate_geometry_001.domain = 'POINT'

			#node Group
			group_31 = separate_polymers.nodes.new("GeometryNodeGroup")
			group_31.name = "Group"
			group_31.node_tree = is_peptide
			#Socket_1
			group_31.inputs[0].default_value = True
			#Socket_3
			group_31.inputs[1].default_value = False

			#node Group.001
			group_001_20 = separate_polymers.nodes.new("GeometryNodeGroup")
			group_001_20.name = "Group.001"
			group_001_20.node_tree = is_nucleic
			#Socket_1
			group_001_20.inputs[0].default_value = True
			#Socket_3
			group_001_20.inputs[1].default_value = False




			#Set locations
			group_input_85.location = (-360.0, 220.0)
			group_output_86.location = (260.0, 80.0)
			separate_geometry_2.location = (-200.0, 100.0)
			separate_geometry_001.location = (0.0, -40.0)
			group_31.location = (-200.0, -60.0)
			group_001_20.location = (0.0, -200.0)

			#Set dimensions
			group_input_85.width, group_input_85.height = 140.0, 100.0
			group_output_86.width, group_output_86.height = 140.0, 100.0
			separate_geometry_2.width, separate_geometry_2.height = 140.0, 100.0
			separate_geometry_001.width, separate_geometry_001.height = 140.0, 100.0
			group_31.width, group_31.height = 140.0, 100.0
			group_001_20.width, group_001_20.height = 140.0, 100.0

			#initialize separate_polymers links
			#group_input_85.Atoms -> separate_geometry_2.Geometry
			separate_polymers.links.new(group_input_85.outputs[0], separate_geometry_2.inputs[0])
			#separate_geometry_2.Inverted -> separate_geometry_001.Geometry
			separate_polymers.links.new(separate_geometry_2.outputs[1], separate_geometry_001.inputs[0])
			#separate_geometry_2.Selection -> group_output_86.Peptide
			separate_polymers.links.new(separate_geometry_2.outputs[0], group_output_86.inputs[0])
			#separate_geometry_001.Selection -> group_output_86.Nucleic
			separate_polymers.links.new(separate_geometry_001.outputs[0], group_output_86.inputs[1])
			#separate_geometry_001.Inverted -> group_output_86.Other
			separate_polymers.links.new(separate_geometry_001.outputs[1], group_output_86.inputs[2])
			#group_31.Selection -> separate_geometry_2.Selection
			separate_polymers.links.new(group_31.outputs[0], separate_geometry_2.inputs[1])
			#group_001_20.Selection -> separate_geometry_001.Selection
			separate_polymers.links.new(group_001_20.outputs[0], separate_geometry_001.inputs[1])
			return separate_polymers

		separate_polymers = separate_polymers_node_group()

		#initialize select_nucleic_type node group
		def select_nucleic_type_node_group():
			select_nucleic_type = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Select Nucleic Type")

			select_nucleic_type.color_tag = 'INPUT'
			select_nucleic_type.description = ""


			#select_nucleic_type interface
			#Socket is_purine
			is_purine_socket = select_nucleic_type.interface.new_socket(name = "is_purine", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			is_purine_socket.attribute_domain = 'POINT'

			#Socket is_pyrimidine
			is_pyrimidine_socket = select_nucleic_type.interface.new_socket(name = "is_pyrimidine", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			is_pyrimidine_socket.attribute_domain = 'POINT'

			#Socket And
			and_socket_9 = select_nucleic_type.interface.new_socket(name = "And", in_out='INPUT', socket_type = 'NodeSocketBool')
			and_socket_9.attribute_domain = 'POINT'
			and_socket_9.hide_value = True

			#Socket Or
			or_socket_8 = select_nucleic_type.interface.new_socket(name = "Or", in_out='INPUT', socket_type = 'NodeSocketBool')
			or_socket_8.attribute_domain = 'POINT'
			or_socket_8.hide_value = True


			#initialize select_nucleic_type nodes
			#node Named Attribute.010
			named_attribute_010 = select_nucleic_type.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_010.name = "Named Attribute.010"
			named_attribute_010.data_type = 'INT'
			#Name
			named_attribute_010.inputs[0].default_value = "res_name"

			#node Group Output
			group_output_87 = select_nucleic_type.nodes.new("NodeGroupOutput")
			group_output_87.name = "Group Output"
			group_output_87.is_active_output = True

			#node Index Switch
			index_switch_3 = select_nucleic_type.nodes.new("GeometryNodeIndexSwitch")
			index_switch_3.name = "Index Switch"
			index_switch_3.data_type = 'BOOLEAN'
			index_switch_3.index_switch_items.clear()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.index_switch_items.new()
			index_switch_3.inputs[1].hide = True
			index_switch_3.inputs[2].hide = True
			index_switch_3.inputs[3].hide = True
			index_switch_3.inputs[4].hide = True
			index_switch_3.inputs[5].hide = True
			index_switch_3.inputs[6].hide = True
			index_switch_3.inputs[7].hide = True
			index_switch_3.inputs[8].hide = True
			index_switch_3.inputs[9].hide = True
			index_switch_3.inputs[10].hide = True
			index_switch_3.inputs[11].hide = True
			index_switch_3.inputs[12].hide = True
			index_switch_3.inputs[13].hide = True
			index_switch_3.inputs[14].hide = True
			index_switch_3.inputs[15].hide = True
			index_switch_3.inputs[16].hide = True
			index_switch_3.inputs[17].hide = True
			index_switch_3.inputs[18].hide = True
			index_switch_3.inputs[19].hide = True
			index_switch_3.inputs[20].hide = True
			index_switch_3.inputs[21].hide = True
			index_switch_3.inputs[22].hide = True
			index_switch_3.inputs[23].hide = True
			index_switch_3.inputs[24].hide = True
			index_switch_3.inputs[25].hide = True
			index_switch_3.inputs[26].hide = True
			index_switch_3.inputs[27].hide = True
			index_switch_3.inputs[28].hide = True
			index_switch_3.inputs[29].hide = True
			index_switch_3.inputs[30].hide = True
			index_switch_3.inputs[31].hide = True
			index_switch_3.inputs[33].hide = True
			index_switch_3.inputs[35].hide = True
			index_switch_3.inputs[36].hide = True
			index_switch_3.inputs[37].hide = True
			index_switch_3.inputs[38].hide = True
			index_switch_3.inputs[39].hide = True
			index_switch_3.inputs[40].hide = True
			index_switch_3.inputs[41].hide = True
			index_switch_3.inputs[43].hide = True
			index_switch_3.inputs[45].hide = True
			#Item_0
			index_switch_3.inputs[1].default_value = False
			#Item_1
			index_switch_3.inputs[2].default_value = False
			#Item_2
			index_switch_3.inputs[3].default_value = False
			#Item_3
			index_switch_3.inputs[4].default_value = False
			#Item_4
			index_switch_3.inputs[5].default_value = False
			#Item_5
			index_switch_3.inputs[6].default_value = False
			#Item_6
			index_switch_3.inputs[7].default_value = False
			#Item_7
			index_switch_3.inputs[8].default_value = False
			#Item_8
			index_switch_3.inputs[9].default_value = False
			#Item_9
			index_switch_3.inputs[10].default_value = False
			#Item_10
			index_switch_3.inputs[11].default_value = False
			#Item_11
			index_switch_3.inputs[12].default_value = False
			#Item_12
			index_switch_3.inputs[13].default_value = False
			#Item_13
			index_switch_3.inputs[14].default_value = False
			#Item_14
			index_switch_3.inputs[15].default_value = False
			#Item_15
			index_switch_3.inputs[16].default_value = False
			#Item_16
			index_switch_3.inputs[17].default_value = False
			#Item_17
			index_switch_3.inputs[18].default_value = False
			#Item_18
			index_switch_3.inputs[19].default_value = False
			#Item_19
			index_switch_3.inputs[20].default_value = False
			#Item_20
			index_switch_3.inputs[21].default_value = False
			#Item_21
			index_switch_3.inputs[22].default_value = False
			#Item_22
			index_switch_3.inputs[23].default_value = False
			#Item_23
			index_switch_3.inputs[24].default_value = False
			#Item_24
			index_switch_3.inputs[25].default_value = False
			#Item_25
			index_switch_3.inputs[26].default_value = False
			#Item_26
			index_switch_3.inputs[27].default_value = False
			#Item_27
			index_switch_3.inputs[28].default_value = False
			#Item_28
			index_switch_3.inputs[29].default_value = False
			#Item_29
			index_switch_3.inputs[30].default_value = False
			#Item_30
			index_switch_3.inputs[31].default_value = False
			#Item_32
			index_switch_3.inputs[33].default_value = False
			#Item_34
			index_switch_3.inputs[35].default_value = False
			#Item_35
			index_switch_3.inputs[36].default_value = False
			#Item_36
			index_switch_3.inputs[37].default_value = False
			#Item_37
			index_switch_3.inputs[38].default_value = False
			#Item_38
			index_switch_3.inputs[39].default_value = False
			#Item_39
			index_switch_3.inputs[40].default_value = False
			#Item_40
			index_switch_3.inputs[41].default_value = False
			#Item_42
			index_switch_3.inputs[43].default_value = False

			#node Boolean
			boolean = select_nucleic_type.nodes.new("FunctionNodeInputBool")
			boolean.name = "Boolean"
			boolean.boolean = True

			#node Index Switch.001
			index_switch_001_2 = select_nucleic_type.nodes.new("GeometryNodeIndexSwitch")
			index_switch_001_2.name = "Index Switch.001"
			index_switch_001_2.data_type = 'BOOLEAN'
			index_switch_001_2.index_switch_items.clear()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.index_switch_items.new()
			index_switch_001_2.inputs[1].hide = True
			index_switch_001_2.inputs[2].hide = True
			index_switch_001_2.inputs[3].hide = True
			index_switch_001_2.inputs[4].hide = True
			index_switch_001_2.inputs[5].hide = True
			index_switch_001_2.inputs[6].hide = True
			index_switch_001_2.inputs[7].hide = True
			index_switch_001_2.inputs[8].hide = True
			index_switch_001_2.inputs[9].hide = True
			index_switch_001_2.inputs[10].hide = True
			index_switch_001_2.inputs[11].hide = True
			index_switch_001_2.inputs[12].hide = True
			index_switch_001_2.inputs[13].hide = True
			index_switch_001_2.inputs[14].hide = True
			index_switch_001_2.inputs[15].hide = True
			index_switch_001_2.inputs[16].hide = True
			index_switch_001_2.inputs[17].hide = True
			index_switch_001_2.inputs[18].hide = True
			index_switch_001_2.inputs[19].hide = True
			index_switch_001_2.inputs[20].hide = True
			index_switch_001_2.inputs[21].hide = True
			index_switch_001_2.inputs[22].hide = True
			index_switch_001_2.inputs[23].hide = True
			index_switch_001_2.inputs[24].hide = True
			index_switch_001_2.inputs[25].hide = True
			index_switch_001_2.inputs[26].hide = True
			index_switch_001_2.inputs[27].hide = True
			index_switch_001_2.inputs[28].hide = True
			index_switch_001_2.inputs[29].hide = True
			index_switch_001_2.inputs[30].hide = True
			index_switch_001_2.inputs[32].hide = True
			index_switch_001_2.inputs[34].hide = True
			index_switch_001_2.inputs[35].hide = True
			index_switch_001_2.inputs[36].hide = True
			index_switch_001_2.inputs[37].hide = True
			index_switch_001_2.inputs[38].hide = True
			index_switch_001_2.inputs[39].hide = True
			index_switch_001_2.inputs[40].hide = True
			index_switch_001_2.inputs[42].hide = True
			index_switch_001_2.inputs[44].hide = True
			index_switch_001_2.inputs[45].hide = True
			#Item_0
			index_switch_001_2.inputs[1].default_value = False
			#Item_1
			index_switch_001_2.inputs[2].default_value = False
			#Item_2
			index_switch_001_2.inputs[3].default_value = False
			#Item_3
			index_switch_001_2.inputs[4].default_value = False
			#Item_4
			index_switch_001_2.inputs[5].default_value = False
			#Item_5
			index_switch_001_2.inputs[6].default_value = False
			#Item_6
			index_switch_001_2.inputs[7].default_value = False
			#Item_7
			index_switch_001_2.inputs[8].default_value = False
			#Item_8
			index_switch_001_2.inputs[9].default_value = False
			#Item_9
			index_switch_001_2.inputs[10].default_value = False
			#Item_10
			index_switch_001_2.inputs[11].default_value = False
			#Item_11
			index_switch_001_2.inputs[12].default_value = False
			#Item_12
			index_switch_001_2.inputs[13].default_value = False
			#Item_13
			index_switch_001_2.inputs[14].default_value = False
			#Item_14
			index_switch_001_2.inputs[15].default_value = False
			#Item_15
			index_switch_001_2.inputs[16].default_value = False
			#Item_16
			index_switch_001_2.inputs[17].default_value = False
			#Item_17
			index_switch_001_2.inputs[18].default_value = False
			#Item_18
			index_switch_001_2.inputs[19].default_value = False
			#Item_19
			index_switch_001_2.inputs[20].default_value = False
			#Item_20
			index_switch_001_2.inputs[21].default_value = False
			#Item_21
			index_switch_001_2.inputs[22].default_value = False
			#Item_22
			index_switch_001_2.inputs[23].default_value = False
			#Item_23
			index_switch_001_2.inputs[24].default_value = False
			#Item_24
			index_switch_001_2.inputs[25].default_value = False
			#Item_25
			index_switch_001_2.inputs[26].default_value = False
			#Item_26
			index_switch_001_2.inputs[27].default_value = False
			#Item_27
			index_switch_001_2.inputs[28].default_value = False
			#Item_28
			index_switch_001_2.inputs[29].default_value = False
			#Item_29
			index_switch_001_2.inputs[30].default_value = False
			#Item_31
			index_switch_001_2.inputs[32].default_value = False
			#Item_33
			index_switch_001_2.inputs[34].default_value = False
			#Item_34
			index_switch_001_2.inputs[35].default_value = False
			#Item_35
			index_switch_001_2.inputs[36].default_value = False
			#Item_36
			index_switch_001_2.inputs[37].default_value = False
			#Item_37
			index_switch_001_2.inputs[38].default_value = False
			#Item_38
			index_switch_001_2.inputs[39].default_value = False
			#Item_39
			index_switch_001_2.inputs[40].default_value = False
			#Item_41
			index_switch_001_2.inputs[42].default_value = False
			#Item_43
			index_switch_001_2.inputs[44].default_value = False

			#node Group
			group_32 = select_nucleic_type.nodes.new("GeometryNodeGroup")
			group_32.name = "Group"
			group_32.node_tree = boolean_andor

			#node Group Input
			group_input_86 = select_nucleic_type.nodes.new("NodeGroupInput")
			group_input_86.name = "Group Input"

			#node Group.001
			group_001_21 = select_nucleic_type.nodes.new("GeometryNodeGroup")
			group_001_21.name = "Group.001"
			group_001_21.node_tree = boolean_andor




			#Set locations
			named_attribute_010.location = (60.0, 400.0)
			group_output_87.location = (780.0, 560.0)
			index_switch_3.location = (340.0, 220.0)
			boolean.location = (120.0, 260.0)
			index_switch_001_2.location = (340.0, 420.0)
			group_32.location = (578.2772216796875, 565.6964111328125)
			group_input_86.location = (340.0, 540.0)
			group_001_21.location = (580.0, 380.0)

			#Set dimensions
			named_attribute_010.width, named_attribute_010.height = 206.99917602539062, 100.0
			group_output_87.width, group_output_87.height = 140.0, 100.0
			index_switch_3.width, index_switch_3.height = 140.0, 100.0
			boolean.width, boolean.height = 140.0, 100.0
			index_switch_001_2.width, index_switch_001_2.height = 140.0, 100.0
			group_32.width, group_32.height = 140.0, 100.0
			group_input_86.width, group_input_86.height = 140.0, 100.0
			group_001_21.width, group_001_21.height = 140.0, 100.0

			#initialize select_nucleic_type links
			#named_attribute_010.Attribute -> index_switch_3.Index
			select_nucleic_type.links.new(named_attribute_010.outputs[0], index_switch_3.inputs[0])
			#boolean.Boolean -> index_switch_3.31
			select_nucleic_type.links.new(boolean.outputs[0], index_switch_3.inputs[32])
			#boolean.Boolean -> index_switch_3.33
			select_nucleic_type.links.new(boolean.outputs[0], index_switch_3.inputs[34])
			#boolean.Boolean -> index_switch_3.41
			select_nucleic_type.links.new(boolean.outputs[0], index_switch_3.inputs[42])
			#boolean.Boolean -> index_switch_3.43
			select_nucleic_type.links.new(boolean.outputs[0], index_switch_3.inputs[44])
			#boolean.Boolean -> index_switch_001_2.30
			select_nucleic_type.links.new(boolean.outputs[0], index_switch_001_2.inputs[31])
			#boolean.Boolean -> index_switch_001_2.32
			select_nucleic_type.links.new(boolean.outputs[0], index_switch_001_2.inputs[33])
			#boolean.Boolean -> index_switch_001_2.40
			select_nucleic_type.links.new(boolean.outputs[0], index_switch_001_2.inputs[41])
			#boolean.Boolean -> index_switch_001_2.42
			select_nucleic_type.links.new(boolean.outputs[0], index_switch_001_2.inputs[43])
			#named_attribute_010.Attribute -> index_switch_001_2.Index
			select_nucleic_type.links.new(named_attribute_010.outputs[0], index_switch_001_2.inputs[0])
			#group_input_86.And -> group_32.And
			select_nucleic_type.links.new(group_input_86.outputs[0], group_32.inputs[0])
			#group_input_86.Or -> group_32.Or
			select_nucleic_type.links.new(group_input_86.outputs[1], group_32.inputs[1])
			#index_switch_001_2.Output -> group_32.Boolean
			select_nucleic_type.links.new(index_switch_001_2.outputs[0], group_32.inputs[2])
			#group_input_86.And -> group_001_21.And
			select_nucleic_type.links.new(group_input_86.outputs[0], group_001_21.inputs[0])
			#group_input_86.Or -> group_001_21.Or
			select_nucleic_type.links.new(group_input_86.outputs[1], group_001_21.inputs[1])
			#group_32.Boolean -> group_output_87.is_purine
			select_nucleic_type.links.new(group_32.outputs[0], group_output_87.inputs[0])
			#index_switch_3.Output -> group_001_21.Boolean
			select_nucleic_type.links.new(index_switch_3.outputs[0], group_001_21.inputs[2])
			#group_001_21.Boolean -> group_output_87.is_pyrimidine
			select_nucleic_type.links.new(group_001_21.outputs[0], group_output_87.inputs[1])
			return select_nucleic_type

		select_nucleic_type = select_nucleic_type_node_group()

		#initialize _sample_nucleic_base_values node group
		def _sample_nucleic_base_values_node_group():
			_sample_nucleic_base_values = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".Sample Nucleic Base Values")

			_sample_nucleic_base_values.color_tag = 'NONE'
			_sample_nucleic_base_values.description = ""


			#_sample_nucleic_base_values interface
			#Socket base_valid
			base_valid_socket = _sample_nucleic_base_values.interface.new_socket(name = "base_valid", in_out='OUTPUT', socket_type = 'NodeSocketBool')
			base_valid_socket.attribute_domain = 'POINT'

			#Socket base_pivot'
			base_pivot__socket = _sample_nucleic_base_values.interface.new_socket(name = "base_pivot'", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			base_pivot__socket.subtype = 'NONE'
			base_pivot__socket.default_value = (0.0, 0.0, 0.0)
			base_pivot__socket.min_value = -3.4028234663852886e+38
			base_pivot__socket.max_value = 3.4028234663852886e+38
			base_pivot__socket.attribute_domain = 'POINT'

			#Socket base_Z
			base_z_socket = _sample_nucleic_base_values.interface.new_socket(name = "base_Z", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			base_z_socket.subtype = 'NONE'
			base_z_socket.default_value = (0.0, 0.0, 0.0)
			base_z_socket.min_value = -3.4028234663852886e+38
			base_z_socket.max_value = 3.4028234663852886e+38
			base_z_socket.attribute_domain = 'POINT'

			#Socket base_Y
			base_y_socket = _sample_nucleic_base_values.interface.new_socket(name = "base_Y", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			base_y_socket.subtype = 'NONE'
			base_y_socket.default_value = (0.0, 0.0, 0.0)
			base_y_socket.min_value = -3.4028234663852886e+38
			base_y_socket.max_value = 3.4028234663852886e+38
			base_y_socket.attribute_domain = 'POINT'

			#Socket base_position
			base_position_socket = _sample_nucleic_base_values.interface.new_socket(name = "base_position", in_out='OUTPUT', socket_type = 'NodeSocketVector')
			base_position_socket.subtype = 'NONE'
			base_position_socket.default_value = (0.0, 0.0, 0.0)
			base_position_socket.min_value = -3.4028234663852886e+38
			base_position_socket.max_value = 3.4028234663852886e+38
			base_position_socket.attribute_domain = 'POINT'

			#Socket Base Color
			base_color_socket = _sample_nucleic_base_values.interface.new_socket(name = "Base Color", in_out='OUTPUT', socket_type = 'NodeSocketColor')
			base_color_socket.attribute_domain = 'POINT'

			#Socket Input
			input_socket_3 = _sample_nucleic_base_values.interface.new_socket(name = "Input", in_out='INPUT', socket_type = 'NodeSocketInt')
			input_socket_3.subtype = 'NONE'
			input_socket_3.default_value = 0
			input_socket_3.min_value = -2147483648
			input_socket_3.max_value = 2147483647
			input_socket_3.attribute_domain = 'POINT'


			#initialize _sample_nucleic_base_values nodes
			#node Group Output
			group_output_88 = _sample_nucleic_base_values.nodes.new("NodeGroupOutput")
			group_output_88.name = "Group Output"
			group_output_88.is_active_output = True

			#node Group Input
			group_input_87 = _sample_nucleic_base_values.nodes.new("NodeGroupInput")
			group_input_87.name = "Group Input"

			#node Group.001
			group_001_22 = _sample_nucleic_base_values.nodes.new("GeometryNodeGroup")
			group_001_22.name = "Group.001"
			group_001_22.node_tree = residue_mask
			#Socket_1
			group_001_22.inputs[0].default_value = 61
			#Socket_5
			group_001_22.inputs[1].default_value = False

			#node Group.008
			group_008_7 = _sample_nucleic_base_values.nodes.new("GeometryNodeGroup")
			group_008_7.name = "Group.008"
			group_008_7.node_tree = residue_mask
			#Socket_5
			group_008_7.inputs[1].default_value = False

			#node Reroute.015
			reroute_015 = _sample_nucleic_base_values.nodes.new("NodeReroute")
			reroute_015.name = "Reroute.015"
			#node Switch.010
			switch_010 = _sample_nucleic_base_values.nodes.new("GeometryNodeSwitch")
			switch_010.name = "Switch.010"
			switch_010.input_type = 'INT'
			#False
			switch_010.inputs[1].default_value = 65
			#True
			switch_010.inputs[2].default_value = 68

			#node Switch.011
			switch_011 = _sample_nucleic_base_values.nodes.new("GeometryNodeSwitch")
			switch_011.name = "Switch.011"
			switch_011.input_type = 'INT'
			#False
			switch_011.inputs[1].default_value = 62
			#True
			switch_011.inputs[2].default_value = 64

			#node Group.013
			group_013_3 = _sample_nucleic_base_values.nodes.new("GeometryNodeGroup")
			group_013_3.name = "Group.013"
			group_013_3.node_tree = select_nucleic_type
			#Socket_0
			group_013_3.inputs[0].default_value = True
			#Socket_1
			group_013_3.inputs[1].default_value = False

			#node Group.014
			group_014_4 = _sample_nucleic_base_values.nodes.new("GeometryNodeGroup")
			group_014_4.name = "Group.014"
			group_014_4.node_tree = residue_mask
			#Socket_5
			group_014_4.inputs[1].default_value = False

			#node Vector Math.007
			vector_math_007_2 = _sample_nucleic_base_values.nodes.new("ShaderNodeVectorMath")
			vector_math_007_2.name = "Vector Math.007"
			vector_math_007_2.operation = 'SUBTRACT'

			#node Vector Math.008
			vector_math_008_1 = _sample_nucleic_base_values.nodes.new("ShaderNodeVectorMath")
			vector_math_008_1.name = "Vector Math.008"
			vector_math_008_1.operation = 'SUBTRACT'

			#node Group.007
			group_007_5 = _sample_nucleic_base_values.nodes.new("GeometryNodeGroup")
			group_007_5.name = "Group.007"
			group_007_5.node_tree = residue_mask
			#Socket_1
			group_007_5.inputs[0].default_value = 55
			#Socket_5
			group_007_5.inputs[1].default_value = False

			#node Group.009
			group_009_7 = _sample_nucleic_base_values.nodes.new("GeometryNodeGroup")
			group_009_7.name = "Group.009"
			group_009_7.node_tree = residue_mask
			#Socket_1
			group_009_7.inputs[0].default_value = 57
			#Socket_5
			group_009_7.inputs[1].default_value = False

			#node Reroute.018
			reroute_018 = _sample_nucleic_base_values.nodes.new("NodeReroute")
			reroute_018.name = "Reroute.018"
			#node Mix.001
			mix_001_1 = _sample_nucleic_base_values.nodes.new("ShaderNodeMix")
			mix_001_1.name = "Mix.001"
			mix_001_1.blend_type = 'MIX'
			mix_001_1.clamp_factor = True
			mix_001_1.clamp_result = False
			mix_001_1.data_type = 'VECTOR'
			mix_001_1.factor_mode = 'UNIFORM'
			#Factor_Float
			mix_001_1.inputs[0].default_value = 0.0

			#node Group.010
			group_010_9 = _sample_nucleic_base_values.nodes.new("GeometryNodeGroup")
			group_010_9.name = "Group.010"
			group_010_9.node_tree = residue_mask
			#Socket_1
			group_010_9.inputs[0].default_value = 67
			#Socket_5
			group_010_9.inputs[1].default_value = False

			#node Evaluate at Index.001
			evaluate_at_index_001_5 = _sample_nucleic_base_values.nodes.new("GeometryNodeFieldAtIndex")
			evaluate_at_index_001_5.name = "Evaluate at Index.001"
			evaluate_at_index_001_5.data_type = 'FLOAT_COLOR'
			evaluate_at_index_001_5.domain = 'POINT'

			#node Named Attribute
			named_attribute_9 = _sample_nucleic_base_values.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_9.name = "Named Attribute"
			named_attribute_9.data_type = 'FLOAT_COLOR'
			#Name
			named_attribute_9.inputs[0].default_value = "Color"

			#node Reroute.007
			reroute_007_1 = _sample_nucleic_base_values.nodes.new("NodeReroute")
			reroute_007_1.name = "Reroute.007"
			#node Boolean Math
			boolean_math_18 = _sample_nucleic_base_values.nodes.new("FunctionNodeBooleanMath")
			boolean_math_18.name = "Boolean Math"
			boolean_math_18.operation = 'AND'

			#node Boolean Math.001
			boolean_math_001_14 = _sample_nucleic_base_values.nodes.new("FunctionNodeBooleanMath")
			boolean_math_001_14.name = "Boolean Math.001"
			boolean_math_001_14.operation = 'AND'

			#node Reroute.006
			reroute_006_2 = _sample_nucleic_base_values.nodes.new("NodeReroute")
			reroute_006_2.label = "base_valid"
			reroute_006_2.name = "Reroute.006"
			#node Reroute.010
			reroute_010_2 = _sample_nucleic_base_values.nodes.new("NodeReroute")
			reroute_010_2.label = "base_pivot"
			reroute_010_2.name = "Reroute.010"
			#node Reroute.011
			reroute_011_1 = _sample_nucleic_base_values.nodes.new("NodeReroute")
			reroute_011_1.label = "base_Z"
			reroute_011_1.name = "Reroute.011"
			#node Reroute.012
			reroute_012_1 = _sample_nucleic_base_values.nodes.new("NodeReroute")
			reroute_012_1.label = "base_Y"
			reroute_012_1.name = "Reroute.012"
			#node Frame.001
			frame_001_10 = _sample_nucleic_base_values.nodes.new("NodeFrame")
			frame_001_10.label = "Sample relevant base positions for orientations"
			frame_001_10.name = "Frame.001"
			frame_001_10.label_size = 20
			frame_001_10.shrink = True

			#node Reroute
			reroute_21 = _sample_nucleic_base_values.nodes.new("NodeReroute")
			reroute_21.name = "Reroute"


			#Set parents
			group_001_22.parent = frame_001_10
			group_008_7.parent = frame_001_10
			reroute_015.parent = frame_001_10
			switch_010.parent = frame_001_10
			switch_011.parent = frame_001_10
			group_013_3.parent = frame_001_10
			group_014_4.parent = frame_001_10
			vector_math_007_2.parent = frame_001_10
			vector_math_008_1.parent = frame_001_10
			group_007_5.parent = frame_001_10
			group_009_7.parent = frame_001_10
			reroute_018.parent = frame_001_10
			mix_001_1.parent = frame_001_10
			group_010_9.parent = frame_001_10
			evaluate_at_index_001_5.parent = frame_001_10
			named_attribute_9.parent = frame_001_10
			reroute_007_1.parent = frame_001_10
			boolean_math_18.parent = frame_001_10
			boolean_math_001_14.parent = frame_001_10
			reroute_006_2.parent = frame_001_10
			reroute_010_2.parent = frame_001_10
			reroute_011_1.parent = frame_001_10
			reroute_012_1.parent = frame_001_10
			reroute_21.parent = frame_001_10

			#Set locations
			group_output_88.location = (641.2861328125, 0.0)
			group_input_87.location = (-754.88525390625, 0.0)
			group_001_22.location = (-4200.0, -820.0)
			group_008_7.location = (-4200.0, -1040.0)
			reroute_015.location = (-4300.0, -1060.0)
			switch_010.location = (-4540.0, -1040.0)
			switch_011.location = (-4540.0, -1220.0)
			group_013_3.location = (-4800.0, -1120.0)
			group_014_4.location = (-4194.8857421875, -1270.199951171875)
			vector_math_007_2.location = (-4000.0, -980.0)
			vector_math_008_1.location = (-3994.8857421875, -1150.199951171875)
			group_007_5.location = (-4200.0, -360.0)
			group_009_7.location = (-4200.0, -600.0)
			reroute_018.location = (-4320.0, -680.0)
			mix_001_1.location = (-4020.0, -360.0)
			group_010_9.location = (-4200.0, 0.0)
			evaluate_at_index_001_5.location = (-4020.0, -100.0)
			named_attribute_9.location = (-4200.0, -220.0)
			reroute_007_1.location = (-4480.0, -680.0)
			boolean_math_18.location = (-4000.0, -840.0)
			boolean_math_001_14.location = (-4000.0, -700.0)
			reroute_006_2.location = (-3720.0, -760.0)
			reroute_010_2.location = (-3720.0, -800.0)
			reroute_011_1.location = (-3720.0, -840.0)
			reroute_012_1.location = (-3720.0, -880.0)
			frame_001_10.location = (4274.8857421875, 610.2000122070312)
			reroute_21.location = (-4016.738525390625, -1053.5716552734375)

			#Set dimensions
			group_output_88.width, group_output_88.height = 140.0, 100.0
			group_input_87.width, group_input_87.height = 140.0, 100.0
			group_001_22.width, group_001_22.height = 140.0, 100.0
			group_008_7.width, group_008_7.height = 140.0, 100.0
			reroute_015.width, reroute_015.height = 16.0, 100.0
			switch_010.width, switch_010.height = 145.0830078125, 100.0
			switch_011.width, switch_011.height = 145.0830078125, 100.0
			group_013_3.width, group_013_3.height = 221.22412109375, 100.0
			group_014_4.width, group_014_4.height = 140.0, 100.0
			vector_math_007_2.width, vector_math_007_2.height = 140.0, 100.0
			vector_math_008_1.width, vector_math_008_1.height = 140.0, 100.0
			group_007_5.width, group_007_5.height = 140.0, 100.0
			group_009_7.width, group_009_7.height = 140.0, 100.0
			reroute_018.width, reroute_018.height = 16.0, 100.0
			mix_001_1.width, mix_001_1.height = 140.0, 100.0
			group_010_9.width, group_010_9.height = 140.0, 100.0
			evaluate_at_index_001_5.width, evaluate_at_index_001_5.height = 140.0, 100.0
			named_attribute_9.width, named_attribute_9.height = 140.0, 100.0
			reroute_007_1.width, reroute_007_1.height = 16.0, 100.0
			boolean_math_18.width, boolean_math_18.height = 140.0, 100.0
			boolean_math_001_14.width, boolean_math_001_14.height = 140.0, 100.0
			reroute_006_2.width, reroute_006_2.height = 16.0, 100.0
			reroute_010_2.width, reroute_010_2.height = 16.0, 100.0
			reroute_011_1.width, reroute_011_1.height = 16.0, 100.0
			reroute_012_1.width, reroute_012_1.height = 16.0, 100.0
			frame_001_10.width, frame_001_10.height = 1146.08544921875, 1545.199951171875
			reroute_21.width, reroute_21.height = 16.0, 100.0

			#initialize _sample_nucleic_base_values links
			#group_013_3.is_pyrimidine -> switch_010.Switch
			_sample_nucleic_base_values.links.new(group_013_3.outputs[1], switch_010.inputs[0])
			#group_008_7.Is Valid -> boolean_math_18.Boolean
			_sample_nucleic_base_values.links.new(group_008_7.outputs[0], boolean_math_18.inputs[1])
			#group_013_3.is_pyrimidine -> switch_011.Switch
			_sample_nucleic_base_values.links.new(group_013_3.outputs[1], switch_011.inputs[0])
			#group_014_4.Position -> vector_math_007_2.Vector
			_sample_nucleic_base_values.links.new(group_014_4.outputs[2], vector_math_007_2.inputs[0])
			#group_014_4.Is Valid -> boolean_math_001_14.Boolean
			_sample_nucleic_base_values.links.new(group_014_4.outputs[0], boolean_math_001_14.inputs[1])
			#group_009_7.Position -> mix_001_1.B
			_sample_nucleic_base_values.links.new(group_009_7.outputs[2], mix_001_1.inputs[5])
			#switch_011.Output -> group_014_4.atom_name
			_sample_nucleic_base_values.links.new(switch_011.outputs[0], group_014_4.inputs[0])
			#group_010_9.Index -> evaluate_at_index_001_5.Index
			_sample_nucleic_base_values.links.new(group_010_9.outputs[1], evaluate_at_index_001_5.inputs[0])
			#reroute_018.Output -> group_009_7.Group ID
			_sample_nucleic_base_values.links.new(reroute_018.outputs[0], group_009_7.inputs[2])
			#named_attribute_9.Attribute -> evaluate_at_index_001_5.Value
			_sample_nucleic_base_values.links.new(named_attribute_9.outputs[0], evaluate_at_index_001_5.inputs[1])
			#reroute_015.Output -> group_014_4.Group ID
			_sample_nucleic_base_values.links.new(reroute_015.outputs[0], group_014_4.inputs[2])
			#boolean_math_18.Boolean -> boolean_math_001_14.Boolean
			_sample_nucleic_base_values.links.new(boolean_math_18.outputs[0], boolean_math_001_14.inputs[0])
			#vector_math_008_1.Vector -> reroute_012_1.Input
			_sample_nucleic_base_values.links.new(vector_math_008_1.outputs[0], reroute_012_1.inputs[0])
			#group_001_22.Is Valid -> boolean_math_18.Boolean
			_sample_nucleic_base_values.links.new(group_001_22.outputs[0], boolean_math_18.inputs[0])
			#group_001_22.Position -> reroute_010_2.Input
			_sample_nucleic_base_values.links.new(group_001_22.outputs[2], reroute_010_2.inputs[0])
			#boolean_math_001_14.Boolean -> reroute_006_2.Input
			_sample_nucleic_base_values.links.new(boolean_math_001_14.outputs[0], reroute_006_2.inputs[0])
			#reroute_015.Output -> group_001_22.Group ID
			_sample_nucleic_base_values.links.new(reroute_015.outputs[0], group_001_22.inputs[2])
			#reroute_018.Output -> group_007_5.Group ID
			_sample_nucleic_base_values.links.new(reroute_018.outputs[0], group_007_5.inputs[2])
			#reroute_015.Output -> group_008_7.Group ID
			_sample_nucleic_base_values.links.new(reroute_015.outputs[0], group_008_7.inputs[2])
			#group_007_5.Position -> mix_001_1.A
			_sample_nucleic_base_values.links.new(group_007_5.outputs[2], mix_001_1.inputs[4])
			#group_014_4.Position -> vector_math_008_1.Vector
			_sample_nucleic_base_values.links.new(group_014_4.outputs[2], vector_math_008_1.inputs[1])
			#reroute_007_1.Output -> reroute_018.Input
			_sample_nucleic_base_values.links.new(reroute_007_1.outputs[0], reroute_018.inputs[0])
			#switch_010.Output -> group_008_7.atom_name
			_sample_nucleic_base_values.links.new(switch_010.outputs[0], group_008_7.inputs[0])
			#reroute_007_1.Output -> reroute_015.Input
			_sample_nucleic_base_values.links.new(reroute_007_1.outputs[0], reroute_015.inputs[0])
			#reroute_018.Output -> group_010_9.Group ID
			_sample_nucleic_base_values.links.new(reroute_018.outputs[0], group_010_9.inputs[2])
			#group_008_7.Position -> vector_math_008_1.Vector
			_sample_nucleic_base_values.links.new(group_008_7.outputs[2], vector_math_008_1.inputs[0])
			#vector_math_007_2.Vector -> reroute_011_1.Input
			_sample_nucleic_base_values.links.new(vector_math_007_2.outputs[0], reroute_011_1.inputs[0])
			#group_input_87.Input -> reroute_007_1.Input
			_sample_nucleic_base_values.links.new(group_input_87.outputs[0], reroute_007_1.inputs[0])
			#mix_001_1.Result -> group_output_88.base_position
			_sample_nucleic_base_values.links.new(mix_001_1.outputs[1], group_output_88.inputs[4])
			#evaluate_at_index_001_5.Value -> group_output_88.Base Color
			_sample_nucleic_base_values.links.new(evaluate_at_index_001_5.outputs[0], group_output_88.inputs[5])
			#reroute_006_2.Output -> group_output_88.base_valid
			_sample_nucleic_base_values.links.new(reroute_006_2.outputs[0], group_output_88.inputs[0])
			#reroute_010_2.Output -> group_output_88.base_pivot'
			_sample_nucleic_base_values.links.new(reroute_010_2.outputs[0], group_output_88.inputs[1])
			#reroute_011_1.Output -> group_output_88.base_Z
			_sample_nucleic_base_values.links.new(reroute_011_1.outputs[0], group_output_88.inputs[2])
			#reroute_012_1.Output -> group_output_88.base_Y
			_sample_nucleic_base_values.links.new(reroute_012_1.outputs[0], group_output_88.inputs[3])
			#group_001_22.Position -> reroute_21.Input
			_sample_nucleic_base_values.links.new(group_001_22.outputs[2], reroute_21.inputs[0])
			#reroute_21.Output -> vector_math_007_2.Vector
			_sample_nucleic_base_values.links.new(reroute_21.outputs[0], vector_math_007_2.inputs[1])
			return _sample_nucleic_base_values

		_sample_nucleic_base_values = _sample_nucleic_base_values_node_group()

		#initialize _mn_utils_style_ribbon_nucleic node group
		def _mn_utils_style_ribbon_nucleic_node_group():
			_mn_utils_style_ribbon_nucleic = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".MN_utils_style_ribbon_nucleic")

			_mn_utils_style_ribbon_nucleic.color_tag = 'GEOMETRY'
			_mn_utils_style_ribbon_nucleic.description = ""

			_mn_utils_style_ribbon_nucleic.is_modifier = True

			#_mn_utils_style_ribbon_nucleic interface
			#Socket Geometry
			geometry_socket_16 = _mn_utils_style_ribbon_nucleic.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			geometry_socket_16.attribute_domain = 'POINT'

			#Socket Curve
			curve_socket_6 = _mn_utils_style_ribbon_nucleic.interface.new_socket(name = "Curve", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			curve_socket_6.attribute_domain = 'POINT'

			#Socket Atoms
			atoms_socket_10 = _mn_utils_style_ribbon_nucleic.interface.new_socket(name = "Atoms", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			atoms_socket_10.attribute_domain = 'POINT'
			atoms_socket_10.description = "Atomic geometry that contains vertices and edges"

			#Socket Selection
			selection_socket_13 = _mn_utils_style_ribbon_nucleic.interface.new_socket(name = "Selection", in_out='INPUT', socket_type = 'NodeSocketBool')
			selection_socket_13.attribute_domain = 'POINT'
			selection_socket_13.hide_value = True
			selection_socket_13.description = "Selection of atoms to apply this node to"

			#Socket Material
			material_socket_2 = _mn_utils_style_ribbon_nucleic.interface.new_socket(name = "Material", in_out='INPUT', socket_type = 'NodeSocketMaterial')
			material_socket_2.attribute_domain = 'POINT'
			material_socket_2.description = "Material to apply to the resulting geometry"

			#Socket Blur Color
			blur_color_socket = _mn_utils_style_ribbon_nucleic.interface.new_socket(name = "Blur Color", in_out='INPUT', socket_type = 'NodeSocketBool')
			blur_color_socket.attribute_domain = 'POINT'

			#Panel Backbone
			backbone_panel = _mn_utils_style_ribbon_nucleic.interface.new_panel("Backbone")
			#Socket Backbone Subdivisions
			backbone_subdivisions_socket = _mn_utils_style_ribbon_nucleic.interface.new_socket(name = "Backbone Subdivisions", in_out='INPUT', socket_type = 'NodeSocketInt', parent = backbone_panel)
			backbone_subdivisions_socket.subtype = 'NONE'
			backbone_subdivisions_socket.default_value = 3
			backbone_subdivisions_socket.min_value = 1
			backbone_subdivisions_socket.max_value = 10
			backbone_subdivisions_socket.attribute_domain = 'POINT'

			#Socket Backbone Resolution
			backbone_resolution_socket = _mn_utils_style_ribbon_nucleic.interface.new_socket(name = "Backbone Resolution", in_out='INPUT', socket_type = 'NodeSocketInt', parent = backbone_panel)
			backbone_resolution_socket.subtype = 'NONE'
			backbone_resolution_socket.default_value = 8
			backbone_resolution_socket.min_value = 3
			backbone_resolution_socket.max_value = 50
			backbone_resolution_socket.attribute_domain = 'POINT'

			#Socket Backbone Radius
			backbone_radius_socket = _mn_utils_style_ribbon_nucleic.interface.new_socket(name = "Backbone Radius", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = backbone_panel)
			backbone_radius_socket.subtype = 'DISTANCE'
			backbone_radius_socket.default_value = 2.0
			backbone_radius_socket.min_value = 0.0
			backbone_radius_socket.max_value = 3.4028234663852886e+38
			backbone_radius_socket.attribute_domain = 'POINT'

			#Socket Backbone Shade Smooth
			backbone_shade_smooth_socket = _mn_utils_style_ribbon_nucleic.interface.new_socket(name = "Backbone Shade Smooth", in_out='INPUT', socket_type = 'NodeSocketBool', parent = backbone_panel)
			backbone_shade_smooth_socket.attribute_domain = 'POINT'


			#Panel Base
			base_panel = _mn_utils_style_ribbon_nucleic.interface.new_panel("Base")
			#Socket Realise Bases
			realise_bases_socket = _mn_utils_style_ribbon_nucleic.interface.new_socket(name = "Realise Bases", in_out='INPUT', socket_type = 'NodeSocketBool', parent = base_panel)
			realise_bases_socket.attribute_domain = 'POINT'

			#Socket Base Radius
			base_radius_socket = _mn_utils_style_ribbon_nucleic.interface.new_socket(name = "Base Radius", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = base_panel)
			base_radius_socket.subtype = 'DISTANCE'
			base_radius_socket.default_value = 0.20000000298023224
			base_radius_socket.min_value = 0.0
			base_radius_socket.max_value = 3.4028234663852886e+38
			base_radius_socket.attribute_domain = 'POINT'

			#Socket Base Resolution
			base_resolution_socket = _mn_utils_style_ribbon_nucleic.interface.new_socket(name = "Base Resolution", in_out='INPUT', socket_type = 'NodeSocketInt', parent = base_panel)
			base_resolution_socket.subtype = 'NONE'
			base_resolution_socket.default_value = 6
			base_resolution_socket.min_value = 3
			base_resolution_socket.max_value = 512
			base_resolution_socket.attribute_domain = 'POINT'



			#initialize _mn_utils_style_ribbon_nucleic nodes
			#node Frame
			frame_15 = _mn_utils_style_ribbon_nucleic.nodes.new("NodeFrame")
			frame_15.label = "Delete between chains and distance too large"
			frame_15.name = "Frame"
			frame_15.label_size = 20
			frame_15.shrink = True

			#node Frame.006
			frame_006 = _mn_utils_style_ribbon_nucleic.nodes.new("NodeFrame")
			frame_006.label = "Slightly Extend Curve Ends"
			frame_006.name = "Frame.006"
			frame_006.label_size = 20
			frame_006.shrink = True

			#node Frame.005
			frame_005_1 = _mn_utils_style_ribbon_nucleic.nodes.new("NodeFrame")
			frame_005_1.label = "Instance simple base cylinder"
			frame_005_1.name = "Frame.005"
			frame_005_1.label_size = 20
			frame_005_1.shrink = True

			#node Group Output
			group_output_89 = _mn_utils_style_ribbon_nucleic.nodes.new("NodeGroupOutput")
			group_output_89.name = "Group Output"
			group_output_89.is_active_output = True

			#node Endpoint Selection
			endpoint_selection_4 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeCurveEndpointSelection")
			endpoint_selection_4.name = "Endpoint Selection"
			#Start Size
			endpoint_selection_4.inputs[0].default_value = 1
			#End Size
			endpoint_selection_4.inputs[1].default_value = 1

			#node Set Position.001
			set_position_001_4 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeSetPosition")
			set_position_001_4.name = "Set Position.001"
			set_position_001_4.inputs[2].hide = True
			#Position
			set_position_001_4.inputs[2].default_value = (0.0, 0.0, 0.0)

			#node Combine XYZ
			combine_xyz_1 = _mn_utils_style_ribbon_nucleic.nodes.new("ShaderNodeCombineXYZ")
			combine_xyz_1.name = "Combine XYZ"
			#X
			combine_xyz_1.inputs[0].default_value = 0.0
			#Y
			combine_xyz_1.inputs[1].default_value = 0.0

			#node Math
			math_27 = _mn_utils_style_ribbon_nucleic.nodes.new("ShaderNodeMath")
			math_27.name = "Math"
			math_27.operation = 'DIVIDE'
			math_27.use_clamp = False
			#Value_001
			math_27.inputs[1].default_value = 2.0

			#node Cylinder
			cylinder = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeMeshCylinder")
			cylinder.name = "Cylinder"
			cylinder.fill_type = 'NGON'
			#Side Segments
			cylinder.inputs[1].default_value = 1
			#Fill Segments
			cylinder.inputs[2].default_value = 1

			#node Value
			value_1 = _mn_utils_style_ribbon_nucleic.nodes.new("ShaderNodeValue")
			value_1.name = "Value"

			value_1.outputs[0].default_value = 1.0
			#node Group Input.005
			group_input_005_1 = _mn_utils_style_ribbon_nucleic.nodes.new("NodeGroupInput")
			group_input_005_1.name = "Group Input.005"
			group_input_005_1.outputs[0].hide = True
			group_input_005_1.outputs[1].hide = True
			group_input_005_1.outputs[2].hide = True
			group_input_005_1.outputs[3].hide = True
			group_input_005_1.outputs[4].hide = True
			group_input_005_1.outputs[5].hide = True
			group_input_005_1.outputs[6].hide = True
			group_input_005_1.outputs[7].hide = True
			group_input_005_1.outputs[8].hide = True
			group_input_005_1.outputs[11].hide = True

			#node Store Named Attribute.006
			store_named_attribute_006_1 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_006_1.name = "Store Named Attribute.006"
			store_named_attribute_006_1.data_type = 'FLOAT_VECTOR'
			store_named_attribute_006_1.domain = 'CORNER'
			#Selection
			store_named_attribute_006_1.inputs[1].default_value = True
			#Name
			store_named_attribute_006_1.inputs[2].default_value = "uv_map"

			#node Group Input
			group_input_88 = _mn_utils_style_ribbon_nucleic.nodes.new("NodeGroupInput")
			group_input_88.name = "Group Input"
			group_input_88.outputs[2].hide = True
			group_input_88.outputs[3].hide = True
			group_input_88.outputs[4].hide = True
			group_input_88.outputs[5].hide = True
			group_input_88.outputs[7].hide = True
			group_input_88.outputs[8].hide = True
			group_input_88.outputs[9].hide = True
			group_input_88.outputs[10].hide = True
			group_input_88.outputs[11].hide = True

			#node Transform
			transform = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeTransform")
			transform.name = "Transform"
			transform.mode = 'COMPONENTS'
			#Rotation
			transform.inputs[2].default_value = (0.0, 0.0, 0.7853981852531433)
			#Scale
			transform.inputs[3].default_value = (1.0, 1.0, 1.0)

			#node Instance on Points
			instance_on_points = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeInstanceOnPoints")
			instance_on_points.name = "Instance on Points"
			#Pick Instance
			instance_on_points.inputs[3].default_value = False
			#Instance Index
			instance_on_points.inputs[4].default_value = 0

			#node Set Material
			set_material_1 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeSetMaterial")
			set_material_1.name = "Set Material"
			#Selection
			set_material_1.inputs[1].default_value = True

			#node Join Geometry.001
			join_geometry_001_1 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeJoinGeometry")
			join_geometry_001_1.name = "Join Geometry.001"

			#node Is Nucleic
			is_nucleic_1 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeGroup")
			is_nucleic_1.label = "Is Nucleic"
			is_nucleic_1.name = "Is Nucleic"
			is_nucleic_1.node_tree = is_nucleic
			is_nucleic_1.inputs[1].hide = True
			is_nucleic_1.outputs[1].hide = True
			#Socket_3
			is_nucleic_1.inputs[1].default_value = False

			#node Capture Attribute.002
			capture_attribute_002_4 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeCaptureAttribute")
			capture_attribute_002_4.name = "Capture Attribute.002"
			capture_attribute_002_4.active_index = 1
			capture_attribute_002_4.capture_items.clear()
			capture_attribute_002_4.capture_items.new('FLOAT', "Selection")
			capture_attribute_002_4.capture_items["Selection"].data_type = 'BOOLEAN'
			capture_attribute_002_4.capture_items.new('FLOAT', "Backbone Radius")
			capture_attribute_002_4.capture_items["Backbone Radius"].data_type = 'FLOAT'
			capture_attribute_002_4.domain = 'POINT'

			#node Separate Geometry.002
			separate_geometry_002 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeSeparateGeometry")
			separate_geometry_002.name = "Separate Geometry.002"
			separate_geometry_002.domain = 'POINT'

			#node Group.002
			group_002_21 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeGroup")
			group_002_21.name = "Group.002"
			group_002_21.node_tree = res_group_id

			#node Capture Attribute.003
			capture_attribute_003 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeCaptureAttribute")
			capture_attribute_003.name = "Capture Attribute.003"
			capture_attribute_003.active_index = 0
			capture_attribute_003.capture_items.clear()
			capture_attribute_003.capture_items.new('FLOAT', "Unique Group ID")
			capture_attribute_003.capture_items["Unique Group ID"].data_type = 'INT'
			capture_attribute_003.domain = 'POINT'

			#node Capture Attribute.004
			capture_attribute_004_1 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeCaptureAttribute")
			capture_attribute_004_1.label = "base_pivot"
			capture_attribute_004_1.name = "Capture Attribute.004"
			capture_attribute_004_1.active_index = 4
			capture_attribute_004_1.capture_items.clear()
			capture_attribute_004_1.capture_items.new('FLOAT', "base_valid")
			capture_attribute_004_1.capture_items["base_valid"].data_type = 'BOOLEAN'
			capture_attribute_004_1.capture_items.new('FLOAT', "base_pivot")
			capture_attribute_004_1.capture_items["base_pivot"].data_type = 'FLOAT_VECTOR'
			capture_attribute_004_1.capture_items.new('FLOAT', "base_Z")
			capture_attribute_004_1.capture_items["base_Z"].data_type = 'FLOAT_VECTOR'
			capture_attribute_004_1.capture_items.new('FLOAT', "base_Y")
			capture_attribute_004_1.capture_items["base_Y"].data_type = 'FLOAT_VECTOR'
			capture_attribute_004_1.capture_items.new('FLOAT', "base_position")
			capture_attribute_004_1.capture_items["base_position"].data_type = 'FLOAT_VECTOR'
			capture_attribute_004_1.capture_items.new('FLOAT', "Base Color")
			capture_attribute_004_1.capture_items["Base Color"].data_type = 'FLOAT_COLOR'
			capture_attribute_004_1.domain = 'POINT'

			#node Mesh to Points
			mesh_to_points = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeMeshToPoints")
			mesh_to_points.name = "Mesh to Points"
			mesh_to_points.mode = 'VERTICES'
			#Radius
			mesh_to_points.inputs[3].default_value = 0.05000000074505806

			#node Compare.002
			compare_002_8 = _mn_utils_style_ribbon_nucleic.nodes.new("FunctionNodeCompare")
			compare_002_8.name = "Compare.002"
			compare_002_8.data_type = 'INT'
			compare_002_8.mode = 'ELEMENT'
			compare_002_8.operation = 'EQUAL'
			#B_INT
			compare_002_8.inputs[3].default_value = 55

			#node Named Attribute.010
			named_attribute_010_1 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_010_1.name = "Named Attribute.010"
			named_attribute_010_1.data_type = 'INT'
			#Name
			named_attribute_010_1.inputs[0].default_value = "atom_name"

			#node Reroute.005
			reroute_005_2 = _mn_utils_style_ribbon_nucleic.nodes.new("NodeReroute")
			reroute_005_2.name = "Reroute.005"
			#node Store Named Attribute
			store_named_attribute_4 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_4.name = "Store Named Attribute"
			store_named_attribute_4.data_type = 'BOOLEAN'
			store_named_attribute_4.domain = 'POINT'
			#Selection
			store_named_attribute_4.inputs[1].default_value = True
			#Name
			store_named_attribute_4.inputs[2].default_value = "is_backbone"
			#Value
			store_named_attribute_4.inputs[3].default_value = True

			#node Store Named Attribute.001
			store_named_attribute_001_3 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_001_3.name = "Store Named Attribute.001"
			store_named_attribute_001_3.data_type = 'BOOLEAN'
			store_named_attribute_001_3.domain = 'POINT'
			#Selection
			store_named_attribute_001_3.inputs[1].default_value = True
			#Name
			store_named_attribute_001_3.inputs[2].default_value = "is_side_chain"
			#Value
			store_named_attribute_001_3.inputs[3].default_value = True

			#node Remove Named Attribute
			remove_named_attribute_1 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeRemoveAttribute")
			remove_named_attribute_1.name = "Remove Named Attribute"
			remove_named_attribute_1.pattern_mode = 'WILDCARD'
			#Name
			remove_named_attribute_1.inputs[1].default_value = "tmp_*"

			#node Store Named Attribute.002
			store_named_attribute_002_3 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_002_3.name = "Store Named Attribute.002"
			store_named_attribute_002_3.data_type = 'FLOAT_COLOR'
			store_named_attribute_002_3.domain = 'POINT'
			#Selection
			store_named_attribute_002_3.inputs[1].default_value = True
			#Name
			store_named_attribute_002_3.inputs[2].default_value = "Color"

			#node Reroute.014
			reroute_014 = _mn_utils_style_ribbon_nucleic.nodes.new("NodeReroute")
			reroute_014.label = "Base Instances"
			reroute_014.name = "Reroute.014"
			#node Group
			group_33 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeGroup")
			group_33.name = "Group"
			group_33.node_tree = curve_custom_profile
			#Socket_8
			group_33.inputs[2].default_value = 'Default Profile'
			#Socket_6
			group_33.inputs[3].default_value = (0.0, 0.0, 0.0)
			#Input_2
			group_33.inputs[4].default_value = (1.0, 1.0, 1.0)
			#Input_13
			group_33.inputs[7].default_value = 1.0
			#Input_14
			group_33.inputs[8].default_value = 0.7853981852531433

			#node Group.005
			group_005_9 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeGroup")
			group_005_9.name = "Group.005"
			group_005_9.node_tree = _cleanup

			#node Group Input.001
			group_input_001_14 = _mn_utils_style_ribbon_nucleic.nodes.new("NodeGroupInput")
			group_input_001_14.name = "Group Input.001"
			group_input_001_14.outputs[0].hide = True
			group_input_001_14.outputs[1].hide = True
			group_input_001_14.outputs[4].hide = True
			group_input_001_14.outputs[6].hide = True
			group_input_001_14.outputs[8].hide = True
			group_input_001_14.outputs[9].hide = True
			group_input_001_14.outputs[10].hide = True
			group_input_001_14.outputs[11].hide = True

			#node Reroute.008
			reroute_008_1 = _mn_utils_style_ribbon_nucleic.nodes.new("NodeReroute")
			reroute_008_1.label = "Curve"
			reroute_008_1.name = "Reroute.008"
			#node Store Named Attribute.003
			store_named_attribute_003_3 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_003_3.name = "Store Named Attribute.003"
			store_named_attribute_003_3.data_type = 'FLOAT_COLOR'
			store_named_attribute_003_3.domain = 'FACE'
			#Selection
			store_named_attribute_003_3.inputs[1].default_value = True
			#Name
			store_named_attribute_003_3.inputs[2].default_value = "Color"
			#Value
			store_named_attribute_003_3.inputs[3].default_value = (0.0, 0.0, 0.0, 1.0)

			#node Realize Instances
			realize_instances_1 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeRealizeInstances")
			realize_instances_1.name = "Realize Instances"
			#Selection
			realize_instances_1.inputs[1].default_value = True
			#Realize All
			realize_instances_1.inputs[2].default_value = True
			#Depth
			realize_instances_1.inputs[3].default_value = 0

			#node Capture Attribute
			capture_attribute_8 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeCaptureAttribute")
			capture_attribute_8.name = "Capture Attribute"
			capture_attribute_8.active_index = 0
			capture_attribute_8.capture_items.clear()
			capture_attribute_8.capture_items.new('FLOAT', "Attribute")
			capture_attribute_8.capture_items["Attribute"].data_type = 'FLOAT_COLOR'
			capture_attribute_8.domain = 'INSTANCE'

			#node Named Attribute.002
			named_attribute_002_5 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_002_5.name = "Named Attribute.002"
			named_attribute_002_5.data_type = 'FLOAT_COLOR'
			#Name
			named_attribute_002_5.inputs[0].default_value = "Color"

			#node Store Named Attribute.004
			store_named_attribute_004_2 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_004_2.name = "Store Named Attribute.004"
			store_named_attribute_004_2.data_type = 'FLOAT_COLOR'
			store_named_attribute_004_2.domain = 'FACE'
			#Selection
			store_named_attribute_004_2.inputs[1].default_value = True
			#Name
			store_named_attribute_004_2.inputs[2].default_value = "Color"

			#node Switch.001
			switch_001_9 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeSwitch")
			switch_001_9.name = "Switch.001"
			switch_001_9.input_type = 'GEOMETRY'

			#node Group Input.002
			group_input_002_7 = _mn_utils_style_ribbon_nucleic.nodes.new("NodeGroupInput")
			group_input_002_7.name = "Group Input.002"
			group_input_002_7.outputs[0].hide = True
			group_input_002_7.outputs[1].hide = True
			group_input_002_7.outputs[2].hide = True
			group_input_002_7.outputs[3].hide = True
			group_input_002_7.outputs[4].hide = True
			group_input_002_7.outputs[5].hide = True
			group_input_002_7.outputs[6].hide = True
			group_input_002_7.outputs[7].hide = True
			group_input_002_7.outputs[9].hide = True
			group_input_002_7.outputs[10].hide = True
			group_input_002_7.outputs[11].hide = True

			#node Group.003
			group_003_13 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeGroup")
			group_003_13.name = "Group.003"
			group_003_13.node_tree = curve_split_splines
			#Socket_5
			group_003_13.inputs[1].default_value = True
			#Socket_4
			group_003_13.inputs[2].default_value = 'Minimum Twist'
			#Socket_2
			group_003_13.inputs[3].default_value = 0
			#Socket_7
			group_003_13.inputs[4].default_value = 'Split Distance'
			#Socket_6
			group_003_13.inputs[5].default_value = 0.10000000149011612
			#Socket_9
			group_003_13.inputs[6].default_value = (0.0, 0.0, 0.0)
			#Socket_16
			group_003_13.inputs[7].default_value = 0.0
			#Socket_17
			group_003_13.inputs[8].default_value = 'Bezier'
			#Socket_18
			group_003_13.inputs[9].default_value = 12

			#node Points to Curves
			points_to_curves_1 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodePointsToCurves")
			points_to_curves_1.name = "Points to Curves"
			#Weight
			points_to_curves_1.inputs[2].default_value = 0.0

			#node Named Attribute.003
			named_attribute_003_2 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_003_2.name = "Named Attribute.003"
			named_attribute_003_2.data_type = 'INT'
			#Name
			named_attribute_003_2.inputs[0].default_value = "chain_id"

			#node Set Curve Radius
			set_curve_radius_1 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeSetCurveRadius")
			set_curve_radius_1.name = "Set Curve Radius"
			#Selection
			set_curve_radius_1.inputs[1].default_value = True

			#node Group.004
			group_004_8 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeGroup")
			group_004_8.name = "Group.004"
			group_004_8.node_tree = curve_endpoint_values
			#Socket_5
			group_004_8.inputs[0].default_value = 1
			#Socket_1
			group_004_8.inputs[1].default_value = 1
			#Socket_2
			group_004_8.inputs[2].default_value = 0
			#Socket_6
			group_004_8.inputs[3].default_value = 1
			#Socket_3
			group_004_8.inputs[4].default_value = -1

			#node Group.006
			group_006_8 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeGroup")
			group_006_8.name = "Group.006"
			group_006_8.node_tree = vector_in_angstroms
			#Socket_4
			group_006_8.inputs[1].default_value = False

			#node Group.011
			group_011_8 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeGroup")
			group_011_8.name = "Group.011"
			group_011_8.node_tree = offset_vector
			#Socket_2
			group_011_8.inputs[0].default_value = 0

			#node Curve Tangent
			curve_tangent_1 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeInputTangent")
			curve_tangent_1.name = "Curve Tangent"

			#node Math.001
			math_001_10 = _mn_utils_style_ribbon_nucleic.nodes.new("ShaderNodeMath")
			math_001_10.name = "Math.001"
			math_001_10.operation = 'MULTIPLY'
			math_001_10.use_clamp = False
			#Value_001
			math_001_10.inputs[1].default_value = -2.0

			#node Group Input.003
			group_input_003_4 = _mn_utils_style_ribbon_nucleic.nodes.new("NodeGroupInput")
			group_input_003_4.name = "Group Input.003"
			group_input_003_4.outputs[0].hide = True
			group_input_003_4.outputs[1].hide = True
			group_input_003_4.outputs[2].hide = True
			group_input_003_4.outputs[3].hide = True
			group_input_003_4.outputs[5].hide = True
			group_input_003_4.outputs[6].hide = True
			group_input_003_4.outputs[7].hide = True
			group_input_003_4.outputs[8].hide = True
			group_input_003_4.outputs[9].hide = True
			group_input_003_4.outputs[10].hide = True
			group_input_003_4.outputs[11].hide = True

			#node Group.012
			group_012_4 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeGroup")
			group_012_4.name = "Group.012"
			group_012_4.node_tree = _sample_nucleic_base_values

			#node Set Curve Normal
			set_curve_normal_3 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeSetCurveNormal")
			set_curve_normal_3.name = "Set Curve Normal"
			set_curve_normal_3.mode = 'FREE'
			#Selection
			set_curve_normal_3.inputs[1].default_value = True

			#node Group.007
			group_007_6 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeGroup")
			group_007_6.name = "Group.007"
			group_007_6.node_tree = vector_in_angstroms
			#Socket_2
			group_007_6.inputs[0].default_value = (3.7899999618530273, 1.0900001525878906, 2.6100001335144043)
			#Socket_4
			group_007_6.inputs[1].default_value = False
			#Socket_3
			group_007_6.inputs[2].default_value = 2.5

			#node Axes to Rotation
			axes_to_rotation_1 = _mn_utils_style_ribbon_nucleic.nodes.new("FunctionNodeAxesToRotation")
			axes_to_rotation_1.name = "Axes to Rotation"
			axes_to_rotation_1.primary_axis = 'Z'
			axes_to_rotation_1.secondary_axis = 'X'

			#node Set Curve Normal.001
			set_curve_normal_001_2 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeSetCurveNormal")
			set_curve_normal_001_2.name = "Set Curve Normal.001"
			set_curve_normal_001_2.mode = 'MINIMUM_TWIST'
			#Selection
			set_curve_normal_001_2.inputs[1].default_value = True

			#node Store Named Attribute.005
			store_named_attribute_005_2 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_005_2.name = "Store Named Attribute.005"
			store_named_attribute_005_2.data_type = 'INT'
			store_named_attribute_005_2.domain = 'POINT'
			#Selection
			store_named_attribute_005_2.inputs[1].default_value = True
			#Name
			store_named_attribute_005_2.inputs[2].default_value = "tmp_idx"

			#node Index
			index_7 = _mn_utils_style_ribbon_nucleic.nodes.new("GeometryNodeInputIndex")
			index_7.name = "Index"

			#node Reroute
			reroute_22 = _mn_utils_style_ribbon_nucleic.nodes.new("NodeReroute")
			reroute_22.name = "Reroute"
			#node Reroute.001
			reroute_001_15 = _mn_utils_style_ribbon_nucleic.nodes.new("NodeReroute")
			reroute_001_15.name = "Reroute.001"
			#node Group Input.004
			group_input_004_3 = _mn_utils_style_ribbon_nucleic.nodes.new("NodeGroupInput")
			group_input_004_3.name = "Group Input.004"
			group_input_004_3.outputs[0].hide = True
			group_input_004_3.outputs[1].hide = True
			group_input_004_3.outputs[2].hide = True
			group_input_004_3.outputs[3].hide = True
			group_input_004_3.outputs[4].hide = True
			group_input_004_3.outputs[6].hide = True
			group_input_004_3.outputs[7].hide = True
			group_input_004_3.outputs[8].hide = True
			group_input_004_3.outputs[9].hide = True
			group_input_004_3.outputs[10].hide = True
			group_input_004_3.outputs[11].hide = True



			#Set parents
			endpoint_selection_4.parent = frame_006
			combine_xyz_1.parent = frame_005_1
			math_27.parent = frame_005_1
			cylinder.parent = frame_005_1
			value_1.parent = frame_005_1
			group_input_005_1.parent = frame_005_1
			store_named_attribute_006_1.parent = frame_005_1
			transform.parent = frame_005_1
			instance_on_points.parent = frame_005_1
			mesh_to_points.parent = frame_15
			compare_002_8.parent = frame_15
			named_attribute_010_1.parent = frame_15
			store_named_attribute_001_3.parent = frame_005_1
			store_named_attribute_002_3.parent = frame_005_1
			store_named_attribute_003_3.parent = frame_005_1
			group_003_13.parent = frame_15
			points_to_curves_1.parent = frame_15
			named_attribute_003_2.parent = frame_15
			group_004_8.parent = frame_006
			group_006_8.parent = frame_006
			group_011_8.parent = frame_006
			curve_tangent_1.parent = frame_006
			math_001_10.parent = frame_006
			group_007_6.parent = frame_005_1
			axes_to_rotation_1.parent = frame_005_1
			store_named_attribute_005_2.parent = frame_15
			index_7.parent = frame_15
			reroute_22.parent = frame_005_1
			reroute_001_15.parent = frame_005_1

			#Set locations
			frame_15.location = (-3213.76806640625, -105.34455871582031)
			frame_006.location = (-4340.0, -330.0)
			frame_005_1.location = (-3002.0, 255.0)
			group_output_89.location = (-700.0, 200.0)
			endpoint_selection_4.location = (1810.0, 700.0)
			set_position_001_4.location = (-2040.0, 320.0)
			combine_xyz_1.location = (-224.1474609375, -1353.7237548828125)
			math_27.location = (-396.513427734375, -1358.8675537109375)
			cylinder.location = (-567.352783203125, -1144.41748046875)
			value_1.location = (-807.352783203125, -1404.41748046875)
			group_input_005_1.location = (-807.352783203125, -1304.41748046875)
			store_named_attribute_006_1.location = (-399.6494140625, -1142.027099609375)
			group_input_88.location = (-5620.0, -20.0)
			transform.location = (-47.352783203125, -1144.41748046875)
			instance_on_points.location = (302.0, -835.0)
			set_material_1.location = (-1420.0, 20.0)
			join_geometry_001_1.location = (-980.0, 240.0)
			is_nucleic_1.location = (-5440.0, -80.0)
			capture_attribute_002_4.location = (-5240.0, -20.0)
			separate_geometry_002.location = (-5060.0, 40.0)
			group_002_21.location = (-5060.0, -120.0)
			capture_attribute_003.location = (-4880.0, 40.0)
			capture_attribute_004_1.location = (-4380.0, 20.0)
			mesh_to_points.location = (-557.1708984375, 167.0)
			compare_002_8.location = (-566.23193359375, -14.655441284179688)
			named_attribute_010_1.location = (-726.23193359375, -14.655441284179688)
			reroute_005_2.location = (-860.0, -140.0)
			store_named_attribute_4.location = (-2380.0, 160.0)
			store_named_attribute_001_3.location = (100.702880859375, -795.0)
			remove_named_attribute_1.location = (-1260.0, 20.0)
			store_named_attribute_002_3.location = (-99.297119140625, -795.0)
			reroute_014.location = (-2240.0, -620.0)
			group_33.location = (-1860.0, 320.0)
			group_005_9.location = (-1420.0, 240.0)
			group_input_001_14.location = (-1760.0, 80.0)
			reroute_008_1.location = (-1840.0, -140.0)
			store_named_attribute_003_3.location = (-229.649658203125, -1144.41748046875)
			realize_instances_1.location = (-2020.0, -700.0)
			capture_attribute_8.location = (-2180.0, -700.0)
			named_attribute_002_5.location = (-2380.0, -720.0)
			store_named_attribute_004_2.location = (-1860.0, -700.0)
			switch_001_9.location = (-1860.0, -520.0)
			group_input_002_7.location = (-2060.0, -560.0)
			group_003_13.location = (-17.1708984375, 187.0)
			points_to_curves_1.location = (-197.1708984375, 167.0)
			named_attribute_003_2.location = (-197.1708984375, 27.0)
			set_curve_radius_1.location = (-3000.0, 80.0)
			group_004_8.location = (1630.0, 940.0)
			group_006_8.location = (1970.0, 1000.0)
			group_011_8.location = (1808.6024169921875, 1010.1329345703125)
			curve_tangent_1.location = (1650.0, 1000.0)
			math_001_10.location = (1810.0, 860.0)
			group_input_003_4.location = (-2040.0, 180.0)
			group_012_4.location = (-4675.97412109375, -72.46146392822266)
			set_curve_normal_3.location = (-2780.0, 40.0)
			group_007_6.location = (282.0, -1055.0)
			axes_to_rotation_1.location = (102.0, -995.0)
			set_curve_normal_001_2.location = (-2780.0, 180.0)
			store_named_attribute_005_2.location = (-377.431884765625, 171.47378540039062)
			index_7.location = (-386.23193359375, -34.65544128417969)
			reroute_22.location = (-538.0, -1055.0)
			reroute_001_15.location = (-538.0, -1035.0)
			group_input_004_3.location = (-2040.0, -20.0)

			#Set dimensions
			frame_15.width, frame_15.height = 908.800048828125, 418.79998779296875
			frame_006.width, frame_006.height = 540.0, 476.4000244140625
			frame_005_1.width, frame_005_1.height = 1309.60009765625, 781.199951171875
			group_output_89.width, group_output_89.height = 140.0, 100.0
			endpoint_selection_4.width, endpoint_selection_4.height = 140.0, 100.0
			set_position_001_4.width, set_position_001_4.height = 140.0, 100.0
			combine_xyz_1.width, combine_xyz_1.height = 140.0, 100.0
			math_27.width, math_27.height = 140.0, 100.0
			cylinder.width, cylinder.height = 140.0, 100.0
			value_1.width, value_1.height = 140.0, 100.0
			group_input_005_1.width, group_input_005_1.height = 140.0, 100.0
			store_named_attribute_006_1.width, store_named_attribute_006_1.height = 140.0, 100.0
			group_input_88.width, group_input_88.height = 140.0, 100.0
			transform.width, transform.height = 140.0, 100.0
			instance_on_points.width, instance_on_points.height = 140.0, 100.0
			set_material_1.width, set_material_1.height = 140.0, 100.0
			join_geometry_001_1.width, join_geometry_001_1.height = 140.0, 100.0
			is_nucleic_1.width, is_nucleic_1.height = 144.1632843017578, 100.0
			capture_attribute_002_4.width, capture_attribute_002_4.height = 140.0, 100.0
			separate_geometry_002.width, separate_geometry_002.height = 140.0, 100.0
			group_002_21.width, group_002_21.height = 140.0, 100.0
			capture_attribute_003.width, capture_attribute_003.height = 140.0, 100.0
			capture_attribute_004_1.width, capture_attribute_004_1.height = 140.0, 100.0
			mesh_to_points.width, mesh_to_points.height = 140.0, 100.0
			compare_002_8.width, compare_002_8.height = 140.0, 100.0
			named_attribute_010_1.width, named_attribute_010_1.height = 140.0, 100.0
			reroute_005_2.width, reroute_005_2.height = 16.0, 100.0
			store_named_attribute_4.width, store_named_attribute_4.height = 140.0, 100.0
			store_named_attribute_001_3.width, store_named_attribute_001_3.height = 140.0, 100.0
			remove_named_attribute_1.width, remove_named_attribute_1.height = 148.5031280517578, 100.0
			store_named_attribute_002_3.width, store_named_attribute_002_3.height = 140.0, 100.0
			reroute_014.width, reroute_014.height = 16.0, 100.0
			group_33.width, group_33.height = 140.0, 100.0
			group_005_9.width, group_005_9.height = 248.1259765625, 100.0
			group_input_001_14.width, group_input_001_14.height = 140.0, 100.0
			reroute_008_1.width, reroute_008_1.height = 16.0, 100.0
			store_named_attribute_003_3.width, store_named_attribute_003_3.height = 140.0, 100.0
			realize_instances_1.width, realize_instances_1.height = 140.0, 100.0
			capture_attribute_8.width, capture_attribute_8.height = 140.0, 100.0
			named_attribute_002_5.width, named_attribute_002_5.height = 140.0, 100.0
			store_named_attribute_004_2.width, store_named_attribute_004_2.height = 140.0, 100.0
			switch_001_9.width, switch_001_9.height = 140.0, 100.0
			group_input_002_7.width, group_input_002_7.height = 140.0, 100.0
			group_003_13.width, group_003_13.height = 140.0, 100.0
			points_to_curves_1.width, points_to_curves_1.height = 140.0, 100.0
			named_attribute_003_2.width, named_attribute_003_2.height = 140.0, 100.0
			set_curve_radius_1.width, set_curve_radius_1.height = 140.0, 100.0
			group_004_8.width, group_004_8.height = 140.0, 100.0
			group_006_8.width, group_006_8.height = 140.0, 100.0
			group_011_8.width, group_011_8.height = 140.0, 100.0
			curve_tangent_1.width, curve_tangent_1.height = 140.0, 100.0
			math_001_10.width, math_001_10.height = 140.0, 100.0
			group_input_003_4.width, group_input_003_4.height = 140.0, 100.0
			group_012_4.width, group_012_4.height = 212.7861328125, 100.0
			set_curve_normal_3.width, set_curve_normal_3.height = 140.0, 100.0
			group_007_6.width, group_007_6.height = 140.0, 100.0
			axes_to_rotation_1.width, axes_to_rotation_1.height = 140.0, 100.0
			set_curve_normal_001_2.width, set_curve_normal_001_2.height = 140.0, 100.0
			store_named_attribute_005_2.width, store_named_attribute_005_2.height = 140.0, 100.0
			index_7.width, index_7.height = 140.0, 100.0
			reroute_22.width, reroute_22.height = 16.0, 100.0
			reroute_001_15.width, reroute_001_15.height = 16.0, 100.0
			group_input_004_3.width, group_input_004_3.height = 140.0, 100.0

			#initialize _mn_utils_style_ribbon_nucleic links
			#store_named_attribute_003_3.Geometry -> transform.Geometry
			_mn_utils_style_ribbon_nucleic.links.new(store_named_attribute_003_3.outputs[0], transform.inputs[0])
			#combine_xyz_1.Vector -> transform.Translation
			_mn_utils_style_ribbon_nucleic.links.new(combine_xyz_1.outputs[0], transform.inputs[1])
			#value_1.Value -> math_27.Value
			_mn_utils_style_ribbon_nucleic.links.new(value_1.outputs[0], math_27.inputs[0])
			#value_1.Value -> cylinder.Depth
			_mn_utils_style_ribbon_nucleic.links.new(value_1.outputs[0], cylinder.inputs[4])
			#math_27.Value -> combine_xyz_1.Z
			_mn_utils_style_ribbon_nucleic.links.new(math_27.outputs[0], combine_xyz_1.inputs[2])
			#join_geometry_001_1.Geometry -> group_output_89.Geometry
			_mn_utils_style_ribbon_nucleic.links.new(join_geometry_001_1.outputs[0], group_output_89.inputs[0])
			#store_named_attribute_001_3.Geometry -> instance_on_points.Points
			_mn_utils_style_ribbon_nucleic.links.new(store_named_attribute_001_3.outputs[0], instance_on_points.inputs[0])
			#remove_named_attribute_1.Geometry -> join_geometry_001_1.Geometry
			_mn_utils_style_ribbon_nucleic.links.new(remove_named_attribute_1.outputs[0], join_geometry_001_1.inputs[0])
			#group_input_005_1.Base Radius -> cylinder.Radius
			_mn_utils_style_ribbon_nucleic.links.new(group_input_005_1.outputs[9], cylinder.inputs[3])
			#group_input_005_1.Base Resolution -> cylinder.Vertices
			_mn_utils_style_ribbon_nucleic.links.new(group_input_005_1.outputs[10], cylinder.inputs[0])
			#transform.Geometry -> instance_on_points.Instance
			_mn_utils_style_ribbon_nucleic.links.new(transform.outputs[0], instance_on_points.inputs[2])
			#cylinder.Mesh -> store_named_attribute_006_1.Geometry
			_mn_utils_style_ribbon_nucleic.links.new(cylinder.outputs[0], store_named_attribute_006_1.inputs[0])
			#cylinder.UV Map -> store_named_attribute_006_1.Value
			_mn_utils_style_ribbon_nucleic.links.new(cylinder.outputs[4], store_named_attribute_006_1.inputs[3])
			#store_named_attribute_4.Geometry -> set_position_001_4.Geometry
			_mn_utils_style_ribbon_nucleic.links.new(store_named_attribute_4.outputs[0], set_position_001_4.inputs[0])
			#endpoint_selection_4.Selection -> set_position_001_4.Selection
			_mn_utils_style_ribbon_nucleic.links.new(endpoint_selection_4.outputs[0], set_position_001_4.inputs[1])
			#group_input_88.Atoms -> capture_attribute_002_4.Geometry
			_mn_utils_style_ribbon_nucleic.links.new(group_input_88.outputs[0], capture_attribute_002_4.inputs[0])
			#group_input_88.Selection -> is_nucleic_1.And
			_mn_utils_style_ribbon_nucleic.links.new(group_input_88.outputs[1], is_nucleic_1.inputs[0])
			#is_nucleic_1.Selection -> capture_attribute_002_4.Selection
			_mn_utils_style_ribbon_nucleic.links.new(is_nucleic_1.outputs[0], capture_attribute_002_4.inputs[1])
			#capture_attribute_002_4.Geometry -> separate_geometry_002.Geometry
			_mn_utils_style_ribbon_nucleic.links.new(capture_attribute_002_4.outputs[0], separate_geometry_002.inputs[0])
			#separate_geometry_002.Selection -> capture_attribute_003.Geometry
			_mn_utils_style_ribbon_nucleic.links.new(separate_geometry_002.outputs[0], capture_attribute_003.inputs[0])
			#group_002_21.Unique Group ID -> capture_attribute_003.Unique Group ID
			_mn_utils_style_ribbon_nucleic.links.new(group_002_21.outputs[0], capture_attribute_003.inputs[1])
			#capture_attribute_003.Geometry -> capture_attribute_004_1.Geometry
			_mn_utils_style_ribbon_nucleic.links.new(capture_attribute_003.outputs[0], capture_attribute_004_1.inputs[0])
			#group_012_4.base_pivot' -> capture_attribute_004_1.base_pivot
			_mn_utils_style_ribbon_nucleic.links.new(group_012_4.outputs[1], capture_attribute_004_1.inputs[2])
			#group_012_4.base_Z -> capture_attribute_004_1.base_Z
			_mn_utils_style_ribbon_nucleic.links.new(group_012_4.outputs[2], capture_attribute_004_1.inputs[3])
			#group_012_4.base_Y -> capture_attribute_004_1.base_Y
			_mn_utils_style_ribbon_nucleic.links.new(group_012_4.outputs[3], capture_attribute_004_1.inputs[4])
			#capture_attribute_004_1.base_valid -> instance_on_points.Selection
			_mn_utils_style_ribbon_nucleic.links.new(capture_attribute_004_1.outputs[1], instance_on_points.inputs[1])
			#group_012_4.base_valid -> capture_attribute_004_1.base_valid
			_mn_utils_style_ribbon_nucleic.links.new(group_012_4.outputs[0], capture_attribute_004_1.inputs[1])
			#capture_attribute_004_1.Geometry -> mesh_to_points.Mesh
			_mn_utils_style_ribbon_nucleic.links.new(capture_attribute_004_1.outputs[0], mesh_to_points.inputs[0])
			#group_012_4.base_position -> capture_attribute_004_1.base_position
			_mn_utils_style_ribbon_nucleic.links.new(group_012_4.outputs[4], capture_attribute_004_1.inputs[5])
			#named_attribute_010_1.Attribute -> compare_002_8.A
			_mn_utils_style_ribbon_nucleic.links.new(named_attribute_010_1.outputs[0], compare_002_8.inputs[2])
			#compare_002_8.Result -> mesh_to_points.Selection
			_mn_utils_style_ribbon_nucleic.links.new(compare_002_8.outputs[0], mesh_to_points.inputs[1])
			#capture_attribute_004_1.base_position -> mesh_to_points.Position
			_mn_utils_style_ribbon_nucleic.links.new(capture_attribute_004_1.outputs[5], mesh_to_points.inputs[2])
			#set_curve_normal_001_2.Curve -> store_named_attribute_4.Geometry
			_mn_utils_style_ribbon_nucleic.links.new(set_curve_normal_001_2.outputs[0], store_named_attribute_4.inputs[0])
			#store_named_attribute_002_3.Geometry -> store_named_attribute_001_3.Geometry
			_mn_utils_style_ribbon_nucleic.links.new(store_named_attribute_002_3.outputs[0], store_named_attribute_001_3.inputs[0])
			#group_012_4.Base Color -> capture_attribute_004_1.Base Color
			_mn_utils_style_ribbon_nucleic.links.new(group_012_4.outputs[5], capture_attribute_004_1.inputs[6])
			#set_curve_normal_3.Curve -> store_named_attribute_002_3.Geometry
			_mn_utils_style_ribbon_nucleic.links.new(set_curve_normal_3.outputs[0], store_named_attribute_002_3.inputs[0])
			#capture_attribute_004_1.Base Color -> store_named_attribute_002_3.Value
			_mn_utils_style_ribbon_nucleic.links.new(capture_attribute_004_1.outputs[6], store_named_attribute_002_3.inputs[3])
			#instance_on_points.Instances -> reroute_014.Input
			_mn_utils_style_ribbon_nucleic.links.new(instance_on_points.outputs[0], reroute_014.inputs[0])
			#reroute_005_2.Output -> group_output_89.Curve
			_mn_utils_style_ribbon_nucleic.links.new(reroute_005_2.outputs[0], group_output_89.inputs[1])
			#set_position_001_4.Geometry -> group_33.Curve
			_mn_utils_style_ribbon_nucleic.links.new(set_position_001_4.outputs[0], group_33.inputs[0])
			#group_33.Geometry -> group_005_9.Geometry
			_mn_utils_style_ribbon_nucleic.links.new(group_33.outputs[0], group_005_9.inputs[0])
			#group_input_001_14.Blur Color -> group_005_9.Blurred Color
			_mn_utils_style_ribbon_nucleic.links.new(group_input_001_14.outputs[3], group_005_9.inputs[1])
			#store_named_attribute_4.Geometry -> reroute_008_1.Input
			_mn_utils_style_ribbon_nucleic.links.new(store_named_attribute_4.outputs[0], reroute_008_1.inputs[0])
			#group_input_001_14.Backbone Shade Smooth -> group_005_9.Shade Smooth
			_mn_utils_style_ribbon_nucleic.links.new(group_input_001_14.outputs[7], group_005_9.inputs[4])
			#group_input_001_14.Material -> group_005_9.Material
			_mn_utils_style_ribbon_nucleic.links.new(group_input_001_14.outputs[2], group_005_9.inputs[3])
			#set_material_1.Geometry -> remove_named_attribute_1.Geometry
			_mn_utils_style_ribbon_nucleic.links.new(set_material_1.outputs[0], remove_named_attribute_1.inputs[0])
			#group_input_001_14.Material -> set_material_1.Material
			_mn_utils_style_ribbon_nucleic.links.new(group_input_001_14.outputs[2], set_material_1.inputs[2])
			#store_named_attribute_006_1.Geometry -> store_named_attribute_003_3.Geometry
			_mn_utils_style_ribbon_nucleic.links.new(store_named_attribute_006_1.outputs[0], store_named_attribute_003_3.inputs[0])
			#capture_attribute_8.Geometry -> realize_instances_1.Geometry
			_mn_utils_style_ribbon_nucleic.links.new(capture_attribute_8.outputs[0], realize_instances_1.inputs[0])
			#named_attribute_002_5.Attribute -> capture_attribute_8.Attribute
			_mn_utils_style_ribbon_nucleic.links.new(named_attribute_002_5.outputs[0], capture_attribute_8.inputs[1])
			#realize_instances_1.Geometry -> store_named_attribute_004_2.Geometry
			_mn_utils_style_ribbon_nucleic.links.new(realize_instances_1.outputs[0], store_named_attribute_004_2.inputs[0])
			#capture_attribute_8.Attribute -> store_named_attribute_004_2.Value
			_mn_utils_style_ribbon_nucleic.links.new(capture_attribute_8.outputs[1], store_named_attribute_004_2.inputs[3])
			#store_named_attribute_004_2.Geometry -> switch_001_9.True
			_mn_utils_style_ribbon_nucleic.links.new(store_named_attribute_004_2.outputs[0], switch_001_9.inputs[2])
			#group_input_002_7.Realise Bases -> switch_001_9.Switch
			_mn_utils_style_ribbon_nucleic.links.new(group_input_002_7.outputs[8], switch_001_9.inputs[0])
			#reroute_014.Output -> capture_attribute_8.Geometry
			_mn_utils_style_ribbon_nucleic.links.new(reroute_014.outputs[0], capture_attribute_8.inputs[0])
			#reroute_014.Output -> switch_001_9.False
			_mn_utils_style_ribbon_nucleic.links.new(reroute_014.outputs[0], switch_001_9.inputs[1])
			#switch_001_9.Output -> set_material_1.Geometry
			_mn_utils_style_ribbon_nucleic.links.new(switch_001_9.outputs[0], set_material_1.inputs[0])
			#reroute_008_1.Output -> reroute_005_2.Input
			_mn_utils_style_ribbon_nucleic.links.new(reroute_008_1.outputs[0], reroute_005_2.inputs[0])
			#points_to_curves_1.Curves -> group_003_13.Curve
			_mn_utils_style_ribbon_nucleic.links.new(points_to_curves_1.outputs[0], group_003_13.inputs[0])
			#store_named_attribute_005_2.Geometry -> points_to_curves_1.Points
			_mn_utils_style_ribbon_nucleic.links.new(store_named_attribute_005_2.outputs[0], points_to_curves_1.inputs[0])
			#named_attribute_003_2.Attribute -> points_to_curves_1.Curve Group ID
			_mn_utils_style_ribbon_nucleic.links.new(named_attribute_003_2.outputs[0], points_to_curves_1.inputs[1])
			#group_input_88.Backbone Radius -> capture_attribute_002_4.Backbone Radius
			_mn_utils_style_ribbon_nucleic.links.new(group_input_88.outputs[6], capture_attribute_002_4.inputs[2])
			#capture_attribute_002_4.Backbone Radius -> set_curve_radius_1.Radius
			_mn_utils_style_ribbon_nucleic.links.new(capture_attribute_002_4.outputs[2], set_curve_radius_1.inputs[2])
			#group_004_8.Value -> group_011_8.Offset
			_mn_utils_style_ribbon_nucleic.links.new(group_004_8.outputs[0], group_011_8.inputs[2])
			#curve_tangent_1.Tangent -> group_011_8.Vector
			_mn_utils_style_ribbon_nucleic.links.new(curve_tangent_1.outputs[0], group_011_8.inputs[1])
			#group_011_8.Value -> group_006_8.Vector
			_mn_utils_style_ribbon_nucleic.links.new(group_011_8.outputs[0], group_006_8.inputs[0])
			#group_006_8.Vector -> set_position_001_4.Offset
			_mn_utils_style_ribbon_nucleic.links.new(group_006_8.outputs[0], set_position_001_4.inputs[3])
			#group_004_8.Value -> math_001_10.Value
			_mn_utils_style_ribbon_nucleic.links.new(group_004_8.outputs[0], math_001_10.inputs[0])
			#math_001_10.Value -> group_006_8.Angstrom
			_mn_utils_style_ribbon_nucleic.links.new(math_001_10.outputs[0], group_006_8.inputs[2])
			#store_named_attribute_4.Geometry -> group_005_9.Color Source
			_mn_utils_style_ribbon_nucleic.links.new(store_named_attribute_4.outputs[0], group_005_9.inputs[2])
			#capture_attribute_002_4.Selection -> separate_geometry_002.Selection
			_mn_utils_style_ribbon_nucleic.links.new(capture_attribute_002_4.outputs[1], separate_geometry_002.inputs[1])
			#capture_attribute_003.Unique Group ID -> group_012_4.Input
			_mn_utils_style_ribbon_nucleic.links.new(capture_attribute_003.outputs[1], group_012_4.inputs[0])
			#group_007_6.Vector -> instance_on_points.Scale
			_mn_utils_style_ribbon_nucleic.links.new(group_007_6.outputs[0], instance_on_points.inputs[6])
			#capture_attribute_004_1.base_Y -> set_curve_normal_3.Normal
			_mn_utils_style_ribbon_nucleic.links.new(capture_attribute_004_1.outputs[4], set_curve_normal_3.inputs[2])
			#reroute_22.Output -> axes_to_rotation_1.Secondary Axis
			_mn_utils_style_ribbon_nucleic.links.new(reroute_22.outputs[0], axes_to_rotation_1.inputs[1])
			#reroute_001_15.Output -> axes_to_rotation_1.Primary Axis
			_mn_utils_style_ribbon_nucleic.links.new(reroute_001_15.outputs[0], axes_to_rotation_1.inputs[0])
			#axes_to_rotation_1.Rotation -> instance_on_points.Rotation
			_mn_utils_style_ribbon_nucleic.links.new(axes_to_rotation_1.outputs[0], instance_on_points.inputs[5])
			#set_curve_radius_1.Curve -> set_curve_normal_001_2.Curve
			_mn_utils_style_ribbon_nucleic.links.new(set_curve_radius_1.outputs[0], set_curve_normal_001_2.inputs[0])
			#group_003_13.Curve -> set_curve_radius_1.Curve
			_mn_utils_style_ribbon_nucleic.links.new(group_003_13.outputs[0], set_curve_radius_1.inputs[0])
			#set_curve_radius_1.Curve -> set_curve_normal_3.Curve
			_mn_utils_style_ribbon_nucleic.links.new(set_curve_radius_1.outputs[0], set_curve_normal_3.inputs[0])
			#mesh_to_points.Points -> store_named_attribute_005_2.Geometry
			_mn_utils_style_ribbon_nucleic.links.new(mesh_to_points.outputs[0], store_named_attribute_005_2.inputs[0])
			#index_7.Index -> store_named_attribute_005_2.Value
			_mn_utils_style_ribbon_nucleic.links.new(index_7.outputs[0], store_named_attribute_005_2.inputs[3])
			#capture_attribute_004_1.base_Y -> reroute_22.Input
			_mn_utils_style_ribbon_nucleic.links.new(capture_attribute_004_1.outputs[4], reroute_22.inputs[0])
			#capture_attribute_004_1.base_Z -> reroute_001_15.Input
			_mn_utils_style_ribbon_nucleic.links.new(capture_attribute_004_1.outputs[3], reroute_001_15.inputs[0])
			#group_input_004_3.Backbone Resolution -> group_33.Profile Resolution
			_mn_utils_style_ribbon_nucleic.links.new(group_input_004_3.outputs[5], group_33.inputs[6])
			#group_input_003_4.Backbone Subdivisions -> group_33.Subdivisions
			_mn_utils_style_ribbon_nucleic.links.new(group_input_003_4.outputs[4], group_33.inputs[1])
			#group_005_9.Geometry -> join_geometry_001_1.Geometry
			_mn_utils_style_ribbon_nucleic.links.new(group_005_9.outputs[0], join_geometry_001_1.inputs[0])
			return _mn_utils_style_ribbon_nucleic

		_mn_utils_style_ribbon_nucleic = _mn_utils_style_ribbon_nucleic_node_group()

		#initialize style_cartoon node group
		def style_cartoon_node_group():
			style_cartoon = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Style Cartoon")

			style_cartoon.color_tag = 'GEOMETRY'
			style_cartoon.description = ""

			style_cartoon.is_modifier = True

			#style_cartoon interface
			#Socket Geometry
			geometry_socket_17 = style_cartoon.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			geometry_socket_17.attribute_domain = 'POINT'
			geometry_socket_17.description = "The resulting cartoon geometry, calculated from the given atoms, selection and parameters"

			#Socket Atoms
			atoms_socket_11 = style_cartoon.interface.new_socket(name = "Atoms", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			atoms_socket_11.attribute_domain = 'POINT'
			atoms_socket_11.description = "Atomic geometry that contains vertices and edges"

			#Socket Selection
			selection_socket_14 = style_cartoon.interface.new_socket(name = "Selection", in_out='INPUT', socket_type = 'NodeSocketBool')
			selection_socket_14.attribute_domain = 'POINT'
			selection_socket_14.hide_value = True
			selection_socket_14.description = "Selection of atoms to apply this style to"

			#Socket Quality
			quality_socket = style_cartoon.interface.new_socket(name = "Quality", in_out='INPUT', socket_type = 'NodeSocketInt')
			quality_socket.subtype = 'NONE'
			quality_socket.default_value = 2
			quality_socket.min_value = 0
			quality_socket.max_value = 6
			quality_socket.attribute_domain = 'POINT'
			quality_socket.description = "Number of subdivisions,  ‘quality’ of the cartoon."

			#Panel Cartoon
			cartoon_panel = style_cartoon.interface.new_panel("Cartoon", default_closed=True)
			#Socket DSSP
			dssp_socket = style_cartoon.interface.new_socket(name = "DSSP", in_out='INPUT', socket_type = 'NodeSocketBool', parent = cartoon_panel)
			dssp_socket.attribute_domain = 'POINT'
			dssp_socket.description = "Use the DSSP algorithm to compute the `sec_struct` attribute"

			#Socket Cylinders
			cylinders_socket = style_cartoon.interface.new_socket(name = "Cylinders", in_out='INPUT', socket_type = 'NodeSocketBool', parent = cartoon_panel)
			cylinders_socket.attribute_domain = 'POINT'
			cylinders_socket.description = "Use cylinders for helices instead of ribbons"

			#Socket Arrows
			arrows_socket_1 = style_cartoon.interface.new_socket(name = "Arrows", in_out='INPUT', socket_type = 'NodeSocketBool', parent = cartoon_panel)
			arrows_socket_1.attribute_domain = 'POINT'
			arrows_socket_1.description = "User arrows for sheets"

			#Socket Rounded
			rounded_socket_2 = style_cartoon.interface.new_socket(name = "Rounded", in_out='INPUT', socket_type = 'NodeSocketBool', parent = cartoon_panel)
			rounded_socket_2.attribute_domain = 'POINT'
			rounded_socket_2.description = "Create rounded sheets and helices"

			#Socket Thickness
			thickness_socket_3 = style_cartoon.interface.new_socket(name = "Thickness", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = cartoon_panel)
			thickness_socket_3.subtype = 'NONE'
			thickness_socket_3.default_value = 0.6000000238418579
			thickness_socket_3.min_value = 0.0
			thickness_socket_3.max_value = 3.4028234663852886e+38
			thickness_socket_3.attribute_domain = 'POINT'
			thickness_socket_3.description = "Thickness for the sheets and helices"

			#Socket Width
			width_socket_3 = style_cartoon.interface.new_socket(name = "Width", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = cartoon_panel)
			width_socket_3.subtype = 'NONE'
			width_socket_3.default_value = 2.200000047683716
			width_socket_3.min_value = 0.0
			width_socket_3.max_value = 3.4028234663852886e+38
			width_socket_3.attribute_domain = 'POINT'
			width_socket_3.description = "Width for the sheets and helices"

			#Socket Loop Radius
			loop_radius_socket_1 = style_cartoon.interface.new_socket(name = "Loop Radius", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = cartoon_panel)
			loop_radius_socket_1.subtype = 'NONE'
			loop_radius_socket_1.default_value = 0.4000000059604645
			loop_radius_socket_1.min_value = 0.0
			loop_radius_socket_1.max_value = 3.0
			loop_radius_socket_1.attribute_domain = 'POINT'
			loop_radius_socket_1.description = "Radius of the loops for unstructure regions"

			#Socket Smoothing
			smoothing_socket = style_cartoon.interface.new_socket(name = "Smoothing", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = cartoon_panel)
			smoothing_socket.subtype = 'FACTOR'
			smoothing_socket.default_value = 0.5
			smoothing_socket.min_value = 0.0
			smoothing_socket.max_value = 1.0
			smoothing_socket.attribute_domain = 'POINT'
			smoothing_socket.description = "Smoothing to apply to sheets"


			#Panel Material
			material_panel = style_cartoon.interface.new_panel("Material", default_closed=True)
			#Socket Color Blur
			color_blur_socket = style_cartoon.interface.new_socket(name = "Color Blur", in_out='INPUT', socket_type = 'NodeSocketBool', parent = material_panel)
			color_blur_socket.attribute_domain = 'POINT'
			color_blur_socket.description = "Smoothly interpolate between the different color values, or have each bit of geometry be cleanly one color or another"

			#Socket Shade Smooth
			shade_smooth_socket_2 = style_cartoon.interface.new_socket(name = "Shade Smooth", in_out='INPUT', socket_type = 'NodeSocketBool', parent = material_panel)
			shade_smooth_socket_2.attribute_domain = 'POINT'
			shade_smooth_socket_2.description = "Apply smooth shading to the created geometry"

			#Socket Material
			material_socket_3 = style_cartoon.interface.new_socket(name = "Material", in_out='INPUT', socket_type = 'NodeSocketMaterial', parent = material_panel)
			material_socket_3.attribute_domain = 'POINT'
			material_socket_3.description = "Material to apply to the resulting geometry"



			#initialize style_cartoon nodes
			#node Group Output
			group_output_90 = style_cartoon.nodes.new("NodeGroupOutput")
			group_output_90.name = "Group Output"
			group_output_90.is_active_output = True

			#node Group Input
			group_input_89 = style_cartoon.nodes.new("NodeGroupInput")
			group_input_89.name = "Group Input"
			group_input_89.outputs[3].hide = True

			#node Group.067
			group_067 = style_cartoon.nodes.new("GeometryNodeGroup")
			group_067.name = "Group.067"
			group_067.node_tree = _mn_utils_style_cartoon
			#Input_69
			group_067.inputs[8].default_value = True
			#Input_86
			group_067.inputs[15].default_value = True
			#Input_122
			group_067.inputs[18].default_value = False
			#Input_80
			group_067.inputs[19].default_value = 1.309999942779541
			#Input_81
			group_067.inputs[20].default_value = 1.0299999713897705
			#Input_87
			group_067.inputs[21].default_value = 0.0

			#node Math
			math_28 = style_cartoon.nodes.new("ShaderNodeMath")
			math_28.name = "Math"
			math_28.operation = 'MULTIPLY'
			math_28.use_clamp = False
			#Value_001
			math_28.inputs[1].default_value = 3.0

			#node Math.002
			math_002_8 = style_cartoon.nodes.new("ShaderNodeMath")
			math_002_8.name = "Math.002"
			math_002_8.operation = 'MULTIPLY'
			math_002_8.use_clamp = False
			#Value_001
			math_002_8.inputs[1].default_value = 3.0

			#node Switch
			switch_18 = style_cartoon.nodes.new("GeometryNodeSwitch")
			switch_18.name = "Switch"
			switch_18.input_type = 'INT'
			#False
			switch_18.inputs[1].default_value = 4

			#node Math.001
			math_001_11 = style_cartoon.nodes.new("ShaderNodeMath")
			math_001_11.name = "Math.001"
			math_001_11.operation = 'MULTIPLY'
			math_001_11.use_clamp = False
			#Value_001
			math_001_11.inputs[1].default_value = 5.0

			#node Reroute
			reroute_23 = style_cartoon.nodes.new("NodeReroute")
			reroute_23.name = "Reroute"
			#node Store Named Attribute
			store_named_attribute_5 = style_cartoon.nodes.new("GeometryNodeStoreNamedAttribute")
			store_named_attribute_5.name = "Store Named Attribute"
			store_named_attribute_5.data_type = 'INT'
			store_named_attribute_5.domain = 'POINT'

			#node Named Attribute
			named_attribute_10 = style_cartoon.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_10.name = "Named Attribute"
			named_attribute_10.data_type = 'INT'

			#node String
			string = style_cartoon.nodes.new("FunctionNodeInputString")
			string.name = "String"
			string.string = "sec_struct"

			#node Boolean Math
			boolean_math_19 = style_cartoon.nodes.new("FunctionNodeBooleanMath")
			boolean_math_19.name = "Boolean Math"
			boolean_math_19.operation = 'NOT'

			#node Select Peptide
			select_peptide = style_cartoon.nodes.new("GeometryNodeGroup")
			select_peptide.label = "Select Peptide"
			select_peptide.name = "Select Peptide"
			select_peptide.node_tree = is_peptide
			#Socket_1
			select_peptide.inputs[0].default_value = True
			#Socket_3
			select_peptide.inputs[1].default_value = False

			#node Switch.002
			switch_002_5 = style_cartoon.nodes.new("GeometryNodeSwitch")
			switch_002_5.name = "Switch.002"
			switch_002_5.input_type = 'INT'
			#False
			switch_002_5.inputs[1].default_value = 0
			#True
			switch_002_5.inputs[2].default_value = 3

			#node Group
			group_34 = style_cartoon.nodes.new("GeometryNodeGroup")
			group_34.name = "Group"
			group_34.node_tree = topology_dssp
			#Socket_6
			group_34.inputs[1].default_value = True

			#node Switch.001
			switch_001_10 = style_cartoon.nodes.new("GeometryNodeSwitch")
			switch_001_10.name = "Switch.001"
			switch_001_10.input_type = 'GEOMETRY'

			#node Group Input.001
			group_input_001_15 = style_cartoon.nodes.new("NodeGroupInput")
			group_input_001_15.name = "Group Input.001"
			group_input_001_15.outputs[0].hide = True
			group_input_001_15.outputs[1].hide = True
			group_input_001_15.outputs[2].hide = True
			group_input_001_15.outputs[4].hide = True
			group_input_001_15.outputs[5].hide = True
			group_input_001_15.outputs[6].hide = True
			group_input_001_15.outputs[7].hide = True
			group_input_001_15.outputs[8].hide = True
			group_input_001_15.outputs[9].hide = True
			group_input_001_15.outputs[10].hide = True
			group_input_001_15.outputs[11].hide = True
			group_input_001_15.outputs[12].hide = True
			group_input_001_15.outputs[13].hide = True
			group_input_001_15.outputs[14].hide = True

			#node Frame
			frame_16 = style_cartoon.nodes.new("NodeFrame")
			frame_16.label = "If no sec_struct, assign ribbon to peptide"
			frame_16.name = "Frame"
			frame_16.label_size = 20
			frame_16.shrink = True

			#node Frame.001
			frame_001_11 = style_cartoon.nodes.new("NodeFrame")
			frame_001_11.label = "Manually compute sec_struct"
			frame_001_11.name = "Frame.001"
			frame_001_11.label_size = 20
			frame_001_11.shrink = True

			#node Reroute.001
			reroute_001_16 = style_cartoon.nodes.new("NodeReroute")
			reroute_001_16.name = "Reroute.001"
			#node Reroute.002
			reroute_002_11 = style_cartoon.nodes.new("NodeReroute")
			reroute_002_11.name = "Reroute.002"
			#node Group.001
			group_001_23 = style_cartoon.nodes.new("GeometryNodeGroup")
			group_001_23.name = "Group.001"
			group_001_23.node_tree = separate_polymers

			#node Group.068
			group_068 = style_cartoon.nodes.new("GeometryNodeGroup")
			group_068.name = "Group.068"
			group_068.node_tree = _mn_utils_style_ribbon_nucleic
			#Socket_4
			group_068.inputs[8].default_value = True
			#Input_28
			group_068.inputs[9].default_value = 0.25999999046325684
			#Input_29
			group_068.inputs[10].default_value = 4

			#node Group Input.002
			group_input_002_8 = style_cartoon.nodes.new("NodeGroupInput")
			group_input_002_8.name = "Group Input.002"
			group_input_002_8.outputs[0].hide = True
			group_input_002_8.outputs[3].hide = True
			group_input_002_8.outputs[4].hide = True
			group_input_002_8.outputs[5].hide = True
			group_input_002_8.outputs[6].hide = True
			group_input_002_8.outputs[7].hide = True
			group_input_002_8.outputs[8].hide = True
			group_input_002_8.outputs[10].hide = True
			group_input_002_8.outputs[14].hide = True

			#node Join Geometry
			join_geometry_1 = style_cartoon.nodes.new("GeometryNodeJoinGeometry")
			join_geometry_1.name = "Join Geometry"

			#node Math.003
			math_003_6 = style_cartoon.nodes.new("ShaderNodeMath")
			math_003_6.name = "Math.003"
			math_003_6.operation = 'MULTIPLY'
			math_003_6.use_clamp = False
			#Value_001
			math_003_6.inputs[1].default_value = 2.0

			#node Math.004
			math_004_2 = style_cartoon.nodes.new("ShaderNodeMath")
			math_004_2.name = "Math.004"
			math_004_2.operation = 'MULTIPLY'
			math_004_2.use_clamp = False
			#Value_001
			math_004_2.inputs[1].default_value = 4.0

			#node Math.005
			math_005_2 = style_cartoon.nodes.new("ShaderNodeMath")
			math_005_2.name = "Math.005"
			math_005_2.operation = 'MULTIPLY'
			math_005_2.use_clamp = False
			#Value_001
			math_005_2.inputs[1].default_value = 3.0

			#node Reroute.003
			reroute_003_11 = style_cartoon.nodes.new("NodeReroute")
			reroute_003_11.name = "Reroute.003"
			#node Domain Size
			domain_size_1 = style_cartoon.nodes.new("GeometryNodeAttributeDomainSize")
			domain_size_1.name = "Domain Size"
			domain_size_1.component = 'MESH'
			domain_size_1.outputs[1].hide = True
			domain_size_1.outputs[2].hide = True
			domain_size_1.outputs[3].hide = True
			domain_size_1.outputs[4].hide = True
			domain_size_1.outputs[5].hide = True
			domain_size_1.outputs[6].hide = True

			#node Compare
			compare_16 = style_cartoon.nodes.new("FunctionNodeCompare")
			compare_16.name = "Compare"
			compare_16.data_type = 'INT'
			compare_16.mode = 'ELEMENT'
			compare_16.operation = 'EQUAL'
			#B_INT
			compare_16.inputs[3].default_value = 0

			#node Switch.003
			switch_003_1 = style_cartoon.nodes.new("GeometryNodeSwitch")
			switch_003_1.name = "Switch.003"
			switch_003_1.input_type = 'GEOMETRY'

			#node Capture Attribute.001
			capture_attribute_001_4 = style_cartoon.nodes.new("GeometryNodeCaptureAttribute")
			capture_attribute_001_4.name = "Capture Attribute.001"
			capture_attribute_001_4.active_index = 0
			capture_attribute_001_4.capture_items.clear()
			capture_attribute_001_4.domain = 'POINT'



			#Set parents
			store_named_attribute_5.parent = frame_16
			named_attribute_10.parent = frame_16
			string.parent = frame_16
			boolean_math_19.parent = frame_16
			select_peptide.parent = frame_16
			switch_002_5.parent = frame_16
			group_34.parent = frame_001_11
			switch_001_10.parent = frame_001_11
			group_input_001_15.parent = frame_001_11

			#Set locations
			group_output_90.location = (1180.0, 360.0)
			group_input_89.location = (-895.9766845703125, 240.0)
			group_067.location = (380.0, 420.0)
			math_28.location = (-60.0, -20.0)
			math_002_8.location = (-60.0, 320.0)
			switch_18.location = (120.0, 175.53955078125)
			math_001_11.location = (-60.0, 140.0)
			reroute_23.location = (-140.0, -60.0)
			store_named_attribute_5.location = (-60.0, 640.0)
			named_attribute_10.location = (-380.0, 640.0)
			string.location = (-580.0, 540.0)
			boolean_math_19.location = (-220.0, 640.0)
			select_peptide.location = (-380.0, 480.0)
			switch_002_5.location = (-220.0, 480.0)
			group_34.location = (240.0, 480.0)
			switch_001_10.location = (240.0, 640.0)
			group_input_001_15.location = (240.0, 720.0)
			frame_16.location = (-70.0, 140.0)
			frame_001_11.location = (-90.0, 60.0)
			reroute_001_16.location = (-420.0, 380.0)
			reroute_002_11.location = (40.0, 380.0)
			group_001_23.location = (-619.9998779296875, 380.0)
			group_068.location = (380.0000305175781, -520.0)
			group_input_002_8.location = (-220.00001525878906, -580.0)
			join_geometry_1.location = (1000.0, 360.0)
			math_003_6.location = (159.99998474121094, -600.0)
			math_004_2.location = (159.99998474121094, -920.0)
			math_005_2.location = (159.99998474121094, -760.0)
			reroute_003_11.location = (100.0, -700.0)
			domain_size_1.location = (480.0, 560.0)
			compare_16.location = (640.0, 560.0)
			switch_003_1.location = (820.0, 480.0)
			capture_attribute_001_4.location = (-5949.44482421875, 2146.60888671875)

			#Set dimensions
			group_output_90.width, group_output_90.height = 140.0, 100.0
			group_input_89.width, group_input_89.height = 131.2183837890625, 100.0
			group_067.width, group_067.height = 216.97686767578125, 100.0
			math_28.width, math_28.height = 140.0, 100.0
			math_002_8.width, math_002_8.height = 140.0, 100.0
			switch_18.width, switch_18.height = 140.0, 100.0
			math_001_11.width, math_001_11.height = 140.0, 100.0
			reroute_23.width, reroute_23.height = 16.0, 100.0
			store_named_attribute_5.width, store_named_attribute_5.height = 140.0, 100.0
			named_attribute_10.width, named_attribute_10.height = 140.0, 100.0
			string.width, string.height = 140.0, 100.0
			boolean_math_19.width, boolean_math_19.height = 140.0, 100.0
			select_peptide.width, select_peptide.height = 130.07904052734375, 100.0
			switch_002_5.width, switch_002_5.height = 140.0, 100.0
			group_34.width, group_34.height = 140.0, 100.0
			switch_001_10.width, switch_001_10.height = 140.0, 100.0
			group_input_001_15.width, group_input_001_15.height = 140.0, 100.0
			frame_16.width, frame_16.height = 720.0, 374.0
			frame_001_11.width, frame_001_11.height = 200.0, 430.79998779296875
			reroute_001_16.width, reroute_001_16.height = 16.0, 100.0
			reroute_002_11.width, reroute_002_11.height = 16.0, 100.0
			group_001_23.width, group_001_23.height = 140.0, 100.0
			group_068.width, group_068.height = 216.97686767578125, 100.0
			group_input_002_8.width, group_input_002_8.height = 131.2183837890625, 100.0
			join_geometry_1.width, join_geometry_1.height = 140.0, 100.0
			math_003_6.width, math_003_6.height = 140.0, 100.0
			math_004_2.width, math_004_2.height = 140.0, 100.0
			math_005_2.width, math_005_2.height = 140.0, 100.0
			reroute_003_11.width, reroute_003_11.height = 16.0, 100.0
			domain_size_1.width, domain_size_1.height = 140.0, 100.0
			compare_16.width, compare_16.height = 140.0, 100.0
			switch_003_1.width, switch_003_1.height = 140.0, 100.0
			capture_attribute_001_4.width, capture_attribute_001_4.height = 140.0, 100.0

			#initialize style_cartoon links
			#group_input_89.Selection -> group_067.Selection
			style_cartoon.links.new(group_input_89.outputs[1], group_067.inputs[1])
			#group_input_89.Shade Smooth -> group_067.Shade Smooth
			style_cartoon.links.new(group_input_89.outputs[12], group_067.inputs[2])
			#group_input_89.Color Blur -> group_067.Interpolate Color
			style_cartoon.links.new(group_input_89.outputs[11], group_067.inputs[3])
			#group_input_89.Material -> group_067.Material
			style_cartoon.links.new(group_input_89.outputs[13], group_067.inputs[4])
			#group_input_89.Thickness -> group_067.Sheet Thickness
			style_cartoon.links.new(group_input_89.outputs[7], group_067.inputs[22])
			#group_input_89.Width -> group_067.Sheet Width
			style_cartoon.links.new(group_input_89.outputs[8], group_067.inputs[23])
			#group_input_89.Smoothing -> group_067.Sheet Smoothing
			style_cartoon.links.new(group_input_89.outputs[10], group_067.inputs[24])
			#group_input_89.Loop Radius -> group_067.Loop Radius
			style_cartoon.links.new(group_input_89.outputs[9], group_067.inputs[26])
			#group_input_89.Rounded -> group_067.Arrows Sharp
			style_cartoon.links.new(group_input_89.outputs[6], group_067.inputs[17])
			#group_input_89.Cylinders -> group_067.As Cylinders
			style_cartoon.links.new(group_input_89.outputs[4], group_067.inputs[7])
			#reroute_23.Output -> math_28.Value
			style_cartoon.links.new(reroute_23.outputs[0], math_28.inputs[0])
			#math_28.Value -> group_067.Cylinder Subdivisions
			style_cartoon.links.new(math_28.outputs[0], group_067.inputs[11])
			#math_28.Value -> group_067.Loop Subdivisions
			style_cartoon.links.new(math_28.outputs[0], group_067.inputs[27])
			#math_28.Value -> group_067.Sheet Subdivision
			style_cartoon.links.new(math_28.outputs[0], group_067.inputs[25])
			#math_28.Value -> group_067.Helix Subdivisions
			style_cartoon.links.new(math_28.outputs[0], group_067.inputs[14])
			#group_input_89.Arrows -> group_067.As Arrows
			style_cartoon.links.new(group_input_89.outputs[5], group_067.inputs[16])
			#group_input_89.Quality -> math_002_8.Value
			style_cartoon.links.new(group_input_89.outputs[2], math_002_8.inputs[0])
			#group_input_89.Rounded -> switch_18.Switch
			style_cartoon.links.new(group_input_89.outputs[6], switch_18.inputs[0])
			#math_002_8.Value -> switch_18.True
			style_cartoon.links.new(math_002_8.outputs[0], switch_18.inputs[2])
			#switch_18.Output -> group_067.Profile Resolution
			style_cartoon.links.new(switch_18.outputs[0], group_067.inputs[6])
			#group_input_89.Width -> group_067.Helix Width
			style_cartoon.links.new(group_input_89.outputs[8], group_067.inputs[13])
			#group_input_89.Thickness -> group_067.Helix Thickness
			style_cartoon.links.new(group_input_89.outputs[7], group_067.inputs[12])
			#math_002_8.Value -> group_067.Loop Resolution
			style_cartoon.links.new(math_002_8.outputs[0], group_067.inputs[28])
			#group_input_89.Width -> group_067.Cylinder Radius
			style_cartoon.links.new(group_input_89.outputs[8], group_067.inputs[9])
			#reroute_23.Output -> math_001_11.Value
			style_cartoon.links.new(reroute_23.outputs[0], math_001_11.inputs[0])
			#group_input_89.Quality -> reroute_23.Input
			style_cartoon.links.new(group_input_89.outputs[2], reroute_23.inputs[0])
			#math_001_11.Value -> group_067.Cylinder Resolution
			style_cartoon.links.new(math_001_11.outputs[0], group_067.inputs[10])
			#reroute_001_16.Output -> store_named_attribute_5.Geometry
			style_cartoon.links.new(reroute_001_16.outputs[0], store_named_attribute_5.inputs[0])
			#string.String -> named_attribute_10.Name
			style_cartoon.links.new(string.outputs[0], named_attribute_10.inputs[0])
			#string.String -> store_named_attribute_5.Name
			style_cartoon.links.new(string.outputs[0], store_named_attribute_5.inputs[2])
			#named_attribute_10.Exists -> boolean_math_19.Boolean
			style_cartoon.links.new(named_attribute_10.outputs[1], boolean_math_19.inputs[0])
			#boolean_math_19.Boolean -> store_named_attribute_5.Selection
			style_cartoon.links.new(boolean_math_19.outputs[0], store_named_attribute_5.inputs[1])
			#select_peptide.Selection -> switch_002_5.Switch
			style_cartoon.links.new(select_peptide.outputs[0], switch_002_5.inputs[0])
			#switch_002_5.Output -> store_named_attribute_5.Value
			style_cartoon.links.new(switch_002_5.outputs[0], store_named_attribute_5.inputs[3])
			#reroute_002_11.Output -> group_34.Atoms
			style_cartoon.links.new(reroute_002_11.outputs[0], group_34.inputs[0])
			#group_34.Atoms -> switch_001_10.True
			style_cartoon.links.new(group_34.outputs[0], switch_001_10.inputs[2])
			#store_named_attribute_5.Geometry -> switch_001_10.False
			style_cartoon.links.new(store_named_attribute_5.outputs[0], switch_001_10.inputs[1])
			#switch_001_10.Output -> group_067.Atoms
			style_cartoon.links.new(switch_001_10.outputs[0], group_067.inputs[0])
			#group_input_001_15.DSSP -> switch_001_10.Switch
			style_cartoon.links.new(group_input_001_15.outputs[3], switch_001_10.inputs[0])
			#group_001_23.Peptide -> reroute_001_16.Input
			style_cartoon.links.new(group_001_23.outputs[0], reroute_001_16.inputs[0])
			#reroute_001_16.Output -> reroute_002_11.Input
			style_cartoon.links.new(reroute_001_16.outputs[0], reroute_002_11.inputs[0])
			#group_input_89.Atoms -> group_001_23.Atoms
			style_cartoon.links.new(group_input_89.outputs[0], group_001_23.inputs[0])
			#group_068.Geometry -> join_geometry_1.Geometry
			style_cartoon.links.new(group_068.outputs[0], join_geometry_1.inputs[0])
			#join_geometry_1.Geometry -> group_output_90.Geometry
			style_cartoon.links.new(join_geometry_1.outputs[0], group_output_90.inputs[0])
			#group_001_23.Nucleic -> group_068.Atoms
			style_cartoon.links.new(group_001_23.outputs[1], group_068.inputs[0])
			#group_input_002_8.Material -> group_068.Material
			style_cartoon.links.new(group_input_002_8.outputs[13], group_068.inputs[2])
			#group_input_002_8.Color Blur -> group_068.Blur Color
			style_cartoon.links.new(group_input_002_8.outputs[11], group_068.inputs[3])
			#reroute_003_11.Output -> math_003_6.Value
			style_cartoon.links.new(reroute_003_11.outputs[0], math_003_6.inputs[0])
			#math_003_6.Value -> group_068.Backbone Subdivisions
			style_cartoon.links.new(math_003_6.outputs[0], group_068.inputs[4])
			#reroute_003_11.Output -> math_004_2.Value
			style_cartoon.links.new(reroute_003_11.outputs[0], math_004_2.inputs[0])
			#math_004_2.Value -> group_068.Backbone Resolution
			style_cartoon.links.new(math_004_2.outputs[0], group_068.inputs[5])
			#group_input_002_8.Shade Smooth -> group_068.Backbone Shade Smooth
			style_cartoon.links.new(group_input_002_8.outputs[12], group_068.inputs[7])
			#group_input_002_8.Selection -> group_068.Selection
			style_cartoon.links.new(group_input_002_8.outputs[1], group_068.inputs[1])
			#group_input_002_8.Loop Radius -> math_005_2.Value
			style_cartoon.links.new(group_input_002_8.outputs[9], math_005_2.inputs[0])
			#math_005_2.Value -> group_068.Backbone Radius
			style_cartoon.links.new(math_005_2.outputs[0], group_068.inputs[6])
			#group_input_002_8.Quality -> reroute_003_11.Input
			style_cartoon.links.new(group_input_002_8.outputs[2], reroute_003_11.inputs[0])
			#domain_size_1.Point Count -> compare_16.A
			style_cartoon.links.new(domain_size_1.outputs[0], compare_16.inputs[2])
			#group_067.Cartoon Mesh -> switch_003_1.False
			style_cartoon.links.new(group_067.outputs[0], switch_003_1.inputs[1])
			#compare_16.Result -> switch_003_1.Switch
			style_cartoon.links.new(compare_16.outputs[0], switch_003_1.inputs[0])
			#switch_001_10.Output -> domain_size_1.Geometry
			style_cartoon.links.new(switch_001_10.outputs[0], domain_size_1.inputs[0])
			#switch_003_1.Output -> join_geometry_1.Geometry
			style_cartoon.links.new(switch_003_1.outputs[0], join_geometry_1.inputs[0])
			return style_cartoon

		style_cartoon = style_cartoon_node_group()

		#initialize color_common node group
		def color_common_node_group():
			color_common = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Color Common")

			color_common.color_tag = 'COLOR'
			color_common.description = ""


			#color_common interface
			#Socket Color
			color_socket_2 = color_common.interface.new_socket(name = "Color", in_out='OUTPUT', socket_type = 'NodeSocketColor')
			color_socket_2.attribute_domain = 'POINT'
			color_socket_2.description = "The output colors for the common elements"

			#Socket Hydrogen
			hydrogen_socket = color_common.interface.new_socket(name = "Hydrogen", in_out='INPUT', socket_type = 'NodeSocketColor')
			hydrogen_socket.attribute_domain = 'POINT'
			hydrogen_socket.description = "Color to set for the element Hydrogen"

			#Socket Carbon
			carbon_socket = color_common.interface.new_socket(name = "Carbon", in_out='INPUT', socket_type = 'NodeSocketColor')
			carbon_socket.attribute_domain = 'POINT'
			carbon_socket.description = "Color to set for the element Carbon"

			#Socket Nitrogen
			nitrogen_socket = color_common.interface.new_socket(name = "Nitrogen", in_out='INPUT', socket_type = 'NodeSocketColor')
			nitrogen_socket.attribute_domain = 'POINT'
			nitrogen_socket.description = "Color to set for the element Nitrogen"

			#Socket Oxygen
			oxygen_socket = color_common.interface.new_socket(name = "Oxygen", in_out='INPUT', socket_type = 'NodeSocketColor')
			oxygen_socket.attribute_domain = 'POINT'
			oxygen_socket.description = "Color to set for the element Oxygen"

			#Socket Phosphorous
			phosphorous_socket = color_common.interface.new_socket(name = "Phosphorous", in_out='INPUT', socket_type = 'NodeSocketColor')
			phosphorous_socket.attribute_domain = 'POINT'
			phosphorous_socket.description = "Color to set for the element Phosphorous"

			#Socket Sulfur
			sulfur_socket = color_common.interface.new_socket(name = "Sulfur", in_out='INPUT', socket_type = 'NodeSocketColor')
			sulfur_socket.attribute_domain = 'POINT'
			sulfur_socket.description = "Color to set for the element Sulfur"


			#initialize color_common nodes
			#node Reroute.001
			reroute_001_17 = color_common.nodes.new("NodeReroute")
			reroute_001_17.name = "Reroute.001"
			#node Reroute.007
			reroute_007_2 = color_common.nodes.new("NodeReroute")
			reroute_007_2.name = "Reroute.007"
			#node Switch.002
			switch_002_6 = color_common.nodes.new("GeometryNodeSwitch")
			switch_002_6.name = "Switch.002"
			switch_002_6.input_type = 'RGBA'

			#node Reroute.009
			reroute_009_1 = color_common.nodes.new("NodeReroute")
			reroute_009_1.name = "Reroute.009"
			#node Reroute
			reroute_24 = color_common.nodes.new("NodeReroute")
			reroute_24.name = "Reroute"
			#node Reroute.006
			reroute_006_3 = color_common.nodes.new("NodeReroute")
			reroute_006_3.name = "Reroute.006"
			#node Reroute.004
			reroute_004_4 = color_common.nodes.new("NodeReroute")
			reroute_004_4.name = "Reroute.004"
			#node Switch
			switch_19 = color_common.nodes.new("GeometryNodeSwitch")
			switch_19.name = "Switch"
			switch_19.input_type = 'RGBA'

			#node Switch.001
			switch_001_11 = color_common.nodes.new("GeometryNodeSwitch")
			switch_001_11.name = "Switch.001"
			switch_001_11.input_type = 'RGBA'

			#node Compare
			compare_17 = color_common.nodes.new("FunctionNodeCompare")
			compare_17.name = "Compare"
			compare_17.data_type = 'INT'
			compare_17.mode = 'ELEMENT'
			compare_17.operation = 'EQUAL'
			#B_INT
			compare_17.inputs[3].default_value = 1

			#node Reroute.011
			reroute_011_2 = color_common.nodes.new("NodeReroute")
			reroute_011_2.name = "Reroute.011"
			#node Reroute.002
			reroute_002_12 = color_common.nodes.new("NodeReroute")
			reroute_002_12.name = "Reroute.002"
			#node Compare.001
			compare_001_11 = color_common.nodes.new("FunctionNodeCompare")
			compare_001_11.name = "Compare.001"
			compare_001_11.data_type = 'INT'
			compare_001_11.mode = 'ELEMENT'
			compare_001_11.operation = 'EQUAL'
			#B_INT
			compare_001_11.inputs[3].default_value = 6

			#node Reroute.003
			reroute_003_12 = color_common.nodes.new("NodeReroute")
			reroute_003_12.name = "Reroute.003"
			#node Compare.002
			compare_002_9 = color_common.nodes.new("FunctionNodeCompare")
			compare_002_9.name = "Compare.002"
			compare_002_9.data_type = 'INT'
			compare_002_9.mode = 'ELEMENT'
			compare_002_9.operation = 'EQUAL'
			#B_INT
			compare_002_9.inputs[3].default_value = 7

			#node Reroute.005
			reroute_005_3 = color_common.nodes.new("NodeReroute")
			reroute_005_3.name = "Reroute.005"
			#node Compare.003
			compare_003_4 = color_common.nodes.new("FunctionNodeCompare")
			compare_003_4.name = "Compare.003"
			compare_003_4.data_type = 'INT'
			compare_003_4.mode = 'ELEMENT'
			compare_003_4.operation = 'EQUAL'
			#B_INT
			compare_003_4.inputs[3].default_value = 8

			#node Reroute.012
			reroute_012_2 = color_common.nodes.new("NodeReroute")
			reroute_012_2.name = "Reroute.012"
			#node Reroute.013
			reroute_013 = color_common.nodes.new("NodeReroute")
			reroute_013.name = "Reroute.013"
			#node Reroute.014
			reroute_014_1 = color_common.nodes.new("NodeReroute")
			reroute_014_1.name = "Reroute.014"
			#node Switch.003
			switch_003_2 = color_common.nodes.new("GeometryNodeSwitch")
			switch_003_2.name = "Switch.003"
			switch_003_2.input_type = 'RGBA'

			#node Compare.004
			compare_004_2 = color_common.nodes.new("FunctionNodeCompare")
			compare_004_2.name = "Compare.004"
			compare_004_2.data_type = 'INT'
			compare_004_2.mode = 'ELEMENT'
			compare_004_2.operation = 'EQUAL'
			#B_INT
			compare_004_2.inputs[3].default_value = 15

			#node Compare.005
			compare_005_2 = color_common.nodes.new("FunctionNodeCompare")
			compare_005_2.name = "Compare.005"
			compare_005_2.data_type = 'INT'
			compare_005_2.mode = 'ELEMENT'
			compare_005_2.operation = 'EQUAL'
			#B_INT
			compare_005_2.inputs[3].default_value = 16

			#node Reroute.015
			reroute_015_1 = color_common.nodes.new("NodeReroute")
			reroute_015_1.name = "Reroute.015"
			#node Switch.004
			switch_004_2 = color_common.nodes.new("GeometryNodeSwitch")
			switch_004_2.name = "Switch.004"
			switch_004_2.input_type = 'RGBA'

			#node Reroute.016
			reroute_016 = color_common.nodes.new("NodeReroute")
			reroute_016.name = "Reroute.016"
			#node Reroute.017
			reroute_017 = color_common.nodes.new("NodeReroute")
			reroute_017.name = "Reroute.017"
			#node Reroute.010
			reroute_010_3 = color_common.nodes.new("NodeReroute")
			reroute_010_3.name = "Reroute.010"
			#node Named Attribute
			named_attribute_11 = color_common.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_11.name = "Named Attribute"
			named_attribute_11.data_type = 'INT'
			#Name
			named_attribute_11.inputs[0].default_value = "atomic_number"

			#node Named Attribute.002
			named_attribute_002_6 = color_common.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_002_6.name = "Named Attribute.002"
			named_attribute_002_6.data_type = 'FLOAT_COLOR'
			#Name
			named_attribute_002_6.inputs[0].default_value = "Color"

			#node Switch.005
			switch_005 = color_common.nodes.new("GeometryNodeSwitch")
			switch_005.name = "Switch.005"
			switch_005.input_type = 'RGBA'

			#node Group Output
			group_output_91 = color_common.nodes.new("NodeGroupOutput")
			group_output_91.name = "Group Output"
			group_output_91.is_active_output = True

			#node Group Input
			group_input_90 = color_common.nodes.new("NodeGroupInput")
			group_input_90.name = "Group Input"




			#Set locations
			reroute_001_17.location = (40.0, -160.0)
			reroute_007_2.location = (200.00003051757812, -180.0)
			switch_002_6.location = (240.0, 19.999969482421875)
			reroute_009_1.location = (339.9999694824219, -200.0)
			reroute_24.location = (-119.99996948242188, -160.0)
			reroute_006_3.location = (-119.99996948242188, -179.99996948242188)
			reroute_004_4.location = (-119.99996948242188, -200.0)
			switch_19.location = (-120.0, 20.0)
			switch_001_11.location = (60.0, 20.0)
			compare_17.location = (-120.0, 199.99996948242188)
			reroute_011_2.location = (-160.0, 219.99998474121094)
			reroute_002_12.location = (20.0, 219.99998474121094)
			compare_001_11.location = (59.99998474121094, 199.99998474121094)
			reroute_003_12.location = (200.0, 220.00001525878906)
			compare_002_9.location = (240.0, 200.00001525878906)
			reroute_005_3.location = (379.9999694824219, 220.00003051757812)
			compare_003_4.location = (420.0, 200.0)
			reroute_012_2.location = (560.0000610351562, 219.99996948242188)
			reroute_013.location = (520.0000610351562, -220.0)
			reroute_014_1.location = (-120.0, -220.0)
			switch_003_2.location = (420.0, 20.0)
			compare_004_2.location = (600.0000610351562, 199.99996948242188)
			compare_005_2.location = (780.0, 200.0)
			reroute_015_1.location = (760.0, 220.0)
			switch_004_2.location = (600.0000610351562, 20.0)
			reroute_016.location = (680.0, -240.0)
			reroute_017.location = (-120.0, -240.0)
			reroute_010_3.location = (-168.18707275390625, 82.08197021484375)
			named_attribute_11.location = (-440.0, 260.0)
			named_attribute_002_6.location = (-380.0, 40.0)
			switch_005.location = (780.0, 20.0)
			group_output_91.location = (1020.0, 220.0)
			group_input_90.location = (-380.0, -100.0)

			#Set dimensions
			reroute_001_17.width, reroute_001_17.height = 16.0, 100.0
			reroute_007_2.width, reroute_007_2.height = 16.0, 100.0
			switch_002_6.width, switch_002_6.height = 140.0, 100.0
			reroute_009_1.width, reroute_009_1.height = 16.0, 100.0
			reroute_24.width, reroute_24.height = 16.0, 100.0
			reroute_006_3.width, reroute_006_3.height = 16.0, 100.0
			reroute_004_4.width, reroute_004_4.height = 16.0, 100.0
			switch_19.width, switch_19.height = 140.0, 100.0
			switch_001_11.width, switch_001_11.height = 140.0, 100.0
			compare_17.width, compare_17.height = 140.0, 100.0
			reroute_011_2.width, reroute_011_2.height = 16.0, 100.0
			reroute_002_12.width, reroute_002_12.height = 16.0, 100.0
			compare_001_11.width, compare_001_11.height = 140.0, 100.0
			reroute_003_12.width, reroute_003_12.height = 16.0, 100.0
			compare_002_9.width, compare_002_9.height = 140.0, 100.0
			reroute_005_3.width, reroute_005_3.height = 16.0, 100.0
			compare_003_4.width, compare_003_4.height = 140.0, 100.0
			reroute_012_2.width, reroute_012_2.height = 16.0, 100.0
			reroute_013.width, reroute_013.height = 16.0, 100.0
			reroute_014_1.width, reroute_014_1.height = 16.0, 100.0
			switch_003_2.width, switch_003_2.height = 140.0, 100.0
			compare_004_2.width, compare_004_2.height = 140.0, 100.0
			compare_005_2.width, compare_005_2.height = 140.0, 100.0
			reroute_015_1.width, reroute_015_1.height = 16.0, 100.0
			switch_004_2.width, switch_004_2.height = 140.0, 100.0
			reroute_016.width, reroute_016.height = 16.0, 100.0
			reroute_017.width, reroute_017.height = 16.0, 100.0
			reroute_010_3.width, reroute_010_3.height = 16.0, 100.0
			named_attribute_11.width, named_attribute_11.height = 199.0511474609375, 100.0
			named_attribute_002_6.width, named_attribute_002_6.height = 140.0, 100.0
			switch_005.width, switch_005.height = 140.0, 100.0
			group_output_91.width, group_output_91.height = 140.0, 100.0
			group_input_90.width, group_input_90.height = 140.0, 100.0

			#initialize color_common links
			#compare_17.Result -> switch_19.Switch
			color_common.links.new(compare_17.outputs[0], switch_19.inputs[0])
			#group_input_90.Hydrogen -> switch_19.True
			color_common.links.new(group_input_90.outputs[0], switch_19.inputs[2])
			#switch_19.Output -> switch_001_11.False
			color_common.links.new(switch_19.outputs[0], switch_001_11.inputs[1])
			#reroute_001_17.Output -> switch_001_11.True
			color_common.links.new(reroute_001_17.outputs[0], switch_001_11.inputs[2])
			#group_input_90.Carbon -> reroute_24.Input
			color_common.links.new(group_input_90.outputs[1], reroute_24.inputs[0])
			#reroute_24.Output -> reroute_001_17.Input
			color_common.links.new(reroute_24.outputs[0], reroute_001_17.inputs[0])
			#switch_001_11.Output -> switch_002_6.False
			color_common.links.new(switch_001_11.outputs[0], switch_002_6.inputs[1])
			#reroute_007_2.Output -> switch_002_6.True
			color_common.links.new(reroute_007_2.outputs[0], switch_002_6.inputs[2])
			#group_input_90.Nitrogen -> reroute_006_3.Input
			color_common.links.new(group_input_90.outputs[2], reroute_006_3.inputs[0])
			#reroute_006_3.Output -> reroute_007_2.Input
			color_common.links.new(reroute_006_3.outputs[0], reroute_007_2.inputs[0])
			#switch_002_6.Output -> switch_003_2.False
			color_common.links.new(switch_002_6.outputs[0], switch_003_2.inputs[1])
			#reroute_009_1.Output -> switch_003_2.True
			color_common.links.new(reroute_009_1.outputs[0], switch_003_2.inputs[2])
			#group_input_90.Oxygen -> reroute_004_4.Input
			color_common.links.new(group_input_90.outputs[3], reroute_004_4.inputs[0])
			#reroute_004_4.Output -> reroute_009_1.Input
			color_common.links.new(reroute_004_4.outputs[0], reroute_009_1.inputs[0])
			#reroute_010_3.Output -> compare_17.A
			color_common.links.new(reroute_010_3.outputs[0], compare_17.inputs[2])
			#reroute_010_3.Output -> reroute_011_2.Input
			color_common.links.new(reroute_010_3.outputs[0], reroute_011_2.inputs[0])
			#compare_001_11.Result -> switch_001_11.Switch
			color_common.links.new(compare_001_11.outputs[0], switch_001_11.inputs[0])
			#reroute_002_12.Output -> compare_001_11.A
			color_common.links.new(reroute_002_12.outputs[0], compare_001_11.inputs[2])
			#reroute_011_2.Output -> reroute_002_12.Input
			color_common.links.new(reroute_011_2.outputs[0], reroute_002_12.inputs[0])
			#reroute_003_12.Output -> compare_002_9.A
			color_common.links.new(reroute_003_12.outputs[0], compare_002_9.inputs[2])
			#reroute_002_12.Output -> reroute_003_12.Input
			color_common.links.new(reroute_002_12.outputs[0], reroute_003_12.inputs[0])
			#compare_002_9.Result -> switch_002_6.Switch
			color_common.links.new(compare_002_9.outputs[0], switch_002_6.inputs[0])
			#reroute_005_3.Output -> compare_003_4.A
			color_common.links.new(reroute_005_3.outputs[0], compare_003_4.inputs[2])
			#reroute_003_12.Output -> reroute_005_3.Input
			color_common.links.new(reroute_003_12.outputs[0], reroute_005_3.inputs[0])
			#compare_003_4.Result -> switch_003_2.Switch
			color_common.links.new(compare_003_4.outputs[0], switch_003_2.inputs[0])
			#reroute_012_2.Output -> compare_004_2.A
			color_common.links.new(reroute_012_2.outputs[0], compare_004_2.inputs[2])
			#compare_004_2.Result -> switch_004_2.Switch
			color_common.links.new(compare_004_2.outputs[0], switch_004_2.inputs[0])
			#reroute_005_3.Output -> reroute_012_2.Input
			color_common.links.new(reroute_005_3.outputs[0], reroute_012_2.inputs[0])
			#reroute_013.Output -> switch_004_2.True
			color_common.links.new(reroute_013.outputs[0], switch_004_2.inputs[2])
			#reroute_014_1.Output -> reroute_013.Input
			color_common.links.new(reroute_014_1.outputs[0], reroute_013.inputs[0])
			#group_input_90.Phosphorous -> reroute_014_1.Input
			color_common.links.new(group_input_90.outputs[4], reroute_014_1.inputs[0])
			#switch_003_2.Output -> switch_004_2.False
			color_common.links.new(switch_003_2.outputs[0], switch_004_2.inputs[1])
			#reroute_015_1.Output -> compare_005_2.A
			color_common.links.new(reroute_015_1.outputs[0], compare_005_2.inputs[2])
			#compare_005_2.Result -> switch_005.Switch
			color_common.links.new(compare_005_2.outputs[0], switch_005.inputs[0])
			#reroute_012_2.Output -> reroute_015_1.Input
			color_common.links.new(reroute_012_2.outputs[0], reroute_015_1.inputs[0])
			#switch_004_2.Output -> switch_005.False
			color_common.links.new(switch_004_2.outputs[0], switch_005.inputs[1])
			#reroute_016.Output -> switch_005.True
			color_common.links.new(reroute_016.outputs[0], switch_005.inputs[2])
			#reroute_017.Output -> reroute_016.Input
			color_common.links.new(reroute_017.outputs[0], reroute_016.inputs[0])
			#group_input_90.Sulfur -> reroute_017.Input
			color_common.links.new(group_input_90.outputs[5], reroute_017.inputs[0])
			#named_attribute_11.Attribute -> reroute_010_3.Input
			color_common.links.new(named_attribute_11.outputs[0], reroute_010_3.inputs[0])
			#switch_005.Output -> group_output_91.Color
			color_common.links.new(switch_005.outputs[0], group_output_91.inputs[0])
			#named_attribute_002_6.Attribute -> switch_19.False
			color_common.links.new(named_attribute_002_6.outputs[0], switch_19.inputs[1])
			return color_common

		color_common = color_common_node_group()

		#initialize color_attribute_random node group
		def color_attribute_random_node_group():
			color_attribute_random = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Color Attribute Random")

			color_attribute_random.color_tag = 'COLOR'
			color_attribute_random.description = ""


			#color_attribute_random interface
			#Socket Color
			color_socket_3 = color_attribute_random.interface.new_socket(name = "Color", in_out='OUTPUT', socket_type = 'NodeSocketColor')
			color_socket_3.attribute_domain = 'POINT'
			color_socket_3.description = "The randomly generated color based on the input attribute"

			#Socket Name
			name_socket_3 = color_attribute_random.interface.new_socket(name = "Name", in_out='INPUT', socket_type = 'NodeSocketString')
			name_socket_3.attribute_domain = 'POINT'
			name_socket_3.description = "Attribute to base the random color generation on "

			#Panel Color
			color_panel = color_attribute_random.interface.new_panel("Color", default_closed=True)
			#Socket Color Saturation
			color_saturation_socket = color_attribute_random.interface.new_socket(name = "Color Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color_panel)
			color_saturation_socket.subtype = 'FACTOR'
			color_saturation_socket.default_value = 0.6000000238418579
			color_saturation_socket.min_value = 0.0
			color_saturation_socket.max_value = 1.0
			color_saturation_socket.attribute_domain = 'POINT'
			color_saturation_socket.description = "Saturlation level for the random color"

			#Socket Color Lightness
			color_lightness_socket = color_attribute_random.interface.new_socket(name = "Color Lightness", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color_panel)
			color_lightness_socket.subtype = 'FACTOR'
			color_lightness_socket.default_value = 0.6000000238418579
			color_lightness_socket.min_value = 0.0
			color_lightness_socket.max_value = 1.0
			color_lightness_socket.attribute_domain = 'POINT'
			color_lightness_socket.description = "Lightness value for the generated random color"

			#Socket Color Seed
			color_seed_socket = color_attribute_random.interface.new_socket(name = "Color Seed", in_out='INPUT', socket_type = 'NodeSocketInt', parent = color_panel)
			color_seed_socket.subtype = 'NONE'
			color_seed_socket.default_value = 0
			color_seed_socket.min_value = -10000
			color_seed_socket.max_value = 10000
			color_seed_socket.attribute_domain = 'POINT'
			color_seed_socket.description = "Seed value for the random generation of the colors"



			#initialize color_attribute_random nodes
			#node Group Output
			group_output_92 = color_attribute_random.nodes.new("NodeGroupOutput")
			group_output_92.name = "Group Output"
			group_output_92.is_active_output = True

			#node Combine Color
			combine_color = color_attribute_random.nodes.new("FunctionNodeCombineColor")
			combine_color.name = "Combine Color"
			combine_color.mode = 'HSL'
			#Alpha
			combine_color.inputs[3].default_value = 1.0

			#node Named Attribute
			named_attribute_12 = color_attribute_random.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_12.name = "Named Attribute"
			named_attribute_12.data_type = 'INT'

			#node Random Value
			random_value = color_attribute_random.nodes.new("FunctionNodeRandomValue")
			random_value.name = "Random Value"
			random_value.data_type = 'FLOAT'
			#Min_001
			random_value.inputs[2].default_value = 0.0
			#Max_001
			random_value.inputs[3].default_value = 1.0

			#node Group Input
			group_input_91 = color_attribute_random.nodes.new("NodeGroupInput")
			group_input_91.name = "Group Input"

			#node Math
			math_29 = color_attribute_random.nodes.new("ShaderNodeMath")
			math_29.name = "Math"
			math_29.operation = 'ADD'
			math_29.use_clamp = False

			#node Integer
			integer_4 = color_attribute_random.nodes.new("FunctionNodeInputInt")
			integer_4.name = "Integer"
			integer_4.integer = 6




			#Set locations
			group_output_92.location = (272.6910400390625, 0.0)
			combine_color.location = (100.0, 0.0)
			named_attribute_12.location = (-220.0, 0.0)
			random_value.location = (-60.0, 0.0)
			group_input_91.location = (-400.0, -80.0)
			math_29.location = (-220.0, -180.0)
			integer_4.location = (-400.0, -280.0)

			#Set dimensions
			group_output_92.width, group_output_92.height = 140.0, 100.0
			combine_color.width, combine_color.height = 140.0, 100.0
			named_attribute_12.width, named_attribute_12.height = 140.0, 100.0
			random_value.width, random_value.height = 140.0, 100.0
			group_input_91.width, group_input_91.height = 140.0, 100.0
			math_29.width, math_29.height = 140.0, 100.0
			integer_4.width, integer_4.height = 140.0, 100.0

			#initialize color_attribute_random links
			#random_value.Value -> combine_color.Red
			color_attribute_random.links.new(random_value.outputs[1], combine_color.inputs[0])
			#named_attribute_12.Attribute -> random_value.ID
			color_attribute_random.links.new(named_attribute_12.outputs[0], random_value.inputs[7])
			#group_input_91.Name -> named_attribute_12.Name
			color_attribute_random.links.new(group_input_91.outputs[0], named_attribute_12.inputs[0])
			#combine_color.Color -> group_output_92.Color
			color_attribute_random.links.new(combine_color.outputs[0], group_output_92.inputs[0])
			#group_input_91.Color Saturation -> combine_color.Green
			color_attribute_random.links.new(group_input_91.outputs[1], combine_color.inputs[1])
			#group_input_91.Color Lightness -> combine_color.Blue
			color_attribute_random.links.new(group_input_91.outputs[2], combine_color.inputs[2])
			#group_input_91.Color Seed -> math_29.Value
			color_attribute_random.links.new(group_input_91.outputs[3], math_29.inputs[0])
			#math_29.Value -> random_value.Seed
			color_attribute_random.links.new(math_29.outputs[0], random_value.inputs[8])
			#integer_4.Integer -> math_29.Value
			color_attribute_random.links.new(integer_4.outputs[0], math_29.inputs[1])
			return color_attribute_random

		color_attribute_random = color_attribute_random_node_group()

		#initialize _mn_utils_style_spheres_points node group
		def _mn_utils_style_spheres_points_node_group():
			_mn_utils_style_spheres_points = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".MN_utils_style_spheres_points")

			_mn_utils_style_spheres_points.color_tag = 'GEOMETRY'
			_mn_utils_style_spheres_points.description = ""

			_mn_utils_style_spheres_points.is_modifier = True

			#_mn_utils_style_spheres_points interface
			#Socket Point Cloud
			point_cloud_socket = _mn_utils_style_spheres_points.interface.new_socket(name = "Point Cloud", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			point_cloud_socket.attribute_domain = 'POINT'

			#Socket Atoms
			atoms_socket_12 = _mn_utils_style_spheres_points.interface.new_socket(name = "Atoms", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			atoms_socket_12.attribute_domain = 'POINT'
			atoms_socket_12.description = "Atomic geometry that contains vertices and edges"

			#Socket Selection
			selection_socket_15 = _mn_utils_style_spheres_points.interface.new_socket(name = "Selection", in_out='INPUT', socket_type = 'NodeSocketBool')
			selection_socket_15.attribute_domain = 'POINT'
			selection_socket_15.hide_value = True
			selection_socket_15.description = "Selection of atoms to apply this node to"

			#Socket Radii
			radii_socket = _mn_utils_style_spheres_points.interface.new_socket(name = "Radii", in_out='INPUT', socket_type = 'NodeSocketFloat')
			radii_socket.subtype = 'NONE'
			radii_socket.default_value = 0.800000011920929
			radii_socket.min_value = 0.0
			radii_socket.max_value = 10000.0
			radii_socket.attribute_domain = 'POINT'

			#Socket Material
			material_socket_4 = _mn_utils_style_spheres_points.interface.new_socket(name = "Material", in_out='INPUT', socket_type = 'NodeSocketMaterial')
			material_socket_4.attribute_domain = 'POINT'
			material_socket_4.description = "Material to apply to the resulting geometry"


			#initialize _mn_utils_style_spheres_points nodes
			#node Group Input
			group_input_92 = _mn_utils_style_spheres_points.nodes.new("NodeGroupInput")
			group_input_92.name = "Group Input"

			#node Mesh to Points
			mesh_to_points_1 = _mn_utils_style_spheres_points.nodes.new("GeometryNodeMeshToPoints")
			mesh_to_points_1.name = "Mesh to Points"
			mesh_to_points_1.mode = 'VERTICES'
			#Position
			mesh_to_points_1.inputs[2].default_value = (0.0, 0.0, 0.0)

			#node Switch
			switch_20 = _mn_utils_style_spheres_points.nodes.new("GeometryNodeSwitch")
			switch_20.name = "Switch"
			switch_20.input_type = 'FLOAT'

			#node Named Attribute
			named_attribute_13 = _mn_utils_style_spheres_points.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_13.name = "Named Attribute"
			named_attribute_13.data_type = 'FLOAT'
			#Name
			named_attribute_13.inputs[0].default_value = "vdw_radii"

			#node Group
			group_35 = _mn_utils_style_spheres_points.nodes.new("GeometryNodeGroup")
			group_35.name = "Group"
			group_35.node_tree = mn_units
			#Input_1
			group_35.inputs[0].default_value = 0.800000011920929

			#node Math
			math_30 = _mn_utils_style_spheres_points.nodes.new("ShaderNodeMath")
			math_30.name = "Math"
			math_30.operation = 'MULTIPLY'
			math_30.use_clamp = False

			#node Group Output
			group_output_93 = _mn_utils_style_spheres_points.nodes.new("NodeGroupOutput")
			group_output_93.name = "Group Output"
			group_output_93.is_active_output = True

			#node Set Material
			set_material_2 = _mn_utils_style_spheres_points.nodes.new("GeometryNodeSetMaterial")
			set_material_2.name = "Set Material"
			#Selection
			set_material_2.inputs[1].default_value = True




			#Set locations
			group_input_92.location = (-1060.0, 60.0)
			mesh_to_points_1.location = (-540.0, 220.0)
			switch_20.location = (-900.0, -100.0)
			named_attribute_13.location = (-1080.0, -100.0)
			group_35.location = (-1080.0, -240.0)
			math_30.location = (-720.0, 40.0)
			group_output_93.location = (-220.0, 220.0)
			set_material_2.location = (-380.0, 220.0)

			#Set dimensions
			group_input_92.width, group_input_92.height = 140.0, 100.0
			mesh_to_points_1.width, mesh_to_points_1.height = 140.0, 100.0
			switch_20.width, switch_20.height = 140.0, 100.0
			named_attribute_13.width, named_attribute_13.height = 140.0, 100.0
			group_35.width, group_35.height = 140.0, 100.0
			math_30.width, math_30.height = 140.0, 100.0
			group_output_93.width, group_output_93.height = 140.0, 100.0
			set_material_2.width, set_material_2.height = 140.0, 100.0

			#initialize _mn_utils_style_spheres_points links
			#set_material_2.Geometry -> group_output_93.Point Cloud
			_mn_utils_style_spheres_points.links.new(set_material_2.outputs[0], group_output_93.inputs[0])
			#group_input_92.Selection -> mesh_to_points_1.Selection
			_mn_utils_style_spheres_points.links.new(group_input_92.outputs[1], mesh_to_points_1.inputs[1])
			#group_input_92.Radii -> math_30.Value
			_mn_utils_style_spheres_points.links.new(group_input_92.outputs[2], math_30.inputs[0])
			#math_30.Value -> mesh_to_points_1.Radius
			_mn_utils_style_spheres_points.links.new(math_30.outputs[0], mesh_to_points_1.inputs[3])
			#group_input_92.Material -> set_material_2.Material
			_mn_utils_style_spheres_points.links.new(group_input_92.outputs[3], set_material_2.inputs[2])
			#named_attribute_13.Attribute -> switch_20.Switch
			_mn_utils_style_spheres_points.links.new(named_attribute_13.outputs[0], switch_20.inputs[0])
			#named_attribute_13.Attribute -> switch_20.True
			_mn_utils_style_spheres_points.links.new(named_attribute_13.outputs[0], switch_20.inputs[2])
			#switch_20.Output -> math_30.Value
			_mn_utils_style_spheres_points.links.new(switch_20.outputs[0], math_30.inputs[1])
			#group_input_92.Atoms -> mesh_to_points_1.Mesh
			_mn_utils_style_spheres_points.links.new(group_input_92.outputs[0], mesh_to_points_1.inputs[0])
			#mesh_to_points_1.Points -> set_material_2.Geometry
			_mn_utils_style_spheres_points.links.new(mesh_to_points_1.outputs[0], set_material_2.inputs[0])
			#group_35.Angstrom -> switch_20.False
			_mn_utils_style_spheres_points.links.new(group_35.outputs[0], switch_20.inputs[1])
			return _mn_utils_style_spheres_points

		_mn_utils_style_spheres_points = _mn_utils_style_spheres_points_node_group()

		#initialize _mn_utils_style_spheres_icosphere node group
		def _mn_utils_style_spheres_icosphere_node_group():
			_mn_utils_style_spheres_icosphere = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = ".MN_utils_style_spheres_icosphere")

			_mn_utils_style_spheres_icosphere.color_tag = 'GEOMETRY'
			_mn_utils_style_spheres_icosphere.description = ""

			_mn_utils_style_spheres_icosphere.is_modifier = True

			#_mn_utils_style_spheres_icosphere interface
			#Socket Instances
			instances_socket = _mn_utils_style_spheres_icosphere.interface.new_socket(name = "Instances", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			instances_socket.attribute_domain = 'POINT'

			#Socket Atoms
			atoms_socket_13 = _mn_utils_style_spheres_icosphere.interface.new_socket(name = "Atoms", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			atoms_socket_13.attribute_domain = 'POINT'
			atoms_socket_13.description = "Atomic geometry that contains vertices and edges"

			#Socket Selection
			selection_socket_16 = _mn_utils_style_spheres_icosphere.interface.new_socket(name = "Selection", in_out='INPUT', socket_type = 'NodeSocketBool')
			selection_socket_16.attribute_domain = 'POINT'
			selection_socket_16.hide_value = True
			selection_socket_16.description = "Selection of atoms to apply this node to"

			#Socket Radii
			radii_socket_1 = _mn_utils_style_spheres_icosphere.interface.new_socket(name = "Radii", in_out='INPUT', socket_type = 'NodeSocketFloat')
			radii_socket_1.subtype = 'NONE'
			radii_socket_1.default_value = 0.800000011920929
			radii_socket_1.min_value = 0.0
			radii_socket_1.max_value = 10000.0
			radii_socket_1.attribute_domain = 'POINT'
			radii_socket_1.description = "Scale the VDW radii of the atoms."

			#Socket Subdivisions
			subdivisions_socket_4 = _mn_utils_style_spheres_icosphere.interface.new_socket(name = "Subdivisions", in_out='INPUT', socket_type = 'NodeSocketInt')
			subdivisions_socket_4.subtype = 'NONE'
			subdivisions_socket_4.default_value = 2
			subdivisions_socket_4.min_value = 0
			subdivisions_socket_4.max_value = 5
			subdivisions_socket_4.attribute_domain = 'POINT'

			#Socket Shade Smooth
			shade_smooth_socket_3 = _mn_utils_style_spheres_icosphere.interface.new_socket(name = "Shade Smooth", in_out='INPUT', socket_type = 'NodeSocketBool')
			shade_smooth_socket_3.attribute_domain = 'POINT'
			shade_smooth_socket_3.description = "Apply smooth shading to the created geometry"

			#Socket Material
			material_socket_5 = _mn_utils_style_spheres_icosphere.interface.new_socket(name = "Material", in_out='INPUT', socket_type = 'NodeSocketMaterial')
			material_socket_5.attribute_domain = 'POINT'
			material_socket_5.description = "Material to apply to the resulting geometry"


			#initialize _mn_utils_style_spheres_icosphere nodes
			#node Frame
			frame_17 = _mn_utils_style_spheres_icosphere.nodes.new("NodeFrame")
			frame_17.label = "Different Levels of Detail."
			frame_17.name = "Frame"
			frame_17.label_size = 20
			frame_17.shrink = True

			#node Reroute
			reroute_25 = _mn_utils_style_spheres_icosphere.nodes.new("NodeReroute")
			reroute_25.name = "Reroute"
			#node Math.001
			math_001_12 = _mn_utils_style_spheres_icosphere.nodes.new("ShaderNodeMath")
			math_001_12.name = "Math.001"
			math_001_12.operation = 'MINIMUM'
			math_001_12.use_clamp = False

			#node Group Output
			group_output_94 = _mn_utils_style_spheres_icosphere.nodes.new("NodeGroupOutput")
			group_output_94.name = "Group Output"
			group_output_94.is_active_output = True

			#node Group Input.002
			group_input_002_9 = _mn_utils_style_spheres_icosphere.nodes.new("NodeGroupInput")
			group_input_002_9.name = "Group Input.002"
			group_input_002_9.outputs[0].hide = True
			group_input_002_9.outputs[1].hide = True
			group_input_002_9.outputs[2].hide = True
			group_input_002_9.outputs[3].hide = True
			group_input_002_9.outputs[6].hide = True

			#node Set Shade Smooth
			set_shade_smooth_1 = _mn_utils_style_spheres_icosphere.nodes.new("GeometryNodeSetShadeSmooth")
			set_shade_smooth_1.name = "Set Shade Smooth"
			set_shade_smooth_1.domain = 'FACE'
			#Selection
			set_shade_smooth_1.inputs[1].default_value = True

			#node Set Material
			set_material_3 = _mn_utils_style_spheres_icosphere.nodes.new("GeometryNodeSetMaterial")
			set_material_3.name = "Set Material"
			#Selection
			set_material_3.inputs[1].default_value = True

			#node Group Input
			group_input_93 = _mn_utils_style_spheres_icosphere.nodes.new("NodeGroupInput")
			group_input_93.name = "Group Input"
			group_input_93.outputs[2].hide = True
			group_input_93.outputs[3].hide = True
			group_input_93.outputs[4].hide = True
			group_input_93.outputs[5].hide = True
			group_input_93.outputs[6].hide = True

			#node Reroute.001
			reroute_001_18 = _mn_utils_style_spheres_icosphere.nodes.new("NodeReroute")
			reroute_001_18.name = "Reroute.001"
			#node Group Input.001
			group_input_001_16 = _mn_utils_style_spheres_icosphere.nodes.new("NodeGroupInput")
			group_input_001_16.name = "Group Input.001"
			group_input_001_16.outputs[0].hide = True
			group_input_001_16.outputs[1].hide = True
			group_input_001_16.outputs[2].hide = True
			group_input_001_16.outputs[4].hide = True
			group_input_001_16.outputs[5].hide = True
			group_input_001_16.outputs[6].hide = True

			#node Ico Sphere.001
			ico_sphere_001 = _mn_utils_style_spheres_icosphere.nodes.new("GeometryNodeMeshIcoSphere")
			ico_sphere_001.name = "Ico Sphere.001"
			#Radius
			ico_sphere_001.inputs[0].default_value = 1.0
			#Subdivisions
			ico_sphere_001.inputs[1].default_value = 1

			#node Ico Sphere.002
			ico_sphere_002 = _mn_utils_style_spheres_icosphere.nodes.new("GeometryNodeMeshIcoSphere")
			ico_sphere_002.name = "Ico Sphere.002"
			#Radius
			ico_sphere_002.inputs[0].default_value = 1.0
			#Subdivisions
			ico_sphere_002.inputs[1].default_value = 2

			#node Ico Sphere.003
			ico_sphere_003 = _mn_utils_style_spheres_icosphere.nodes.new("GeometryNodeMeshIcoSphere")
			ico_sphere_003.name = "Ico Sphere.003"
			#Radius
			ico_sphere_003.inputs[0].default_value = 1.0
			#Subdivisions
			ico_sphere_003.inputs[1].default_value = 3

			#node Geometry to Instance
			geometry_to_instance = _mn_utils_style_spheres_icosphere.nodes.new("GeometryNodeGeometryToInstance")
			geometry_to_instance.name = "Geometry to Instance"

			#node Ico Sphere.004
			ico_sphere_004 = _mn_utils_style_spheres_icosphere.nodes.new("GeometryNodeMeshIcoSphere")
			ico_sphere_004.name = "Ico Sphere.004"
			#Radius
			ico_sphere_004.inputs[0].default_value = 1.0
			#Subdivisions
			ico_sphere_004.inputs[1].default_value = 4

			#node Ico Sphere.005
			ico_sphere_005 = _mn_utils_style_spheres_icosphere.nodes.new("GeometryNodeMeshIcoSphere")
			ico_sphere_005.name = "Ico Sphere.005"
			#Radius
			ico_sphere_005.inputs[0].default_value = 1.0
			#Subdivisions
			ico_sphere_005.inputs[1].default_value = 5

			#node Reroute.002
			reroute_002_13 = _mn_utils_style_spheres_icosphere.nodes.new("NodeReroute")
			reroute_002_13.name = "Reroute.002"
			#node Transform Geometry
			transform_geometry = _mn_utils_style_spheres_icosphere.nodes.new("GeometryNodeTransform")
			transform_geometry.name = "Transform Geometry"
			transform_geometry.mode = 'COMPONENTS'
			#Translation
			transform_geometry.inputs[1].default_value = (0.0, 0.0, 0.0)
			#Rotation
			transform_geometry.inputs[2].default_value = (0.7853981852531433, 0.7853981852531433, 0.0)
			#Scale
			transform_geometry.inputs[3].default_value = (1.0, 1.0, 1.0)

			#node Cube
			cube = _mn_utils_style_spheres_icosphere.nodes.new("GeometryNodeMeshCube")
			cube.name = "Cube"
			#Size
			cube.inputs[0].default_value = (1.0, 1.0, 1.0)
			#Vertices X
			cube.inputs[1].default_value = 2
			#Vertices Y
			cube.inputs[2].default_value = 2
			#Vertices Z
			cube.inputs[3].default_value = 2

			#node Named Attribute
			named_attribute_14 = _mn_utils_style_spheres_icosphere.nodes.new("GeometryNodeInputNamedAttribute")
			named_attribute_14.name = "Named Attribute"
			named_attribute_14.data_type = 'FLOAT'
			#Name
			named_attribute_14.inputs[0].default_value = "vdw_radii"

			#node Radius
			radius = _mn_utils_style_spheres_icosphere.nodes.new("GeometryNodeInputRadius")
			radius.name = "Radius"

			#node Math
			math_31 = _mn_utils_style_spheres_icosphere.nodes.new("ShaderNodeMath")
			math_31.name = "Math"
			math_31.operation = 'MAXIMUM'
			math_31.use_clamp = False

			#node Math.003
			math_003_7 = _mn_utils_style_spheres_icosphere.nodes.new("ShaderNodeMath")
			math_003_7.name = "Math.003"
			math_003_7.operation = 'MULTIPLY'
			math_003_7.use_clamp = False

			#node Group Input.003
			group_input_003_5 = _mn_utils_style_spheres_icosphere.nodes.new("NodeGroupInput")
			group_input_003_5.name = "Group Input.003"
			group_input_003_5.outputs[0].hide = True
			group_input_003_5.outputs[1].hide = True
			group_input_003_5.outputs[3].hide = True
			group_input_003_5.outputs[4].hide = True
			group_input_003_5.outputs[5].hide = True
			group_input_003_5.outputs[6].hide = True

			#node Math.002
			math_002_9 = _mn_utils_style_spheres_icosphere.nodes.new("ShaderNodeMath")
			math_002_9.name = "Math.002"
			math_002_9.operation = 'ADD'
			math_002_9.use_clamp = False

			#node Integer
			integer_5 = _mn_utils_style_spheres_icosphere.nodes.new("FunctionNodeInputInt")
			integer_5.name = "Integer"
			integer_5.integer = -1

			#node Domain Size
			domain_size_2 = _mn_utils_style_spheres_icosphere.nodes.new("GeometryNodeAttributeDomainSize")
			domain_size_2.name = "Domain Size"
			domain_size_2.component = 'INSTANCES'

			#node Instance on Points
			instance_on_points_1 = _mn_utils_style_spheres_icosphere.nodes.new("GeometryNodeInstanceOnPoints")
			instance_on_points_1.name = "Instance on Points"
			#Pick Instance
			instance_on_points_1.inputs[3].default_value = True
			#Rotation
			instance_on_points_1.inputs[5].default_value = (0.0, 0.0, 0.0)



			#Set parents
			ico_sphere_001.parent = frame_17
			ico_sphere_002.parent = frame_17
			ico_sphere_003.parent = frame_17
			geometry_to_instance.parent = frame_17
			ico_sphere_004.parent = frame_17
			ico_sphere_005.parent = frame_17
			reroute_002_13.parent = frame_17
			transform_geometry.parent = frame_17
			cube.parent = frame_17

			#Set locations
			frame_17.location = (0.0, 0.0)
			reroute_25.location = (-560.0, -40.0)
			math_001_12.location = (-140.0, 60.0)
			group_output_94.location = (835.407470703125, 359.5566711425781)
			group_input_002_9.location = (320.0, 260.0)
			set_shade_smooth_1.location = (500.0, 340.0)
			set_material_3.location = (660.0, 340.0)
			group_input_93.location = (-160.0, 240.0)
			reroute_001_18.location = (-480.0, 120.0)
			group_input_001_16.location = (-300.0, 60.0)
			ico_sphere_001.location = (-1180.0, 120.0)
			ico_sphere_002.location = (-1180.0, -20.0)
			ico_sphere_003.location = (-1180.0, -160.0)
			geometry_to_instance.location = (-940.0, 0.0)
			ico_sphere_004.location = (-1180.0, -300.0)
			ico_sphere_005.location = (-1180.0, -440.0)
			reroute_002_13.location = (-1040.0, 160.0)
			transform_geometry.location = (-1360.0, 200.0)
			cube.location = (-1520.0, 200.0)
			named_attribute_14.location = (-240.0, -340.0)
			radius.location = (-240.0, -480.0)
			math_31.location = (-60.0, -340.0)
			math_003_7.location = (100.0, -340.0)
			group_input_003_5.location = (-60.0, -520.0)
			math_002_9.location = (-140.0, -100.0)
			integer_5.location = (-320.0, -220.0)
			domain_size_2.location = (-320.0, -100.0)
			instance_on_points_1.location = (91.33897399902344, 216.86837768554688)

			#Set dimensions
			frame_17.width, frame_17.height = 800.0, 829.0
			reroute_25.width, reroute_25.height = 16.0, 100.0
			math_001_12.width, math_001_12.height = 140.0, 100.0
			group_output_94.width, group_output_94.height = 140.0, 100.0
			group_input_002_9.width, group_input_002_9.height = 140.0, 100.0
			set_shade_smooth_1.width, set_shade_smooth_1.height = 140.0, 100.0
			set_material_3.width, set_material_3.height = 140.0, 100.0
			group_input_93.width, group_input_93.height = 140.0, 100.0
			reroute_001_18.width, reroute_001_18.height = 16.0, 100.0
			group_input_001_16.width, group_input_001_16.height = 140.0, 100.0
			ico_sphere_001.width, ico_sphere_001.height = 140.0, 100.0
			ico_sphere_002.width, ico_sphere_002.height = 140.0, 100.0
			ico_sphere_003.width, ico_sphere_003.height = 140.0, 100.0
			geometry_to_instance.width, geometry_to_instance.height = 160.0, 100.0
			ico_sphere_004.width, ico_sphere_004.height = 140.0, 100.0
			ico_sphere_005.width, ico_sphere_005.height = 140.0, 100.0
			reroute_002_13.width, reroute_002_13.height = 16.0, 100.0
			transform_geometry.width, transform_geometry.height = 140.0, 100.0
			cube.width, cube.height = 140.0, 100.0
			named_attribute_14.width, named_attribute_14.height = 140.0, 100.0
			radius.width, radius.height = 140.0, 100.0
			math_31.width, math_31.height = 140.0, 100.0
			math_003_7.width, math_003_7.height = 140.0, 100.0
			group_input_003_5.width, group_input_003_5.height = 140.0, 100.0
			math_002_9.width, math_002_9.height = 140.0, 100.0
			integer_5.width, integer_5.height = 140.0, 100.0
			domain_size_2.width, domain_size_2.height = 140.0, 100.0
			instance_on_points_1.width, instance_on_points_1.height = 140.9404296875, 100.0

			#initialize _mn_utils_style_spheres_icosphere links
			#set_material_3.Geometry -> group_output_94.Instances
			_mn_utils_style_spheres_icosphere.links.new(set_material_3.outputs[0], group_output_94.inputs[0])
			#set_shade_smooth_1.Geometry -> set_material_3.Geometry
			_mn_utils_style_spheres_icosphere.links.new(set_shade_smooth_1.outputs[0], set_material_3.inputs[0])
			#group_input_93.Atoms -> instance_on_points_1.Points
			_mn_utils_style_spheres_icosphere.links.new(group_input_93.outputs[0], instance_on_points_1.inputs[0])
			#reroute_001_18.Output -> instance_on_points_1.Instance
			_mn_utils_style_spheres_icosphere.links.new(reroute_001_18.outputs[0], instance_on_points_1.inputs[2])
			#ico_sphere_005.Mesh -> geometry_to_instance.Geometry
			_mn_utils_style_spheres_icosphere.links.new(ico_sphere_005.outputs[0], geometry_to_instance.inputs[0])
			#math_001_12.Value -> instance_on_points_1.Instance Index
			_mn_utils_style_spheres_icosphere.links.new(math_001_12.outputs[0], instance_on_points_1.inputs[4])
			#group_input_001_16.Subdivisions -> math_001_12.Value
			_mn_utils_style_spheres_icosphere.links.new(group_input_001_16.outputs[3], math_001_12.inputs[0])
			#reroute_25.Output -> domain_size_2.Geometry
			_mn_utils_style_spheres_icosphere.links.new(reroute_25.outputs[0], domain_size_2.inputs[0])
			#geometry_to_instance.Instances -> reroute_25.Input
			_mn_utils_style_spheres_icosphere.links.new(geometry_to_instance.outputs[0], reroute_25.inputs[0])
			#named_attribute_14.Attribute -> math_31.Value
			_mn_utils_style_spheres_icosphere.links.new(named_attribute_14.outputs[0], math_31.inputs[0])
			#radius.Radius -> math_31.Value
			_mn_utils_style_spheres_icosphere.links.new(radius.outputs[0], math_31.inputs[1])
			#group_input_002_9.Material -> set_material_3.Material
			_mn_utils_style_spheres_icosphere.links.new(group_input_002_9.outputs[5], set_material_3.inputs[2])
			#instance_on_points_1.Instances -> set_shade_smooth_1.Geometry
			_mn_utils_style_spheres_icosphere.links.new(instance_on_points_1.outputs[0], set_shade_smooth_1.inputs[0])
			#group_input_002_9.Shade Smooth -> set_shade_smooth_1.Shade Smooth
			_mn_utils_style_spheres_icosphere.links.new(group_input_002_9.outputs[4], set_shade_smooth_1.inputs[2])
			#group_input_93.Selection -> instance_on_points_1.Selection
			_mn_utils_style_spheres_icosphere.links.new(group_input_93.outputs[1], instance_on_points_1.inputs[1])
			#math_31.Value -> math_003_7.Value
			_mn_utils_style_spheres_icosphere.links.new(math_31.outputs[0], math_003_7.inputs[0])
			#group_input_003_5.Radii -> math_003_7.Value
			_mn_utils_style_spheres_icosphere.links.new(group_input_003_5.outputs[2], math_003_7.inputs[1])
			#reroute_25.Output -> reroute_001_18.Input
			_mn_utils_style_spheres_icosphere.links.new(reroute_25.outputs[0], reroute_001_18.inputs[0])
			#math_003_7.Value -> instance_on_points_1.Scale
			_mn_utils_style_spheres_icosphere.links.new(math_003_7.outputs[0], instance_on_points_1.inputs[6])
			#cube.Mesh -> transform_geometry.Geometry
			_mn_utils_style_spheres_icosphere.links.new(cube.outputs[0], transform_geometry.inputs[0])
			#transform_geometry.Geometry -> reroute_002_13.Input
			_mn_utils_style_spheres_icosphere.links.new(transform_geometry.outputs[0], reroute_002_13.inputs[0])
			#domain_size_2.Instance Count -> math_002_9.Value
			_mn_utils_style_spheres_icosphere.links.new(domain_size_2.outputs[5], math_002_9.inputs[0])
			#integer_5.Integer -> math_002_9.Value
			_mn_utils_style_spheres_icosphere.links.new(integer_5.outputs[0], math_002_9.inputs[1])
			#math_002_9.Value -> math_001_12.Value
			_mn_utils_style_spheres_icosphere.links.new(math_002_9.outputs[0], math_001_12.inputs[1])
			#ico_sphere_004.Mesh -> geometry_to_instance.Geometry
			_mn_utils_style_spheres_icosphere.links.new(ico_sphere_004.outputs[0], geometry_to_instance.inputs[0])
			#ico_sphere_003.Mesh -> geometry_to_instance.Geometry
			_mn_utils_style_spheres_icosphere.links.new(ico_sphere_003.outputs[0], geometry_to_instance.inputs[0])
			#ico_sphere_002.Mesh -> geometry_to_instance.Geometry
			_mn_utils_style_spheres_icosphere.links.new(ico_sphere_002.outputs[0], geometry_to_instance.inputs[0])
			#ico_sphere_001.Mesh -> geometry_to_instance.Geometry
			_mn_utils_style_spheres_icosphere.links.new(ico_sphere_001.outputs[0], geometry_to_instance.inputs[0])
			#reroute_002_13.Output -> geometry_to_instance.Geometry
			_mn_utils_style_spheres_icosphere.links.new(reroute_002_13.outputs[0], geometry_to_instance.inputs[0])
			return _mn_utils_style_spheres_icosphere

		_mn_utils_style_spheres_icosphere = _mn_utils_style_spheres_icosphere_node_group()

		#initialize style_spheres node group
		def style_spheres_node_group():
			style_spheres = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Style Spheres")

			style_spheres.color_tag = 'GEOMETRY'
			style_spheres.description = ""

			style_spheres.is_modifier = True

			#style_spheres interface
			#Socket Geometry
			geometry_socket_18 = style_spheres.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			geometry_socket_18.attribute_domain = 'POINT'

			#Socket Atoms
			atoms_socket_14 = style_spheres.interface.new_socket(name = "Atoms", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			atoms_socket_14.attribute_domain = 'POINT'
			atoms_socket_14.description = "Atomic geometry that contains vertices and edges"

			#Socket Selection
			selection_socket_17 = style_spheres.interface.new_socket(name = "Selection", in_out='INPUT', socket_type = 'NodeSocketBool')
			selection_socket_17.attribute_domain = 'POINT'
			selection_socket_17.hide_value = True
			selection_socket_17.description = "Selection of atoms to apply this style to"

			#Panel Sphere
			sphere_panel = style_spheres.interface.new_panel("Sphere")
			#Socket Sphere As Mesh
			sphere_as_mesh_socket = style_spheres.interface.new_socket(name = "Sphere As Mesh", in_out='INPUT', socket_type = 'NodeSocketBool', parent = sphere_panel)
			sphere_as_mesh_socket.attribute_domain = 'POINT'
			sphere_as_mesh_socket.description = "Use Eevee or Cycles compatible atoms."

			#Socket Sphere Radii
			sphere_radii_socket = style_spheres.interface.new_socket(name = "Sphere Radii", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = sphere_panel)
			sphere_radii_socket.subtype = 'NONE'
			sphere_radii_socket.default_value = 0.800000011920929
			sphere_radii_socket.min_value = 0.0
			sphere_radii_socket.max_value = 2.0
			sphere_radii_socket.attribute_domain = 'POINT'
			sphere_radii_socket.description = "Scale the `vdw_radii` of the atoms."

			#Socket Sphere Subdivisions
			sphere_subdivisions_socket = style_spheres.interface.new_socket(name = "Sphere Subdivisions", in_out='INPUT', socket_type = 'NodeSocketInt', parent = sphere_panel)
			sphere_subdivisions_socket.subtype = 'NONE'
			sphere_subdivisions_socket.default_value = 2
			sphere_subdivisions_socket.min_value = 0
			sphere_subdivisions_socket.max_value = 5
			sphere_subdivisions_socket.attribute_domain = 'POINT'
			sphere_subdivisions_socket.description = "Subdivisions for Eevee compatible atoms."


			#Panel Material
			material_panel_1 = style_spheres.interface.new_panel("Material", default_closed=True)
			#Socket Shade Smooth
			shade_smooth_socket_4 = style_spheres.interface.new_socket(name = "Shade Smooth", in_out='INPUT', socket_type = 'NodeSocketBool', parent = material_panel_1)
			shade_smooth_socket_4.attribute_domain = 'POINT'
			shade_smooth_socket_4.description = "Apply smooth shading to the created geometry"

			#Socket Material
			material_socket_6 = style_spheres.interface.new_socket(name = "Material", in_out='INPUT', socket_type = 'NodeSocketMaterial', parent = material_panel_1)
			material_socket_6.attribute_domain = 'POINT'
			material_socket_6.description = "Material to apply to the resulting geometry"



			#initialize style_spheres nodes
			#node Group Input
			group_input_94 = style_spheres.nodes.new("NodeGroupInput")
			group_input_94.name = "Group Input"

			#node Group Output
			group_output_95 = style_spheres.nodes.new("NodeGroupOutput")
			group_output_95.name = "Group Output"
			group_output_95.is_active_output = True

			#node Join Geometry
			join_geometry_2 = style_spheres.nodes.new("GeometryNodeJoinGeometry")
			join_geometry_2.name = "Join Geometry"

			#node Separate Geometry
			separate_geometry_3 = style_spheres.nodes.new("GeometryNodeSeparateGeometry")
			separate_geometry_3.name = "Separate Geometry"
			separate_geometry_3.domain = 'POINT'

			#node Group.014
			group_014_5 = style_spheres.nodes.new("GeometryNodeGroup")
			group_014_5.name = "Group.014"
			group_014_5.node_tree = _mn_utils_style_spheres_points

			#node Group.026
			group_026_1 = style_spheres.nodes.new("GeometryNodeGroup")
			group_026_1.name = "Group.026"
			group_026_1.node_tree = _mn_utils_style_spheres_icosphere

			#node Realize Instances
			realize_instances_2 = style_spheres.nodes.new("GeometryNodeRealizeInstances")
			realize_instances_2.name = "Realize Instances"
			#Selection
			realize_instances_2.inputs[1].default_value = True
			#Realize All
			realize_instances_2.inputs[2].default_value = True
			#Depth
			realize_instances_2.inputs[3].default_value = 0




			#Set locations
			group_input_94.location = (-679.2061157226562, -54.561466217041016)
			group_output_95.location = (480.0, 40.0)
			join_geometry_2.location = (320.0, 40.0)
			separate_geometry_3.location = (-420.0, 80.0)
			group_014_5.location = (-200.0, -200.0)
			group_026_1.location = (-200.0, 60.0)
			realize_instances_2.location = (100.0, 60.0)

			#Set dimensions
			group_input_94.width, group_input_94.height = 140.0, 100.0
			group_output_95.width, group_output_95.height = 140.0, 100.0
			join_geometry_2.width, join_geometry_2.height = 140.0, 100.0
			separate_geometry_3.width, separate_geometry_3.height = 140.0, 100.0
			group_014_5.width, group_014_5.height = 277.9979248046875, 100.0
			group_026_1.width, group_026_1.height = 278.0207824707031, 100.0
			realize_instances_2.width, realize_instances_2.height = 140.0, 100.0

			#initialize style_spheres links
			#group_input_94.Atoms -> separate_geometry_3.Geometry
			style_spheres.links.new(group_input_94.outputs[0], separate_geometry_3.inputs[0])
			#group_input_94.Selection -> group_014_5.Selection
			style_spheres.links.new(group_input_94.outputs[1], group_014_5.inputs[1])
			#group_input_94.Selection -> group_026_1.Selection
			style_spheres.links.new(group_input_94.outputs[1], group_026_1.inputs[1])
			#group_input_94.Sphere As Mesh -> separate_geometry_3.Selection
			style_spheres.links.new(group_input_94.outputs[2], separate_geometry_3.inputs[1])
			#group_input_94.Sphere Radii -> group_014_5.Radii
			style_spheres.links.new(group_input_94.outputs[3], group_014_5.inputs[2])
			#group_input_94.Sphere Radii -> group_026_1.Radii
			style_spheres.links.new(group_input_94.outputs[3], group_026_1.inputs[2])
			#group_input_94.Sphere Subdivisions -> group_026_1.Subdivisions
			style_spheres.links.new(group_input_94.outputs[4], group_026_1.inputs[3])
			#group_input_94.Shade Smooth -> group_026_1.Shade Smooth
			style_spheres.links.new(group_input_94.outputs[5], group_026_1.inputs[4])
			#group_input_94.Material -> group_014_5.Material
			style_spheres.links.new(group_input_94.outputs[6], group_014_5.inputs[3])
			#group_input_94.Material -> group_026_1.Material
			style_spheres.links.new(group_input_94.outputs[6], group_026_1.inputs[5])
			#join_geometry_2.Geometry -> group_output_95.Geometry
			style_spheres.links.new(join_geometry_2.outputs[0], group_output_95.inputs[0])
			#realize_instances_2.Geometry -> join_geometry_2.Geometry
			style_spheres.links.new(realize_instances_2.outputs[0], join_geometry_2.inputs[0])
			#group_026_1.Instances -> realize_instances_2.Geometry
			style_spheres.links.new(group_026_1.outputs[0], realize_instances_2.inputs[0])
			#separate_geometry_3.Inverted -> group_014_5.Atoms
			style_spheres.links.new(separate_geometry_3.outputs[1], group_014_5.inputs[0])
			#separate_geometry_3.Selection -> group_026_1.Atoms
			style_spheres.links.new(separate_geometry_3.outputs[0], group_026_1.inputs[0])
			#group_014_5.Point Cloud -> join_geometry_2.Geometry
			style_spheres.links.new(group_014_5.outputs[0], join_geometry_2.inputs[0])
			return style_spheres

		style_spheres = style_spheres_node_group()

		#initialize mn_1fap_001 node group
		def glow_nodetree_group():
			glow_nodetree = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "MN_1FAP.001")

			glow_nodetree.color_tag = 'NONE'
			glow_nodetree.description = ""


			#mn_1fap_001 interface
			#Socket Geometry
			geometry_socket_19 = glow_nodetree.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
			geometry_socket_19.attribute_domain = 'POINT'

			#Socket Geometry
			geometry_socket_20 = glow_nodetree.interface.new_socket(name = "Geometry", in_out='INPUT', socket_type = 'NodeSocketGeometry')
			geometry_socket_20.attribute_domain = 'POINT'


			#initialize mn_1fap_001 nodes
			#node Group Input
			group_input_95 = glow_nodetree.nodes.new("NodeGroupInput")
			group_input_95.name = "Group Input"

			#node Group Output
			group_output_96 = glow_nodetree.nodes.new("NodeGroupOutput")
			group_output_96.name = "Group Output"
			group_output_96.is_active_output = True

			#node Style Cartoon
			style_cartoon_1 = glow_nodetree.nodes.new("GeometryNodeGroup")
			style_cartoon_1.name = "Style Cartoon"
			style_cartoon_1.node_tree = style_cartoon
			#Input_1
			style_cartoon_1.inputs[1].default_value = True
			#Input_2
			style_cartoon_1.inputs[2].default_value = 2
			#Socket_3
			style_cartoon_1.inputs[3].default_value = False
			#Input_4
			style_cartoon_1.inputs[4].default_value = False
			#Input_3
			style_cartoon_1.inputs[5].default_value = True
			#Input_11
			style_cartoon_1.inputs[6].default_value = False
			#Input_5
			style_cartoon_1.inputs[7].default_value = 0.6000000238418579
			#Input_6
			style_cartoon_1.inputs[8].default_value = 2.200000047683716
			#Input_12
			style_cartoon_1.inputs[9].default_value = 0.4000000059604645
			#Input_7
			style_cartoon_1.inputs[10].default_value = 0.5
			#Socket_1
			style_cartoon_1.inputs[11].default_value = True
			#Input_8
			style_cartoon_1.inputs[12].default_value = True
			if "MN Default" in bpy.data.materials:
				style_cartoon_1.inputs[13].default_value = bpy.data.materials["MN Default"]

			#node Set Color
			set_color_1 = glow_nodetree.nodes.new("GeometryNodeGroup")
			set_color_1.name = "Set Color"
			set_color_1.node_tree = set_color
			#Input_15
			set_color_1.inputs[1].default_value = True

			#node Color Common
			color_common_1 = glow_nodetree.nodes.new("GeometryNodeGroup")
			color_common_1.name = "Color Common"
			color_common_1.node_tree = color_common
			#Input_4
			color_common_1.inputs[1].default_value = (0.20190106332302094, 0.20190106332302094, 0.20190106332302094, 1.0)
			#Input_5
			color_common_1.inputs[2].default_value = (0.1599999964237213, 0.2333349734544754, 0.800000011920929, 1.0)
			#Input_6
			color_common_1.inputs[3].default_value = (0.800000011920929, 0.16102071106433868, 0.1599999964237213, 1.0)
			#Input_7
			color_common_1.inputs[4].default_value = (0.8000000715255737, 0.1718127280473709, 0.525249719619751, 1.0)
			#Input_8
			color_common_1.inputs[5].default_value = (0.8000000715255737, 0.7220579385757446, 0.051990706473588943, 1.0)

			#node Color Attribute Random
			color_attribute_random_1 = glow_nodetree.nodes.new("GeometryNodeGroup")
			color_attribute_random_1.name = "Color Attribute Random"
			color_attribute_random_1.node_tree = color_attribute_random
			#Input_0
			color_attribute_random_1.inputs[0].default_value = "chain_id"
			#Input_2
			color_attribute_random_1.inputs[1].default_value = 0.6000000238418579
			#Input_3
			color_attribute_random_1.inputs[2].default_value = 0.6000000238418579
			#Input_4
			color_attribute_random_1.inputs[3].default_value = 0

			#node Separate Polymers
			separate_polymers_1 = glow_nodetree.nodes.new("GeometryNodeGroup")
			separate_polymers_1.label = "Separate Polymers"
			separate_polymers_1.name = "Separate Polymers"
			separate_polymers_1.node_tree = separate_polymers

			#node Style Spheres
			style_spheres_1 = glow_nodetree.nodes.new("GeometryNodeGroup")
			style_spheres_1.label = "Style Spheres"
			style_spheres_1.name = "Style Spheres"
			style_spheres_1.node_tree = style_spheres
			#Input_1
			style_spheres_1.inputs[1].default_value = True
			#Input_2
			style_spheres_1.inputs[2].default_value = False
			#Input_3
			style_spheres_1.inputs[3].default_value = 0.800000011920929
			#Input_4
			style_spheres_1.inputs[4].default_value = 2
			#Input_5
			style_spheres_1.inputs[5].default_value = True
			if "GreenGLow" in bpy.data.materials:
				style_spheres_1.inputs[6].default_value = bpy.data.materials["GreenGlow"]

			#node Color
			color = glow_nodetree.nodes.new("FunctionNodeInputColor")
			color.name = "Color"
			color.value = (0.35422274470329285, 0.3680456876754761, 0.4998120665550232, 1.0)

			#node Group
			group_36 = glow_nodetree.nodes.new("GeometryNodeGroup")
			group_36.name = "Group"
			group_36.node_tree = set_color
			#Input_15
			group_36.inputs[1].default_value = True

			#node Join Geometry
			join_geometry_3 = glow_nodetree.nodes.new("GeometryNodeJoinGeometry")
			join_geometry_3.name = "Join Geometry"

			#node Group.001
			group_001_24 = glow_nodetree.nodes.new("GeometryNodeGroup")
			group_001_24.name = "Group.001"
			group_001_24.node_tree = style_cartoon
			#Input_1
			group_001_24.inputs[1].default_value = True
			#Input_2
			group_001_24.inputs[2].default_value = 2
			#Socket_3
			group_001_24.inputs[3].default_value = False
			#Input_4
			group_001_24.inputs[4].default_value = False
			#Input_3
			group_001_24.inputs[5].default_value = True
			#Input_11
			group_001_24.inputs[6].default_value = False
			#Input_5
			group_001_24.inputs[7].default_value = 0.6000000238418579
			#Input_6
			group_001_24.inputs[8].default_value = 2.200000047683716
			#Input_12
			group_001_24.inputs[9].default_value = 0.4000000059604645
			#Input_7
			group_001_24.inputs[10].default_value = 0.5
			#Socket_1
			group_001_24.inputs[11].default_value = True
			#Input_8
			group_001_24.inputs[12].default_value = True




			#Set locations
			group_input_95.location = (-311.7392578125, 202.91488647460938)
			group_output_96.location = (952.3370361328125, -27.03854751586914)
			style_cartoon_1.location = (439.3011169433594, 324.5626220703125)
			set_color_1.location = (216.04833984375, 294.246337890625)
			color_common_1.location = (-105.60498046875, -378.2232666015625)
			color_attribute_random_1.location = (-464.44403076171875, -315.0353088378906)
			separate_polymers_1.location = (-70.58402252197266, 118.24871826171875)
			style_spheres_1.location = (433.6322021484375, -275.1498107910156)
			color.location = (-273.1452941894531, 583.984619140625)
			group_36.location = (190.66256713867188, -310.68280029296875)
			join_geometry_3.location = (724.6257934570312, -125.4471435546875)
			group_001_24.location = (427.2284851074219, 102.12726593017578)

			#Set dimensions
			group_input_95.width, group_input_95.height = 140.0, 100.0
			group_output_96.width, group_output_96.height = 140.0, 100.0
			style_cartoon_1.width, style_cartoon_1.height = 180.0, 100.0
			set_color_1.width, set_color_1.height = 180.0, 100.0
			color_common_1.width, color_common_1.height = 180.0, 100.0
			color_attribute_random_1.width, color_attribute_random_1.height = 180.0, 100.0
			separate_polymers_1.width, separate_polymers_1.height = 180.0, 100.0
			style_spheres_1.width, style_spheres_1.height = 180.0, 100.0
			color.width, color.height = 140.0, 100.0
			group_36.width, group_36.height = 140.0, 100.0
			join_geometry_3.width, join_geometry_3.height = 140.0, 100.0
			group_001_24.width, group_001_24.height = 140.0, 100.0

			#initialize glow_nodetree links
			#set_color_1.Atoms -> style_cartoon_1.Atoms
			glow_nodetree.links.new(set_color_1.outputs[0], style_cartoon_1.inputs[0])
			#group_input_95.Geometry -> separate_polymers_1.Atoms
			glow_nodetree.links.new(group_input_95.outputs[0], separate_polymers_1.inputs[0])
			#separate_polymers_1.Peptide -> set_color_1.Atoms
			glow_nodetree.links.new(separate_polymers_1.outputs[0], set_color_1.inputs[0])
			#color.Color -> set_color_1.Color
			glow_nodetree.links.new(color.outputs[0], set_color_1.inputs[2])
			#separate_polymers_1.Other -> group_36.Atoms
			glow_nodetree.links.new(separate_polymers_1.outputs[2], group_36.inputs[0])
			#color_common_1.Color -> group_36.Color
			glow_nodetree.links.new(color_common_1.outputs[0], group_36.inputs[2])
			#color_attribute_random_1.Color -> color_common_1.Hydrogen
			glow_nodetree.links.new(color_attribute_random_1.outputs[0], color_common_1.inputs[0])
			#group_36.Atoms -> style_spheres_1.Atoms
			glow_nodetree.links.new(group_36.outputs[0], style_spheres_1.inputs[0])
			#join_geometry_3.Geometry -> group_output_96.Geometry
			glow_nodetree.links.new(join_geometry_3.outputs[0], group_output_96.inputs[0])
			#separate_polymers_1.Nucleic -> group_001_24.Atoms
			glow_nodetree.links.new(separate_polymers_1.outputs[1], group_001_24.inputs[0])
			#group_001_24.Geometry -> join_geometry_3.Geometry
			glow_nodetree.links.new(group_001_24.outputs[0], join_geometry_3.inputs[0])
			#style_cartoon_1.Geometry -> join_geometry_3.Geometry
			glow_nodetree.links.new(style_cartoon_1.outputs[0], join_geometry_3.inputs[0])
			#style_spheres_1.Geometry -> join_geometry_3.Geometry
			glow_nodetree.links.new(style_spheres_1.outputs[0], join_geometry_3.inputs[0])
			return glow_nodetree

		glow_nodetree = glow_nodetree_group()

		name = bpy.context.object.name
		obj = bpy.data.objects[name]
		mod = obj.modifiers.new(name = "GlowNode", type = 'NODES')
		mod.node_group = glow_nodetree
		return {'FINISHED'}

def menu_func(self, context):
	self.layout.operator(LigandGlow.bl_idname)

def register():
	bpy.utils.register_class(LigandGlow)
	bpy.types.NODE_MT_add.append(menu_func)

def unregister():
	bpy.utils.unregister_class(LigandGlow)
	bpy.types.NODE_MT_add.remove(menu_func)

if __name__ == "__main__":
	register()
