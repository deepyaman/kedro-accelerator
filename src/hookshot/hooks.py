from kedro.framework.hooks import hook_impl
from kedro.io import DataCatalog, MemoryDataSet
from kedro.pipeline import Pipeline


class TeePlugin:
    @hook_impl
    def before_pipeline_run(self, pipeline: Pipeline, catalog: DataCatalog) -> None:
        # Create a copy of the unmodified data catalog for future saves.
        self.physical_catalog = catalog.shallow_copy()

        # Replace intermediate inputs and outputs with in-memory stores.
        # TODO(deepyaman): Identify the default data set for the runner.
        catalog.add_all(
            {
                name: MemoryDataSet()
                for name in set(catalog.list()) - pipeline.inputs() - pipeline.outputs()
            },
            replace=True,
        )
