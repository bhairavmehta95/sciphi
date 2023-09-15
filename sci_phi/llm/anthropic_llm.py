"""A module for creating Anthropic models."""

from dataclasses import dataclass

from anthropic import AI_PROMPT, HUMAN_PROMPT, Anthropic

from sci_phi.core import ProviderName
from sci_phi.llm.base import LLM, LLMConfig
from sci_phi.llm.config_manager import model_config


@model_config
@dataclass
class AnthropicConfig(LLMConfig):
    """Configuration for Anthropic models."""

    # Base
    provider_name: ProviderName = ProviderName.ANTHROPIC
    model_name: str = "claude-2"
    version: str = "0.1.0"
    temperature: float = 0.7
    top_p: float = 1.0

    # Anthropic Extras
    top_k: float = 100.0
    stream: bool = False
    max_tokens_to_sample: int = 256


class AnthropicLLM(LLM):
    """A concrete class for creating Anthropic models."""

    def __init__(
        self,
        config: AnthropicConfig,
    ) -> None:
        super().__init__(
            config,
        )
        self.anthropic = Anthropic()
        if not self.anthropic.api_key:
            raise ValueError(
                "Anthropic API key not found. Please set the ANTHROPIC_API_KEY environment variable."
            )

    def get_completion(self, prompt: str) -> str:
        """Get a completion from the Anthropic API based on the provided messages."""

        formatted_prompt = f"{HUMAN_PROMPT} {prompt} {AI_PROMPT}"

        completion = self.anthropic.completions.create(
            model=self.model_name.value,
            prompt=formatted_prompt,
            temperature=self.config.temperature,
            top_p=self.config.top_p,
            top_k=self.config.top_k,
            max_tokens_to_sample=self.config.max_tokens_to_sample,
            stream=self.config.stream,
        )  # type: ignore

        return completion.completion