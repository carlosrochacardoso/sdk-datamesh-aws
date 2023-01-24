from sdk_datamesh.platform import DataMeshPlatform

dm_platform = DataMeshPlatform()

payments_domain = dm_platform.create_domain("payments")

dm_product_issued = dm_platform.create_data_product(
    domain=payments_domain,
    name="boleto-event-issued",
    job_script="boleto_event_issued.py"
    #workflow=
    #port_in=
    #port_out=
)

dm_product_settled = dm_platform.create_data_product(
    domain=payments_domain,
    name="boleto-event-settled",
    job_script="boleto_event_settled.py"
)

dm_platform.compile()