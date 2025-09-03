"""Sample random mutation plugin."""

import random
from typing import Any, Dict
from evosuite.plugins import Mutator, PluginMetadata


class RandomMutator(Mutator):
    """Applies random mutations to candidates."""
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="random_mutator",
            version="0.2.0", 
            description="Applies random mutations with configurable strength",
            author="EvoSuite Team",
            provides=["mutation.random"],
            requires_core=">=0.2,<0.3"
        )
    
    async def mutate(self, candidate: Any, context: Dict[str, Any]) -> Any:
        """Apply random mutation to candidate."""
        mutation_rate = self.config.get("mutation_rate", 0.1)
        mutation_strength = self.config.get("mutation_strength", 1.0)
        
        # Handle different candidate types
        if isinstance(candidate, str):
            return self._mutate_string(candidate, mutation_rate, mutation_strength)
        elif isinstance(candidate, list):
            return self._mutate_list(candidate, mutation_rate, mutation_strength)
        elif isinstance(candidate, dict):
            return self._mutate_dict(candidate, mutation_rate, mutation_strength)
        else:
            # For unknown types, return with minor random perturbation
            return f"{candidate}_mutated_{random.randint(1, 1000)}"
    
    def _mutate_string(self, s: str, rate: float, strength: float) -> str:
        """Mutate string by randomly changing characters."""
        chars = list(s)
        for i in range(len(chars)):
            if random.random() < rate:
                # Simple character substitution
                chars[i] = chr((ord(chars[i]) + random.randint(1, int(strength * 10))) % 128)
        return ''.join(chars)
    
    def _mutate_list(self, lst: list, rate: float, strength: float) -> list:
        """Mutate list by randomly modifying elements."""
        result = lst.copy()
        for i in range(len(result)):
            if random.random() < rate:
                if isinstance(result[i], (int, float)):
                    result[i] += random.uniform(-strength, strength)
                elif isinstance(result[i], str):
                    result[i] = self._mutate_string(result[i], rate, strength)
        return result
    
    def _mutate_dict(self, d: dict, rate: float, strength: float) -> dict:
        """Mutate dictionary by randomly modifying values."""
        result = d.copy()
        for key, value in result.items():
            if random.random() < rate:
                if isinstance(value, (int, float)):
                    result[key] = value + random.uniform(-strength, strength)
                elif isinstance(value, str):
                    result[key] = self._mutate_string(value, rate, strength)
                elif isinstance(value, list):
                    result[key] = self._mutate_list(value, rate, strength)
        return result