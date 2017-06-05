package task1;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.charset.CharsetEncoder;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapreduce.Mapper;

import org.apache.hadoop.mapred.Reporter;
import org.apache.hadoop.mapreduce.Mapper.Context;
import org.apache.hadoop.mapreduce.filecache.DistributedCache;


public class Map2 extends Mapper<Object, Text, Text, Text> {

private Text word = new Text(),place=new Text(), upplace=new Text();

public void map(Object key, Text value, Context context) throws IOException, InterruptedException {

//	/United+States/NY/Avon	7	1
//	/United+States/NY/Avon/South+Avon	22	1
	String[] line= value.toString().split("\t");
	
	String ulr=line[0];

	int jud=Integer.parseInt(line[1]);
	if(jud==22){
		String[] res=zhengli(ulr);
		String newkey=res[0];
		String newvalue="22"+"\t"+res[1]+"\t"+line[2];
		place.set(newkey);
		word.set(newvalue);
		context.write(place, word);

//		/United+States/NY/Avon	22	South+Avon	1
	}else{
		place.set(line[0]);
		String newline2="7"+"\t"+line[2];
		word.set(newline2);
		context.write(place, word);}
//	/United+States/NY/Avon	7	1
} 

public String[] zhengli(String a){
String[] placename = a.split("/");
int i=placename.length;
	String placeulr="";					
	for(int j=1;j<=i-2;j++){
		placeulr=placeulr+"/"+placename[j];	
	}
String[] res=new String[2];
res[0]=placeulr;
res[1]=placename[i-1];
	return res;
}

}


