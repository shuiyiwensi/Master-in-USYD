package task1;

import java.io.IOException;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.NullWritable;
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
public class filterreduce extends Reducer<NullWritable, Text, NullWritable, Text> {
	Text result = new Text();
	private int numberofplace;
	private int numberofid;	
	private Text word = new Text(),place=new Text();
	private static ArrayList<String> res=new ArrayList<String>();
	private static ArrayList<Integer> numbers=new ArrayList<Integer>();
	private int K=50;
	public void reduce(NullWritable key, Iterable<Text> values, 
			Context context
	) throws IOException, InterruptedException {

		// create a map to remember the owner frequency
		// keyed on owner id
		for(Text value:values){
		try {
			String line = value.toString();	
			String[] dataArray = line.toString().split("\t"); //split the data into array
			String newline=palceulrtoname(line);
			int number=Integer.parseInt(dataArray[1]);
			int z=findnumber(number,numbers);
			insertlist(z,number,numbers);
			insertlist2(z,newline,res);
			} catch (Exception e) {
			    context.getCounter("TopK", "errorLog").increment(1L);
			}
		}
	    for(int i=0;i<K;i++){
	    	place.set(res.get(i));	    	
	    	word.set(" ");
	    context.write(NullWritable.get(), place);}
	}
	public String palceulrtoname(String a){
		String X="";
		String[] A=a.split("\t");
		String[] name=A[0].replace("+"," ").split("/");
		for(int i=0;i<name.length;i++){
			X=X+name[name.length-1-i];
		if(i<(name.length-2)){X=X+",";}		
		}
		X=X+"\t"+A[1]+"\t"+A[2];
		return X;
	}
	
	
	public int findnumber(int number,ArrayList<Integer> list){
		//System.out.println(number);
		int listlong=list.size();
		if(listlong==0){return 0;}
		else{
		if(number>list.get(0)){return 0;}else{
		if(number<list.get(listlong-1)){return listlong;}else{
		//System.out.println(listlong);
		
		return search(number,0,listlong,list);}}}
	}
	public int search(int number,int a, int b, ArrayList<Integer>list){
		if((b-a)<=1){
				return b;
			}		
		int mid=(a+b)/2;
		if(number==list.get(mid)){
			return mid;
		}else{
			if(number>list.get(mid)){ return search(number,0,mid,list);}
				else{return search(number,mid,b,list);}			
		}			
		}
	public void insertlist(int index,int number, ArrayList<Integer> list){
		
		int size=list.size();
		if(size==0){list.add(number);}else{
			if(size<K){
				list.add(list.get(size-1));
				for(int i=0;i<(size-1-index);i++){
					list.set(size-1-i,list.get(size-2-i));
				}
				list.set(index,number);
				
				
			}else{
		for(int i=0;i<(size-1-index);i++){
			list.set(size-1-i,list.get(size-2-i));
		}
		list.set(index,number);}}
	}
	public void insertlist2(int index,String str, ArrayList<String> list){
	
		int size=list.size();
		if(size==0){list.add(str);}else{
			if(size<K){
				list.add(list.get(size-1));
				for(int i=0;i<(size-1-index);i++){
					list.set(size-1-i,list.get(size-2-i));
				}
				list.set(index,str);
				
				
			}else{
		for(int i=0;i<(size-1-index);i++){
			list.set(size-1-i,list.get(size-2-i));
		}
		list.set(index,str);}}
	}
	
	
}
