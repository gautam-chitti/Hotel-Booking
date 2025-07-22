from application.use_cases.guest_booking_history import GuestBookingHistoryUseCase


def test_guest_booking_history():
    class Repo:
        def get_by_guest_id(self, guest_id): return ["Booking1", "Booking2"]

    use_case = GuestBookingHistoryUseCase(Repo())
    result = use_case.execute("guest-id")
    assert result == ["Booking1", "Booking2"]
