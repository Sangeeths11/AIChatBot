def getVideoSearchQuery(topic, count=10):
    return """You are a searcher for the best educational content on youtube. 
    Your students wants some helpful resources on "topic": """ + topic + """.

    Recommend """ + str(count) + """ different search queries that he can try on youtube, to find the best possible educational content exactly on the "topic" that he needs help with.
    When you make a recommendation take into consideration, that not every student has the same level and previous knowledge, so provide queries to search for different levels of knowledge from beginner to advanced.
    Additionaly try to find different kinds of explanatory videos like "summary", "tutorial", "introduction", "in-depth", "deep-dive", and so on, the goal is to provide a variety of different content.
    Additionally, try to provide queries that may explain the "topic" from different perspectives, try to interpret the topic and search for what he really wants to know.
    Additionaly if your not sure what the exact topic is, try to give queries for familiar topics, that relate very closely to the one that is searched for.

    return the answers in json format, like specified below:

    {
    "queries": [
            {
                "query": "put your query here"
            },
            {
                "query": "put your query here"
            }
            ...
        ]
    }
        """
        
    
    
def getBestVideosPrompt(topic, videos, count=3):
    return """
    Select the top """ + str(count) + """ videos to learn about """+ topic + """ from the options provided in the Json below.
    Use the "name", "url", "sentimentScore" attributes of each video to determine which three are the best ones.

    If presented to an unknown user, there should be a video for everyone, from beginner to advanced.
    So keep in mind to not only select beginner or only videos that cover advanced topics.

    Return a Json with the same structure as the provided one below, containing your top """ + str(count) + """ videos, starting with the best one.
    Return the modified  json and the modified json only!!!

    The Videos:

    """ +  videos