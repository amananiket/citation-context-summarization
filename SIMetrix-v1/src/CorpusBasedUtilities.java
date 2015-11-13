import java.util.LinkedList;
import java.io.BufferedReader;
import java.io.FileReader;
import java.util.Hashtable;
import java.io.File;
import java.util.Enumeration;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.text.DecimalFormat;

   /**
    * Class where all processing involving auxiliary data is processed--cosine, computing topic signatures, 
    * storing stopword lists. Contains methods for computing vocabulary distributions and reading already
    * created distributions into memory.
    * @author Annie Louis
    */
public class CorpusBasedUtilities{
	
    LinkedList<String> stopWords = new LinkedList<String>(); //this list will be empty throughout if stopword=N option is specified
    Hashtable<String, Double> wordToIdf = new Hashtable<String, Double>();
    int totalDocs = 0;
    vocabDist backgroundDist;
    boolean stemOption;
   

    /** 
     * Reads in any info files provided 
     * <br> 1. stopword list
     * <br> 2. file with frequency counts of words from a large background corpus (to use for computing topic signatures)
     * <br><br> If stopwords must not be filtered, then the string must be empty "". Similarly for other files if they need not be used.
     */


    public CorpusBasedUtilities(ConfigOptions conf) throws java.io.IOException, java.io.FileNotFoundException
    {
	stemOption = conf.performStemming;  //if true, then all vocabulary distributions--input, summary, background and idf values file are stemmed.
	//System.out.println("stemopt= "+stemOption);
	if(conf.removeStopWords)
	    {
		System.out.println("Reading stopwords from "+ conf.stopFile);
		readStopWords(conf.stopFile);
	    }

	if(conf.topic)
	    {
		System.out.println("Reading background corpus frequency counts "+conf.bgCountFile);
		readBackgroundCorpusCounts(conf.bgCountFile, conf.performStemming);
	    }

	if(conf.cosine)
	    {
		if(conf.performStemming)
		    {
			System.out.println("Reading idf values" + conf.bgIdfStemmedFile);
			readBackgroundIdf(conf.bgIdfStemmedFile);
		    }
		else
		    {
			System.out.println("Reading idf values" + conf.bgIdfUnstemmedFile);
			readBackgroundIdf(conf.bgIdfUnstemmedFile);
		    }
	    }
    }
    
    /**
     * Read the stopwords from file into a list
     */
    public void readStopWords(String filepath) throws java.io.IOException, java.io.FileNotFoundException 
    {
	File stpfile = new File(filepath);
	if(!stpfile.exists())
	    error("Stopword file not found: "+filepath);
	BufferedReader br = new BufferedReader(new FileReader(filepath));
	String line;
	while ((line = br.readLine()) != null) {
	    if(line.trim().equals(""))
	       continue;
	    stopWords.add(line.trim().toLowerCase());
	}
    }
	
    /**
     * Read the idf values from given file 
     */
    public void readBackgroundIdf(String filepath) throws java.io.IOException, java.io.FileNotFoundException 
    {
	File idffile = new File(filepath);
	if(!idffile.exists())
	    error("Idf file not found: "+filepath);
	BufferedReader br = new BufferedReader(new FileReader(filepath));
	totalDocs = Integer.parseInt(br.readLine().trim());
	String line;
	while ((line = br.readLine()) != null) {
	    if(line.trim().equals(""))
	       continue;
	    String toks[] = line.trim().split("[ ]+");
	    String wd = toks[0];
	    double idf = Double.parseDouble(toks[1]);
	    wordToIdf.put(wd, idf);
	}
    }


