# Ollama Option Surface, Environment Variables, and Free Open-Source Backend Alternatives

## Executive readout

Your current `SUPPORTED_OPTIONS` set is not aligned with the current Ollama server. In the current server code, Ollama validates `options` against a fixed server-side `api.Options` schema and warns on unknown keys instead of treating them as model-defined free-form settings. That means the option namespace is **not purely “whatever the model wants”**. It is a hybrid: the **keys** are mostly determined by the Ollama server version, while the **effect** of some keys is still model- and capability-dependent. citeturn8view0turn7view0turn22view0

For your specific snippet, `plan` does **not** belong in Ollama generation `options`. In the current official code, `plan` appears in cloud/user-related response structs, not in `GenerateRequest`, `ChatRequest`, or `api.Options`. By contrast, your set is missing several current server-side options, including `num_keep`, `typical_p`, `presence_penalty`, `frequency_penalty`, `main_gpu`, `use_mmap`, and `num_thread`. citeturn16view0turn2view0turn9search1

The other important finding is source drift. Ollama’s Modelfile docs currently document a smaller parameter subset; the API docs still show an example that claims to set “every available option”; and the official JavaScript and Python SDK typings still expose a larger, older superset that includes keys the current server code no longer defines. If you need one canonical allow-list for your app, the **running server version** or its matching source is the least misleading source of truth. citeturn4view0turn22view0turn24view0turn26view0turn8view0

## What Ollama currently accepts in `options`

If your backend is meant to mirror the **current Ollama server-side `options` object**, the effective allow-list in the current official source is:

```python
SUPPORTED_OPTIONS = {
    "num_keep",
    "seed",
    "num_predict",
    "top_k",
    "top_p",
    "min_p",
    "typical_p",
    "repeat_last_n",
    "temperature",
    "repeat_penalty",
    "presence_penalty",
    "frequency_penalty",
    "stop",
    "num_ctx",
    "num_batch",
    "num_gpu",
    "main_gpu",
    "use_mmap",
    "num_thread",
}
```

That list comes from the current `api.Options` struct plus the embedded runner fields, and the `FromMap` parser warns and skips keys that are not present in that struct. citeturn2view0turn9search1turn8view0

Compared with your current set, the gaps are straightforward. You are **missing** `num_keep`, `typical_p`, `presence_penalty`, `frequency_penalty`, `main_gpu`, `use_mmap`, and `num_thread`. You also have one clear **extra**: `plan`. Based on current official code, `plan` is not an Ollama generation option and should not be in an `options` allow-list. citeturn2view0turn9search1turn16view0

It is also worth separating **top-level request fields** from `options` keys. In current Ollama request structs, things like `keep_alive`, `think`, `logprobs`, `top_logprobs`, `raw`, `format`, `truncate`, `shift`, `tools`, `images`, and the experimental image-generation fields (`width`, `height`, `steps`) are request-level fields, not `options` entries. If your command-and-control layer flattens everything into one option bucket, it will blur two different surfaces that Ollama keeps separate. citeturn7view0turn7view1

## Why this is partly server-defined and partly model-defined

Your instinct that “some of this might actually be an individual model thing” is partly right, but only partly. Ollama’s request structs explicitly describe `Options` as **model-specific options**, with the example that something like `temperature` can be set through this field “if the model supports it.” At the same time, the server still validates the keys against its own option schema. So the practical rule is: **the key names are Ollama-version-defined; the runtime impact is model-dependent**. citeturn7view0turn8view0

Ollama’s own API docs reinforce that split. They say you can use `options` to set custom values at runtime instead of baking them into the model’s `Modelfile`, which means the model may carry defaults while the request overrides them. That is another reason not to think of `options` as either “purely server-global” or “purely model-native.” They sit at the boundary between the Ollama runtime and the model’s configured behavior. citeturn22view0turn4view0

There are also capability-gated fields outside `options`. The current request structs mark `think` as applying to supported thinking models, tools as optional model-accessible tools, multimodal `images` as model-dependent, and the image-generation fields as experimental and only relevant to image-generation models. So for your app architecture, the cleanest mental model is: **backend schema**, **backend request fields**, and **model capabilities** are three separate layers. citeturn7view0turn7view1

## Where the official Ollama sources currently drift

The current Modelfile reference documents a relatively small parameter set: `num_ctx`, `repeat_last_n`, `repeat_penalty`, `temperature`, `seed`, `stop`, `num_predict`, `top_k`, `top_p`, and `min_p`. That means if you build your allow-list only from the Modelfile docs, you will under-accept compared with the current server code. citeturn4view0

