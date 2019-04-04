# TFX Notes

## Summary

Notes on [https://github.com/tensorflow/tfx](https://github.com/tensorflow/tfx) as I learn the code base and how it uses Apache Airflow.

## Notes

`AirflowDAGRunner` - returns the main DAG and SubDag's

`AirflowPipeline` - return the main DAG

`_TfxWorker` - is the SubDagOperator for each step in the TFX Pipeline
