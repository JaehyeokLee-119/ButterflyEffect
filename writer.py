import os
from prompt import (
    SYSTEM_MESSAGE, 
    INSIGHTS,
    FEWSHOTS
)

def write_result(dir_path, df):
    tsv_path = os.path.join(dir_path, "result.tsv")
    df.to_csv(tsv_path, index=False, sep="\t")

def write_message(dir_path, message_logs):
    message_path = os.path.join(dir_path, "messages.txt")
    with open(message_path, 'w') as f:
        f.write('\n'.join(message_logs))

def write_metric(dir_path, answer_metric, sp_metric):
    metric_path = os.path.join(dir_path, "metric.txt")
    with open(metric_path, 'w') as f:
        f.write(str(answer_metric)+"\n")
        f.write(str(sp_metric))

def write_prompt(dir_path):
    prompt_path = os.path.join(dir_path, "prompt.txt")
    with open(prompt_path, 'w') as f:
        f.write("SYSTEM MESSAGE")
        f.write(SYSTEM_MESSAGE + "\n")

        f.write("INSIGHTS")
        f.write(INSIGHTS + "\n")

        f.write("FEWSHOTS\n")
        for FEWSHOT in FEWSHOTS:
            f.write(FEWSHOT + "\n\n")


