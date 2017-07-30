#-- Response build helpers --

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - {}".format(title),
            'content': "SessionSpeechlet - {}".format(output)
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

#-- Skills behavior --

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
        add those here
    """

    session_attributes = {}
    card_title = "Welcome to Travel Time"
    speech_ouput = "Welcome to the Alexa Travel Time skill." \
                  "You can ask me how long it will take to get to" \
                  "a place from another in the US."
    reprompt_text = "Please tell me an address, city, or location you want to go to."

    should_end_session = False
    speechlet_response = build_speechlet_response(card_title, speech_output, \
      reprompt_text, should_end_session)

    return build_response(session_attributes, speechlet_response)

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Have a safe trip!"

    should_end_session = True
    speechlet_response = build_speechlet_response(card_title, speech_output, \
      None, should_end_session)

    return build_response({}, speechlet_response)

def get_travel_time_from_session(intent, session):
    #pass
    session_attributes = {}
    card_title = "Travel Time"
    reprompt_text = "Please let me know where you want to go, and " \
                    "I'll let you know how long it will take to get there. " \
                    "For example, ask me how long it will take to get from " \
                    "one address to another."
    should_end_session = False

#-- Events --

def on_session_started(session_started_request, session):
    print "on_session_started requestId={}, sessionId={}" \
    .format(session_started_request['requestId'], session['sessionId'])

def on_launch(launch_request, session):
    print "on_launch requestId={}, sessionId={}" \
    .format(launch_request['requestId'], session['sessionId'])

    return get_welcome_response()

def on_intent(intent_request, session):
    print "on_intent requestId={}, sessionId={}" \
    .format(intent_request['requestId'], sessionId['sessionId'])

    intent = intent_request['intent']
    intent_name = intent['name']

    if intent_name == "GetTravelTime":
        return get_travel_time_from_session(intent, session)
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    print "on_session_ended requestId={}, sessionId={}" \
    .format(session_ended_request['requestId'], session['sessionId'])

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print "event.session.application.applicationId={}" \
    .format(event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']}, event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
