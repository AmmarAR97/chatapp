def calculate_similarity(user1, user2):
    similarity = 0
    try:
        interests1 = user1["interests"]
        interests2 = user2["interests"]
        for interest, score1 in interests1.items():
            if interest in interests2:
                score2 = interests2[interest]
                similarity += abs(score1 - score2)
    except Exception as E:
        print(E)

    return similarity


