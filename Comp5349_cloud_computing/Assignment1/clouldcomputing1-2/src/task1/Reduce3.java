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
public class Reduce3 extends Reducer<Text, Text, Text, Text> {
	Text result = new Text();
	
	public void reduce(Text key, Iterable<Text> values, 
			Context context
	) throws IOException, InterruptedException {

//		/United+States/NY/Avon	22	South+Avon	1
//		/United+States/NY/Avon	7	1
		Map<String, String> ownerFrequency = new HashMap<String,String>();
		String number="0";
		String bestneighbor="";
		int neigbornumber=0;
		int[] numberresult={0,0,0,0,0,0,0,0,0,0};
		String[] localresult=new String[10];
		String[] neiberresult=new String[10];
		
		for (Text text: values){
			String ownername=text.toString();
			String[] informations=ownername.split("\t");
			String leftinfo="";
			if(informations.length==4){
			leftinfo=informations[2]+":"+informations[3];	}
			else{leftinfo="";}
			int num=Integer.parseInt(informations[1]);
					  for(int i=0;i<10;i++){
						  if(num>=numberresult[i]){
							  for(int j=0;j<9-i;j++){
								  numberresult[9-j]=numberresult[8-j];
								  localresult[9-j]=localresult[8-j];
								  neiberresult[9-j]=neiberresult[8-j];
							  }
							  numberresult[i]=num;
							  localresult[i]=informations[0];
							  neiberresult[i]=leftinfo;
							  i=9;
						  }
					  }					 						
		}
		
		  String a="";
		  for(int i=0;i<10;i++){
			  if(numberresult[i]>0){
				  String loc=localresult[i].replace("+", " ");
				  String nei=neiberresult[i].replace("+"," ");				  
				  a=a+"{("+loc+":"+String.valueOf(numberresult[i])+","+nei+")}";
				  if(i<9){if(numberresult[i+1]!=0){a=a+"+";}}
			  }
		  }	 
		String newkey=key.toString();
		newkey.replace("+", " ");
		result.set(a);
		key.set(newkey);
		context.write(key, result);
	}
}
