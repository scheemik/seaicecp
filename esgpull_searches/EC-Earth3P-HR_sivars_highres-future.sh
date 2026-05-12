uv run esgpull search \
project:CMIP6 \
activity_id:HighResMIP \
experiment_id:highres-future \
data_node:eagle.alcf.anl.gov,esgf-node.ornl.gov \
source_id:EC-Earth3P-HR \
frequency:mon \
variable_id:siage,siconc,sithick,siu,siv
# Expect to find 25 datasets.