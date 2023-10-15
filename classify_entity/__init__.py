"""
"""
import json
import numpy as np
from typing import List, Dict
from .entity import Entity
from .flag import Flag
from sklearn.metrics.pairwise import cosine_similarity


class ClassifyEntity:
    """
    ClassifyEntity finds the legal entity that best fits a user's business needs.
    It finds the ideal order to ask questions about the user's business and sorts
    the legal entities based on similarity to the user's answers.
    Args:
        _entities (List[Entity]): List of entities.
        _flags (List[Flag]): List of flags.
        _flag_index_mapping (Dict[str, int]): Mapping of flag mnemonics
        to flag indexes.
        _entity_vector_mapping (Dict[str, List[int]]): Mapping of entity
        mnemonics to entity flag vectors.
        _flag_variance_matrix (np.ndarray): Variance matrix of flags.
        _sorted_flag_indexes (List[int]): List of flag indexes sorted by variance.
        _input_flags (List[str]): List of input flags.
        _entity_similarity_vector (np.ndarray): Vector of entity similarities
        to input flags.
    """

    _docs_dir: str
    _entities: List[Entity] = []
    _flags: List[Flag] = []
    _flag_index_mapping: Dict[str, int] = {}
    _entity_vector_mapping: Dict[str, List[int]] = {}
    _flag_variance_matrix: np.ndarray = np.array([])
    _sorted_flag_indexes: List[int] = []
    _input_flags: List[str] = []
    _entity_similarities: Dict[str, float] = {}

    def __init__(self, entities_json_path: str, flags_json_path: str, docs_dir: str):
        """
        Args:
            entities_json_path (str): Path to the entities JSON file.
            flags_json_path (str): Path to the flags JSON file.
        """
        self._docs_dir = docs_dir

        with open(entities_json_path, "r") as entities_json_file:
            raw_entities = json.load(entities_json_file)

        with open(flags_json_path, "r") as flags_json_file:
            raw_flags = json.load(flags_json_file)

        for raw_entity in raw_entities["entities"]:
            flag_mnemonics = raw_entity["flags"]
            flags = []
            for flag_mnemonic in flag_mnemonics:
                for raw_flag in raw_flags["flags"]:
                    if raw_flag["mnemonic"] == flag_mnemonic:
                        flags.append(
                            Flag(
                                raw_flag["mnemonic"],
                                raw_flag["name"],
                                raw_flag["description"],
                                raw_flag["question"],
                                raw_flag["deps"],
                            )
                        )
            self._entities.append(
                Entity(
                    raw_entity["mnemonic"],
                    raw_entity["name"],
                    raw_entity["state"],
                    raw_entity["statue"],
                    raw_entity["docs"],
                    raw_entity["description"],
                    flags,
                )
            )

        for raw_flag in raw_flags["flags"]:
            self._flags.append(
                Flag(
                    raw_flag["mnemonic"],
                    raw_flag["name"],
                    raw_flag["description"],
                    raw_flag["question"],
                    raw_flag["deps"],
                )
            )

        # order the flags by variance
        # optimal order to minimize the number of questions asked
        self._sort_flags()

    def _sort_flags(self):
        # Create an index mapping for flags based on their mnemonics.
        self._flag_index_mapping = {
            flag.mnemonic: i for i, flag in enumerate(self._flags)
        }

        # Convert entities' flags into binary vectors.
        for entity in self._entities:
            entity_vector = [0] * len(self._flags)
            for flag in entity.flags:
                index = self._flag_index_mapping[flag.mnemonic]
                entity_vector[index] = 1
            self._entity_vector_mapping[entity.mnemonic] = entity_vector

        # Compute the variance for each flag across entities.
        entity_flags_matrix = np.array(list(self._entity_vector_mapping.values()))
        self._flag_variance_matrix = np.var(entity_flags_matrix, axis=0)

        # Sort the flags based on their variance.
        self._sorted_flag_indexes = np.argsort(self._flag_variance_matrix)[::-1]
        self._flags = [self._flags[i] for i in self._sorted_flag_indexes]

    def sort(self):
        # encode the input flags
        input_flag_vector = np.zeros(len(self._flags))
        for flag in self._input_flags:
            flag_index = self._flag_index_mapping[flag]
            input_flag_vector[flag_index] = 1

        # compute the similarity for each entity
        entity_similarities = {}
        for entity, vector in self._entity_vector_mapping.items():
            similarity = cosine_similarity([input_flag_vector], [vector])[0][0]
            entity_similarities[entity] = similarity

        self._entity_similarities = entity_similarities

        # sort the entities based on computed similarities
        self._entities.sort(
            key=lambda entity: entity_similarities[entity.mnemonic], reverse=True
        )

    @property
    def flags(self) -> List[Flag]:
        return self._flags

    @property
    def entities(self) -> List[Entity]:
        return self._entities

    @property
    def input_flags(self) -> List[str]:
        return self._input_flags

    @property
    def similarities(self) -> np.ndarray:
        similarities = [
            self._entity_similarities[entity.mnemonic] for entity in self._entities
        ]
        return np.array(similarities)

    @property
    def top(self) -> Entity:
        return self._entities[0]

    @input_flags.setter
    def input_flags(self, value: List[str]):
        available_flags = set([flag.mnemonic for flag in self._flags])
        extra_flags = set(value) - available_flags
        if extra_flags:
            raise ValueError(
                f"Flags {extra_flags} are not available in the current list of flags."
            )
        self._input_flags = value
        self.sort()
