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

### Prerequisites

The following conditions must be met to _accelerate_ your pipeline:
