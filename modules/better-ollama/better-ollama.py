import ollama
import json
import os
import requests
from pathlib import Path
from rich.console import Console

console = Console()

CONFIG_DIR = os.path.expanduser("~/.terminal_config/better-ollama")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
PROMPTS_DIR = os.path.join(CONFIG_DIR, "prompts")

DEFAULT_CONFIG = {
    "model": "mistral:latest",
    "google_api_key": "",
    "google_cse_id": "",
    "system_prompt": "You are a helpful AI assistant.",
    "temperature": 0.7,
    "top_p": 0.9,
    "context_window": 4096
}

def ensure_config():
    Path(CONFIG_DIR).mkdir(parents=True, exist_ok=True)
    Path(PROMPTS_DIR).mkdir(parents=True, exist_ok=True)
    
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
    
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def google_search(query, config):
    if not config.get("google_api_key") or not config.get("google_cse_id"):
        return "Error: Google Search API key and Custom Search Engine ID not configured"
    
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": config["google_api_key"],
        "cx": config["google_cse_id"],
        "q": query,
        "num": 3
    }
    
    try:
        response = requests.get(url, params=params)
        results = response.json()
        
        if "items" not in results:
            return "No results found"
        
        search_results = []
        for item in results["items"]:
            content = requests.get(item["link"]).text
            
            search_results.append(f"Title: {item['title']}")
            search_results.append(f"Link: {item['link']}")
            search_results.append(f"Snippet: {item.get('snippet', 'No snippet available')}")
            search_results.append(f"Content: {content}")
            search_results.append("")
        
        return "\n".join(search_results)
    except Exception as e:
        return f"Error performing search: {str(e)}"

def send_to_ollama(prompt, config, include_web_search=False):
    if include_web_search:
        querry = ollama.generate(
            model=config["model"],
            prompt="Generate a concise web search query based on the following user input to retrieve the most relevant information (answer only with the querry avoid any extra text): " + prompt
        )
        search_results = google_search(querry.response, config)
        prompt = f"Web search results:\n{search_results}\n\nBased on these results: {prompt}"
    
    try:
        options = {
            "temperature": float(config.get("temperature", 0.7)),
            "top_p": float(config.get("top_p", 0.9)),
            "num_ctx": int(config.get("context_window", 4096))
        }
        
        response = ollama.generate(
            model=config["model"],
            prompt=prompt,
            system=config["system_prompt"],
            options=options,
            stream=True
        )
        
        full_response = ""
        for chunk in response:
            if chunk.get('response'):
                console.print(chunk['response'], end='')
                full_response += chunk['response']
        print()
        return full_response
        
    except Exception as e:
        return f"Error: {str(e)}"

def save_prompt(name, prompt):
    prompt_file = os.path.join(PROMPTS_DIR, f"{name}.txt")
    with open(prompt_file, 'w') as f:
        f.write(prompt)

def load_prompt(name):
    prompt_file = os.path.join(PROMPTS_DIR, f"{name}.txt")
    try:
        with open(prompt_file, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None

def list_prompts():
    prompts = []
    for file in os.listdir(PROMPTS_DIR):
        if file.endswith('.txt'):
            prompts.append(file[:-4])
    return prompts

def list_models():
    try:
        models = ollama.list()
        return [model['model'] for model in models['models']]
    except Exception as e:
        return f"Error listing models: {str(e)}"

def print_help():
    print("Usage: better-ollama [options] [prompt]")
    print("\nOptions:")
    print("  --config <key> <value>    Set configuration value")
    print("  --show-config             Show current configuration")
    print("  --save-prompt <name>      Save the prompt for later use")
    print("  --load-prompt <name>      Load and use a saved prompt")
    print("  --list-prompts            List all saved prompts")
    print("  --delete-prompt <name>    Delete a saved prompt")
    print("  --web                     Include web search results")
    print("  --models                  List available models")
    print("  --help                    Show this help message")
    print("\nConfiguration keys:")
    print("  model              The Ollama model to use")
    print("  system_prompt      System prompt for the AI")
    print("  temperature        Temperature (0.0 to 1.0)")
    print("  top_p             Top P sampling (0.0 to 1.0)")
    print("  context_window    Context window size")
    print("  google_api_key    Google Custom Search API key")
    print("  google_cse_id     Google Custom Search Engine ID")

def run_command(args):
    config = ensure_config()
    
    if not args or args == "--help":
        print_help()
        return
    
    parts = args.split()
    
    if parts[0] == "--config":
        if len(parts) < 3:
            print("Usage: better-ollama --config <key> <value>")
            return
        key, value = parts[1], " ".join(parts[2:])
        if key in config:
            config[key] = value
            save_config(config)
            print(f"Configuration updated: {key} = {value}")
        else:
            print(f"Unknown configuration key: {key}")
    
    elif parts[0] == "--show-config":
        console.print("\n[bold]Current Configuration:[/bold]")
        for key, value in config.items():
            console.print(f"  [cyan]{key}[/cyan]: {value}")
    
    elif parts[0] == "--models":
        models = list_models()
        if isinstance(models, list):
            console.print("\n[bold]Available Models:[/bold]")
            for model in models:
                console.print(f"  [cyan]{model}[/cyan]")
        else:
            print(models)
    
    elif parts[0] == "--save-prompt":
        if len(parts) < 3:
            print("Usage: better-ollama --save-prompt <name> <prompt>")
            return
        name, prompt = parts[1], " ".join(parts[2:])
        save_prompt(name, prompt)
        print(f"Prompt saved as '{name}'")
    
    elif parts[0] == "--load-prompt":
        if len(parts) < 2:
            print("Usage: better-ollama --load-prompt <name>")
            return
        name = parts[1]
        prompt = load_prompt(name)
        if prompt:
            response = send_to_ollama(prompt, config)
        else:
            print(f"Prompt '{name}' not found")
    
    elif parts[0] == "--list-prompts":
        prompts = list_prompts()
        if prompts:
            console.print("\n[bold]Saved Prompts:[/bold]")
            for prompt in prompts:
                console.print(f"  [cyan]{prompt}[/cyan]")
        else:
            print("No saved prompts")
    
    elif parts[0] == "--delete-prompt":
        if len(parts) < 2:
            print("Usage: better-ollama --delete-prompt <name>")
            return
        name = parts[1]
        prompt_file = os.path.join(PROMPTS_DIR, f"{name}.txt")
        try:
            os.remove(prompt_file)
            print(f"Prompt '{name}' deleted")
        except FileNotFoundError:
            print(f"Prompt '{name}' not found")
    
    elif parts[0] == "--web":
        prompt = " ".join(parts[1:])
        response = send_to_ollama(prompt, config, include_web_search=True)
    
    else:
        response = send_to_ollama(" ".join(parts), config)