#https://rapidapi.com/matchilling/api/chuck-norris?endpoint=581c477be4b0036abc91c750

#['animal', 'career', 'celebrity', 'dev', 'explicit', 'fashion', 'food', 'history', 'money', 'movie', 'music', 'political', 'religion', 'science', 'sport', 'travel']
@chucky_category
Feature: Chuck Norris jokes categories

    @chucky_category
    Scenario: Chuck Norris jokes categories
        Given the chuck norris service contains categories
        When the categories are "animal", "career"
        #Remaining categories: 'celebrity', 'dev', 'explicit', 'fashion', 'food', 'history', 'money', 'movie', 'music', 'political', 'religion', 'science', 'sport', 'travel'
        Then the response is successful
