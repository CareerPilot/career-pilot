import itertools as it
import json
import os
from typing import Any

import boto3
import docx
from langchain.llms.sagemaker_endpoint import (LLMContentHandler,
                                               SagemakerEndpoint)
from langchain_community.llms import Replicate
from pypdf import PdfReader


def is_local() -> bool:
    return os.environ.get('PROMPT') is not None or os.environ.get('PS1') is not None


def doc_to_text(doc_file_path: str) -> str:
    def item_to_text(tp) -> str:
        if type(tp) == docx.text.paragraph.Paragraph:
            text = tp.text
        elif type(tp) == docx.table.Table:
            g = (s for s, _ in it.groupby(c.text for r in tp.rows for c in r.cells))
            text = "\n".join(filter(None, g))
        else:
            raise ValueError(f"unexpected {type(tp)} object in document")
        return text

    doc = docx.Document(doc_file_path)
    g = (tp for s in doc.sections for tp in s.iter_inner_content())
    text = "\n".join(item_to_text(tp) for tp in g)
    return text


def pdf_to_text(pdf_file_path: str) -> str:
    reader = PdfReader(pdf_file_path)
    text = "\n".join(page.extract_text() for page in reader.pages)
    return text


def get_replicate_llm() -> Any:
    return Replicate(
        model="meta/meta-llama-3-8b-instruct",
        model_kwargs={"temperature": 0.75, "max_length": 1000, "top_p": 1},
    )


def get_llama_llm() -> Any:
    class ContentHandler(LLMContentHandler):
        content_type = "application/json"
        accepts = "application/json"

        def transform_input(self, prompt: str, model_kwargs: dict) -> bytes:
            input_str = json.dumps({"inputs": prompt, "parameters": model_kwargs})
            return input_str.encode("utf-8")

        def transform_output(self, output: bytes) -> str:
            response_json = json.loads(output.read().decode("utf-8"))
            return response_json[0]["generated_text"]

    client = boto3.client("sagemaker-runtime", region_name="us-west-2")
    content_handler = ContentHandler()
    return SagemakerEndpoint(
        endpoint_name="llama-7b-chat-endpoint",
        client=client,
        content_handler=content_handler,
        model_kwargs={"max_new_tokens": 700, "top_p": 0.9, "temperature": 0.6},
        endpoint_kwargs={
            "InferenceComponentName": "jumpstart-dft-meta-textgeneration-l-20240509-19-20240509-190922"
        },
    )


def get_llm() -> Any:
    if is_local():
        return get_replicate_llm()
    else:
        return get_llama_llm()
