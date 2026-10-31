---
layout: archive
title: "Locally running open-weight LLMs"
permalink: /local-llms/
excerpt: "Running open source AI models on Apple silicon using CoreAI"
collection: portfolio
#author_profile: true
---
# Using MLX-LM
A few days after comitting the [Swift](#using-swift) section of this experiment, I found [mlx-lm](https://pypi.org/project/mlx-lm/) which provides a python package for generating text and fine-tuning llm's on Apple Silicon with MLX.
mlx-lm allows running most open-weight llms on Hugging Face, hosting them on their [models page](https://huggingface.co/mlx-community/models) within the MLX community on HF.

I'm going to outline the steps I took to run Googles Gemma 4 model my local environment which uses Homewbrew package manager and virtual python environments.

You can install MLX-LM with:
```commandline
pip install mlx-lm
```

From there I emulated the same structure and usecase as the swift cli tool and made a script that accepts a prompt as a variable from the command line, then prints the response:

```python
import sys
from mlx_lm import generate, load

repo_slug = "mlx-community/gemma-4-e2b-it-OptiQ-4bit-decision"
model, tokenizer = load(repo_slug)

# sys.argv[0] == this will always the filename (unused)
# sys.argv[1] == prompt
prompt = sys.argv[1]

messages = [{"role": "user", "content": prompt}]
prompt = tokenizer.apply_chat_template(
    messages, add_generation_prompt=True,
)
text = generate(model, tokenizer, prompt=prompt, verbose=True)

print(text)
```
## Usage
To use the tool go to the directory it is located in and run
```commandline
python -m gemma-4-e2b-test "<prompt>"
```
It would also be possible to run this tool from any directory if you made a user binary pointed at the script or at a shell script that points to the python script. This would allow for a more diverse set of use cases.

## Example output

```commandline
python -m gemma-4-e2b-test "hellooooo my ai friend how are ya"
    	Fetching 13 files: 100%|███████████████████████████████████████████████████████████████████| 13/13 [01:53<00:00,  8.74s/it]
	Download complete: : ██████████████████████████████████████████████████████████████████████████████████| 4.24GB, 22.2MB/s
	Reconstruction complete: 100%|████████████████████████████████████████████████████████████████| 4.31GB / 4.31GB, 66.3MB/s
	==========
	<|channel>thought
	Thinking Process:
	
	1.  **Analyze the input:** The user said "hellooooo my ai friend how are ya". This is a very casual, friendly, and informal greeting.
	2.  **Determine the user's intent:** The user is initiating a friendly conversation and asking how the AI is doing.
	3.  **Formulate a suitable response:**
	    *   Match the tone (friendly, warm, casual).
	    *   Answer the question (state that the AI is functioning well/great).
	    *   Reciprocate the inquiry (ask the user how they are).
	    *   Offer assistance (prompt the user to state their need).
	4.  **Draft the response (Internal Monologue & Refinement):**
	    *   *Initial thought:* I'm good, thanks. How are you?
	    *   *Refinement (Adding personality/matching the enthusiasm):* Hello! I'm doing great, ready to chat. How about you?
	5.  **Final Output Generation.** (This leads to the suggested friendly response.)<channel|>Hello there! I'm doing great, thanks for asking! 😊 I'm ready to chat or help you with anything you
	==========
	Prompt: 24 tokens, 17.989 tokens-per-sec
	Generation: 256 tokens, 109.887 tokens-per-sec
	Peak memory: 4.320 GB
	<|channel>thought
	Thinking Process:
	
	1.  **Analyze the input:** The user said "hellooooo my ai friend how are ya". This is a very casual, friendly, and informal greeting.
	2.  **Determine the user's intent:** The user is initiating a friendly conversation and asking how the AI is doing.
	3.  **Formulate a suitable response:**
	    *   Match the tone (friendly, warm, casual).
	    *   Answer the question (state that the AI is functioning well/great).
	    *   Reciprocate the inquiry (ask the user how they are).
	    *   Offer assistance (prompt the user to state their need).
	4.  **Draft the response (Internal Monologue & Refinement):**
	    *   *Initial thought:* I'm good, thanks. How are you?
	    *   *Refinement (Adding personality/matching the enthusiasm):* Hello! I'm doing great, ready to chat. How about you?
	5.  **Final Output Generation.** (This leads to the suggested friendly response.)<channel|>Hello there! I'm doing great, thanks for asking! 😊 I'm ready to chat or help you with anything you
```
The output shows the reasoning steps as well as the final generated response to my prompt:
```commandline
Hello there! I'm doing great, thanks for asking! 😊 I'm ready to chat or help you with anything you
```

# Using Swift
Prompt: 
"Say Hello to the world."

Running in XCode:
![](../files/gemma3-local.mp4)

Response:
"Hello world! 😊 
It’s nice to be here and connect with you. How’s your day going?"

## Why
Born out of the desire to know where the prompts and other information being used by an LLM to process my requests are stored and used, I wanted to set up a local LLM runner to process prompts and verify that there is no packet of information being sent in or out of the machine its running on, while it is running.

## The process
I first decided to check out [ollama](https://docs.ollama.com/quickstart), but found that after testing a few prompts it still exchanged data over the internet to process my test prompts.

Then after skimming Apples [developer documentation](https://developer.apple.com/machine-learning/), I decided to try Apple Core AI.
This would require familiarity with the Swift programming language because [Core AI](https://developer.apple.com/core-ai/) is a Swift API and the [recipe](https://github.com/apple/coreai-models/tree/main/models/gemma3#run-a-core-ai-language-model) to export and use gemma-3-4b-it (googles open-weight gemma 3 model) with Core AI was in Swift.

![](../files/no-such-modules-error.png)
*This was reinforced by the problems that arose when first trying to emulate the recipe*

After revieweing [the basics of swift](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/guidedtour/) 
and learning how to use [swift package manager](https://docs.swift.org/swiftpm/documentation/packagemanagerdocs/gettingstarted/) 
to [resolve dependencies](https://docs.swift.org/swiftpm/documentation/packagemanagerdocs/introducingpackages#About-Modules),
I was able to diagnose the cause of the errors to be a misconfigured Swift.package manifest file.

The configuration for the package manifest that worked:
```swift
// swift-tools-version: 6.2
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "gemma3-cli-scarr",
    platforms: [
        .macOS("27.0")
    ],
    products: [
        .executable(name: "gemma3-cli", targets: ["gemma3-cli-scarr-target"])
    ],
    dependencies: [
         .package(url: "https://github.com/apple/coreai-models", branch: "main")
    ],
    targets: [
        .executableTarget(
            name: "gemma3-cli-scarr-target",
            dependencies: [
                .product(name: "CoreAILM", package: "coreai-models")
            ],
            path: "Sources",
            swiftSettings: [
                .enableUpcomingFeature("MemberImportVisibility")
            ]
        ),
    ]
)
```
First iterative working version:
```swift
import FoundationModels
import CoreAILanguageModels
import Foundation
import System

@main
struct gemma3_cli_scarr {
    static func main() async {
        let modelURL  = URL(filePath: "/Users/naota/MEDICAL-MECHANICA/the-apple-orchard/coreai-models/exports/gemma_3_4b_it_dynamic")
        do{
            let model = try await CoreAILanguageModel(resourcesAt: modelURL)
            let session = LanguageModelSession(model: model)
            let response = try await session.respond(to: "hello")
            print(response)
        } catch {
            print("error")
        }
    }
}
```
