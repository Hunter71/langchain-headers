import os
import pprint
import uuid
from multiprocessing import Process, Manager

import requests
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

HOST = os.environ.get("SERVER_HOST") or "127.0.0.1"
URL = f"http://{HOST}:8000"
REQUEST_TEXT = "Who is Maria Skłodowska-Curie?"
REQUIRED_HEADERS = {
    "X-User-Header": "Coco",
    "X-User-Header2": "Jambo",
}


def use_requests():
    body = {"contents": [{"parts": [{"text": REQUEST_TEXT}], "role": "user"}]}
    resp = requests.post(f"{URL}/v1/models/myModel123", json=body, headers=REQUIRED_HEADERS)
    if resp.status_code >= 400:
        raise Exception(resp.status_code, resp.json())

    result = resp.json()
    pprint.pprint(result)
    return result["candidates"][0]["content"]["parts"][0]["text"]


def _use_langchain(uuid: str, return_dict: dict):
    chat = ChatGoogleGenerativeAI(
        model="gemini-pro",
        client_options={"api_endpoint": URL},
        transport="rest",
        google_api_key="serial",
        additional_headers=REQUIRED_HEADERS,
    )
    message = HumanMessage(content=[{"text": REQUEST_TEXT, "type": "text"}])
    response = chat.invoke([message])
    pprint.pprint(response.dict())
    return_dict[uuid] = response.content


def use_langchain():
    # workaround langchain retry mechanism with simple timeout
    manager = Manager()
    return_dict = manager.dict()
    identifier = str(uuid.uuid4())

    p1 = Process(target=_use_langchain, args=(identifier, return_dict))
    p1.start()
    p1.join(timeout=5)
    p1.terminate()
    if p1.exitcode != 0:
        pprint.pprint("Error: Timeout!")

    return return_dict.get(identifier)


def run():
    pprint.pprint("----------------------------------------------")
    r1= use_requests()
    pprint.pprint("----------------------------------------------")
    r2= use_langchain()
    pprint.pprint("----------------------------------------------")
    assert r1 == r2


if __name__ == "__main__":
    run()
