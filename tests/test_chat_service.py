from langchain_core.language_models.fake_chat_models import FakeListChatModel

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
    assert response.model == "gemma4:12b"
