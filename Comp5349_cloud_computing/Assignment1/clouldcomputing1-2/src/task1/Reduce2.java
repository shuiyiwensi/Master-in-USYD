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
public class Reduce2 extends Reducer<Text, Text, Text, Text> {
	Text result = new Text();
	
	public void reduce(Text key, Iterable<Text> values, 
			Context context
	) throws IOException, InterruptedException {

//		/United+States/NY/Avon	22	South+Avon	1
//		/United+States/NY/Avon	7	1
		String number="0";
		String bestneighbor="";
		int neigbornumber=0;
		for (Text text: values){
			String information=text.toString();
			String[] informations=information.split("\t");
			
			if(informations[0].equals("22")){

					if (Integer.parseInt(informations[2])>neigbornumber){
							bestneighbor=informations[1];
							neigbornumber=Integer.parseInt(informations[2]);}						
			}else{
				number=informations[1];					
				}
		}
		String res="";
		if(neigbornumber!=0){
		res=number+"\t"+bestneighbor+"\t"+String.valueOf(neigbornumber);}
		else{res=number;}	
		result.set(res);
		context.write(key, result);
	}
}
