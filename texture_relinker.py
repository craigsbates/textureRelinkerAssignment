"""Functions to relink textures in maya."""

import os

import maya.cmds as cmds
from PySide6 import QtWidgets


def texture_relinker(texture_dir):
    """Takes the given folder, traverses immediate sub directories to relink
    textures based on their file name.

    Args:
        texture_dir (str): Directory containing texture files.
    """
    all_file_nodes = cmds.ls(type="file")
    broken_file_nodes = [
        i for i in all_file_nodes
        if not os.path.exists(cmds.getAttr(f"{i}.fileTextureName"))
    ]
    all_texture_dirs = [x[0] for x in os.walk(texture_dir)]

    for i in broken_file_nodes:
        filepath = cmds.getAttr(f"{i}.fileTextureName")
        basename = os.path.basename(filepath)

        for path in all_texture_dirs:
            new_texture_path = os.path.join(path, basename)
            if os.path.exists(new_texture_path):
                cmds.setAttr(f"{i}.fileTextureName", new_texture_path, type="string")
                break


class PathField(QtWidgets.QWidget):
    """Widget that combines LineEdit and PushButton."""

    def __init__(self):
        super(PathField, self).__init__()
        self.line = QtWidgets.QLineEdit()
        self.browse_button = QtWidgets.QPushButton("Select Folder")

        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)

        layout.addWidget(self.line)
        layout.addWidget(self.browse_button)

        self.browse_button.clicked.connect(self.get_path)

    @property
    def path(self):
        """Path property to access path LineEdit data.

        Returns:
            str: Selected Path from FileDialog.
        """
        raw = self.line.text()
        if not raw:
            return ""
        return os.path.normpath(raw)

    def get_path(self):
        """Open a QFileDialog to select a folder, defaults to scene location."""
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select a folder", cmds.file(q=True, sn=True)
        )

        if path:
            self.line.setText(os.path.normpath(path))


class RelinkTextureMain(QtWidgets.QMainWindow):
    """Main UI to select folder and run relink textures."""

    def __init__(self):
        """Initialiser for the UI elements."""
        super(RelinkTextureMain, self).__init__()

        self.setWindowTitle("Texture Relinker")
        self.resize(750, 100)

        self.folder_field = PathField()
        self.relink_button = QtWidgets.QPushButton("Relink Textures")

        ui_layout = QtWidgets.QVBoxLayout()
        ui_layout.addWidget(self.folder_field)
        ui_layout.addWidget(self.relink_button)

        widget = QtWidgets.QWidget()
        widget.setLayout(ui_layout)
        self.setCentralWidget(widget)

        self.relink_button.clicked.connect(self._relink_textures)

    def _relink_textures(self):
        """Run relink textures if a folder is selected."""
        textures_dir = self.folder_field.path
        if textures_dir:
            texture_relinker(textures_dir)