     /**
     * Read the background corpus frequency counts from given file 
     */
    public void readBackgroundCorpusCounts(String filepath, boolean stem) throws java.io.IOException, java.io.FileNotFoundException 
    {
	File idffile = new File(filepath);
	if(!idffile.exists())
	    error("Idf file not found: "+filepath);
	BufferedReader br = new BufferedReader(new FileReader(filepath));
	String line;
	int totalToks = 0;
	LinkedList<String> words = new LinkedList<String>();
	LinkedList<Integer> freqs = new LinkedList<Integer>(); 
	while ((line = br.readLine()) != null) {
	    if(line.trim().equals(""))
	       continue;
	    String toks[] = line.trim().split("[ ]+");
	    String wd = toks[0];
	    if(stem)
		wd = Stemmer.stem(wd);
	    int count = Integer.parseInt(toks[1]);
	    totalToks += count;

	    //update frequency if word already in list else add as new
	    int indInVocab = words.indexOf(wd);
	    if(indInVocab == -1)
		{
		    words.add(wd);
		    freqs.add(count);
		}
	    else
		{
		    int cur = freqs.get(indInVocab);
		    freqs.set(indInVocab, cur+count);
		}
	}

    	//create aggregated vocabulary dist. Only one entry per stem with frequencies totalled over all words adding to the same stem.
    	backgroundDist = new vocabDist(words, freqs, totalToks);
    }



   

    // /**
    //  * Reads the background corpus frequency counts from file 
    //  */
    // public void readBackgroundCorpus(String filepath) throws java.io.IOException, java.io.FileNotFoundException
    // {
    // 	File bgfile = new File(filepath);
    // 	if(!bgfile.exists())
    // 	    error("Backgound frequency file not found: "+filepath);
    // 	BufferedReader br = new BufferedReader(new FileReader(filepath));
    // 	String line;

    // 	line = br.readLine(); //first line must be total number of documents in the corpus
    // 	try
    // 	    {
    // 		totalDocs = Integer.parseInt(line.trim());
    // 	    }
    // 	catch(NumberFormatException e)
    // 	    {
    // 		error("error in backgroundCorpusFrequency file format! "+filepath+"\n"+"first line of the file must specify the total number of documents in the corpus");
    // 	    }

    // 	Hashtable<String, LinkedList<String>> wordToDocList = new Hashtable<String, LinkedList<String>>();
    // 	int totalTokens = 0;
    // 	LinkedList<String> words = new LinkedList<String>();
    // 	LinkedList<Integer> freqs = new LinkedList<Integer>();
    // 	while((line = br.readLine()) != null) 
    // 	    {
    // 		String toks[] = line.trim().split("[ \t]+");	
    //             String wd = toks[0].toLowerCase();
    // 		if(stopWords.contains(wd))
    // 		    continue;
    // 		int freq = 0;
    // 		LinkedList<String> docsContainingWd = new LinkedList<String>();
    // 		for(int t = 1; t < toks.length; t++)
    // 		    {
    // 			String tt[] = toks[t].split(":");
    // 			docsContainingWd.add(tt[0]);
    // 			freq += Integer.parseInt(tt[1]);
    // 			totalTokens += Integer.parseInt(tt[1]);
    // 		    }
    // 		if(stemOption)
    // 		    wd = Stemmer.stem(wd);
		
    // 		//update frequency if word already in list else add as new
    // 		int indInVocab = words.indexOf(wd);
    // 		if(indInVocab == -1)
    // 		    {
    // 			words.add(wd);
    // 			freqs.add(freq);
    // 		    }
    // 		else
    // 		    {
    // 			int cur = freqs.get(indInVocab);
    // 			freqs.set(indInVocab, cur+freq);
    // 		    }
		
    // 		//update document list in the hashtable for doc frequencies
    // 		if(wordToDocList.containsKey(wd))
    // 		    {
    // 			LinkedList<String> curdoclist = wordToDocList.get(wd);
    // 			for(int nn = 0; nn < docsContainingWd.size(); nn++)
    // 			    {
    // 				if(!curdoclist.contains(docsContainingWd.get(nn)))
    // 				    curdoclist.add(docsContainingWd.get(nn));
    // 			    }
    // 			wordToDocList.put(wd, curdoclist);
    // 		    }
    // 		else
    // 		    wordToDocList.put(wd, docsContainingWd);
    // 	    }
	
