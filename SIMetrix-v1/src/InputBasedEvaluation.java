import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.FileWriter;
import java.io.FileReader;
import java.io.File;
import java.util.LinkedList;
import java.text.DecimalFormat;

    /**
     * Main module for evaluation. The main function takes a file containing input summary mappings and returns
     *  evaluation scores for features specified in the config file.
     * @author Annie Louis
     */ 
public class InputBasedEvaluation
{	
    /**
     * Given the vocabulary distributions of an input and its summary and a list of features to compute,
     * the function returns a string containing the values of these features.
     * <br><br> For smoothing KL and JS divergence the following values are assumed for bins and gamma
     * <br> LidStone smoothing: The total possible outcomes ie, words in the vocabulary distribution 
     * are set as 1.5 times the input vocabulary size. The fractional count added to the original count 
     * for each vocabulary item is 0.005.
     */
    public String generateFeatures(vocabDist inputDist, vocabDist summaryDist, LinkedList<String> listOfFeatures, EvalFeatures feat, CorpusBasedUtilities cbu, double topicCutoff) 
    {
	// for smoothing kl and js divergence the following values are assumed for bins and gamma
	// LidStone smoothing:
        // the total possible outcomes ie, words in the vocabulary distribution are set as 1.5 times the input vocabulary size
        // the fractional count added to the original count for each vocabulary item is 0.005
	DecimalFormat myFormatter = new DecimalFormat("0.#####");
	String featString = "";
	if(listOfFeatures.contains("KLInputSummary"))
	    {
		double klarray[] = feat.getKLdivergenceSmoothed(inputDist, summaryDist, 0.005, 1.5 * inputDist.vocabWords.size());
		featString += myFormatter.format(klarray[0])+" "+myFormatter.format(klarray[1])+" ";
		featString += myFormatter.format(feat.getJSDivergence(inputDist, summaryDist))+" ";
		featString += myFormatter.format(feat.getSmoothedJSDivergence(inputDist, summaryDist, 0.005, 1.5 * inputDist.vocabWords.size()))+" ";
	    }	
	if(listOfFeatures.contains("cosineAllWords"))
	    featString += myFormatter.format(cbu.computeTfIdfCosineGivenVocabDists(inputDist, summaryDist))+" ";
	if(listOfFeatures.contains("percentTopicTokens"))    
	    {
		LinkedList<String> inputTopicWords = cbu.getTopicSignatures(inputDist, topicCutoff);  
		String percentTokensTopicWords = myFormatter.format(feat.getPercentTokensThatIsSignTerms(inputTopicWords, summaryDist));
		String fractionTopicWordsCovered = myFormatter.format(feat.getPercentTopicWordsCoveredByGivenDist(inputTopicWords, summaryDist));
		featString += percentTokensTopicWords+" "+fractionTopicWordsCovered+" ";
		LinkedList<Integer> topicWordFrequencies = new LinkedList<Integer>();
		int totalCount = 0;
		for(int tp = 0; tp < inputTopicWords.size(); tp++)
		    {
			int indtopic = inputDist.vocabWords.indexOf(inputTopicWords.get(tp));
			int freq = inputDist.vocabFreq.get(indtopic);
			topicWordFrequencies.add(freq);
			totalCount += freq;
		    }
		vocabDist inputTopicDist = new vocabDist(inputTopicWords, topicWordFrequencies, totalCount);
		String topicOverlap = myFormatter.format(cbu.computeTfIdfCosineGivenVocabDists(inputTopicDist, summaryDist));
		featString += topicOverlap + " ";
	    }
	if(listOfFeatures.contains("unigramProb"))
	    {
		double uniprob = feat.getUnigramProbability(inputDist, summaryDist);
		double multprob = feat.getMultinomialProbability(inputDist, summaryDist);
		featString += myFormatter.format(uniprob)+" "+myFormatter.format(multprob)+" ";
	    }
	return featString.trim();
    }
	

    /** 
     * Reads configuration options as provided in config file argument to main function
     */
    public ConfigOptions readAndStoreConfigOptions(String configFile) throws java.io.IOException, java.io.FileNotFoundException
    {
	ConfigOptions cf = new ConfigOptions();
	BufferedReader bcr = new BufferedReader(new FileReader(configFile));
	String cline;
	
	while((cline = bcr.readLine())!=null)
	    {
		cline = cline.trim();
		if(cline.equals(""))
		    continue;
		if(cline.startsWith("-"))
		    continue;
		if(cline.startsWith("="))
		    continue;
		cline = cline.replaceAll(" ","");
		String clineToks[] = cline.split("[=]");
		if(clineToks[0].equals("performStemming"))
		    {
			if(clineToks[1].equalsIgnoreCase("n"))
			    cf.performStemming = false;
		    }
		if(clineToks[0].equals("removeStopWords"))
		    {
			if(clineToks[1].equalsIgnoreCase("n"))
			    cf.removeStopWords = false;
		    }
		if(clineToks[0].equals("divergence"))
		    {
			if(clineToks[1].equalsIgnoreCase("n"))
			    cf.divergence = false;
		    }
		if(clineToks[0].equals("cosineOverlap"))
		    {
			if(clineToks[1].equalsIgnoreCase("n"))
			    cf.cosine = false;
		    }
		if(clineToks[0].equals("topicWordFeatures"))
		    {
			if(clineToks[1].equalsIgnoreCase("n"))
			    cf.topic = false;
		    }
		if(clineToks[0].equals("frequencyFeatures"))
		    {
			if(clineToks[1].equalsIgnoreCase("n"))
			    cf.summProb = false;
		    }

		if(clineToks[0].equals("stopFilePath"))
		    cf.stopFile = clineToks[1];

		if(clineToks[0].equals("backgroundCorpusFreqCounts"))
		    cf.bgCountFile = clineToks[1];

		if(clineToks[0].equals("backgroundIdfUnstemmed"))
		    cf.bgIdfUnstemmedFile = clineToks[1];
		if(clineToks[0].equals("backgroundIdfStemmed"))
		    cf.bgIdfStemmedFile = clineToks[1];

		if(clineToks[0].equals("topicWordCutoff"))
		    cf.topicCutoff = Double.parseDouble(clineToks[1]);
	    }

	if(cf.removeStopWords)
	    {
		if(cf.stopFile.equals(""))
		    error("Error in config file: must specify file with stopwords for removeStopWords=Y option");				
	    }
	else
	    cf.stopFile = "";

	if(cf.cosine)
	    {
		if(cf.bgIdfUnstemmedFile.equals("") && !cf.performStemming)
		    error("Error in config file: must specify file with idf file (unstemmed) to compute cosine overlap");				

		if(cf.bgIdfStemmedFile.equals("") && cf.performStemming)
		    error("Error in config file: must specify file with idf file (stemmed) to compute cosine overlap");				
	    }

	if(cf.topic)
	    {
		//System.out.println(cf.bgFile);
		if(cf.bgCountFile.equals(""))
		    error("Error in config file: must specify file with background corpus counts to compute topic word based features");		
		if(cf.topicCutoff <= 0.0)
		    error("Topic word cutoff must be greater than zero to be meaningful, default value is 10.0");
	    }

	// if(!(cf.cosine || cf.topic))
	//     {
	// 	cf.bgFile = "";
	// 	cf.topicCutoff = 0.0;
	//     }
	return cf;
    }
		

