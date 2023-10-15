"""
"""

from typing import Dict
import os
import requests
from urllib.parse import urlparse, unquote, ParseResult
from pypdf import PdfReader, PdfWriter


class Form:
    """
    The form class parses a pdf into a dictionary of fields and their inputs.
    It has functionality for filling out and saving forms.
    """

    _url: str
    _docs_dir: str
    _path: str
    _fields: Dict[str, str]
    _reader: PdfReader

    def __init__(
        self,
        url: str,
        docs_dir: str,
    ):
        """
        Args:
            url (str): URL to the form.
        """
        self._url = urlparse(url)
        self._docs_dir = docs_dir

        if not self._url.path.endswith(".pdf"):
            raise ValueError("URL must be a pdf.")
        if not os.path.isdir(self._docs_dir):
            os.mkdir(self._docs_dir)

        self._path = self._download_form()
        self._reader = PdfReader(self._path)
        self._fields = self.parse_form()

    def _download_form(self, url: ParseResult = None) -> str:
        """
        Downloads the form at the given URL and returns the path to the file.
        """
        if url is None:
            url = self._url
        response = requests.get(url.geturl(), stream=True)
        response.raise_for_status()
        filename = unquote(url.path.split("/")[-1])
        filepath = os.path.join(self._docs_dir, filename)
        with open(filepath, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        return filepath

    def parse_form(self) -> Dict[str, str]:
        """
        Parses the form at the given path and returns a dictionary
        of fields and their inputs.
        """
        return self._reader.get_form_text_fields()

    def save(self) -> None:
        """
        Saves the form to the given path.
        """
        writer = PdfWriter(clone_from=self._reader)
        for page in self._reader.pages:
            writer.add_page(page)
        for i, page in enumerate(writer.pages):
            writer.update_page_form_field_values(page, fields=self._fields)

        with open(self._path, "wb") as file:
            writer.write(file)

    @property
    def url(self) -> str:
        """
        Returns the URL of the form.
        """
        return self._url

    @property
    def path(self) -> str:
        """
        Returns the path of the form.
        """
        return self._path

    @property
    def fields(self) -> Dict[str, str]:
        """
        Returns the fields of the form.
        """
        return self._fields

    @fields.setter
    def fields(self, fields: Dict[str, str]) -> None:
        """
        Sets the fields of the form.
        """
        input_keys = set(fields.keys())
        available_keys = set(self._fields.keys())
        extra_keys = input_keys - available_keys
        if extra_keys:
            raise ValueError(f"Invalid fields: {extra_keys}")
        self._fields = fields