    // 	//create aggregated vocabulary dist. Only one entry per stem with frequencies totalled over all words adding to the same stem.
    // 	backgroundDist = new vocabDist(words, freqs, totalTokens);

    // 	//now for every stem, the hashtable contains the doc list for all words that mapped to that stem. Now compute the total number
    // 	//of documents and the idf value
    // 	Enumeration est = wordToDocList.keys();
    // 	while(est.hasMoreElements())
    // 	    {
    // 		String wdnext = (String)est.nextElement();
    // 		LinkedList<String> doclist = wordToDocList.get(wdnext);
    // 		int numdocs = doclist.size();
    // 		double idf = Math.log(totalDocs/((double)numdocs));
    // 		wordToIdf.put(wdnext, idf);
    // 	    }
	
    // 	//check if background counts are okay
    // 	BufferedWriter bgcnts = new BufferedWriter(new FileWriter("bgFreqCounts.stemmed"));
    // 	bgcnts.write((new Integer(backgroundDist.numTokens)).toString());
    // 	bgcnts.newLine();
    // 	for(int d = 0 ; d < backgroundDist.vocabWords.size(); d++)
    // 	    {
    // 		bgcnts.write(backgroundDist.vocabWords.get(d)+" "+backgroundDist.vocabFreq.get(d));
    // 		bgcnts.newLine();
    // 	    }
    // 	bgcnts.close();

    // 	DecimalFormat df = new DecimalFormat("0.0000");
    // 	BufferedWriter bgdocs = new BufferedWriter(new FileWriter("bgIdfValues.stemmed"));
    // 	Enumeration dn = wordToIdf.keys();
    // 	while(dn.hasMoreElements())
    // 	    {
    // 		String str = (String)dn.nextElement();
    // 		double idfval = wordToIdf.get(str);
    // 		bgdocs.write(str+" "+df.format(idfval));
    // 		bgdocs.newLine();
    // 	    }
    // 	bgdocs.close();
    // }


    /**
     * Given a path to a plaintext file (summary or single document input) or multiple files (multidocument input), computes the vocabulary
     * distribution--unique words and and their counts overall in the file/files.
     */ 
    public vocabDist computeVocabulary(String path) throws java.io.IOException, java.io.FileNotFoundException
    {
	File fp = new File(path);
	if(!fp.exists())
	    error("Cannot compute vocbulary for : non-existent file path : "+path);
	Hashtable<String, Integer> counts = new Hashtable<String, Integer>();
	if(fp.isDirectory())
	    {
		String files[] = fp.list();
		for(int f = 0; f < files.length; f++)
		    {
			BufferedReader brf = new BufferedReader(new FileReader(path+File.separator+files[f]));
			String fline;
			while((fline = brf.readLine())!=null)
			    {
				if(fline.trim().equals(""))
				    continue;
				fline = fline.replaceAll("[^A-Za-z0-9 ]", " ");
				String toks[] = fline.trim().split("[ ]+");
				for(int t = 0; t < toks.length; t++)
				    updateCounts(toks[t].toLowerCase(), counts);
			    }
		    }
	    }
	else
	    {
		BufferedReader bx = new BufferedReader(new FileReader(path));
		String ll;
		while((ll = bx.readLine())!=null)
		    {
			if(ll.trim().equals(""))
			    continue;
			ll =ll.replaceAll("[^a-zA-Z0-9 ]", " ");
			String tks[] = ll.trim().split("[ ]+");
			for(int tk = 0 ; tk < tks.length; tk++)
			    updateCounts(tks[tk].toLowerCase(), counts);
		    }
	    }
	LinkedList<String> words = new LinkedList<String>();
	LinkedList<Integer> freq = new LinkedList<Integer>();
	int totalToks = 0;
	Enumeration em = counts.keys();
	while(em.hasMoreElements())
	    {
		String wd = (String)em.nextElement();
		int fr = counts.get(wd);
		words.add(wd);
		freq.add(fr);
		totalToks += fr;
	    }
	// System.out.println(words);
	// System.out.println(freq);
	return new vocabDist(words, freq, totalToks);
    }

