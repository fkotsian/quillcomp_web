from django.conf import settings
nlp = settings.SPACY_EN

class Nlp:
    prompt = "Schools should not sell junk food on campus, but "

    def __init__(self, prompt = None, training_sents = None):
        # set up user input
        if prompt is not None and len(prompt) > 0:
            self.prompt = prompt

        if training_sents is not None and isinstance(training_sents, list):
            self.training_sents = training_sents
        else:
            self.training_sents = settings.STUDENT_RESPONSES_BUT


    def print_pos(self, doc):
        for token in doc:
            # tokenize and parse parts of speech
            print("{0}/{1} <---{2}-- {3} {4}".format(
                token.text,
                token.tag_,
                token.dep_,
                token.head.text,
                token.head.tag
            ))

    # match user_sent to a set of training_sents via spaCy
    def similar_sentences(self, user_sent, training_sents, debug = False):
        # TEST 1 - check for similarity to existing responses
        # - useful for Feedback categorization (if have typed feedback)
        # - ended up being able to do statement/evidence/consequence without it
        # - TODO: implement in a similar_sentences endpoint that calls this method

        # parse user input
        user_sent_parsed = nlp(user_sent)

        if debug:
            print_pos(user_sent_parsed)

        similarities = []
        for sent in training_sents:
            parsed_sent = nlp(sent)
            similarities.append(user_sent_parsed.similarity(parsed_sent))

        max_similarity = max(similarities)
        similar_sentence_idx = similarities.index(max_similarity)
        similar_sentence = training_sents[similar_sentence_idx]
        #similar_sentence_parsed = nlp(similar_sentence)

        if debug:
            print("MOST SIMILAR SENTENCE: ", similar_sentence)
            print("STRENGTH OF MATCH (out of 1): ", max_similarity)
            print("Sentence " +  str(similar_sentence_idx))

        # maybe want some filter for minimum match percentage here - > .4, .8?
        return similar_sentence



    # analyze user_sent for statement, feedback, and evidence,
    #   and map result to a feedback
    #   @returns {string} feedback
    def feedback_for_sent(self, user_sent, debug = False):
        # TEST 2 - Analyze sent for statement, evidence, consequence
        # - based on ROOT verb and # of consequent phrases
        # parse user input

        user_sent_parsed = nlp(user_sent)
        print(user_sent_parsed)

        if debug:
            print_pos(user_sent_parsed)

        statement_verb = None
        evidence_verb = None
        consequence_verb = None
        statement_components = []
        evidence_components = []
        consequence_components = []

        # get completion of prompt to ID root verb
        prompt_root_verb = None
        for token in user_sent_parsed:
            if token.dep_ == "ROOT":
               prompt_root_verb = token.text


        # strip prompt text from parsed_completion, while keeping taggings
        # - do not reparse stripped sentence, as will lose taggings/embeddings

        prompt_length = len(self.prompt.split(" "))
        parsed_completion = user_sent_parsed[prompt_length:]        # a better parse would be to remove punctuation from both and then remove len(prompt)-1 elements from the full sent; this guarantees we do not remove extra elements due to punctuation


        if debug:
            parsed_completion_str = map(lambda tok: tok.text, parsed_completion)
            print("SENT TO ANALYZE: " + " ".join(parsed_completion_str))
            print("ROOT VERB: " + prompt_root_verb)

        # scan for statement, evidence, consequence verbs
        # - possibly in 3 diff loops if need be
        for token in parsed_completion:
            # if the ROOT is the main verb, then is providing the counter - has statement
            # - instead of hardcoding prompt_root, can use ROOT
            if (token.tag_ == "VB" or token.tag_ == "VBZ") and token.head.text == prompt_root_verb:
                statement_verb = token.text
            # has an additional verb -- has evidence for statement
            if (token.tag_ == "VB" or token.tag_ == "VBZ") and statement_verb and token.head.text == statement_verb:
                evidence_verb = token.text
            # has an additional verb -- has evidence for statement
            if (token.tag_ == "VB" or token.tag_ == "VBZ") and evidence_verb and token.head.text == evidence_verb:
                consequence_verb = token.text

        # gather statement, evidence, consequence phrases
        for token in parsed_completion:
            # get complete verb clauses/components
            if statement_verb and statement_verb == token.head.text:
                statement_components.append(token.text)
            if evidence_verb and evidence_verb == token.head.text:
                evidence_components.append(token.text)
            if consequence_verb and consequence_verb == token.head.text:
                consequence_components.append(token.text)


        if debug:
            print("Statement Verb: " + str(statement_verb) + ": " + " ".join(statement_components))
            print("Evidence Verb: " + str(evidence_verb) + ": " + " ".join(evidence_components))
            print("Consequence Verb: " + str(consequence_verb) + ": " + " ".join(consequence_components))

            print("STATEMENT POS: " + " ".join(statement_components))
            print("EVIDENCE POS: " + " ".join(evidence_components))
            print("CONSEQUENCE POS: " + " ".join(consequence_components))

            print("Has statement?: " + str(statement_verb is not None))
            print("Has evidence?: " + str(evidence_verb is not None))
            print("Has consequence?: " + str(consequence_verb is not None))


        return {
            'statement': statement_verb is not None,
            'evidence': evidence_verb is not None,
            'consequence': consequence_verb is not None,
        }


    def translated_feedback(self, feedback_dict):
        statement_feedback = None
        evidence_feedback = None
        consequence_feedback = None

        if not feedback_dict['statement']:
            return "Please provide a complete claim. What statement can you make about the prompt?"
        elif not feedback_dict['evidence']:
            return "Good work providing a claim. Can you make it stronger by citing evidence from the text?"
        elif not feedback_dict['consequence']:
            return "Great job making a claim and supporting it with evidence from the passage. Now consider how you can make your evidence stronger. Provide a consequence of your evidence, so the reader can see the consequences of your claim."




    def run(self):
        # references NLP and USER_RESPONSES_BUT from settings.py
        #for sent in training_sents[-9:]:

        #user_sents = [
        #    prompt + "they should offer a healthy option so that kids can have a snack if they get hungry.",
        #    prompt + "some food options would be helpful when hard-working students get hungry.",
        #    prompt + "ok",
        #    prompt + "good food",
        #    prompt + "junk food is still available elsewhere.",
        #    prompt + "students will still need to learn about the negative effects of junk food.",
        #    prompt + "junk food is still available elsewhere, so students will still need to learn about the negative effects of junk food.",
        #]

        #feedback_for_sents = []
        #for user_sent in user_sents:

        user_sent = self.prompt + " they should offer a healthy option so that kids can have a snack if they get hungry."
        current_feedback_dict = self.feedback_for_sent(user_sent)
        current_feedback = self.translated_feedback(current_feedback_dict)

        #feedback_for_sents.append(
        #    [user_sent, current_feedback]
        #)

        #print(feedback_for_sents)
        return current_feedback


    # from this, give feedback -> "You need statement!"
    # -> "You need evidence! Pls support"
    # -> "You need consequence! Pls expand on evidence"
    #
    # NEXT:
    # - run this through a set of sample responses and see how we do
    # THEN:
    # - set this up on a webserver that can run spacy as well as django (any machine will work really - see how fast it is)






    ### OLD NOTES
    # if match then great
    # - yes match -> has similarity and therefore has evidence
    # - no match  -> "please provide evidence!"

    # 2. if similarity then look for consequence
    # -> do SRL
    #   -> Yes evidence is complex w/ causation word or 'because' -> "good job! provides evidence and a consequence"
    #   -> No  evidence has no causation word or simple statement -> "you provided evidence but can you show a consequnece of this? what happens if they don't / why should they let them <cite response - allow kids to bring it from home>?"
    #
