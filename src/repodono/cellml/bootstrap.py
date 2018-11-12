from cgrspy.bootstrap import (
    fetch,
    loadGenericModule,
)

loadGenericModule('cgrs_cellml')
loadGenericModule('cgrs_celedsexporter')

cellml = fetch('CreateCellMLBootstrap')
celedsexporter = fetch('CreateCeLEDSExporterBootstrap')
