import click
import bpy
import mathutils
import molecularnodes
import blendersynth as bsyn

try:
    molecularnodes.register()
except:
    pass

import wiggle
wiggle.register()


@click.command()
@click.argument('pdb_code', type=str)
@click.argument('output_path', type=click.Path())
@click.option('--frames', default=24, help='Number of frames for the animation')
@click.option('--resolution', default=512, help='Resolution of the output image')
@click.option('--samples', default=10, help='Number of Cycles samples')
def create_protein_animation(pdb_code, output_path, frames, resolution, samples):
    """
    Create a protein animation from a PDB code and save it to the specified output path.
    """
    # Load PDB
    load_pdb(pdb_code)

    # Set camera
    set_camera(1.2)

    # Increase lighting
    increase_lighting()

    # Remove MolecularNodes modifier and add WiggleProt
    obj = bpy.data.objects[pdb_code]
    nm = obj.modifiers.get("MolecularNodes")
    if nm:
        obj.modifiers.remove(nm)

    # note this is hacky.....
    bpy.ops.node.wiggleprot()

    # Set render settings
    bpy.context.scene.render.engine = "CYCLES"
    bpy.context.scene.render.film_transparent = True

    # Set up compositor
    comp = bsyn.Compositor()
    bsyn.render.set_cycles_samples(samples)
    bsyn.render.set_resolution(resolution, resolution)

    # Define output
    comp.define_output("Image", directory=output_path, file_name="test")

    # Render animation
    comp.render(animation=True, frame_end=frames)

    # Convert frames to video
    bsyn.file.frames_to_video(
        directory=output_path,
        output_loc=f"{output_path}/{pdb_code}_animation.gif",
        frame_rate=24,
        delete_images=False,
        output_fmt="gif",
    )

    click.echo(f"Animation created and saved to {output_path}/{pdb_code}_animation.gif")

def load_pdb(code):
    bpy.context.scene.MN_pdb_code = code
    bpy.context.scene.MN_import_style = "cartoon"
    bpy.context.scene.MN_import_centre = True
    bpy.ops.mn.import_wwpdb()

def set_camera(distance):
    camera = bpy.context.scene.camera
    camera.location = mathutils.Vector([distance, 0, 0])
    direction = mathutils.Vector([1, 0, 0])
    direction.normalize()
    up = mathutils.Vector([0, 0, 1])
    rotation = direction.to_track_quat("Z", "Y")
    camera.rotation_euler = rotation.to_euler()
    bpy.context.view_layer.update()

def increase_lighting():
    if "Extra_Light" not in bpy.data.objects:
        light_data = bpy.data.lights.new(name="Extra_Light", type="SUN")
        light_object = bpy.data.objects.new(name="Extra_Light", object_data=light_data)
        bpy.context.collection.objects.link(light_object)
    else:
        light_object = bpy.data.objects["Extra_Light"]

    light_object.data.energy = 2.0
    light_object.rotation_euler = (0.785, 0, 0.785)

    for obj in bpy.data.objects:
        if obj.type == "LIGHT":
            obj.data.energy *= 1.5

if __name__ == '__main__':
    create_protein_animation()
