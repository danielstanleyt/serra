# Entry point for serra command line tool
import sys
import click
import boto3
import botocore
import os
from serra.run import run_job_from_job_dir, update_package, create_job_yaml, run_job_from_aws, translate_job
from serra.databricks import create_job
from serra.aws import download_folder_from_s3
from serra.utils import validate_workspace

@click.group()
def main():
    pass

@main.command(name="start")
@click.argument("job_name")
def cli_start(job_name):
    """Create a yaml for job_name inside the data folder
    """
    create_job_yaml(job_name)

@main.command(name="run")
@click.argument("job_name")
def cli_run_job_from_job_dir(job_name):
    """Run a specific job locally
    """
    validate_workspace()
    run_job_from_job_dir(job_name)

@main.command(name="translate")
@click.argument("sql_path")
@click.option("--run", is_flag=True, default=False, required=False)
def cli_translator(sql_path, run):
    """Run a specific job locally
    """
    translate_job(sql_path, run)

@main.command(name="create_job")
@click.argument("job_name")
def cli_create_job(job_name):
    """Create a databricks job
    """
    validate_workspace()
    create_job(job_name)

@main.command(name="create")
@click.argument("local_path", type=click.Path())
def cli_create(local_path):
    """Copy workspace_example folder from S3 to local_path"""
    bucket_name = "serrademo"
    example_folder_key = "workspace_example"

    s3_client = boto3.client("s3")

    try:
        download_folder_from_s3(s3_client, bucket_name, example_folder_key, local_path)
    except botocore.exceptions.ClientError as e:
        print(f"Error: {e.response['Error']['Message']}")


@main.command(name="update_package")
def cli_update_package():
    """Uploads package to aws, and restarts databricks cluster
    """
    update_package()
    
# only for use by databricks cluster
# Did not use click because there were wierd traceback errors
def serra_databricks():
    assert len(sys.argv) == 2
    job_name = sys.argv[1]
    run_job_from_aws(job_name)
    
if __name__ == '__main__':
  main()