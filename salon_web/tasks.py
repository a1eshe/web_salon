from celery import shared_task
from .models import Booking
import telegram

@shared_task
def send_booking_reminder(booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        message = (
            f"Siz {booking.time.strftime('%H:%M')} da "
            f"{booking.service.name} ga {booking.employee.name} ga yozilgansiz.\n"
            "Iltimos, vaqtida keling 😊"
        )

        bot = telegram.Bot(token='7504002144:AAH8e4h6imFXr3GaWFprL8QNEOQwCihvN4I')
        chat_id = booking.customer.telegram_id
        bot.send_message(chat_id=chat_id, text=message)
    except Booking.DoesNotExist:
        print(f"Booking ID {booking_id} not found.")
    except Exception as e:
        print(f"Error in send_booking_reminder task: {e}")
