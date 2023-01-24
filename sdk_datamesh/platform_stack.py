from aws_cdk import (
    # Duration,
    Stack,
    aws_glue as glue,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    RemovalPolicy
)
from constructs import Construct
from pathlib import Path
import os

class SdkDataMeshPlatformStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, domain_name:str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        ROOT_DIR = Path(__file__).parent.parent

        code_bucket_name = f"datamesh-data-product-code"
        code_bucket = s3.Bucket(self, code_bucket_name,
            bucket_name=code_bucket_name, 
            removal_policy=RemovalPolicy.DESTROY, 
            auto_delete_objects=True
        )

        data_bucket_name = f"datamesh-data-product-storage"
        data_bucket = s3.Bucket(self, data_bucket_name, 
            bucket_name=data_bucket_name, 
            removal_policy=RemovalPolicy.DESTROY, 
            auto_delete_objects=True
        )

        cfn_database = glue.CfnDatabase(self, "MyCfnDatabase",
            catalog_id=self.account,
            database_input=glue.CfnDatabase.DatabaseInputProperty(
                description="description",
                name=f"datamesh-{domain_name}",
            )
        )

        self.__code_bucket = code_bucket
        self.__data_bucket = data_bucket
        self.__database_name = domain_name

    def get_code_bucket(self):
        return self.__code_bucket

    def get_data_bucket(self):
        return self.__data_bucket

    def get_database_name(self):
        return self.__database_name
