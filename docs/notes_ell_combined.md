# Configuration

ell provides various configuration options to customize its behavior.

## ell.init(store: Store | str | None = None, verbose: bool = False, autocommit: bool = True, lazy_versioning: bool = True, default_api_params: Dict[str, Any] = None, default_openai_client: Any = None, autocommit_model: str = 'gpt-4o-mini') → None

Initialize the ELL configuration with various settings.

**Parameters:**

- **verbose** (`bool`) – Set verbosity of ELL operations.

- **store** (`Union[Store, str]`, optional) – Set the store for ELL. Can be a Store instance or a string path for SQLiteStore.

- **autocommit** (`bool`) – Set autocommit for the store operations.

- **lazy_versioning** (`bool`) – Enable or disable lazy versioning.

- **default_api_params** (`Dict[str, Any]`, optional) – Set default parameters for language models.

- **default_openai_client** (`openai.Client`, optional) – Set the default OpenAI client.

- **autocommit_model** (`str`) – Set the model used for autocommitting.

This `init` function is a convenience function that sets up the configuration for ell. It is a thin wrapper around the `Config` class, which is a Pydantic model.

You can modify the global configuration using the `ell.config` object which is an instance of `Config`:

```python
# Example of modifying the configuration
ell.config.verbose = True
```

**End of relevant content.**


---

# Getting Started

Welcome to ell, the Language Model Programming Library. This guide will walk you through creating your first Language Model Program (LMP), exploring ell’s unique features, and leveraging its powerful versioning and visualization capabilities.

## From Traditional API Calls to ell

Let’s start by comparing a traditional API call to ell’s approach. Here’s a simple example using the OpenAI chat completions API:

```python
import openai

openai.api_key = "your-api-key-here"

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Say hello to Sam Altman!"}
]

response = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=messages
)

print(response['choices'][0]['message']['content'])
```

Now, let’s see how we can achieve the same result using ell:

```python
import ell

@ell.simple(model="gpt-4o")
def hello(name: str):
    """You are a helpful assistant."""  # System prompt
    return f"Say hello to {name}!"  # User prompt

greeting = hello("Sam Altman")
print(greeting)
```

`ell` simplifies prompting by encouraging you to define prompts as functional units. In this example, the `hello` function defines a system prompt via the docstring and a user prompt via the return string. Users of your prompt can then simply call the function with the defined arguments, rather than manually constructing the messages. This approach makes prompts more readable, maintainable, and reusable.

### Understanding `@ell.simple`

The `@ell.simple` decorator is a key concept in ell. It transforms a regular Python function into a **Language Model Program (LMP)**. Here’s what’s happening:

1. The function’s **docstring** becomes the **system message**.
2. The **return value** of the function becomes the **user message**.
3. The decorator **handles the API call** and returns the model’s response as a string.

This encapsulation allows for cleaner, more reusable code. You can now call your LMP like any other Python function.

### Verbose Mode

To get more insight into what’s happening behind the scenes, you can enable verbose mode:

```python
ell.init(verbose=True)
```

With verbose mode enabled, you’ll see detailed information about the inputs and outputs of your language model calls.

