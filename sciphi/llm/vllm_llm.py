"""A module for managing local vLLM models."""

from dataclasses import dataclass

from sciphi.core import ProviderName
from sciphi.llm.base import LLM, LLMConfig
from sciphi.llm.config_manager import model_config


@model_config
@dataclass
class vLLMConfig(LLMConfig):
    """Configuration for local vLLM models."""

    # Base
    provider_name: ProviderName = ProviderName.VLLM
    model_name: str = "gpt2"
    temperature: float = 0.7
    top_p: float = 1.0

    # Generation parameters
    top_k: int = 100
    max_tokens_to_sample: int = 256


class vLLM(LLM):
    """Configuration for local vLLM models."""

    def __init__(
        self,
        config: vLLMConfig,
    ) -> None:
        super().__init__(config)
        try:
            from vllm import LLM as vvLLM
            from vllm import SamplingParams
        except ImportError:
            raise ImportError(
                "Please install the vllm package before attempting to run with an vLLM model. This can be accomplished via `poetry install -E vllm_support, ...OTHER_DEPENDENCIES_HERE`."
            )
        self.model = vvLLM(model=config.model_name)
        self.sampling_params = SamplingParams(
            temperature=config.temperature,
            top_p=config.top_p,
            top_k=config.top_k,
            max_tokens=config.max_tokens_to_sample,
        )

    def get_chat_completion(self, messages: list[dict[str, str]]) -> str:
        """Get a completion from the OpenAI API based on the provided messages."""
        raise NotImplementedError(
            "Chat completion not yet implemented for vLLM."
        )

    def get_instruct_completion(self, prompt: str) -> str:
        """Get an instruction completion from local vLLM API."""
        outputs = self.model.generate([prompt], self.sampling_params)
        return outputs[0].outputs[0].text

    def get_batch_instruct_completion(self, prompts: list[str]) -> list[str]:
        """Get batch instruction completion from local vLLM."""
        raw_outputs = self.model.generate(prompts, self.sampling_params)
        return [ele.outputs[0].text for ele in raw_outputs]
