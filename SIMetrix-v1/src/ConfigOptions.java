/**
 * Stores the options specified in the config file provided.
 *
 * @author Annie Louis
 */
public class ConfigOptions
{
    boolean performStemming;
    boolean removeStopWords;
    
    String stopFile;
    String bgCountFile;
    
    String bgIdfUnstemmedFile;
    String bgIdfStemmedFile;
    
    boolean divergence;
    boolean cosine;
    boolean topic;
    boolean summProb;
    
    double topicCutoff;

    /**
     * By default, stemming and stop word removal will be done. All features are computed.
     */
    public ConfigOptions()
    {
	performStemming = true;
	removeStopWords = true;
	
	stopFile = "";
	bgCountFile = "";
	bgIdfUnstemmedFile = "";
	bgIdfStemmedFile = "";
	
	divergence = true;
	cosine = true;
	topic = true;
	summProb = true;

	topicCutoff = 10.0;
    }
}