    /**
     * Given a new token updates the frequency count of that word in the vocabulary distribution
     */
    public void updateCounts(String word, Hashtable<String, Integer> currCounts)
    {
	if(stopWords.contains(word))
	    return;
	if(stemOption)
	    word = Stemmer.stem(word);
	if(currCounts.containsKey(word))
	    {
		int cur = currCounts.get(word);
		currCounts.put(word, cur+1);
	    }
	else
	    currCounts.put(word, 1);
    }

    
    /**
     * Returns the cosine similarity given two distributions--words and frequency counts.
     * Vector contents are tf weights.
     */
    public double computeTfCosineGivenVocabDists(vocabDist distA, vocabDist distB)
    {
	LinkedList<String> complete = new LinkedList<String>();
	complete.addAll(distA.vocabWords);
	for(int p = 0; p < distB.vocabWords.size(); p++ )
	    {
		if(!complete.contains(distB.vocabWords.get(p)))
		    complete.add(distB.vocabWords.get(p));
	    }
	double vecA[]= new double[complete.size()];
	double vecB[] = new double[complete.size()];
	for(int i = 0;i < complete.size();i++)
	    {
		int indA = distA.vocabWords.indexOf(complete.get(i));
		if(indA != -1)
		    vecA[i] = distA.vocabFreq.get(indA);
		else
		    vecA[i] = 0;
		
		int indB = distB.vocabWords.indexOf(complete.get(i));
		if(indB != -1)
		    vecB[i] = distB.vocabFreq.get(indB);
		else
		    vecB[i] = 0;
	    }
	return computeCosine(vecA, vecB);
    }

