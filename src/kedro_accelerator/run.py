# Copyright 2020 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
# or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.

"""Application entry point."""
from pathlib import Path
from typing import Any, Dict, Tuple, Union

import kedro
from kedro.framework.context import KedroContext
from kedro.pipeline import Pipeline

from kedro_accelerator.pipeline import create_pipelines


class ProjectContext(KedroContext):
    """Users can override the remaining methods from the parent class here,
    or create new ones (e.g. as required by plugins)
    """

    project_name = "Kedro-Accelerator"
    # `project_version` is the version of kedro used to generate the project
    project_version = "0.16.1"
    package_name = "kedro_accelerator"

    def __init__(
        self,
        project_path: Union[Path, str],
        package_name: str = None,  # Argument not used before Kedro 0.17
        env: str = None,
        extra_params: Dict[str, Any] = None,
        extra_hooks: Tuple = None,
    ):
        """Create a context object by providing the root of a Kedro project and
        the environment configuration subfolders (see ``kedro.config.ConfigLoader``)

        Raises:
            KedroContextError: If there is a mismatch
                between Kedro project version and package version.

        Args:
            project_path: Project path to define the context for.
            package_name: Package name for the Kedro project the context is
                created for.
            env: Optional argument for configuration default environment to be used
                for running the pipeline. If not specified, it defaults to "local".
            extra_params: Optional dictionary containing extra project parameters.
                If specified, will update (and therefore take precedence over)
                the parameters retrieved from the project configuration.
            extra_hooks: Optional tuple containing extra hooks to extend
                KedroContext's execution. If specified, will be appended
                to the list of hooks provided by user.
        """
        if kedro.__version__ < "0.17":
            self.hooks += extra_hooks or ()
        super().__init__(package_name, project_path, env, extra_params)

    def _get_pipelines(self) -> Dict[str, Pipeline]:
        return create_pipelines()


def run_package():
    # Entry point for running a Kedro project packaged with `kedro package`
    # using `python -m <project_package>.run` command.
    from kedro.framework.context import load_package_context

    project_context = load_package_context(
        project_path=Path.cwd(), package_name=Path(__file__).resolve().parent.name
    )
    project_context.run()


if __name__ == "__main__":
    run_package()