    /**
     * Computes input and system level scores according to desired features. Takes two command line arguments.
     * <br><br> 1) path to mappings file where each line is of the following format
     * <br> inputid &lt;space&gt; systemid &lt;space&gt; path_to_input_file/files &lt;space&gt; path_to_summary_file
     * <br> 2) path to a file containing configuration settings 
     * <br><br> Creates two files in the same directory as mappings file - mappingsfile.ieval.macro (system level scores--average over test set)
     * and mappingsfile.ieval.micro (input level scores--for each individual input)
     */
    public static void main(String args[]) throws java.io.IOException, java.io.FileNotFoundException
	{
	    InputBasedEvaluation ieval = new InputBasedEvaluation();
	    if(args.length != 2)
		ieval.error("Two arguments - path to file with mappings and path to config file");
	    String mappingsFile = args[0];
	    String configFile = args[1];
	    if(!(new File(mappingsFile)).exists())
		ieval.error("mappings file does not exist: "+ mappingsFile);
	    if(!(new File(configFile)).exists())
		ieval.error("config file does not exist: "+ configFile);
	    
	    String stopFile = "";
	    String bgFile = "";
	    String idfFile = "";
	    ConfigOptions opt = ieval.readAndStoreConfigOptions(configFile);
	    LinkedList<String> featuresToCompute = new LinkedList<String>();
	    if(opt.divergence)
		{
		    featuresToCompute.add("KLInputSummary");
		    featuresToCompute.add("KLSummaryInput");
		    featuresToCompute.add("unsmoothedJSD");
		    featuresToCompute.add("smoothedJSD");
		}
	    if(opt.cosine)
		    featuresToCompute.add("cosineAllWords");
	    if(opt.topic)
		{
		    featuresToCompute.add("percentTopicTokens");
		    featuresToCompute.add("fractionTopicWords");
		    featuresToCompute.add("topicWordOverlap");
		}
	    if(opt.summProb)
		{
		    featuresToCompute.add("unigramProb");
		    featuresToCompute.add("multinomialProb");
		}
	    CorpusBasedUtilities cbu = new CorpusBasedUtilities(opt);
	    EvalFeatures feat = new EvalFeatures();
	    
	    BufferedWriter bwmicro = new BufferedWriter(new FileWriter(mappingsFile+".ieval.micro"));
	    bwmicro.write("inputId sysId");
	    for(int f = 0; f < featuresToCompute.size(); f++)
		bwmicro.write(" "+featuresToCompute.get(f));
	    bwmicro.newLine();
	    
	    BufferedReader bmr = new BufferedReader(new FileReader(mappingsFile));
	    String line;
	    while((line = bmr.readLine())!=null)
		{
		    String toks[] = line.trim().split("[ \t]+");
		    if(toks.length != 4)
			ieval.error("Error in mappings file: "+mappingsFile+"\n must have the format inputid <space> systemid <space> path_to_input_vocabulary_file <space> path_to_summary_vocabulary_file");
		    bwmicro.write(toks[0]+" "+toks[1]+" ");
		    System.out.println("Evaluating summary "+toks[1]+" for input "+toks[0]);
		    vocabDist inputVocabDist = cbu.computeVocabulary(toks[2]);
		    vocabDist summaryVocabDist = cbu.computeVocabulary(toks[3]);
		    String features = ieval.generateFeatures(inputVocabDist, summaryVocabDist, featuresToCompute, feat, cbu, opt.topicCutoff);
		    bwmicro.write(features);
		    bwmicro.newLine();
		}
	    bwmicro.close();

	    //other tables no longer needed
	    cbu.clearAll();

	    //compute average feature values - sys level evaluation
	    int numFeatures = featuresToCompute.size();
	    AverageScores.computeAndWriteMacroScores(mappingsFile+".ieval.micro", 2, numFeatures+1, mappingsFile+".ieval.macro");
	    System.out.println("done");
	}


    /**
     * print error and quit
     */
    public void error(String msg)
    {
	System.out.println("\n\n"+msg+"\n\n");
	Runtime cur = Runtime.getRuntime();
	cur.exit(1);
    }

}

