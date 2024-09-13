# Minimal Blender + Molecular Nodes CLI

## Running

Takes a PDB file and an output location and returns a GIF of the protein animated by B-factor.

```sh
pixi run help

# (base) zcpowers@Zacharys-MacBook-Air wobble % pixi run help
# ✨ Pixi task (help): wobble --help
# Usage: wobble [OPTIONS] COMMAND [ARGS]...
#
#   Main command group for protein wobble animations.
#
# Options:
#   --help  Show this message and exit.
#
# Commands:
#   create-protein-animation  Create a protein animation from a PDB code...
#   glowing-ligand            Create an image of a glowing ligand.

pixi run example  # this makes the example in this directory ...
pixi run wobble   # entrypoint to click handler
```

## Result

![](./1FAP_animation.gif)

## Background

This is a distilled version of [mol-nodes utils](https://github.com/zachcp/molnodes-utils). Basically, you need only extract a node gorup of interest
and register it as a class for it to be available for use as a node in a scriptable environment. It opens up the possibility o making
custom, reproducible figures on top of Molecular Nodes
