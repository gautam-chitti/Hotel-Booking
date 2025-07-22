from src.application.interfaces.payment_service import IPaymentService
from src.domain.entities.booking import Booking


class MockPaymentService(IPaymentService):
    def process_payment(self, booking: Booking) -> bool:
        # In real life, you'd integrate with Stripe or Razorpay here.
        print(f"💳 Processing mock payment for Booking: {booking.reference.value}")
        return True
