from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.messages import HumanMessage

from app.core.config import get_settings
from app.services.chat import ChatService


def test_chat_service() -> None:
    fake_model = FakeListChatModel(
        responses=["Motor insurance protects vehicles against covered financial losses."]
    )

    service = ChatService(
        chat_model=fake_model,
    )

    response = service.chat("What is motor insurance?")

    assert response.answer == (
        "Motor insurance protects vehicles against covered financial losses."
    )
    assert (response.model == get_settings().ollama_chat_model)

def test_chat_service_invoke() -> None:
    fake_model = FakeListChatModel(
        responses=[
            "Grounded insurance answer."
        ]
    )

    service = ChatService(
        chat_model=fake_model,
    )

    response = service.invoke(
        [
            HumanMessage(
                content="Insurance question"
            )
        ]
    )

    assert response == (
        "Grounded insurance answer."
    )    
