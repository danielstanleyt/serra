![Project Header](./etc/serra.png)

# What is Serra?
Serra provides a library of readers, transformers and writers to simplify the process of writing data pipelines.

For example, you can specify that you want to read a CSV file from an S3 bucket, apply a transformation to the data, then write the data to a Snowflake table with the following config:

```yaml
step_read:
  AmazonS3Reader:
    bucket_name: serrademo
    file_path: sales.csv
    file_type: csv

step_map:
  MapTransformer:
    input_block: step_read
    name: 'state_abbreviation'
    map_dict_path: 'examples/states_to_abbreviation.json'
    col_key: 'region'

step_write:
  SnowflakeWriter:
   input_block: step_map
   warehouse: compute_wh
   database: serra
   schema: demo
   table: sales_mapped
   type: create
```

# How does it work?
Every step of the data pipeline corresponds to a specific class in the Serra framework. Above there are three classes that are used.

These are defined in the folders readers, writers, and transformers. If you decide you want to support a new type of step, you simply write corresponding PySpark code in a new file in these folders, and it is ready to use in your config! To chain together steps, supply the input_block, or prior step name!

# Getting Started
Create a new directory and run an interactive bash shell with docker to get started with all the required dependencies:

```bash
git clone https://github.com/Serra-Technologies/serra.git
cd serra
docker run --mount type=bind,source="$(pwd)",target=/app -it serraio/serra /bin/bash
```

Run `serra create` to create a workspace folder. 

```bash
serra create
```

Navigate to the workspace folder and run your first job!

```bash
cd workspace
serra run Demo
```

Other jobs available can be found in the **workspace/jobs** folder.

# Commands

## Test Locally
```bash
serra run {job_name}
```
Your job name is what you name your configuration file. Place your configuration files in **workspace/jobs** folder.

## Translate SQL to Serra Config File using GPT

Place your sql scripts in the **workspace/sql** folder.

```bash
cd workspace
serra translate hard_demo.sql
```

The translated config file can be found at **workspace/hard_demo.sql**

