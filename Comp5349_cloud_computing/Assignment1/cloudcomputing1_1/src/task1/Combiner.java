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
public class Combiner extends Reducer<Text, Text, Text, Text> {
	Text result = new Text();
	
	public void reduce(Text key, Iterable<Text> values, 
			Context context
	) throws IOException, InterruptedException {

		// create a map to remember the owner frequency
		// keyed on owner id
		Map<String, Integer> ownerFrequency = new HashMap<String,Integer>();
		int sum = 0;
		int tagsum=0;
		for (Text text: values){
			String[] sumtag=text.toString().split("\t");
			sum=sum+Integer.parseInt(sumtag[0]);
			// each value may contains several owner's data
			// separated by "," after the combiner
			// dataArray stores ownData in the format of
			// ownerName = freq
			if(sumtag.length==2){
			String[] tags=sumtag[1].toString().split(" ");

			for (int i = 0; i < tags.length; i=i+2){

				try{if(!tags[i].equals("")){
					if (ownerFrequency.containsKey(tags[i])){
						ownerFrequency.put(tags[i], ownerFrequency.get(tags[i]) +Integer.parseInt(tags[i+1]));
						tagsum=tagsum+Integer.parseInt(tags[i+1]);
					}else{
						ownerFrequency.put(tags[i], Integer.parseInt(tags[i+1]));
						tagsum=tagsum+Integer.parseInt(tags[i+1]);
					}}
				}catch (NumberFormatException e){
					System.out.println(text.toString());
				}
			}
		}}
		String str=String.valueOf(sum)+"\t";
		  for(String tag:ownerFrequency.keySet()){	
			  int a=ownerFrequency.get(tag);
			  String A=String.valueOf(a);
			  str=str+tag+" "+A+" ";
			  }		
		  result.set(str);
		context.write(key, result);
	}
}
