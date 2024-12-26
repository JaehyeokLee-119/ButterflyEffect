#!/bin/bash
DATA_PATH="./data/hotpotqa_wiki_test.joblib"
OUTPUT_DIR="gpt-4o-fullwiki-test"

python main.py --data $DATA_PATH --output-dir $OUTPUT_DIR