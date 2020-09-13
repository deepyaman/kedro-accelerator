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

As of Kedro 0.16.4, `TeePlugin`—the core of Kedro-Accelerator—will be auto-discovered upon [installation](#how-do-i-install-kedro-accelerator). In older versions, [hook implementations should be registered with Kedro through the `ProjectContext`](https://kedro.readthedocs.io/en/0.16.3/04_user_guide/15_hooks.html#registering-your-hook-implementations-with-kedro). Hooks were introduced in Kedro 0.16.0.

### Prerequisites

The following conditions must be true for Kedro-Accelerator to speed up your pipeline:

* Your pipeline must not use transcoding.
* Your project must use `SequentialRunner`.

## What license do you use?

Kedro-Airflow is licensed under the [MIT](LICENSE) License.
