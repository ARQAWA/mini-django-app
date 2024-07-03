from fake_useragent import UserAgent  # type: ignore

fake_user_agent = UserAgent(browsers=["safari", "chrome"], os=["ios", "android"])
