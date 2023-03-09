def generate_bot():
    import vk_api
    from vk_api.longpoll import VkLongPoll, VkEventType

    vk_session = vk_api.VkApi(token='YOUR_ACCESS_TOKEN')
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            print(event.user_id)
            vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'Hello, world!'})

    return bot

if (__name__ == "__main__"):
    bot = generate_bot()
    #