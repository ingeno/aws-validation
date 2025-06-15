#!/bin/bash +x +e


python3 remove_markdown_formatting.py ecs/acimtl/acimtl-partner-common-response.md --csv
python3 remove_markdown_formatting.py ecs/acimtl/acimtl-partner-ecs-response.md --csv

python3 remove_markdown_formatting.py ecs/valmetal/valmetal-partner-common-response.md --csv
python3 remove_markdown_formatting.py ecs/valmetal/valmetal-partner-ecs-response.md --csv

