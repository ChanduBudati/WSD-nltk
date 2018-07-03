# WSD-nltk

Input – Input reads from a file named input.txt (sample file provided) that contains the following
• A single noun word having multiple senses (e.g, bat)
• For each of two selected senses of the noun provide: a) a short tag identifying the sense (e.g., flying
mammal or baseball bat); and b) its WordNet synset (e.g., bat.n.01 or bat.n.05)
• An unspecified number of short sentences to be classified into one of the senses by your disambiguation
method (e.g., The new bat improved her hitting) – You may avoid punctuation if you choose to
• Processing
• Your chosen features for computing a word’s sense should be gathered and applied to the input sentence
• You must use one of the synset similarity measures provided in WordNet
• Your method must be consistent and may not select features based on individual input (i.e, use hyponyms in
some cases but not others)
• Output – The program should output the following:
• The given input sentence and the short tag for its computed sense – Do not use the uninformative
synset tag like bat.n.01. See example below for the proper output format.