![ell demonstration](https://example.com/_images/gif1.webp)

### Alternative Message Formats

While the previous example used the docstring for the system message and the return value for the user message, ell offers more flexibility. You can explicitly define messages using `ell.system`, `ell.user`, and `ell.assistant`:

```python
import ell

@ell.simple(model="gpt-4o")
def hello(name: str):
    return [
        ell.system("You are a helpful assistant."),
        ell.user(f"Say hello to {name}!"),
        ell.assistant("Hello! I'd be happy to greet Sam Altman."),
        ell.user("Great! Now do it more enthusiastically."),
    ]

greeting = hello("Sam Altman")
print(greeting)
```

This approach allows you to construct more complex conversations within your LMP.

## Prompting as Language Model Programming

One of ell’s most powerful features is its treatment of prompts as programs rather than simple strings. This approach allows you to leverage the full power of Python in your prompt engineering. Let’s see how this works:

```python
import ell
import random

def get_random_adjective():
    adjectives = ["enthusiastic", "cheerful", "warm", "friendly"]
    return random.choice(adjectives)

@ell.simple(model="gpt-4o")
def hello(name: str):
    """You are a helpful assistant."""  # System prompt
    adjective = get_random_adjective()
    return f"Say a {adjective} hello to {name}!"

greeting = hello("Sam Altman")
print(greeting)
```

In this example, our hello LMP depends on the `get_random_adjective` function. Each time `hello` is called, it generates a different adjective, creating dynamic, varied prompts.

This compositional approach to prompt engineering enables you to break down complex tasks into smaller, more manageable steps.


---

# ell: The Language Model Programming Library

[![Install](https://img.shields.io/badge/get_started-blue)](https://docs.ell.so/installation)  
[![Discord](https://dcbadge.limes.pink/api/server/vWntgU52Xb?style=flat)](https://discord.gg/vWntgU52Xb)  
[![X (formerly Twitter) Follow](https://img.shields.io/twitter/follow/wgussml)](https://twitter.com/wgussml)  
[![Jobs Board](https://img.shields.io/badge/jobs-board-green)](https://jobs.ell.so)  

`ell` is a lightweight prompt engineering library treating prompts as functions. After years of building and using language models at OpenAI and in the startup ecosystem, `ell` was designed from the following principles:

## Prompts are programs, not strings

```python
import ell

@ell.simple(model="gpt-4o-mini")
def hello(world: str):
    """You are a helpful assistant"""  # System prompt
    name = world.capitalize()
    return f"Say hello to {name}!"  # User prompt

hello("sam altman")  # just a str, "Hello Sam Altman! ..."
```

Prompts aren’t just strings; they are all the code that leads to strings being sent to a language model. In ell, we think of one particular way of using a language model as a discrete subroutine called a **language model program** (LMP).

LMPs are fully encapsulated functions that produce either a string prompt or a list of messages to be sent to various multimodal language models. This encapsulation creates a clean interface for users, who only need to be aware of the required data specified to the LMP.

## Prompt engineering is an optimization process

The process of prompt engineering involves many iterations, similar to the optimization processes in machine learning. Because LMPs are just functions, `ell` provides rich tooling for this process.

```python
import ell

ell.init(store='./logdir')  # Versions your LMPs and their calls

# ... define your lmps
hello("strawberry")  # the source code of the LMP the call is saved to the store
```

## Tools for monitoring, versioning, and visualization

![ell demonstration](https://example-url-for-image.com/ell_studio_better.webp)

```bash
ell-studio --storage ./logdir
```

Prompt engineering goes from a dark art to a science with the right tools. **Ell Studio is a local, open source tool for prompt version control, monitoring, visualization**. With Ell Studio you can empiricize your prompt optimization process over time and catch regressions before it's too late.

## Test-time compute is important

Going from a demo to something that actually works, often means prompt engineering solutions that involve multiple calls to a language model. By forcing a functional decomposition of the problem, `ell` makes it **easy to implement test-time compute leveraged techniques in a readable and modular way.**

```python
import ell
from typing import List

@ell.simple(model="gpt-4o-mini", temperature=1.0, n=10)
def write_ten_drafts(idea: str):
    """You are an adept story writer. The story should only be 3 paragraphs"""
    return f"Write a story about {idea}."

drafts = write_ten_drafts("stock market")  # Best of 10 sampling.
```

## Every call to a language model is valuable

Every call to a language model is worth its weight in credits. In practice, LLM invocations are used for fine tuning, distillation, k-shot prompting, reinforcement learning from human feedback, and more. A good prompt engineering system should capture these as first-class concepts.

![ell demonstration](https://example-url-for-image.com/invocations.webp)

In addition to storing the source code of every LMP, `ell` optionally saves every call to a language model locally. This allows you to generate invocation datasets, compare LMP outputs by version, and generally do more with the full spectrum of prompt engineering artifacts.

## Complexity when you need it, simplicity when you don’t

Using language models is **just passing strings around, except when it’s not.**

```python
import ell

@ell.tool()
def scrape_website(url: str):
    return requests.get(url).text

@ell.complex(model="gpt-5-omni", tools=[scrape_website])
def get_news_story(topic: str):
    return [
        ell.system("Use the web to find a news story about the topic"),
        ell.user(f"Find a news story about {topic}.")
    ]

message_response = get_news_story("stock market")
if message_response.tool_calls:
    for tool_call in message_response.tool_calls:
        #...
if message_response.text:
    print(message_response.text)
if message_response.audio:
    # message_response.play_audio() support for multimodal outputs will work as soon as the LLM supports it
    pass
```

Using `@ell.simple` causes LMPs to yield **simple string outputs.** But when more complex or multimodal output is needed, `@ell.complex` can be used to yield `Message` objects responses from language models.

## Multimodality should be first class

LLMs can process and generate various types of content, including text, images, audio, and video. Prompt engineering with these data types should be as easy as it is with text.

```python
from PIL import Image
import ell

@ell.simple(model="gpt-4o", temperature=0.1)
def describe_activity(image: Image.Image):
    return [
        ell.system("You are VisionGPT. Answer <5 words all lower case."),
        ell.user(["Describe what the person in the image is doing:", image])
    ]

# Capture an image from the webcam
describe_activity(capture_webcam_image())  # "they are holding a book"
```

`ell` supports rich type coercion for multimodal inputs and outputs. You can use PIL images, audio, and other multimodal inputs inline in `Message` objects returned by LMPs.

## Prompt engineering libraries shouldn’t interfere with your workflow

`ell` is designed to be a lightweight and unobtrusive library. It doesn’t require you to change your coding style or use special editors.

![ell demonstration](https://example-url-for-image.com/useitanywhere_compressed.webp)

You can continue to use regular Python code in your IDE to define and modify your prompts while leveraging `ell`’s features to visualize and analyze your prompts. Migrate from langchain to `ell` one function at a time.

---

To get started with `ell`, see the [Getting Started](getting_started.html) section, or go onto [Installation](installation.html) and get ell installed.


---

# Installation

`ell` and `ell studio` are both contained within the `ell-ai` python package available on PyPI. You simply need to install the package and set up your API keys.

## Installing ell

1. Install using pip:

   ```bash
   pip install -U ell-ai
   ```

   By default, this installs only the OpenAI client SDK. If you want to include the Anthropic client SDK, use the “anthropic” extra like so:

   ```bash
   pip install -U 'ell-ai[anthropic]'
   ```

2. Verify installation:

   ```bash
   python -c "import ell; print(ell.__version__)"
   ```

## API Key Setup

### OpenAI API Key

1. Get API key from [OpenAI API Keys](https://platform.openai.com/account/api-keys).

2. Install the OpenAI Python package:

   ```bash
   pip install openai
   ```

3. Set environment variable:

   - Windows:

     ```bash
     setx OPENAI_API_KEY "your-openai-api-key"
     ```

   - macOS/Linux:

     ```bash
     # in your .bashrc or .zshrc
     export OPENAI_API_KEY='your-openai-api-key'
     ```

### Anthropic API Key

1. Get API key from [Anthropic](https://www.anthropic.com/).

2. Install the Anthropic Python package:

   ```bash
   pip install anthropic
   ```

3. Set environment variable:

   - Windows:

     ```bash
     setx ANTHROPIC_API_KEY "your-anthropic-api-key"
     ```

   - macOS/Linux:

     ```bash
     # in your .bashrc or .zshrc
     export ANTHROPIC_API_KEY='your-anthropic-api-key'
     ```

## Troubleshooting

- Update pip:

   ```bash
   pip install --upgrade pip
   ```

- Use virtual environment.

- Try `pip3` instead of `pip`.

- Use `sudo` (Unix) or run as administrator (Windows) if permission errors occur.

For more help, see the Troubleshooting section or file an issue on GitHub.

## Next Steps

Proceed to the Getting Started guide to create your first Language Model Program.


---

# Messages

Messages are the fundamental unit of interaction with chat-based language models. They consist of a role and some form of content. For text-only language models, the content is typically just a string. However, with multimodal language models that can process images, audio, text, and other modalities, the content object becomes more complex.

In practice, the content that a language model can consume forms a markup language, where there are different content blocks for text, images, audio, tool use, and so on.

## Challenges with LLM APIs

The potential complexity of a message object has led language model APIs to establish message specifications that are often quite pedantic, even when users only want to pass around simple types like strings or images. This issue is compounded by the fact that most language model APIs are automatically generated using tools like Stainless, which take an API spec and build multi-language client-side API bindings. Because these APIs are automatically generated, they can’t be optimized for user-friendliness.

For example, many prompt engineering libraries exist primarily to solve the inconvenience of indexing into responses from APIs like OpenAI’s. This complexity in both specifying prompts and handling responses can make working with language models unnecessarily cumbersome for developers.

```python
result: str = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of the moon?"}
    ]
)["choices"][0]["message"]["content"]  # hughkguht this line
```

Likewise, the specification of prompts themselves is also quite cumbersome. Because language model provider API client bindings are often automatically generated, they lack developer-friendly features. As a result, users need to be as verbose and pedantic as possible when constructing prompts. Consider the complexity of passing an input with both text and images to a language model API:

```python
result: str = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": [
            {"type": "text", "text": "What is the capital of the moon?"},
            {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
        ]}
    ]
)["choices"][0]["message"]["content"]
```

In essence, the user has to explicitly specify two different content blocks and their types, even though these types are implicit and could be inferred. This is because the language bindings use typed dictionaries and validators generated by tools like Stainless or similar co-generation tools. While not inherently wrong, this approach creates a gap in developer experience, making the code less readable and more cumbersome to work with.

This leads us to a core philosophy in ell:

> “Using language models is just passing around strings, except when it’s not.”

Users should be able to specify the minimal amount of complexity necessary for the data they want to pass to a language model. To achieve this, we’ve drawn inspiration from machine learning and scientific computing libraries like TensorFlow, PyTorch, and NumPy to create a new type of message API. In this API, type coercion and implicit inference are key features that enhance the developer experience.

## The ell Message API

Our API centers around two key objects: Messages and ContentBlocks.

### ell.Message

**Fields:**

- `content` (List[ell.types.message.ContentBlock])
- `role` (str)

### ell.ContentBlock

**Fields:**

- `audio` (numpy.ndarray | List[float] | None)
- `image` (ell.types.message.ImageContent | None)
- `parsed` (pydantic.main.BaseModel | None)
- `text` (ell.types._lstr._lstr | str | None)
- `tool_call` (ell.types.message.ToolCall | None)
- `tool_result` (ell.types.message.ToolResult | None)

### Solving the construction problem

The Message and ContentBlock objects solve the problem of pedantic construction by incorporating type coercion directly into their constructors.

Consider constructing a message that contains both text and an image. Traditionally, you might need to create a Message with a role and two ContentBlocks - one for text and one for an image:

```python
from ell import Message, ContentBlock

message = Message(
    role="user",
    content=[
        ContentBlock(text="What is the capital of the moon?"),
        ContentBlock(image=some_PIL_image_object)
    ]
)
```

However, the Message object can infer the types of content blocks within it. This allows for a more concise construction:

```python
message = Message(
    role="user",
    content=[
        "What is the capital of the moon?",
        some_PIL_image_object
    ]
)
```

Furthermore, if a message contains only one type of content (for example, just an image), we also support shape coercion:

```python
message = Message(
    role="user",
    content=some_PIL_image_object
)
```

Coercion is an important concept in ell, and you can read more about it in the Content Block Coercion API reference page.

### Common roles

Ell’s message API provides several common helper functions for constructing messages with specific roles in language model APIs. These functions essentially partially compose the Message constructor with a specific role. All of the type coercion and convenient functionality from before is automatically handled.

```python
message = ell.user([
    "What is the capital of the moon?",
    some_PIL_image_object
])
```

### Solving the parsing problem

Complex message structures shouldn’t mean complex interactions. Drawing inspiration from rich HTML APIs and JavaScript’s document selector API, as well as BeautifulSoup’s helper functions for extracting text from HTML documents, we’ve built convenient functions for interacting with the contents of a message.

```python
from ell import Message, ContentBlock
import openai

# Assume we have a response from a multimodal language model
response = openai.ChatCompletion.create(
    model="gpt-5-omni",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": [
            {"type": "text", "text": "Draw me a sketch version of this image"},
            {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
        ]}
    ]
)

# Access the message content from the OpenAI response
message_content = response.choices[0].message.content

# Check for different types of content in the traditional OpenAI API format
has_image = any(content.get('type') == 'image_url' for content in message_content if isinstance(content, dict))
has_text = any(content.get('type') == 'text' for content in message_content if isinstance(content, dict))
has_tool_call = 'function_call' in response.choices[0].message

if has_image:
    image_content = [content['image_url']['url'] for content in message_content if isinstance(content, dict) and content.get('type') == 'image_url']
    show(image_content[0])

if has_text:
    # Extract text content
    text_content = [content['text'] for content in message_content if isinstance(content, dict) and content.get('type') == 'text']
    print("".join(text_content[0]))

if has_tool_call:
    print("The message contains a tool call.")
```

Now let’s see how we can do the same thing using ell’s message API. In the following example, we’ll use ell’s `@ell.complex` decorator which is similar to `@ell.simple`. However, instead of returning a string after calling the language model program, it returns a Message object representing the response from the language model. This allows you to have language model responses with multimodal output, including structured and tool call output. You can learn more about this in the [@ell.complex](ell_complex.html) section.

```python
import ell

@ell.complex(model="gpt-5-omni")
def draw_sketch(image: PILImage.Image):
    return [
        ell.system("You are a helpful assistant."),
        ell.user(["Draw me a sketch version of this image", image]),
    ]

response = draw_sketch(some_PIL_image_object)

if response.images:
    show(response.images[0])

if response.text:
    print(response.text)

if response.tool_calls:
    print("The message contains a tool call.")
```

The following convenience functions and properties are available on a Message object:

- **Message.text**: Returns all text content, replacing non-text content with their representations.
- **Message.text_only**: Returns only the text content, ignoring non-text content.
- **Message.tool_calls**: Returns a list of all tool calls.
- **Message.tool_results**: Returns a list of all tool results.
- **Message.parsed**: Returns a list of all parsed content.
- **Message.images**: Returns a list of all image content.
- **Message.audios**: Returns a list of all audio content.
- **Message.call_tools_and_collect_as_message**: Method to call tools and collect results as a message.


---

# Models & API Clients

In language model programming, the relationship between models and API clients is crucial. ell provides a robust framework for managing this relationship, offering various ways to specify clients for models, register custom models, and leverage default configurations.

## Model Registration and Default Clients

ell automatically registers numerous models from providers like OpenAI, Anthropic, Cohere, and Groq upon initialization. This allows you to use models without explicitly specifying a client.

If no client is found for a model, ell falls back to a default OpenAI client. This enables the utilization of newly released models without updating ell for new model registrations. If the fallback fails because the model is not available in the OpenAI API, you can register your own client for the model using the *ell.config.register_model* method or specify a client when calling the language model program below.

## Specifying Clients for Models

ell offers multiple methods to specify clients for models:

1. **Decorator-level Client Specification:**

    ```python
    import ell
    import openai

    client = openai.Client(api_key="your-api-key")

    @ell.simple(model="gpt-next", client=client)
    def my_lmp(prompt: str):
        return f"Respond to: {prompt}"
    ```

2. **Function Call-level Client Specification:**

    ```python
    result = my_lmp("Hello, world!", client=another_client)
    ```

3. **Global Client Registration:**

    ```python
    ell.config.register_model("gpt-next", my_custom_client)
    ```

## Custom Model Registration

For custom or newer models, ell provides a straightforward registration method:

```python
import ell
import my_custom_client

ell.config.register_model("my-custom-model", my_custom_client)
```


---

# Multimodality

As the capabilities of language models continue to expand, so too does the need for frameworks that can seamlessly handle multiple modalities of input and output. ell rises to this challenge by providing robust support for multimodal interactions, allowing developers to work with text, images, audio, and more within a unified framework.

## The Evolution of Multimodal Interactions

Traditionally, working with language models has been primarily text-based. However, the landscape is rapidly changing. Models like GPT-4 with vision capabilities, or DALL-E for image generation, have opened up new possibilities for multimodal applications. This shift presents both opportunities and challenges for developers.

Consider the complexity of constructing a prompt that includes both text and an image using a traditional API:

```python
result = openai.ChatCompletion.create(
    model="gpt-4-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
            ]
        }
    ]
)
```

This approach, while functional, is verbose and can become unwieldy as the complexity of inputs increases. It doesn’t align well with the natural flow of programming and can make code less readable and more error-prone.

## ell’s Approach to Multimodality

ell addresses these challenges by treating multimodal inputs and outputs as first-class citizens within its framework. Let’s explore how ell simplifies working with multiple modalities:

1. **Simplified Input Construction**

   ell’s Message and ContentBlock objects, which we explored in the Message API chapter, shine when it comes to multimodal inputs. They allow for intuitive construction of complex prompts:

   ```python
   from PIL import Image
   import ell

   @ell.simple(model="gpt-4-vision-preview")
   def describe_image(image: Image.Image):
       return [
           ell.system("You are a helpful assistant that describes images."),
           ell.user(["What's in this image?", image])
       ]

   result = describe_image(some_pil_image)  # 'There's a cat in the image'
   ```

   Notice how ell automatically handles the conversion of the PIL Image object into the appropriate format for the language model. This abstraction allows developers to focus on their application logic rather than the intricacies of API payloads.

   ell also supports working with image URLs, making it easy to reference images hosted online:

   ```python
   from ell.types.message import ImageContent

   @ell.simple(model="gpt-4o-2024-08-06")
   def describe_image_from_url(image_url: str):
       return [
           ell.system("You are a helpful assistant that describes images."),
           ell.user(["What's in this image?", ImageContent(url=image_url, detail="low")])
       ]

   result = describe_image_from_url("https://example.com/cat.jpg")
   ```

   This flexibility allows developers to work with both local images and remote image URLs seamlessly within the ell framework.

2. **Flexible Output Handling**

   Just as ell simplifies input construction, it also provides flexible ways to handle multimodal outputs. The Message object returned by `@ell.complex` decorators offers convenient properties for accessing different types of content:

   ```python
   @ell.complex(model="gpt-5-omni")
   def generate_audiovisual_novel(topic: str):
       return [
           ell.system("You are a helpful assistant that can generate audiovisual novels. Output images, text, and audio simultaneously."),
           ell.user(f"Generate a novel on the topic of {topic}")
       ]

   result = generate_audiovisual_novel("A pirate adventure")
   ```

   In this example, we’ve created a workflow that takes an image, generates a caption for it, converts that caption to speech, and then combines all these elements into a social media post. ell’s multimodal support makes this complex interaction feel natural and intuitive.

3. **Seamless Integration with Python Ecosystem**

   ell’s design philosophy extends to its integration with popular Python libraries for handling different media types. For instance, it works seamlessly with PIL for images, making it easy to preprocess or postprocess visual data:

   ```python
   from PIL import Image, ImageEnhance

   def enhance_image(image: Image.Image) -> Image.Image:
       enhancer = ImageEnhance.Contrast(image)
       return enhancer.enhance(1.5)

   @ell.complex(model="gpt-4-vision-preview")
   def analyze_enhanced_image(image: Image.Image):
       enhanced = enhance_image(image)
       return [
           ell.system("Analyze the enhanced image and describe any notable features."),
           ell.user(enhanced)
       ]
   ```

   This example demonstrates how ell allows for the seamless integration of image processing techniques within the language model workflow.

## The Power of Multimodal Composition

One of the most powerful aspects of ell’s multimodal support is the ability to compose complex workflows that involve multiple modalities. Let’s consider a more advanced example:

```python
@ell.simple(model="gpt-4o")
def generate_image_caption(image: Image.Image):
    return [
        ell.system("Generate a concise, engaging caption for the image."),
        ell.user(image)
    ]

@ell.complex(model="gpt-4-audio")
def text_to_speech(text: str):
    return [
        ell.system("Convert the following text to speech."),
        ell.user(text)
    ]

@ell.complex(model="gpt-4")
def create_social_media_post(image: Image.Image):
    caption = generate_image_caption(image)
    audio = text_to_speech(caption)
    return [
        ell.system("Create a social media post using the provided image, caption, and audio."),
        ell.user([
            "Image:", image,
            "Caption:", caption,
            "Audio:", audio.audios[0]
        ])
    ]

post = create_social_media_post(some_image)
```

Multimodality in ell isn’t just a feature; it’s a fundamental design principle that reflects the evolving landscape of AI and machine learning. By providing a unified, intuitive interface for working with various types of data, ell empowers developers to create sophisticated, multimodal applications with ease.


---

# @ell.simple

The core unit of prompt engineering in ell is the `@ell.simple` decorator. This decorator transforms a function that provides system and user prompts into a callable object. When invoked, this callable sends the provided prompts to a language model and returns the model’s response.

The development of `@ell.simple` is driven by several important objectives:

- Improve readability and usability of prompt engineering code.

- Force a functional decomposition of prompt systems into reusable components.

- Enable versioning, serialization, and tracking of prompts over time.

## Usage

The `@ell.simple` decorator can be used in two main ways:

1. Using the docstring as the system prompt, and the return value as the user message:

   ```python
   @ell.simple(model="gpt-4")
   def hello(name: str):
       """You are a helpful assistant."""
       return f"Say hello to {name}!"
   ```

2. Explicitly defining messages:

   ```python
   @ell.simple(model="gpt-4")
   def hello(name: str):
       return [
           ell.system("You are a helpful assistant."),
           ell.user(f"Say hello to {name}!")
       ]
   ```

> **Note**: Messages in ell are not the same as the dictionary messages used in the OpenAI API. ell’s Message API provides a more intuitive and flexible way to construct and manipulate messages. You can read more about ell’s Message API and type coercion in the [Messages](message_api.html) page.

### Invoking an `@ell.simple` LMP

To use the decorated function, we can call it as a normal function. However, instead of receiving the typical return value, we will receive the result of passing the system and user prompts directly to the model specified in the decorator constructor, in this case GPT-4.

   ```python
   >>> hello("world")
   'Hello, world!'
   ```

As you can see from this example, the return type of an `@ell.simple` LMP is a string. This is to optimize for readability and usability, as most invocations of language models revolve around passing strings around. Additional metadata is only needed occasionally.

Therefore, we have two decorators within the ell framework:

1. `@ell.simple`: Returns simple strings, as shown here.

2. `@ell.complex`: Returns message objects containing all of the typical message API metadata and additional helper functions for interacting with multimodal output data. You can read more about this in the [@ell.complex](ell_complex.html) page.

### Variable system prompts

One of the challenges with specifying the system prompt in the docstring of a language model program is that if you want to use variable system prompts, Python will no longer treat the string literal at the top of the function as a docstring. For example:

   ```python
   def my_func(var: int):
       f"""my variable doc string for my_func. {var}"""
       pass
        
   >>> my_func.__doc__
   None
   ```

This behavior makes sense because a function’s docstring should not change during execution and should be extractable through static analysis.

To address this issue with `@ell.simple`, you need to use the second method of defining an `@ell.simple` language model program by creating a function that returns a list of messages (see [Messages](message_api.html) for more details).

   ```python
   @ell.simple(model="gpt-4")
   def my_func(name: str, var: int):
       return [
           ell.system(f"You are a helpful assistant. {var}"),
           ell.user(f"Say hello to {name}!")
       ]
   ```

With this approach, ell will ignore the docstring of `my_func` and instead supply the messages returned by the function to the language model API.

### Passing parameters to an LLM API

One of the most convenient functions of the `@ell.simple` decorator is that you can easily pass parameters to an LLM API, both at definition time and runtime. For example, models within the OpenAI API have parameters like `temperature`, `max_tokens`, stop tokens, and `logit_bias`. Due to how `@ell.simple` works, you can simply specify these in the decorator as keyword arguments.

   ```python
   @ell.simple(model="gpt-4", temperature=0.5, max_tokens=100, stop=["."])
   def hello(name: str):
       """You are a helpful assistant."""
       return f"Hey there {name}!"
   ```

Likewise, if you want to modify those parameters for a particular invocation of that prompt, you simply pass them in as `api_params` keyword arguments to the function when calling it. For example:

   ```python
   >>> hello("world", api_params=dict(temperature=0.7))
   'Hey there world!'
   ```

#### Multiple outputs (n>1)

As is often important in prompt engineering to leverage test-time compute, many language model APIs allow you to specify a count parameter, usually ‘n’, which will generate several outputs from the language model given a particular prompt.

In the OpenAI API, for example, this is actually quite cumbersome because the API specification separates different completions into ‘choices’ objects. For example:

   ```python
   response = openai.Completion.create(
       model="gpt-4",
       prompt="Say hello to everyone",
       n=2
   )
   r1 = response.choices[0].text
   r2 = response.choices[1].text
   ```

In the spirit of simplicity, we’ve designed it to automatically coerce the return type into the correct shape, similar to NumPy and PyTorch. This means that when you call an `@ell.simple` language model program with `n` greater than one, instead of returning a string, it returns a list of strings.

   ```python
   @ell.simple(model="gpt-4", n=2)
   def hello(name: str):
       """You are a helpful assistant."""
       return f"Say hello to {name}!"
   ```

   ```python
   >>> hello("world")
   ['Hey there world!', 'Hi, world.']
   ```

Similarly, this behavior applies when using runtime `api_params` to specify multiple outputs.

   ```python
   >>> hello("world", api_params=dict(n=3))
   ['Hey there world!', 'Hi, world.', 'Hello, world!']
   ```

> **Note**: In the future, we may modify this interface as preserving the `api_params` keyword in its current form could potentially lead to conflicts with user-defined functions. However, during the beta phase, we are closely monitoring for feedback and will make adjustments based on user experiences and needs.

### Multimodal inputs

`@ell.simple` supports multimodal inputs, allowing you to easily work with both text and images in your language model programs. This is particularly useful for models with vision capabilities, such as GPT-4 with vision.

Here’s an example of how to use `@ell.simple` with multimodal inputs:

   ```python
   from PIL import Image
   import ell
   from ell.types.message import ImageContent

   @ell.simple(model="gpt-4-vision-preview")
   def describe_image(image: Image):
       return [
           ell.system("You are a helpful assistant that describes images."),
           ell.user(["What's in this image?", image])
       ]

   # Usage with PIL Image
   image = Image.open("path/to/your/image.jpg")
   description = describe_image(image)
   print(description)  # This will print a text description of the image
   ```

In these examples, the `describe_image` function takes a PIL Image object as input, while `describe_image_url` takes a string URL. The `ell.user` message combines both text and image inputs. `@ell.simple` automatically handles the conversion of the PIL Image object or ImageContent into the appropriate format for the language model.

This approach simplifies working with multimodal inputs, allowing you to focus on your application logic rather than the intricacies of API payloads.

> **Note**: Not all language model providers support image URLs. For example, as of the current version, Anthropic’s models do not support image URLs. Always check the capabilities and requirements of your chosen language model provider when working with multimodal inputs.

> **Warning**: While `@ell.simple` supports multimodal inputs, it is designed to return text-only outputs. For handling multimodal outputs (such as generated images or audio), you need to use `@ell.complex`. Please refer to the [@ell.complex](ell_complex.html) documentation for more information on working with multimodal outputs.

### What about multiturn conversations, tools, structured outputs, and other features?

While `@ell.simple` is great for straightforward text-based interactions with language models, there are scenarios where you might need more complex functionality. For instance, you may want to work with multiturn conversations, utilize tools, generate structured outputs, or handle multimodal content beyond just text.

In such cases, you’ll need an LMP that can return rich `Message` objects instead of just strings. This is where `@ell.complex` comes into play. The `@ell.complex` decorator provides enhanced capabilities for more sophisticated interactions with language models.

For more information on how to use `@ell.complex` and its advanced features, please refer to the [@ell.complex](ell_complex.html) documentation.

### Reference

#### `ell.simple`

   ```python
   ell.simple(model: str, client: Optional[openai.Client] = None, exempt_from_tracking: bool = False, **api_params)
   ```

The fundamental unit of language model programming in ell.

This decorator simplifies the process of creating Language Model Programs (LMPs) that return text-only outputs from language models, while supporting multimodal inputs. It wraps the more complex ‘complex’ decorator, providing a streamlined interface for common use cases.

**Parameters**:

- **model** (`str`) – The name or identifier of the language model to use.

- **client** (`Optional[openai.Client]`) – An optional OpenAI client instance. If not provided, a default client will be used.

- **exempt_from_tracking** (`bool`) – If True, the LMP usage won’t be tracked. Default is False.

- **api_params** (`Any`) – Additional keyword arguments to pass to the underlying API call.

**Usage**:

The decorated function can return either a single prompt or a list of `ell.Message` objects:

   ```python
   @ell.simple(model="gpt-4", temperature=0.7)
   def summarize_text(text: str) -> str:
       """You are an expert at summarizing text."""
       return f"Please summarize the following text:\n\n{text}"
   ```

**Note**:

- This decorator is designed for text-only model outputs, but supports multimodal inputs.

- For preserving complex model outputs (e.g., structured data, function calls, or multimodal outputs), use the `@ell.complex` decorator instead. `@ell.complex` returns a Message object (role=’assistant’).

   ```python
   @ell.simple(model="gpt-4", temperature=0.7)
   def generate_story(prompt: str) -> str:
       return f"Write a short story based on this prompt: {prompt}"
   ```

   ```python
   # Using default parameters
   story1 = generate_story("A day in the life of a time traveler")

   # Overriding parameters during function call
   story2 = generate_story("An AI's first day of consciousness", api_params={"temperature": 0.9, "max_tokens": 500})
   ```


---

# Structured Outputs

Structured outputs are essential for ensuring that language model responses are both controlled and predictable. By defining a clear schema for the expected output, we can leverage the power of language models to generate responses that adhere to specific formats and constraints.

Consider the following example, which demonstrates how to use Pydantic models to define structured outputs in ell:

1. Define the *MovieReview* model:

   ```python
   from pydantic import BaseModel, Field

   class MovieReview(BaseModel):
       title: str = Field(description="The title of the movie")
       rating: int = Field(description="The rating of the movie out of 10")
       summary: str = Field(description="A brief summary of the movie")

   @ell.complex(model="gpt-4o-2024-08-06", response_format=MovieReview)
   def generate_movie_review(movie: str) -> MovieReview:
       """You are a movie review generator. Given the name of a movie, you need to return a structured review."""
       return f"generate a review for the movie {movie}"
   ```

   By defining the *MovieReview* model, we ensure that the output of the *generate_movie_review* function adheres to a specific structure, making it easier to parse and utilize in downstream applications. This approach not only enhances the reliability of the generated content but also simplifies the integration of language model outputs into larger systems.

2. Access and manipulate structured outputs:

   ```python
   # Generate a movie review
   message = generate_movie_review("The Matrix")
   review = message.parsed

   # Access individual fields
   print(f"Movie Title: {review.title}")
   print(f"Rating: {review.rating}/10")
   print(f"Summary: {review.summary}")
   ```

   In this example, we first generate a movie review using our *generate_movie_review* function. We can then access individual fields of the structured output directly, as shown in the first part of the code.

> **Note**
>
> Structured outputs using Pydantic models are currently only available for the `gpt-4o-2024-08-06` model. For other models, you’ll need to manually prompt the model and enable JSON mode to achieve similar functionality.
>
> We purposefully chose to not opinionate prompting for other non-native json models because each prompt should be customized to the specific model and situation. For example, if you want to get gpt-3.5-turbo to return json you should explicitly allow it by prompting the model to do so:

3. Custom prompting for other models:

   ```python
   class MovieReview(BaseModel):
       title: str = Field(description="The title of the movie")
       rating: int = Field(description="The rating of the movie out of 10")
       summary: str = Field(description="A brief summary of the movie")

   @ell.simple(model="gpt-3.5-turbo")
   def generate_movie_review_manual(movie: str):
       return [
           ell.system(f"""You are a movie review generator. Given the name of a movie, you need to return a structured review in JSON format.
   You must absolutely respond in this format with no exceptions.
   {MovieReview.model_json_schema()}"""),
           ell.user(f"Review the movie: {movie}"),
       ]

   # parser support coming soon!
   unparsed = generate_movie_review_manual("The Matrix")
   parsed = MovieReview.model_validate_json(unparsed)
   ```


---

# Tool Usage

**Warning**  
Tool usage in ell is currently a beta feature and is highly underdeveloped. The API is likely to change significantly in future versions. Use with caution in production environments.

Tool usage is a powerful feature in ell that allows language models to interact with external functions and services. This capability enables the creation of more dynamic and interactive language model programs (LMPs) that can perform actions, retrieve information, and make decisions based on real-time data.

## Defining Tools

In ell, tools are defined using the `@ell.tool()` decorator. This decorator transforms a regular Python function into a tool that can be used by language models. Here’s an example of a simple tool definition:

```python
@ell.tool()
def create_claim_draft(claim_details: str,
                        claim_type: str,
                        claim_amount: float,
                        claim_date: str = Field(description="The date of the claim in the format YYYY-MM-DD.")):
    """Create a claim draft. Returns the claim id created."""
    print("Create claim draft", claim_details, claim_type, claim_amount, claim_date)
    return "claim_id-123234"
```

The `@ell.tool()` decorator automatically generates a schema for the tool based on the function’s signature, type annotations, and docstring. This schema is used to provide structured information about the tool to the language model.

## Schema Generation

ell uses a combination of function inspection and Pydantic models to generate the tool schema. The process involves:

- Extracting parameter information from the function signature.

- Using type annotations to determine parameter types.

- Utilizing Pydantic’s `Field` for additional parameter metadata.

- Creating a Pydantic model to represent the tool’s parameters.

This generated schema is then converted into a format compatible with the OpenAI API. For example:

```python
{
    "type": "function",
    "function": {
        "name": "create_claim_draft",
        "description": "Create a claim draft. Returns the claim id created.",
        "parameters": {
            "type": "object",
            "properties": {
                "claim_details": {
                    "type": "string"
                },
                "claim_type": {
                    "type": "string"
                },
                "claim_amount": {
                    "type": "number"
                },
                "claim_date": {
                    "type": "string",
                    "description": "The date of the claim in the format YYYY-MM-DD."
                }
            },
            "required": ["claim_details", "claim_type", "claim_amount", "claim_date"]
        }
    }
}
```

## Using Tools in LMPs

To use tools in a language model program, you need to specify them in the `@ell.complex` decorator:

```python
@ell.complex(model="gpt-4o", tools=[create_claim_draft], temperature=0.1)
def insurance_claim_chatbot(message_history: List[Message]) -> List[Message]:
    return [
        ell.system("""You are an insurance adjuster AI. You are given a dialogue with a user and have access to various tools to effectuate the insurance claim adjustment process. Ask questions until you have enough information to create a claim draft. Then ask for approval."""),
    ] + message_history
```

This allows the language model to access and use the specified tools within the context of the LMP.

## Single-Step Tool Usage

In single-step tool usage, the language model decides to use a tool once during its execution. The process typically involves the LMP receiving input, generating a response with a tool call.

Here’s an example where we want to take a natural language string for a website and convert it into a URL to get its content. We’ll call this LMP `get_website_content`, and it will allow the user to get the HTML page of any website they ask for in natural language. The chief goal of the language model here is to convert the website description into a URL and then invoke the `get_html_content` tool.

```python
@ell.tool()
def get_html_content(url: str = Field(description="The URL to get the HTML content of. Never include the protocol (like http:// or https://)")):
    """Get the HTML content of a URL."""
    response = requests.get("https://" + url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text()[:100]

@ell.complex(model="gpt-4o", tools=[get_html_content])
def get_website_content(website: str) -> str:
    """You are an agent that can summarize the contents of a website."""
    return f"Tell me what's on {website}"
```

We could also handle text based message responses from the language model where it may decline to call the tool or ask for clarification. 

## Multi-Step Tool Usage

Multi-step tool usage involves a more complex interaction where the language model may use tools multiple times in a conversation or processing flow. This is particularly useful for chatbots or interactive systems.

In a typical LLM API, the flow for multi-step tool usage looks like this:

1. You call the LLM with a message.

2. The LLM returns a message with a tool call.

3. You call the tools on your end and format the results back into a message.

4. You call the LLM with the tool result message.

5. The LLM returns a message with its final response.

This process can be error-prone and requires a lot of boilerplate code. To simplify this process, ell provides a helper function `call_tools_and_collect_as_message()`. This function executes all tool calls in a response and collects the results into a single message, which can then be easily added to the conversation history.

Here’s an example of a multi-step interaction using the insurance claim chatbot:

```python
@ell.complex(model="gpt-4o", tools=[create_claim_draft], temperature=0.1)
def insurance_claim_chatbot(message_history: List[Message]) -> List[Message]:
    return [
        ell.system("""You are an insurance adjuster AI. You are given a dialogue with a user and have access to various tools to effectuate the insurance claim adjustment process. Ask questions until you have enough information to create a claim draft. Then ask for approval."""), 
    ] + message_history

message_history = []
user_messages = [
    "Hello, I'm a customer",
    "I broke my car",
    "smashed by someone else, today, $5k",
    "please file it."
]

for user_message in user_messages:
    message_history.append(ell.user(user_message))
    response_message = insurance_claim_chatbot(message_history)
    message_history.append(response_message)

    if response_message.tool_calls:
        next_message = response_message.call_tools_and_collect_as_message()
        message_history.append(next_message)
        insurance_claim_chatbot(message_history)
```

## Future Features: Eager Mode

In the future, ell may introduce an “eager mode” for tool usage. This feature would automatically execute tool calls made by the language model, creating a multi-step interaction behind the scenes. This could streamline the development process by reducing the need for explicit tool call handling in the code.

Eager mode could potentially work like this:

- The LMP generates a response with a tool call.

- ell automatically executes the tool and captures its result.

- The result is immediately fed back into the LMP for further processing.

- This cycle continues until the LMP generates a final response without tool calls.

This feature would make it easier to create complex, multi-step interactions without the need for explicit loop handling in the user code. It would be particularly useful for scenarios where the number of tool calls is not known in advance, such as in open-ended conversations or complex problem-solving tasks.

## Future Features: Tool Spec Autogeneration

**Note**  
Thanks to [Aidan McLau](https://x.com/aidan_mclau) for suggesting this feature.

In an ideal world, a prompt engineering library would not require the user to meticulously specify the schema for a tool. Instead, a language model should be able to infer the tool specification directly from the source code of the tool. In ell, we can extract the lexically closed source of any Python function, enabling a feature where the schema is automatically generated by another language model when a tool is given to an ell decorator.

This approach eliminates the need for users to manually type every argument and provide a tool description, as the description becomes implicit from the source code.


---

# Versioning & Tracing

Prompt Engineering is the process of rapidly iterating on the set of system, user, and pre-packaged assistant messages sent to a language model. The goal is to maximize some explicit or implied objective function. In an ideal scientific scenario, we would have reward models or metrics that could automatically assess the quality of prompts. One would simply modify the text or formatting of the sent messages to maximize this objective.

However, the reality of this process is much messier. Often, a prompt engineer will work on a few examples for the language model program they’re trying to develop, tweaking the prompt slightly over time, testing and hoping that the resulting outputs seem better in practice. This process comes with several issues:

1. It’s often unclear if a change in a prompt will uniformly improve the quality of a language model program.

2. Sometimes regressions are introduced, unknown to the prompt engineer, due to dependencies elsewhere in the codebase.

3. The process of testing different hypotheses and then reverting those tests often involves using the undo/redo shortcuts in the editor of choice, which is not ideal for tracking changes.

## Checkpointing prompts

A solution to this problem can be found by drawing analogies to the training process in machine learning. Prompt engineering, in essence, is a form of parameter search. We modify a model over time with local updates, aiming to maximize or minimize some global objective function.

In machine learning, this process is known as the training loop. Each instance of the model’s parameters is called a checkpoint. These checkpoints are periodically saved and evaluated for quality. If a hyperparameter change leads to a failure in the training process, practitioners can quickly revert to a previous checkpoint, much like version control in software engineering.

However, versioning or checkpointing prompts during the prompt engineering process is cumbersome with standard language model API calls or current frameworks. Prompt engineers often resort to inefficient methods:

- Checking in prompt code to version control systems like git for every minor change during the iterative prompt engineering process

- Storing commit hashes alongside outputs for comparison

- Saving prompts and outputs to text files

These approaches are highly cumbersome and go against typical version control workflows in software development. Some prompt engineering frameworks offer versioning, but they often require the use of pre-built IDEs or specific naming conventions. This approach doesn’t align well with real-world LLM applications, where calls are often scattered throughout a codebase.

A key feature of `ell` is its behind-the-scenes version control system for language model programs. This system allows for comparison, visualization, and storage of prompts as the codebase evolves, both in production and development settings. Importantly, it requires no changes to the prompt engineer’s workflow.

### Serializing prompts via lexical closures

This automatic versioning is possible because `ell` treats prompts as discrete functional units called language model programs. By encapsulating the prompt within a function, we can use static and dynamic analysis tools to extract the source code of a prompt program and all its lexical dependencies at any point in time. This approach captures the exact set of source code needed to reproduce the prompt.

Consider the following function embedded in a large code base.

```python
from myother_module import CONSTANT

def other_code():
    print("hello")

def some_other_function():
    return "to bob"

@ell.simple(model="gpt-4o")
def hi():
    """You are a helpful assistant"""
    return f"say hi {some_other_function()} {CONSTANT} times."

def some_other_code():
    return "some other code"
```

What does it mean to serialize and version the LMP *hi* above? A first approach might be to simply capture the source code of the function body and its signature.

```python
@ell.simple(model="gpt-4o")
def hi():
    """You are a helpful assistant"""
    return f"say hi {some_other_function()} {CONSTANT} times."
```

However, this approach isn’t quite sufficient. If the dependency *some_other_function* changes, the language model program *hi* has fundamentally changed as well. Consequently, all the outputs you expect to see when calling it would also change. Fortunately, the solution is to compute the lexical closure. The lexical closure of a function is essentially its source code along with the source of every global and free variable that it depends on. For example:

```python
>>> lexical_closure(hi)
'''
CONSTANT = 6

def some_other_function():
    return "to bob"

@ell.simple(model="gpt-4o")
def hi():
    """You are a helpful assistant"""
    return f"say hi {some_other_function()} {CONSTANT} times."
'''
```

Full closure can be computed through static analysis by inspecting the Abstract Syntax Tree (AST) of the function and all of its bound globals. This process recursively enumerates dependencies to compute a minimal set of source code that would enable you to reproduce the function. For brevity, we can ignore system and user libraries that were installed by package managers, as these are typically considered part of the execution environment rather than the function’s specific closure.

### Constructing a dependency graph

In addition, when a language model program depends on another prompt (i.e., when one language model program calls another), the dependent prompt will automatically appear within the lexical closure of the calling prompt. This allows us to construct a computation graph that illustrates how language model programs depend on one another to execute, effectively leveraging test-time compute. This graph provides a clear visualization of the relationships and dependencies between different prompts in a complex language model program.

```python
import ell
from typing import List

@ell.simple(model="gpt-4o-mini", temperature=1.0)
def generate_story_ideas(about: str):
    """You are an expert story ideator. Only answer in a single sentence."""
    return f"Generate a story idea about {about}."

@ell.simple(model="gpt-4o-mini", temperature=1.0)
def write_a_draft_of_a_story(idea: str):
    """You are an adept story writer. The story should only be 3 paragraphs."""
    return f"Write a story about {idea}."

@ell.simple(model="gpt-4-turbo", temperature=0.2)
def choose_the_best_draft(drafts: List[str]):
    """You are an expert fiction editor."""
    return f"Choose the best draft from the following list: {'\n'.join(drafts)}."
```

## Versioning

With the ability to checkpoint and serialize prompts, we can now facilitate a key promise of a useful prompt engineering library: automatic versioning.

Prompt versioning comes in two flavors: automatic versioning during the prompt engineering process, and archival versioning in storage during production deployments. The former is important for the reasons previously mentioned; as a prompt engineer changes and tunes the prompt over time, they may often revert to previous versions or need to compare across them. The latter is crucial for debugging and regression checks of production deployments, as well as the creation of large-scale fine-tuning and comparison datasets. `ell` is designed with both of these in mind.

In designing `ell`, it was essential that this versioning system happened entirely behind the scenes and did not dictate any specific way in which the prompt engineer needs to facilitate their own process. Therefore, to enable automatic versioning, one simply passes in a storage parameter to the initialization function of `ell`, where various settings are configured:

```python
ell.init(store='./logdir')
```

The argument `store` points to either a local path to store data or an `ell.storage.Store` object. An `ell` store is an interface for storing prompts and their invocations, i.e., the input and outputs of a language model program as well as the language model called, generated, and any other metadata. By default, when a path is specified, `ell` uses a local SQLite DB and an expandable file-based blob store for larger language model programs or invocations that cannot effectively fit into rows of the database.

> **Note:** For production use, `ell` can utilize a store in any arbitrary database. In the near future, `ell` will be launching a service similar to Weights & Biases (wandb), where your team can store all prompts in a centralized prompt version control system. This will provide collaborative features and advanced versioning capabilities, much like what wandb offers for machine learning experiments.

When `ell` is initialized with a store of any kind, anytime a language model program is invoked (actually, the first time it’s invoked), the lexical closure of source of that language model program is computed and hashed to create a version hash for that language model program. In addition, the aforementioned dependency graph is computed, and this language model program is then written to the store. After the invocation occurs, all of the input and output data associated with that version of the language model program is also stored in the database for later analysis. As the prompt engineering process continues, new versions of the language model programs are only added to the store if they are invoked at least once.

```python
import ell
from ell.stores.sql import SQLiteStore

ell.init(store='./logdir', autocommit=True)

@ell.simple(model="gpt-4o-mini")
def greet(name: str):
    """You are a friendly greeter."""
    return f"Generate a greeting for {name}."

result = greet("Alice")
print(result)  # Output: "Hello, Alice! It's wonderful to meet you."
```

After this execution, a row might be added to the *SerializedLMP* table:

```
lmp_id: "1a2b3c4d5e6f7g8h"
name: "greet"
source: "@ell.simple(model=\"gpt-4o-mini\")\ndef greet(name: str):\n    \"\"\"You are a friendly greeter.\"\"\"\n    return f\"Generate a greeting for {name}.\""
dependencies: ""
created_at: "2023-07-15T10:30:00Z"
lmp_type: "LM"
api_params: {"model": "gpt-4o-mini"}
initial_free_vars: {}
initial_global_vars: {}
num_invocations: 1
commit_message: "Initial version of greet function"
version_number: 1
```

And a corresponding row in the *Invocation* table:

```
id: "9i8u7y6t5r4e3w2q"
lmp_id: "1a2b3c4d5e6f7g8h"
latency_ms: 250.5
prompt_tokens: 15
completion_tokens: 10
created_at: "2023-07-15T10:30:01Z"
```

With its associated *InvocationContents*:

```
invocation_id: "9i8u7y6t5r4e3w2q"
params: {"name": "Alice"}
results: ["Hello, Alice! It's wonderful to meet you."]
invocation_api_params: {"temperature": 1.0, "max_tokens": 50}
```

This structure allows for efficient tracking and analysis of LMP usage and performance over time.

### Autocommitting

Because prompts are just their source code and versions and diffs between versions are automatically computed in the background, we can additionally automatically create human-readable commit messages between versions:

```python
ell.init(store='./logdir', autocommit=True)
```

By providing the `autocommit=True` argument to the initialization function for `ell`, every time a version is created that supersedes a previous version of a prompt (as collocated by their fully qualified name), `ell` will use GPT-4-mini to automatically generate a human-readable commit message that can then be viewed later to show effective changes across versions. This works both for the local automatic prompt versioning during prompt engineering to quickly locate an ideal prompt or previous prompt that was developed, and for archival prompt versioning in production when seeking out regressions or previously differently performing language model programs.

## Tracing

Central to the prompt engineering process is understanding not just how prompts change, but how they are used.

Traditionally, without a dedicated prompt engineering framework, developers resort to manually storing inputs and outputs from language model API providers. This approach typically involves intercepting API calls and constructing custom database schemas for production applications. However, this method often proves cumbersome, lacking scalability across projects and necessitating frequent re-implementation.

To address these challenges, solutions like Weave and LangChain/LangSmith have emerged, each offering distinct approaches:

1. **Function-level tracing:** This method captures inputs and outputs of arbitrary Python functions. While effective for monitoring production deployments, it falls short in tracking intra-version changes that often occur during local development and prompt engineering iterations.

2. **Framework-specific versioning:** This approach, exemplified by LangChain, requires prompts to be versioned within a specific framework. Prompts are typically compressed into template strings or combinations of template strings and versioned Python code. While structured, this method can be restrictive and may not suit all development workflows.

`ell` takes the best of both worlds by serializing arbitrary Python code. This allows us to track how language model programs are used through their inputs and outputs, organizing these uses by version for later comparison. Importantly, this is achieved without requiring users to do anything more than write normal Python code to produce their prompt strings for the language model API.

### Constructing a computation graph

When using the `ell` store, all inputs and outputs of language model programs are stored. But what about interactions between them?

To track how language model programs interact during execution and construct a computation graph of data flow (similar to deep learning frameworks like PyTorch and TensorFlow), `ell` wraps the outputs of all language model programs with a tracing object.

Tracing objects are wrappers around immutable base types in Python. They keep track of originating language model programs and other metadata, preserving this trace of origination across arbitrary operations. One of the most important tracing objects is the _lstr object.

For example, consider the following language model program:

```python
import ell

@ell.simple(model="gpt-4o")  # version: ae8f32s664200e1
def hi():
    return "say hi"

x = hi()  # invocation id: 4hdfjhe8ehf (version: ae8f32s664200e1)
```

While x in this example is functionally a string and behaves exactly like one, it is actually an _lstr:

```python
>>> type(x)
<class 'ell.types._lstr.lstr'>

>>> x
'hi'

>>> x.__origin_trace__
{'4hdfjhe8ehf'}
```

Furthermore, continued manipulation of the string preserves its origin trace, as all original string operations are overridden to produce new immutable instances that contain or combine origin traces.

```python
>>> x[0]
'h'
```

```python
>>> x[0].__origin_trace__
{'4hdfjhe8ehf'}
```

```python
>>> x + " there"
'hi there'
```

```python
>>> (x + " there").__origin_trace__
{'4hdfjhe8ehf'}
```

Additionally, when two mutable objects are combined, the resulting trace is the union of the two traces.

```python
>>> x = hi()  # invocation id: 4hdfjhe8ehf
>>> y = hi()  # invocation id: 345hef345h
>>> z = x + y
>>> z.__origin_trace__
{'4hdfjhe8ehf', '345hef345h'}
```

By tracking both inputs and outputs of language model programs, we can use these origin traces to construct a computation graph. This graph illustrates how language model programs interact during execution.

This capability allows you to easily track the flow of language model outputs, identify weak points in prompt chains, understand unintended mutations in inputs and outputs of prompts as they are executed, and more generally, create a path for future symbolic and discrete optimization techniques applied to language model programs.

In the next chapter, we will explore how to visualize versioning and tracing data using `ell studio`. This powerful tool provides a comprehensive interface for analyzing and understanding the complex interactions within your language model programs.
