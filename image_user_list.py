# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


import bpy


bl_info = {
    "name": "Image User List",
    "author": "todashuta",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "Image Editor > Sidebar > Image > Image User List",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Image"
}


class IMAGE_USER_LIST_PT_panel(bpy.types.Panel):
    bl_label = "Image User List"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Image"

    def draw(self, context):
        if hasattr(context.space_data, "image"):
            if context.space_data.image is None:
                return
        image = context.space_data.image
        layout = self.layout
        for m in bpy.data.materials:
            if not m.use_nodes:
                continue
            if len([n for n in m.node_tree.nodes if n.type == "TEX_IMAGE" and n.image == image]) > 0:
                layout.label(icon="MATERIAL", text=m.name)


classes = [
    IMAGE_USER_LIST_PT_panel,
]


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
