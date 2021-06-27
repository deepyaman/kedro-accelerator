import inspect
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict

import kedro
from kedro.framework.hooks import hook_impl
from kedro.io import CachedDataSet, DataCatalog
from kedro.pipeline.pipeline import TRANSCODING_SEPARATOR, Pipeline
from kedro.runner import AbstractRunner


def _sub_nonword_chars(data_set_name: str) -> str:
    """Replace non-word characters in data set names since Kedro 0.16.2.

    Args:
        data_set_name: The data set name registered in the data catalog.

    Returns:
        The Kedro-version-dependent name used in `DataCatalog.datasets`.
    """
    if kedro.__version__ >= "0.16.6":
        # https://github.com/quantumblacklabs/kedro/commit/93e4cc3fe7a5ac3d4d7e6a372a2bcb26ce123b85
        return re.sub(r"\W+", "__", data_set_name)
    elif kedro.__version__ >= "0.16.2":
        # https://github.com/quantumblacklabs/kedro/commit/3faa0d454f3584f39285843f1ae28bec18cc3fee
        return re.sub("[^0-9a-zA-Z_]+", "__", data_set_name)
    else:
        return data_set_name


class TeePlugin:
    @hook_impl
    def before_pipeline_run(self, pipeline: Pipeline, catalog: DataCatalog) -> None:
        # Create a copy of the unmodified data catalog for future saves.
        self.physical_catalog = catalog.shallow_copy()

        # Get a reference to the runner object the pipeline is run with.
        runner = next(
            caller[0].f_locals.get("runner")
            for caller in inspect.stack()
            if isinstance(caller[0].f_locals.get("runner"), AbstractRunner)
        )

        # Replace intermediate inputs and outputs with in-memory stores.
        # Transcoding is a case where writing to disk is required, since
        # the act of reading/writing affects the object in the pipeline.
        self.data_set_names = set(catalog.list())
        catalog.add_all(
            {
                name: runner.create_default_data_set(name)
                for name in self.data_set_names - pipeline.inputs() - pipeline.outputs()
                if TRANSCODING_SEPARATOR not in name
            },
            replace=True,
        )

        self.pool = ThreadPoolExecutor()
        self.save_futures = set()

    @hook_impl
    def after_node_run(self, catalog: DataCatalog, outputs: Dict[str, Any]) -> None:
        for name, data in outputs.items():
            if name in self.data_set_names:  # ``DataSet`` is registered
                cleaned_name = _sub_nonword_chars(name)
                physical_dataset = getattr(self.physical_catalog.datasets, cleaned_name)

                # If the intermediate data set was "replaced," persist a
                # copy of the output data with the original save method.
                if getattr(catalog.datasets, cleaned_name) is not physical_dataset:
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
                name: CachedDataSet(getattr(catalog.datasets, _sub_nonword_chars(name)))
                for name in set(catalog.list()) - pipeline.inputs() - pipeline.outputs()
            },
            replace=True,
        )
