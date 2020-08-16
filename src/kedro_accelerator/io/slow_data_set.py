"""``SlowDataSet`` is a ``MemoryDataSet`` with parametrizable delays."""
from time import sleep
from typing import Any

from kedro.io import MemoryDataSet

_EMPTY = object()


class SlowDataSet(MemoryDataSet):
    """``SlowDataSet`` loads and saves data from/to an in-memory
    Python object after a parametrized delay.

    Example:
    ::

        >>> from kedro_accelerator.io import SlowDataSet
        >>> import pandas as pd
        >>>
        >>> data = pd.DataFrame({'col1': [1, 2], 'col2': [4, 5],
        >>>                      'col3': [5, 6]})
        >>> data_set = SlowDataSet(1, 2, data=data)
        >>>
        >>> loaded_data = data_set.load()
        >>> assert loaded_data.equals(data)
        >>>
        >>> new_data = pd.DataFrame({'col1': [1, 2], 'col2': [4, 5]})
        >>> data_set.save(new_data)
        >>> reloaded_data = data_set.load()
        >>> assert reloaded_data.equals(new_data)

    """

    def __init__(
        self,
        load_delay: int,
        save_delay: int,
        data: Any = _EMPTY,
        copy_mode: str = None,
    ):
        """Creates a new instance of ``SlowDataSet`` pointing to the
        provided Python object.

        Args:
            load_delay: The number of seconds to wait before loading the
                data.
            save_delay: The number of seconds to wait before saving the
                data.
            data: Python object containing the data.
            copy_mode: The copy mode used to copy the data. Possible
                values are: "deepcopy", "copy" and "assign". If not
                provided, it is inferred based on the data type.
        """
        self._load_delay = load_delay
        self._save_delay = save_delay
        super().__init__(data, copy_mode)

    def __str__(self):
        return f"{super().__str__()} at {hex(id(self))}"

    def _load(self) -> Any:
        self._logger.debug("Loading %s", str(self))
        sleep(self._load_delay)
        data = super()._load()
        self._logger.debug("Loaded %s", str(self))
        return data

    def _save(self, data: Any):
        self._logger.debug("Saving %s", str(self))
        sleep(self._save_delay)
        super()._save(data)
        self._logger.debug("Saved %s", str(self))
