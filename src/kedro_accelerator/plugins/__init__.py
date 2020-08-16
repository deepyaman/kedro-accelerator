from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict

from kedro.framework.hooks import hook_impl
from kedro.io import CachedDataSet, DataCatalog, MemoryDataSet
from kedro.pipeline import Pipeline


class TeePlugin:
    @hook_impl
    def before_pipeline_run(self, pipeline: Pipeline, catalog: DataCatalog) -> None:
        # Create a copy of the unmodified data catalog for future saves.
        self.physical_catalog = catalog.shallow_copy()

        # Replace intermediate inputs and outputs with in-memory stores.
        # TODO(deepyaman): Identify the default data set for the runner.
        self.data_set_names = set(catalog.list())
        catalog.add_all(
            {
                name: MemoryDataSet()
                for name in self.data_set_names - pipeline.inputs() - pipeline.outputs()
            },
            replace=True,
        )

        self.pool = ThreadPoolExecutor()
        self.save_futures = set()

    @hook_impl
    def after_node_run(self, catalog: DataCatalog, outputs: Dict[str, Any]) -> None:
        for name, data in outputs.items():
            if name in self.data_set_names:  # ``DataSet`` is registered
                physical_dataset = getattr(self.physical_catalog.datasets, name)

                # If the intermediate data set was "replaced," persist a
                # copy of the output data with the original save method.
                if getattr(catalog.datasets, name) is not physical_dataset:
                    self.save_futures.add(
                        self.pool.submit(self.physical_catalog.save, name, data)
                    )

    def _cleanup(self):
        try:
            for future in as_completed(self.save_futures):
                exception = future.exception()
                if exception:
                    raise exception
        finally:
            self.pool.shutdown(wait=True)

    @hook_impl
    def after_pipeline_run(self) -> None:
        self._cleanup()

    @hook_impl
    def on_pipeline_error(self) -> None:
        self._cleanup()


hooks = TeePlugin()


class CachePlugin:
    @hook_impl
    def before_pipeline_run(self, pipeline: Pipeline, catalog: DataCatalog) -> None:
        # Wrap intermediate inputs and outputs using ``CachedDataSet``s.
        catalog.add_all(
            {
                name: CachedDataSet(getattr(catalog.datasets, name))
                for name in set(catalog.list()) - pipeline.inputs() - pipeline.outputs()
            },
            replace=True,
        )
