# A Practical Intro to Airflow - Notes

Notes on this talk: [https://youtu.be/cHATHSB_450](https://youtu.be/cHATHSB_450)

**metadata db**

sqlite

mysql

postgres

**webserver**

flask

**scheduler**

nothing can run without this

crawls the configured dir's to find DAGs

**celery**

tasks are sent from the scheduler to run on Celery workers

would use *rabbitmq* or *redis* for Celery Queue

## Airflow objects

Tasks

Executors (workers)

## Code

**Useful DAG Arguments**

`start_date` - will say when to start, if in the past, Airflow will backfill the tasks to that date based on the `schedule_interval`

- can put the `start_date` for the future, if we don't want it to run yet

`schedule_interval` - cron config

- max interval to run should be at fractions of hour, not per minute, because Airflow kicks off tasks every 30 seconds

`default_args` - arguments supplied to the `DAG`, but get passed to the `Operators`

`max_active_runs` - can set globally or per Pipeline how may parallel pipelines to run at the same time

`concurrency` - max number of tasks run in a single Pipeline to run at a sinble time

can retry tasks

can put timeouts in Pipeline for when tasks start

**Useful Task Arguments**

`retries` -how many times to retry

`pool` - a worker pool - can limit slots here

`queue` - named Celery Queues - and assign certain Workers to a Queue based upon the type of Worker if biefy, lightweight, etc..

`execution_timeout` - set a max time for a Task to run

`trigger_rule` - default is "all upstream tasks are successful. Can change to things like

- "all upstream tasks failed"
- "all upstream tasks are done" - either success or fail

args for python

env vars

template vars

`provide_context` - supplies a dict of Task arguments, like "execution date", from Airflow context

`op_args` - positional arguments for the Task

`op_kwargs` - kwarg arguments supplied to the Task

**Executors**

`CeleryExecutor` - for prod, puts exec request on a queue and sends it to a Celery Worker

`SequentialExecutor` - good for debugging, will stop scheduling to run Tasks

`LocalExecutor` - uses Python's `multiprocess` module to run in a diff process, so Scheduler can continue scheduling things

- used in Prod for some companies - if don't want a distributed worker queue

`MesosExecutor`

**Local debugging**

To use `pdb`, use the `SequentialExecutor`, and run `airflow test` to hit `pdb` debugger

**Local Pipeline testing**

`start_date` - should be some date in the past

`schedule_interval='@once'`

can delete a DAG using the UI, in order to re-run this Local Pipeline for testing

**Separate Business Logic**

develop code first, then integrate with Airflow

**Deploying new code**

to get new Python code, we have to restart the process, so new code is imported. to do this with Airflow, we can do

`airflow scheduler --num_runs` - this will stop the scheduler after `num_runs` has occurred. You need a separate mechanism to restart the scheduler. Speaker uses a bash script

`CELERYD_MAX_TASKS_PER_CHILD` - will configure Celery workers to restart after the "max tasks"

speaker sets the above to 1 max, so each run, always gets new deployed code
