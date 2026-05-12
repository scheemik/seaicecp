uv run esgpull search \
project:CMIP6 \
activity_id:HighResMIP \
experiment_id:hist-1950,highres-future \
source_id:HadGEM3-GC31-HH,HadGEM3-GC31-HM,HadGEM3-GC31-MM \
frequency:mon \
variable_id:siage,siconc,sithick,siu,siv
# Expect to find 140 datasets.