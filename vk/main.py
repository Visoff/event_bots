def generate_bot():
    import random
    import vk_api
    from vk_api.longpoll import VkLongPoll, VkEventType

    vk_session = vk_api.VkApi(token='vk1.a.qg1d1aa9wPKA33tjYnhLKoAJjwE68ZU3v_zmfjyc94fsR2qidnxYOqnsll4PhrFi5_6XhM1_lE4kXHMVTBgzbO-gqcdTz0vGiOdJXspJZktk6FqhI3m-7plotkaKQFaG_lPYbO8U2qUQwKNO0UmxGGLtZtxoE1ubtw12CwJxRT6RzC1LtQ5iyBesV7Cx-MEMeRn3Ta1pDtr2d3x0LBUWXw')
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