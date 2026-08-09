# Framework integration boundary

Keep framework-specific Tavily components behind the same application-owned adapter used by direct
SDK calls. Framework defaults must not silently control result count, raw-content inclusion,
timeouts, retries, or logging.

Map the framework's tool input and output to validated local types. Preserve source URLs and error
classes; do not flatten provider failure into an empty result. Apply prompt-injection and content
sanitization controls before retrieved text enters an agent or renderer.

Pin integration packages independently from the core SDK and verify their compatibility in the
current official documentation. Test serialization, async/cancellation behavior, callback tracing,
and version upgrades at the adapter boundary. Do not keep copied LangChain, LlamaIndex, CrewAI,
Vercel AI SDK, or other framework signatures in this repository.
