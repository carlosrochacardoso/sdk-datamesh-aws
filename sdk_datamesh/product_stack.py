from aws_cdk import (
    # Duration,
    Stack,
    aws_glue as glue,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_iam as iam
)
from constructs import Construct
from pathlib import Path
import os
import uuid

class SdkDataMeshProductStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, domain, data_product_name: str, job_script: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        ROOT_DIR = Path(__file__).parent.parent
        data_product_full_name = f"datamesh-product-{domain.name}-{data_product_name}"

        deployment = s3deploy.BucketDeployment(self, f"{data_product_full_name}-deploy",
            sources=[s3deploy.Source.asset(os.path.join(ROOT_DIR,"job_scripts",data_product_name))],
            destination_bucket=domain.code_bucket,
            retain_on_delete=False,
            prune=False
        )

        job_name = f"{data_product_full_name}-job"
        glue_role = iam.Role.from_role_name(self, uuid.uuid4().hex,
            role_name="AWSGlueServiceRole-dataplatform"
        )

        cfn_job = glue.CfnJob(self, job_name,
            name=job_name,
            command=glue.CfnJob.JobCommandProperty(
                name=job_name,
                python_version="3",
                script_location=f"s3://{domain.code_bucket.bucket_name}/{job_script}"
            ),
            role=glue_role.role_arn,

            # the properties below are optional
            description="description",
            execution_property=glue.CfnJob.ExecutionPropertyProperty(
                max_concurrent_runs=1
            ),
            glue_version="3.0",
            max_retries=0,
            number_of_workers=5,
            worker_type="G.1X"
        )

        crawler_name = f"{data_product_full_name}-crawler"
        cfn_crawler = glue.CfnCrawler(self, crawler_name,
            role=glue_role.role_arn,
            targets=glue.CfnCrawler.TargetsProperty(
                s3_targets=[glue.CfnCrawler.S3TargetProperty(
                    path="s3://path",
                )]
            ),
            # the properties below are optional
            database_name=domain.database_name,
            description="description",
            name=crawler_name
        )