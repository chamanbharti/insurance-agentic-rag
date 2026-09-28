from fastapi.testclient import TestClient

from app.api.chat import get_chat_service
from app.main import app
from app.models.chat import ChatResponse


class FakeChatService:
    def chat(self, message: str) -> ChatResponse:
        return ChatResponse(
            answer=f"Fake answer for: {message}",
            model="gemma4:12b",
        )


def override_chat_service() -> FakeChatService:
    return FakeChatService()


app.dependency_overrides[get_chat_service] = override_chat_service

client = TestClient(app)


def test_chat_endpoint() -> None:
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "What is motor insurance?",
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "answer": "Fake answer for: What is motor insurance?",
        "model": "gemma4:12b",
    }


def test_chat_rejects_empty_message() -> None:
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "",
        },
    )

    assert response.status_code == 422