    /**
     * Returns the cosine similarity given two distributions of words and frequency counts
     * Vector contents are tf*idf weights
     */
    public double computeTfIdfCosineGivenVocabDists(vocabDist distA, vocabDist distB) 
	{
	    LinkedList<String> complete = new LinkedList<String>();
	    complete.addAll(distA.vocabWords);
	    for(int p = 0; p < distB.vocabWords.size(); p++ )
		{
		    if(!complete.contains(distB.vocabWords.get(p)))
			complete.add(distB.vocabWords.get(p));
		}
	    double vecA[]= new double[complete.size()];
	    double vecB[] = new double[complete.size()];
	    for(int i = 0;i < complete.size();i++)
		{
		    int indA = distA.vocabWords.indexOf(complete.get(i));
		    if(indA != -1)
			vecA[i] = distA.vocabFreq.get(indA);
		    else
			vecA[i] = 0;
		    
		    int indB = distB.vocabWords.indexOf(complete.get(i));
		    if(indB != -1)
			vecB[i] = distB.vocabFreq.get(indB);
		    else
			vecB[i] = 0;
		}
	    // for(int i  = 0; i < complete.size(); i++)
	    // 	{
	    // 	    System.out.println(complete.get(i)+"\t"+vecA[i]+"\t"+vecB[i]);
	    // 	}
	    return multiplyIdfAndGetCosine(complete, vecA, vecB);
	}	
    
    
    /**
     * Function to multiply tf values in given vectors with idf and compute cosine similarity
     * 
     */
    public double multiplyIdfAndGetCosine(LinkedList<String> stringsInVector, double [] tfVecA, double [] tfVecB) 
    {
	double tfidf[][] = new double[2][stringsInVector.size()];
	for (int i = 0; i < stringsInVector.size(); i++) 
	    {
		double idf; 
		if(wordToIdf.containsKey(stringsInVector.get(i)))
		    idf = wordToIdf.get(stringsInVector.get(i));
		else
		    idf = Math.log(totalDocs);
		tfidf[0][i] = tfVecA[i] * idf;
		tfidf[1][i] = tfVecB[i] * idf;
	    }
	return computeCosine(tfidf[0], tfidf[1]);
    }
    
    
    /**
     * Function to perform cosine similarity computation between two vectors
     */
    public double computeCosine(double vecA[], double vecB[]) 
    {
	double dotProd = 0.0;
	double vecAMag = 0.0;
	double vecBMag = 0.0;
	double cosSim = 0.0;
	for(int n = 0; n < vecA.length; n++) 
	    {
		dotProd += vecA[n] * vecB[n];
		vecAMag += vecA[n] * vecA[n];
		vecBMag += vecB[n] * vecB[n];
	    }
	if(dotProd == 0.0)
	    cosSim = 0.0;
	else
	    cosSim = dotProd / (Math.sqrt(vecAMag) * Math.sqrt(vecBMag));
	return cosSim;
    }
		
	
    /**
     * Given a set of words and frequency counts, this function computes the 
     * loglikelihood ratios in comparison with the background corpus supplied.
     * Returns a list of loglikelihood ratios corresponding to each of
     * the words in the given vocabulary distribution.
     */
   public LinkedList<Double> computeLogLikelihoodRatio(vocabDist dist)
    { 
    	LinkedList<Double> chisqValues = new LinkedList<Double>();
    	for(int i =0 ; i< dist.vocabWords.size(); i++)
	    {
	    	double wfreq = dist.vocabFreq.get(i);
	    	int bgIndex = backgroundDist.vocabWords.indexOf(dist.vocabWords.get(i));
	    	double bgfreq;
	    	if(bgIndex == -1)
		    bgfreq = 0.0;
	    	else
		    bgfreq = backgroundDist.vocabFreq.get(bgIndex);
    		double o11 = wfreq;
	    	double o12 = bgfreq;

	        double o21 = (double)dist.numTokens - wfreq;
	        double o22 = (double)backgroundDist.numTokens - bgfreq;
	        double N = o11 + o12 + o21 + o22;
	        double p = (o11 + o12) / N;
	        double p1 = o11 / (o11 + o21);
	        double p2 = o12 / (o12 + o22);
	        double t1, t2, t3, t4, t5, t6;
	        if(p == 0)
	        	t1 = 0.0;
	        else
	        	t1 = Math.log10(p) * (o11 + o12);
	        if(p == 1)
	        	t2 = 0.0;
	        else
	        	t2 = (o21+o22) * Math.log10(1 - p);
	        
	        if(p1 == 0)
	        	t3 = 0.0;
	        else
	        	t3 = o11 * Math.log10(p1);
	        if(p1 == 1)
	        	t4 = 0.0;
	        else
	        	t4 = o21 * Math.log10(1-p1);
	        	
	        if(p2 == 0)
	        	t5 = 0.0;
	        else
	        	t5 = o12 * Math.log10(p2);
	        if(p2 == 1)
	        	t6 = 0.0;
	        else
	        	t6 = o22 * Math.log10(1-p2);
	        
	        double loglik = -2.0 * (t1+ t2 - (t3 + t4 + t5 + t6));
		chisqValues.add(loglik);
	    }
       return chisqValues;
    }


    /**
     * Given a set of words and frequency counts, this function computes the
     * loglikelihood ratios for each word and returns those for which the
     * ratio exceeds the given critical value.
     * A value of 10 corresponds to a confidence level of 0.001 and is the cutoff
     * used for our experiments.
     */
    public LinkedList<String> getTopicSignatures(vocabDist dist, double criticalValue)
    {
	LinkedList<Double> loglikRatios = computeLogLikelihoodRatio(dist);
	LinkedList<String> topicWords = new LinkedList<String>();
	for(int x = 0; x < dist.vocabWords.size(); x++)
	    {
		if(loglikRatios.get(x) > criticalValue)                                    
	        	topicWords.add(dist.vocabWords.get(x));
	    }
	return topicWords;
    }

    
    /** 
     * Clear wordToIdf mappings and stopword lists. No longer needed.
     */
    public void clearAll()
    {
	wordToIdf.clear();
	stopWords.clear();
    }


    /**
     * Print error and exit. 
     */	
    public void error(String msg)
    {
	System.out.println("Error - CorpusBasedUtilities.java\n\n"+msg);
	Runtime cur = Runtime.getRuntime();
	cur.exit(1);
    }

}