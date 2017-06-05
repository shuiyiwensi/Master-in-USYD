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


public class Map3 extends Mapper<Object, Text, Text, Text> {

private Text word = new Text(),place=new Text(), upplace=new Text();

public void map(Object key, Text value, Context context) throws IOException, InterruptedException {


	String[] line= value.toString().split("\t");
	String newvalue="";
	String ulr=line[0];
	newvalue=getlocal(ulr)+"\t";

	for(int i=1;i<line.length;i++){
		newvalue=newvalue+line[i]+"\t";
	}
	String[] placenames=ulr.split("/");
	String newkey=placenames[1];
	place.set(newkey);
	word.set(newvalue);
		context.write(place, word);
//	/United+States/NY/Avon	7	1
} 

public String getlocal(String a){
String[] placename = a.split("/");

String res=placename[placename.length-1];
	return res;
}

}


