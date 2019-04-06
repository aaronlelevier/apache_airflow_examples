# TFX Notes

## Summary

Notes on [https://github.com/tensorflow/tfx](https://github.com/tensorflow/tfx) as I learn the code base and how it uses Apache Airflow.

## Notes

`AirflowDAGRunner` - returns the main DAG and SubDag's

`AirflowPipeline` - return the main DAG

`_TfxWorker` - is the SubDagOperator for each step in the TFX Pipeline

## CsvExampleGen

### checkcache

`chicago_taxi_simple.CsvExampleGen.checkcache`

Uses the `metadata.Metadata` and CsvExampleGen custom `Driver` to check if inputs already exist

`TfxType`'s are created that have a `uri`. The `uri` is a filepath. This `uri` is then compared against in the `Metadata` store to see if the artifact exists. `Metadata` is a Database, defaulted to:

`$TFX_DIR/metadata/chicago_taxi_simple/metadata.db`

### exec