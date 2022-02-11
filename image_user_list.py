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
    "version": (1, 4, 1),
    "blender": (2, 80, 0),
    "location": "Image Editor > Sidebar > Image > Image User List",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Image"
}


translation_dict = {
        "en_US": {
            ("Operator", "Search"): "Search",
            ("*", "Search This Name in Outliner"): "Search This Name in Outliner",
            ("*", "Filter `Exact Match' Enabled."): "Filter `Exact Match' Enabled.",
            ("*", "Copy Name to Clipboard"): "Copy Name to Clipboard",
            ("*", "No Items."): "No Items.",
        },
        "ja_JP": {
            ("Operator", "Search"): "検索",
            ("*", "Search This Name in Outliner"): "アウトライナーでこの名前を検索します",
            ("*", "Filter `Exact Match' Enabled."): "「完全に一致」をオンにしました。",
            ("*", "Copy Name to Clipboard"): "名前をクリップボードにコピーします",
            ("*", "No Items."): "該当なし",
        },
}


class IMAGE_USER_LIST_OT_search_in_outliner(bpy.types.Operator):
    bl_idname = "image.image_user_list_search_in_outliner"
    bl_label = "Search"
    bl_description = "Search This Name in Outliner"
    bl_options = {"INTERNAL"}

    filter_text: bpy.props.StringProperty(default="", options={"HIDDEN"})

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        for area in context.screen.areas:
            if area.type == "OUTLINER":
                for space in area.spaces:
                    if space.type == "OUTLINER" and space.display_mode == "VIEW_LAYER":
                        space.filter_text = self.filter_text
                        if not space.use_filter_complete:
                            space.use_filter_complete = True
                            self.report({"INFO"}, "Filter `Exact Match' Enabled.")
        return {"FINISHED"}


class IMAGE_USER_LIST_OT_set_clipboard(bpy.types.Operator):
    bl_idname = "image.image_user_list_set_clipboard"
    bl_label = "Copy"
    bl_description = "Copy Name to Clipboard"
    bl_options = {"INTERNAL"}

    content: bpy.props.StringProperty(default="", options={"HIDDEN"})

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        context.window_manager.clipboard = self.content

        return {"FINISHED"}


#def get_material_list_callback(scene, context):
#    items = []
#    if not hasattr(context.space_data, "image"):
#        return items
#    if context.space_data.image is None:
#        return items
#    image = context.space_data.image
#    for m in bpy.data.materials:
#        if not m.use_nodes:
#            continue
#        if len([n for n in m.node_tree.nodes if n.type == "TEX_IMAGE" and n.image == image]) > 0:
#            items.append((m.name, m.name, ""))
#    return items


#def filter_image_user_materials(self, mat):
#    context = bpy.context
#    if not hasattr(context.space_data, "image"):
#        return False
#    if context.space_data.image is None:
#        return False
#    image = context.space_data.image
#    users = []
#    for m in bpy.data.materials:
#        if not m.use_nodes:
#            continue
#        if len([n for n in m.node_tree.nodes if n.type == "TEX_IMAGE" and n.image == image]) > 0:
#            users.append(m)
#    return mat.name in [u.name for u in users]


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
        #layout.prop(context.scene, "image_user_list_search", text="")
        #layout.operator(IMAGE_USER_LIST_OT_search.bl_idname)
        #layout.separator()
        layout.label(text="Materials:")
        found = False
        for m in bpy.data.materials:
            if not m.use_nodes:
                continue
            ns = [n for n in m.node_tree.nodes if n.type == "TEX_IMAGE" and n.image == image]
            #print(ns)
            len_ = len(ns)
            if len_ > 0:
                found = True
                split = layout.split(factor=0.7)
                split.label(icon="MATERIAL", text=f"{m.name}", translate=False)
                split.operator(IMAGE_USER_LIST_OT_set_clipboard.bl_idname, text="", icon="COPY_ID").content = m.name
                split.operator(IMAGE_USER_LIST_OT_search_in_outliner.bl_idname, text="", icon="VIEWZOOM").filter_text = m.name
                col = layout.column(align=True)
                for n in sorted(ns, key=lambda it: it.name):
                    num_color_links = len(n.outputs['Color'].links)
                    num_alpha_links = len(n.outputs['Alpha'].links)
                    if num_color_links > 0 or num_alpha_links > 0:
                        icon = "LINKED"
                        s = f" (Col:{num_color_links}, Alp:{num_alpha_links})"
                    else:
                        icon = "UNLINKED"
                        s = "" #" (Not Connected)"
                    split = col.split(factor=0.04)
                    split.label(text="")
                    split.label(icon=icon, text=f"{n.name}{s}", translate=False)
        if not found:
            layout.label(icon="INFO", text="No Items.")


classes = [
        IMAGE_USER_LIST_OT_search_in_outliner,
        IMAGE_USER_LIST_OT_set_clipboard,
        IMAGE_USER_LIST_PT_panel,
]


def register():
    #bpy.types.Scene.image_user_list_search = bpy.props.PointerProperty(
    #        type=bpy.types.Material,
    #        poll=filter_image_user_materials
    #)

    for c in classes:
        bpy.utils.register_class(c)

    bpy.app.translations.register(__name__, translation_dict)


def unregister():
    #if hasattr(bpy.types.Scene, "image_user_list_search"):
    #    del bpy.types.Scene.image_user_list_search

    bpy.app.translations.unregister(__name__)

    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
