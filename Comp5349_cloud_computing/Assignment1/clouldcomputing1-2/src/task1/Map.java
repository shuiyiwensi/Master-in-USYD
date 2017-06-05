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


public class Map extends Mapper<Object, Text, Text, Text> {
	public static final String HDFS_STOPWORD_LIST = "/user/wtan4210/place.txt";
	private ArrayList<String> pureplaceidlist=new ArrayList<String>();
	private ArrayList<String> pureidtoplace=new ArrayList<String>();
	static CharsetEncoder asciiEncoder = Charset.forName("US-ASCII").newEncoder();

	private int numberofid;
	
	private void readline(String P) {
		// TODO Auto-generated method stub
System.out.println(P);
String[] placeArray = P.split("\t");
if(placeArray.length==7){
	int jud=Integer.parseInt(placeArray[5]);
	if(jud==22||jud==7){								
	String placedetal=placeArray[6]+"\t"+String.valueOf(jud);
		paixu2(placeArray[0],placedetal,pureplaceidlist,pureidtoplace);
	}
}
	}
public void paixu2(String a,String c,ArrayList<String> b,ArrayList<String> d){
if(numberofid==0){
	b.add(a);
	d.add(c);
	numberofid=numberofid+1;
}else{
haha2(a,0,b.size(),b,d,c);
}}
public void haha2(String a, int i, int j,ArrayList<String> b,ArrayList<String> d,String c){
int mid=(i+j)/2;
if(a.compareTo(b.get(mid))==0){return;}
if(j-i<=1){
	if(a.compareTo(b.get(mid))>0){
		b.add(i+1,a);d.add(i+1,c);numberofid=numberofid+1;return;}else{
			b.add(i,a);d.add(i,c);numberofid=numberofid+1;return;}}
if(a.compareTo(b.get((i+j)/2))<0){haha2(a,i,mid,b,d,c);}
else{haha2(a,mid,j,b,d,c);}
}

public int search(String a,int i, int j, ArrayList<String> b ){
int res;
int mid=(i+j)/2;
if(a.equals(b.get(mid))){res=mid; return res;}
if(j-i<=1){
	if(!(a.equals(b.get(i))||a.equals(b.get(j)))){
		res=-1;return res;}}
if(a.compareTo(b.get((i+j)/2))<0){return search(a,i,mid,b);}
else{return search(a,mid,j,b);}	

}	
	  public void setup(Context context) throws java.io.IOException, InterruptedException{
		    
		      
		      Path[] cacheFiles = DistributedCache.getLocalCacheFiles(context.getConfiguration());
		      if (null != cacheFiles && cacheFiles.length > 0) {		        		          
		            loadStopWords(cacheFiles);		           		        
		      }
		     
		  }

		public void loadStopWords(Path[] cachePath) throws IOException {
		    // note use of regular java.io methods here - this is a local file now
		    BufferedReader wordReader = new BufferedReader(new FileReader(cachePath[0].toString()));
		    try {
		      String line;
		      
		      //this.stopWords = new HashSet<String>();
		      while ((line = wordReader.readLine()) != null) {
		        readline(line);
		      }
		    } finally {
		      wordReader.close();
		    }
		  }





private Text word = new Text(),place=new Text(), upplace=new Text();

public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
	
	String line = value.toString();
	
	String[] dataArray = line.toString().split("\t"); //split the data into array
	if (dataArray.length < 6){ //  record with incomplete data
		return; // don't emit anything
	}

	String ownerString = dataArray[1];
	String placeidString = dataArray[4];
	String placename;
	int result=search(placeidString,0,numberofid,pureplaceidlist);	
	if(result!=-1){
	placename=pureidtoplace.get(result);	
	String[] placedetal=placename.split("\t");
	if(Integer.parseInt(placedetal[1])==22){
		place.set(placename);
		word.set(ownerString);
		context.write(place, word);
		String newplace=zhengli(placename)+"\t"+"7";
		upplace.set(newplace);
		context.write(upplace, word);
		
	}else{
				place.set(placename);
				word.set(ownerString);
				context.write(place, word);}
  }
} 

public String zhengli(String a){
String[] placename = a.split("/");
int i=placename.length;
	String placeulr="";					
	for(int j=1;j<=i-2;j++){
		placeulr=placeulr+"/"+placename[j];	
	}
	return placeulr;
}

}

