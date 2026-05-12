uv run esgpull search \
project:CMIP6 \
activity_id:HighResMIP \
data_node:eagle.alcf.anl.gov,esgf-node.ornl.gov \
variable_id:areacello
# Expect to find 46 datasets.
# Downloads 24 files (1.2 GiB)