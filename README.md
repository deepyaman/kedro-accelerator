# Kedro-Accelerator

Kedro pipelines consist of nodes, where an output from one node _A_ can be an input to another node _B_. The Data Catalog defines where and how Kedro loads and saves these inputs and outputs, respectively. By default, a sequential Kedro pipeline:

1. runs node _A_
2. persists the output of _A_, often to remote storage like Amazon S3
3. potentially runs other nodes
4. fetches the output of _A_, loading it back into memory
5. runs node _B_

Persisting intermediate data sets enables partial pipeline runs (e.g. running node _B_ without rerunning node _A_) and analysis/debugging of these data sets. However, the I/O in steps 2 and 4 above was not necessary to run node _B_, given the requisite data was already in memory after step 1. Kedro-Accelerator speeds up pipelines by parallelizing this I/O in the background.

## How do I install Kedro-Accelerator?

Kedro-Accelerator is a Python plugin. To install it:

```bash
pip install kedro-accelerator
```

## How do I use Kedro-Accelerator?

As of Kedro 0.16.4, `TeePlugin`—the core of Kedro-Accelerator—will be auto-discovered upon [installation](https://github.com/deepyaman/kedro-accelerator/blob/v0.1.0/README.md#how-do-i-install-kedro-accelerator). In older versions, [hook implementations should be registered with Kedro through the `ProjectContext`](https://kedro.readthedocs.io/en/0.16.3/04_user_guide/15_hooks.html#registering-your-hook-implementations-with-kedro). Hooks were introduced in Kedro 0.16.0.

### Prerequisites

The following conditions must be true for Kedro-Accelerator to speed up your pipeline:

- Your project must use either `SequentialRunner` or `ParallelRunner`.

### Example

The Kedro-Accelerator repository includes the Iris data set example pipeline generated using Kedro 0.16.1. Intermediate data sets have been replaced with custom `SlowDataSet` instances to simulate a slow filesystem. You can try different load and save delays by modifying [`catalog.yml`](https://github.com/deepyaman/kedro-accelerator/blob/v0.1.0/conf/base/catalog.yml).

To get started, [create and activate a new virtual environment](https://kedro.readthedocs.io/en/0.17.4/02_get_started/01_prerequisites.html#virtual-environments). Then, clone the repository and pip install requirements:

```bash
git clone https://github.com/deepyaman/kedro-accelerator.git
cd kedro-accelerator
KEDRO_VERSION=0.17.4 pip install -r src/requirements.txt  # Specify your desired Kedro version.
```

You can compare pipeline execution times with and without `TeePlugin`. Kedro-Accelerator also provides `CachePlugin` so that you can test performance using `CachedDataSet` in asynchronous mode. Assuming parametrized load and save delays of 10 seconds for intermediate datasets, you should see the following results:

| Strategy                                                  | Command                                                           | Total time                                                                  | Log                                                                                |
| --------------------------------------------------------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Baseline (i.e. no caching/plugins)                        | `kedro run`                                                       | 2 minutes                                                                   | [Log](https://github.com/quantumblacklabs/kedro/issues/420#issuecomment-658320262) |
| `TeePlugin`                                               | `kedro run --hooks kedro_accelerator.plugins.TeePlugin`           | 10 seconds (saving all outputs)                                             | [Log](https://github.com/quantumblacklabs/kedro/issues/420#issuecomment-658323282) |
| `CachePlugin` (i.e. `CachedDataSet`) with `is_async=True` | `kedro run --async --hooks kedro_accelerator.plugins.CachePlugin` | 30 seconds (saving `split_data`, `train_model`, and `predict` node outputs) | [Log](https://github.com/quantumblacklabs/kedro/issues/420#issuecomment-658331422) |

Prior to Kedro version 0.17.0, prefix extra hooks passed to `kedro run` with `src.` (e.g. `src.kedro_accelerator.plugins.TeePlugin`).

For a more complete discussion of the above benchmarks, see [quantumblacklabs/kedro#420 (comment)](https://github.com/quantumblacklabs/kedro/issues/420#issuecomment-658320132).

## What license do you use?

Kedro-Accelerator is licensed under the [MIT](https://github.com/deepyaman/kedro-accelerator/blob/v0.1.0/LICENSE) License.
