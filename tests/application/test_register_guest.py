from application.use_cases.register_guest import RegisterGuestUseCase


def test_register_guest_success():
    class Repo:
        def __init__(self): self.saved = None
        def save(self, guest): self.saved = guest

    repo = Repo()
    use_case = RegisterGuestUseCase(repo)

    guest = use_case.execute("Test User", "test@example.com", "1234567890", 25)

    assert guest.full_name == "Test User"
    assert repo.saved is not None
