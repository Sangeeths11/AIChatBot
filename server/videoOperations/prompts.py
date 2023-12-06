def getVideoSearchQuery(topic, count=10):
    """
    Generates a list of search queries for a given topic.

    Args:
      topic (str): The topic to generate search queries for.
      count (int, optional): The number of search queries to generate. Defaults to 10.

    Returns:
      str: A JSON string containing the generated search queries.

    Examples:
      >>> getVideoSearchQuery('Python', 5)
      {
        "queries": [
          {
            "query": "Python beginner tutorial"
          },
          {
            "query": "Python advanced tutorial"
          },
          {
            "query": "Python introduction"
          },
          {
            "query": "Python in-depth"
          },
          {
            "query": "Python deep-dive"
          }
        ]
      }
    """
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
    """
    Selects the top videos to learn about a given topic.

    Args:
      topic (str): The topic to select videos for.
      videos (str): A JSON string containing the videos to select from.
      count (int, optional): The number of videos to select. Defaults to 3.

    Returns:
      str: A JSON string containing the selected videos.

    Examples:
      >>> getBestVideosPrompt('Python', '[{"name": "Python Tutorial for Beginners", "watchurl": "www.example.com/python-tutorial-for-beginners", "sentimentScore": 0.9}, {"name": "Python Advanced Tutorial", "watchurl": "www.example.com/python-advanced-tutorial", "sentimentScore": 0.8}]', 2)
      {
        "videos": [
          {
            "name": "Python Tutorial for Beginners",
            "watchurl": "www.example.com/python-tutorial-for-beginners",
            "sentimentScore": 0.9
          },
          {
            "name": "Python Advanced Tutorial",
            "watchurl": "www.example.com/python-advanced-tutorial",
            "sentimentScore": 0.8
          }
        ]
      }
    """
    return """
    Select the top """ + str(count) + """ videos to learn about """+ topic + """ from the options provided in the Json below.
    Use the "name", "watchurl", "sentimentScore" attributes of each video to determine which three are the best ones.

    If presented to an unknown user, there should be a video for everyone, from beginner to advanced.
    So keep in mind to not only select beginner or only videos that cover advanced topics.
    
    Additionally, DO NOT return multiple videos with the same "name" or "url", return a set of """ + str(count) + """ unique videos.

    Return a Json with the same structure as the provided one below, containing your top """ + str(count) + """ videos, starting with the best one.
    Return the modified  json and the modified json only!!!

    VERIFY THAT IT IS VALID JSON!!!
    
    The Videos:

    """ +  videos