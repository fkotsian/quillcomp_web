## Challenge

- Use NLP libs and a set of training sentences to provide writing feedback on a student prompt

## Rationale

- Research shows that conjunction use is key to leading to the development of new thought patterns.
- Training students to use AND, OR, BUT, and SO conjunctions can expand their repertoire of thought
- Doing this in an automated fashion without requiring the use of a teacher for reinforcement can have an outsized impact.

## Solution Outline

- parse student prompt
- extract student response
- provide feedback on response according to following model:
  - Statement -> Evidence(s) -> Consequence(s)
  - if any step of the above is missing from the response, detect it and prompt the student to revise their response

## Proof-of-Concept

- uses SpaCy library to parse student prompts, and provides 2 types of feedback:
  1. Matches student sentence to a set of similar training sentences, which already have been matched with feedback, & return this feedback
  2. Parse student sentence for Statement, Evidence, and Consequence, and give feedback according to which parts are needed
    - 
- start with conjunction BUT because is well-studied and have sample response prompts for this

## Results

- Able to build PoC according to both methods 1 & 2
- Used method 1 sentence data as test set for method 2 (543 sentences)
  - Method 2 involves using out-of-the-box parts-of-speech tagging and semantic-role-labeling (subject-verb/noun-adjective/etc matching) to assess whether the sentence contains Statement, Evidence, and Consequence
  - Observed that method 2 came up with the correct feedback level for ~83% of sentences, which is surprisingly high

## Conclusions

- Method 2 (NLP-based parts-of-speech and semantic-role-labeling parsing via the SpaCy library) is quite robust and can possibly be improved with better identification of Statement, Evidence, and Consequence
- Further testing is required to assess performance on more complex sentences, and with other conjunctions beyond BUT
- However, we are quite satisfied that automated derivation of feedback is quite possible based on only existing NLP methods, without need for more complex machine learning at this stage.