The official API docs go the other direction. The “Generate request (With options)” example says it sets “every available option,” and the example includes `num_keep`, `typical_p`, `presence_penalty`, `frequency_penalty`, `num_ctx`, `num_batch`, `num_gpu`, `main_gpu`, `use_mmap`, and `num_thread`, which match the current server. But that same example also includes `penalize_newline` and `numa`, which do **not** appear in the current server’s `api.Options` schema. On a current server, extra unknown keys are warned as invalid and skipped. citeturn22view0turn8view0

The official SDK typings are looser still. The current official JavaScript and Python clients expose a much larger option superset that still includes older or legacy-looking fields such as `numa`, `low_vram`, `f16_kv`, `logits_all`, `vocab_only`, `use_mlock`, `embedding_only`, `tfs_z`, `mirostat`, `mirostat_tau`, `mirostat_eta`, and `penalize_newline`. Those SDK typings are useful for compatibility, but they are not a reliable reflection of the **current server parser**. If you want your controller to be strict, the server source is the better authority. If you want it to be forgiving, the SDK-era superset is useful as a compatibility layer, but you should warn that some keys may be ignored by current Ollama. citeturn24view0turn26view0turn8view0

## The current Ollama environment variable surface

The current core environment surface comes from Ollama’s `envconfig/config.go`, and the FAQ shows that these variables are intended to be scoped at the OS, process, service, or container level: on macOS via `launchctl`, on Linux via `systemctl` service environment entries, and on Windows via user/system environment variables. In practice, that means they **can** be overridden locally in the sense of “for this shell, service, unit, or container,” but most of them are **not** request-level overrides. citeturn11view0turn39view0

The **server, network, and storage** controls are `OLLAMA_HOST` for bind address, `OLLAMA_ORIGINS` for additional allowed origins, `OLLAMA_MODELS` for the models directory, `OLLAMA_REMOTES` for allowed remote model hosts, `OLLAMA_LLM_LIBRARY` to force the LLM library instead of autodetection, `OLLAMA_NEW_ENGINE` to enable the new engine, and `OLLAMA_VULKAN` for experimental Vulkan support on non-macOS builds. These are startup/process-scoped controls; there is no documented per-request override for them. citeturn11view0turn21view0turn39view0

The **logging, scheduling, queueing, and residency** controls are `OLLAMA_DEBUG`, `OLLAMA_DEBUG_LOG_REQUESTS`, `OLLAMA_KEEP_ALIVE`, `OLLAMA_LOAD_TIMEOUT`, `OLLAMA_MAX_LOADED_MODELS`, `OLLAMA_MAX_TRANSFER_STREAMS`, `OLLAMA_MAX_QUEUE`, `OLLAMA_NUM_PARALLEL`, `OLLAMA_SCHED_SPREAD`, `OLLAMA_MULTIUSER_CACHE`, and `OLLAMA_GPU_OVERHEAD`. Of that group, `OLLAMA_KEEP_ALIVE` is the main one with a request-level analog, because current generate/chat requests also expose a top-level `keep_alive` field. The rest are effectively server runtime knobs. citeturn11view0turn21view0turn7view0turn7view1

The **model execution defaults** are where overrides matter most. `OLLAMA_CONTEXT_LENGTH` sets the default context length, and Ollama’s docs explicitly show that it can be overridden per run via `/set parameter num_ctx` or per API request via `options.num_ctx`. The context-length docs also say the server’s default context choice now varies with available VRAM. `OLLAMA_FLASH_ATTENTION` enables flash attention. `OLLAMA_KV_CACHE_TYPE` controls K/V cache quantization; the FAQ documents it as a **global** option, with `f16`, `q8_0`, and `q4_0` as the current values it documents. citeturn39view0turn14view1turn11view0turn38search14

The **CLI, cloud, and auth-adjacent** controls are `OLLAMA_NOHISTORY`, `OLLAMA_NOPRUNE`, `OLLAMA_EDITOR`, `OLLAMA_NO_CLOUD`, and `OLLAMA_AUTH`. `OLLAMA_NO_CLOUD` is special because current code checks both the environment variable and `~/.ollama/server.json` with `disable_ollama_cloud`, so it has a second local configuration path beyond the environment itself. `OLLAMA_AUTH` is also special: the current code defines it as enabling authentication between the Ollama client and server, while the auth docs separately note that local API access does not require authentication by default. citeturn13view4turn11view0turn19view0turn18view0

The **proxy and device-selection** variables are `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY`, plus lowercase `http_proxy`, `https_proxy`, and `no_proxy` on non-Windows systems, and `CUDA_VISIBLE_DEVICES`, `HIP_VISIBLE_DEVICES`, `ROCR_VISIBLE_DEVICES`, `GGML_VK_VISIBLE_DEVICES`, `GPU_DEVICE_ORDINAL`, and `HSA_OVERRIDE_GFX_VERSION` on non-macOS builds. Ollama’s FAQ explicitly recommends `HTTPS_PROXY` for model pulls and warns against `HTTP_PROXY` because model pulls use HTTPS and `HTTP_PROXY` can interrupt client connections to the local server. citeturn11view0turn39view0

