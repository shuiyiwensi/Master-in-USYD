package task1;

import java.io.IOException;
import java.math.BigDecimal;
import java.util.HashMap;
import java.util.Map;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Reducer.Context;

/**
 * Input record format
 * dog -> {(48889082718@N01=1,48889082718@N01=3,), 423249@N01=4,}
 *
 * Output for the above input key valueList
 * dog -> 48889082718@N01=4,3423249@N01=4,
 * 
 * @see TagSmartMapper
 * @see TagSmartDriver
 * 
 * @author Ying Zhou
 *
 */
public class Reduce extends Reducer<Text, Text, Text, Text> {
	Text result = new Text();
	
	public void reduce(Text key, Iterable<Text> values, 
			Context context
	) throws IOException, InterruptedException {

		// create a map to remember the owner frequency
		// keyed on owner id
		Map<String, Integer> ownerFrequency = new HashMap<String,Integer>();
		for (Text text: values){
			String ownername=text.toString();
				try{
					if (!ownerFrequency.containsKey(ownername)){
						ownerFrequency.put(ownername, 1);
					}
				}catch (NumberFormatException e){
					System.out.println(text.toString());
				}

		}
		int sum=0;
		for(String people:ownerFrequency.keySet()){
			sum=sum+1;
		}
		String res=String.valueOf(sum);
		result.set(res);

		context.write(key, result);
	}
}
