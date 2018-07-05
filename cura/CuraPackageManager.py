# Copyright (c) 2018 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher.

from cura.CuraApplication import CuraApplication #To find some resource types.
from cura.Settings.GlobalStack import GlobalStack

from UM.Logger import Logger
from UM.PackageManager import PackageManager #The class we're extending.
from UM.Resources import Resources #To find storage paths for some resource types.
from UM.Settings.ContainerRegistry import ContainerRegistry


class CuraPackageManager(PackageManager):
    def __init__(self, application, parent = None):
        super().__init__(application, parent)

    def initialize(self):
        self._installation_dirs_dict["materials"] = Resources.getStoragePath(CuraApplication.ResourceTypes.MaterialInstanceContainer)
        self._installation_dirs_dict["qualities"] = Resources.getStoragePath(CuraApplication.ResourceTypes.QualityInstanceContainer)

        super().initialize()

    ##  Returns a list of where the package is used
    #   empty if it is never used.
    #   It loops through all the package contents and see if some of the ids are used.
    def packageUsed(self, package_id: str):
        ids = self.packageContainerIds(package_id)
        container_stacks = ContainerRegistry.getInstance().findContainerStacks()
        global_stacks = [container_stack for container_stack in container_stacks if isinstance(container_stack, GlobalStack)]
        machine_with_materials = []
        machine_with_qualities = []
        for container_id in ids:
            for global_stack in global_stacks:
                for extruder_nr, extruder_stack in global_stack.extruders.items():
                    if container_id == extruder_stack.material.getId() or container_id == extruder_stack.material.getMetaData().get("base_file"):
                        machine_with_materials.append((global_stack, extruder_nr))
                    if container_id == extruder_stack.quality.getId():
                        machine_with_qualities.append((global_stack, extruder_nr))

        return machine_with_materials, machine_with_qualities
