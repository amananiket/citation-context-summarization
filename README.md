# citation-context-summarization
Citation Context based scientific summarization algorithm based on C-LexRank (http://www-personal.umich.edu/~vahed/c-lexrank.html)

## Modified summarization algorithm:
*Available at /summaryModAlgo*

* The dataset is present in summaryModAlgo/contextFiles as {paperID}.txt
* The factoids for the dataset required for evaluation is present in summaryModAlgo/facts as {paperID}.ann
* The log for the runs is present in the file log.txt
* The scripts are present in summaryModAlgo/scripts

### List of features
*For 2 sentences in the citation context S1, S2*

* **1 - Unigrams**<br/>
Cosine similarity using TD-IDF vectorization of unigrams after removing stopwords (stopwords are removed using NLTK corpuses)

* **2 - Bigrams**<br/>
Cosine similarity using TD-IDF vectorization of bigrams without removing stopwords

* **3 - Number of citations**<br/>
sim( S1, S2 ) = min (C(S1), C(S2)) / max (C(S1), C(S2))<br/>
Where, C(Si) = Number of out-citations in the sentence Si

* **4 - POS Tag unigrams**<br/>
Cosine similarity using TD-IDF of unigrams of POS tags after removing stopwords.<br/>

* **5 - POS Tag Bigrams**<br/>
Cosine similarity using TD-IDF of bigrams of POS tags withought removing stopwords.<br/>

* **6 - Bibilographic Coupling**<br/>
sim (S1, S2) = |intersection(outCites(S1), outCites(S2)|/ min ( |outCites(S1)|, |outCites(S2)| )<br/>
Where, <br/>
inCites(Si) = Out-vertices of Si in the citation graph<br/>
intersection(A, B) = set of common elements in A & B<br/>
and |A| = cardinality of list A<br/>

* **7 - Co-citation matrix**<br/>
sim (S1, S2) = |intersection(inCites(S1), inCites(S2)|/ min ( |inCites(S1)|, |inCites(S2)| )<br/>
Where, <br/>
inCites(Si) = In-vertices of Si in the citation graph<br/>

* **8 - Title similarity**<br/>
sim (S1, S2) = Unigram-Similarity(Title(paper1), Title(paper2))<br/>
 
* **9 - Author similarty**<br/>
sim (S1, S2) = |intersection(authors(S1), authors(S2)|/ min ( |authors(S1)|, |authors(S2)| )<br/>
Where,<br/>
authors(Si) = list of authors of Si<br/>

* **10 - Time based similarity**
sim (S1, S2) = max( 0, (1 - abs(year1 - year2)/5))<br/>
Where,<br/>
abs (x) = absolute value of x<br/>
year1 = publication year of S1<br/>
year2 = publication year of S2<br/>



# Running the algorithm

* **Execute the algorithm over the whole dataset and run the pyramid evaluation scheme**

```
python executeAndEvaluate.py <featureIndex> <comments>

```

* **Execute the algorithm over a paper**

```
python executeModAlgo.py <paperID> <featureIndex>

```

* **Output**
* The output summaries are added to summaryModAlgo/modOutput as {paperID}-C-LR.txt
* The pyramid scores can be obtained from the log file at summaryModAlgo/log.txt and summaryModAlgo/pScore.ods






