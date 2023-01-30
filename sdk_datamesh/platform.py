import os
import aws_cdk as cdk
from .platform_stack import SdkDataMeshPlatformStack
from .product_stack import SdkDataMeshProductStack

class DataMeshPlatform:
    def __init__(self) -> None:
        self.context = cdk.App()

    def create_domain(self, name):  
        return DataMeshDomain(self.context, name)

    def create_data_product(self, domain, name, job_script):
        return DataMeshDataProduct(domain, name, job_script)

    def compile(self):
        self.context.synth()

class DataMeshDomain:
    def __init__(self, platform_context, name) -> None:
        self.name = name
        self.platform_context = platform_context
        platform_stack = SdkDataMeshPlatformStack(
            platform_context, 
            f"datamesh-platform-{name}-stack", 
            domain_name=name
        ) 
        self.code_bucket = platform_stack.get_code_bucket()
        self.data_bucket = platform_stack.get_data_bucket()
        self.database_name = platform_stack.get_database_name()

class DataMeshDataProduct:
    def __init__(self, domain, name, job_script) -> None:
        self.name = name
        SdkDataMeshProductStack(
            domain.platform_context,
            f"datamesh-product-{domain.name}-{name}-stack",
            domain=domain,
            data_product_name=name,
            job_script=job_script
        ) 
        
