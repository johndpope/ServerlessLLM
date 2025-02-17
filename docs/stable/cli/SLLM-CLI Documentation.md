## ServerlessLLM CLI Documentation

### Overview
`sllm-cli` is a command-line interface (CLI) tool designed for managing and interacting with ServerlessLLM models. This document provides an overview of the available commands and their usage.

### Getting Started

Before using the `sllm-cli` commands, you need to start the ServerlessLLM cluster. Follow the guides below to set up your cluster:

- [Installation Guide](../getting_started/installation.md)
- [Docker Quickstart Guide](../getting_started/docker_quickstart.md)
- [Quickstart Guide](../getting_started/quickstart.md)

After setting up the ServerlessLLM cluster, you can use the commands listed below to manage and interact with your models.

### sllm-cli deploy
Deploy a model using a configuration file or model name.

##### Usage
```bash
sllm-cli deploy [OPTIONS]
```

##### Options
- `--model <model_name>`
  - Model name to deploy with default configuration.

- `--config <config_path>`
  - Path to the JSON configuration file.

##### Example
```bash
sllm-cli deploy --model facebook/opt-1.3b
sllm-cli deploy --config /path/to/config.json
```

##### Example Configuration File (`config.json`)
```json
{
    "model": "facebook/opt-1.3b",
    "backend": "transformers",
    "num_gpus": 1,
    "auto_scaling_config": {
        "metric": "concurrency",
        "target": 1,
        "min_instances": 0,
        "max_instances": 10
    },
    "backend_config": {
        "pretrained_model_name_or_path": "facebook/opt-1.3b",
        "device_map": "auto",
        "torch_dtype": "float16"
    }
}
```

### sllm-cli delete
Delete deployed models by name.

##### Usage
```bash
sllm-cli delete [MODELS]
```

##### Arguments
- `MODELS`
  - Space-separated list of model names to delete.

##### Example
```bash
sllm-cli delete facebook/opt-1.3b facebook/opt-2.7b meta/llama2
```

### sllm-cli generate
Generate outputs using the deployed model.

##### Usage
```bash
sllm-cli generate [OPTIONS] <input_path>
```

##### Options
- `-t`, `--threads <num_threads>`
  - Number of parallel generation processes. Default is 1.

##### Arguments
- `input_path`
  - Path to the JSON input file.

##### Example
```bash
sllm-cli generate --threads 4 /path/to/request.json
```

##### Example Request File (`request.json`)
```json
{
    "model": "facebook/opt-1.3b",
    "messages": [
        {
            "role": "user",
            "content": "Please introduce yourself."
        }
    ],
    "temperature": 0.3,
    "max_tokens": 50
}
```

### sllm-cli replay
Replay requests based on workload and dataset.

##### Usage
```bash
sllm-cli replay [OPTIONS]
```

##### Options
- `--workload <workload_path>`
  - Path to the JSON workload file.

- `--dataset <dataset_path>`
  - Path to the JSON dataset file.

- `--output <output_path>`
  - Path to the output JSON file for latency results. Default is `latency_results.json`.

##### Example
```bash
sllm-cli replay --workload /path/to/workload.json --dataset /path/to/dataset.json --output /path/to/output.json
```

#### sllm-cli update
Update a deployed model using a configuration file or model name.

##### Usage
```bash
sllm-cli update [OPTIONS]
```

##### Options
- `--model <model_name>`
  - Model name to update with default configuration.

- `--config <config_path>`
  - Path to the JSON configuration file.

##### Example
```bash
sllm-cli update --model facebook/opt-1.3b
sllm-cli update --config /path/to/config.json
```

### Example Workflow

1. **Deploy a Model**
    ```bash
    sllm-cli deploy --model facebook/opt-1.3b
    ```

2. **Generate Output**
    ```bash
    echo '{
      "model": "facebook/opt-1.3b",
      "messages": [
        {
          "role": "user",
          "content": "Please introduce yourself."
        }
      ],
      "temperature": 0.7,
      "max_tokens": 50
    }' > input.json
    sllm-cli generate input.json
    ```

3. **Delete a Model**
    ```bash
    sllm-cli delete facebook/opt-1.3b
    ```