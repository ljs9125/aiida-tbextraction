# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines the base class for workflows that calculate the Wannier90 input files.
"""

from fsc.export import export

from aiida import orm
from aiida.engine import WorkChain


@export
class WannierInputBase(WorkChain):
    """
    The base class for WorkChains which can be used to calculate the Wannier90 input files. It defines the inputs required by these WorkChains.
    """
    @classmethod
    def define(cls, spec):
        super().define(spec)

        ParameterData = orm.Dict
        spec.input(
            'structure',
            valid_type=orm.StructureData,
            help='Structure of the material.'
        )
        spec.input(
            'kpoints_mesh',
            valid_type=orm.KpointsData,
            help='K-points mesh used when calculating the Wannier inputs.'
        )
        spec.input_namespace(
            'potentials',
            dynamic=True,
            help='Pseudopotentials used in the calculation.'
        )

        spec.input(
            'wannier_parameters',
            valid_type=ParameterData,
            required=False,
            help='Parameters of the Wannier calculation.'
        )
        spec.input(
            'wannier_projections',
            valid_type=(orm.OrbitalData, orm.List),
            required=False,
            help=
            'Projections used in the Wannier90 calculation, given either as ``OrbitalData``, or a list of strings corresponding to the lines in the ``wannier90.win`` projections input block.'
        )

        spec.output(
            'wannier_input_folder',
            valid_type=orm.FolderData,
            help=
            'Folder containing the ``.mmn``, ``.amn`` and ``.eig`` input files.'
        )
        spec.output(
            'wannier_parameters',
            valid_type=ParameterData,
            help='Parameters for the Wannier90 calculation.'
        )
        spec.output(
            'wannier_bands',
            valid_type=orm.BandsData,
            help='Bands parsed from the ``.eig`` file.'
        )
        spec.output(
            'wannier_settings',
            valid_type=ParameterData,
            required=False,
        )
        spec.output('wannier_projections', valid_type=orm.List, required=False)
