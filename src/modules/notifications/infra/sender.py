from dataclasses import dataclass

import httpx

from src.modules.notifications.application.ports.notification_sender import NotificationSender 


@dataclass
class TelegramNotificationSender(NotificationSender):
    bot_token: str
    timeout_seconds: float = 10.0
    
    async def send(
        self, 
        *,
        recipient: str,
        message: str,
    ) -> None:
        if not self.bot_token:
            raise RuntimeError("Telegram bot token is not configured")
        
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        
        payload = {
            "chat_id": recipient,
            "text": message,
        }
        
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await client.post(
                url,
                json=payload,
            )
        
        if response.status_code >= 400:
            raise RuntimeError(
                f"Telegram API error: status={response.status_code}, "
                f"body={response.text}",
            )