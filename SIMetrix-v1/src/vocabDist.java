import java.util.LinkedList;

/**
 * Stores a set of words and their frequency counts. All text is converted into such
 * vocabulary distributions before computing any of the features.
 * @author Annie Louis
 */
public class vocabDist{
    LinkedList<String> vocabWords;
    LinkedList<Integer> vocabFreq;
    int numTokens;

    public vocabDist(LinkedList<String> words, LinkedList<Integer> freq, int tokens)
    {
	vocabWords = words;
	vocabFreq = freq;
	numTokens = tokens;
    }

    public void printStats()
    {
	System.out.println("vocabulary size = "+vocabWords.size());
	System.out.println("total tokens = "+numTokens);
    }
}
    