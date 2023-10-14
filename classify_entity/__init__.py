"""
"""
import json
import numpy as np
from typing import List, Dict
from .entity import Entity
from .flag import Flag


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

    _entities: List[Entity] = []
    _flags: List[Flag] = []
    _flag_index_mapping: Dict[str, int] = {}
    _entity_vector_mapping: Dict[str, List[int]] = {}
    _flag_variance_matrix: np.ndarray = np.array([])
    _sorted_flag_indexes: List[int] = []
    _input_flags: List[str] = []
    _entity_similarity_vector: np.ndarray = np.array([])

    def __init__(self, entities_json_path: str, flags_json_path: str):
        """
        Args:
            entities_json_path (str): Path to the entities JSON file.
            flags_json_path (str): Path to the flags JSON file.
        """
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
                Flag(raw_flag["mnemonic"], raw_flag["name"], raw_flag["description"])
            )

        for i, flag in enumerate(self._flags):
            self._flag_index_mapping[flag.mnemonic] = i

        for i, entity in enumerate(self._entities):
            self._entity_vector_mapping[entity.mnemonic] = [0] * len(self._flags)
            for flag in entity.flags:
                self._entity_vector_mapping[entity.mnemonic][
                    self._flag_index_mapping[flag.mnemonic]
                ] = 1

        # find the ideal order of flags
        entity_flags_matrix = np.array(list(self._entity_vector_mapping.values()))
        self._flag_variance_matrix = np.var(entity_flags_matrix, axis=0)
        self._sorted_flag_indexes = np.argsort(self._flag_variance_matrix)[::-1]

        # sort the flags
        self._flags = [self._flags[i] for i in self._sorted_flag_indexes]

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
    def entity_similarity(self) -> np.ndarray:
        return self._entity_similarity_vector

    @input_flags.setter
    def input_flags(self, value: List[str]):
        self._input_flags = value

        # encode the input flags
        input_flag_indexes = [
            self._flag_index_mapping[flag] for flag in self._input_flags
        ]
        input_flag_vector = [0] * len(self._flags)
        for flag_index in input_flag_indexes:
            input_flag_vector[flag_index] = 1
        input_flag_vector = np.array(input_flag_vector)

        # sort the entities by similarity to the input flags
        entity_flags_matrix = np.array(list(self._entity_vector_mapping.values()))
        self._entity_similarity_vector = np.dot(entity_flags_matrix, input_flag_vector)
        sorted_entity_indexes = np.argsort(self._entity_similarity_vector)[::-1]
        self._entities = [self._entities[i] for i in sorted_entity_indexes]