There is one more environment variable you should keep separate from local `ollama serve` configuration: `OLLAMA_API_KEY`. The auth docs use it for direct access to the `ollama.com` API, not for configuring the local Ollama server process. In other words, it belongs in your “cloud provider/client auth” layer, not your “local Ollama backend settings” layer. citeturn18view0

## Free open-source alternatives that make sense for a command-and-control app

**llama.cpp** is the leanest self-hosted alternative if your app needs a local server with a small footprint and GGUF-first model support. Its project goal is LLM inference with minimal setup across a wide range of hardware, and its `llama-server` component exposes a lightweight OpenAI-compatible HTTP server with chat completions, embeddings, reranking, multi-user support, and parallel decoding. It is MIT-licensed. citeturn35view0turn30view0turn35view1

**vLLM** is the strongest general-purpose choice if you care about throughput, batching, and modern serving features more than “it runs everywhere.” The project describes itself as a high-throughput, memory-efficient inference and serving engine, and its quickstart docs say it can run as an OpenAI-compatible server that acts as a drop-in replacement for OpenAI-style clients. It is Apache 2.0 licensed. For a controller app, this is one of the best targets if you expect GPU-backed multi-user load. citeturn30view1turn34view0turn35view2

**SGLang** is another strong performance-oriented backend, especially if you want an OpenAI-compatible API surface but also care about broader hardware and model coverage. The official docs say SGLang provides OpenAI-compatible APIs for smooth migration from OpenAI services to self-hosted local models, and the project advertises broad model support plus support across NVIDIA, AMD, Intel Xeon, Google TPU, and Ascend hardware. It is Apache 2.0 licensed. citeturn36search0turn30view5turn35view5

**LocalAI** is the closest “Swiss army knife” alternative if you want one backend that can front many engines. The project describes itself as an open-source AI engine that can run LLMs, vision, voice, image, and video models on many kinds of hardware, says it offers drop-in compatibility with OpenAI, Anthropic, and ElevenLabs-style APIs, and lists dozens of underlying backends including llama.cpp and vLLM. It is MIT-licensed. For a control-center app, LocalAI is attractive when you want a **meta-backend** rather than one inference stack. citeturn30view3turn35view4

**Xinference** is the most obviously “serving platform” oriented option in this set. Its official repo presents it as a way to serve language, speech, and multimodal models with a unified API, single-command startup, OpenAI-compatible REST API support, heterogeneous CPU/GPU usage, and distributed deployment. It is Apache 2.0 licensed. If your app may eventually need multi-node deployment, non-LLM modalities, or a richer control plane, it is a credible Ollama alternative. citeturn32view0turn32view2turn32view3

**Hugging Face Text Generation Inference** is still worth knowing about because it offers an OpenAI-compatible chat-completions-style API and remains Apache 2.0 licensed, but there is an important current caveat: the official GitHub repository is archived and read-only as of March 21, 2026. For a new backend integration in 2026, that makes it a legacy option rather than a first-choice target. citeturn30view2turn35view3

## What I would change in your app design

For your controller app, I would keep **three separate allow-lists** instead of one giant bag of “options”: a list for Ollama `options`, a list for top-level request fields, and a capability map for model-dependent features such as thinking, tools, multimodal inputs, logprobs, and image generation. That separation matches the current Ollama request structs much more closely and prevents bugs where a valid request field gets shoved into `options` or where a stale SDK option gets treated as current. citeturn7view0turn7view1turn8view0

I would also remove `plan` from Ollama `SUPPORTED_OPTIONS`, add the current server-defined keys listed earlier, and decide whether you want a **strict** mode or a **compatibility** mode. In strict mode, only the current server keys pass. In compatibility mode, you can accept legacy SDK-era keys like `mirostat`, `tfs_z`, `penalize_newline`, `numa`, `low_vram`, `f16_kv`, `use_mlock`, and `embedding_only`, but mark them as “legacy/SDK-visible, may be ignored by current Ollama server.” Given the current source drift, that is the cleanest way to avoid both false rejects and silent no-ops. citeturn24view0turn26view0turn22view0turn8view0

The shortest blunt summary is this: **your gut was directionally right, but the key names themselves are not mainly model-defined**. For current Ollama, the canonical `options` namespace is controlled by the server version; the model mainly affects whether a given knob has meaning, what defaults are already baked into the model, and whether adjacent top-level features like thinking, tools, or multimodality are actually supported. citeturn7view0turn22view0turn8view0