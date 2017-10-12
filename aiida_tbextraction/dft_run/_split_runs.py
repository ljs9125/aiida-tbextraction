try:
    from collections import ChainMap
except ImportError:
    from chainmap import ChainMap

from aiida.work.run import submit
from aiida.work.workchain import ToContext

from ._base import DFTRunBase
from .reference_bands import ReferenceBandsBase
from .wannier_input import WannierInputBase

from .._utils import check_workchain_step
from .._workchain_inputs import WORKCHAIN_INPUT_KWARGS


class SplitDFTRun(DFTRunBase):
    """
    Independently runs the DFT calculations for creating the reference bands and Wannier90 input.
    """

    @classmethod
    def define(cls, spec):
        super(SplitDFTRun, cls).define(spec)

        spec.input('reference_bands_workflow', **WORKCHAIN_INPUT_KWARGS)
        spec.input('to_wannier90_workflow', **WORKCHAIN_INPUT_KWARGS)

        # Add dynamic namespaces
        spec.expose_inputs(
            ReferenceBandsBase, namespace='reference_bands', include=[]
        )
        spec.expose_inputs(
            WannierInputBase, namespace='to_wannier90', include=[]
        )

        spec.outline(cls.dft_run, cls.finalize)

    @check_workchain_step
    def dft_run(self):
        self.report('Submitting reference_bands workflow.')
        reference_bands = submit(
            self.get_deserialized_input('reference_bands_workflow'),
            **ChainMap(
                self.inputs['reference_bands'],
                self.exposed_inputs(
                    ReferenceBandsBase, namespace='reference_bands'
                )
            )
        )
        self.report('Submitting to_wannier90 workflow.')
        to_wannier90 = submit(
            self.get_deserialized_input('to_wannier90_workflow'),
            **ChainMap(
                self.inputs['to_wannier90'],
                self.exposed_inputs(
                    WannierInputBase, namespace='to_wannier90'
                )
            )
        )
        return ToContext(
            reference_bands=reference_bands, to_wannier90=to_wannier90
        )

    @check_workchain_step
    def finalize(self):
        self.out_many(
            **self.exposed_outputs(
                self.ctx.reference_bands, ReferenceBandsBase
            )
        )
        self.out_many(
            **self.exposed_outputs(self.ctx.to_wannier90, WannierInputBase)
        )