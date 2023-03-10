def generate_bot():
    import random
    import vk_api
    from vk_api.longpoll import VkLongPoll, VkEventType

    vk_session = vk_api.VkApi(token='2f8e67fa9b1433144b127ea4e88a9d11df35b1474029f9b1799fa04759e6b91d7bf841c23ac34840d00ec')
    longpoll = VkLongPoll(vk_session)
    def polling():
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                print(event.user_id)
                vk_session.method('messages.send', {'random_id':random.randint(1, 1000000), 'user_id': event.user_id, 'message': 'Hello, world!'})
    def send(message):
        vk_session.method('messages.send', {'random_id':random.randint(1, 1000000), 'user_id': 351463594, 'message': message})

    print("vk bot is ready")
    return {"polling":polling, "send":send}

if (__name__ == "__main__"):
    bot = generate_bot()
    bot["polling"]()