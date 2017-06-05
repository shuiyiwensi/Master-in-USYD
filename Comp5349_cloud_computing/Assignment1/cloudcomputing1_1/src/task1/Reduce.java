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
		  int[] numberresult={0,0,0,0,0,0,0,0,0,0};
		  String[] tagresult=new String[10];
		  for(String tag:ownerFrequency.keySet()){
			  int num=ownerFrequency.get(tag);
			  for(int i=0;i<10;i++){
				  if(num>=numberresult[i]){
					  for(int j=0;j<9-i;j++){
						  numberresult[9-j]=numberresult[8-j];
						  tagresult[9-j]=tagresult[8-j];
					  }
					  numberresult[i]=num;
					  tagresult[i]=tag;
					  i=9;
				  }
			  }
			  }
		  String a="";
		  for(int i=0;i<10;i++){
			  if(numberresult[i]>0){
				  a=a+"{("+tagresult[i]+":"+numberresult[i]+")}";
				  if(i<9){if(numberresult[i+1]!=0){a=a+"+";}}
			  }
		  }	 
		
		String str=String.valueOf(sum);
		StringBuffer strBuf = new StringBuffer();
		strBuf.append(str+"\t");
			strBuf.append(a);
		String res=strBuf.toString();
		result.set(res);

		context.write(key, result);
	}
}
