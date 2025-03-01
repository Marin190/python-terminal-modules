# Better-Ollama

Better-Ollama is an addon module designed to enhance interaction with the Ollama model via the command line. This module allows users to configure settings, save and load prompts, perform web searches, and list available models.

## Features

- **Configuration Management**: Easily set and view configuration settings.
- **Prompt Management**: Save, load, list, and delete prompts.
- **Web Search Integration**: Include web search results in your prompts.
- **Model Listing**: View available Ollama models.

## Installation

To use Better-Ollama, ensure you have the necessary dependencies installed:

```bash
pip install ollama requests rich
```

## Usage

```bash
better-ollama [options] [prompt]
```

### Options

- `--config <key> <value>`: Set configuration value.
- `--show-config`: Show current configuration.
- `--save-prompt <name>`: Save the prompt for later use.
- `--load-prompt <name>`: Load and use a saved prompt.
- `--list-prompts`: List all saved prompts.
- `--delete-prompt <name>`: Delete a saved prompt.
- `--web`: Include web search results.
- `--models`: List available models.
- `--help`: Show help message.

### Configuration Keys

- `model`: The Ollama model to use.
- `system_prompt`: System prompt for the AI.
- `temperature`: Temperature (0.0 to 1.0).
- `top_p`: Top P sampling (0.0 to 1.0).
- `context_window`: Context window size.
- `google_api_key`: Google Custom Search API key.
- `google_cse_id`: Google Custom Search Engine ID.

## Examples

### Set Configuration

```bash
better-ollama --config model "mistral:latest"
better-ollama --config temperature 0.7
```

### Show Current Configuration

```bash
better-ollama --show-config
```

### Save a Prompt

```bash
better-ollama --save-prompt python-expert "You are an expert in python."
```

### Load a Prompt

```bash
better-ollama --load-prompt python-expert "code this script"
```

### List Saved Prompts

```bash
better-ollama --list-prompts
```

### Delete a Prompt

```bash
better-ollama --delete-prompt my_prompt
```

### Include Web Search Results

```bash
better-ollama --web "What are the latest news about AI?"
```

### List Available Models

```bash
better-ollama --models
```

### Get Help

```bash
better-ollama --help
```

## Required Arguments

- `prompt`: The prompt to send to the Ollama model.

## Optional Flags

- `--web`: Include web search results in the prompt.

## Configuration File

The configuration file is located at `~/.terminal_config/better-ollama/config.json`. It contains default settings that can be modified using the `--config` option.

## Prompts Directory

Saved prompts are stored in `~/.terminal_config/better-ollama/prompts`.

## Dependencies

- `ollama`: The main module for interacting with the Ollama model.
- `requests`: For performing web searches.
- `rich`: For enhanced console output.