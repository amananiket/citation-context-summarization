import java.io.BufferedReader;
import java.io.FileReader;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.File;
import java.util.LinkedList;
import java.util.Hashtable;
import java.util.Enumeration;
import java.text.DecimalFormat;

/**
 * Computes the macro (system-level) scores by averaging a system's score for its summaries to different input
 * documents.
 */
public class AverageScores{
    /**
     * Computes the system-level scores from the per input evaluation scores. 
     * @parameter microfile - name of micro evaluation file created from InputBasedEvaluation
     * @parameter startindex - index of the column in the micro file where feature values begin
     * @parameter endindex - the last column that is a feature value (indices start from 0)
     * @parameter macrofilename - name of output file
     */
    public static void computeAndWriteMacroScores(String microfile, int startindex, int endindex, String macrofilename)  throws java.io.IOException, java.io.FileNotFoundException
    {
	System.out.println("Computing average scores...");
	if(!(new File(microfile)).exists())
	    error("Error creating macro scores: Micro scores file not found: "+microfile);
	Hashtable<String, LinkedList<LinkedList<Double>>> sysidToScores = new Hashtable<String, LinkedList<LinkedList<Double>>>();
	
	BufferedReader br = new BufferedReader(new FileReader(microfile));
	String miline;
	String header = br.readLine(); //first line must be header of micro file
	while((miline = br.readLine())!=null)
	    {
		String toks[] = miline.trim().split("[ ]+");
		String sysid = toks[1];
		LinkedList<Double> featureValues = new LinkedList<Double>();
		for(int x = startindex; x <= endindex; x++)
		    featureValues.add(Double.parseDouble(toks[x]));
		if(sysidToScores.containsKey(sysid))
		    sysidToScores.get(sysid).add(featureValues);
		else
		    {
			LinkedList<LinkedList<Double>> listForDiffInputs = new LinkedList<LinkedList<Double>>();
			listForDiffInputs.add(featureValues);
			sysidToScores.put(sysid, listForDiffInputs);
		    }
	    }
	
	//all scores in memory now
	Enumeration eht = sysidToScores.keys();
	int maxInputs = 0;
	while(eht.hasMoreElements())
	    {
		String sid = (String)eht.nextElement();
		LinkedList<LinkedList<Double>> inplists = sysidToScores.get(sid);
		if(inplists.size() > maxInputs)
		    maxInputs = inplists.size();
	    }
	
	BufferedWriter bw = new BufferedWriter(new FileWriter(macrofilename));
	//write header to macro file
	String headToks[] = header.trim().split("[ ]+");
	bw.write(headToks[1]);
	for(int h = 2; h < headToks.length; h++)
	    {
		if(h >= startindex && h <= endindex)
		    bw.write(" "+"Avg"+headToks[h]);
	    }
	bw.newLine();
		
	System.out.println("Total number of inputs = "+maxInputs);
	Enumeration eh = sysidToScores.keys();
	while(eh.hasMoreElements())
	    {
		String sid = (String)eh.nextElement();
		LinkedList<LinkedList<Double>> ilists = sysidToScores.get(sid);
		if(ilists.size() < maxInputs)
		    System.out.println("Warning: Only "+ilists.size()+" summaries averaged for system "+sid+". Max number of inputs = "+maxInputs);
		String avgFeatures = getAverageValues(ilists);
		bw.write(sid +" "+avgFeatures);
		bw.newLine();
	    }
	bw.close();
	//	System.out.println("Finished computing average feature values.");
    }

    /**
     * Scores for each system are stored as lists one for each input. Calculates 
     * average feature values across all inputs.
     */
    public static String getAverageValues(LinkedList<LinkedList<Double>> diffInpFeatures)
    {
	DecimalFormat df = new DecimalFormat("0.#####");
	double avgValues[] = new double[diffInpFeatures.getFirst().size()];
	for(int inp = 0; inp < diffInpFeatures.size(); inp++)
	    {
		LinkedList<Double> featValues = diffInpFeatures.get(inp);
		for(int feat = 0; feat < featValues.size(); feat++)
		    avgValues[feat] += featValues.get(feat);
	    }
	int numInputs = diffInpFeatures.size();
	String ret = "";
	for(int a = 0; a < avgValues.length; a++)
	    ret += df.format(avgValues[a]/numInputs)+" ";
	return ret.trim();
    }
    
    /** 
     * Print error and exit program
     */
    public static void error(String msg)
    {
	System.out.println("AverageScores.java :  \n");
	System.out.println(msg+"\n\n");
	Runtime cur = Runtime.getRuntime();
	cur.exit(1);
    }
}
	
	
			
		